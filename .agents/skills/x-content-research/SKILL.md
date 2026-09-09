---
name: x-content-research
description: Исследует свежие X/news/product claims для будущего поста, предпочитает первичные источники и возвращает короткий evidence ledger. Использовать до написания claim-heavy, news, case-study или quote-post контента; не использовать для публикации.
---

# X Content Research

Исследуй только пробелы, которые меняют точность, угол или полезность поста. Не превращай каждый личный тезис в академический отчёт. Для публичных X-данных основной инструмент — Apify Actor `xquik/x-tweet-scraper` через `apify-x` MCP.

## Процесс

1. Сформулируй 1–3 проверяемых вопроса.
2. Выбери один workflow из [references/apify-xquik.md](references/apify-xquik.md) и поставь минимальный достаточный `maxItems`.
3. Следуй иерархии из [references/source-policy.md](references/source-policy.md).
4. Для каждой цифры, цитаты, даты, valuation и product claim найди источник-владельца вне X, когда X-автор не является первичным источником.
5. Отдели факт события от мнения автора X-поста.
6. Удали дубликаты и ранжируй кандидатов по relevance, engagement quality, freshness, evidence potential и fit с контентными pillars.
7. Зафиксируй противоречия и неопределённость вместо усреднения.
8. Собери pre-draft context/resource pack по `x-content-engine/knowledge/context-storytelling.md`: people/entities, resource map, counterpoint, original contribution и attribution plan.
9. Верни concise research brief и evidence ledger по [references/evidence-ledger.md](references/evidence-ledger.md).

Для research-based поста нужен минимум один реальный external anchor: original post, person, company, product, tool, repo, article, paper or dataset. Это требование относится к research context, но не заставляет вставлять ссылку или tag в primary post.

## Notion routing

Если пользователь просит сохранить результат или задача является частью постоянного content workflow, прочитай `x-content-engine/operations/notion-schema.md`. Используй только существующие четыре базы и точные data source IDs. Создавай отобранные competitors, reusable formats и idea cards; не выгружай raw Apify rows. Перед create проверяй duplicate по handle или source URL.

## Apify budget

Default: до 100 delivered rows на задачу. Для быстрого fact-check используй 5–20; для одного автора 20–50; для idea mining 50–100. Более 500 строк, followers/following collection или recurring scrape требует отдельного согласования. Actor тарифицирует только принятые строки; Apify platform usage может учитываться отдельно.

Не переключай токены для обхода лимита или биллинга. В проекте используется один основной аккаунт Apify.

X-пост подтверждает, что конкретный автор это сказал. Он не доказывает внешнюю статистику, если автор не является первичным источником.

После синтеза сохраняй в Notion только отобранные idea cards и ссылки. Полный raw dataset оставляй в Apify dataset, если он не нужен для отдельного анализа.
