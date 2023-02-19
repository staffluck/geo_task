import re

from src.business_logic.common.validators import ValidationError

# Минимум 8 сиволов, 1 цифра
password_re = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

common_password_validation_error = ValidationError(
    ["password"],
    context_message="Пароль должен состоять минимум из 8 символов, содержать в себе 1 цифру",
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
    length = len(first_name)
    if length > 15 or length <= 1:
        raise first_name_length_validation_error


def validate_last_name(last_name: str) -> None:
    length = len(last_name)
    if length > 15 or length <= 1:
        raise last_name_length_validation_error
