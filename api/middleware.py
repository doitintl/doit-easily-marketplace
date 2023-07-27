import os
from typing import Dict
import structlog


def field_name_modifier(logger: structlog._loggers.PrintLogger, log_method: str, event_dict: Dict) -> Dict:
    # Changes the keys for some of the fields, to match Cloud Logging's expectations
    event_dict["severity"] = event_dict["level"]
    del event_dict["level"]
    event_dict["message"] = event_dict["event"]
    del event_dict["event"]
    return event_dict


# TOOD: this log level setting needs to be tested
log_level = structlog.stdlib._NAME_TO_LEVEL[os.getenv("LOG_LEVEL", "debug")]
print(f'log level is {structlog.stdlib._LEVEL_TO_NAME[log_level]}')


def get_json_logger() -> structlog._config.BoundLoggerLazyProxy:
    # extend using https://www.structlog.org/en/stable/processors.html
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            field_name_modifier,
            structlog.processors.TimeStamper("iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level)
    )
    return structlog.get_logger()


logger = get_json_logger()


def logging_flush() -> None:
    # Setting PYTHONUNBUFFERED in Dockerfile ensured no buffering
    pass

def add_request_context_to_log(request_id):
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)