import re

from src.business_logic.common.validators import ValidationError, length_validator

# Минимум 8 сиволов, 1 цифра
password_re = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,30}$"

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 25

common_password_validation_error = ValidationError(
    ["password"],
    context_message="""Пароль должен состоять минимум из 8 и максимум из 30 символов,
    содержать в себе 1 цифру""",
)
first_name_length_validation_error = ValidationError(
    ["first_name"],
    context_message="Имя должно состоять минимум из 2 и максимум из 15 символов",
)
last_name_length_validation_error = ValidationError(
    ["last_name"],
    context_message="Фамилия должна состоять минимум из 2 и максимум из 15 символов",
)


def validate_password(password: str) -> None:
    if not re.match(password_re, password):
        raise common_password_validation_error


def validate_first_name(first_name: str) -> None:
    if not length_validator(first_name, NAME_MIN_LENGTH, NAME_MAX_LENGTH):
        raise first_name_length_validation_error


def validate_last_name(last_name: str) -> None:
    if not length_validator(last_name, NAME_MIN_LENGTH, NAME_MAX_LENGTH):
        raise last_name_length_validation_error
