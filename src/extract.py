import requests

from config import get_cmf_api_key


CMF_UF_URL = (
    "https://api.cmfchile.cl/"
    "api-sbifv3/recursos_api/uf/2025/01"
)


def fetch_uf_data() -> dict:
    api_key = get_cmf_api_key()

    params = {
        "apikey": api_key,
        "formato": "json",
    }

    try:
        response = requests.get(
            CMF_UF_URL,
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
