import logging
import sys

from src.utils.log import (
    LOGGER_NAMESPACE,
    OperationFormatter,
    get_logger,
    supports_color,
)

_log = get_logger("configure_logging")


def configure_logging(stream=None, level: int = logging.INFO) -> logging.Handler:
    """Send every operation's log output to a stream, formatted as aligned lines.

    Attaches one handler to the ``portfolio`` logger, which every operation
    logs under (see ``get_logger``). Calling it again replaces that handler
    rather than adding a second one, so lines are never printed twice.

    Args:
        stream: Where to write log lines. Defaults to ``sys.stderr``.
        level: The lowest level to show. Defaults to ``logging.INFO``.

    Returns:
        logging.Handler: The handler that was attached.
    """
    if stream is None:
        stream = sys.stderr

    logger = logging.getLogger(LOGGER_NAMESPACE)
    for existing in list(logger.handlers):
        if getattr(existing, "_portfolio_handler", False):
            logger.removeHandler(existing)

    handler = logging.StreamHandler(stream)
    handler.setFormatter(OperationFormatter(use_color=supports_color(stream)))
    handler._portfolio_handler = True
    logger.addHandler(handler)
    logger.setLevel(level)

    _log.debug("Logging configured at level %s", logging.getLevelName(level))
    return handler
