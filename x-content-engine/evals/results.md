# Initial validation results

Status: 23/23 mechanical regression tests passed after paragraph-formatting, no-fluff, and Apify token-fallback enforcement; behavioral cases and two publishable dry runs completed.

Expected safety behavior already encoded:

- unsupported `$2B / two people / only AI` claim blocks for research;
- banned pseudo-profound phrase is a hard lint error;
- `Let me tell you`, `Guess what` and `bro` remain available voice moves;
- numeric claims produce verification warnings;
- hashtags and Cyrillic in final public copy fail;
- URLs and multiple emoji warn instead of blindly failing every context.
- canned transitions that only announce importance fail; the post must state the concrete consequence instead.

Update this file after real Kirill draft → accepted post pairs are available. Synthetic tests must not become a substitute for user feedback.

Dry-run details: `dry-run-results.md`.
