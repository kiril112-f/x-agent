---
name: x-cover-reference-library
description: "Скачивает именно обложки статей по ссылкам и сохраняет originals, provenance, contact sheets и визуальные теги; для пополнения библиотеки, без полного сбора статей."
---

# Cover reference library

Use the existing manifest/contact sheets in `x-content-engine/assets/cover-references/2026-10-07/` first. Numbering matches input order including gaps for duplicates/profile.

For new X URLs follow `$x-content-research`, the project Apify/Xquik path and default 100 delivered rows. Deduplicate exact post IDs. A profile URL is not a cover: complete concrete URLs and report the profile separately; don't silently pick a post or substitute avatar/banner.

Retrieve only needed article metadata: source post/article ID, author, title, cover URL, dimensions. Do not save bodies or embedded article media for a covers-only request. If the service internally extracts an article, project the needed fields on retrieval; don't claim the remote service never processed the body.

Download actual original-size cover bytes where available. Verify image decode, dimensions and hash. One manifest entry per input: downloaded, duplicate or explicit unresolved/failure status; preserve source page/image URLs, retrieval date/method, local path and SHA-256. Originals are immutable; crops/contact sheets are derivatives.

Tested batch helper: `x-content-engine/assets/cover-references/2026-10-07/collect.py`. Inspect before reusing; it rebuilds a specific batch from metadata, not arbitrary cover discovery. Already-resolved public image URLs require no X account writes.

Inspect actual images and tag composition, type, material, palette, proof type and topic fit. Distinguish observed design from inferred production/performance. Source metrics remain source-author claims, not Kirill's evidence; post popularity is not proof the cover caused views.

Pinterest/web discovery is optional for missing directions. Follow the available research workflow, preserve the original creator/source where discoverable, label uncertain provenance. A saved reference is not automatically licensed for republication; create original compositions rather than republish the reference.
