# One-shot: $10M app idea → мой промпт

**Источник идеи:** @ideabrowser — "$10M app idea: Workouts for desk workers"
https://x.com/ideabrowser/status/2097393868043956531 (78,7 тыс. просмотров на 09.09.2026)

**Формат-референс:** @ErnestoSOFTWARE
https://x.com/ErnestoSOFTWARE/status/2093396854822052158

## Файлы
- `deskreps-prompt.png` — готовый скрин для поста (2560×3468)
- `deskreps-shot.html` — исходник скрина, правится и перегенерируется

Перегенерировать после правок:
```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --no-sandbox --hide-scrollbars --force-device-scale-factor=2 --window-size=1280,2600 --virtual-time-budget=4000 "--screenshot=C:\Users\User\Desktop\X Agent\raw.png" "file:///C:/Users/User/Desktop/X%20Agent/deskreps-shot.html"
```

## Механика формата (из разбора скринов Ernesto)
- Промпт-скрин в виде терминального окна macOS: traffic lights, вкладки, шапка с моделью, строка `> запрос`, полоса `1. THE PROMPT`, тело.
- Тело — секции капсом с двоеточием и буллеты под ними. Плотно, без пустот.
- Открывается одной строкой задачи: `Build me a native iOS app in SwiftUI called "X" — [что это]. Make it [3 качества].`
- Закрывается строкой приоритета: что важнее всего, чтобы модель не разменивалась.
- Есть секция «most important part» — она задаёт, куда модель вкладывает усилия.

---

## ПРОМПТ (то, что на скрине — копируемый текст в ответ под постом)

```
Build me a native iOS app in SwiftUI called "DeskReps" — a 3-minute workout app for people who sit at a desk all day. Make it calm, fast, and impossible to skip.

ONBOARDING (under 40 seconds):
- Ask 3 things only: hours seated per day, what hurts most (neck, lower back, wrists, hips, eyes), and where they work (open office, home, hybrid).
- Deliver the first session immediately — no account, no sign-in wall, no paywall.

HOME SCREEN:
- One large "Start a Break" button, with the next session already loaded under it: duration, target area, noise level.
- Above it, a Sitting Debt meter — a bar that fills the longer you sit and drains as you finish sessions.
- No streaks. A missed day lowers a number, it does not break a chain.

THE BREAK PLAYER (most important part):
- 3–5 minutes, 4–6 movements, all done at the desk. No floor, no equipment, no sweat.
- A low-poly 3D figure demonstrates each movement seated in or standing beside an office chair.
- Circular countdown ring around the figure, haptic pulse on every transition.
- One cue line per movement: what to do, and what it should feel like.

EXERCISE LIBRARY:
- Tag every movement: noise (silent / quiet / audible), visibility (invisible on a video call / subtle / obvious), equipment (none / chair / desk edge / wall), target area, sweat level 0–3.
- The session generator picks from those tags: pain areas + minutes available + noise limit + recent history. Never the same session twice in a row.

SMART SCHEDULING:
- With calendar access, find gaps of 5+ minutes between meetings and put the nudge there.
- Never fire during an event. Learn from dismissals and stop offering rejected time windows.
- Camera-On Safe mode: only movements tagged invisible on a video call, so a break can happen mid-meeting.

VISUALS:
- Light theme on warm off-white paper, charcoal text, one terracotta accent, sage only on completion. Dark theme in desaturated navy-charcoal.
- Slow, breath-paced motion. No confetti, no shouting typography, no red streak-loss alerts.

DATA:
- Store onboarding answers, pain weights that shift with feedback, session history with skipped movements, the Sitting Debt value, and notification response history.
- Works fully offline from a cached library. Write finished sessions to HealthKit.

EDGE CASES:
- A meeting runs over mid-session. A user returns after 14 days away. A user reports pain on a movement — suppress it and everything like it. Time zone changes. Calendar access revoked. Notifications disabled at the OS level.

FLOW:
- Open → one tap → moving in under 5 seconds. Fully usable start to finish on day one.

Prioritize how the break feels — calm pacing and movements someone will actually do at their desk in front of coworkers. That matters more than graphics.
```

---

## ТЕКСТ ТВИТА (quote-post оригинала @ideabrowser)

**Основной:**
```
$10M app idea from @ideabrowser.
This is the prompt I'd 1-shot it with — ChatGPT Astra, Ultra Mode:
```

**Альтернатива 1 — с реальной цифрой охвата:**
```
This app idea did 78K views on X in a day.
One prompt, ChatGPT Astra + Ultra Mode. Here it is:
```

**Альтернатива 2 — короче:**
```
Desk workers can't get to a gym. So build the gym into the desk.
One prompt. ChatGPT Astra, Ultra Mode:
```

**Альтернатива 3 — если one-shot уже проверен:**
```
$10M app idea from @ideabrowser, built in one prompt.
ChatGPT Astra + Ultra Mode. Exact prompt:
```

**CTA первым ответом под постом:**
```
Full copyable prompt below. Save it for your next build.
```
(и следом промпт текстом — на скрине он не копируется)

---

## Чек-лист перед публикацией
- [ ] Название модели в шапке скрина написано точно так, как в интерфейсе (строки `.l1` / `.l2` в HTML)
- [ ] Промпт на скрине читается с телефона
- [ ] Авторство идеи отмечено — @ideabrowser; промпт мой
- [ ] "1-shot" только если реально проверил. Не проверил — формулировка "the prompt I'd use"
- [ ] Копируемый промпт текстом в первом ответе
