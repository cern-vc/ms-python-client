import logging
import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    "WARNING": YELLOW,
    "INFO": GREEN,
    "DEBUG": BLUE,
    "CRITICAL": MAGENTA,
    "ERROR": RED,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        msg = msg.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        logging.Formatter.__init__(self, msg)

    def format(self, record):  # pragma: no cover
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = (
                COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            )
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def setup_logs(log_level=logging.WARNING):
    logger = logging.getLogger("ms_python_client")

    logger.setLevel(log_level)
    format_string = (
        "%(asctime)s | %(levelname)-18s | $BOLD%(name)-20s$RESET | "
        "%(message)s | %(pathname)s:%(lineno)d | %(funcName)s()"
    )
    color_formatter = ColoredFormatter(format_string)

    configure_stdout_logging(
        logger=logger, formatter=color_formatter, log_level=log_level
    )

    return logger


def configure_stdout_logging(logger, formatter=None, log_level=logging.WARNING):
    stream_handler = logging.StreamHandler(stream=sys.stdout)

    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    logger.addHandler(stream_handler)
    print(f"Logging {str(logger)} to stdout -> True")
