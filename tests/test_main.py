import pytest

from src.extract import DEFAULT_MONTH, DEFAULT_YEAR
from src.main import parse_args


def test_parse_args_uses_default_period() -> None:
    args = parse_args([])

    assert args.year == DEFAULT_YEAR
    assert args.month == DEFAULT_MONTH


def test_parse_args_accepts_requested_period() -> None:
    args = parse_args(["--year", "2024", "--month", "12"])

    assert args.year == 2024
    assert args.month == 12


@pytest.mark.parametrize("month", ["0", "13"])
def test_parse_args_rejects_invalid_month(month: str) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--month", month])
