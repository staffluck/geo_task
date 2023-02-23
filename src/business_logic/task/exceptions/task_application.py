from src.business_logic.common.exceptions import (
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


class TaskApplicationAlreadyExistsError(ObjectAlreadyExistsError):
    context_message = "Пользователь уже отправил отклик на данное задание"


class TaskApplicationNotFoundError(ObjectNotFoundError):
    ...
