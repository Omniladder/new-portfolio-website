# 0030 — Agents may edit data.json when the user asks

**Status:** Accepted. Partially supersedes [[0014-generate-data-flag-and-protected-data-json]] and [[0025-smoke-test-real-data-after-template]] (the ban on modifying `data.json`).

## Context

0014 banned agents from creating, overwriting, moving, or deleting `data.json`,
after smoke tests destroyed it. 0025 kept that ban. In practice that meant a
plain content request ("add my phone number to contact") couldn't be finished:
the agent changed the code, then had to hand the user a line to paste into
`data.json` themselves. The user wants agents to make those content edits
directly.

The original failure was never a content edit the user asked for. It was
agents replacing or deleting the file as part of testing.

## Decision

- When the user asks for a content change, agents may edit `data.json` in
  place. Change only the fields the request covers and leave the rest as is.
- Still never delete, move, or recreate `data.json`, and never replace it with
  `data.template.json` or test data. It's gitignored and has no backup.
- Smoke tests still follow 0014/0025: `--data data.template.json` first, then
  a read-only build of the real `data.json`. If the real build fails, don't
  edit `data.json` to make it pass unless the user asks for that change.
- If `data.json` is missing, ask the user. Don't create one.

## Consequences

- Content requests can be finished in one step.
- An edit to `data.json` can't be undone with git, so keep it to the fields
  asked for and tell the user what changed.

## Keywords

data.json, edit, content change, protected, gitignored, phone, contact, profile
