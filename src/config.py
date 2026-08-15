import os

from dotenv import load_dotenv


def get_cmf_api_key() -> str:
    load_dotenv()

    api_key = os.getenv("CMF_API_KEY")

    if not api_key:
        raise RuntimeError("No se encontró CMF_API_KEY en el archivo .env")

    return api_key


if __name__ == "__main__":
    get_cmf_api_key()
    print("Configuración cargada correctamente")

