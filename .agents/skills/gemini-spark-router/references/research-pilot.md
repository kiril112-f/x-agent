# X Agent: публичный исследовательский пилот

Это реальный локальный адаптер к работе **через пользовательский браузерный интерфейс**, а не Spark API. Сохраняет input hash, выбранный mode, task ID/URL, deadline, сырые outputs и review. Нет сети, внешних записей, фонового polling или расписания. Нужен Python3.10+; для команды и приёма результата нужен работающий ПК. Само уже запущенное облачное исследование не зависит от процесса адаптера; восстановление после закрытия вкладки проверено.

## Запуск из X Agent

```powershell
python .agents/skills/gemini-spark-router/scripts/research_pilot.py prepare --case .agents/skills/gemini-spark-router/references/pilot-case.json --out .agent-tools/research-pilots --mode google-spark-app
```

По умолчанию mode=existing. Для альтернативного режима приложения — google-deep-research-app; он не называется Spark. Возьми `job_dir` из ответа. В управляемом браузере выбери Spark (или отдельно Deep Research), передай только подготовленный публичный prompt. Не открывай новые connected apps, не добавляй личные файлы, расписания и действия записи. Если вход/доступ/квота недоступны, сохранить существующий путь. Один remote launch; повторный prepare не продлевает deadline и не запускает сервис.

После реального запуска сохрани **наблюдённые** URL и ID:

```powershell
python .agents/skills/gemini-spark-router/scripts/research_pilot.py register --job "<job_dir>" --url "https://gemini.google.com/spark/chat/<observed-hex>" --task-id "goal-c_<same-observed-hex>"
python .agents/skills/gemini-spark-router/scripts/research_pilot.py status --job "<job_dir>"
```

Для Deep Research используй действительный `/app/<hex>` без --task-id. Ссылка `/spark/tasks` допускается только вместе с наблюдённым task ID и может быть уточнена до matching chat URL без нового запуска. Не конструируй URL из предположения; сначала наблюдай его в UI.

После завершения сохрани ответ со ссылками в локальный Markdown и импортируй:

```powershell
python .agents/skills/gemini-spark-router/scripts/research_pilot.py import --job "<job_dir>" --result "<result.md>"
```

Это всегда `review_required`. Наличие трёх URL не доказывает достоверность: reviewer сверяет каждый факт/цитату с актуальным первичным источником. Reject для выдуманных гарантий, лишних прав, неверной поверхности/API, неподтверждённой цены. Лимит слов — предупреждение, исходник сохраняется неизменным. Для приемки review JSON должен иметь verdict=accept, reason и явные true: claims_supported, sources_primary, rules_preserved, format_usable, no_private_data, no_external_writes. `verdict=reject` также сохраняется. `review --job ... --review-file ...` никогда не публикует результат.

## Ошибки и возврат

Повторный import того же hash — no-op. Другой output не перезаписывает первый. Ошибки пустого/повреждённого ответа, URL, схемы, истёкшего deadline возвращают `{ok:false}`. Unknown outcome не порождает повторный облачный запуск. `status` читает сохранённый state после перезапуска; ОС освобождает блокировку при завершении процесса. Данные и результат облачного сервиса собираются после восстановления доступа по старой ссылке.

`cancel --job ...` отменяет **локальный** приём; если provider зарегистрирован, возвращается remote_stop_required=true. В браузере отдельно нажать Stop именно этого задания и проверить его состояние. Это не отменяет чужие задачи/расписания. Возврат к прежнему поведению: `--mode existing` для новой задачи; x-content-research и другие процессы не менялись.

Исходный сырой brief Spark и Deep Research не прошли gate замены. Ограниченный помощник должен возвращать source ledger с короткими проверяемыми цитатами, раздельными fact/inference/not-found, датой источника и новой/противоречащей ссылкой; без собственных обобщений и публикации. Любой первый ответ остаётся draft. Автоматических Notion writes нет, даже если обычный content workflow умеет сохранять карточки.

## Проверка адаптера

```powershell
python -B .agents/skills/gemini-spark-router/tests/test_research_pilot.py --report-prefix .agent-tools/research-pilot-tests
```

133 офлайн проверки прошли: input schema, URL, deduplication, expiry, conflicting import, review, три режима, process restart/locking и local cancellation. Это не эмуляция cloud quality, region, quota или schedule. Реально проверены отдельно две облачные задачи и повторное открытие результатов; cloud quota exhaustion и потеря аккаунта принудительно не создавались.

## Итог ограниченного пилота — 27 сентября 2026

**Оставить существующий x-content-research.** Spark и Deep Research app технически выполнили публичные задачи и восстановили результаты после закрытия вкладки. Однако сырой brief и единственная корректирующая проба source ledger не прошли проверку: у ledger настоящие цитаты, но два verdict противоречат заявленным claims; есть и нарушения формата. Автоматически выбирать облачный путь для обычного ресерча сейчас нельзя. Не повторять этот пилот на каждом запросе.

Адаптер сохранён как воспроизводимый сравнительный инструмент с default `existing`. Режимы `google-spark-app` / `google-deep-research-app` выбирать только при явном новом запросе на эксперимент либо существенном изменении модели, документации или требований задачи с заранее заданным бюджетом. Никаких автоматических публикаций, Notion writes или фонового сбора. Новых расписаний не создано.
