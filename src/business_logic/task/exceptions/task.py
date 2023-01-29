from src.business_logic.common.exceptions import (
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


class TaskAlreadyExistsError(ObjectAlreadyExistsError):
    ...


class TaskNotFoundError(ObjectNotFoundError):
    ...
