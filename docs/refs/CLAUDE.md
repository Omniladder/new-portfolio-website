# docs/refs/ — visual reference material

This folder holds reference images and links used for visual/design inspiration (90s web aesthetic: tiled backgrounds, marquees, visitor counters, table-based layouts, etc.).

Everything in this folder, images included, is tracked and committed ([0031](../arch/0031-docs-refs-tracked.md)), so never add personal files here. Nothing here is read by `generate.py` or referenced from `data.json`. If a design idea from this folder gets adopted, the decision belongs in `docs/arch/` or `docs/design/` (see `docs/CLAUDE.md`) and the actual asset, if needed at runtime, belongs in `assets/`.

Check this folder when asked to make styling decisions or when `static/styles.css` needs direction on "what should this look like."

## Images

The four images are mockups of the two project page templates, each in both themes. They are the main visual target for `templates/project_home.html` and `templates/project.html`, both now built. The templates deliberately depart from the mockups in places: they keep the shared header and boxed sections of the rest of the site, drop the Deployment section, show project links as buttons under the title, and add a gallery, highlights, and facts.

| Image | Template it targets | Theme |
|---|---|---|
| `dark_mode_project_home.png` | `templates/project_home.html` (projects index, `projects/index.html`) | Dark, the default ([0026](../arch/0026-dark-mode-default.md)) |
| `light_mode_project_home.png` | `templates/project_home.html` | Light, the toggle palette ([0018](../arch/0018-light-dark-theme-toggle.md)) |
| `dark_mode_project.png` | `templates/project.html` (one page per project, [0010](../arch/0010-project-pages-from-single-template.md)) | Dark |
| `light_mode_project.png` | `templates/project.html` | Light |

### Project home (`*_project_home.png`)

Layout to take from these:

- Shared header (name, title, computer image, top nav). This already exists as `templates/partials/header.html` ([0024](../arch/0024-shared-header-partial.md)); the mockup confirms it, it doesn't redefine it.
- Two columns: a left sidebar (site navigation, a list of projects, a site info / visitor counter box) and a main "Project Directory" column.
- One entry per project: title link plus short tagline, a paragraph description, an "Enter project page »" link, and a framed screenshot on the right. Entries are separated by horizontal rules.
- A "Project Index" table below, with Project and Focus columns, one row per project.
- A footer with "best viewed with" badges, a W3C badge, and (in dark mode) the under-construction banner.

### Project page (`*_project.png`)

Layout to take from these:

- The same shared header and footer as the project home.
- The project's title and tagline at the top of the main column, plus a "« Back to Project Directory" link in dark mode.
- A left sidebar with three boxes: "On this page" anchors to the sections, project links ("View source", "Visit website"), and a list of all projects.
- Main sections, each with an icon heading: Background (prose), Application Preview (framed screenshot with a caption), Technologies (a Layer / Technology / Purpose table), Deployment (prose).
- Prev/next navigation at the bottom ("« COSMOS", "Back to all projects", "Lambda Check »").

### How the two themes differ

The dark mockups are the louder, more 90s version: starfield background, yellow/red/cyan headings, bracketed nav links (`[ Home ]`), a blue table header, under-construction graphics, a digit-style visitor counter. The light mockups are calmer: a gray textured page around a bordered white frame, a lavender sidebar, blue serif headings, pipe-separated nav links, and a lavender table header. The layout of each page is the same in both themes, so only colors, backgrounds, and decorative extras should differ. That matches [0018](../arch/0018-light-dark-theme-toggle.md): one structure, with the palette switched through CSS variables in `static/styles.css`.

### What not to copy literally

- **Content.** The names, project titles (COSMOS, Chapp., Lambda Check), descriptions, technology rows, links, dates, and visitor numbers are sample data. Each of them must come from `data.json` ([0003](../arch/0003-data-json-source-of-truth.md)), so the schema in `src/schema/data.schema.json` may need fields for them (tagline, screenshot, technologies table, source/site links, sections).
- **Icons.** The mockups use clip-art icons. Use the icon approach recorded in [0020](../arch/0020-core-assets-copy-pipeline-and-icon-theming.md), [0021](../arch/0021-emoji-icons-with-brand-mark-exception.md), and [0022](../arch/0022-inline-svg-icons-and-real-computer-image.md), not new `<img>` clip art.
- **Small differences between the dark and light versions.** The two themes don't match on details like sidebar box titles ("Browse Projects" vs. "Projects"), the "Quick Info" box, and the heading icons. Treat these as mockup noise. Pick one structure and use it for both themes unless the user says otherwise.
- **Links.** Internal links still need explicit `index.html` targets ([0027](../arch/0027-explicit-index-html-links.md)), whatever the mockup's link text says.
