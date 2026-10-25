import shutil
from pathlib import Path

from tqdm import tqdm

from src.errors.process_core_assets import CoreAssetsProcessingError
from src.utils.images import (
    IMAGE_EXTENSIONS,
    process_image_data,
    read_image_data,
    write_image_data,
)
from src.utils.log import get_logger, pluralize
from src.utils.paths import DIST_DIR, ROOT_DIR

_log = get_logger("process_core_assets")


def process_core_assets(process_images: bool = True) -> None:
    """Process assets/core-assets/ into dist/assets/core-assets/.

    Core assets are app-owned (not per-fork content, see docs/arch/0017).
    Their images go through the same read → process → write pipeline as
    process_assets; any other file (e.g. a license) is copied as-is. See
    docs/arch/0042.

    Args:
        process_images: Whether to run each image through
            process_image_data(). False copies images as-is (generate.py's
            ``--no-image-processing``, see docs/arch/0043).

    Returns:
        None.
    """
    core_dir = ROOT_DIR / "assets" / "core-assets"
    paths = sorted(path for path in core_dir.rglob("*") if path.is_file())

    image_count = 0
    for source_path in tqdm(paths, desc="Processing core assets"):
        image_count += process_core_asset(source_path, process_images)

    _log.info(
        "Processed assets/core-assets/ -> dist/assets/core-assets/ (%s%s, %s copied)",
        pluralize(image_count, "image"),
        "" if process_images else " unprocessed",
        pluralize(len(paths) - image_count, "other file"),
    )


def process_core_asset(source_path: Path, process_images: bool = True) -> bool:
    """Process one core-asset image, or copy one non-image file, into dist/.

    Args:
        source_path: Path of the file, somewhere under ROOT_DIR. Its path
            relative to ROOT_DIR is reproduced under DIST_DIR, per the
            mirroring convention in docs/arch/0005.
        process_images: Whether to run an image through
            process_image_data(). False copies it unchanged.

    Returns:
        bool: True if the file was an image, False if it was some other file.

    Raises:
        CoreAssetsProcessingError: If the file can't be read, processed,
            copied, or written.
    """
    destination_path = DIST_DIR / source_path.relative_to(ROOT_DIR)
    is_image = source_path.suffix.lower() in IMAGE_EXTENSIONS
    try:
        if is_image:
            data = read_image_data(source_path)
            if process_images:
                data = process_image_data(data)
            write_image_data(destination_path, data)
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)
    except OSError as e:
        raise CoreAssetsProcessingError(
            f"Failed to process core asset '{source_path.relative_to(ROOT_DIR)}': {e}"
        ) from e
    return is_image
