# 0013 — assets/ contents are gitignored; only the folder structure is tracked

**Status:** Accepted

## Context

`assets/` and `assets/download/` hold one person's images and downloadable files (headshots, resume, project screenshots, tech logos used on their pages). Tracking these in git has the same problem [[0009-data-json-gitignored-with-tracked-example]] solved for `data.json`: every fork would carry the original owner's personal files in its history. Unlike `data.json`, there's no single template file to swap in — assets are a pile of arbitrarily-named binary files, not one JSON document.

## Decision

- The contents of `/assets/` and `/assets/download/` are gitignored, not the directories themselves. `.gitignore` uses the standard "ignore all, then un-ignore the placeholder" idiom:
  ```
  /assets/*
  !/assets/.gitkeep
  !/assets/download/
  /assets/download/*
  !/assets/download/.gitkeep
  ```
- `assets/.gitkeep` and `assets/download/.gitkeep` are the only tracked files under `assets/`, so the directories exist on a fresh clone even though they're empty.
- Whoever forks the repo drops their own images into `assets/` and their own downloadable files into `assets/download/`; `data.json` (per [[0003-data-json-source-of-truth]]) references them by filename.

## Consequences

- A fresh clone has empty `assets/` and `assets/download/` directories; `generate.py` will fail to find referenced images/files until the user adds their own, same expected-failure shape as a missing `data.json`.
- There is no tracked example asset to validate against (unlike `data.template.json`), because there's no fixed schema for binary filenames — `docs/guides/` is the place to describe what's expected, by hand.

## Keywords

assets, gitignore, .gitkeep, placeholder, per-fork content, fork workflow
