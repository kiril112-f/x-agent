# X post formatting

Reference image: `x-content-engine/research/sources/paragraph-spacing-reference.png`.

Цель — сделать текст лёгким для сканирования на мобильном экране. Использовать настоящие переносы строк, а не визуальную стену текста.

## Core contract

- Один смысловой beat — один абзац.
- Между соседними абзацами — ровно одна пустая строка: два символа newline (`\n\n`).
- Обычный абзац чаще всего содержит 1–2 предложения. Это ориентир, а не механическая квота.
- Hook обычно стоит отдельным первым абзацем.
- Контекст, механизм, proof/example и conclusion/next step разделяются, когда выполняют разные функции.
- Короткий one-liner или одно простое предложение не нужно искусственно дробить.

## Line wrapping

- Не нажимать Enter в середине предложения только потому, что строка длинная на текущем экране.
- X сам переносит текст по ширине viewport.
- Ручной перенос нужен на semantic boundary, а не на фиксированной колонке.
- Не использовать leading spaces или tabs для создания «отступа»; в X они нестабильны и не заменяют blank line.

## Lists

- Перед списком и после него оставлять пустую строку, если рядом есть prose.
- Каждый пункт — с новой строки.
- Использовать один marker style внутри списка: `→`, `1.`, `-` или другой выбранный формат.
- Не вставлять пустую строку между каждым коротким list item, если элементы принадлежат одному списку.
- После списка новый semantic beat начинается через пустую строку.

Example:

```text
One creator. One app. One dedicated account.

Every post improves the next:
→ sharper hooks
→ objections from comments
→ formats worth repeating

The account becomes a distribution asset.
```

## By interaction type

### Single post / quote-post copy

- Hook, development and payoff get separate paragraphs when all three exist.
- Quoted source provides context, so do not repeat its entire setup; still use blank lines inside Kirill's added copy.

### Reply

- A one-sentence reply stays one paragraph.
- A substantive reply with claim + mechanism/example uses 2–3 short paragraphs with blank lines.
- Do not compress a valuable multi-part reply into one dense line.

### Thread

- Every tweet works independently.
- Inside each tweet, apply the same paragraph contract.
- Do not use line breaks as fake suspense across tweets.

### Article / long-form post

- Use short paragraphs, descriptive subheads where they help navigation, and whitespace between sections.
- Do not create a subhead for one tiny paragraph.
- Preserve the first two lines as a readable feed preview.

## Delivery and storage

- Return final copy with exact blank lines preserved; do not collapse it into inline prose.
- Do not wrap final copy in quotation marks.
- In Notion post page body, store final copy exactly as it should be pasted into X.
- When creating a plain-text artifact, use UTF-8 and preserve `\n\n` paragraph separators.

## QA failures

- A multi-beat post is returned as one wall-of-text paragraph.
- Paragraphs are separated by spaces or tabs instead of a blank line.
- Sentences are hard-wrapped at an arbitrary screen width.
- Different semantic functions are jammed into one dense paragraph.
- Blank lines disappear between draft, Notion storage and final handoff.
