from src.business_logic.common.exceptions import ApplicationError


class AuthError(ApplicationError):
    message = "Ошибка во время аутентификации"


class BadCredentialsError(AuthError):
    message = "Переданные email/password не совпадают"
    ...
