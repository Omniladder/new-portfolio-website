import pytest

from src.errors.scaffold_dist import DistScaffoldError
from src.operations import scaffold_dist as scaffold_dist_module


def _make_fake_root(tmp_path):
    """Build a throwaway root directory with the shape scaffold_dist expects.

    Args:
        tmp_path: pytest's per-test temporary directory fixture.

    Returns:
        Path: the fake root directory, populated with assets/, static/, and
        a templates/ directory that must NOT be mirrored into dist/.
    """
    (tmp_path / "assets" / "download").mkdir(parents=True)
    (tmp_path / "assets" / "download" / "resume.pdf").write_text("pdf")
    (tmp_path / "static").mkdir()
    (tmp_path / "static" / "styles.css").write_text("body {}")
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "home.html").write_text("<html></html>")
    return tmp_path


def _patch_paths(monkeypatch, root_dir):
    """Point scaffold_dist's module-level path constants at a fake root.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        root_dir: the fake root directory to scaffold a dist/ under.
    """
    monkeypatch.setattr(scaffold_dist_module, "ROOT_DIR", root_dir)
    monkeypatch.setattr(scaffold_dist_module, "DIST_DIR", root_dir / "dist")


def test_scaffold_dist_mirrors_only_configured_dirs(tmp_path, monkeypatch):
    """Mirrored directories get recreated; non-mirrored ones do not."""
    root_dir = _make_fake_root(tmp_path)
    _patch_paths(monkeypatch, root_dir)

    scaffold_dist_module.scaffold_dist()

    dist_dir = root_dir / "dist"
    assert (dist_dir / "assets" / "download").is_dir()
    assert (dist_dir / "static").is_dir()
    assert not (dist_dir / "templates").exists()


def test_scaffold_dist_does_not_copy_files(tmp_path, monkeypatch):
    """scaffold_dist creates directory structure only, never files."""
    root_dir = _make_fake_root(tmp_path)
    _patch_paths(monkeypatch, root_dir)

    scaffold_dist_module.scaffold_dist()

    dist_dir = root_dir / "dist"
    assert not (dist_dir / "assets" / "download" / "resume.pdf").exists()
    assert not (dist_dir / "static" / "styles.css").exists()


def test_scaffold_dist_clears_stale_dist_contents(tmp_path, monkeypatch):
    """Re-running scaffold_dist wipes anything left over from a prior build."""
    root_dir = _make_fake_root(tmp_path)
    _patch_paths(monkeypatch, root_dir)

    dist_dir = root_dir / "dist"
    dist_dir.mkdir()
    stale_file = dist_dir / "stale.html"
    stale_file.write_text("leftover")

    scaffold_dist_module.scaffold_dist()

    assert not stale_file.exists()
    assert (dist_dir / "assets" / "download").is_dir()


def test_scaffold_dist_raises_on_os_error(tmp_path, monkeypatch):
    """A filesystem failure raises DistScaffoldError, not a raw OSError."""
    root_dir = _make_fake_root(tmp_path)
    _patch_paths(monkeypatch, root_dir)

    def _broken_rmtree(*args, **kwargs):
        raise OSError("disk error")

    monkeypatch.setattr(scaffold_dist_module.shutil, "rmtree", _broken_rmtree)
    (root_dir / "dist").mkdir()

    with pytest.raises(DistScaffoldError, match="disk error"):
        scaffold_dist_module.scaffold_dist()
