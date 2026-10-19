# docs/ — guidance for AI agents

This folder has four kinds of material, plus a TODO list. They're for different purposes — don't conflate them.

- `docs/arch/` — **decisions already made.** Numbered ADRs explaining *why* the project is structured the way it is. Read these before proposing a structural change; if a decision here conflicts with a request, flag the conflict instead of silently overriding it.
- `docs/refs/` — **visual inspiration only.** Images/links collected for the 90s aesthetic. Not consumed by `generate.py`, not content, not something `data.json` points to. See `docs/refs/CLAUDE.md`.
- `docs/guides/` — **human-readable, user-facing documentation.** How-to material for someone forking the repo (e.g. setting up `data.json`), not rationale for agents. See `docs/guides/CLAUDE.md`.
- `docs/examples/` — **example projects (placeholder, empty for now).** Reserved for complete example forks (sample `data.json` + assets). See `docs/examples/CLAUDE.md`.
- `docs/TODO.md` — **deferred work.** Agreed-on things to come back to that aren't decisions yet. When one becomes a real decision, it gets an ADR and comes off the list.

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
| Track, untrack, or restructure `assets/` and `assets/download/` contents | [0013-assets-gitignored-with-tracked-placeholders](arch/0013-assets-gitignored-with-tracked-placeholders.md) |
| Run `generate.py` for a test/smoke build, add a CLI flag, or create/modify/delete `data.json` | [0014-generate-data-flag-and-protected-data-json](arch/0014-generate-data-flag-and-protected-data-json.md) |
| Add an operation, add/change log output or its format, or `print()` from build code | [0015-operations-log-on-completion](arch/0015-operations-log-on-completion.md) |
| Change how `assets/` images get copied/processed into `dist/assets/`, or add an image-manipulation step | [0016-process-assets-image-pipeline](arch/0016-process-assets-image-pipeline.md) |
| Add an asset the app itself depends on (not per-fork content), or change what's tracked in `assets/core-assets/` | [0017-core-assets-tracked](arch/0017-core-assets-tracked.md) |
| Add or change light/dark theme styling, the theme toggle, or `static/theme-toggle.js` | [0018-light-dark-theme-toggle](arch/0018-light-dark-theme-toggle.md) |
| Add/change a browser/end-to-end test, or anything under `tests/playwright/` | [0019-playwright-e2e-tests](arch/0019-playwright-e2e-tests.md) |
| Add a core asset that needs to appear in `dist/`, or change how `assets/core-assets/` is copied | [0020-core-assets-copy-pipeline-and-icon-theming](arch/0020-core-assets-copy-pipeline-and-icon-theming.md) |
| Add/change an icon, or add a brand/trademarked mark | [0021-emoji-icons-with-brand-mark-exception](arch/0021-emoji-icons-with-brand-mark-exception.md) |
| Inline an SVG into a template, or change how the header computer image works | [0022-inline-svg-icons-and-real-computer-image](arch/0022-inline-svg-icons-and-real-computer-image.md) |

New decisions get a new numbered file in `docs/arch/`, not an edit to an old one (unless the old decision was wrong, in which case mark it Superseded and link forward).
