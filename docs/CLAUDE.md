# docs/ — guidance for AI agents

This folder has five kinds of material, plus a TODO list. They're for different purposes — don't conflate them.

- `docs/arch/` — **decisions already made.** Numbered ADRs explaining *why* the project is structured the way it is. Read these before proposing a structural change; if a decision here conflicts with a request, flag the conflict instead of silently overriding it.
- `docs/design/` — **design decisions and style guides for AI agents.** Numbered, ADR-shaped records for durable non-architectural visual, content, and interaction guidance. Read these before changing presentation; see `docs/design/CLAUDE.md`.
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
| Add, change, or bypass a git hook (pre-commit, etc.) | [0007-pre-commit-runs-tests](arch/0007-pre-commit-runs-tests.md), [0011-linting-with-ruff](arch/0011-linting-with-ruff.md), [0039-drop-large-file-check](arch/0039-drop-large-file-check.md) |
| Add or change how `data.json` is loaded/validated, or edit `src/schema/` | [0008-data-json-schema-validation](arch/0008-data-json-schema-validation.md) |
| Track, untrack, or restructure `data.json` vs. its example/template | [0009-data-json-gitignored-with-tracked-example](arch/0009-data-json-gitignored-with-tracked-example.md) |
| Add/remove a project, change how project pages are generated, or rename a template vs. its output path | [0010-project-pages-from-single-template](arch/0010-project-pages-from-single-template.md) |
| Add/change a linter or formatter, its rules, or `ruff.toml` | [0011-linting-with-ruff](arch/0011-linting-with-ruff.md) |
| Raise, catch, or wrap an exception in `src/operations/`, or add a new error type | [0012-explicit-errors-per-operation](arch/0012-explicit-errors-per-operation.md) |
| Track, untrack, or restructure `assets/` and `assets/download/` contents | [0013-assets-gitignored-with-tracked-placeholders](arch/0013-assets-gitignored-with-tracked-placeholders.md) |
| Run `generate.py` for a test/smoke build, add a CLI flag, or create/modify/delete `data.json` | [0014-generate-data-flag-and-protected-data-json](arch/0014-generate-data-flag-and-protected-data-json.md), [0030-agents-may-edit-data-json-on-request](arch/0030-agents-may-edit-data-json-on-request.md) |
| Edit `data.json` content because the user asked for it | [0030-agents-may-edit-data-json-on-request](arch/0030-agents-may-edit-data-json-on-request.md) |
| Verify a build after a change (real `data.json` only, no template build) | [0033-test-against-data-json-only](arch/0033-test-against-data-json-only.md), [0025-smoke-test-real-data-after-template](arch/0025-smoke-test-real-data-after-template.md) |
| Add an operation, add/change log output or its format, or `print()` from build code | [0015-operations-log-on-completion](arch/0015-operations-log-on-completion.md) |
| Change how `assets/` images get copied/processed into `dist/assets/`, or add an image-manipulation step | [0016-process-assets-image-pipeline](arch/0016-process-assets-image-pipeline.md), [0032-assets-organized-in-subfolders](arch/0032-assets-organized-in-subfolders.md) |
| Reorganize `assets/` into folders, or change which subfolders `process_assets` skips | [0032-assets-organized-in-subfolders](arch/0032-assets-organized-in-subfolders.md) |
| Add an asset the app itself depends on (not per-fork content), or change what's tracked in `assets/core-assets/` | [0017-core-assets-tracked](arch/0017-core-assets-tracked.md) |
| Add or change light/dark theme styling, the theme toggle, or `static/theme-toggle.js` | [0018-light-dark-theme-toggle](arch/0018-light-dark-theme-toggle.md) |
| Add/change a browser/end-to-end test, or anything under `tests/playwright/` | [0019-playwright-e2e-tests](arch/0019-playwright-e2e-tests.md), [0029-playwright-tests-run-against-data-json](arch/0029-playwright-tests-run-against-data-json.md), [0033-test-against-data-json-only](arch/0033-test-against-data-json-only.md) |
| Add a core asset that needs to appear in `dist/`, or change how `assets/core-assets/` is processed/copied | [0042-process-core-assets](arch/0042-process-core-assets.md), [0020-core-assets-copy-pipeline-and-icon-theming](arch/0020-core-assets-copy-pipeline-and-icon-theming.md) |
| Add/change an icon, or add a brand/trademarked mark | [0021-emoji-icons-with-brand-mark-exception](arch/0021-emoji-icons-with-brand-mark-exception.md) |
| Inline an SVG into a template, or change how the header computer image works | [0022-inline-svg-icons-and-real-computer-image](arch/0022-inline-svg-icons-and-real-computer-image.md) |
| Create or change where durable design decisions and AI-facing style guides are recorded | [0023-design-decision-records](arch/0023-design-decision-records.md) |
| Change the site header, or add a new page template that needs it | [0024-shared-header-partial](arch/0024-shared-header-partial.md) |
| Change which theme loads by default | [0026-dark-mode-default](arch/0026-dark-mode-default.md) |
| Add or change an internal link between pages | [0027-explicit-index-html-links](arch/0027-explicit-index-html-links.md) |
| Change the header quote, or add a top-level page that needs its own quote | [0028-per-section-header-quotes](arch/0028-per-section-header-quotes.md) |
| Change how a project page lists its technologies or highlights, the per-technology `featured` flag, or the collapsible Also Used / More highlights sections | [0034-featured-project-technologies](arch/0034-featured-project-technologies.md) |
| Change the education or experience pages, or add another top-level page/nav link | [0035-education-and-experience-pages](arch/0035-education-and-experience-pages.md), [0024-shared-header-partial](arch/0024-shared-header-partial.md), [0028-per-section-header-quotes](arch/0028-per-section-header-quotes.md) |
| Change what the education page shows, the `education` / `terms` / `courses` fields in `data.json`, or the GPA chart | [0036-education-content-model](arch/0036-education-content-model.md), [0035-education-and-experience-pages](arch/0035-education-and-experience-pages.md) |
| Change what the experience page shows, the `experience` / `positions` / `events` / `certifications` fields in `data.json`, the career timeline, or the `build_month` template global | [0037-experience-content-model](arch/0037-experience-content-model.md), [0035-education-and-experience-pages](arch/0035-education-and-experience-pages.md) |
| Change how event cards get their picture, or the `events[].image` field | [0038-event-image-field](arch/0038-event-image-field.md), [0037-experience-content-model](arch/0037-experience-content-model.md) |
| Change how images are pixelated, dithered or color-reduced, `SHRINK_FACTOR` / `PALETTE_SIZE`, or the Pillow dependency | [0041-pixelate-in-reduce-image-quality](arch/0041-pixelate-in-reduce-image-quality.md), [0040-pillow-dither-and-32-color-palette](arch/0040-pillow-dither-and-32-color-palette.md), [0016-process-assets-image-pipeline](arch/0016-process-assets-image-pipeline.md) |
| Add a `generate.py` flag, change `--no-image-processing`, or decide which flags smoke builds use | [0043-no-image-processing-flag](arch/0043-no-image-processing-flag.md), [0014-generate-data-flag-and-protected-data-json](arch/0014-generate-data-flag-and-protected-data-json.md) |
| Deploy the site, or change anything under `infra/` (Ansible playbook, nginx config, `deploy.sh`) | [0044-ansible-deploy-to-nginx-host](arch/0044-ansible-deploy-to-nginx-host.md), [0043-no-image-processing-flag](arch/0043-no-image-processing-flag.md) |
| Change the 404 page, how missing URLs are handled, or add a page served at an unknown depth | [0045-404-page-root-absolute-links](arch/0045-404-page-root-absolute-links.md), [0027-explicit-index-html-links](arch/0027-explicit-index-html-links.md) |
| Add/commit reference images in `docs/refs/`, or edit `.gitignore` rules | [0031-docs-refs-tracked](arch/0031-docs-refs-tracked.md) |

New architectural decisions get a new numbered file in `docs/arch/`, not an edit to an old one (unless the old decision was wrong, in which case mark it Superseded and link forward). New durable design decisions follow the equivalent rule in `docs/design/`.
