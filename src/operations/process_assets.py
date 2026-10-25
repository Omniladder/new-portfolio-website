from pathlib import Path

from tqdm import tqdm

from src.errors.process_assets import AssetProcessingError
from src.utils.images import (
    IMAGE_EXTENSIONS,
    process_image_data,
    read_image_data,
    write_image_data,
)
from src.utils.log import get_logger, pluralize
from src.utils.paths import DIST_DIR, ROOT_DIR

_log = get_logger("process_assets")


# Subdirectories of assets/ that other operations copy, so process_assets
# leaves them alone: copy_downloads and process_core_assets respectively.
SKIPPED_SUBDIRS = {"download", "core-assets"}


def process_assets(process_images: bool = True) -> None:
    """Process every image in assets/ and its subfolders into dist/assets/.

    Images can be organized into any folder structure under ``assets/``
    (e.g. ``assets/projects/<project_name>/``), which is mirrored into
    ``dist/assets/``. ``assets/download/`` and ``assets/core-assets/`` are
    skipped: copy_downloads copies the former as-is, and process_core_assets
    handles the latter. See docs/arch/0032.

    Args:
        process_images: Whether to run each image through
            process_image_data(). False copies images as-is (generate.py's
            ``--no-image-processing``, see docs/arch/0043).

    Returns:
        None.
    """
    assets_dir = ROOT_DIR / "assets"
    image_paths = sorted(
        path
        for path in assets_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
        and path.relative_to(assets_dir).parts[0] not in SKIPPED_SUBDIRS
    )

    for source_path in tqdm(image_paths, desc="Processing assets"):
        process_asset(source_path, process_images)

    _log.info(
        "Processed assets/ -> dist/assets/ (%s%s)",
        pluralize(len(image_paths), "image"),
        "" if process_images else ", copied unprocessed",
    )


def process_asset(source_path: Path, process_images: bool = True) -> None:
    """Read, process, and write a single image from assets/ to dist/assets/.

    Args:
        source_path: Path of the image file, somewhere under ROOT_DIR, to
            process. Its path relative to ROOT_DIR is reproduced under
            DIST_DIR, per the mirroring convention in docs/arch/0005.
        process_images: Whether to run the image through
            process_image_data(). False copies its bytes unchanged.

    Returns:
        None.

    Raises:
        AssetProcessingError: If the image can't be read, processed, or
            written.
    """
    try:
        data = read_image_data(source_path)
        if process_images:
            data = process_image_data(data)
        destination_path = DIST_DIR / source_path.relative_to(ROOT_DIR)
        write_image_data(destination_path, data)
    except OSError as e:
        raise AssetProcessingError(
            f"Failed to process asset '{source_path.relative_to(ROOT_DIR)}': {e}"
        ) from e
