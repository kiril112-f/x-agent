# X Content Engine

Система помогает Кириллу Морозову превращать собственные идеи и черновики в сильный English-language контент для X. Она исследует факты, улучшает структуру и язык, предлагает визуалы и со временем учится на принятых и отклонённых версиях. Она не заменяет автора и не публикует без подтверждения.

## Контекст

- `knowledge/creator-profile.md` — опыт, текущие проекты и интересы.
- `knowledge/audience-and-goals.md` — аудитория, цели и позиционирование.
- `knowledge/brand-voice.md` — рабочий voice profile и запреты.
- `knowledge/eps-content-playbook.md` — приоритетная content methodology из EP's X Signal, включая no-fluff compression.
- `knowledge/content-strategy.md` — темы, форматы и предварительный mix.
- `knowledge/x-algorithm-playbook.md` — проверенная механика X, редакционные выводы и короткая проверка distribution fit.
- `knowledge/privacy-and-approval.md` — личные границы и разрешения.
- `knowledge/proof-and-claims.md` — цифры, которые можно или нельзя использовать.
- `knowledge/reference-creators.md` — что изучать у референсов без копирования.
- `knowledge/questionnaire-60.md` — полный реестр ответов на исходные 60 вопросов с открытыми пунктами.
- `knowledge/voice-feedback.md` — датированный журнал явных правок Кирилла, влияющих на voice.
- `knowledge/context-storytelling.md` — pre-draft resource pack, attribution и честные storytelling structures.
- `knowledge/post-formatting.md` — обязательные paragraph breaks, whitespace и copy-safe output для X.
- `research/sources/x-article-virality-corpus-2026-09-12.md` — замеры и структура 19 статей (18 референсов двух когорт плюс своя неудачная статья), источник правил `$x-viral-article`.

## Рабочие процессы

- `operations/algorithm-review-loop.md` — перепроверка версии алгоритма и обучение на результатах ручных публикаций, без фонового мониторинга.

- `$x-draft-to-post` — черновик или тезис в готовый пост (короткий формат, треды, реплаи).
- `$x-viral-article` — X Article от идеи или рукописного черновика до готового длинного текста: виральные паттерны корпуса плюс brand voice, шесть скелетов, визуальный план и рерайт-пайплайн.
- `$x-content-research` — свежий ресерч и evidence ledger.
- `$x-brand-voice` — применение и обновление голоса.
- `$x-visuals` — решение о визуале и работа с Zubbix Studio.
- `$x-article-cover` — обложка X Article в фирменном стиле: поле, стеклянный объект, крупная типографика.
- `$x-article-chart` — график, статистика или инфографика внутри статьи: пять форм, фирменное поле, рендер в PNG.
- Статья всегда вызывает обложку и графики из себя: слот-карта в `.agents/skills/x-viral-article/references/visual-integration.md`.
- Публикация выполняется Кириллом вручную. Агент заканчивает работу готовым review-пакетом и записью в Notion.
- `$no-ai-slop` — финальная минимальная редактура без потери характера.

## Источники истины

1. Последняя явная инструкция пользователя.
2. Подтверждённые knowledge-файлы этого каталога.
3. Реальные принятые/опубликованные посты и правки пользователя.
4. Свежие первичные источники.
5. Эвристики и внешние playbooks только как гипотезы.

Notion — операционный источник истины для идей, статусов, финальных версий и аналитики. Локальные файлы содержат устойчивые правила и контекст, которые не должны зависеть от доступности Notion.

Точные IDs, properties и правила маршрутизации четырёх рабочих баз описаны в `operations/notion-schema.md`. Не создавать альтернативную content database.

<!-- gemini-spark-router:begin -->
## Выбор исследовательского исполнителя

Перед сменой AI-исполнителя, новой исследовательской задачей или автоматизацией используй [gemini-spark-router](../.agents/skills/gemini-spark-router/SKILL.md). Он сохраняет x-content-research, voice profile и все запреты публикации; Spark сейчас лишь будущий кандидат для сравнительного source brief.
<!-- gemini-spark-router:end -->
