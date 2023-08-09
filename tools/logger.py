import sys
import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default_formatter": {
            "format": f"\n%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s"
        },
    },

    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": sys.stdout
        },
    },

    "loggers": {
        "main_logger": {
            "handlers": ["stream_handler"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}


def get_logger(name: str = __name__):
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
