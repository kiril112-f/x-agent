# Cover production — current routes

## General production

Use the built-in image tool for illustration/object assets and `$x-cover-compose` for exact type, actual logo assets and layer placement. Select style first; there is no mandatory global cobalt palette. Discover actual available tool capabilities instead of copying historical model IDs.

Do not silently start another local image service, install software, use an API model or assume credentials just because old experiments used it. An explicitly requested available tool can be used within the task's authorization. Keep prompts/results/provenance with the cover.

For real brand identities, acquire/reuse real artwork. A generated casing is acceptable; paste the real mark into it separately. Example: `cover-lab-2026-10-07/refine_depth.py`. Inspect source dimensions and visible alpha bounds, not merely the file box. Glass/translucency needs genuine alpha; no automatic color-key fallback that destroys refraction.

Render the selected crop, then compare reference and candidate side by side at identical dimensions and at 340 px after each material revision. Check scale relationships, compact line spacing, readable overlap and contact shadows. Script geometry pass is not design approval.

## Special legacy l5 compositor

Only for the selected giant-type/occlusion direction. `assets/render.ps1` renders 1536×512 at scale 1, defaults to scale 2 and l5. l5 requires 1–3 `-Plate` objects. That is a local implementation constraint, not a universal rule for every style.

```powershell
.agents/skills/x-article-cover/assets/render.ps1 -Hero 'organic|installs' -Plate '<actual-plate.png>' -Field cobalt -Layout l5 -Out '<article-folder>/cover.png'
```

Actual flags live in the script. Useful l5 controls: `-Cover` overlap percentage, `-BandMin/-BandMax`, `-Gap`, `-ClusterMax`, `-Tilt`, `-Fill`, `-Scale`. `-Hero`: `|` explicit line break. For other layouts, `~small words~`, `*accent*`, `@` icon slot are supported by the historical HTML compositor. Inspect current script before reusing commands from older docs.

Old defaults and numeric geometry guards are starting points for this font/layout. Open the rendered image and compare to the intended reference; do not assume a no-warning console result is adequate. Preserve `cover.cmd.txt` or editable source so it can be rebuilt.

## Delivery

Use `x-content-engine/assets/covers/<slug>/`. Save brief/choice, prompts, assets, exact font identity, editable source, final PNG, thumbnail and review. Keep source reference originals in the library. Practice studies are labeled practice outside the public image. No automatic publishing or external Notion write is implied by making a cover.
