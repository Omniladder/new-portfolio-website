# 0038 — Optional image on experience events

**Status:** Accepted. Extends [[0037-experience-content-model]].

## Context

In 0037, an event card only gets a picture when the event links a `project`.
Some events produce no project, for example a hackathon you sponsored,
judged, or spoke at. Those cards had no picture, even though the event
usually has its own logo.

## Decision

- `experience.events[]` gains an optional `image`: a path under `assets/`
  (recommended: `assets/events/<event>/`), processed like any other image
  ([[0016-process-assets-image-pipeline]], [[0032-assets-organized-in-subfolders]]).
- A linked `project` still wins. `image` is shown only when there's no project.
- The image isn't a link (there's no page to link to). It's shown whole with
  `object-fit: contain` instead of cropped, because it's usually a logo.

## Consequences

- Forks can show sponsored, judged, or attended events with their own art.
- The card's thumbnail has two variants, a linked project screenshot and an
  unlinked event image, both styled by `.event-thumb`.

## Keywords

experience, events, hackathon, image, logo, sponsor, event-thumb, data.json, schema
