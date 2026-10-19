import shutil

from src.utils.paths import DIST_DIR, ROOT_DIR


def copy_path_to_dist(relative_path: str) -> None:
    """Copy a root-level file or directory into its mirrored path under dist/.

    Args:
        relative_path: Path relative to ROOT_DIR (e.g. ``"static"``) to copy.
            The same relative path is used under DIST_DIR, per the mirroring
            convention in docs/arch/0005.

    Returns:
        None.
    """
    source = ROOT_DIR / relative_path
    destination = DIST_DIR / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)
