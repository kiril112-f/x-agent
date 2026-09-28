# What performs: own posts and niche breakouts — 2026-09-28

Snapshot for the X trend radar and idea selection. Metrics are counts at collection time, not proof of revenue or other claims inside the posts. Data: Apify `xquik/x-tweet-scraper`, 40 rows from `@KirillMorozovop` (profileTweets) and 60 top posts since 2026-09-26 from three niche searches with engagement floors (100 rows total). The For You timeline itself was not readable in this pass because the browser window stayed in the background; Spark's Chrome timeline step covers it going forward.

## Own posts (about 15 followers)

33 originals, median 45 views. Saves were almost zero, so views are the only usable signal at this size.

| Views | vs median | Post type |
|---:|---:|---|
| 911 | 20x | Timely breakdown of a major launch: "iOS 27 shipped yesterday. Here's everything that actually matters", structured list |
| 733 | 16x | Own build with a real artifact: the MERA calorie tracker built without writing code |
| 615 | 14x | Quote of a viral one-shot AI video with concrete cost math |
| 494 | 11x | Practical unlock: installing any .ipa on an iPhone, resources in a self-reply (271 views on the reply) |
| 132 | 3x | Own build: a local Higgsfield replacement |

Underperformed (3–122 views): short hype reactions to model rumors and benchmarks ("We are cooked", "194x faster"), emoji "this app makes $X" quotes without his own angle, generic motivation, one-word quotes.

## Niche breakouts (2026-09-26 → 28)

- Highest save rates (2–3% of views) came from copyable artifacts: one prompt or skill plus a visible demo, open-sourced courses and libraries, and "stop doing X, do Y" workflow fixes for coding agents.
- Small accounts broke out at 30–500x their follower count with demos built on the newest model (games, launch videos, interactive web pieces) and practical Claude Code or Codex tricks.
- The current wave is code-generated motion design, launch videos and UGC ad prompts on the newest Claude model; it will fade, the pattern (artifact + demo + prompt) is what transfers.

## Implications for ideas

1. Prefer ideas where Kirill can add something he tries himself: a prompt, a screenshot, his own build or a measured test. Name what he would need to try.
2. Timely launch breakdowns work when they explain what actually changes for builders, not when they only repeat the announcement.
3. Put resources or the copyable object in a self-reply or the post; saves follow usefulness.
4. Treat hype without an artifact as low value, even when the source post has large reach.

## Where this is used

- The radar prompt (`lib/radar/providers.ts`, `RADAR_INSTRUCTIONS`, calibration paragraph) and its Apify queries with engagement floors in the tg-notes repository.
- Kirill's approvals, rejections and published results outrank this snapshot as they accumulate; refresh it when the pattern visibly changes.
