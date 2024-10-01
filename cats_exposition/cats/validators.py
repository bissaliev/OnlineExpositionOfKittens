import datetime as dt

from django.core.exceptions import ValidationError


def validate_birth_date(value):
    """
    Валидатор проверяет чтобы дата рождения была в диапазоне
    от today - 40 year and today.
    """
    today = dt.date.today()
    if not (today - dt.timedelta(days=365 * 40) < value <= today):
        raise ValidationError("Проверьте дату рождения!")
