# X system verification — 30 September 2026

Scope: X radar, official releases, personal feed, competitors, Notion and radar Telegram bot only. LinkedIn deferred. Other projects and processes were not changed. Work stayed in the existing `tg-notes-x-radar` worktree. Secrets were loaded from existing local files and production configuration, never included in this report.

## Integration recovery

Initial live GETs confirmed radar enabled and Spark reports for 29 September 11/15/19, posts failures=13 with no successful run, following healthy, LinkedIn off. The old `radar-probe` omitted posts. Added posts and safe resource-level error context, deployed as `9719ef0`. Exact failing request was `GET /data_sources/af065d54-c401-4b85-b355-07fca5a7fc50` with Notion 404 under integration «Заметки». Notion MCP could read the same ID. After the owner added that connection, all five server targets returned readable=true.

Real posts sync at 29 September 20:58 UTC: 32 usable posts, 20 creates, 6 links, 1 relink, 1 metadata update, 4 unchanged. Telegram message 9, confirmed sent at 21:00:29 UTC. Repeat: 32 usable posts, zero creates/links/relinks/updates, 32 unchanged. Each request capped at 40 Apify rows; no paid limit was raised. Live Notion SQL aggregate checks: no repeated nonempty post URL, no repeated normalized competitor profile URL. Following already had a successful run at 07:29 UTC and confirmed Telegram message 5; it was not needlessly rescraped.

## Official source path

Implemented registry of 15 channels: OpenAI news and API changelog; Anthropic; Gemini API and Google AI; ElevenLabs; Vercel; GitHub; Cursor; Supabase; Cloudflare; HubSpot developer changelog; Google Ads API and Ads/commerce; Buffer. All 15 parsed successfully from the deployed Vercel service on the second live pass. Initial real failures exposed slash-redirect loops and Google's HTTP Feedburner redirect; both were corrected with transport slash preservation and an explicit HTTPS source/evidence allowlist.

Sources are polled every 30 minutes by the existing five-minute heartbeat, three due channels per invocation. No new paid collection or LLM-per-poll. First poll is silent history; updates do not reset event identity or delivery. Exact per-channel state, times and errors are available from authenticated `radar-official-status`. Deterministic relevance and release classification are conservative heuristics, not an independently verified benchmark or universal semantic clustering.

## Historical acceptance runs — TEST, not fresh alerts

| Case | Official evidence | Publication | Actual test observation | Telegram confirmed |
| --- | --- | --- | --- | --- |
| GPT-6.1 Sol | https://developers.openai.com/api/docs/changelog (Markdown adapter) | 29 Sep, day precision only; actual hour unknown | 29 Sep 21:15:21 UTC | 21:15:27 UTC, message 10 |
| Eleven v4 and v4 Turbo | https://elevenlabs.io/blog/eleven-v4 (Article JSON-LD) | 28 Sep 12:00 UTC; modified 29 Sep 08:52:01 UTC | 29 Sep 21:15:21 UTC | 21:15:33 UTC, message 11 |

Test processing/delivery latency: about 7 and 13 seconds. These observations do not prove historical discovery within an hour. With successful 30-minute polling, detection would be the first poll after an entry became observable. For GPT there is no source timestamp precise enough to name a historical hour. For Eleven the published timestamp is not proof of first public visibility; its CDN advertises `s-maxage=3600` and stale-while-revalidate. Publication-to-detection must not use the modification timestamp.

Notion reports were read back through MCP:

- GPT: https://www.notion.so/3ea79173929781ecba7afef495ceff62
- Eleven: https://www.notion.so/3ea791739297818b82a3c4ee9220d67a

Repeated replay returned exactly the same run IDs, report IDs and messages 10/11, without a new send. The two test candidates are in the existing approval queue; they have not been automatically promoted to the ideas database. A real owner tap was requested separately; do not infer it from delivery success.

## Personal feed and Spark

`x-radar-feed` was missing. It was installed with read-only X instructions, exact timestamps, null unknown metrics, a maximum of 30 posts/eight minutes and only the existing feed document as write target. Three existing analysis schedules received the new officialSources/sourceIds contract and explicit prohibition on invented acceleration/growth. `x-algorithm-audit` remains inactive.

First manual Spark feed task https://gemini.google.com/spark/chat/c6d507ba30f8bd4b failed during initialization with “Something went wrong. Please try again later.” It did not update the feed Doc. No permission prompt was observed, which is not proof that one will never be required.

A separately labelled manual Codex-browser pass read two real posts from the user's existing For You tab, wrote the existing feed Doc with `collector=manual-codex-browser-test`, and exported it back. Server `radar-feed-status` returned both as origin=feed. A feed-only run `390f09d7-8944-4b91-9d40-73c89fcca728`, key `test:2026-09-30T00:18`, persisted sourceCount=2/feedCount=2 and wrote its server input. No Apify request was used for this test. This proves Chrome → Doc → server input, not autonomous Spark browsing.

Live fault probes subsequently replaced only the feed Doc with an empty feed and a feed collected 19 hours earlier. Server accepted 0 posts in both cases. A `finally` restoration restored the exact saved payload; readback and server probe again confirmed 2 posts. The evidence file is `tmp/x-verification/feed-faults.json`. A later real Spark analysis through the existing 19:15 schedule read the new input (2 feed posts + 35 official sources), but Google Docs editing failed with `out of capacity`. At 21:49 UTC the actual output Doc still held old run `957c472b-3d17-440c-9044-b26175729621`; the server correctly did not accept it for the new test run. The new run remained awaiting its bounded deadline/API recovery at that observation; it is not a successful full Spark delivery.

Chrome feed depends on an awake computer, open Chrome, the signed-in X profile, permitted Gemini browsing and service quota. Empty/stale/unreadable feed falls back to the existing public Apify collection; official release polling does not depend on either. The feed alone is never advertised as a fully autonomous cloud collector.

Spark schedule UI does not expose a timezone. September observations fit UTC+3. Google's help states that a schedule locks to the location's timezone at creation and may be delayed/skipped under quota: https://support.google.com/gemini/answer/17094710?hl=en#schedules_timezones . This does not establish Riga versus Moscow DST behavior. Server compatibility windows cover both from 25 October using one paid run key; the noon digest remains Riga civil time.

## API reserve and test coverage

A real authenticated backup check on the deployed code returned Gemini 503 after 6.2 seconds; the API-reserve switch alone is not readiness. Previous 28 September grounding quota exhaustion is retained as historical evidence. The reserve was corrected to try all existing configured keys within a bounded two-minute request budget, rather than stopping at the first key. No subscription, billing or quota limit was changed. Source-only responses do not promote claims, ideas or forecasts as verified.

The repeat after deployment of key rotation still returned 503, after 32.6 seconds. This is a real upstream limitation; the analytical reserve is currently degraded, while the independent official monitor remains operational.

## Scheduled Chrome probe and local replacement

The new Spark feed schedule actually started unattended at 30 September 00:31 Moscow (29 September 21:31 UTC). Task: https://gemini.google.com/spark/chat/38fd921196df2027 . It explicitly reported that local Chrome automation and the signed-in X session were unavailable in its execution environment, and correctly left the feed Doc unchanged. No recurring approval prompt appeared; access to the local browser itself was absent. The computer and Chrome were open at the time. This disproves autonomous local feed collection through the tested Spark path, even though scheduled execution and Google Docs access work.

The two newly created Spark feed schedules are paused after this failure. The three existing Spark analysis schedules remain active. A local Codex heartbeat `x-radar`, titled «Лента X → Radar», is scheduled at 10:30/14:30/18:30 in this computer's local time (Windows Russian Standard Time, current UTC+3). It reads only the existing For You session through the browser extension, up to 20 records/eight minutes, and calls `scripts/radar-feed-upload.mjs` with a JSON file. That helper strictly validates dates, IDs, metrics, age and row count, replaces only the existing feed Doc and verifies the write by rereading it. The exact helper passed a live upload/readback on the two observed posts. Its first unattended timer run remains unverified; the automation should notify once when that happens.

The local route requires Codex and Chrome running on an awake PC. This worktree and its ignored `.env.radar.google.local` are now runtime dependencies of that local automation: do not archive/remove them without migrating the job. The fallback when the PC/browser/feed is unavailable remains server Apify plus official sources, not an invented personalized feed. The heartbeat stays quiet on normal runs and unchanged failures, notifying on a first success, changed failure, recovery or required action.

Full ship checks include TypeScript, all Vitest suites and Mini App production build. New regression coverage includes official sources with no X IDs, exact changelog fragments, wrong run ID, empty/stale feed, Spark failures, 429/503, publication versus modification, source alias clustering, repeated callback/decision CAS, uncertain writes, Telegram deduplication and the October timezone boundary. Test results are not a substitute for the live evidence above.

The final full suite passed 811 tests, including the additional regression for calling the same Telegram callback handler twice with an expired callback's Telegram 400 response, without a second decision or promotion. This is a mocked transport test. An attempted live replay of an already settled decision stopped locally before network access because the owner ID is masked in the pulled environment; no user identity was guessed. Real owner taps on the newly delivered test messages were still pending at the final observation. Clicking «Отклонить» on one test is the remaining human step for a fresh decision round-trip; no new approval is fabricated to make the test green.

Final live failure-path check at 29 September 22:02 UTC: after the test deadline and the two permitted API attempts, run `390f09d7-8944-4b91-9d40-73c89fcca728` became `failed` with `radar_backup_attempt_limit`. Error delivery was confirmed as Telegram message 12 at 22:02:02 UTC. The run no longer holds the analysis pipeline; sync and official-monitor ticks remained healthy. The old Spark report was never presented as a new result, and no false verified idea was created. This proves bounded recovery/failure notification, not a healthy upstream model service. Empty/stale feed and HTTP authorization were also checked live: 0/0 accepted posts and HTTP 401 on unauthenticated diagnostics.

Detailed response captures are in ignored `tmp/x-verification/`; public HTTP fixtures and hashes are in ignored `tmp/official-fixtures/`. These are diagnostic artifacts, not committed credentials or raw Notion datasets.

Final discovery check at 29 September 22:06 UTC used the real fetchOfficial → listingUrls path on the ElevenLabs blog without supplying the regression URL: eleven-v4 was the first discovered article. The adapter caps discovery at eight links, so non-featured articles below that cap are a coverage limitation. Corporate appointments and political/election posts are explicitly excluded from release alerts even when their body mentions AI models. Final runtime deployed via ship: ef73dcb; all 811 tests, type checks, build and production probes passed.
