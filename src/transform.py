from datetime import date
from decimal import Decimal

from src.extract import fetch_uf_data


def transform_uf_record(record: dict) -> dict:
    uf_date = date.fromisoformat(record["Fecha"])

    normalized_value = (
        record["Valor"]
        .replace(".", "")
        .replace(",", ".")
    )
    uf_value = Decimal(normalized_value)

    return {
        "date": uf_date,
        "value": uf_value,
    }


def transform_uf_data(data: dict) -> list[dict]:
    records = data.get("UFs", [])

    return [
        transform_uf_record(record)
        for record in records
    ]


if __name__ == "__main__":
    raw_data = fetch_uf_data()
    transformed_records = transform_uf_data(raw_data)

    print("Cantidad transformada:", len(transformed_records))

    if transformed_records:
        first_record = transformed_records[0]

        print("Primer registro:", first_record)
        print("Tipo de date:", type(first_record["date"]))
        print("Tipo de value:", type(first_record["value"]))