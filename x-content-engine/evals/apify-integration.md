# Apify X research integration — validation

Validated on 2026-08-30.

- Both user-provided tokens were valid; only the selected primary token is retained in the Windows user environment as `APIFY_TOKEN`.
- Project config exposes only `xquik/x-tweet-scraper` through the official Apify MCP endpoint.
- MCP initialize handshake succeeded with protocol `2025-06-18`.
- Tool discovery confirmed the Actor tool plus run and dataset inspection tools.
- Direct Actor smoke test returned 3 public posts from `@KirillMorozovop`.
- Fallback script smoke test returned 2 public posts from the same account.
- Unit suite: 12/12 tests passed after integration.
- X API publishing MCP was removed; `x-publish` is deprecated and disabled.

Operational limits:

- Default research pull: 5–100 rows depending on task.
- Hard local script cap: 500 rows.
- Larger or recurring scrapes require approval.
- Raw rows stay in Apify unless a specific export is needed; Notion receives selected idea cards and conclusions.
