import logging
from logging import Logger

from colorlog import ColoredFormatter


def create_named_logger(name: str) -> Logger:
    prefix: str = f"[{name}]".rjust(8)
    formatter = ColoredFormatter(
        f"%(purple)s{prefix} %(log_color)s%(levelname)-8s |%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )

    logger: Logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.debug(f"Successfully set up the '{name}' logger")

    return logger
