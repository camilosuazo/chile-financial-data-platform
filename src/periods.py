Period = tuple[int, int]


def parse_period(value: str) -> Period:
    parts = value.split("-")

    if (
        len(parts) != 2
        or len(parts[0]) != 4
        or len(parts[1]) != 2
        or not all(part.isdigit() for part in parts)
    ):
        raise ValueError("el período debe usar el formato YYYY-MM")

    year, month = map(int, parts)

    if year < 1:
        raise ValueError("el año debe ser mayor que cero")

    if month not in range(1, 13):
        raise ValueError("el mes debe estar entre 01 y 12")

    return year, month


def months_between(start: Period, end: Period) -> list[Period]:
    start_index = start[0] * 12 + start[1] - 1
    end_index = end[0] * 12 + end[1] - 1

    if start_index > end_index:
        raise ValueError(
            "el período inicial no puede ser posterior al final"
        )

    periods = []

    for month_index in range(start_index, end_index + 1):
        year, zero_based_month = divmod(month_index, 12)
        periods.append((year, zero_based_month + 1))

    return periods
