from src.utils import copy as copy_module
from src.utils.copy import copy_path_to_dist


def _patch_dirs(monkeypatch, root_dir, dist_dir):
    """Point copy_path_to_dist's module-level path constants at fake dirs.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        root_dir: fake repo root to copy source paths from.
        dist_dir: fake dist directory to copy into.
    """
    monkeypatch.setattr(copy_module, "ROOT_DIR", root_dir)
    monkeypatch.setattr(copy_module, "DIST_DIR", dist_dir)


def test_copy_path_to_dist_copies_directory_contents(tmp_path, monkeypatch):
    """Copying a directory copies every file and subdirectory inside it."""
    root_dir = tmp_path / "root"
    (root_dir / "static" / "images").mkdir(parents=True)
    (root_dir / "static" / "styles.css").write_text("body {}")
    (root_dir / "static" / "images" / "logo.png").write_text("binary")
    dist_dir = tmp_path / "dist"
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    copy_path_to_dist("static")

    assert (dist_dir / "static" / "styles.css").read_text() == "body {}"
    assert (dist_dir / "static" / "images" / "logo.png").read_text() == "binary"


def test_copy_path_to_dist_overwrites_existing_destination(tmp_path, monkeypatch):
    """A pre-existing (e.g. scaffolded) destination directory doesn't error."""
    root_dir = tmp_path / "root"
    (root_dir / "static").mkdir(parents=True)
    (root_dir / "static" / "styles.css").write_text("body {}")
    dist_dir = tmp_path / "dist"
    (dist_dir / "static").mkdir(parents=True)
    _patch_dirs(monkeypatch, root_dir, dist_dir)

    copy_path_to_dist("static")

    assert (dist_dir / "static" / "styles.css").read_text() == "body {}"
