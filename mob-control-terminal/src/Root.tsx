import "./index.css";
import { Composition } from "remotion";
import { Terminal, FPS, FRAMES } from "./Terminal";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MobControlTerminal"
        component={Terminal}
        defaultProps={{
          modelName: "ChatGPT-6 Sol",
          terminalName: "OpenAI Codex",
        }}
        durationInFrames={FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
      <Composition
        id="MobControlOpus"
        component={Terminal}
        defaultProps={{ modelName: "Claude Opus 5.5", terminalName: "Claude" }}
        durationInFrames={FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
