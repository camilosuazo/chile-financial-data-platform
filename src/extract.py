import requests

from src.config import get_cmf_api_key


CMF_UF_BASE_URL = (
    "https://api.cmfchile.cl/"
    "api-sbifv3/recursos_api/uf"
)
DEFAULT_YEAR = 2025
DEFAULT_MONTH = 1


def build_uf_url(year: int, month: int) -> str:
    if year < 1:
        raise ValueError("El año debe ser mayor que cero")

    if month not in range(1, 13):
        raise ValueError("El mes debe estar entre 1 y 12")

    return f"{CMF_UF_BASE_URL}/{year:04d}/{month:02d}"


def fetch_uf_data(
    year: int = DEFAULT_YEAR,
    month: int = DEFAULT_MONTH,
) -> dict:
    api_key = get_cmf_api_key()
    url = build_uf_url(year, month)

    params = {
        "apikey": api_key,
        "formato": "json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )
    except requests.RequestException:
        raise RuntimeError(
            "No fue posible conectarse a la API de la CMF"
        ) from None

    if response.status_code != 200:
        raise RuntimeError(
            f"La API respondió con estado HTTP {response.status_code}"
        )

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError(
            "La API no entregó una respuesta JSON válida"
        ) from None


if __name__ == "__main__":
    data = fetch_uf_data()

    print("Tipo de dato recibido:", type(data))
    print("Claves principales:", data.keys())

    uf_records = data.get("UFs", [])

    print("Cantidad de registros:", len(uf_records))

    if uf_records:
        print("Primer registro:", uf_records[0])
