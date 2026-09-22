# Mob Control terminal prompt loop

32-second portrait Remotion video: 1080 x 1920, 60 fps, silent H.264.

This is a designed prompt preview, not a recording of an executed model session. ChatGPT-6 Sol is the user-requested launch label. The composition does not assert an official release date or a successful game build.

## Preview

npm install
npm run dev

## Render

npx remotion render src/index.ts MobControlTerminal out/mob-control-terminal-32s.mp4 --codec=h264 --crf=16 --pixel-format=yuv420p

The duplicated document moves exactly one document height every 1,920 frames. All motion is frame-driven. The cursor pulse completes eight cycles per video.

Edit src/prompt.json to change the prompt. prompt.txt contains the same copyable prompt. Fonts are JetBrains Mono under the included OFL license.
