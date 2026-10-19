from src.errors.copy_core_assets import CoreAssetsCopyError
from src.utils.copy import copy_path_to_dist
from src.utils.log import get_logger, pluralize
from src.utils.paths import ROOT_DIR

_log = get_logger("copy_core_assets")


def copy_core_assets() -> None:
    """Copy assets/core-assets/ and everything inside it into dist/assets/core-assets/.

    Core assets are app-owned (not per-fork content) and copied as-is, the
    same way copy_downloads handles assets/download/ (see docs/arch/0017).

    Returns:
        None.

    Raises:
        CoreAssetsCopyError: If assets/core-assets/ can't be copied into
            dist/assets/core-assets/.
    """
    try:
        copy_path_to_dist("assets/core-assets")
    except OSError as e:
        raise CoreAssetsCopyError(
            f"Failed to copy assets/core-assets/ into dist/assets/core-assets/: {e}"
        ) from e

    file_count = sum(
        1 for path in (ROOT_DIR / "assets" / "core-assets").rglob("*") if path.is_file()
    )
    _log.info(
        "Copied assets/core-assets/ -> dist/assets/core-assets/ (%s)",
        pluralize(file_count, "file"),
    )
