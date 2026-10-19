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


def process_assets() -> None:
    """Process every top-level image in assets/ into dist/assets/.

    Only files directly inside ``assets/`` are processed — subdirectories
    (e.g. ``assets/download/``, which holds non-image downloadable files)
    are left alone, per docs/arch/0013.

    Returns:
        None.
    """
    assets_dir = ROOT_DIR / "assets"
    image_paths = sorted(
        path
        for path in assets_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    for source_path in tqdm(image_paths, desc="Processing assets"):
        process_asset(source_path)

    _log.info(
        "Processed assets/ -> dist/assets/ (%s)",
        pluralize(len(image_paths), "image"),
    )


def process_asset(source_path: Path) -> None:
    """Read, process, and write a single image from assets/ to dist/assets/.

    Args:
        source_path: Path of the image file, somewhere under ROOT_DIR, to
            process. Its path relative to ROOT_DIR is reproduced under
            DIST_DIR, per the mirroring convention in docs/arch/0005.

    Returns:
        None.

    Raises:
        AssetProcessingError: If the image can't be read, processed, or
            written.
    """
    try:
        data = read_image_data(source_path)
        data = process_image_data(data)
        destination_path = DIST_DIR / source_path.relative_to(ROOT_DIR)
        write_image_data(destination_path, data)
    except OSError as e:
        raise AssetProcessingError(
            f"Failed to process asset '{source_path.name}': {e}"
        ) from e
