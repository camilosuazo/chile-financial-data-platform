import sys

from src.database import insert_uf_records
from src.extract import fetch_uf_data
from src.transform import transform_uf_data


def run_pipeline() -> None:
    print("Iniciando pipeline de la UF")

    raw_data = fetch_uf_data()
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
    try:
        run_pipeline()
    except RuntimeError as error:
        print(
            f"El pipeline falló: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)