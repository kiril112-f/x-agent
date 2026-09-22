import React from "react";
import {
  AbsoluteFill,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { loadFont } from "@remotion/fonts";
import sections from "./prompt.json";

loadFont({
  family: "JetBrains",
  url: staticFile("fonts/mono-regular.woff2"),
  weight: "400",
});
loadFont({
  family: "JetBrains",
  url: staticFile("fonts/mono-medium.woff2"),
  weight: "500",
});

export const FPS = 60;
export const FRAMES = 32 * FPS;
const LINE = 47;
const MINT = "#b5f5d5";
const DIM = "#697570";
type Row = { text: string; kind: "title" | "body" | "blank"; section: number };
const wrap = (text: string, limit = 46) => {
  const lines: string[] = [];
  let line = "";
  for (const word of text.split(" ")) {
    if (line.length + word.length + 1 > limit) {
      lines.push(line);
      line = word;
    } else line = line ? `${line} ${word}` : word;
  }
  if (line) lines.push(line);
  return lines;
};
const rows: Row[] = [];
sections.forEach((section, index) => {
  rows.push({
    text: `${String(index + 1).padStart(2, "0")}  ${section.title}`,
    kind: "title",
    section: index,
  });
  rows.push({ text: "", kind: "blank", section: index });
  section.paragraphs.forEach((paragraph) => {
    wrap(paragraph).forEach((text) =>
      rows.push({ text, kind: "body", section: index }),
    );
    rows.push({ text: "", kind: "blank", section: index });
  });
  rows.push({ text: "", kind: "blank", section: index });
});
const CYCLE = rows.length * LINE;
const highlights =
  /(TypeScript|Three\.js|x2|x3|60 fps|spatial hash|object pooling|instanced meshes|README)/g;
function Syntax({ text }: { text: string }) {
  return (
    <>
      {text.split(highlights).map((part, i) => (
        <span key={i} style={{ color: i % 2 ? MINT : undefined }}>
          {part}
        </span>
      ))}
    </>
  );
}

export const Terminal: React.FC = () => {
  const frame = useCurrentFrame() % FRAMES;
  // One document height per cycle. Frame 1920 is identical to frame 0.
  const scroll = interpolate(frame, [0, FRAMES], [0, CYCLE]);
  const firstVisible = Math.ceil(scroll / LINE) % rows.length;
  const activeSection = rows[firstVisible].section;
  const breathe = 0.65 + 0.35 * Math.cos((2 * Math.PI * frame) / 240);
  return (
    <AbsoluteFill
      style={{
        background: "#080b0a",
        fontFamily: "JetBrains, monospace",
        color: "#d7deda",
        WebkitFontSmoothing: "antialiased",
      }}
    >
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 5%, #1d332a 0%, #101814 33%, #080b0a 68%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 43,
          top: 64,
          width: 994,
          height: 1792,
          borderRadius: 27,
          overflow: "hidden",
          border: "1px solid #3a443e",
          background: "#101412",
          boxShadow: "0 35px 90px #0009, 0 1px 0 #ffffff10 inset",
        }}
      >
        <div
          style={{
            height: 83,
            display: "flex",
            alignItems: "center",
            padding: "0 29px",
            borderBottom: "1px solid #2a332d",
            background: "#1a211d",
            position: "relative",
          }}
        >
          <div style={{ display: "flex", gap: 12 }}>
            {["#ef837b", "#eac174", "#8bbd92"].map((color) => (
              <div
                key={color}
                style={{
                  width: 15,
                  height: 15,
                  borderRadius: "50%",
                  background: color,
                }}
              />
            ))}
          </div>
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              textAlign: "center",
              fontSize: 22,
              color: "#a1ada5",
              letterSpacing: 0.2,
            }}
          >
            ~/projects/mob-control
          </div>
          <div style={{ marginLeft: "auto", fontSize: 21, color: "#637168" }}>
            zsh
          </div>
        </div>
        <div
          style={{
            height: 280,
            margin: "0 36px",
            borderBottom: "1px solid #303b33",
            paddingTop: 34,
            boxSizing: "border-box",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 15,
              fontSize: 26,
              marginBottom: 29,
            }}
          >
            <span style={{ color: MINT, fontSize: 32 }}>›_</span>
            <span style={{ fontWeight: 500, color: "#f1f3ef" }}>
              OpenAI Codex
            </span>
            <span
              style={{
                marginLeft: "auto",
                color: "#a1aea5",
                fontSize: 18,
                border: "1px solid #39463d",
                borderRadius: 6,
                padding: "7px 11px",
                letterSpacing: 1.2,
              }}
            >
              PROMPT PREVIEW
            </span>
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              fontSize: 29,
              marginBottom: 16,
            }}
          >
            <span style={{ color: DIM, width: 184 }}>model</span>
            <span style={{ color: MINT, fontWeight: 500 }}>ChatGPT-6 Sol</span>
            <span
              style={{
                color: "#e5e9df",
                fontSize: 21,
                marginLeft: 24,
                padding: "5px 13px",
                background: "#2a352b",
                border: "1px solid #42523f",
                borderRadius: 6,
              }}
            >
              ultra
            </span>
          </div>
          <div style={{ display: "flex", fontSize: 24, marginBottom: 24 }}>
            <span style={{ color: DIM, width: 184 }}>directory</span>
            <span style={{ color: "#b1bcb4" }}>~/projects/mob-control</span>
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 14,
              fontSize: 23,
              color: "#89988d",
            }}
          >
            <span style={{ color: MINT }}>›</span> build a playable browser game
            <span
              style={{
                width: 11,
                height: 23,
                background: MINT,
                opacity: breathe,
              }}
            />
          </div>
        </div>
        <div
          style={{
            height: 99,
            display: "flex",
            alignItems: "center",
            padding: "0 36px",
            gap: 19,
          }}
        >
          <div
            style={{ width: 4, height: 33, borderRadius: 2, background: MINT }}
          />
          <div
            style={{
              color: "#f1f4ed",
              fontSize: 35,
              fontWeight: 500,
              letterSpacing: -1.2,
            }}
          >
            Mob Control
          </div>
          <div style={{ marginLeft: "auto", color: "#79877e", fontSize: 21 }}>
            BUILD SPEC / 09 SECTIONS
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            top: 462,
            left: 0,
            right: 0,
            bottom: 109,
            overflow: "hidden",
            maskImage:
              "linear-gradient(to bottom, transparent 0px, black 24px, black calc(100% - 66px), transparent 100%)",
          }}
        >
          <div style={{ transform: `translate3d(0, ${26 - scroll}px, 0)` }}>
            {[0, 1].map((copy) => (
              <div key={copy} style={{ height: CYCLE }}>
                {rows.map((row, index) => (
                  <div
                    key={index}
                    style={{
                      height: LINE,
                      display: "flex",
                      alignItems: "center",
                      whiteSpace: "pre",
                      fontSize: 29,
                      lineHeight: `${LINE}px`,
                      letterSpacing: -0.35,
                    }}
                  >
                    <span
                      style={{
                        flex: "0 0 87px",
                        textAlign: "right",
                        paddingRight: 22,
                        boxSizing: "border-box",
                        color: row.kind === "title" ? "#7caa90" : "#414d45",
                        fontSize: 19,
                      }}
                    >
                      {row.kind !== "blank"
                        ? String(index + 1).padStart(3, "0")
                        : ""}
                    </span>
                    <span
                      style={{
                        height: "100%",
                        borderLeft: "1px solid #28342c",
                        paddingLeft: 23,
                        flex: 1,
                        background:
                          row.kind === "title"
                            ? "linear-gradient(90deg,#233b2d99,transparent 90%)"
                            : "transparent",
                        color: row.kind === "title" ? MINT : "#ced5cf",
                        fontWeight: row.kind === "title" ? 500 : 400,
                        fontSize: row.kind === "title" ? 25 : 29,
                      }}
                    >
                      <Syntax text={row.text} />
                    </span>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: 108,
            borderTop: "1px solid #303b33",
            display: "flex",
            alignItems: "center",
            padding: "0 36px",
            background: "#141c16",
            boxSizing: "border-box",
          }}
        >
          <span style={{ color: MINT, fontSize: 25, marginRight: 14 }}>↳</span>
          <span style={{ fontSize: 20, color: "#b7c4bb", letterSpacing: 0.3 }}>
            {sections[activeSection].title.toLowerCase()}
          </span>
          <div
            style={{
              display: "flex",
              gap: 7,
              marginLeft: "auto",
              alignItems: "center",
            }}
          >
            {sections.map((section, index) => (
              <div
                key={section.title}
                style={{
                  width: index === activeSection ? 29 : 9,
                  height: 6,
                  borderRadius: 3,
                  background: index === activeSection ? MINT : "#35483b",
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
