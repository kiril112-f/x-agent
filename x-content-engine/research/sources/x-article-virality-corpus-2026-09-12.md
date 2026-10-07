# X Article virality corpus — 2026-09-12

**Исторический snapshot.** Актуальная проверка присланных ссылок — [исследование 2026-10-07](x-article-study-2026-10-07/analysis.md). Заголовки в таблицах ниже местами пересказаны; утверждения «18 из 18», «у всех», общие длины и причинные редакционные выводы не использовать как верифицированную базу новых правил. Новый разбор хранит точные source titles и различает наблюдения, гипотезы и house rules.

Источник: Apify actor `xquik/x-tweet-scraper` (id `wAusCMrm284Voaw86`), run `AD5zU4QJ0KgevhdDm`, dataset `Px7W9YElDyeKa0Tn2`.
Вход: `{ mode: "article", outputVariant: "rich", fieldStyle: "camelCase", outputPreset: "nested", articleTweetIds: [19 ids], maxItems: 40 }`.
Прочитано полное тело всех 19 статей через `article.bodyText` (offset 0–18). 18 референсов Кирилла + 1 его собственная статья.
Замечание по API: вложенный массив `article.contents` не выбирается через `fields`; брать `article.bodyText`.

Выводы живут в `.agents/skills/x-viral-article/references/viral-patterns.md`. Здесь — сырые данные.

## Когорта A — массовые

| Автор | Заголовок | Views | Likes | Followers | Скелет |
| --- | --- | --- | --- | --- | --- |
| thedankoe | How to fix your entire life in 1 day | 237.1M | 349k | 1.006M | lessons |
| Tim_Denning | I'm 38. If You're in Your 20's or 30's, Read This. | 25.8M | 34.3k | 145k | lessons |
| thedankoe | If you have multiple interests, do not waste the next 2-3 years | 17.7M | 40k | 1.006M | lessons |
| ErnestoSOFTWARE | I built 10 apps in 10 months and make $800,000/yr ( full guide ) | 7.24M | 12k | 60.9k | channel playbook |
| alexeixbt | Neuroplasticity: How Repetition Quietly Decides Who You Become | 6.65M | 8.9k | 77.5k | mechanism |
| sairahul1 | How To Build a One-Person Company Using Grok Bot | 5.5M | 4.7k | 144k | system build |
| PaulSolt | Install These Skills Before Codex Touches Your Xcode Project | 1.49M | 2.3k | 23.3k | tool pack |
| VibeMarketer_ | How to Build a Company Brain That Gets Smarter Every Week | 1.23M | 1.8k | 40.5k | system build |
| VibeMarketer_ | How to Build a One-Person Media Company With Hermes Bots | 811k | 3.7k | 40.5k | system build |

## Когорта B — ниша, высокий views-per-follower

| Автор | Заголовок | Views | Likes | Followers | V/F | Скелет |
| --- | --- | --- | --- | --- | --- | --- |
| EXM7777 | $2M video production pipeline | 406k | — | 142k | 3x | system build |
| lucaspatiri_ | ChatGPT Astra for UGC so well it feels illegal | 363k | — | 5.9k | 61x | system build |
| PerezHatesAI | AI UGC Slideshows +26.4M views/week Using GPT-6 | 360k | — | 1.4k | 257x | case autopsy |
| aleksascales | How to scale an app to six figures MRR with organic distribution | 336k | — | 1.0k | 332x | channel playbook |
| 0xfJuan | Why Some Startups Become 'Everywhere' Overnight | 284k | — | 8.7k | 33x | mechanism |
| wickedguro | Postiz crossed $2M ARR while everybody says SaaS is dead (Step-by-Step to replicate) | 205k | — | 18.3k | 11x | case autopsy |
| aureliuscajigas | How I scaled two apps to $240,000/yr with paid ads | 203k | — | 2.6k | 78x | channel playbook |
| leonabboud | How to become so good at marketing your competition thinks you're cheating | 185k | — | 27.3k | 7x | mechanism |
| adamtwtz | How this GLP-1 app generated 20m+ views | 107k | — | 1.9k | 55x | case autopsy |

## База сравнения — статья Кирилла

| Автор | Заголовок | Views | Likes | Replies | Followers |
| --- | --- | --- | --- | --- | --- |
| KirillMorozovop | I'm 16 and I've Made $70k Online. If You're Under 18, Read This. | 1,958 | 4 | 1 | 8 |

Разбор из 11 дефектов — в `.agents/skills/x-viral-article/references/rewriter-playbook.md`.

## Замеры по структуре

- Длина: когорта A 2,500–5,500 слов; когорта B 900–2,600 слов. adamtwtz — ~900 слов на 107k просмотров.
- Визуалы: 8–15 слотов на статью, все в роли доказательства (дашборды, скрины, схемы, чеки).
- Переиспользуемый объект: есть в 18 из 18 референсов (промпты, чек-листы, таблицы ставок, структура папок, shot card на 22 поля).
- Первый экран: результат/чек — 7 статей, зеркало читателя во втором лице — 7, признание/шрамы — 4. Разгона и фраз вида `in this article I will` — 0.
- Финал: одно действие + просьба сохранить — у всех в когорте B.
- Язык: американский английский B1–B2, презент, второе лицо, сокращения; в когорте B часто нативный лоуеркейс.

## Метод повторения замера

См. `.agents/skills/x-content-research/references/apify-xquik.md`, раздел `6. Article corpus mining`.
