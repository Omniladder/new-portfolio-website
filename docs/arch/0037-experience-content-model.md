# 0037 — Experience page content model

**Status:** Accepted. Fills in the content [[0035-education-and-experience-pages]] deferred.

## Context

0035 shipped the experience page as an empty placeholder. The previous React
portfolio's experience page was one vertical timeline mixing jobs,
hackathons, a certification, and school milestones, each a dated card with a
paragraph. The resume adds per-job technologies and accomplishment bullets.
That content needs a home in `data.json` ([[0003-data-json-source-of-truth]])
shaped so another fork can describe their own career. School milestones
already live on the education page ([[0036-education-content-model]]), so
they're left out here.

## Decision

- `data.json` gains an **optional** top-level `experience` object with an
  optional `summary`, `links`, and three lists, each most recent first:
  - `positions[]`: jobs. `title`, `organization`, and `start` are required;
    `end`, `location`, `type`, `summary`, `highlights`, `technologies`
    (`name` plus an optional `logo`), and `projects` are optional.
  - `events[]`: hackathons and similar events. `name` and `date` are
    required; `host`, `location`, `dates`, `role`, `team`, `awards`,
    `summary`, and `project` are optional.
  - `certifications[]`: `name`, `issuer`, and `date` required; `expires`,
    `logo`, and `summary` optional.

  Three typed lists, not one list with a `kind` field, so each shape
  validates on its own and the schema documents itself.
- Job dates are machine-readable months (`YYYY-MM`); the template derives
  the displayed range, the duration ("1 yr 5 mos"), and the timeline from
  them, so dates aren't written twice. Events take `YYYY-MM(-DD)` for
  placement plus an optional free-text `dates` for display, since
  hackathons need day ranges.
- A job with no `end` is ongoing and runs to "Present". To know when "now"
  is, `render_template_to_dist` exposes a `build_month` global (`YYYY-MM`,
  the build's current month) to every template, next to `inline_svg`. A
  rebuild is needed for durations to advance.
- If the first position has no `end`, the hero shows it as the current
  role ("Currently"); otherwise the hero is just titled Experience.
- The template derives everything else: a Gantt-style timeline (a bar per
  job, oldest at the top, plus marker rows for events and certifications on
  a whole-year axis; ongoing jobs are striped and award-winning events get a
  star, so neither relies on color alone), At a Glance counts, and a Toolbox
  that merges every job's technologies, most-used first.
- `positions[].projects` and `events[].project` are `project_name` slugs
  from `projects[]`, like courses on the education page. An event's card
  shows its project's `image` and links to the project page. Unknown slugs
  are ignored, not errors.
- The page reuses the project page's hero, sidebar layout, and boxes and the
  education page's glance list and fact list, so it reads as part of the
  same site. New rules live in an "Experience page" section of
  `static/styles.css` ([[0002-single-css-and-js-per-template]]); no JS.

## Consequences

- Durations and the "Present" end of the timeline are as of the last build,
  not the visitor's date. That's deliberate: the site is static, and a
  per-template script just for this isn't worth it.
- Without an `experience` key the page keeps its placeholder, so an
  existing `data.json` still validates and builds.
- `generate_pages` needs no changes: the template reads `experience` from
  the full data context.

## Keywords

experience, jobs, positions, work history, hackathons, events, awards,
certifications, timeline, toolbox, build_month, data.json, schema,
experience.html
