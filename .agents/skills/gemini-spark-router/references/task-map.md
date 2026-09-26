# Карта задач — X Agent

Проверено 26–27 сентября 2026. A/А = оставить; B/Б = помощник; C/В = сравнительный пилот; G/Г = отдельный Google API; D/Д = недоступно/не подтверждено. Доступ Spark наблюдался после включения VPN пользователем; B/C не означают production-переключение. existing=false — предлагаемое расширение. Полные свойства и статус пилота: task-map.json.

| Задача | Модуль / функция | Решение | Основание |
|---|---|---|---|
| Сбор публичных источников | .agents/skills/x-content-research/SKILL.md · public X research workflow | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
| Исследование темы | .agents/skills/x-content-research/SKILL.md · Research steps 1–9 | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
| Исследование конкурентов | .agents/skills/x-content-research/SKILL.md · Notion routing / creator workflow | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
| Проверка фактов, цифр и цитат | x-content-engine/knowledge/proof-and-claims.md · External claims verification | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
| Формирование пакета источников | x-content-engine/knowledge/context-storytelling.md · Pre-draft context/resource pack | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
| Идеи и контентная стратегия | x-content-engine/knowledge/content-strategy.md · Pillars / creation model | Б — помощник | Подготовительная подборка свежих кейсов, не автоматический контент-план публикаций. |
| Редактура исходного черновика | .agents/skills/x-draft-to-post/SKILL.md · draft-to-post / no-fluff + voice | В — сравнительный пилот | Проверить качество редактуры независимо; победа Spark не предполагается. |
| Короткие посты | .agents/skills/x-draft-to-post/SKILL.md · x-draft-to-post | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Треды | .agents/skills/x-draft-to-post/SKILL.md · x-draft-to-post format selection | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Длинные статьи | .agents/skills/x-viral-article/SKILL.md · X Viral Article workflow | Б — помощник | Больше глубины исходных материалов; структуру и авторский голос сохраняет узкоспециализированный skill. |
| Соблюдение авторского голоса | .agents/skills/x-brand-voice/SKILL.md · Apply/update voice | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Финальная проверка текста | .agents/skills/x-draft-to-post/references/quality-gate.md · Hard failures / no-ai-slop | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Подготовка обложек | .agents/skills/x-article-cover/SKILL.md · X Article Cover route | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Графики | .agents/skills/x-article-chart/SKILL.md · Chart spec → render.ps1 | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Инфографика | .agents/skills/x-article-chart/SKILL.md · Five chart forms / illustrative curve | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Сохранение результатов в существующих Notion базах | x-content-engine/operations/notion-schema.md · Routing / Notion lifecycle | А — текущий путь | Существующие skills содержат проектный voice/quality/privacy; перенос без измерений повышает риск потери правил. |
| Анализ результатов опубликованного контента | x-content-engine/operations/algorithm-review-loop.md · After manual publication | Б — помощник | Второй аналитический взгляд возможен для серии; My Life это не заменяет, но постоянный Spark job не нужен. |
| Обновление знаний об алгоритме X | x-content-engine/operations/algorithm-review-loop.md · Check default branch+HEAD → compare SHA | В — сравнительный пилот | Многошаговый поиск первичных источников и противоречий потенциально экономит ручные переходы; измерить against x-content-research. |
