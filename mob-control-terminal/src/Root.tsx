import "./index.css";
import { Composition } from "remotion";
import { Terminal, FPS, FRAMES } from "./Terminal";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MobControlTerminal"
        component={Terminal}
        durationInFrames={FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
