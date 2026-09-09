# Initial dry-run results

These scores use the original 16-point rubric. Future tests use the 22-point context/storytelling/formatting/no-fluff rubric.

## Case 01 — unsupported viral claim

Result: correctly blocked before rewriting. This is the required behavior for the existing `$2B / two people / only AI` post when no source is attached.

## Case 02 — build in public before launch

- Mechanical lint: passed with 0 errors and 0 warnings.
- Rubric: 14/16 provisional.
- Strengths: preserves the early-stage thesis, contains no invented result, reads cleanly on mobile, and turns “research” into a concrete tradeoff.
- Weakness: voice confidence remains provisional until more accepted Kirill posts exist.

## Case 03 — project voice overrides generic anti-slop

- Mechanical lint: passed with 0 errors and 0 warnings.
- Rubric: 15/16 provisional.
- Strengths: keeps `Let me tell you` and `bro` without stacking extra slang or forcing a CTA.
- Weakness: a real post should name the blocker when that information is available.

These results validate failure handling and project overrides. They do not replace shadow-mode testing on Kirill's next 10–20 real drafts.
