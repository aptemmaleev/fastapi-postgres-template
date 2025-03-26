from os import mkdir, getcwd, makedirs
from sys import stdout
from logging import DEBUG, INFO, WARN, ERROR, FATAL
from logging import basicConfig, debug
from logging import FileHandler, StreamHandler
from os.path import isdir, exists
from datetime import datetime

from .settings import SETTINGS


def setup():
    if not isdir("logs"):
        mkdir("logs")

    logging_level = 0
    env_logging_level = SETTINGS.LOGGING_LEVEL
    if env_logging_level == "DEBUG":
        logging_level = DEBUG
    elif env_logging_level == "INFO":
        logging_level = INFO
    elif env_logging_level in ("WARN", "WARNING"):
        logging_level = WARN
    elif env_logging_level == "ERROR":
        logging_level = ERROR
    elif env_logging_level in ("FATAL", "CRITICAL"):
        logging_level = FATAL

    if not exists(f'{datetime.now().strftime("logs/%m.%Y")}'):
        makedirs(f'{datetime.now().strftime("logs/%m.%Y")}')

    # Setting up logging
    basicConfig(
        level=logging_level,
        format="%(levelname)s - [%(module)s] - %(message)s",
        handlers=[
            FileHandler(f'{datetime.now().strftime("logs/%m.%Y/%d.%m.%Y.log")}'),
            StreamHandler(stdout),
        ],
        encoding="utf-32",
    )

    debug(f"Logger set up! Cwd: {getcwd()}")
