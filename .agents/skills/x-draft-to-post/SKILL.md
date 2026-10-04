---
name: x-draft-to-post
description: Превращает сырой русский, английский или смешанный черновик Кирилла в исследованный, voice-matched English-пост для X. Использовать для draft-to-post, quote-post, thread и любого короткого формата; для длинного X Article использовать $x-viral-article; не использовать для автономной публикации без approval.
---

# X Draft to Post

Сохраняй авторскую мысль и улучшай только то, что повышает ясность, доказательность, читабельность или силу подачи.

## Перед работой

Прочитай:

- `x-content-engine/knowledge/creator-profile.md`
- `x-content-engine/knowledge/brand-voice.md`
- `x-content-engine/knowledge/eps-content-playbook.md`
- `x-content-engine/knowledge/content-strategy.md`
- `x-content-engine/knowledge/x-algorithm-playbook.md`
- `x-content-engine/knowledge/privacy-and-approval.md`
- `x-content-engine/knowledge/proof-and-claims.md`
- `x-content-engine/knowledge/context-storytelling.md`
- `x-content-engine/knowledge/post-formatting.md`

Если задача опирается на новость, чужой пост, цифру или кейс, используй `$x-content-research` до финального текста.

## Обязательный процесс

1. Зафиксируй внутренне исходный тезис, цель и то, что нельзя потерять.
2. Подготовь context/resource pack. Для research-based поста используй `$x-content-research`; для личного поста зафиксируй real artifact/experience anchor или явно отметь, что внешний источник не нужен.
   Добавь короткую distribution hypothesis по `x-content-engine/operations/algorithm-review-loop.md`: конкретный читатель, payoff, evidence и одна естественная причина взаимодействия. Это внутренняя заметка, а не обязательный CTA.
3. Отдели личные утверждения Кирилла от внешних claims. Не добавляй личный опыт, которого нет во входе или knowledge-файлах.
4. Выбери формат и самую короткую честную story spine по содержанию, а не по шаблону. Подробности — в [references/workflow.md](references/workflow.md).
5. Примени правила референсов из `context-storytelling.md`: материал может быть любого формата и не задаёт формат результата. Не добавляй имя/@handle автора референса или рассказ о том, откуда взята идея. Ссылку оставь отдельно для ручного встраивания Кириллом; quote-post не выбирать автоматически.
6. Напиши честный hook, который обещает ровно тот payoff, который есть в теле.
7. Примени `$x-brand-voice`. Список выражений задаёт допустимый register, но для agent-generated draft по умолчанию не вставляй ни одной готовой фразы. Предпочитай свежий контекстный язык.
8. Проведи no-fluff compression pass из `eps-content-playbook.md`. Оставь claim, minimum proof, mechanism, strongest consequence/application и только необходимые voice/caveat lines. Удали повторы и secondary branches.
9. Проведи минимальную редактуру через `$no-ai-slop`. При конфликте проектный `brand-voice.md` выше общих запретов no-ai-slop.
10. Отформатируй exact final copy по `post-formatting.md`: semantic paragraphs, одна пустая строка между ними, list items по строкам, без arbitrary hard-wrap.
11. Если задача — длинный X Article, останови этот процесс и передай её в `$x-viral-article` вместе с собранным context/resource pack: заголовок, скелет, переиспользуемый объект и визуальный план живут там.
12. Для Article реши визуалы: обложка через `$x-article-cover`; каждая цифра, доля или динамика в теле — через `$x-article-chart`. Если ключевую цифру нельзя проследить до первичного источника или до `proof-and-claims.md`, график не собирается, а цифра снимается из текста.
13. Проверь результат по [references/quality-gate.md](references/quality-gate.md). Любой hard failure исправь до ответа. Для Article дополнительно действует `.agents/skills/x-viral-article/eval.md`.
   Пройди preflight из `x-algorithm-playbook.md`; не вычисляй выдуманный algorithm score и не растягивай текст ради dwell time.

## Контракт ответа

Сначала покажи готовый English-текст без длинного предисловия.

Сохрани exact paragraph breaks. Не превращай финальный copy в inline paragraph и не оборачивай его в кавычки.

Добавляй только полезные для конкретной задачи элементы:

- 1–2 альтернативных hooks, если выбор действительно неоднозначен;
- источники и короткий evidence note, если был ресерч;
- ссылка на референс отдельно от готового текста, если она предоставлена или найдена; без дополнительных упоминаний автора и attribution-предисловий;
- first reply, если туда логично вынести ссылку или продолжение;
- visual direction, если визуал заметно усилит proof или понимание; для Article — список собранных графиков с путями к PNG и спекам;
- `BLOCKED — needs source/confirmation`, если ключевой claim нельзя честно подтвердить.

Не навязывай CTA, вопрос, thread или визуал. Не публикуй и не ставь в расписание из этого скилла.

## Notion lifecycle

Когда работа ведётся через постоянную базу, используй существующую `✍️ Посты · черновик → публикация` по `x-content-engine/operations/notion-schema.md`. Один post — одна карточка. В body — исходный черновик, если есть, и актуальный чистовик; при необходимости только ссылки и готовые медиа. Не сохраняй research pack, отчёты о правках, открытые вопросы и пояснения агента. Properties заполняй кратко и только по фактически закрытому этапу. Никогда не ставь `Опубликовано`: это делает пользователь после ручной публикации или агент по предоставленной им ссылке/метрикам.
