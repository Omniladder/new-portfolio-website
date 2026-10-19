import json
from pathlib import Path

import jsonschema

from src.errors.parse_data import DataParseError
from src.utils.log import get_logger, pluralize
from src.utils.paths import DATA_PATH, DATA_SCHEMA_PATH, display_path

_log = get_logger("parse_data")


def parse_data(data_path: Path = None) -> dict:
    """Load a JSON data file and validate it against the data schema.

    Args:
        data_path: Path to the JSON file to load. Defaults to
            ``DATA_PATH`` (``ROOT_DIR / "data.json"``).

    Returns:
        dict: The parsed JSON content, once it has validated against the
        schema at ``DATA_SCHEMA_PATH``.

    Raises:
        DataParseError: If data_path or the schema file can't be read as
            JSON, or if data_path doesn't match the schema.
    """
    if data_path is None:
        data_path = DATA_PATH
    try:
        data = json.loads(data_path.read_text())
        schema = json.loads(DATA_SCHEMA_PATH.read_text())
        jsonschema.validate(instance=data, schema=schema)
    except (OSError, json.JSONDecodeError) as e:
        raise DataParseError(f"Failed to read or parse {data_path}: {e}") from e
    except jsonschema.ValidationError as e:
        raise DataParseError(
            f"{data_path} does not match the schema: {e.message}"
        ) from e
    _log.info(
        "Validated %s against the schema (%s)",
        display_path(data_path),
        pluralize(len(data.get("projects", [])), "project"),
    )
    return data
