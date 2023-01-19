from src.business_logic.common.exceptions import ApplicationError


class BadCredentialsError(ApplicationError):
    message = "Не найден аккаунт с переданным email/password"
    status = 401
