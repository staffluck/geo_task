from src.business_logic.common.validators import ValidationError, length_validator

TITLE_MIN_LENGTH = 10
TITLE_MAX_LENGTH = 80
DESCRIPTION_MIN_LENGTH = 20
DESCRIPTION_MAX_LENGTH = 300
title_length_validation_error = ValidationError(
    ["title"],
    context_message="Название задания должно состоять минимум из 10 и максимум из 80 символов",
)
description_length_validation_error = ValidationError(
    ["title"],
    context_message="Описание задания должно состоять минимум из 20 и максимум из 300 символов",
)


def validate_title(title: str) -> None:
    if not length_validator(title, TITLE_MIN_LENGTH, TITLE_MAX_LENGTH):
        raise title_length_validation_error


def validate_description(description: str) -> None:
    if not length_validator(description, DESCRIPTION_MIN_LENGTH, DESCRIPTION_MAX_LENGTH):
        raise title_length_validation_error
