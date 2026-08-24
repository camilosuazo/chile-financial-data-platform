import os

from dotenv import load_dotenv


def get_required_env(variable_name: str) -> str:
    value = os.getenv(variable_name)

    if not value:
        raise RuntimeError(
            f"No se encontró {variable_name} en el archivo .env"
        )

    return value


def get_cmf_api_key() -> str:
    load_dotenv()

    return get_required_env("CMF_API_KEY")


def get_database_config() -> dict:
    load_dotenv()

    db_name = get_required_env("DB_NAME")
    db_user = get_required_env("DB_USER")
    db_host = get_required_env("DB_HOST")
    db_port = get_required_env("DB_PORT")

    try:
        db_port = int(db_port)
    except ValueError:
        raise RuntimeError(
            "DB_PORT debe ser un número entero"
        ) from None

    return {
        "dbname": db_name,
        "user": db_user,
        "host": db_host,
        "port": db_port,
    }


if __name__ == "__main__":
    get_cmf_api_key()
    get_database_config()

    print("Configuración cargada correctamente")