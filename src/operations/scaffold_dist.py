import shutil

from src.errors.scaffold_dist import DistScaffoldError
from src.utils.paths import DIST_DIR, MIRRORED_DIRS, ROOT_DIR


def scaffold_dist() -> None:
    """Rebuild the dist/ directory tree from scratch.

    Deletes any existing ``DIST_DIR`` and recreates it, then recreates the
    directory (not file) structure of every entry in ``MIRRORED_DIRS``
    underneath it, so later operations can write mirrored assets into a
    directory tree that already exists. See docs/arch/0005 for which
    directories are mirrored and why.

    Returns:
        None.

    Raises:
        DistScaffoldError: If DIST_DIR can't be cleared or recreated.
    """
    try:
        if DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)
        DIST_DIR.mkdir(parents=True)

        for relative_dir in MIRRORED_DIRS:
            source_root = ROOT_DIR / relative_dir
            (DIST_DIR / relative_dir).mkdir(parents=True, exist_ok=True)
            for path in source_root.rglob("*"):
                if path.is_dir():
                    (DIST_DIR / path.relative_to(ROOT_DIR)).mkdir(
                        parents=True, exist_ok=True
                    )
    except OSError as e:
        raise DistScaffoldError(f"Failed to rebuild {DIST_DIR}: {e}") from e
