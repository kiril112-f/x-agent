# Cover practice and feedback — 2026-10-07

## Status

Six initial studies were produced. These are practice briefs, not finished Articles or measured marketing campaigns. No study has been approved by Kirill. The blue study received explicit corrections and was revised five times; the latest is a candidate. Other studies remain exploration, and the flat type/system examples are not defaults for the newly clarified dramatic type preference.

Reference collection: 28 actual covers from 31 input links; originals and metadata in `../../cover-references/2026-10-07/`. The two repeated links resolve to the same downloaded originals. The Jesse URL identifies only a profile, not a specific article. Article bodies were not saved locally; the extraction service may process article data remotely before field projection.

## Studies

| File | Brief and references | Assessment |
|---|---|---|
| 01-monochrome | Focus as a single path; narrative engraving family 15/16/22 | Targeted edit enlarged the figure for feed recognition. Art-led, no text. Agent candidate |
| 02-editorial | Repeatable content production; warm print language 17 | Same generated press, heavy sans initial and serif/italic alternative. Serif choice is agent judgment; not user-approved |
| 03-cinematic | Short-form production; cinematic object language 05/19 | Exact two-line type over generated studio. Exploratory baseline; needs foreground integration if chosen under current type-depth preference |
| 04-type | Signal/noise, typographic contrast | Deliberately art-free baseline, not representative of user's preferred layered type covers |
| 05-glass | Organic distribution; source 06 with depth grammar from 11/31 | v1 and v3 rejected by user. v5 corrects compact typography and grounding, remains candidate |
| 06-system | Slideshow mechanism; reduced structure from 26/27 | Exact diagram, no invented metric. Restrained reference route, not a dramatic cover default |

## Real blue iteration history

1. **v1 — rejected by Kirill.** Two similarly large lines, generic glass play cards at side. Color alone did not match reference hierarchy/depth. The user said the result did not give the same reason to click. Keep as negative example.
2. **v2 — internal rejection.** Real sourced TikTok/Instagram artwork placed into generated glass casings; giant organic + smaller playbook. Object hid the initial p in playbook. Repositioned.
3. **v3 — rejected by Kirill.** Letter visible, but the was too far above the large word and playbook too low. Objects still floated. The user explicitly required full original-vs-output comparison after every iteration. `iterations/reference-vs-v3.jpg` records the actual comparison.
4. **v4 — internal rejection after side-by-side.** Text group compacted; surface light/contact shadows added, yet a gap remained beneath objects. Actual alpha bounds revealed near-transparent pixels outside the casing. `iterations/reference-vs-v4.jpg` records this stage.
5. **v5 — current candidate.** Visible silhouette crop (alpha>8 for this specific asset, with padding), shared object baseline, contact shadows at visible base, revised scale/spacing. `reference-comparison.jpg` shows original and current at equal size and at 340 px. No claim of perfect material match: reference glass is more translucent/tinted; candidate uses heavier clear casings and real App Store tile art.

Historical v2/v3/v4 JSON references shared assets that were subsequently refined, so re-rendering those JSONs is not byte-exact archival reproduction. The saved reference-vs-v3 and reference-vs-v4 comparison boards are the faithful snapshots of those viewed states. New substantive iterations should snapshot changed assets as well as JSON; the build now preserves existing iteration PNGs instead of overwriting them.

## What was actually checked

- Every source cover decoded, dimensions matched metadata, SHA-256 recorded by collector.
- Current outputs 2000×800; previews 340×136.
- Exact final text independently typeset; spelling/line breaks inspected.
- Real TikTok/Instagram icon art reused from Apple's App Store artwork collected on 2026-10-05, source URLs in assets/sources.md. Generated casing has no logo.
- Reference and candidate compared side by side at full comparison size and feed size.
- Geometry tests distinguish automated checks from visual judgment; no CTR/engagement test exists.
- Independent QA: 18/18 renderer tests pass, including descenders, overflow, real spec smoke, alpha/layer order, stable hashes and invalid fit/opacity/centering. Three initial schema validation defects were fixed. Reusable test: `.agents/skills/x-cover-compose/scripts/test_render_cover.py`. Five skill entrypoints passed quick_validate in UTF-8 mode.
- The generated scenes are illustrations, not documentary photos of Kirill's work or results.

## Reproduction

`python x-content-engine/assets/covers/cover-lab-2026-10-07/build_lab.py` rebuilds current saved final specs, retaining historical PNGs. Requires Pillow and fonts named by specs.

`python x-content-engine/assets/covers/cover-lab-2026-10-07/refine_depth.py` rebuilds the current sourced-logo/casing treatment and blue spec. Requires Pillow, NumPy and the saved assets. Face insertion coordinates are specific to the inspected 1254×1254 casing.

`python x-content-engine/assets/covers/cover-lab-2026-10-07/compare_reference.py` updates the reference comparison. `build_gallery.py` rebuilds the local review gallery.

Do not use `--init-specs` after revisions unless intentionally restoring the first-pass baseline. Do not label automated rebuilds as new visual reviews.
