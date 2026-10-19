# 0022 — GitHub's mark is inlined, the header computer icon is a real image

**Status:** Accepted. Supersedes part of
[[0021-emoji-icons-with-brand-mark-exception]].

## Context

0021 kept GitHub's mark as a `mask-image`-loaded external SVG (the one
exception to the new emoji-based icons), reasoning that it was "appropriate
here" without re-checking whether it had the same `file://` loading problem
0021 had just diagnosed and fixed for every other icon. It did: opening the
built site directly (not through a server) still showed no GitHub icon,
for the identical reason 0021 already explained — `mask-image` loading a
same-origin resource is unreliable outside a server context.

Separately, the header's computer icon was changed to a 🖥️ emoji in 0021
to fix the same loading problem. That fixed the bug, but it's not what was
wanted there specifically: a plan to keep developing that one graphic
further (swap it out, make it distinctive) needs it to be an actual tracked
image file, not a font glyph with no file behind it to replace.

## Decision

- **GitHub's mark is now inlined directly into the rendered HTML**, not
  referenced from CSS. `src/utils/render.py` gained `inline_svg(relative_path)`,
  registered as a Jinja global, which reads an SVG file's raw contents at
  build time; `templates/home.html` calls
  `{{ inline_svg('assets/core-assets/icons/github.svg') | safe }}` inside the
  icon `<span>`. `static/styles.css` themes it with `.icon-github-mark svg {
  fill: currentColor; }` — this works now because the `<svg>` is truly part
  of the page's DOM, not a separate resource, so there's nothing to fail to
  load and `currentColor` resolves against the surrounding CSS normally.
- **The header computer icon is a real tracked image**, not an emoji:
  `assets/core-assets/icons/computer.svg`, the "Desktop computer" icon from
  Microsoft's [Fluent Emoji](https://github.com/microsoft/fluentui-emoji)
  set (MIT-licensed, Color style), referenced with a plain `<img>` tag.
  A plain `<img src="...">` load is reliable under `file://` the same way
  `profile.picture` and the skills-table tech logos already are — it's
  specifically `mask-image`/`background-image` compositing of local
  resources that's unreliable there, not `<img>` itself. Sized via
  `.computer-icon { width: 72px; height: 72px; }` rather than `font-size`,
  since it's no longer text.
- Both are real files under `assets/core-assets/icons/`, still copied into
  `dist/` by `copy_core_assets` ([[0020-core-assets-copy-pipeline-and-icon-theming]]),
  and still subject to the same license-check requirement 0020/0021 set:
  Fluent Emoji is MIT, confirmed before use.
- Emoji stays the default for every other icon (0021's reasoning there is
  unaffected — those were never loaded from a file in the first place, so
  they don't have this problem).

## Consequences

- `inline_svg()` only makes sense for same-repo, trusted SVG content — it
  writes the file's raw text straight into the page via `| safe`, with no
  sanitization. Fine for `assets/core-assets/`, not something to point at
  user-supplied or `data.json`-sourced paths.
- `assets/core-assets/icons/` now holds `github.svg` and `computer.svg`.
- Verified by rendering `dist/index.html` directly via `file://` (no
  server) and confirming both icons show up, which is the exact scenario
  that broke twice before this fix.

## Keywords

inline_svg, mask-image, file://, computer icon, fluentui-emoji, github mark,
jinja global
