import os
import sys
import logging
from inspect import stack

INITIALIZED = False
LOG_FORMAT_MSG = "%(asctime)s | name(%(name)s) | level(%(levelname)s) | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
ROOT_LOGGER, BOT_LOGGER = logging.getLogger(), logging.getLogger("BOT")

class InfoStack:
    """Information about the 'Stack' being executed."""

    line: str
    """Number of the code line"""
    name: str
    """File name"""
    path: str
    """File path"""

    def __init__ (self, index=1) -> None:
        frame = stack()[index]
        self.line = frame.lineno
        self.name = os.path.basename(frame.filename)


def initialize () -> None:
    """Initialize the logger"""
    LOG_CURRENT_PATH = os.path.join(os.getcwd(), ".log")

    logging.basicConfig(
        force = True,
        encoding = "utf-8",
        datefmt = LOG_DATE_FORMAT,
        format = LOG_FORMAT_MSG,
        level = logging.INFO,
        handlers = [logging.FileHandler(LOG_CURRENT_PATH, "w", "utf-8"), logging.StreamHandler(sys.stdout)]
    )

    global INITIALIZED
    INITIALIZED = True

def create_message (message: str) -> str:
    if not INITIALIZED: initialize()
    stack = InfoStack(3)

    return f"line({ stack.line }) | file({ stack.name }) | { message }"

def debug (message: str) -> None:
    """`DEBUG` Log level """
    BOT_LOGGER.debug(create_message(message), exc_info=sys.exc_info())

def info (message: str) -> None:
    """`INFO` Log level """
    BOT_LOGGER.info(create_message(message))

def warning (message: str) -> None:
    """`WARNING` Log level """
    BOT_LOGGER.warning(create_message(message))

def error (message: str) -> None:
    """`ERROR` Log level """
    BOT_LOGGER.error(create_message(message))

all = [
    "debug",
    "info",
    "warning",
    "error"
]