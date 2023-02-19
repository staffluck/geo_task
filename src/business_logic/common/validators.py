from src.business_logic.common.exceptions import FieldBasedError


class ValidationError(FieldBasedError):
    message = "Ошибка при валидации значений"


def length_validator(obj: str, min: int, max: int) -> bool:
    length = len(obj)
    if length > max or length < min:
        return False
    return True
