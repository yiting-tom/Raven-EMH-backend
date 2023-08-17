"""
Author: Yi-Ting Li
Email: yitingli.public@gmail.com
Date Created: 2023-08-17
Last Modified: 2023-08-17
Description: This script is a logging utility that configures
             log output for the application.
"""
import logging
import sys
from pprint import pformat

from loguru import logger
from loguru._defaults import LOGURU_FORMAT


class InterceptHandler(logging.Handler):
    """
    InterceptHandler class extends the logging.Handler class to
    intercept standard logging messages and redirect them to loguru logger.
    """

    def emit(self, record: logging.LogRecord):
        """
        Override of logging.Handler emit function. Captures a logging.LogRecord
        object and forwards it as a loguru log record.

        Parameters:
        record (logging.LogRecord): The record to be logged.
        """
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Redirect the record message to loguru logger with given level
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    Format the log record dictionary to a string suitable for logging output.

    Parameters:
    record (dict): The log record to be formatted, in dict form.

    Returns:
    str: The formatted log record string.
    """
    format_string = LOGURU_FORMAT

    if record["extra"].get("payload") is not None:
        # Pretty print the payload if it exists
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging():
    """
    Initialize logging configuration. Sets up the InterceptHandler to redirect
    uvicorn logs through loguru and configures the loguru logger output format.
    """
    # Get all loggers that start with "uvicorn."
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        # Remove existing handlers from uvicorn loggers
        uvicorn_logger.handlers = []

    # Create a new InterceptHandler instance
    intercept_handler = InterceptHandler()

    # Change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # Set logs output (stdout), level (DEBUG) and format (via format_record function)
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )
