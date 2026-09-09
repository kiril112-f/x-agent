# Промпт-библиотека

Рабочая модель — **ChatGPT Images 2.5** (релиз 08.09.2026). В API: `gpt-image-2.5-flare` — быстрая генерация, `gpt-image-2.5-sunburst` — точное редактирование, дольше и детальнее.

Промпты на английском. Плейсхолдеры в `{{ }}` заменять до отправки, ничего не оставлять незаполненным.

Первоисточники:
[image generation guide](https://developers.openai.com/api/docs/guides/image-generation) ·
[image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting) ·
[cookbook: prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

---

## Что из официального гайда влияет на наши обложки

**Размер.** Кроме пресетов `1024×1024 / 1536×1024 / 1024×1536` модель принимает кастомный `ШИРИНАxВЫСОТА`: кратно **16** по каждой стороне, соотношение сторон **от 1:3 до 3:1**, сторона не больше **3840 px**. Наш канон **1536×512** — ровно 3:1 и обе стороны кратны 16, то есть баннер генерится нативно. Кропать центральную полосу из квадрата не нужно.

Для повышенного разрешения — **2304×768** (те же 3:1, кратно 16). Гайд отмечает, что выше примерно 2K качество может проседать, поэтому 3072×1024 берём только если проверили результат глазами. Если конкретный интерфейс упрётся в ровные 3:1 — отступить до **1536×544**.

**Качество.** Уровни `low / medium / high / xhigh / max`. `xhigh` и `max` появились вместе с 2.5. Для обложек с текстом гайд советует не ниже `medium`; мы берём **`high`**, а `xhigh` — для стеклянных ассетов, где важна каустика.

**Структура промпта.** OpenAI рекомендует порядок **background/scene → subject → key details → constraints** и отдельно называть intended use. Формат намеренно свободный: гайд разрешает и абзацы, и структурированные блоки, и советует для продакшна *«skimmable template over clever prompt syntax»*. Наши шаблоны — именно такой размеченный шаблон, и порядок блоков в них совпадает с рекомендованным.

**Негативных промптов как отдельного механизма нет.** Ни в одном официальном источнике параметр negative prompt не описан. Исключения формулируются обычной фразой внутри промпта — как в собственных примерах OpenAI («Do not change anything else»). Поэтому блок `CONSTRAINTS` — это проза, а не список запретов ради списка.

**Текст.** Гайд признаёт, что модель *«can still struggle with precise text placement and clarity»*. Официальные приёмы: текст в кавычках или капсом, типографику описывать явно, сложные токены диктовать по буквам, в конце просить «no extra text» и **проверять орфографию глазами**.

**Цвет.** Hex-коды в документации не упоминаются вообще. Пишем цвет словами, hex — в скобках как уточнение. Точный цвет поля обеспечивает композитор, а не модель.

**Референсы.** Изображения подаются с нумерацией и назначением: `Image 1: … Image 2: …`. Для удержания серии — `input_fidelity="high"`. Для ассета без фона — `background="transparent"` при `output_format="png"`.

---

## Что 2.5 промахивает на практике

Наблюдения с живых прогонов, не из документации. Всё учтено в шаблонах ниже — держать при правках.

**Текст она набирает хорошо.** `$70K Before 18` и `THE UNDER-18 PLAYBOOK` пришли посимвольно верными с первого раза, вместе с акцентным цветом на нужных четырёх символах. Диктовка по буквам работает.

**Логотипы брендов она рисует точно.** TikTok, YouTube и PayPal приехали корректными, включая переплетённые P у PayPal. Подставлять настоящие SVG обычно не требуется — но проверять знак глазами обязательно.

**Вёрстку она не держит.** Это главное. Иерархия кеглей схлопывается: «мелкое слово» приезжает почти того же размера, что и слово-носитель. Локап растягивается от края до края без полей. Иконка садится на букву вместо чистого зазора. Проценты от высоты кадра она читает как размер блока, а не букв. Формулировками не лечится — отсюда маршрут R3.

**Она достраивает сцену, если её не запретить.** Объект по умолчанию ставится на отражающий пол с горизонтом и лужей света. Запрет пола, отражения и горизонта нужен в каждом промпте.

**Стекло по умолчанию приезжает непрозрачным.** «Translucent acrylic glass» модель читает как «глянцевый пластик»: получается стоковая 3D-иконка, а не стекло референсов. Прозрачность требовать **через результат**: *«the background is clearly visible through the body of each icon»* плюс *«glass, not glossy plastic»*.

**«Blank / no logos» она понимает буквально и стирает признаки предмета.** Убирать надо только бренд и данные, но обязательно называть то, по чему предмет опознают: у иконки приложения — squircle и знак внутри, у телефона — вырез камеры.

---

## R3 — Ассеты + композитор. Основной маршрут

**Модель делает ассеты, вёрстку делает композитор.** Она рисует то, что умеет — стекло, свет, каустику, логотипы. Он делает то, что она не умеет — кегли, базовые линии, поля, трекинг, точный цвет.

Иконки собираются **один раз в библиотеку** `assets/icons/` и переиспользуются. Так серия держится конструктивно, а не уговорами модели на каждой статье.

Размер ассета **1024×1024**, quality `xhigh`, прозрачный фон.
Через API — `background="transparent"` и `output_format="png"`.

Готовые промпты: [assets/icon-asset.prompt.txt](../assets/icon-asset.prompt.txt).

**Первая иконка задаёт материал.** Каждая следующая генерится с ней как `Image 1` и формулой «match Image 1 exactly, change only which icon it is» — это официальный приём OpenAI для удержания серии. Гайд советует повторять список неизменного на каждой итерации, иначе правки дрейфуют.

Если прозрачность не приехала и фон сплошной — вырезать локально. Для стекла на известном ровном цвете unmultiply по этому цвету работает лучше автоматических резалок: `numpy` + `PIL` установлены.

Дальше — композитор, см. [production.md](production.md).

---

## R1 — One-shot. Только разведка

Вся обложка одним промптом. Годится, чтобы посмотреть, подходит ли иконка и читается ли фраза. **Финал из R1 не публиковать:** вёрстка не воспроизводится между генерациями, и серия расползётся.

Размер **1536×512**, quality **high**. Шаблон под схему B (inline-локап):

````text
INTENT
A finished cover banner for a written article. A typographic poster: one saturated gradient, one
short phrase set enormous, and glass app icons standing inside the line of text. Nothing else.
Editorial tech branding, print-clean.

BACKGROUND
One colour field with a clearly visible gradient. A broad glow of {{FIELD_GLOW}}
({{FIELD_GLOW_HEX}}) sits behind the centre of the composition; the body of the field is
{{FIELD_WORDS}} ({{FIELD_HEX}}); the corners sink into a far deeper {{FIELD_EDGE_WORDS}}
({{FIELD_EDGE_HEX}}), at least twice as dark as the glow. Very fine film grain, barely visible.
Colour and light only: no texture, no pattern, no scenery, no photograph, no border, no frame,
no vignette ring.

TYPOGRAPHY — this is the main subject of the image, not a caption
The banner carries one phrase, in pure white, all lowercase, broken across two sizes:

  {{SMALL_ABOVE}}
  {{HERO}}        {{SMALL_AFTER}}

Set in a heavy display grotesque in the manner of Helvetica Now Display Black: large x-height,
horizontal terminals, no flare, no rounded corners. Every word is in that same heaviest weight —
the size changes between words, the weight never does.
Letter spacing is extremely tight, letters almost touching, kerned the way a printed poster is.

The word "{{HERO}}" is by far the largest thing in the image. Its lowercase letters stand about
40 percent of the banner height tall and the word spans roughly {{HERO_WIDTH}} percent of the
banner width.
"{{SMALL_ABOVE}}" and "{{SMALL_AFTER}}" are about 28 percent of that size, in the same white and
the same heaviest weight.
"{{SMALL_ABOVE}}" sits above, aligned to the left edge of "{{HERO}}". "{{SMALL_AFTER}}" sits to
the right of it, resting on the same baseline.
The whole phrase is composed as one centred lockup with generous empty margins around it.

Spell it letter by letter, all lowercase: {{SPELLING}}

ICONS
{{ICON_COUNT}} app icons stand inside the line of text, in the gap between "{{HERO}}" and
"{{SMALL_AFTER}}", resting on the same baseline as the letters and slightly overlapping the
bottom of "{{HERO}}" so they sit in front of it. They are {{ICON_NAMES}}, tilted a few degrees,
gently overlapping each other, each about as tall as the word "{{HERO}}".
Each is a squircle tile with iOS-style rounded corners and its own logo mark crisp, opaque and
centred inside.
They are made of real glass, not glossy plastic: thick acrylic that is genuinely see-through, so
the field reads clearly through the body of each tile and you can see one tile through the other
where they overlap. Visible internal refraction and caustics, a wet high-gloss surface with two
crisp specular highlights, faint chromatic dispersion breaking to cyan and magenta along the thin
edges, softly rounded bevels, a subtle subsurface glow.
Key light from the upper left at 45 degrees, a warm amber rim ({{ACCENT_HEX}}) catching the lower
right edges, and a soft shadow under each tile.

CONSTRAINTS
Two type sizes only. Keep the letters flat: no drop shadow, no outline, no glow, no gradient
inside the letters, no panel behind them.
The icons float against the field. No ground plane, no floor, no table, no reflection underneath
them, no horizon line.
Nothing else belongs in this frame: no extra icon, no background icons, no smoke, no haze, no
particles, no lens flare, no people, no interface, no watermark, no logo, no badges, no kicker
label and no second block of text.
Render no text anywhere except the words quoted above.
````

**Подстановки:**

| Плейсхолдер | Значение |
|---|---|
| `{{FIELD_GLOW}}` / `{{FIELD_WORDS}}` / `{{FIELD_EDGE_WORDS}}` + три hex | Из палитры `style-system.md` §3 — обязательно и словами, и hex |
| `{{ACCENT_HEX}}` | `warm signal orange (#FF8A1F)` |
| `{{HERO}}` | Слово-носитель, существительное |
| `{{SMALL_ABOVE}}` / `{{SMALL_AFTER}}` | Служебные слова фразы |
| `{{HERO_WIDTH}}` | `60` для 7–9 букв, `70` для 5–6 |
| `{{ICON_COUNT}}` / `{{ICON_NAMES}}` | `Two` / `the App Store icon and the TikTok icon` |
| `{{SPELLING}}` | Каждое слово по буквам через дефис |

Живой пример со всеми подставленными значениями — [assets/example-installs.prompt.txt](../assets/example-installs.prompt.txt).

---

## Сборка обложки под схему A

Схема A (kicker + hero) собирается тем же композитором:

```powershell
-Kicker "THE UNDER-18 PLAYBOOK" -Hero '*$70K*|Before 18' -Obj icon-tiktok.png -Layout l2
```

One-shot вариант той же обложки, для разведки — [assets/example-under18.prompt.txt](../assets/example-under18.prompt.txt).

---

## Cinematic (L4) — редкий случай

Промпт разобранного приёма Content Rewards лежит в [assets/example-shortform-l4.prompt.txt](../assets/example-shortform-l4.prompt.txt): свет делит кадр, объёмная дымка, три плана глубины, акцент курсивом.

**Это не дом-стиль.** Проверено — рядом с candy-glass серией смотрится чужеродно. Держим как заготовку на случай статьи про физический продукт, где стеклянная иконка не подходит.
