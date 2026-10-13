import pytest

from src import extract
from src.extract import build_uf_url


def test_build_uf_url_formats_year_and_month() -> None:
    url = build_uf_url(2025, 1)

    assert url.endswith("/uf/2025/01")


@pytest.mark.parametrize("month", [0, 13])
def test_build_uf_url_rejects_invalid_month(month: int) -> None:
    with pytest.raises(ValueError, match="mes"):
        build_uf_url(2025, month)


def test_build_uf_url_rejects_invalid_year() -> None:
    with pytest.raises(ValueError, match="año"):
        build_uf_url(0, 1)


def test_fetch_uf_data_requests_the_selected_period(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request_data = {}

    class FakeResponse:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {"UFs": []}

    def fake_get(
        url: str,
        params: dict,
        timeout: int,
    ) -> FakeResponse:
        request_data.update(
            url=url,
            params=params,
            timeout=timeout,
        )
        return FakeResponse()

    monkeypatch.setattr(
        extract,
        "get_cmf_api_key",
        lambda: "test-api-key",
    )
    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.fetch_uf_data(2024, 12)

    assert result == {"UFs": []}
    assert request_data == {
        "url": f"{extract.CMF_UF_BASE_URL}/2024/12",
        "params": {
            "apikey": "test-api-key",
            "formato": "json",
        },
        "timeout": 10,
    }
