# 0026 — Dark mode is the default theme

**Status:** Accepted. Supersedes the "light mode is the default" part of
[[0018-light-dark-theme-toggle]]; the rest of 0018 still stands.

## Context

0018 made light the default theme and dark the opt-in. The site owner
prefers the dark theme and wants it to be what every visitor sees first,
on every page.

## Decision

- **Dark is the default.** With no stored preference, every page loads in
  the dark theme. The toggle switches to light, and the choice is still
  remembered in `localStorage` under `theme`.
- `static/theme-toggle.js` applies `light` only when the stored value is
  `"light"`; anything else, including no value, gives `dark`.
- `static/styles.css` defines the dark palette on `:root, [data-theme="dark"]`
  and the light palette as the `[data-theme="light"]` override. The
  starfield applies to `:root:not([data-theme="light"]) body`. Theme-
  independent variables (fonts) sit in their own `:root` block.
- Page templates ship `<html data-theme="dark">`, and the shared header
  ([[0024-shared-header-partial]]) renders the toggle as "Light Mode" with
  `aria-pressed="true"`. The first paint already matches the default, and
  with JavaScript off the page is still dark.

## Consequences

- Returning visitors who chose dark before keep dark; anyone who picked
  light keeps light.
- Visitors with JavaScript disabled get the dark theme and can't switch it.
- The dark-mode twinkle (see `docs/TODO.md`) now runs for everyone by
  default, so whether to keep it matters more.
- `tests/playwright/test_home.py` expects dark on first load.

## Keywords

dark mode, default theme, data-theme, theme-toggle.js, localStorage,
prefers dark, starfield
