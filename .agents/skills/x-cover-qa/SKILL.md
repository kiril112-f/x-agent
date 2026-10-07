---
name: x-cover-qa
description: "Проверяет обложку статьи в полном размере и в ленте, находит дефекты типографики, глубины, иллюстрации и фактов, направляет итерацию и сохраняет практические уроки."
---

# Review and refine an article cover

After EVERY substantive iteration, open the exported PNG and chosen original **side by side at identical dimensions**, then both at 340 px. This is Kirill's explicit instruction, not optional QA. Know the topic, exact copy, reference and evidence status. Check render success: an old PNG after failure is not the new result. Use the lab's `compare_reference.py` or an equivalent comparison board.

## Review

1. Meaning: explain what the image communicates without reading the brief. Is it specific to the topic or generic decorative imagery?
2. Feed: read intended words; identify the focal subject without zoom. No-text art must retain a recognizable silhouette/tension.
3. Full size: spelling, glyph collisions/descenders, cutout halos/alpha, believable anatomy/geometry, repeated objects, generated writing, correct brand marks against source assets.
4. Reference comparison: relative type scale, hierarchy, light/dark masses, material and depth. For Kirill's type-led preference, verify that actual foreground objects overlap the letters; a tiny detached icon is a failure even if spelling/contrast pass.
5. Spatial coherence: small/large text must form one compact lockup. Compare gaps using visible letter ink rather than CSS boxes. Objects standing on a surface need a shared baseline and contact shadows touching their visible silhouette. An offset drop shadow can make them float. Check alpha noise/margins before placing shadows.
6. Truth/crop: real data and screenshots, no fake proof; practice remains labeled in delivery. Inspect the target crop. A fallback 3:1 crop of 5:2 may require recomposition.

Automated checks prove file integrity, dimensions, hashes, alpha or font bounds only. They cannot prove taste, semantic readability, truth, absence of all AI artifacts or user approval.

## Iteration

Save v1. Name a concrete defect and correct its layer. Type/spacing → spec. Malformed/small subject → image asset edit. Busy image → simpler scene/light masses. Missing proof → remove claim or obtain real evidence.

Compare before/after at the same size. Stop when material defects are resolved and remaining differences are subjective; show the strongest candidates. If correction drifts or plateaus, change composition/tool or disclose the unresolved issue. Neither an arbitrary iteration count nor an agent's own score means perfection.

Save each material revision with brief, reference IDs, before/after paths, defect, intervention, observed result and uncertainty. Separate measured check, agent judgment and explicit user preference. A human rejection overrides a prior agent pass.

Concrete failure to remember: the lab's first blue cover passed text bounds and mobile readability but Kirill rejected its generic icon, weak hierarchy and absent depth. The second revision introduced real icons but hid the p in playbook. The third moved the objects and text to restore the whole word while preserving foreground overlap with organic.

Practice log: `x-content-engine/assets/covers/cover-lab-2026-10-07/review.md`. Durable lesson summary: `../x-article-cover/references/practice-lessons.md`. Do not present illustrative generated photography as documentation of Kirill's own life.
