from src.errors.copy_static import StaticCopyError
from src.utils.copy import copy_path_to_dist
from src.utils.log import get_logger, pluralize
from src.utils.paths import ROOT_DIR

_log = get_logger("copy_static")


def copy_static() -> None:
    """Copy static/ and everything inside it into dist/static/.

    Returns:
        None.

    Raises:
        StaticCopyError: If static/ can't be copied into dist/static/.
    """
    try:
        copy_path_to_dist("static")
    except OSError as e:
        raise StaticCopyError(f"Failed to copy static/ into dist/static/: {e}") from e

    file_count = sum(1 for path in (ROOT_DIR / "static").rglob("*") if path.is_file())
    _log.info("Copied static/ -> dist/static/ (%s)", pluralize(file_count, "file"))
