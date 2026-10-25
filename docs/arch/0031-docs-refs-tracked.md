# 0031 — `docs/refs/` images are tracked in git

**Status:** Accepted

## Context

`docs/refs/` holds the design mockups (`*_project_home.png`, `*_project.png`) that `docs/refs/CLAUDE.md` describes as the visual target for the project templates. Unlike `assets/` ([[0013-assets-gitignored-with-tracked-placeholders]]), they aren't one fork's personal content. They are shared design reference that agents and contributors need on a fresh clone. The root `.gitignore` had been replaced with a venv-style `*` stub, which silently ignored every new file, these images included.

## Decision

- Everything in `docs/refs/`, binary images included, is tracked and committed like any other doc.
- `.gitignore` must never contain a rule that matches `docs/refs/`. A comment in `.gitignore` says so.
- The root `.gitignore` was rebuilt from the rules in [[0009-data-json-gitignored-with-tracked-example]], [[0013-assets-gitignored-with-tracked-placeholders]] and [[0017-core-assets-tracked]], plus `/dist/` and Python tooling caches. A catch-all `*` is not allowed there.

## Consequences

- A fresh clone includes the mockups, so template and styling work has its visual target available.
- The images add to the repo's size. Keep them at a reasonable resolution and don't add near-duplicates.
- Personal content still must not go in `docs/refs/`, because anything there ends up in every fork's history.

## Keywords

docs/refs, gitignore, reference images, mockups, tracked docs
