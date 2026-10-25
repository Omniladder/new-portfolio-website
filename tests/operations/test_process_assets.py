import logging

import pytest

from src.errors.process_assets import AssetProcessingError
from src.operations import process_assets as process_assets_module
from src.operations.process_assets import process_asset, process_assets


def _patch_dirs(monkeypatch, root_dir, dist_dir):
    """Point process_assets' module-level path constants at fake dirs.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        root_dir: fake repo root to read assets/ from.
        dist_dir: fake dist directory to write processed images into.
    """
    monkeypatch.setattr(process_assets_module, "ROOT_DIR", root_dir)
    monkeypatch.setattr(process_assets_module, "DIST_DIR", dist_dir)


def test_process_asset_reads_processes_and_writes_an_image(tmp_path, monkeypatch):
    """process_asset round-trips a single image from assets/ into dist/assets/."""
    root_dir = tmp_path / "root"
    (root_dir / "assets").mkdir(parents=True)
    source_path = root_dir / "assets" / "logo.png"
    source_path.write_bytes(b"raw bytes")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    process_asset(source_path)

    assert (dist_dir / "assets" / "logo.png").read_bytes() == b"raw bytes"


def test_process_asset_raises_on_os_error(tmp_path, monkeypatch):
    """A filesystem failure raises AssetProcessingError naming the file."""
    root_dir = tmp_path / "root"
    (root_dir / "assets").mkdir(parents=True)
    source_path = root_dir / "assets" / "logo.png"
    source_path.write_bytes(b"raw bytes")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    def _broken_write(path, data):
        raise OSError("disk error")

    monkeypatch.setattr(process_assets_module, "write_image_data", _broken_write)

    with pytest.raises(AssetProcessingError, match="logo.png"):
        process_asset(source_path)


def test_process_assets_processes_images_in_subfolders(tmp_path, monkeypatch):
    """process_assets mirrors images in nested folders, skipping non-images."""
    root_dir = tmp_path / "root"
    assets_dir = root_dir / "assets"
    (assets_dir / "projects" / "chapp").mkdir(parents=True)
    (assets_dir / "logo.png").write_bytes(b"png bytes")
    (assets_dir / "projects" / "chapp" / "shot.jpg").write_bytes(b"jpg bytes")
    (assets_dir / "projects" / "notes.txt").write_bytes(b"text")
    (assets_dir / ".gitkeep").write_bytes(b"")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    process_assets()

    assert (dist_dir / "assets" / "logo.png").read_bytes() == b"png bytes"
    assert (dist_dir / "assets" / "projects" / "chapp" / "shot.jpg").read_bytes() == (
        b"jpg bytes"
    )
    assert not (dist_dir / "assets" / "projects" / "notes.txt").exists()
    assert not (dist_dir / "assets" / ".gitkeep").exists()


def test_process_assets_skips_download_and_core_assets(tmp_path, monkeypatch):
    """assets/download/ and assets/core-assets/ are left to their own operations."""
    root_dir = tmp_path / "root"
    assets_dir = root_dir / "assets"
    (assets_dir / "download").mkdir(parents=True)
    (assets_dir / "download" / "poster.png").write_bytes(b"png bytes")
    (assets_dir / "core-assets" / "icons").mkdir(parents=True)
    (assets_dir / "core-assets" / "icons" / "computer.svg").write_bytes(b"svg")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    process_assets()

    assert not (dist_dir / "assets" / "download").exists()
    assert not (dist_dir / "assets" / "core-assets").exists()


def test_process_assets_calls_process_asset_for_each_image(tmp_path, monkeypatch):
    """process_assets delegates each image to process_asset."""
    root_dir = tmp_path / "root"
    assets_dir = root_dir / "assets"
    assets_dir.mkdir(parents=True)
    (assets_dir / "logo.png").write_bytes(b"png bytes")
    (assets_dir / "photo.jpg").write_bytes(b"jpg bytes")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)
    calls = []
    monkeypatch.setattr(
        process_assets_module, "process_asset", lambda path: calls.append(path)
    )

    process_assets()

    assert calls == [assets_dir / "logo.png", assets_dir / "photo.jpg"]


def test_process_assets_logs_image_count(tmp_path, monkeypatch, caplog):
    """process_assets logs how many images it processed."""
    caplog.set_level(logging.INFO, logger="portfolio")
    root_dir = tmp_path / "root"
    (root_dir / "assets").mkdir(parents=True)
    (root_dir / "assets" / "logo.png").write_bytes(b"png bytes")
    _patch_dirs(monkeypatch, root_dir, tmp_path / "dist")
    monkeypatch.setattr(process_assets_module, "process_asset", lambda path: None)

    process_assets()

    assert "Processed assets/ -> dist/assets/ (1 image)" in caplog.text
