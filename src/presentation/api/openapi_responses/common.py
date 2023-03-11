from typing import Any

from src.business_logic.common.exceptions import AccessDeniedError
from src.presentation.api.openapi_responses.generator import generate_example_schema

RESPONSE_TYPE = dict[int | str, dict[str, Any]]


access_denied_response = {
    "description": "Forbidden",
    "content": {
        "application/json": {
            "examples": {
                "access_denied": {
                    "summary": "Нет доступа",
                    "value": generate_example_schema(AccessDeniedError()),
                }
            }
        }
    },
}
