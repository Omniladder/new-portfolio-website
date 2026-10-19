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


def test_process_assets_processes_only_top_level_images(tmp_path, monkeypatch):
    """process_assets skips subdirectories and non-image files in assets/."""
    root_dir = tmp_path / "root"
    assets_dir = root_dir / "assets"
    assets_dir.mkdir(parents=True)
    (assets_dir / "logo.png").write_bytes(b"png bytes")
    (assets_dir / "photo.jpg").write_bytes(b"jpg bytes")
    (assets_dir / ".gitkeep").write_bytes(b"")
    (assets_dir / "download").mkdir()
    (assets_dir / "download" / "resume.pdf").write_bytes(b"pdf bytes")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    process_assets()

    assert (dist_dir / "assets" / "logo.png").read_bytes() == b"png bytes"
    assert (dist_dir / "assets" / "photo.jpg").read_bytes() == b"jpg bytes"
    assert not (dist_dir / "assets" / ".gitkeep").exists()
    assert not (dist_dir / "assets" / "download").exists()


def test_process_assets_calls_process_asset_for_each_image(tmp_path, monkeypatch):
    """process_assets delegates each top-level image to process_asset."""
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
