from datetime import date


def calculating_age_in_months(date: date) -> int:
    """Функция вычисляет возраст в месяцах."""
    today = date.today()
    years_diff = today.year - date.year
    months_diff = today.month - date.month
    total_month = years_diff * 12 + months_diff
    if today.day < date.day:
        total_month -= 1
    return total_month
