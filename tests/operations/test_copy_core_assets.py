import logging

import pytest

from src.errors.copy_core_assets import CoreAssetsCopyError
from src.operations import copy_core_assets as copy_core_assets_module
from src.operations.copy_core_assets import copy_core_assets


def test_copy_core_assets_copies_core_assets_dir_to_dist(monkeypatch):
    """copy_core_assets delegates to copy_path_to_dist with assets/core-assets."""
    calls = []
    monkeypatch.setattr(
        copy_core_assets_module,
        "copy_path_to_dist",
        lambda relative_path: calls.append(relative_path),
    )

    copy_core_assets()

    assert calls == ["assets/core-assets"]


def test_copy_core_assets_raises_on_os_error(monkeypatch):
    """A filesystem failure raises CoreAssetsCopyError, not a raw OSError."""

    def _broken_copy(relative_path):
        raise OSError("disk error")

    monkeypatch.setattr(copy_core_assets_module, "copy_path_to_dist", _broken_copy)

    with pytest.raises(CoreAssetsCopyError, match="disk error"):
        copy_core_assets()


def test_copy_core_assets_logs_file_count(tmp_path, monkeypatch, caplog):
    """copy_core_assets logs how many files assets/core-assets/ held."""
    caplog.set_level(logging.INFO, logger="portfolio")
    (tmp_path / "assets" / "core-assets" / "icons").mkdir(parents=True)
    (tmp_path / "assets" / "core-assets" / "stars-tile.svg").write_text("<svg></svg>")
    (tmp_path / "assets" / "core-assets" / "icons" / "home.svg").write_text(
        "<svg></svg>"
    )
    monkeypatch.setattr(copy_core_assets_module, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(copy_core_assets_module, "copy_path_to_dist", lambda path: None)

    copy_core_assets()

    assert (
        "Copied assets/core-assets/ -> dist/assets/core-assets/ (2 files)"
        in caplog.text
    )
