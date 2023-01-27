from src.business_logic.common.exceptions import (
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


class UserAlreadyExistsError(ObjectAlreadyExistsError):
    ...


class UserNotFoundError(ObjectNotFoundError):
    ...
