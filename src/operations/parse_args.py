import argparse
from pathlib import Path

from src.utils.log import get_logger
from src.utils.paths import DATA_PATH, display_path

_log = get_logger("parse_args")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse generate.py's command-line arguments.

    Args:
        argv: Arguments to parse, excluding the program name. Defaults to
            ``sys.argv[1:]``.

    Returns:
        argparse.Namespace: Parsed arguments. ``data`` is the Path of the
        JSON file to build from, defaulting to ``DATA_PATH``
        (``ROOT_DIR / "data.json"``). ``no_image_processing`` is True when
        ``--no-image-processing`` was passed, meaning images should be copied
        as-is instead of going through process_image_data().
    """
    parser = argparse.ArgumentParser(
        description="Generate the static site in dist/ from a data file."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DATA_PATH,
        metavar="PATH",
        help="JSON data file to build from (default: data.json at the repo root)",
    )
    parser.add_argument(
        "--no-image-processing",
        action="store_true",
        help="copy images into dist/ as-is, skipping pixelation, dithering, "
        "and palette reduction (faster builds)",
    )
    args = parser.parse_args(argv)
    _log.info(
        "Building from %s%s",
        display_path(args.data),
        " (image processing off)" if args.no_image_processing else "",
    )
    return args
