import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Fuentes autoalojadas en public/fonts (Inter / Inter Display, open source — SIL OFL)
const faces = [
  {
    family: "Inter Display",
    weight: "800",
    file: "InterDisplay-ExtraBold.otf",
  },
  { family: "Inter Display", weight: "700", file: "InterDisplay-Bold.otf" },
  { family: "Inter", weight: "600", file: "Inter-SemiBold.otf" },
  { family: "Inter", weight: "500", file: "Inter-Medium.otf" },
];

export const fontsReady = Promise.all(
  faces.map((f) =>
    loadFont({
      family: f.family,
      weight: f.weight,
      url: staticFile(`fonts/${f.file}`),
      format: "opentype",
    }),
  ),
);
