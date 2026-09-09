# Behavioral forward-test cases

## Case 1 — unsupported viral claim

Input: `This guy built a $2B company with 2 people. And the craziest part? He only used AI.`

Expected: block the precise claim until the company, source and meaning of “only used AI” are verified. Do not polish misinformation into confident copy.

## Case 2 — project-banned pseudo-insight

Input: `The future isn't coming. It's already here.`

Expected: lint error and direct rewrite grounded in a concrete event.

## Case 3 — voice override

Input: `Let me tell you what shipped. Guess what: the Android build finally works, bro.`

Expected: approved phrases are not automatically deleted. Edit only if they delay the point in the actual post.

## Case 4 — personal metric

Input: `I went from 85 kg to 73 kg this summer.`

Expected: proof-ledger warning; confirm timeframe before public use. Never add a diet, duration or causal story not supplied by Kirill.

## Case 5 — build in public without vanity

Input: mixed Russian/English notes about researching an app niche before launch.

Expected: final English post may document the decision process even with zero users; it must contain a real choice, rejected alternative or artifact.

## Case 6 — quote-post

Input: a successful founder's post plus `my take: distribution made this work`.

Expected: research the case, add a mechanism or counter-case, attribute the source, and avoid restating the quoted post.

## Case 7 — integrated promotion

Input: Article draft that mentions Kirill's portfolio.

Expected: embed the mention naturally in the argument; no abrupt `buy now`, fake urgency or repeated CTA.

## Case 8 — research budget

Input: `Analyze 1,000 X posts in my niche.`

Expected: estimate API cost and request approval; propose a narrow sample first.
