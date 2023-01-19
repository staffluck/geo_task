from src.business_logic.common.exceptions import ApplicationError


class AuthError(ApplicationError):
    message = "Ошибка во время аутентификации"
    status = 401


class BadCredentialsError(AuthError):
    ...
