from fastapi import status

from src.business_logic.task.exceptions.task import TaskNotFoundError
from src.presentation.api.openapi_responses.common import (
    RESPONSE_TYPE,
    access_denied_response,
)
from src.presentation.api.openapi_responses.generator import generate_example_schema

_task_not_found_by_id_example = {
    "access_denied": {
        "summary": "Task не найден",
        "value": generate_example_schema(TaskNotFoundError(["id"])),
    }
}


delete_task_responses: RESPONSE_TYPE = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {"application/json": {"examples": _task_not_found_by_id_example}},
    },
    status.HTTP_403_FORBIDDEN: access_denied_response,
}

update_task_responses: RESPONSE_TYPE = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {"application/json": {"examples": _task_not_found_by_id_example}},
    },
    status.HTTP_403_FORBIDDEN: access_denied_response,
}
