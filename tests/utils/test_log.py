import io
import logging
import sys

from src.utils.log import (
    LOGGER_NAMESPACE,
    OperationFormatter,
    get_logger,
    pluralize,
    supports_color,
)


def _record(name="portfolio.parse_data", level=logging.INFO, msg="Loaded data"):
    """Build a bare LogRecord for exercising the formatter directly.

    Args:
        name: logger name the record appears to come from.
        level: the record's log level.
        msg: the record's message.

    Returns:
        logging.LogRecord: the record.
    """
    return logging.LogRecord(name, level, __file__, 1, msg, None, None)


def test_get_logger_namespaces_under_portfolio():
    """Operation loggers live under the shared namespace configure_logging targets."""
    assert get_logger("parse_data").name == f"{LOGGER_NAMESPACE}.parse_data"


def test_formatter_aligns_columns_and_shows_operation_name():
    """Lines read as time, padded level, padded operation name, then message."""
    line = OperationFormatter().format(_record())

    _timestamp, rest = line.split("  ", 1)
    assert rest == "INFO     parse_data       Loaded data"


def test_formatter_without_color_emits_no_escape_codes():
    """Plain output (non-terminal, NO_COLOR) never contains ANSI codes."""
    assert "\033[" not in OperationFormatter(use_color=False).format(_record())


def test_formatter_with_color_emits_escape_codes():
    """Colored output wraps columns in ANSI codes but keeps the message intact."""
    line = OperationFormatter(use_color=True).format(_record())

    assert "\033[" in line
    assert line.endswith("Loaded data")


def test_formatter_appends_traceback_when_exc_info_present():
    """A record logged with exc_info includes the traceback below the line."""
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord(
            "portfolio.x", logging.ERROR, __file__, 1, "failed", None, True
        )
        record.exc_info = sys.exc_info()

    assert "ValueError: boom" in OperationFormatter().format(record)


def test_supports_color_false_for_non_terminal_stream(monkeypatch):
    """A StringIO (or a pipe/file) never gets colors."""
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert supports_color(io.StringIO()) is False


def test_supports_color_true_for_terminal_stream(monkeypatch):
    """A stream that reports itself as a terminal gets colors."""
    monkeypatch.delenv("NO_COLOR", raising=False)

    class _FakeTty(io.StringIO):
        def isatty(self):
            return True

    assert supports_color(_FakeTty()) is True


def test_supports_color_respects_no_color(monkeypatch):
    """NO_COLOR disables colors even on a terminal."""
    monkeypatch.setenv("NO_COLOR", "1")

    class _FakeTty(io.StringIO):
        def isatty(self):
            return True

    assert supports_color(_FakeTty()) is False


def test_pluralize_singular_and_plural():
    """One takes the singular; anything else takes the plural."""
    assert pluralize(1, "project") == "1 project"
    assert pluralize(0, "project") == "0 projects"
    assert pluralize(3, "project") == "3 projects"


def test_pluralize_uses_explicit_plural_when_given():
    """Irregular plurals can be passed in rather than appending "s"."""
    assert pluralize(2, "directory", "directories") == "2 directories"
    assert pluralize(1, "directory", "directories") == "1 directory"
