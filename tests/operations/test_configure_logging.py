import io
import logging

import pytest

from src.operations.configure_logging import configure_logging
from src.utils.log import LOGGER_NAMESPACE, get_logger


@pytest.fixture
def portfolio_logger():
    """Restore the portfolio logger's handlers and level after each test.

    Yields:
        logging.Logger: the shared ``portfolio`` logger.
    """
    logger = logging.getLogger(LOGGER_NAMESPACE)
    saved_handlers, saved_level = list(logger.handlers), logger.level
    yield logger
    logger.handlers[:] = saved_handlers
    logger.setLevel(saved_level)


def test_configure_logging_writes_operation_logs_to_stream(portfolio_logger):
    """Once configured, an operation's INFO line reaches the given stream."""
    stream = io.StringIO()
    configure_logging(stream)

    get_logger("parse_data").info("Loaded data")

    assert "parse_data" in stream.getvalue()
    assert "Loaded data" in stream.getvalue()


def test_configure_logging_twice_does_not_duplicate_lines(portfolio_logger):
    """Reconfiguring replaces the handler, so each line is written once."""
    configure_logging(io.StringIO())
    stream = io.StringIO()
    configure_logging(stream)

    get_logger("parse_data").info("Loaded data")

    assert stream.getvalue().count("Loaded data") == 1


def test_configure_logging_hides_lines_below_level(portfolio_logger):
    """Records below the configured level are dropped."""
    stream = io.StringIO()
    configure_logging(stream, level=logging.WARNING)

    get_logger("parse_data").info("Loaded data")

    assert stream.getvalue() == ""
