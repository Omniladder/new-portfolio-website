from src.errors.copy_downloads import DownloadsCopyError
from src.utils.copy import copy_path_to_dist
from src.utils.log import get_logger, pluralize
from src.utils.paths import ROOT_DIR

_log = get_logger("copy_downloads")


def copy_downloads() -> None:
    """Copy assets/download/ and everything inside it into dist/assets/download/.

    Downloadable files are copied as-is, unlike the images directly inside
    assets/, which process_assets handles (see docs/arch/0013).

    Returns:
        None.

    Raises:
        DownloadsCopyError: If assets/download/ can't be copied into
            dist/assets/download/.
    """
    try:
        copy_path_to_dist("assets/download")
    except OSError as e:
        raise DownloadsCopyError(
            f"Failed to copy assets/download/ into dist/assets/download/: {e}"
        ) from e

    file_count = sum(
        1 for path in (ROOT_DIR / "assets" / "download").rglob("*") if path.is_file()
    )
    _log.info(
        "Copied assets/download/ -> dist/assets/download/ (%s)",
        pluralize(file_count, "file"),
    )
