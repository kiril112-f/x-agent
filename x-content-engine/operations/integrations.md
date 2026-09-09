# Integrations

## X Docs MCP

Enabled in `.codex/config.toml`. It is read-only and needs no account credentials.

## Notion MCP

Notion is already connected in the user's global Codex configuration. This project intentionally does not redeclare `mcp_servers.notion`, because Codex merges global and project configuration layers. Use the existing connection and its current permissions.

## Apify X research MCP

Configured at `https://mcp.apify.com?tools=xquik/x-tweet-scraper` with a bearer token read from the Windows user environment variable `APIFY_TOKEN`.

Actor: `xquik/x-tweet-scraper`.

- Reads public X posts, profiles, search, lists, threads, replies and quote context.
- Has no X account credentials and cannot perform actions on X.
- Default cap: 100 delivered rows per research task.
- More than 500 rows or recurring collection requires approval.
- The primary key is stored as `APIFY_TOKEN` and the second key as `APIFY_TOKEN_FALLBACK`, both in the Windows user environment rather than project files.
- The MCP uses the primary key. The local `scripts/apify_x_scrape.py` fallback uses `APIFY_TOKEN_FALLBACK` only when the primary variable is absent.
- Restart Codex after changing either environment variable so a new process inherits the values.

The selected Actor advertises $0.15 per 1,000 delivered rows on every Apify plan; Apify platform usage may be additional. Check current Actor pricing before large runs.

## Manual X publishing

No X API or publishing MCP is configured. Kirill posts, schedules, replies and reacts manually after review.
