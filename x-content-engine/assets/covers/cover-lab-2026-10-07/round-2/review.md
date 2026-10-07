# Practice round 2 — six families, 2026-10-07

## Scope and status

Kirill asked for genuinely translucent 3D icons, permitted reference-guided icon generation directly with a scene, and requested practice across at least half the style families plus a professional iterative checklist and a short handoff for his Article agent.

Six of the twelve families identified in the saved corpus are represented here. This is coverage of an editorial taxonomy, not a measured ranking of the “most viral” styles. Five new image assets were generated with the built-in image tool; the blueprint was composed precisely from text and geometry. Final headlines are independently typeset. No source figures, screenshots or personal results were fabricated. None of the covers has user approval or measured publication performance.

## Concepts and actual review

| Family | Chosen relationship | Reference comparison | Observed result / limitation |
|---|---|---|---|
| Glass | Recognizable distribution platforms as a shared foreground group | 06: main-word scale, compact type, translucent bodies, physical depth | New pair removes the opaque inserts of round 1. Symbols are reference-guided model renderings, not unchanged official source pixels. Brand identity visually checked |
| Monochrome | A person deliberately opens a curtain to reveal a horizon | 15: monumental scale, strong value masses, legible figure/action, engraved material | The action reads at 340 px. Intentional symbolic scale; local hand/cloth/ledge relation checked. Different scene/tension from source, deliberately |
| Warm editorial | One operator uses a repeatable printing mechanism | 17: warm print medium, readable serif hierarchy, coherent scene | Separate type and foreground wheel integrate; copy says no revenue/result. Final d/period and wheel edge inspected. Lowercase editorial variation rather than copying source typography |
| Cinematic | Make work able to travel, symbolized by folded paper | 19: condensed type, dark stage, directional warm light, tangible object | V2 was closer but still did not overlap letters; independent review caught it. V3 created upper T overlap but stone hid the lower L. V4 changed lower type size, retaining upper overlap and restoring L. Plane topology/contact checked |
| Collage | Attention is human, represented by a single eye | 12: serif, layered tactile paper, grayscale focal motif | V2 fixed remote secondary copy and balance. Full-size check then found overly tight t crossbars; v3 restored native whole-line kerning. Eye is ordinary, not extra/surreal anatomy |
| Blueprint | A designed route links idea, format and audience | 20: continuous route and exact labels with a quiet technical field | V1 label/connector collisions. V2 moved labels off bends and increased size. Three semantic nodes replace source's tiny dense map; deliberately restrained option |

## Iterations retained

- `assets/*-v1.png` are immutable generated originals for this round. Actual prompts/reference paths in `assets/prompts.json`.
- `iterations/04-cinematic-v1*`, `05-collage-v1*`, `06-blueprint-v1*` retain old specs, PNGs, previews, QA output and original/candidate comparison boards.
- Additional cinematic v2/v3 and collage v2 snapshots retain the later rejected layouts. Current recipes document these subsequent corrections.
- `final/*.json` are editable current compositions. They reference saved source assets and stable procedural stages.
- `comparisons/*.jpg` show original and candidate at equal 1000×400 size, then both at 340×136.
- `six-styles.jpg` and `thumbnails.png` show all requested directions, not only the blue one.

Changing every image for the sake of a revision count would not add evidence. The monochrome and warm illustration first renders met the identified concept/material requirements after inspection; the collage, cinematic and system layouts had specific corrections. Further changes remain possible after the user's style preference/review.

## Mechanical checks versus judgment

All final masters are 2000×800; thumbnails 340×136. Renderer checked text bounds and saved source/font hashes. Real image dimensions inspected; alpha outside cutouts verified. A nonzero/partial alpha channel alone is not proof of optically transparent material. Visible glass transmission/refraction was reviewed in the actual composed blue image beside reference 06.

The mandatory comparison and concept checks are design judgments grounded in visible artifacts. They are not proof of CTR, “no possible hallucinations”, or the user's approval. No changes were made to the user's concurrently edited Article.

## Rebuild

`python x-content-engine/assets/covers/cover-lab-2026-10-07/round-2/build.py` renders saved final specs and rebuilds comparison boards. Python/Pillow and installed fonts as recorded in `.qa.json` are required; NumPy is used for the procedural stages on initialization.

`--init` resets specs to v1. Do not use it on edited specs unless deliberately restoring the baseline. `refine.py` applies the documented final corrections and preserves v1 if absent. For a new revision, snapshot current specs/assets before modifying.

## Durable instruction changes

The five skills now allow coherent icon/scene generation with identity checking; distinguish alpha from body translucency; require an explainable philosophical concept; and route through the explicit designer checklist. The checklist has no arbitrary two- or three-pass completion cap. Repeated failure should change method rather than consume generations without diagnosing the cause. Handoff copy: `HANDOFF.txt`.
