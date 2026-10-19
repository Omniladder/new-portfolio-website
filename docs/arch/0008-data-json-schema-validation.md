# 0008 — data.json is validated against a JSON Schema

**Status:** Accepted

## Context

[[0003-data-json-source-of-truth]] already calls `data.json`'s shape "effectively the project's public API" and flags that validation would need to live in `src/utils` once generation logic exists. That logic now exists.

## Decision

- A new build step, `parse_data()` in `src/operations/parse_data.py`, loads a JSON file and validates it against a schema before returning the parsed content as a `dict`.
- The schema lives in a new `src/schema/` directory, alongside `src/operations/` and `src/utils/` — it's an internal build-time input consumed by `src/operations/parse_data.py`, not something a fork is meant to edit directly (unlike `templates/` or `static/`). `src/schema/data.schema.json` is the schema for `data.json`.
- Validation uses the `jsonschema` library (added to `requirements.txt`, since `generate.py` needs it at runtime, not just for tests).
- `generate.py` calls `parse_data()` (defaulting to `DATA_PATH`) as its first step, so a malformed `data.json` fails generation immediately with a validation error rather than producing a broken or partial site.
- For now, `src/schema/data.schema.json` declares `data.json` as an object with no properties and `additionalProperties: false` — i.e. the only valid document is `{}`. No content fields have been designed yet; the schema will gain real fields alongside the generation logic that consumes them, not ahead of it.

## Consequences

- Adding a content field to `data.json` means updating `src/schema/data.schema.json` in the same change, or `parse_data()` will reject it.
- `data.template.json` (see [[0009-data-json-gitignored-with-tracked-example]]) must stay in lockstep with the schema — a test asserts it parses successfully.
- `jsonschema` becomes a runtime dependency, not just a dev one.

## Keywords

data.json, schema, validation, jsonschema, parse_data, src/schema, data schema
