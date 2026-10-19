import logging

import pytest

from src.errors.copy_static import StaticCopyError
from src.operations import copy_static as copy_static_module
from src.operations.copy_static import copy_static


def test_copy_static_copies_static_dir_to_dist(monkeypatch):
    """copy_static delegates to copy_path_to_dist with the static/ path."""
    calls = []
    monkeypatch.setattr(
        copy_static_module,
        "copy_path_to_dist",
        lambda relative_path: calls.append(relative_path),
    )

    copy_static()

    assert calls == ["static"]


def test_copy_static_raises_on_os_error(monkeypatch):
    """A filesystem failure raises StaticCopyError, not a raw OSError."""

    def _broken_copy(relative_path):
        raise OSError("disk error")

    monkeypatch.setattr(copy_static_module, "copy_path_to_dist", _broken_copy)

    with pytest.raises(StaticCopyError, match="disk error"):
        copy_static()


def test_copy_static_logs_file_count(tmp_path, monkeypatch, caplog):
    """copy_static logs how many files static/ held."""
    caplog.set_level(logging.INFO, logger="portfolio")
    (tmp_path / "static" / "images").mkdir(parents=True)
    (tmp_path / "static" / "styles.css").write_text("body {}")
    (tmp_path / "static" / "images" / "logo.png").write_text("binary")
    monkeypatch.setattr(copy_static_module, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(copy_static_module, "copy_path_to_dist", lambda path: None)

    copy_static()

    assert "Copied static/ -> dist/static/ (2 files)" in caplog.text
