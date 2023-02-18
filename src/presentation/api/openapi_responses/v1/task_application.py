from fastapi import status

from src.presentation.api.openapi_responses.common import (
    RESPONSE_TYPE,
    access_denied_response,
)
from src.presentation.api.openapi_responses.v1.task import _task_not_found_by_id_example

add_application_reponses: RESPONSE_TYPE = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {"application/json": {"examples": _task_not_found_by_id_example}},
    },
    status.HTTP_403_FORBIDDEN: access_denied_response,
}
