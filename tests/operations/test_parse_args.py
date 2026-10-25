import logging
from pathlib import Path

import pytest

from src.operations.parse_args import parse_args
from src.utils.paths import DATA_PATH


def test_parse_args_defaults_data_to_data_path():
    """With no arguments, --data falls back to DATA_PATH."""
    assert parse_args([]).data == DATA_PATH


def test_parse_args_data_flag_overrides_default():
    """--data PATH is returned as a Path, replacing the default."""
    assert parse_args(["--data", "data.template.json"]).data == Path(
        "data.template.json"
    )


def test_parse_args_image_processing_on_by_default():
    """Without the flag, no_image_processing is False."""
    assert parse_args([]).no_image_processing is False


def test_parse_args_no_image_processing_flag(caplog):
    """--no-image-processing sets no_image_processing and is logged."""
    caplog.set_level(logging.INFO, logger="portfolio")

    assert parse_args(["--no-image-processing"]).no_image_processing is True
    assert "(image processing off)" in caplog.text


def test_parse_args_rejects_unknown_arguments():
    """Unknown arguments exit with argparse's usage error rather than being ignored."""
    with pytest.raises(SystemExit):
        parse_args(["--nope"])


def test_parse_args_logs_data_path(caplog):
    """parse_args logs which data file the build will read."""
    caplog.set_level(logging.INFO, logger="portfolio")

    parse_args(["--data", "data.template.json"])

    assert "Building from data.template.json" in caplog.text
