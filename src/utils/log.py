import logging
import os

# Every operation logs under this namespace, e.g. "portfolio.parse_data", so
# configure_logging() can attach one handler that covers all of them without
# touching the root logger. See docs/arch/0015.
LOGGER_NAMESPACE = "portfolio"

_RESET = "\033[0m"
_DIM = "\033[2m"
_BOLD = "\033[1m"
_CYAN = "\033[36m"
_LEVEL_COLORS = {
    "DEBUG": "\033[34m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[1;31m",
}


class OperationFormatter(logging.Formatter):
    """Format log records as aligned ``time  LEVEL  operation  message`` lines.

    The operation column is the last segment of the logger's name, so a
    record from ``portfolio.parse_data`` is shown as ``parse_data``.
    """

    def __init__(self, use_color: bool = False) -> None:
        """Create the formatter.

        Args:
            use_color: Whether to wrap columns in ANSI color codes. Only
                pass True when writing to a terminal.
        """
        super().__init__(datefmt="%H:%M:%S")
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        """Render one record as a single aligned line.

        Args:
            record: The log record to format.

        Returns:
            str: The formatted line, followed by the traceback if the record
            carries exception info.
        """
        timestamp = self.formatTime(record, self.datefmt)
        level = f"{record.levelname:<7}"
        operation = f"{record.name.rpartition('.')[2]:<15}"
        message = record.getMessage()

        if self.use_color:
            timestamp = f"{_DIM}{timestamp}{_RESET}"
            level_color = _LEVEL_COLORS.get(record.levelname, "")
            level = f"{_BOLD}{level_color}{level}{_RESET}"
            operation = f"{_CYAN}{operation}{_RESET}"

        line = f"{timestamp}  {level}  {operation}  {message}"
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


def get_logger(operation: str) -> logging.Logger:
    """Return the logger an operation should log through.

    Args:
        operation: The operation's name, e.g. ``"parse_data"``. Shown in the
            operation column of every line it logs.

    Returns:
        logging.Logger: The ``portfolio.<operation>`` logger.
    """
    return logging.getLogger(LOGGER_NAMESPACE).getChild(operation)


def supports_color(stream) -> bool:
    """Decide whether ANSI colors should be written to a stream.

    Args:
        stream: The stream log output will be written to.

    Returns:
        bool: True if the stream is a terminal and the ``NO_COLOR``
        environment variable isn't set (see https://no-color.org).
    """
    if "NO_COLOR" in os.environ:
        return False
    isatty = getattr(stream, "isatty", None)
    return bool(isatty and isatty())


def pluralize(count: int, noun: str, plural: str = None) -> str:
    """Pair a count with a noun, using the plural form unless the count is one.

    Args:
        count: How many of the thing there are.
        noun: The singular noun, e.g. ``"project"``.
        plural: The plural noun, for nouns that don't just take an "s"
            (e.g. ``"directories"``). Defaults to ``noun + "s"``.

    Returns:
        str: e.g. ``"1 project"`` or ``"3 projects"``.
    """
    if count == 1:
        return f"{count} {noun}"
    return f"{count} {plural or noun + 's'}"
