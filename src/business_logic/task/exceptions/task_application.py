from src.business_logic.common.exceptions import (
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


class TaskApplicationAlreadyExistsError(ObjectAlreadyExistsError):
    context_message = "Пользователь уже отправил отклик на данное задание"


class TaskApplicationNotFoundError(ObjectNotFoundError):
    ...


class TaskApplicationByOwnerError(ApplicationError):
    message = "Пользователь не может откликнуться на своё задание"
