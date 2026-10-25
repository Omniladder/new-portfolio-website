import json
import logging

import pytest

from src.errors.parse_data import DataParseError
from src.operations import parse_data as parse_data_module
from src.operations.parse_data import parse_data
from src.utils.paths import DATA_TEMPLATE_PATH

_SCHEMA = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


def _patch_schema(monkeypatch, tmp_path, schema):
    """Point parse_data's schema constant at a throwaway schema file.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        tmp_path: pytest's per-test temporary directory fixture.
        schema: dict to write out as the schema JSON.

    Returns:
        Path: the fake schema file's path.
    """
    schema_path = tmp_path / "data.schema.json"
    schema_path.write_text(json.dumps(schema))
    monkeypatch.setattr(parse_data_module, "DATA_SCHEMA_PATH", schema_path)
    return schema_path


def test_parse_data_returns_parsed_dict_when_valid(tmp_path, monkeypatch):
    """A JSON file matching the schema is returned as a parsed dict."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    data_path = tmp_path / "data.json"
    data_path.write_text("{}")

    assert parse_data(data_path) == {}


def test_parse_data_raises_on_schema_violation(tmp_path, monkeypatch):
    """A JSON file with fields the schema doesn't allow raises DataParseError."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps({"name": "someone"}))

    with pytest.raises(DataParseError, match=str(data_path)):
        parse_data(data_path)


def test_parse_data_raises_on_malformed_json(tmp_path, monkeypatch):
    """A file that isn't valid JSON raises DataParseError, not a raw JSONDecodeError."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    data_path = tmp_path / "data.json"
    data_path.write_text("{not json")

    with pytest.raises(DataParseError, match=str(data_path)):
        parse_data(data_path)


def test_parse_data_raises_on_missing_file(tmp_path, monkeypatch):
    """A data_path that doesn't exist raises DataParseError, not a raw OSError."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    data_path = tmp_path / "missing.json"

    with pytest.raises(DataParseError, match=str(data_path)):
        parse_data(data_path)


def test_parse_data_defaults_to_data_path(tmp_path, monkeypatch):
    """Calling parse_data() with no argument reads from DATA_PATH."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    default_path = tmp_path / "data.json"
    default_path.write_text("{}")
    monkeypatch.setattr(parse_data_module, "DATA_PATH", default_path)

    assert parse_data() == {}


def test_parse_data_explicit_path_overrides_default(tmp_path, monkeypatch):
    """Passing a path explicitly reads that file instead of DATA_PATH."""
    _patch_schema(monkeypatch, tmp_path, _SCHEMA)
    default_path = tmp_path / "default.json"
    default_path.write_text(json.dumps({"should": "not be read"}))
    monkeypatch.setattr(parse_data_module, "DATA_PATH", default_path)

    other_path = tmp_path / "other.json"
    other_path.write_text("{}")

    assert parse_data(other_path) == {}


def test_data_template_json_matches_schema():
    """data.template.json — the tracked file forks copy to data.json — must
    always validate against the real schema, so it never drifts out of sync
    with what parse_data() actually accepts.

    Only validity is checked, not the exact contents, so the example can be
    edited freely. The site is never built from it (docs/arch/0033).
    """
    assert isinstance(parse_data(DATA_TEMPLATE_PATH), dict)


def test_parse_data_logs_path_and_project_count(tmp_path, monkeypatch, caplog):
    """A successful parse logs the file it validated and how many projects it has."""
    caplog.set_level(logging.INFO, logger="portfolio")
    _patch_schema(monkeypatch, tmp_path, {"type": "object"})
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps({"projects": [{}, {}]}))

    parse_data(data_path)

    assert f"Validated {data_path.resolve()}" in caplog.text
    assert "2 projects" in caplog.text
