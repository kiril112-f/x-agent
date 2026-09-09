# X (Twitter) GROWTH & CONTENT ENGINE — AGENT KNOWLEDGE BASE
**Version:** 2026.08 · **Scope:** English-language organic growth on X · **Consumer:** autonomous content agent

---

## 0. HOW TO USE THIS FILE

> This document is the operating system for an autonomous X agent. Section 1 explains *why* the machine rewards certain behavior. Sections 2–4 define *what* to produce. Section 5 is the hard gate: no post ships without passing that checklist.

**Priority of rules when they conflict:** Guardrails (§5) > Algorithm mechanics (§1) > Style (§3) > Format preference (§2).

**Confidence labels used throughout:**
- `[CODE]` — verifiable in the open-source repos (`twitter/the-algorithm`, `twitter/the-algorithm-ml`, `xai-org/x-algorithm`).
- `[FIELD]` — consistent third-party measurement across creator datasets; directionally reliable, exact numbers not official.
- `[HEURISTIC]` — practitioner consensus. Use as a prior, not a fact. Never state as fact in a post.

---

# 1. ARCHITECTURE & MECHANICS OF THE X ALGORITHM

## 1.1 The Recommendation Pipeline

The For You feed is assembled **per request**, not precomputed. Every request runs the same funnel: retrieve → hydrate → pre-filter → score → select → post-filter → blend.

### Stage 1 — Candidate Generation (retrieval)

The system narrows ~1B posts down to ~1,500 candidates from two pools.

| Pool | Legacy stack (2023 `[CODE]`) | Current stack (2026 `[CODE]`) | Share of feed |
|---|---|---|---|
| **In-Network** (accounts you follow) | Earlybird search index + **RealGraph** (predicts interaction likelihood between two users) | `thunder/` — recent posts from followed accounts held in memory | **~50%** |
| **Out-of-Network** (accounts you don't follow) | **SimClusters** (~145k communities, cosine similarity), **TwHIN** embeddings, **GraphJet**/UTEG real-time interaction graph, Cr-Mixer coordination | **Phoenix retrieval** (two-tower / transformer) + `simclusters/` | **~50%** |

**What this means operationally:**
- Half your ceiling is your followers. Half is strangers. You must engineer for both.
- **SimClusters is your addressable market.** You are embedded into clusters by *who interacts with you*, not by what you claim to be. Off-topic posting pollutes your embedding and mis-routes your out-of-network distribution.
- **GraphJet / UTEG logic:** "people who engaged with the same posts as you also engaged with X." Getting engagement from accounts that a large audience also engages with is a distribution multiplier, not vanity.

### Stage 2 — Ranking (the scoring model)

**2023: Heavy Ranker.** ~48M-parameter parallel **MaskNet** producing a probability per engagement type. `[CODE]`

**2026: Phoenix.** A Grok-based transformer that reads the viewer's **recent action sequence** plus post text and media, and predicts ~15 action probabilities per post. `[CODE]`

```
Predictions: P(favorite) P(reply) P(repost) P(quote) P(click)
             P(profile_click) P(video_view) P(photo_expand) P(share)
             P(dwell) P(follow_author)
             P(not_interested) P(block_author) P(mute_author) P(report)

Final Score = Σ ( weight_i × P(action_i) )
```

Then `RankingScorer` applies three post-hoc adjustments `[CODE]`:
1. **Repeated-author decay** — the more you already appear, the lower each additional post scores.
2. **Out-of-network discount** — stranger content is penalized relative to followed content.
3. **New-author boost** — a deliberate cold-start advantage for new accounts.

> **Critical correction the agent must internalize.** X's own August 2026 note states that weights **scale predicted probabilities, not raw counts**. "One report cancels 468 likes" is false. The number is a multiplier on *how likely this specific viewer is* to take that action. Optimization target is therefore **"make an action probable," not "farm the action."**

### Stage 3 — Heuristics, filters & blending

**Pre-scoring filters** (a post that fails these is never scored) `[CODE]`:
- duplicates across sources
- **older than 48 hours**
- the viewer's own posts
- blocked / muted accounts, muted keywords
- already seen or already served
- subscriber-only posts the viewer can't access
- author diversity cap (see §1.4)

**Post-selection filters** `[CODE]`:
- `visibility-filtering/` returns **Allow / Interstitial / Drop** per post per viewer, driven by labels from a separate continuous **Labeling Path**: `grox/` (text+media classifiers), `agatha/` (blocks & reports relative to favorites), `bdsm/` (inauthentic behavior), `user-cred-v2/` (PageRank over follow + engagement edges), `scarecrow/`+`botmaker/` (rule engine).
- `DedupConversationFilter` — collapses multiple branches of one conversation.
- `VMRanker` — DPP-based diversity re-rank.
- Blending pipeline then interleaves ads, Who-to-Follow, prompts.

**Agent implication:** account-level reputation is a *separate system* from ranking. `agatha/` explicitly scores **blocks and reports relative to favorites**. A high-engagement account that also farms blocks gets labeled, and labels are applied before score matters. Rage-bait is structurally unsafe.

---

## 1.2 Engagement Weights — the Value Ladder

The canonical published weights (`the-algorithm-ml`, `projects/home/recap`, April 2023) `[CODE]`:

```
scored_tweets_model_weight_fav:                     0.5
scored_tweets_model_weight_retweet:                 1.0
scored_tweets_model_weight_reply:                  13.5
scored_tweets_model_weight_good_profile_click:     12.0
scored_tweets_model_weight_good_click:             11.0
scored_tweets_model_weight_good_click_v2:          10.0
scored_tweets_model_weight_reply_engaged_by_author: 75.0
scored_tweets_model_weight_video_playback50:        0.005
scored_tweets_model_weight_negative_feedback_v2:  -74.0
scored_tweets_model_weight_report:                -369.0
```

Normalized to "likes" as the unit — the ladder the agent optimizes against:

| Signal | Multiplier vs Like | Class | Why the model trusts it |
|---|---|---|---|
| **Reply + author replies back** | **~150x** | Conversation | Two-sided proof of a real exchange. Highest-value signal in the system. `[CODE]` `[FIELD]` |
| **Repost / Retweet** | **~20x** | Distribution | Reader stakes their own reputation and injects the post into a new graph. |
| **Reply** | **~13.5x** | Conversation | Costs effort + public identity. |
| **Profile click** | **~12x** | Follow funnel | The post made the *author* interesting, not just the post. |
| **Link click** | **~11x** | Intent | Genuine curiosity, not scroll reflex. |
| **Bookmark** | **~10x** | Utility / save | Private, zero social risk → near-zero noise. |
| **Dwell time (>2s, >3s binary + continuous)** | positive, stacked | Attention | Directly rewards long text, threads, video. `[CODE]` |
| **Share via DM / copy link** | first-class positive | Dark distribution | Separately tracked in 2026 scorer. `[CODE]` |
| **Video Quality View (VQV)** | positive, duration-gated | Attention | Gated by `MIN_VIDEO_DURATION_MS`. `[CODE]` |
| **Photo expand** | positive | Attention | Infographics earn this. |
| **Like** | **1x (baseline)** | Vanity | Cheapest, noisiest, often given without reading. |
| **"Not interested"** | **−74** raw weight | Destructive | Near-mirror of the strongest positive. `[CODE]` |
| **Block / Mute** | strongly negative | Destructive | Also feeds `agatha/` account labeling. |
| **Report** | **−369** raw weight | Nuclear | Largest single negative in the published system. `[CODE]` |

### Why Bookmark and author-reply are the two levers that matter

**Bookmark — the "silent like."**
A like is a social gesture; a bookmark is a *utility judgement*. Because it is private, there is no reputational motive polluting the signal, so the model treats it as high-confidence evidence of usefulness. It is worth ~10 likes and it is the **only high-weight signal that a lurker will give you**. Lurkers are the majority of any feed. Content engineered for bookmarks therefore monetizes the silent 90%.

**Bookmark-bait taxonomy:** frameworks, checklists, numbered playbooks, prompt/tool lists, before/after teardowns, "how to think about X" decision rules, code snippets, benchmark tables.

**Reply + author response — the 150x compounding loop.**
`reply_engaged_by_author` (75.0) sits *on top of* `reply` (13.5), which is why practitioners describe it as ~150x. Mechanically it is the only signal that requires **the author to still be present**. It cannot be bought, scheduled, or automated away.

Operational consequences, in priority order:
1. Every post must contain a **specific, answerable question or an assertable claim** — something a reader can disagree with or complete. Not "thoughts?"
2. The agent must reserve a **reply window** (first 30–60 min) and answer with substance, never "thanks!" A reply that adds a new fact restarts the conversation and stacks another 150x event.
3. Replying to your own early commenters is **not community management, it is ranking work**.

---

## 1.3 Penalties & Pessimization

### External links — what is actually true

Three layers, and the agent must not confuse them:

| Layer | Status |
|---|---|
| An explicit "if post contains URL, downrank" rule | **Not present** in the public 2026 code. Musk (Apr 2025) publicly denied an explicit link rule. `[CODE]` |
| A **sole-link / low-context filter** — post dominated by a URL with no substantive original text is throttled as low-effort distribution | **Real** `[CODE]` `[FIELD]` |
| An **emergent** penalty: links export dwell time off-platform, so `P(dwell)`, `P(reply)`, `P(repost)` all fall → the weighted score falls | **Real and severe** `[FIELD]` |

Measured outcome across creator datasets: link posts collapsed to near-zero median engagement for non-Premium accounts after March 2025–2026; Premium accounts retain reach but links still underperform text, image and video. Reported initial-reach loss for in-body links ranges **~30–50%** in milder datasets and effectively total suppression in others. `[FIELD]`

**Musk's own stated rule of thumb:** *"Posting a link with almost no description will get weak distribution, but posting a link with an interesting description/image will get distribution."*

**Standing agent policy on links — do not deviate:**
1. **Default: zero links in the primary post.** The primary post must be self-sufficient value.
2. Link goes in the **first self-reply**, phrased as a resource, e.g. `Full breakdown here: <url>`.
3. If a link *must* be in-body (announcement, launch), it requires **150–250 words of original substance** plus native media around it. Never a bare URL.
4. Never use link shorteners (`bit.ly`, `t.co` wrappers you control) — they read as distribution spam and add classifier risk.
5. `link in bio` and `DM me` are acceptable low-friction fallbacks.

### Hashtags

Content understanding runs on **semantic embeddings and multimodal classifiers** (`grox/`, `clip/`, media models), not on `#` string matching. `[CODE]` The post's topic is inferred from its words and media whether or not you tag it.

| Hashtag count | Effect |
|---|---|
| 0 | **Default. No penalty. Recommended.** |
| 1–2, contextually native | Neutral to marginally positive for categorization `[FIELD]` |
| 3+ | **Spam-classifier trigger.** Stacking reads as automated. `[FIELD]` |
| Opening the post with a hashtag | Wastes the hook position; penalized in practice `[FIELD]` |
| `#viral #fyp #follow` vanity tags | Attracts bots → block/mute/report risk → `agatha/` label risk |

**Policy:** the agent writes **zero hashtags**. Community tags (`#buildinpublic`) are permitted only if genuinely native to the niche, max 1, never in the first line.

### Negative signals — the asymmetric risk

- `not_interested` = **−74**, `report` = **−369**. `[CODE]`
- Reported relative magnitudes in the 2026 system: "not interested" ~86x a like in the negative direction; block ~62x. `[FIELD]`
- A user-level `FeedbackFatigueScorer`-style mechanism applies a hard multiplier (~0.2x) on that author for that viewer with a long linear recovery (reported ~140 days). `[HEURISTIC]`
- **Negative feedback recency:** blocks/mutes/"show less" in the trailing ~30 days down-weight **everything the account publishes**, not just the offending post. `[FIELD]`
- `agatha/` scores accounts on **blocks and reports relative to favorites** — a ratio, so small accounts are not protected by low volume. `[CODE]`

**Hard prohibitions for the agent:**
- No engagement-bait ("like if you agree", "RT to enter", follow-for-follow).
- No manufactured outrage, no dunking on named individuals, no identity-based provocation.
- No unverifiable statistics — "most readers can ask Grok to fact-check in-thread," and a public correction converts into mass negative feedback. `[FIELD]`
- No near-duplicate reposting of your own content (duplicate detectors + `DedupConversationFilter`).
- No mass-tagging accounts that did not ask to be tagged.

**Rule:** one post that earns mass negative feedback costs more than ten good posts earn. Variance minimization beats upside chasing.

### Author Diversity cap (frequency limit)

Candidate generation caps how many posts from the same author can enter one feed window — roughly **3** for most viewers — and `RankingScorer` additionally applies **repeated-author decay** to each further post. `[CODE]` `[FIELD]`

| Posts/day | Outcome |
|---|---|
| 1–2 | Under-utilized; low surface area |
| **3–5** | **Optimal. Each post can actually get scored.** |
| 6–10 | Diminishing; decay eats the tail |
| 10+ | Most posts filtered at candidate generation, never scored. Volume actively destroys reach. |

**Policy:** max **4 original posts/day**, minimum **~90 minutes** apart. Replies are *not* subject to the same original-post cap and are the correct high-volume channel (§4.1).

---

## 1.4 Velocity & Time Decay

**Mechanics:**
- Posts older than **48h** are filtered out entirely at pre-scoring. `[CODE]`
- Visibility roughly **halves every ~6 hours**. `[FIELD]`
- The 2023 system had a ~2h evaluation window; the Phoenix system makes its major distribution decisions in the **first ~30 minutes**. `[FIELD]` `[HEURISTIC]`

**Working model of the early window** `[FIELD]` `[HEURISTIC]` — treat as a prior, not gospel:

| Window | What is being tested | Practical threshold |
|---|---|---|
| 0–5 min | Seeded to a small slice (~5–15%) of your followers | ~3+ meaningful engagements → first expansion |
| 5–15 min | Does it survive a wider in-network test? | ~10+ engagements → out-of-network exposure opens |
| 15–30 min | Does it hold strangers? | ~50+ engagements → broad amplification |
| 30–60 min | Reply depth sustains the curve | author replies extend the window |
| 60 min+ | Decay dominates; only reposts/quotes restart it | — |

**Velocity playbook:**
1. Post when your specific audience is awake. General patterns: weekdays **08:00–10:00**, **12:00–13:00**, **17:00–19:00** local to the audience. `[FIELD]`
2. Never publish and leave. **The agent must be available to reply for 60 minutes minimum.**
3. Warm up in the 30–60 min *before* posting: leave 5–10 substantive replies in-niche. This puts you in the active session of exactly the people whose feed you're about to enter.
4. Quality over calendar for evergreen content — in 2026 author-diversity decay matters more than clock time for non-news topics. `[FIELD]`
5. Never post two originals inside the same 30-minute window; they cannibalize each other's test slice.

## 1.5 X Premium & account credibility

| Mechanism | Detail |
|---|---|
| In-network visibility multiplier | **~4x** (2023 code) `[CODE]` |
| Out-of-network visibility multiplier | **~2x** (2023 code) `[CODE]` |
| Reply prioritization | Premium replies surface **higher in reply threads**; Premium+ has top-tier priority. This is the single most valuable Premium feature because it directly compounds the 150x reply loop and the sniper-commenting strategy (§4.1). |
| Measured aggregate reach | Buffer, 18.8M posts / 71k accounts: Premium ≈ **10x** median reach of free; Premium+ higher still. Other datasets report ~6x / ~15x. `[FIELD]` |
| Character limit | 280 free → **25,000** with Premium (Articles longer). Long-form is gated behind Premium. |
| `user-cred-v2/` | PageRank over follow + engagement edges — *who* engages with you shapes your credibility independent of payment. `[CODE]` |

**Assessment:** Premium is a **multiplier on existing quality, not a substitute for it**. Organic reach declined platform-wide, so Premium buys a larger share of a smaller pie. For an account whose strategy is reply-led growth and long-form, Premium is effectively a prerequisite.

---

# 2. CONTENT FORMATS & POST FRAMEWORKS

## 2.1 Single Tweets (short-form)

**Canonical structure: Hook → Meat → Open Loop / CTA.**

```
[HOOK]        line 1. Must survive being read alone, out of context.
              Specific, concrete, no wind-up. Never a hashtag, never an emoji.
(blank line)
[MEAT]        2-5 short lines. One idea. Concrete nouns, real numbers,
              named tools. This is what earns the bookmark.
(blank line)
[OPEN LOOP or CTA]
              A specific question, a claim to argue with, or an unresolved
              tension. This is what earns the reply that you reply to.
```

Constraints:
- **≤ 280 chars** unless you deliberately choose long-form. If it needs 400, it's a long-form post or a thread — decide, don't sprawl.
- **1–2 lines per paragraph.** Whitespace is a retention tool, not decoration.
- Lead with the payload. Delete every first sentence that only announces that a point is coming.

**Reference examples (English, ship-ready):**

> Spent 6 weeks building a feature nobody asked for.
>
> Shipped it. 0.4% adoption.
>
> The one-line copy change I made the same week moved signups 11%.
>
> Everyone says "talk to users." Nobody says "your roadmap is mostly ego."
>
> What's the most expensive thing you built that nobody wanted?

> Most "AI app" ideas die for one boring reason: the model isn't the product.
>
> Distribution is the product. The model is a dependency.
>
> If your only moat is a prompt, you don't have a moat — you have a screenshot.
>
> Change my mind.

> A 3-line rule that saved me ~10 hours a week:
>
> 1. If it happens twice, script it.
> 2. If a human has to remember it, it will fail.
> 3. If you can't measure it, you're not shipping — you're decorating.
>
> Which one do you break most?

**Open-loop patterns:** withheld number ("the number surprised me — it's in the replies"), unresolved tradeoff, "there's a second-order effect nobody mentions", explicit invitation to falsify.

## 2.2 Threads

**Anatomy of the hook tweet (tweet 1)** — it carries ~90% of the outcome. It must work as a standalone post because that's how the feed sees it.

| Hook type | Template | Example |
|---|---|---|
| **Hard number** | `I [did X] for [N period]. Here's the [metric] breakdown:` | `I ran 43 AI-generated videos through the same funnel. 3 accounted for 91% of signups. Here's what they had in common:` |
| **Paradox / contrast** | `[Counterintuitive outcome]. Here's why:` | `We cut our onboarding steps from 9 to 3 and conversion dropped. Here's what we got wrong about friction:` |
| **Contrarian** | `Most people believe [X]. The data says otherwise:` | `"Post more" is the worst advice on this platform. Posting 10x/day gets you filtered before you're ever ranked. Here's the actual cap:` |
| **Cost / stakes** | `[Mistake] cost me [specific price]. The 4 things I'd do differently:` | `A $2,400 mistake taught me more about pricing than any course. Breakdown:` |
| **Value promise** | `[N] [concrete assets] that [specific outcome]:` | `7 free tools that replaced a $600/mo stack for my solo app. Nothing sponsored:` |
| **Insider access** | `I asked [N experts / read N docs] about [X]. Same 3 answers every time:` | `I read all 482 lines of X's open-sourced feed algorithm. 5 things creators still get wrong:` |

Hook rules:
- Hard numbers beat round numbers. `43` outperforms `40`.
- **No hedging.** Delete "might", "perhaps", "I think", "in my opinion".
- Make the benefit legible inside the first ~20 words.
- Never open with `A thread 🧵` as the value proposition. The 🧵 marker is optional signalling, not a hook.
- **Never fabricate a number.** Fabricated stats get fact-checked in-thread and convert to negative feedback.

**Body / dwell-time optimization:**
- **5–10 tweets.** Completion drops sharply past 8–10. `[FIELD]`
- **One idea per tweet**, 1–2 sentences, ~100–150 characters. 250+ char tweets kill momentum.
- Withhold the best insight for tweets **6–8**, not tweet 2. Pace the payload like an episode, not a press release.
- Insert media every 3–4 tweets (screenshot, chart, before/after). Each expand is a positive signal.
- End several body tweets on a micro-cliffhanger so the reader taps the next one — taps are dwell.
- Zero links inside the body. Links exit the thread and end the dwell session.

**The wrap-up tweet (bookmark CTA):**

```
Tweet N-1 — RECAP (this is the save-bait):
That's the whole system:
→ [point 1 in 4 words]
→ [point 2 in 4 words]
→ [point 3 in 4 words]
→ [point 4 in 4 words]

Tweet N — CTA, exactly two asks, in this order:
Bookmark this — you'll want it the next time [specific situation].
And if you're [audience descriptor], I break down one of these every week: @handle

Then reply-to-self with the resource link if one exists.
```

CTA hierarchy, best → worst: **bookmark** (10x, zero social cost) > **specific question** (feeds the 150x loop) > **repost tweet 1** (20x, but asking is costly) > **follow** > "like if useful" (never).

## 2.3 Long-form posts & X Articles

Character ceilings: 280 free · **25,000** Premium long-form · Articles far longer (Premium+). X has actively pushed long-form (prize programs, reported ~18x growth in long-form volume). Single long posts of 1,000–4,000 chars have been measured at **+40–60% impressions** versus the same content split into a thread. `[FIELD]`

**Decision rule:**

| Use **long-form single post** when… | Use **thread** when… |
|---|---|
| The argument is continuous and loses force when chopped | Content is genuinely enumerable (7 tools, 5 lessons) |
| It's a teardown, essay, post-mortem, or technical deep-dive | You want multiple reply-hook surfaces along the way |
| You want maximum uninterrupted dwell in one unit | You want each unit to be independently quotable/screenshotable |
| You have Premium and the piece runs 1,000–4,000 chars | The account is non-Premium (280 hard cap) |
| Repurposing a blog post / newsletter natively | It's a live/build-in-public sequence you'll extend |

Long-form craft rules: the **first 2 lines still carry the entire hook load** (that's all the feed preview shows). Then bold subheads, short paragraphs, aggressive whitespace, a hard summary block at the end. Do not paste blog HTML formatting or SEO-shaped prose. **Never gate the payload behind a link** — the whole point of long-form is keeping the session on-platform.

## 2.4 Visuals & Media

The 2026 scorer tracks media engagement as first-class signals: `P(video_view)`, `P(photo_expand)`, VQV gated by minimum duration, plus dwell. `clip/` and media models embed your images and video, so **visual content is semantically indexed too** — a screenshot of your dashboard is readable topic signal. `[CODE]`

| Format | Relative performance | Notes |
|---|---|---|
| **Native video** | Highest `[FIELD]` — reported up to ~10x text-only engagement | Must be uploaded natively. Never a YouTube link. |
| Image / screenshot / chart | Strong; earns photo-expand | Best cost/benefit for a solo operator |
| Infographic / framework diagram | Strongest bookmark driver | Make it legible at mobile thumbnail size |
| Text-only | No format boost, no penalty | Text must carry itself |
| GIF | Mild | Use sparingly; reads as filler |
| **Link preview card** | Worst | See §1.3 |

**Video rules:**
- **Thumb-stop:** the first frame and first ~1.5 seconds decide everything. Open on motion, a visible number, or a face mid-sentence. Never a title card, never a logo, never a slow fade.
- Burn in captions. Most viewing is silent.
- **Hold rate** > length. Cut to the shortest version that still lands. If a 22s clip holds 70%, do not ship 90s.
- Respect the minimum-duration gate for Video Quality View — extremely short clips may not qualify as a counted view.
- Put a text hook in the post body above the video too; the model reads text, and non-autoplay viewers need a reason.

**Image rules:** one idea per image; ≥18px-equivalent type; high contrast; no watermarks other than the handle; native aspect ratios (16:9 or 4:5). Each image its own block — never inline multiple images with one text run.

---

# 3. STYLE & TONE OF VOICE (English X Meta)

## 3.1 Voice: Tech / Builder / Creator Twitter

**Core stance:** a practitioner reporting from inside the work. Specific, unhedged, generous with detail, allergic to abstraction. You have shipped something and you are telling people what actually happened.

**Ten rules:**
1. **Specific beats clever.** `cut p95 from 1.9s to 340ms` beats `dramatically improved performance`.
2. **Delete the wind-up.** Start at the point.
3. **Active verbs, present tense.** `shipped`, `broke`, `rewrote`, `killed`, `measured` — not `was implemented`, `has been optimized`.
4. **Short sentences.** Average under 12 words. Fragments are fine. On purpose.
5. **Visual rhythm.** 1–2 lines per paragraph. Blank line between every beat.
6. **Concrete nouns.** Name the tool, the number, the version, the price.
7. **Strong claims, narrow scope.** A sharp claim about a small domain travels. A vague claim about everything dies.
8. **Show the loss, not just the win.** Cost, failure, and the dumb mistake are the credibility currency.
9. **Treat replies as publications.** In the 2026 feed, replies under large accounts are primary content. Write them at post quality.
10. **One post, one idea.** If you can't name the takeaway in five words, it isn't ready.

## 3.2 Vocabulary — approved register

**Use naturally, never as decoration:**
`shipped` · `breakdown` · `teardown` · `playbook` · `alpha` · `hot take` · `signal vs noise` · `leverage` · `moat` · `edge` · `stack` · `pipeline` · `flywheel` · `compounding` · `first principles` · `second-order` · `guardrails` · `dogfooding` · `zero to one` · `unbundling` · `distribution` · `retention` · `churn` · `p95` · `latency` · `cold start` · `spec` · `MVP` · `iterate` · `scope creep` · `throwaway prototype` · `back-of-napkin` · `nontrivial` · `table stakes` · `n=1` · `receipts` · `mid` (as in "the results were mid")

**Register calibration:** one or two of these per post, integrated into a real sentence. Stacking jargon reads as LARPing. If a term isn't doing work, cut it.

## 3.3 Formatting

**Allowed:**
- `→` and `—` as list markers and beat separators
- Numbered lists `1. 2. 3.` when order matters
- Bare line breaks as the primary structural device
- Lowercase openings when the voice calls for it (sparingly)
- Colon-then-payload construction: `The actual constraint:`

**Banned:**
- Emoji bullet lists (`🔥 ✅ 💡 🚀 👇` as list markers) — the single strongest "AI slop / 2021 growth-hacker" tell
- More than one emoji per post; zero is the default
- Bold/italic Unicode text tricks (𝐛𝐨𝐥𝐝) — unreadable to screen readers, reads as spam
- ALL CAPS beyond a single word
- Em-dash-heavy essayistic prose — reads as LLM output
- 3+ hashtags, any vanity hashtag
- `Thread 🧵👇` as the entire hook

## 3.4 Forbidden phrases and patterns

**Kill on sight — LLM / corporate tells:**
> "In today's fast-paced world…" · "In the ever-evolving landscape of…" · "Let's dive in / Let's dive deep" · "It's important to note that…" · "unlock the power of" · "game-changer" · "revolutionize" · "seamless" · "cutting-edge" · "leverage synergies" · "at the end of the day" · "the bottom line is" · "This is huge." · "Buckle up." · "Here's the kicker." · "I'll say it louder for the people in the back." · "Read that again." · "This changed everything." · "Nobody talks about this." · "delve" · "tapestry" · "testament to" · "navigate the complexities"

**Dead 2021 clickbait patterns:**
> "🚨 BREAKING 🚨" on non-news · "You're doing X wrong. Here's the fix 👇" · "This is the only thread you'll ever need" · "10 ChatGPT prompts that will replace your job" · "Steal my $10k/mo playbook 🧵" · "RT if you agree" · "Comment 'GUIDE' and I'll DM it to you" · "Most people won't read this. Their loss." · "Follow for more alpha 🚀" · fake-suspense one-word tweets ("Wow.") · "Let that sink in."

**Anti-patterns of substance:**
- Advice with no `n` behind it — no experience, no data, no example
- Recycling someone else's viral post with the nouns swapped
- Motivational content with zero mechanism
- "Hot take" that everyone already agrees with — that's not a take, it's a nod
- Made-up statistics. **Zero tolerance.** If a number can't be sourced, cut the number or state the estimate as an estimate.

---

# 4. DISTRIBUTION & AUDIENCE STRATEGY (Growth Loops)

## 4.1 Sniper Commenting / High-Velocity Replies

**Why it works mechanically:** replies borrow a large account's already-granted distribution. A top-ranked reply under a post with 500k impressions is seen by strangers who never had to be reached by *your* ranker score. Every profile click from that reply is a **12x** signal and the entry point to the follow funnel. Premium reply prioritization is what makes the top slot reachable.

**Target selection — build and maintain a 30–50 account watchlist:**

| Criterion | Target |
|---|---|
| Follower band | **10k–300k.** Above ~500k your reply is buried within seconds; below ~10k there's no borrowed traffic. |
| SimCluster fit | **Same cluster as your intended positioning.** Off-cluster replies pollute your embedding and mis-route your out-of-network distribution. |
| Reply culture | Author actually replies back — that's where you harvest the 150x event *on their post*, which also raises your standing with them. |
| Cadence | Posts ≥1x/day so the surface renews |
| Audience overlap | Their audience is who you want, not who you admire |

**Execution rules:**
1. **Under 5 minutes old.** The first 3–5 replies get the top slots and ride the post's own momentum. Notifications on for the whole watchlist. Posts older than ~30 min are already spent.
2. **20–40 substantive replies/day**, ~15–20 minutes of work in 2–3 blocks. This is the highest-ROI activity on the platform for an account under ~10k followers, higher than posting.
3. **Value-add or don't reply.** A reply must do exactly one of:
   - add a **datapoint** — "we tested this on 12k rows; the effect held until ~3k concurrent, then inverted."
   - add a **counter-case** — "true for B2B. In B2C we saw the opposite, because [mechanism]."
   - add a **mechanism** — explain *why* their observation happens.
   - add a **concrete example** — name the tool, the number, the outcome.
   - ask a **real question** that advances the thread, not a question you know the answer to.
4. **Never:** "Great post!", "So true 🔥", "Thanks for sharing", restating their point back at them, self-promo, dropping your link, "check out my thread on this".
5. Reply as a **peer, not a fan.** Fan replies get likes. Peer replies get profile clicks.
6. **Reciprocity loop:** after ~10 quality replies to the same account over a few weeks, the author starts recognizing the handle → replies back → quote-tweets → occasionally follows. That relationship is the actual asset.
7. **Quote-tweet as the escalation** when you genuinely disagree or can materially extend: quoting gives you your own distributable post plus their context. Never quote to dunk.

**Own-post reply discipline (non-negotiable):** for 60 minutes after publishing, reply substantively to **every** comment. Each author-reply is a 150x event. Never batch this later — the window has closed.

## 4.2 Repeatable content templates

Weekly mix target: **40% technical / educational · 25% build-in-public · 15% contrarian · 10% curation · 10% conversational**.

### A. Case Study / Post-mortem — *credibility engine*
```
[Specific result with a number] in [timeframe].
Here's the full breakdown — including what didn't work:

The setup: [1 line]
What I expected: [1 line]
What actually happened: [number]
The one variable that mattered: [specific]
What I'd do differently: [specific]

Cost me [time/money] to learn. What's your version of this?
```

### B. Curation / Resource Drop — *bookmark engine*
```
[N] [tools/repos/papers] I actually use for [specific job].
No affiliates, no sponsors:

1. [Name] — [what it does] → [why it beats the obvious alternative]
2. [Name] — [what it does] → [why]
...

Bookmark it. What's missing from this list?
```

### C. Contrarian Opinion — *reply engine*
```
Unpopular take: [specific, falsifiable claim].

Everyone repeats [conventional wisdom].
What actually happens: [mechanism].
Evidence: [number or concrete case].

The exception: [where the conventional view IS right].

Where am I wrong?
```
> Guardrail: contrarian about **ideas, methods and incentives**. Never about people, groups, or identity. The last line ("where am I wrong") is not optional — it converts disagreement into replies instead of blocks.

### D. Build-in-Public Metrics — *retention engine*
```
Week [N] of building [thing] solo.

Shipped: [specific feature]
Numbers: [MRR / users / installs — real, or say "not sharing yet"]
Broke: [the thing that broke]
Learned: [one non-obvious lesson]
Next: [one specific thing]

[screenshot]

Anyone else fighting [specific problem] right now?
```
> Lead with **lessons**, not just numbers. Revenue screenshots earn likes; mechanisms earn follows.

### E. Technical Breakdown — *authority engine*
```
[System/tool] explained in [N] steps — the version I wish I'd read first:

1. [Step] — [what actually happens under the hood]
2. [Step] — [the part everyone gets wrong]
3. [Step] — [the tradeoff nobody mentions]

The counterintuitive bit: [insight].

[diagram]

Bookmark this. Which step do you want expanded?
```

### F. Teardown / Before-After
```
I rewrote [thing]. Same content, [N]x the result.

Before: [screenshot / quote]
After: [screenshot / quote]

The 3 changes:
→ [change] — [why it worked]
→ [change] — [why]
→ [change] — [why]

Which version would you have clicked?
```

### G. Question / Poll — *cheap conversation seeder*
```
Serious question for [specific audience]:

[Binary or forced-choice question with real stakes]

I'll go first: [your answer + 1-line reason].
```
> Max 1–2 per week. Overuse reads as engagement farming.

## 4.3 The compounding loop

```
Reply on 30-50 in-cluster accounts (borrowed reach)
        → profile clicks (12x)
        → follows
        → larger in-network test slice for your originals
        → faster 0-30min velocity
        → out-of-network expansion via Phoenix/SimClusters
        → more in-cluster accounts notice you
        → replies rank higher, quote-tweets appear
        → repeat
```

**Weekly operating rhythm:**

| Block | Duration | Actions |
|---|---|---|
| Morning | ~25 min | Warm-up: 5–10 replies in-niche → publish primary post (highest-effort format) |
| Post+60 min | ongoing | Reply to every comment. Non-negotiable. |
| Midday | ~15 min | 10–15 sniper replies on the watchlist |
| Afternoon | ~10 min | Second post (lighter format: single tweet, question, quick teardown) |
| Evening | ~15 min | Clear remaining comments + 5–10 more replies |
| Sunday | ~45 min | Weekly recap thread + batch-draft next week + prune/refresh watchlist |

**Ratios to hold:** 3–4 originals/day max · 20–40 replies/day · 1 thread or long-form per week minimum · 1 native video per week minimum · ≥90 min between originals.

**Metrics that matter, in order:** bookmarks per post → replies per post (and *your* reply rate) → profile clicks → follows per 1k impressions → reposts. **Impressions and likes are diagnostics, never targets.**

---

# 5. AGENT OPERATIONAL DIRECTIVES

## 5.1 Pre-publication checklist — ALL must pass

```
□  HOOK
   □ Line 1 works as a standalone post, out of context
   □ Contains a specific number, named thing, or falsifiable claim
   □ No wind-up sentence before the point
   □ Does not open with a hashtag, emoji, or "Thread 🧵"

□  SUBSTANCE
   □ One idea, nameable in ≤5 words
   □ Every claim is either sourced, personally observed, or explicitly framed as an estimate
   □ ZERO invented statistics
   □ At least one concrete artifact: number, tool name, code, screenshot, price, timeframe

□  LINKS
   □ Zero external links in the primary post
   □ Any link is queued for the first self-reply
   □ If in-body is unavoidable: ≥150 words of original substance + native media
   □ No URL shorteners

□  STYLE FILTER
   □ 1-2 lines per paragraph; blank line between beats
   □ Average sentence <12 words; active verbs
   □ ≤1 emoji (0 preferred); no emoji bullet lists
   □ 0 hashtags (max 1 only if genuinely native to the niche, never in line 1)
   □ Zero phrases from the §3.4 banned list
   □ Read aloud: does a human practitioner say this? If no → rewrite

□  CONVERSATION TRIGGER
   □ Ends with a specific answerable question, a falsifiable claim, or an open loop
   □ NOT "thoughts?", NOT "let me know below", NOT "like if you agree"
   □ Agent has a substantive first-reply already drafted for the top-3 likely responses

□  BOOKMARK VALUE
   □ Would a competent stranger save this for later use?
   □ If it's a list/framework/playbook: is there a recap block?
   □ If no bookmark value AND no conversation value → DO NOT PUBLISH

□  MEDIA
   □ Threads: media every 3-4 tweets
   □ Video: hook in first 1.5s, captions burned in, shortest version that lands
   □ Images legible at mobile thumbnail size; one idea per image

□  SAFETY / REPUTATION
   □ No engagement bait, no follow-for-follow, no manufactured outrage
   □ No attacks on people, groups, or identity
   □ No unrequested mass-tagging
   □ Not a near-duplicate of anything posted in the last 30 days
   □ Would this earn a block, mute, or "not interested"? If plausibly yes → rewrite

□  TIMING & CADENCE
   □ ≤4 originals today; ≥90 min since the last original
   □ Publishing inside an audience-active window
   □ Agent is available to reply for the next 60 minutes
   □ Content is fresh — nothing ships targeting a >48h-old news cycle
```

## 5.2 Hard constraints (never override)

1. **Never fabricate data, metrics, quotes, or outcomes.** If the source is unavailable, drop the number.
2. **Never publish without an available 60-minute reply window.**
3. **Never exceed 4 original posts per day.**
4. **Never put a bare external link in a primary post.**
5. **Never use engagement bait, rage bait, or identity-based provocation.**
6. **Never use emoji bullet lists or 2021-era clickbait templates.**
7. **Never post outside the account's declared niche/SimCluster** without an explicit human instruction.
8. **Never repost near-duplicate content within 30 days.**
9. **Never reply with generic praise.** Value-add or stay silent.
10. **Never optimize for likes or impressions.** Optimize for bookmarks, replies-you-reply-to, and profile clicks.
11. **Never claim certainty about algorithm internals** in published content. Distinguish `[CODE]` from `[FIELD]`/`[HEURISTIC]` if the topic comes up publicly.
12. **Escalate to the human operator** before: announcements, pricing, partnerships, apologies, anything legal/medical/financial, or engaging with an active controversy.

## 5.3 Decision tree — format selection

```
Is the idea enumerable (N discrete items)?
├─ YES → 5-10 items? → THREAD, list template
│         └─ 3-4 items? → SINGLE TWEET with → bullets
└─ NO → Is the argument continuous and >280 chars?
         ├─ YES + Premium → LONG-FORM POST (1,000-4,000 chars)
         ├─ YES, no Premium → THREAD, narrative template
         └─ NO → SINGLE TWEET (Hook → Meat → Open Loop)

Do I have a screenshot, chart, or clip?  → ALWAYS attach it.
Is it a weekly progress report?          → BUILD-IN-PUBLIC template + screenshot.
Is it a disagreement with consensus?     → CONTRARIAN template + "where am I wrong?"
Is it purely reactive to someone else?   → QUOTE-TWEET or REPLY, not an original post.
```

## 5.4 Self-audit loop (weekly)

1. Rank last week's posts by **bookmarks**, then by **replies-you-replied-to**, then by **profile clicks**. Ignore likes.
2. For the top 2: name the exact structural reason it worked (hook type, format, media, question). Add it to the template rotation.
3. For the bottom 2: diagnose against the §5.1 checklist — which box actually failed?
4. Check the negative-signal trend. Any spike in mutes/blocks/"not interested" → immediately dial down provocation for 30 days; the penalty carries at the account level.
5. Prune the reply watchlist: drop accounts that never reply back, add 3–5 new in-cluster accounts.
6. Confirm SimCluster hygiene: were ≥80% of the week's replies inside the target cluster?

---

## APPENDIX — Source register

| Source | Type |
|---|---|
| `github.com/twitter/the-algorithm` (Scala, Mar 2023) — Earlybird, SimClusters, UTEG/GraphJet, tweepcred | `[CODE]` |
| `github.com/twitter/the-algorithm-ml` — `projects/home/recap` Heavy Ranker README (weight constants, MaskNet) | `[CODE]` |
| `github.com/xai-org/x-algorithm` — home-mixer, thunder, phoenix, simclusters, visibility-filtering, grox, agatha, user-cred-v2; Aug 13–14 2026 release notes incl. the official weights-scale-probabilities clarification | `[CODE]` |
| Buffer — 18.8M posts / 71k accounts on Premium reach; link-format performance collapse | `[FIELD]` |
| Knight Columbia, Sprout Social, Social Media Today, Publora, Postory, OpenTweet, Teract, Glitchwire — weight ladders, filter behavior, velocity windows, format benchmarks | `[FIELD]` |
| Practitioner consensus (builder/creator X, reply-strategy operators) | `[HEURISTIC]` |

**Freshness policy:** weights and filters change without notice. Re-verify §1 against `xai-org/x-algorithm` release notes quarterly. Everything in §2–§5 is downstream of §1 and should be re-derived if the weight ladder or filter set changes.
