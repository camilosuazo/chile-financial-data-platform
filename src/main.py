import argparse
import sys

from src.database import insert_uf_records
from src.extract import DEFAULT_MONTH, DEFAULT_YEAR, fetch_uf_data
from src.transform import transform_uf_data


def positive_year(value: str) -> int:
    year = int(value)

    if year < 1:
        raise argparse.ArgumentTypeError(
            "el año debe ser mayor que cero"
        )

    return year


def parse_args(
    args: list[str] | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Carga valores mensuales de la UF desde la CMF"
    )
    parser.add_argument(
        "--year",
        type=positive_year,
        default=DEFAULT_YEAR,
        help=f"año que se cargará (por defecto: {DEFAULT_YEAR})",
    )
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        default=DEFAULT_MONTH,
        metavar="1-12",
        help=f"mes que se cargará (por defecto: {DEFAULT_MONTH})",
    )

    return parser.parse_args(args)


def run_pipeline(year: int, month: int) -> None:
    print(f"Iniciando pipeline de la UF para {year}-{month:02d}")

    raw_data = fetch_uf_data(year, month)
    print("Extracción completada")

    transformed_records = transform_uf_data(raw_data)
    print(
        "Registros transformados:",
        len(transformed_records),
    )

    inserted_count = insert_uf_records(
        transformed_records
    )
    skipped_count = (
        len(transformed_records) - inserted_count
    )

    print("Registros insertados:", inserted_count)
    print("Registros omitidos:", skipped_count)
    print("Pipeline finalizado correctamente")


if __name__ == "__main__":
    arguments = parse_args()

    try:
        run_pipeline(arguments.year, arguments.month)
    except RuntimeError as error:
        print(
            f"El pipeline falló: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)
