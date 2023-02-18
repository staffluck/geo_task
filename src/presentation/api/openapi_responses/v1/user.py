from fastapi import status

from src.business_logic.user.exceptions.auth import BadCredentialsError
from src.business_logic.user.exceptions.user import UserAlreadyExistsError
from src.presentation.api.openapi_responses.common import RESPONSE_TYPE
from src.presentation.api.openapi_responses.generator import generate_example_schema

signup_responses: RESPONSE_TYPE = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "unique_constaint_failed": {
                        "summary": "Нарушена уникальность полей",
                        "value": generate_example_schema(
                            UserAlreadyExistsError(["email"])
                        ),
                    }
                }
            }
        },
    }
}

signin_responses: RESPONSE_TYPE = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "unique_constaint_failed": {
                        "summary": "Неверные данные",
                        "value": generate_example_schema(BadCredentialsError()),
                    }
                }
            }
        },
    }
}
