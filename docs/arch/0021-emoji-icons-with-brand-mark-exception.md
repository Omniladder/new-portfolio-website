# 0021 — Icons are native color emoji, with a brand-mark exception for GitHub

**Status:** Accepted, with two parts superseded by
[[0022-inline-svg-icons-and-real-computer-image]]: the GitHub mark is now
inlined rather than mask-image'd, and the header computer icon is a real
tracked image, not an emoji. Supersedes the icon-theming portion of
[[0020-core-assets-copy-pipeline-and-icon-theming]] (that ADR's
`copy_core_assets` pipeline decision still stands).

## Context

0020 gave every icon (computer, home, folder, user, skills, mail, link,
download, star, github) the same treatment: a single-color SVG from
[pixelarticons](https://github.com/halfmage/pixelarticons), tinted via a CSS
`mask-image` + `currentColor` so it reads correctly in both themes.

Two problems showed up once it was actually viewed:

- The icons didn't render at all in some cases — `mask-image`/
  `-webkit-mask-image` loading a same-origin SVG is exactly the kind of
  resource Chrome is inconsistent about when a page is opened via `file://`
  instead of a server, which is a completely normal way to preview a static
  site like this one.
- Visually, they were the wrong style. `docs/refs/light_mode_idea.png` and
  `dark_mode_idea.png` use small full-color pictures next to each heading
  (a document, a folder, a hammer, an envelope, a penguin) — closer to
  emoji or clip art than flat single-color line icons. The masked
  monochrome glyphs read as a UI icon font, not "a little picture," which
  wasn't the look being asked for.

## Decision

- **Default: native Unicode emoji**, written directly into
  `templates/home.html` as text (e.g. `📁`, `👤`, `🔨`, `✉️`, `🔗`, `🏠`,
  `📝`, `📄`, `💾`, `⭐`), wrapped in `<span class="icon" aria-hidden="true">`
  only for spacing, not masking. No asset file, no request, no mask
  compositing — they render wherever the OS has a color emoji font, which
  fixes both problems above: there's nothing that can fail to load, and
  they're full-color pictures like the reference mockups, not tinted
  glyphs.
- **Exception: GitHub's mark.** It's a real, recognizable brand symbol
  someone would expect to see as itself, not as a generic icon, and there's
  no emoji for it. `assets/core-assets/icons/github.svg` is the official
  mark from [Simple Icons](https://github.com/simple-icons/simple-icons)
  (CC0-1.0, no attribution required), masked with `currentColor` the same
  way 0020 did it — appropriate here because the mark itself is a single
  silhouette, not multi-color art.
- **LinkedIn does not get the same treatment.** Simple Icons explicitly
  excludes LinkedIn (and Visual Studio, Playwright) from redistribution at
  Microsoft's request — see their `CONTRIBUTING.md`'s "Trademarked icons we
  cannot include" list. That's a real takedown-driven exclusion from the
  project a GitHub mark was sourced from, not a missing file to route
  around by pulling the mark from somewhere else. `profile.links[].type`
  gained a `"linkedin"` enum value (alongside the existing `"github"`,
  `"website"`, `"download"`) so a LinkedIn link can still be identified
  data-driven rather than by matching its label string, but it renders as
  a 💼 emoji instead of the actual logo.
- Icon choice stays keyed off `link.type` / section concept, never off a
  label string, for the same fork-portability reason as 0020.

## Consequences

- `assets/core-assets/icons/` now holds exactly one file, `github.svg`,
  down from the 11-icon pixelarticons set 0020 shipped; the rest were
  deleted since nothing references them anymore.
- Any future "give this concept a real brand mark" request needs the same
  license check 0020/0021 did — confirm the source actually permits
  redistributing that specific mark before adding it, and if it's a
  trademark-excluded brand (check the source library's own exclusion list
  first), don't substitute a different source to get around that.
- Emoji rendering depends on the viewer's OS/browser having a color emoji
  font; on a system with none, these degrade to the Unicode codepoint's
  fallback glyph (not a broken-image icon), which is an acceptable
  trade-off for a personal portfolio site.

## Keywords

icons, emoji, github, linkedin, simple-icons, trademark, brand marks,
mask-image, currentColor, pixelarticons
