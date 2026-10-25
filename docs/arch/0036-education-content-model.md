# 0036 — Education page content model

**Status:** Accepted. Fills in the content [[0035-education-and-experience-pages]] deferred.

## Context

0035 shipped the education page as an empty placeholder. The previous React
portfolio's education page had school facts (majors, minor, concentrations,
GPA), a campus photo, and a semester-by-semester transcript where each course
expanded to show its description, instructor, and credits. That content needs
a home in `data.json` ([[0003-data-json-source-of-truth]]) shaped so another
fork can describe their own schools.

## Decision

- `data.json` gains an **optional** top-level `education` array, one entry per
  school, most recent first. Only `school` and `degree` are required; every
  other field (`subtitle`, `location`, `dates`, `summary`, `image`,
  `image_caption`, `gallery`, `facts`, `highlights`, `links`, `terms`) is
  optional and its section is skipped when unset. An existing `data.json`
  with no `education` key still validates, and the page shows a placeholder.
- `gallery`, `facts`, and `links` reuse the project schema's shapes, and the
  page reuses the project page's hero, sidebar layout, boxes, starred
  highlight list, and CSS-only lightbox, so it reads as part of the same site.
- `terms[]` holds the transcript: `name`, optional `gpa` (number on a 4.0
  scale) and `honors`, and `courses[]` with `code`, `title`, and optional
  `grade`, `credits`, `instructor`, `topic`, `description`, `projects`.
  Courses render as native `<details>` rows, so there's no per-template JS
  ([[0002-single-css-and-js-per-template]]).
- `courses[].projects` lists `project_name` slugs from `projects[]`. Matching
  courses get a link to the project page and are collected into a Course
  Projects box. Unknown slugs are ignored, not errors.
- The template derives everything else: total credits, course and A-grade
  counts, term-honor count (At a Glance box), and a single-series GPA-by-term
  bar chart on a fixed 0–4.0 scale, oldest term first, with each value printed
  next to its bar.
- `templates/education.html` loops over every school, prefixing each section
  and lightbox id with `school-<n>` so several schools can share the page.
- Education images live under `assets/education/` (the existing
  `process_assets` pipeline picks them up, [[0032-assets-organized-in-subfolders]]).

## Consequences

- Derived totals are only as accurate as the transcript in `data.json`;
  official figures (like a major GPA) go in `facts` as text.
- The chart's 0–4.0 scale assumes 4.0-scale GPAs; a school on another scale
  should leave `gpa` unset and put the figure in `facts`.
- `generate_pages` needs no changes: the template reads `education` from the
  full data context.

## Keywords

education, transcript, courses, terms, GPA, chart, school, degree, honors,
dean's list, course projects, data.json, schema, education.html
