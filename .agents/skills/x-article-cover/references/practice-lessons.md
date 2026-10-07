# Lessons from actual practice — 2026-10-07

## Later clarification and current practice

Round-1 blue v5 was subsequently rejected for its **material**, despite improved spacing/shadows: opaque app tiles in transparent casings are not transparent glass bodies. Kirill explicitly allows image-model rendering of recognizable brand symbols together with 3D objects or the whole scene. Exact PNG insertion is an option, not a mandatory rule. Final typography still stays separately typeset by default.

Current practice is `cover-lab-2026-10-07/round-2/`: six distinct families, six reference comparisons, five new generated assets, plus a deterministic blueprint. Current procedures are in designer-checklist.md, six-style-recipes.md and x-cover-art-direction/references/concept-design.md. Do not promote the old v5 to a final glass exemplar.

Additional observed lessons: the collage's subordinate copy was too distant, so the lockup was compacted; diagram labels collided with route bends, so labels moved into clear space; the cinematic object needed a closer relationship to the title. The philosophical monochrome study derives its curtain action from deliberate visibility, rather than decorating an app article with random futuristic scenery.

Source artifacts: `x-content-engine/assets/covers/cover-lab-2026-10-07/`. This records observed failures and explicit feedback, not a performance benchmark. None of these studies has measured CTR or user approval.

| Observation | Intervention | Reusable decision |
|---|---|---|
| Bridge engraving figure was too small in a 340 px feed preview | Targeted image edit enlarged the same figure and retained scene | Check silhouette at the intended display size; fine full-size detail is insufficient |
| First press illustration with heavy sans felt materially different from the warm print reference | Separate serif/italic lettering, same illustration | Match typography to the visual material; this is a design judgment, not a universal serif preference |
| Blue v1 had equal-sized lines and a generic play-card object off to the side | Rebuild the lockup around one dominant word and real platform assets | Palette/legibility alone do not match reference impact. User explicitly rejected this version |
| Blue v2 foreground hid the initial p of playbook | Moved secondary copy/objects | Check actual word recognition, not just numerical overlap |
| Blue v3 still had detached the/playbook and floating objects | Compare original and output at the same size, bring copy close, add common surface/contact shadows | User requires this reference comparison after every material edit; it cannot be an optional final glance |
| Blue v4 shadow was below the visible casing although coordinates appeared aligned | Inspect alpha bounds; threshold near-invisible halo for crop and recalculate contact | File bounding box is not necessarily the visible object footprint |
| Text overflow for More signal. / organic / playbook despite apparently sufficient cap-height space | Renderer measured descenders and rejected render; boxes/min-size were consciously revised | Measure visible ink including g/y/p; never silently crop or squish |
| A failed render left the old PNG on disk | Gate viewing on successful exit/hash | Inspect the new output, not a stale file |

## Historical round-1 blue candidate — superseded

`final/05-glass.png`, its JSON and `reference-comparison.jpg`. Different from v1: one huge word, linked secondary text, genuine sourced TikTok/Instagram artwork in generated casings, shared baseline/contact shadows, source and candidate shown both large and at 340 px. This is the agent's revised candidate, not human approval or an exact recreation.

The original has more translucent colored glass and a greener atmospheric field; round 1 used heavier clear casings and genuine App Store tile artwork. That material treatment was subsequently rejected. The newer reference-guided generation route in round 2 is permitted and preferred when it produces the intended transparent body. Inspect mark fidelity rather than imposing the old source-pixel-only rule.

## User preferences versus local design choices

Confirmed: choose style per topic, offer actual references first, separate final text, real identity assets, large type with readable foreground overlap in type-led covers, compact scale relationships, anchored objects, compare after each material iteration. Baseline monochrome without text remains valid.

Not confirmed: the agent's favorite, the current blue candidate, Georgia as a house font, one global palette, one crop for every X surface, or a promise of more clicks. Do not promote those to permanent rules.
