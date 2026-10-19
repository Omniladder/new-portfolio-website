# 0009 — data.json is gitignored; a tracked template replaces it at root

**Status:** Accepted

## Context

`data.json` holds one person's personal content (name, bio, links). Tracking it in git means every fork either carries the original owner's content in its history or has to immediately overwrite it — neither is the experience [[0001-overview-and-goals]] wants for "clone and edit `data.json`."

## Decision

- `data.json` is gitignored (`/data.json` in `.gitignore`). It's local, per-fork state, not something this repo's history should contain.
- `data.template.json`, a tracked file at repo root (sitting alongside the gitignored `data.json`), is the starting point people copy (`cp data.template.json data.json`). It must always validate against `src/schema/data.schema.json` (see [[0008-data-json-schema-validation]]) — a test asserts this directly on every run, so it can never silently drift out of sync with the schema.
- `docs/guides/data-json.md` is the human-readable walkthrough of this process, in a new `docs/guides/` folder for user-facing documentation (distinct from `docs/arch/`'s agent-facing ADRs — see `docs/guides/CLAUDE.md`). It also embeds an illustrative example JSON snippet inline; that snippet is maintained by hand and not itself validated — `data.template.json` is the one source of truth that's test-enforced. README.md links to the guide rather than duplicating the instructions.

## Consequences

- A fresh clone has no `data.json` until someone runs the copy step; `generate.py` will fail with a "file not found" error until they do, which is expected and not something to special-case away.
- Whoever adds real fields to the schema must update `data.template.json` (test-enforced) and, by hand, the inline example in `docs/guides/data-json.md` — the latter has no automated check, so it's a reminder to future changes, not a guarantee.

## Keywords

data.json, gitignore, data.template.json, template, docs/guides, fork workflow
