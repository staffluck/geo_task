import re

from src.business_logic.user.validators.common import ValidationError

# Минимум 8 сиволов, 1 цифра
password_re = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

common_password_validation_error = ValidationError(
    ["password"],
    context_message="Пароль должен состоять минимум из 8 символов, содержать в себе 1 цифру",
)


def validate_password(password: str) -> None:
    if not re.match(password_re, password):
        raise common_password_validation_error
