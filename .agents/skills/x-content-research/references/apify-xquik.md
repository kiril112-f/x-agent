# Apify Xquik workflows

Actor: `xquik/x-tweet-scraper` via the project `apify-x` MCP.

If the MCP connection is unavailable during local debugging, use `python x-content-engine/scripts/apify_x_scrape.py`. The script reads the same `APIFY_TOKEN` environment variable, uses an Authorization header, and enforces a 500-row hard cap.

Use `outputVariant: "rich"`, `fieldStyle: "camelCase"`, `outputPreset: "flat"`, and `includeSearchTerms: true` unless the task requires the original nested shape.

## 1. Reference-account scan

Use for recent posts from known creators:

```json
{
  "mode": "profileTweets",
  "twitterHandles": ["levelsio", "ErnestoSOFTWARE"],
  "maxItems": 50,
  "maxItemsPerTarget": 25,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "flat"
}
```

Do not treat follower count as quality. Extract the thesis, evidence, structure, audience and performance context.

## 2. Topic/idea discovery

Use 2–4 narrow queries, English only, excluding replies and native retweets unless replies are the research object:

```json
{
  "mode": "search",
  "searchTerms": [
    "(mobile app OR indie app) (growth OR UGC) lang:en min_faves:50 -filter:replies",
    "(AI app OR AI workflow) (shipped OR revenue) lang:en min_faves:50 -filter:replies"
  ],
  "queryType": "Latest + Top",
  "maxItems": 100,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "flat",
  "includeSearchTerms": true
}
```

Adjust thresholds to account size and recency. A low-follower post can be more useful than a viral generic post.

## 3. Quote-post opportunity

Look up the exact tweet plus direct quotes/replies only when they change the angle. Keep the original URL and author. Never turn a paraphrase into Kirill's original insight.

## 4. Competitor pattern mining

Pull 20–50 posts per account, then compare:

- hook type;
- topic/pillar;
- format and length;
- proof type;
- media type;
- CTA;
- likes, replies, reposts, bookmarks/views when present;
- engagement relative to that account's baseline, not only raw totals.

Do not clone wording. Convert recurring patterns into hypotheses to test.

## 5. Own-account learning

Pull `KirillMorozovop` posts, join with Notion review notes, and record which structures earned disproportionate views/replies. Do not infer causality from a tiny sample.

## Candidate scoring

Score internally from 0–2:

- audience fit;
- freshness;
- concrete evidence;
- original angle available to Kirill;
- usefulness beyond the source post;
- reputational safety.

Return the strongest 3–10 ideas, not a dump of every scraped row.

## Failure handling

- Diagnostic row or empty results: narrow/repair the query once, then stop and report the limitation.
- Actor timeout: keep delivered rows and mark coverage incomplete.
- Schema change: inspect the current Actor details before changing the workflow.
- Never send X cookies, passwords or session tokens to an Actor.
