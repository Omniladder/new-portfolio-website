import logging
from io import BytesIO

import pytest
from PIL import Image

from src.errors.process_core_assets import CoreAssetsProcessingError
from src.operations import process_core_assets as process_core_assets_module
from src.operations.process_core_assets import (
    process_core_asset,
    process_core_assets,
)


def _patch_dirs(monkeypatch, root_dir, dist_dir):
    """Point process_core_assets' module-level path constants at fake dirs.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        root_dir: fake repo root to read assets/core-assets/ from.
        dist_dir: fake dist directory to write into.
    """
    monkeypatch.setattr(process_core_assets_module, "ROOT_DIR", root_dir)
    monkeypatch.setattr(process_core_assets_module, "DIST_DIR", dist_dir)


def _make_core_dir(tmp_path):
    """Create a fake assets/core-assets/ with an SVG, a PNG, and a license."""
    core_dir = tmp_path / "root" / "assets" / "core-assets"
    (core_dir / "icons").mkdir(parents=True)
    (core_dir / "icons" / "home.svg").write_text("<svg></svg>")
    (core_dir / "icons" / "LICENSE.txt").write_text("MIT")
    buffer = BytesIO()
    Image.new("RGB", (8, 8), (10, 20, 30)).save(buffer, format="PNG")
    (core_dir / "tile.png").write_bytes(buffer.getvalue())
    return core_dir


def test_process_core_asset_runs_images_through_process_image_data(
    tmp_path, monkeypatch
):
    """An image is written to dist/ as process_image_data returns it."""
    core_dir = _make_core_dir(tmp_path)
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, tmp_path / "root", dist_dir)
    monkeypatch.setattr(
        process_core_assets_module, "process_image_data", lambda data: b"processed"
    )

    assert process_core_asset(core_dir / "tile.png") is True
    assert (dist_dir / "assets" / "core-assets" / "tile.png").read_bytes() == (
        b"processed"
    )


def test_process_core_asset_copies_non_images_unchanged(tmp_path, monkeypatch):
    """A non-image file is copied as-is, never through process_image_data."""
    core_dir = _make_core_dir(tmp_path)
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, tmp_path / "root", dist_dir)
    monkeypatch.setattr(
        process_core_assets_module, "process_image_data", lambda data: b"processed"
    )

    assert process_core_asset(core_dir / "icons" / "LICENSE.txt") is False
    assert (
        dist_dir / "assets" / "core-assets" / "icons" / "LICENSE.txt"
    ).read_text() == "MIT"


def test_process_core_asset_raises_on_os_error(tmp_path, monkeypatch):
    """A filesystem failure raises CoreAssetsProcessingError, not a raw OSError."""
    core_dir = _make_core_dir(tmp_path)
    _patch_dirs(monkeypatch, tmp_path / "root", tmp_path / "dist")

    def _broken_read(path):
        raise OSError("disk error")

    monkeypatch.setattr(process_core_assets_module, "read_image_data", _broken_read)

    with pytest.raises(CoreAssetsProcessingError, match="disk error"):
        process_core_asset(core_dir / "tile.png")


def test_process_core_assets_mirrors_every_file_into_dist(tmp_path, monkeypatch):
    """Every file in assets/core-assets/ lands at its mirrored dist/ path."""
    _make_core_dir(tmp_path)
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, tmp_path / "root", dist_dir)

    process_core_assets()

    out_dir = dist_dir / "assets" / "core-assets"
    assert (out_dir / "icons" / "home.svg").read_text() == "<svg></svg>"
    assert (out_dir / "icons" / "LICENSE.txt").read_text() == "MIT"
    assert Image.open(out_dir / "tile.png").size == (8, 8)


def test_process_core_assets_logs_counts(tmp_path, monkeypatch, caplog):
    """process_core_assets logs how many images it processed and files it copied."""
    caplog.set_level(logging.INFO, logger="portfolio")
    _make_core_dir(tmp_path)
    _patch_dirs(monkeypatch, tmp_path / "root", tmp_path / "dist")

    process_core_assets()

    assert (
        "Processed assets/core-assets/ -> dist/assets/core-assets/ "
        "(2 images, 1 other file copied)"
    ) in caplog.text
