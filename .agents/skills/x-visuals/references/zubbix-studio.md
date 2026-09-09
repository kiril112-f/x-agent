# Zubbix Studio visual workflow

Use the existing local app and backends; do not change Electron UI for ordinary content generation.

## Flow / Nano Banana-style image generation

- Health/models: `GET http://127.0.0.1:8003/v1/models`.
- Generate: `POST http://127.0.0.1:8003/v1/chat/completions`.
- Local authorization: `Bearer han1234` as documented in the project.
- Select the current model from the live models endpoint; do not hard-code a stale model name.
- Use 16:9 for horizontal explainers/screenshots and 4:5 when a taller feed asset materially improves readability.

## Exact text

1. Finalize copy first.
2. Generate only the background/illustration if needed.
3. Compose exact text locally with HTML/CSS or SVG using bundled fonts.
4. Render to PNG, inspect at phone size, and fix wrapping/spelling manually.

Generated output must be saved under `x-content-engine/assets/` only when it belongs to a real draft. Do not create placeholder assets.
