from src.business_logic.common.exceptions import FieldBasedError


class ValidationError(FieldBasedError):
    message = "Ошибка при валидации значений"
