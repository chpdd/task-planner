import time
import logging
from sys import stderr


class TZFormatter(logging.Formatter):
    tz = time.strftime("%z")
    # tz = f"{tz[:-2]}:{tz[-2:]}"

    def format(self, record):
        record.timezone = self.tz
        return super().format(record)


date_format = '%Y-%m-%d %H:%M:%S'
log_format = '%(asctime)s.%(msecs)03d %(timezone)s %(levelname)s - %(name)s (%(filename)s:%(lineno)d): %(message)s'

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "()": TZFormatter,
            "fmt": log_format,
            "datefmt": date_format
        }
    },
    "handlers": {
        "default_handler": {
            "formatter": "default_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["default_handler"]
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO"},
        "fastapi": {"level": "DEBUG"},
        "sqlalchemy.engine": {"level": "INFO"}
    },
}
