---
name: x-draft-to-post
description: Превращает сырой русский, английский или смешанный черновик Кирилла в исследованный, voice-matched English-пост для X. Использовать для draft-to-post, quote-post, thread или Article; не использовать для автономной публикации без approval.
---

# X Draft to Post

Сохраняй авторскую мысль и улучшай только то, что повышает ясность, доказательность, читабельность или силу подачи.

## Перед работой

Прочитай:

- `x-content-engine/knowledge/creator-profile.md`
- `x-content-engine/knowledge/brand-voice.md`
- `x-content-engine/knowledge/eps-content-playbook.md`
- `x-content-engine/knowledge/content-strategy.md`
- `x-content-engine/knowledge/privacy-and-approval.md`
- `x-content-engine/knowledge/proof-and-claims.md`
- `x-content-engine/knowledge/context-storytelling.md`
- `x-content-engine/knowledge/post-formatting.md`

Если задача опирается на новость, чужой пост, цифру или кейс, используй `$x-content-research` до финального текста.

## Обязательный процесс

1. Зафиксируй внутренне исходный тезис, цель и то, что нельзя потерять.
2. Подготовь context/resource pack. Для research-based поста используй `$x-content-research`; для личного поста зафиксируй real artifact/experience anchor или явно отметь, что внешний источник не нужен.
3. Отдели личные утверждения Кирилла от внешних claims. Не добавляй личный опыт, которого нет во входе или knowledge-файлах.
4. Выбери формат и самую короткую честную story spine по содержанию, а не по шаблону. Подробности — в [references/workflow.md](references/workflow.md).
5. Реши attribution: кого/resource назвать в primary copy, что оставить в source note, что предложить для first reply или quote-post.
6. Напиши честный hook, который обещает ровно тот payoff, который есть в теле.
7. Примени `$x-brand-voice`. Список выражений задаёт допустимый register, но для agent-generated draft по умолчанию не вставляй ни одной готовой фразы. Предпочитай свежий контекстный язык.
8. Проведи no-fluff compression pass из `eps-content-playbook.md`. Оставь claim, minimum proof, mechanism, strongest consequence/application и только необходимые voice/caveat lines. Удали повторы и secondary branches.
9. Проведи минимальную редактуру через `$no-ai-slop`. При конфликте проектный `brand-voice.md` выше общих запретов no-ai-slop.
10. Отформатируй exact final copy по `post-formatting.md`: semantic paragraphs, одна пустая строка между ними, list items по строкам, без arbitrary hard-wrap.
11. Для Article реши визуалы: обложка через `$x-article-cover`; каждая цифра, доля или динамика в теле — через `$x-article-chart`. Если ключевую цифру нельзя проследить до первичного источника или до `proof-and-claims.md`, график не собирается, а цифра снимается из текста.
12. Проверь результат по [references/quality-gate.md](references/quality-gate.md). Любой hard failure исправь до ответа.

## Контракт ответа

Сначала покажи готовый English-текст без длинного предисловия.

Сохрани exact paragraph breaks. Не превращай финальный copy в inline paragraph и не оборачивай его в кавычки.

Добавляй только полезные для конкретной задачи элементы:

- 1–2 альтернативных hooks, если выбор действительно неоднозначен;
- источники и короткий evidence note, если был ресерч;
- relevant people/resources и attribution note, если они materially shaped the post;
- first reply, если туда логично вынести ссылку или продолжение;
- visual direction, если визуал заметно усилит proof или понимание; для Article — список собранных графиков с путями к PNG и спекам;
- `BLOCKED — needs source/confirmation`, если ключевой claim нельзя честно подтвердить.

Не навязывай CTA, вопрос, thread или визуал. Не публикуй и не ставь в расписание из этого скилла.

## Notion lifecycle

Когда работа ведётся через постоянную базу, используй существующую `✍️ Посты · черновик → публикация` по `x-content-engine/operations/notion-schema.md`. Один post — одна карточка. Не создавай новую базу. Сохраняй research, raw draft, edited version и evidence в body; properties обновляй только по фактически закрытому этапу. Никогда не ставь `Опубликовано`: это делает пользователь после ручной публикации или агент по предоставленной им ссылке/метрикам.
