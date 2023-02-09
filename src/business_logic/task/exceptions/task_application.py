from src.business_logic.common.exceptions import (
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


class TaskApplicationAlreadyExistsError(ObjectAlreadyExistsError):
    ...


class TaskApplicationNotFoundError(ObjectNotFoundError):
    ...
