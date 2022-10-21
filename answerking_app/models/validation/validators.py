import re
import typing

from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


def validate_positive_number(value: typing.Any) -> int:
    try:
        cast_value_as_int: int = int(value)
        if value < 0 or value > 2147483647:
            raise ValidationError(f"'{value}' is not a valid positive number")
        return cast_value_as_int
    except ValueError:
        raise ValidationError(f"'{value}' is not a valid positive number")


def validate_price(value: typing.Any) -> Decimal:
    try:
        cast_value_as_decimal: Decimal = Decimal(round(value, 2))
        if value < 0:
            raise ValidationError(f"'{value}' is not a valid positive number")
        return cast_value_as_decimal
    except InvalidOperation:
        raise ValidationError(f"'{value}' is not a valid price")


def validate_name_string(value: str | None) -> str:
    if not value or len(value) > 50:
        raise ValidationError(f"'{value}' cannot be empty or more than 50 characters")

    if not re.match("^[a-zA-Z !]+$", value):
        raise ValidationError(f"'{value}' contains invalid characters")

    return_value: str = re.sub(" +", " ", value)

    return return_value


def validate_descriptive_string(value: str | None) -> str | None:
    if not value:
        return value

    if len(value) > 200:
        raise ValidationError(f"'{value}' cannot be more than 200 characters")

    if not re.match("^[a-zA-Z .!,#]+$", value):
        raise ValidationError(f"'{value}' contains invalid characters")

    return_value: str = re.sub(" +", " ", value)

    return return_value


def validate_address_string(value: str | None) -> str:
    if not value or len(value) > 200:
        raise ValidationError(f"'{value}' cannot be empty or more than 200 characters")

    if not re.match("^[a-zA-Z0-9 ,-]+$", value):
        raise ValidationError("Contains invalid characters")

    return_value: str = re.sub(" +", " ", value)

    return return_value
