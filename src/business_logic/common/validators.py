from src.business_logic.common.exceptions import FieldBasedError


class ValidationError(FieldBasedError):
    message = "Ошибка при валидации значений"


def length_validator(obj: str, min_: int, max_: int) -> bool:
    length = len(obj)
    if length > max_ or length < min_:
        return False
    return True
