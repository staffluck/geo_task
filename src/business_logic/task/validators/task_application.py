from src.business_logic.common.validators import ValidationError, length_validator

TEXT_MIN_LENGTH = 10
TEXT_MAX_LENGTH = 150
text_length_validation_error = ValidationError(
    ["text"],
    context_message="Текст отклика должен состоять минимум из 10 и максимум из 150 символов",
)


def validate_text(text: str) -> None:
    if not length_validator(text, TEXT_MIN_LENGTH, TEXT_MAX_LENGTH):
        raise text_length_validation_error
