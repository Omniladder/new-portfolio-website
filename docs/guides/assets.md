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

## How your images are processed

Your images get a 90s-homepage look during the build. Each image in `assets/` goes through three steps on its way to `dist/assets/`:

1. **Pixelate.** It's shrunk to half its width and height, then scaled back up to its original size without smoothing. Every pixel becomes a hard-edged 2×2 block.
2. **Dither.** It's mapped onto a 32-color palette picked from the image's own colors. Floyd–Steinberg dithering turns smooth gradients into speckled dot patterns instead of flat bands.
3. **Reduce colors.** The image is capped at those 32 colors.

The image keeps its original size, file name, and format, so the paths in `data.json` don't change. Transparency is kept. The images in `assets/core-assets/` get the same treatment.

Your original files in `assets/` are never modified. Only the copies in `dist/` are changed.

Some files are copied as-is instead:

- **SVGs**, since they're vector drawings rather than pixels. This keeps logos and icons sharp.
- **Animated GIFs**, since processing would keep only the first frame.
- **Everything in `assets/download/`**, since visitors should get the exact file you put there.

Things to expect:

- **Fine detail gets lost.** Thin lines and small text in logos and screenshots can become hard to read. If a logo needs to stay crisp, use an SVG version.
- **JPEGs end up with more than 32 colors.** They're still pixelated and dithered, but saving as JPEG again adds compression noise. Use PNG if you want the strict 32-color look.
- **Processing is slow.** It takes roughly a quarter of a second per image, so a folder of 150+ images adds most of a minute to every build.

### Skipping processing for faster builds

When you're working on text in `data.json` and just want to check the page quickly, skip the image step:

```bash
python3 generate.py --no-image-processing
```

Images are then copied into `dist/` unchanged, and the build finishes in about a second. The build output says `image processing off` so you can tell which kind of build you have.

Don't publish a build made this way: the images won't have the retro look. Run plain `python3 generate.py` before you deploy `dist/`.

## Tips

- **Paths are case-sensitive** on most web hosts. `assets/Logo.png` and `assets/logo.png` are different files, even if your computer treats them as the same.
- **Avoid spaces** in filenames. Use `my-project.png`, not `my project.png`.
- **Keep images reasonably small.** A screenshot doesn't need to be a 10 MB original; resizing to around 1600px wide is plenty.
- PNG, JPG, and SVG all work in browsers. SVG is a good fit for logos.

## Current state

Images anywhere under `assets/` (except `download/` and `core-assets/`) are copied into `dist/assets/` at the same path, and files in `assets/download/` are copied as-is to `dist/assets/download/`. Raster images (PNG, JPEG, GIF, WebP) are pixelated, dithered, and reduced to 32 colors, unless you pass `--no-image-processing` (see [How your images are processed](#how-your-images-are-processed); [docs/arch/0040](../arch/0040-pillow-dither-and-32-color-palette.md), [0041](../arch/0041-pixelate-in-reduce-image-quality.md), [0043](../arch/0043-no-image-processing-flag.md)). The generator doesn't check that the files you reference actually exist, so a wrong path shows up as a broken image on the page rather than a build error.
