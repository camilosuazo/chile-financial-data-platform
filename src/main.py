import argparse
import sys

from src.database import insert_uf_records
from src.extract import DEFAULT_MONTH, DEFAULT_YEAR, fetch_uf_data
from src.periods import Period, months_between, parse_period
from src.transform import transform_uf_data


def positive_year(value: str) -> int:
    year = int(value)

    if year < 1:
        raise argparse.ArgumentTypeError(
            "el año debe ser mayor que cero"
        )

    return year


def period_argument(value: str) -> Period:
    try:
        return parse_period(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from None


def parse_args(
    args: list[str] | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Carga valores mensuales de la UF desde la CMF"
    )
    parser.add_argument(
        "--year",
        type=positive_year,
        default=None,
        help=f"año que se cargará (por defecto: {DEFAULT_YEAR})",
    )
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        default=None,
        metavar="1-12",
        help=f"mes que se cargará (por defecto: {DEFAULT_MONTH})",
    )
    parser.add_argument(
        "--from-period",
        type=period_argument,
        default=None,
        metavar="YYYY-MM",
        help="primer mes de una carga histórica",
    )
    parser.add_argument(
        "--to-period",
        type=period_argument,
        default=None,
        metavar="YYYY-MM",
        help="último mes de una carga histórica",
    )

    parsed_args = parser.parse_args(args)
    single_period_requested = (
        parsed_args.year is not None
        or parsed_args.month is not None
    )
    range_requested = (
        parsed_args.from_period is not None
        or parsed_args.to_period is not None
    )

    if single_period_requested and range_requested:
        parser.error(
            "--year/--month no se pueden combinar con "
            "--from-period/--to-period"
        )

    if range_requested:
        if (
            parsed_args.from_period is None
            or parsed_args.to_period is None
        ):
            parser.error(
                "--from-period y --to-period deben usarse juntos"
            )

        try:
            parsed_args.periods = months_between(
                parsed_args.from_period,
                parsed_args.to_period,
            )
        except ValueError as error:
            parser.error(str(error))
    else:
        parsed_args.year = parsed_args.year or DEFAULT_YEAR
        parsed_args.month = parsed_args.month or DEFAULT_MONTH
        parsed_args.periods = [
            (parsed_args.year, parsed_args.month)
        ]

    return parsed_args


def run_pipeline(periods: list[Period]) -> None:
    total_transformed = 0
    total_inserted = 0

    print(
        "Iniciando pipeline de la UF para",
        len(periods),
        "período(s)",
    )

    for year, month in periods:
        print(f"Procesando {year}-{month:02d}")

        raw_data = fetch_uf_data(year, month)
        transformed_records = transform_uf_data(raw_data)
        inserted_count = insert_uf_records(
            transformed_records
        )

        transformed_count = len(transformed_records)
        skipped_count = transformed_count - inserted_count
        total_transformed += transformed_count
        total_inserted += inserted_count

        print("  Transformados:", transformed_count)
        print("  Insertados:", inserted_count)
        print("  Omitidos:", skipped_count)

    total_skipped = total_transformed - total_inserted
    print("Resumen de la ejecución")
    print("Registros transformados:", total_transformed)
    print("Registros insertados:", total_inserted)
    print("Registros omitidos:", total_skipped)
    print("Pipeline finalizado correctamente")


if __name__ == "__main__":
    arguments = parse_args()

    try:
        run_pipeline(arguments.periods)
    except RuntimeError as error:
        print(
            f"El pipeline falló: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
