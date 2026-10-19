from src.errors.copy_static import StaticCopyError
from src.utils.copy import copy_path_to_dist


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
