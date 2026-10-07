# Cover designer checklist

This is a working review contract, not a promise of virality. The aim is a clear, distinctive, relevant reason to stop and open the article; actual performance requires publication data. Do not replace design work with a self-awarded score.

## 1. Understand before opening the image tool

- [ ] Read the real article/thesis. Identify reader, promise, tension and strongest visual anchor.
- [ ] Separate supported facts from metaphor. No new revenue, views, product screens or personal results are invented for the cover.
- [ ] Write one visual sentence and its mapping to the article. For a philosophical image, read `x-cover-art-direction/references/concept-design.md`.
- [ ] Generate genuinely different concepts before choosing; palette changes are not different concepts.
- [ ] Check existing user choices. If no style was selected and exploration was not delegated, show 2–3 relevant **actual images inline** with reasons and ask which style to use. Do not make the user open a website just to see the options.

## 2. Read the reference as a designer

- [ ] Open the original at full resolution and at 340 px; do not design from a caption alone.
- [ ] Note what the eye sees first, second and third.
- [ ] Record approximate relative scales: dominant word, subordinate copy, object, negative space. Use visible ink bounds, not just font point sizes.
- [ ] Record alignment, distance between copy blocks, material, light direction, horizon/contact plane and overlap.
- [ ] Identify what is transferable and what belongs to the source: title/claims/artwork are not copied merely because the layout works.
- [ ] Choose a target crop. The library's 5:2 is an observed format, not an unchecked claim about every X surface.

## 3. Design the layers

- [ ] Commit to one focal subject and a limited hierarchy. Secondary copy supports the main word and stays optically connected to it.
- [ ] Pick an actual font family/weight for the visual language; keep exact headline text outside image generation by default.
- [ ] For dramatic type-led covers, map where foreground objects cross the letters. The result must read instantly, without guessing hidden first letters or counters.
- [ ] For a restrained blueprint or art-led engraving, derive depth/hierarchy from the selected reference instead of attaching a random glass icon to satisfy a formula. Do not silently substitute the restrained route for a requested dramatic one.
- [ ] Decide whether to generate a complete coherent scene or separate assets. Whole-scene icon generation is permitted when it improves material/light/refraction. Use exact source insertion only when it serves the chosen look.
- [ ] Brand symbols depict their real recognizable identity. A stylized model rendering is checked against reference assets; a generic play glyph does not stand for TikTok.

## 4. Generate with a controlled concept

- [ ] Prompt subject/action, material, perspective, framing, light and intended copy zone; exclude unrelated scenery and fake text.
- [ ] If requesting glass, distinguish **body translucency/refraction** from **transparent outside background**. Opaque tiles inside a clear rim fail the requested glass look.
- [ ] Keep anatomy, contact points and object topology coherent. Surreal scale is deliberate; extra limbs or disconnected mechanical parts are not.
- [ ] Save actual prompt and output dimensions. Do not assume the prompt's requested pixel dimensions were honored.
- [ ] Inspect the generated asset before layout; reject or repair a broken subject now, not after decorating it.

## 5. Compose exactly

- [ ] Set final wording, line breaks, font and positions independently; never horizontally stretch letters or assets.
- [ ] Measure descenders and visible ink. Render overflow is fixed in the source, not cropped away.
- [ ] Make neighboring text scales/spacing feel like one lockup. The old detached the/playbook failure is a negative example.
- [ ] Match object lighting to the field. Objects standing on a surface share a credible baseline and contact shadows; suspended objects need an intentional contextual reason.
- [ ] Check visible alpha bounds. Faint pixel noise can extend beyond the visible object and misplace its shadow. Do not use an arbitrary threshold on translucent material without inspection.
- [ ] Diagrams use exact labels and meaningful routes. Keep labels clear of connectors/bends. Essential small text must survive feed size.

## 6. Mandatory comparison after every material change

- [ ] Verify the render succeeded; stale PNG after an error is not the new version.
- [ ] Put original and candidate **side by side at identical size**. Open that comparison image.
- [ ] Put both at 340 px and inspect again. Check dominant words, silhouette, crop and source-to-candidate scale relationships.
- [ ] Compare the intended style, not just palette: material, tension, composition, depth and negative space.
- [ ] Inspect the candidate at full size for spelling, seams, halos, malformed glyphs/logos, anatomy, repeated fragments and synthetic noise.
- [ ] State the highest-impact remaining defect in concrete terms. “Needs polish” is not a usable diagnosis.

## 7. Iterate until the actual defect is resolved

- [ ] Snapshot the PNG, JSON and any asset about to change; the comparison must remain reproducible.
- [ ] Choose the proper correction layer: concept, composition, generated subject, typography, mask/light or crop.
- [ ] Change the smallest set of variables that addresses the defect; compare before/after at the same scale.
- [ ] If it did not improve, do not promote the new version merely because it is newer.
- [ ] After repeated failures, change method: simplify the subject, change layout, regenerate only the asset, or use precise composition instead of more prompt adjectives.
- [ ] No arbitrary 2–3-pass stopping rule. Continue while material failures remain. The user's “even 100 edits” expresses quality priority, not a requirement to waste 100 generations.
- [ ] Stop when concrete requirements are met and further changes are subjective, or state a real unresolved limitation. Never call an unresolved defect “a stylistic choice” to end the task.

## 8. Handoff that another chat can use

- [ ] Show the actual final candidates inline, not only gallery links. For multi-style practice show every requested direction.
- [ ] Save full PNG, thumbnail, editable source, used assets/prompts, chosen reference IDs and concept mapping.
- [ ] Record observed failures, intervention and result; distinguish agent judgment from explicit user feedback.
- [ ] Run available mechanical checks, but do not confuse them with visual approval or performance evidence.
- [ ] Deliver a short recommendation. User review status remains explicit. Do not publish automatically.

The completed practice ledger is `x-content-engine/assets/covers/cover-lab-2026-10-07/round-2/review.md`. Six style recipes are in `six-style-recipes.md`.
