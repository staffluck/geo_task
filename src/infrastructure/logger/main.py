import logging
import logging.config

from src.config import LoggingSettings
from src.infrastructure.logger.logger_config import get_logger_config


def setup_logging(logging_settings: LoggingSettings) -> None:
    logging_config = get_logger_config(
        logging_settings.additional_configs,
        log_level=logging_settings.LOGGING_LEVEL,
        render_as_json=logging_settings.RENDER_LOGS_AS_JSON,
    )
    logging.config.dictConfig(logging_config)
