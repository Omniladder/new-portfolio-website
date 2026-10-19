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
        (``ROOT_DIR / "data.json"``).
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
    args = parser.parse_args(argv)
    _log.info("Building from %s", display_path(args.data))
    return args
