import pytest

from src import main
from src.extract import DEFAULT_MONTH, DEFAULT_YEAR
from src.main import parse_args


def test_parse_args_uses_default_period() -> None:
    args = parse_args([])

    assert args.year == DEFAULT_YEAR
    assert args.month == DEFAULT_MONTH
    assert args.periods == [(DEFAULT_YEAR, DEFAULT_MONTH)]


def test_parse_args_accepts_requested_period() -> None:
    args = parse_args(["--year", "2024", "--month", "12"])

    assert args.year == 2024
    assert args.month == 12
    assert args.periods == [(2024, 12)]


def test_parse_args_accepts_historical_range() -> None:
    args = parse_args(
        [
            "--from-period",
            "2024-11",
            "--to-period",
            "2025-01",
        ]
    )

    assert args.periods == [
        (2024, 11),
        (2024, 12),
        (2025, 1),
    ]


@pytest.mark.parametrize("month", ["0", "13"])
def test_parse_args_rejects_invalid_month(month: str) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--month", month])


def test_parse_args_requires_both_range_limits() -> None:
    with pytest.raises(SystemExit):
        parse_args(["--from-period", "2024-01"])


def test_parse_args_rejects_mixed_period_options() -> None:
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--year",
                "2024",
                "--from-period",
                "2024-01",
                "--to-period",
                "2024-02",
            ]
        )


def test_parse_args_rejects_reversed_range() -> None:
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--from-period",
                "2025-01",
                "--to-period",
                "2024-12",
            ]
        )


def test_run_pipeline_processes_every_period(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_periods = []
    inserted_batches = []

    def fake_fetch(year: int, month: int) -> dict:
        requested_periods.append((year, month))
        return {"UFs": [{"period": (year, month)}]}

    def fake_transform(data: dict) -> list[dict]:
        return data["UFs"]

    def fake_insert(records: list[dict]) -> int:
        inserted_batches.append(records)
        return len(records)

    monkeypatch.setattr(main, "fetch_uf_data", fake_fetch)
    monkeypatch.setattr(main, "transform_uf_data", fake_transform)
    monkeypatch.setattr(main, "insert_uf_records", fake_insert)

    main.run_pipeline([(2024, 11), (2024, 12)])

    assert requested_periods == [(2024, 11), (2024, 12)]
    assert len(inserted_batches) == 2
