class ApplicationError(Exception):
    pass


class BadJWTTokenError(ApplicationError):
    pass
