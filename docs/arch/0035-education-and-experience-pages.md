# 0035 — Education and Experience top-level pages

**Status:** Accepted.

## Context

The site had two top-level sections, Home and Projects. Education and
work experience need their own pages rather than more boxes on the home
page. Their content model isn't designed yet, but the pages, navigation,
and build wiring can land first so content can be filled in later.

## Decision

- Two new templates, `templates/education.html` and
  `templates/experience.html`, render to `dist/education/index.html` and
  `dist/experience/index.html`. They set `current_page` to `"education"` /
  `"experience"`, include the shared header ([[0024-shared-header-partial]]),
  and have an empty `<main>` for now.
- `generate_pages` gains `generate_education()` and `generate_experience()`,
  one function per page, following the existing `generate_projects_home()`
  pattern and raising `PageGenerationError` on failure.
- The header nav and every page's footer nav link to both pages, using
  explicit `index.html` paths ([[0027-explicit-index-html-links]]).
- `quotes.education` and `quotes.experience` are added to the schema as
  **optional** keys ([[0028-per-section-header-quotes]]). The header omits
  the quote line when `quotes[current_page]` is unset, so an existing
  `data.json` keeps validating and building without edits.
- No `data.json` content for education or experience exists yet; that
  schema lands with the page content.

## Consequences

- Five page generators now run (home, projects index, project pages,
  education, experience), and the build log counts them.
- A fork without the new quotes gets pages with no header quote rather
  than an empty `“”`.
- The footer nav is still duplicated in each template; adding another
  top-level page means editing every footer, or extracting a footer partial.

## Keywords

education, experience, new page, top-level page, nav, footer, quotes,
current_page, generate_pages, generate_education, generate_experience
