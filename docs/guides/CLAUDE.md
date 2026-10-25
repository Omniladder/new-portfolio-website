# docs/guides/ — human-readable documentation

This folder holds documentation for people forking the repo, not for AI agents. Different purpose from `docs/arch/`: ADRs explain *why* the project is built the way it is for whoever's modifying it; guides explain *how to use it* for whoever's running it.

- Write for someone who just cloned the repo and wants to get their own content on the page — no assumed familiarity with this codebase's internals.
- Keep guides honest about current project status (see root `CLAUDE.md`). Don't document fields or behavior that don't exist yet.
- Inline example snippets (e.g. the JSON block in `data-json.md`) are illustrative only and not validated by any test — keep them in sync by hand whenever the thing they demonstrate changes. A stale example is worse than no example.
- The tracked root-level `data.template.json` is different: it IS validated by a test against `src/schema/data.schema.json` on every run, so it can't silently drift. Prefer pointing guides at that file over duplicating its content where possible.
- Current guides: `getting-started.md` (entry point, what a fork touches and the setup steps), `data-json.md` (every `data.json` field), `assets.md` (`assets/`, `assets/download/`, and the tracked `assets/core-assets/`), `deploying.md` (putting the site on a server with `infra/deploy.sh`). The "Current state" sections in each describe what isn't wired up yet; update them as features land.
- README.md links into this folder rather than duplicating its content; update both together when either changes.
