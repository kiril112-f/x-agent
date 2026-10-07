---
name: x-cover-compose
description: "Верстает точный текст и настоящие логотипы обложек отдельно от генерируемой иллюстрации, управляет слоями и перекрытием, создаёт воспроизводимые PNG и превью из JSON."
---

# Compose a cover

Generated art and deterministic typography are separate layers. Use code-native/vector shapes for exact diagrams and actual evidence for screenshots. Brand marks may be exact source assets OR reference-guided stylized image-model renderings inside a coherent object/scene, per Kirill's later clarification. Inspect shape/identity afterward. Do not invent a generic substitute for a known platform.

## Tested compositor

`scripts/render_cover.py` requires Python 3.10+ and Pillow; no network. JSON contains canvas and ordered layers. It is the editable source.

```powershell
python .agents/skills/x-cover-compose/scripts/render_cover.py path/to/spec.json --out path/to/cover.png
```

Read [schema and working examples](references/spec.md). Choose copy, font, weight, semantic line breaks and boxes yourself. A renderer fits geometry, not design. It measures visible glyph ink including descenders, errors on overflow below the declared minimum, and writes a 340 px thumbnail plus `.qa.json`. It records font/asset hashes. It does not detect collisions, typos, factual errors, bad contrast or design quality.

Fonts come from `--font-dir` (Windows Fonts by default), or explicit paths relative to the spec. Missing font fails clearly, with no silent substitution. Examples use installed Inter/Georgia; font files are not bundled. Another machine must supply the fonts legitimately or consciously redesign and review.

## Layering and real identity

For a type-led cover, place a meaningful dimensional object in front of part of the giant letters. Design the overlap deliberately; preserve word recognition and the font's counters. A detached small icon is not the requested depth effect. Keep shadows local to the object, not a blanket effect on all type.

The historical `cover-lab-2026-10-07/refine_depth.py` demonstrates exact logo insertion, but Kirill rejected its opaque bodies as the glass direction. For current glass see `round-2/final/01-glass.json`: reference-guided symbols/material generated together. The earlier casing coordinates belong to that inspected 1254×1254 image, not a generic template. Generation dimensions are not guaranteed by a prompt.

Distinguish **transparent outside the object** (alpha channel) from **transparent material** (the body transmits the field behind it, with refraction/thickness). A PNG with alpha and an opaque black/white face fails the latter. A coherent generated scene with icons can have an opaque image background and still depict proper transparent glass. Pick the route for the desired optical result; do not force flat app artwork into translucent glass.

Generated alpha can contain near-invisible noise outside the silhouette. In this asset, `alpha>0` included almost the whole canvas, whereas `alpha>8` isolated the visible casing. That invisible margin caused a visible gap above the contact shadow. Inspect thresholds and add a small edge margin before cropping; never apply 8 as a universal threshold to translucent material. The cast shadow must touch the **visible** object, not its file box.

## Output constraints

- Use chosen ratio. Lab master 2000×800/5:2 is observed from supplied originals, not a claim about current X rules.
- Preserve source aspect ratios; explicit `cover` crops need inspection. Never stretch images or fonts.
- Verify actual alpha and edges on light/dark backgrounds. A painted checkerboard is not transparency.
- No fabricated numbers, analytics interfaces, revenue badges or partnership cues.
- Fix type/placement in the spec; do not regenerate the whole art for a text typo.
- Keep earlier substantive versions and prompts. If render fails, do not inspect a stale PNG as though it were the new version; verify command success/hash.

Deliver PNG + thumbnail + editable spec + assets/prompts + review. Run `$x-cover-qa`. Preserve provenance and do not invent usage-license claims.
