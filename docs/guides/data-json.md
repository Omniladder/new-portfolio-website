# Setting up data.json

`data.json` holds all of your site's text content. Along with your files in `assets/` ([assets.md](assets.md)), it's the only thing most forks need to touch. New here? Start with [getting-started.md](getting-started.md).

`data.json` isn't tracked in git (your name, bio, and links are yours, not this repo's), so you start by copying the tracked template:

```bash
cp data.template.json data.json
```

Then edit `data.json` with your own content and run `python3 generate.py`.

## Example

```json
{
  "projects": [
    {
      "project_name": "flashcard-factory",
      "title": "Flashcard Factory",
      "tagline": "Turns lecture notes into study decks",
      "description": "A longer description of what the project does and why you built it.",
      "image": "assets/projects/flashcard-factory/main.png",
      "image_caption": "The deck builder",
      "gallery": [
        { "image": "assets/projects/flashcard-factory/study-mode.png", "caption": "Study mode" },
        { "image": "assets/projects/flashcard-factory/export.png" }
      ],
      "highlights": ["Won Best Educational Hack at HackUMBC 2024"],
      "facts": [
        { "label": "Year", "value": "2024" },
        { "label": "Role", "value": "Backend developer" }
      ],
      "technologies": [
        { "name": "Python", "logo": "assets/logos/pythonLogo.png", "layer": "Backend", "purpose": "API and card generation" },
        { "name": "PostgreSQL", "logo": "assets/logos/postgresLogo.png", "layer": "Database", "purpose": "Stores decks and users" }
      ],
      "links": [
        { "label": "Source", "url": "https://github.com/you/flashcard-factory", "type": "github" },
        { "label": "Live demo", "url": "https://flashcards.example.com", "type": "website" },
        { "label": "Write-up (PDF)", "url": "assets/download/flashcard-factory.pdf", "type": "download" }
      ]
    }
  ]
}
```

This is illustrative, not a file this repo validates automatically. `data.template.json` is checked against the schema by a test on every run; this block is maintained by hand. If you're adding a field to `src/schema/data.schema.json`, update this example in the same change so it never shows something `parse_data()` would reject.

## Fields

The top level has one field, `projects`: a list with one object per project. Fields marked *optional* can be left out; every other project field is required. Fields not listed here are rejected.

| Field | Type | What it is |
|---|---|---|
| `project_name` | text | Short, URL-safe ID, e.g. `flashcard-factory`. Becomes the page's address: `dist/projects/<project_name>/index.html`. Stick to lowercase letters, numbers, and hyphens. |
| `title` | text | The project's display name. |
| `tagline` | text | A one-line summary. |
| `description` | text | The longer explanation, shown as the project page's Background section. Separate paragraphs with a blank line (`\n\n`). |
| `image` | text | Path to the main screenshot in `assets/`, e.g. `assets/projects/flashcard-factory/main.png`. Shown large on the project page (click to enlarge) and as the thumbnail on the projects index. |
| `image_caption` | text, *optional* | Caption under the main screenshot. Defaults to "&lt;title&gt; preview". |
| `gallery` | list, *optional* | Extra screenshots, shown as a thumbnail row at the bottom of the project page. Each entry has `image` (a path in `assets/`) and an optional `caption`. Clicking a thumbnail opens it full size, with Prev/Next to step through every screenshot. |
| `featured` | true/false, *optional* | Show this project in the home page's Featured Projects section and at the top of the projects index. |
| `highlights` | list of text, *optional* | Short bullet points (awards, results, standout features), shown in a Highlights section at the bottom of the page. The first three always show; any more are tucked behind a "More highlights" toggle. |
| `facts` | list, *optional* | Label/value pairs such as Year, Role, Team size, or Status, shown in a Project Facts box in the sidebar. Each entry has `label` and `value`. |
| `technologies` | list | Tools the project uses. Each entry has `name` and `logo` (a path to an image in `assets/`), plus optional `layer` (e.g. "Frontend") and `purpose` (what it does in this project). Mark the main ones `"featured": true` to show them as a large logo grid at the top; the rest are listed underneath in a collapsed "Also Used" section that opens when clicked. Among those, if any has a `layer` or `purpose`, they show as a table with those columns; otherwise as a grid of logos. Can be empty: `[]`. |
| `links` | list | Each entry has `label` (the link text), `url`, and `type`, which is one of `github`, `source`, `linkedin`, `website`, or `download`. On the project page every link becomes a button under the title, so add as many as you like. For a "view source" link use `github` (shown with the GitHub logo), or `source` for any other code host; leave it out if the code isn't public. For `download`, `url` is a path under `assets/download/`. `github` and `linkedin` get a distinct icon on the home page ([docs/arch/0021](../arch/0021-emoji-icons-with-brand-mark-exception.md)); everything else (including `linkedin` itself, since the real logo can't be redistributed) gets a generic one. Can be empty: `[]`. |

Each project gets its own page, rendered from `templates/project.html` ([docs/arch/0010](../arch/0010-project-pages-from-single-template.md)), and is also listed on the projects index page.

## Quotes

The top-level `quotes` object holds the quote shown under your name in the page header. Each top-level section of the site gets its own:

| Field | Type | What it is |
|---|---|---|
| `home` | text | Shown on the home page. |
| `projects` | text | Shown on the projects index and on every individual project page. |
| `education` | text | Optional. Shown on the education page; if left out, that page has no quote. |
| `experience` | text | Optional. Shown on the experience page; if left out, that page has no quote. |

`home` and `projects` are required.

```json
"quotes": {
  "home": "In Your Heart You Know He's Right!",
  "projects": "The purpose of life is not to be happy but to be productive.",
  "education": "Example Education Quote Goes Here",
  "experience": "Example Experience Quote Goes Here"
}
```

## Education

The optional top-level `education` list fills in the education page, one entry per school, most recent first. Leave it out and the page shows a short placeholder. Only `school` and `degree` are required; every section of the page is skipped when its field is missing.

| Field | Type | What it is |
|---|---|---|
| `school` | text | School name, shown as the big title. |
| `degree` | text | Degree earned, e.g. "Bachelor of Science". |
| `subtitle` | text, *optional* | One line under the school name, e.g. your majors and minor. |
| `location` / `dates` | text, *optional* | Shown under the subtitle, e.g. "Salisbury, MD" and "August 2021 – May 2025". |
| `summary` | text, *optional* | Overview paragraph(s). Separate paragraphs with a blank line. |
| `image` / `image_caption` | text, *optional* | Photo in `assets/` (e.g. `assets/education/campus.jpg`) shown beside the overview, with a caption. Click to enlarge. |
| `gallery` | list, *optional* | Extra photos, same shape as a project's `gallery`. |
| `facts` | list, *optional* | Label/value pairs (Majors, Minor, GPA...) shown in a Degree Facts sidebar box. |
| `highlights` | list of text, *optional* | Honors and achievements, shown as a starred list. |
| `links` | list, *optional* | Buttons under the title, same shape as a project's `links`, e.g. a transcript download. |
| `terms` | list, *optional* | Your transcript, most recent term first. Each term has `name` (e.g. "Fall 2024"), `courses`, and optional `gpa` (a number on a 4.0 scale; terms with one appear in the GPA by Term chart) and `honors` (e.g. "Dean's List"). |

Each course in a term's `courses` has `code` and `title`, plus optional `grade`, `credits`, `instructor`, `topic` (for seminars or research courses), `description`, and `projects`: a list of `project_name`s from your `projects` that came out of the course. Those get linked from the course and gathered into a Course Projects box. Credits, course counts, A grades, and term honors are added up automatically for the At a Glance box.

```json
"education": [
  {
    "school": "Example University",
    "degree": "Bachelor of Science",
    "facts": [{ "label": "GPA", "value": "3.9" }],
    "terms": [
      {
        "name": "Fall 2024",
        "gpa": 4.0,
        "honors": "Dean's List",
        "courses": [
          { "code": "CS 101", "title": "Intro to CS", "grade": "A", "credits": 3, "projects": ["flashcard-factory"] }
        ]
      }
    ]
  }
]
```

## Experience

The optional top-level `experience` section fills in the experience page. Leave it out and the page shows a short placeholder. It has an optional `summary` (paragraphs separated by a blank line), optional `links` (buttons at the top, same shape as a project's `links`, e.g. a resume download), and three optional lists, each most recent first.

**`positions`**: your jobs.

| Field | Type | What it is |
|---|---|---|
| `title` / `organization` | text | Job title and employer. |
| `start` | `YYYY-MM` | Start month, e.g. `"2024-06"`. The page shows the date range, works out how long you were there, and places the job on the timeline from this. |
| `end` | `YYYY-MM`, *optional* | End month. Leave it out for your current job: it shows as "Present", and if it's your first position it goes at the top of the page. |
| `location` / `type` | text, *optional* | e.g. "Chantilly, VA" and "Full-time" or "Internship". |
| `summary` | text, *optional* | A paragraph about the role. |
| `highlights` | list of text, *optional* | Accomplishments, shown as a starred list. |
| `technologies` | list, *optional* | Each has `name` and an optional `logo` in `assets/`. Shown on the job and gathered into a Toolbox at the bottom of the page. |
| `projects` | list, *optional* | `project_name`s from your `projects` that came out of the job; linked from it. |

**`events`**: hackathons or similar. Each has `name` and `date` (`YYYY-MM-DD` or `YYYY-MM`, used to place it on the timeline), plus optional `dates` (how the date reads on the page, e.g. "September 28–29, 2024"), `host`, `location`, `role`, `team`, `awards` (a list; award winners get a star), `summary`, `project` (a `project_name`: its picture and a link to it show on the event's card), and `image` (a path under `assets/`, e.g. `assets/events/<event>/logo.png`, shown whole on the card when there's no `project`, for events you didn't build something at, like one you sponsored or judged).

**`certifications`**: each has `name`, `issuer`, and `date` (`YYYY-MM`), plus optional `expires` (`YYYY-MM`), `logo`, and `summary`.

```json
"experience": {
  "positions": [
    { "title": "Cloud Engineer", "organization": "Example Co.", "start": "2025-12",
      "technologies": [{ "name": "AWS", "logo": "assets/logos/awsLogo.png" }] }
  ],
  "events": [
    { "name": "HackUMBC 2024", "date": "2024-09-28", "awards": ["Best Educational Hack"], "project": "testif-ai" }
  ],
  "certifications": [
    { "name": "AWS Certified Cloud Practitioner", "issuer": "Amazon Web Services", "date": "2025-07" }
  ]
}
```

"Present" and how long you've been in a current job are worked out when you run `generate.py`, so rebuild now and then to keep them current.

## Current state

Only `projects` exists so far. Bio, site-wide links, and other sections haven't been designed yet. The templates don't display most of these fields yet either: they're validated, but not all of them show up on the page. This guide, the template, and the schema will grow together as features land.

## Where validation happens

`generate.py` parses `data.json` through `src/operations/parse_data.py`, which checks it against `src/schema/data.schema.json` before anything else runs. If your `data.json` doesn't match the schema, generation fails immediately with a validation error instead of producing a broken site.
