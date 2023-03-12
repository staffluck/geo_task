def get_logger_config(
    *confs: dict,
    log_level: str,
    render_as_json: bool,
) -> dict:
    fmt = "%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": fmt,
                "datefmt": datefmt,
            },
            "json": {
                "format": fmt,
                "datefmt": datefmt,
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "formatter": "json" if render_as_json else "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {"passlib": {"level": "CRITICAL"}},
        "root": {
            "handlers": ["default"],
            "level": log_level,
            "propagate": False,
        },
    }
    for conf in confs:
        for key in conf:
            config[key].update(conf[key])  # type: ignore

    return config
