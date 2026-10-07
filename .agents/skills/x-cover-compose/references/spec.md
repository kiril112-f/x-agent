# Layered cover specification

Coordinates are output pixels. Order is back to front. Paths resolve against the spec. `box` is `[x,y,width,height]`.

```json
{"size":[2000,800],"background":"#f4f0e7","layers":[
  {"type":"text","text":"Less noise.","box":[90,110,1820,265],"size":325,"min_size":290,"font":"sans","weight":900,"tracking":-9},
  {"type":"text","text":"More signal.","box":[90,425,1820,295],"size":320,"min_size":260,"font":"sans","weight":900,"tracking":-9,"fill":"#d94320"}
]}
```

This is a type-only baseline fixture, not the user's preferred depth treatment. For the latter use the lab's revised `05-glass.json`.

| Type | Fields |
|---|---|
| text | text, box, size; optional min_size (default=size), font, weight, tracking in pixels, fill, align left/center/right, valign top/center/bottom, allow_bleed |
| image | path, box; optional fit contain/cover, centering [0..1,0..1], trim_alpha, opacity 0..1 |
| gradient | start, end; vertical, whole canvas |
| rect | box, fill or outline, stroke, radius |
| ellipse | box, fill or outline, stroke |
| line | points flat [x1,y1,x2,y2,...], stroke, fill |
| polygon | points [[x,y],...], fill |

One text layer is one explicit line; no auto-wrap. `sans`: Inter Variable; `serif`/`serif-italic`: Georgia; `condensed`: Impact; `mono`: Consolas. Explicit font paths also work. Inter alias accepts weight; other fonts use the selected file's actual style. With nonzero tracking, glyph placement is per-character; inspect spacing carefully rather than assuming sophisticated shaping.

`contain` preserves ratio without enlarging a small source. `cover` crops/resizes deliberately. Neither certifies source resolution. Opaque shape fills are the supported convention; alpha rectangles do not blend automatically with earlier layers.

Working project-root examples: `x-content-engine/assets/covers/cover-lab-2026-10-07/final/01-monochrome.json` through `06-system.json`. Revised depth example is `05-glass.json`; rejected baseline stays in `iterations/05-glass-v1-rejected.json`.

Rebuild saved specs: `python x-content-engine/assets/covers/cover-lab-2026-10-07/build_lab.py`. Rebuild the revised icon assets/spec: `python x-content-engine/assets/covers/cover-lab-2026-10-07/refine_depth.py`. Do not run `build_lab.py --init-specs` on revised output: that resets to the original baseline including the rejected blue cover.

This is a small Pillow compositor, not Figma, an OCR service, crop checker or semantic QA system. `.qa.json` geometry success must never be treated as overall design/user approval. Use SVG/HTML for richer vector editing when useful.
