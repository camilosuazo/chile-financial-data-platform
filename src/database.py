import psycopg

from src.config import get_database_config


INSERT_UF_SQL = """
    INSERT INTO uf_values (
        observation_date,
        value
    )
    VALUES (%s, %s)
    ON CONFLICT (observation_date) DO NOTHING;
"""


def check_database_connection() -> tuple:
    database_config = get_database_config()

    try:
        with psycopg.connect(**database_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT current_database(), current_user;"
                )

                return cursor.fetchone()

    except psycopg.Error:
        raise RuntimeError(
            "No fue posible conectarse a PostgreSQL"
        ) from None


def insert_uf_records(records: list[dict]) -> int:
    if not records:
        return 0

    database_config = get_database_config()

    values = [
        (
            record["date"],
            record["value"],
        )
        for record in records
    ]

    try:
        with psycopg.connect(**database_config) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    INSERT_UF_SQL,
                    values,
                )

                return cursor.rowcount

    except psycopg.Error:
        raise RuntimeError(
            "No fue posible insertar los registros de la UF"
        ) from None


if __name__ == "__main__":
    database_name, database_user = check_database_connection()

    print("Conexión a PostgreSQL exitosa")
    print("Base de datos:", database_name)
    print("Usuario:", database_user)