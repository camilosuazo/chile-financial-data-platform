import pytest

from src.periods import months_between, parse_period


def test_parse_period_returns_year_and_month() -> None:
    assert parse_period("2024-12") == (2024, 12)


@pytest.mark.parametrize(
    "value",
    ["2024-1", "24-01", "2024/01", "2024-13"],
)
def test_parse_period_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        parse_period(value)


def test_months_between_includes_both_limits() -> None:
    assert months_between((2024, 11), (2025, 2)) == [
        (2024, 11),
        (2024, 12),
        (2025, 1),
        (2025, 2),
    ]


def test_months_between_rejects_reversed_range() -> None:
    with pytest.raises(ValueError, match="inicial"):
        months_between((2025, 1), (2024, 12))
