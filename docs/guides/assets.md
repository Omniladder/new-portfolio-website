# Adding images and downloadable files

Images and files for your site live in two folders:

| Folder | Put here | Examples |
|---|---|---|
| `assets/` | Images shown on your pages | project screenshots, technology logos, a photo of you |
| `assets/download/` | Files visitors download | resume PDF, slides, a paper |

There's also a third folder, `assets/core-assets/`, which holds images and files the site itself uses (not your content). It's part of the repo and shared by every fork. Don't put your own files in it: anything there gets committed. See [docs/arch/0017](../arch/0017-core-assets-tracked.md).

`assets/` and `assets/download/` exist on a fresh clone but are empty apart from a `.gitkeep` placeholder. Leave that file in place: it's what keeps the empty folder in git. Everything else you put in these folders is gitignored, so your personal files never end up in the repo's history ([docs/arch/0013](../arch/0013-assets-gitignored-with-tracked-placeholders.md)). It also means git can't restore them, so keep your own copies.

## Organizing your images

Inside `assets/` you can use any folders you like. The build copies every image, at any depth, into the same place under `dist/assets/` ([docs/arch/0032](../arch/0032-assets-organized-in-subfolders.md)). This layout keeps things easy to find:

```
assets/
  profile/                 your photo, personal logo
  education/               campus photos for the education page
  logos/                   technology logos, shared by every project and the skills table
  projects/
    flashcard-factory/     one folder per project, named after its project_name
      main.png             the screenshot used as "image"
      study-mode.png       extra "gallery" images
  download/                files visitors download (copied as-is, see below)
```

Logos get one shared folder rather than a copy in each project, since the same logo (Python, Docker, ...) usually shows up in many projects. If you move a file, update its path in `data.json`.

## Referencing files from data.json

The generator never scans these folders. A file only appears on your site if `data.json` points to it, using its path from the repo root:

```json
{
  "image": "assets/projects/my-project/main.png",
  "technologies": [
    { "name": "Python", "logo": "assets/logos/pythonLogo.png" }
  ],
  "links": [
    { "label": "Resume", "url": "assets/download/resume.pdf", "type": "download" }
  ]
}
```

- `image` is a project's screenshot, from `assets/`.
- `technologies[].logo` is a small logo for each tool a project uses, from `assets/`. The same logo file can be reused across as many projects as you like.
- A link with `"type": "download"` uses a path under `assets/download/` as its `url`. `github` and `website` links use normal `https://` URLs instead.

See [data-json.md](data-json.md) for the full list of fields.

## Tips

- **Paths are case-sensitive** on most web hosts. `assets/Logo.png` and `assets/logo.png` are different files, even if your computer treats them as the same.
- **Avoid spaces** in filenames. Use `my-project.png`, not `my project.png`.
- **Keep images reasonably small.** A screenshot doesn't need to be a 10 MB original; resizing to around 1600px wide is plenty.
- PNG, JPG, and SVG all work in browsers. SVG is a good fit for logos.

## Current state

Images anywhere under `assets/` (except `download/` and `core-assets/`) are copied into `dist/assets/` at the same path, and files in `assets/download/` are copied as-is to `dist/assets/download/`. Raster images (PNG, JPEG, GIF, WebP) are pixelated (shrunk to half size, then scaled back up into 2×2 blocks) and dithered down to 32 colors for the retro look. SVGs and animated GIFs are copied unchanged ([docs/arch/0040](../arch/0040-pillow-dither-and-32-color-palette.md)). The generator doesn't check that the files you reference actually exist, so a wrong path shows up as a broken image on the page rather than a build error.
