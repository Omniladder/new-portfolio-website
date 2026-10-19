from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def read_image_data(path: Path) -> bytes:
    """Read an image file's raw bytes.

    Args:
        path: Path to the image file to read.

    Returns:
        bytes: The file's raw contents.
    """
    return path.read_bytes()


def process_image_data(data: bytes) -> bytes:
    """Manipulate raw image bytes before they're written back out.

    Currently a no-op passthrough; this is the hook future image processing
    (resizing, recompression, etc.) will plug into.

    Args:
        data: Raw image bytes, as returned by read_image_data().

    Returns:
        bytes: The (currently unmodified) image bytes.
    """
    return data


def write_image_data(path: Path, data: bytes) -> None:
    """Write raw image bytes to a file, creating parent directories as needed.

    Args:
        path: Destination path to write the image bytes to.
        data: Raw image bytes to write.

    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
