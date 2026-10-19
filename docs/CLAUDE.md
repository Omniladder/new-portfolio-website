# docs/ — guidance for AI agents

This folder has three kinds of material. They're for different purposes — don't conflate them.

- `docs/arch/` — **decisions already made.** Numbered ADRs explaining *why* the project is structured the way it is. Read these before proposing a structural change; if a decision here conflicts with a request, flag the conflict instead of silently overriding it.
- `docs/refs/` — **visual inspiration only.** Images/links collected for the 90s aesthetic. Not consumed by `generate.py`, not content, not something `data.json` points to. See `docs/refs/CLAUDE.md`.
- `docs/guides/` — **human-readable, user-facing documentation.** How-to material for someone forking the repo (e.g. setting up `data.json`), not rationale for agents. See `docs/guides/CLAUDE.md`.

## When to check docs/arch/

| If you're about to... | Read this first |
|---|---|
| Add a framework, bundler, build tool, or restructure the generation pipeline | [0001-overview-and-goals](arch/0001-overview-and-goals.md) |
| Add a second stylesheet, component-level CSS, or more than one JS file to a template | [0002-single-css-and-js-per-template](arch/0002-single-css-and-js-per-template.md) |
| Hardcode content in a template, or change what `data.json` is expected to contain | [0003-data-json-source-of-truth](arch/0003-data-json-source-of-truth.md) |
| Put logic directly in `generate.py`, or write to/read from `dist/` as persistent state | [0004-thin-entrypoint-src-layout](arch/0004-thin-entrypoint-src-layout.md) |
| Decide what `dist/` paths a new mirrored directory or asset should land at | [0005-dist-mirrors-root-paths](arch/0005-dist-mirrors-root-paths.md) |
| Add a test, restructure `tests/`, add a test dependency, or decide whether something needs a test | [0006-testing-framework](arch/0006-testing-framework.md) |
| Add, change, or bypass a git hook (pre-commit, etc.) | [0007-pre-commit-runs-tests](arch/0007-pre-commit-runs-tests.md), [0011-linting-with-ruff](arch/0011-linting-with-ruff.md) |
| Add or change how `data.json` is loaded/validated, or edit `src/schema/` | [0008-data-json-schema-validation](arch/0008-data-json-schema-validation.md) |
| Track, untrack, or restructure `data.json` vs. its example/template | [0009-data-json-gitignored-with-tracked-example](arch/0009-data-json-gitignored-with-tracked-example.md) |
| Add/remove a project, change how project pages are generated, or rename a template vs. its output path | [0010-project-pages-from-single-template](arch/0010-project-pages-from-single-template.md) |
| Add/change a linter or formatter, its rules, or `ruff.toml` | [0011-linting-with-ruff](arch/0011-linting-with-ruff.md) |
| Raise, catch, or wrap an exception in `src/operations/`, or add a new error type | [0012-explicit-errors-per-operation](arch/0012-explicit-errors-per-operation.md) |

New decisions get a new numbered file in `docs/arch/`, not an edit to an old one (unless the old decision was wrong, in which case mark it Superseded and link forward).
