import logging

import pytest

from src.errors.copy_downloads import DownloadsCopyError
from src.operations import copy_downloads as copy_downloads_module
from src.operations.copy_downloads import copy_downloads


def test_copy_downloads_copies_download_dir_to_dist(monkeypatch):
    """copy_downloads delegates to copy_path_to_dist with the assets/download path."""
    calls = []
    monkeypatch.setattr(
        copy_downloads_module,
        "copy_path_to_dist",
        lambda relative_path: calls.append(relative_path),
    )

    copy_downloads()

    assert calls == ["assets/download"]


def test_copy_downloads_raises_on_os_error(monkeypatch):
    """A filesystem failure raises DownloadsCopyError, not a raw OSError."""

    def _broken_copy(relative_path):
        raise OSError("disk error")

    monkeypatch.setattr(copy_downloads_module, "copy_path_to_dist", _broken_copy)

    with pytest.raises(DownloadsCopyError, match="disk error"):
        copy_downloads()


def test_copy_downloads_logs_file_count(tmp_path, monkeypatch, caplog):
    """copy_downloads logs how many files assets/download/ held."""
    caplog.set_level(logging.INFO, logger="portfolio")
    (tmp_path / "assets" / "download" / "slides").mkdir(parents=True)
    (tmp_path / "assets" / "download" / "resume.pdf").write_text("pdf")
    (tmp_path / "assets" / "download" / "slides" / "talk.pdf").write_text("pdf")
    monkeypatch.setattr(copy_downloads_module, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(copy_downloads_module, "copy_path_to_dist", lambda path: None)

    copy_downloads()

    assert "Copied assets/download/ -> dist/assets/download/ (2 files)" in caplog.text
