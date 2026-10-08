import { readFileSync } from "node:fs";
import forms from "@tailwindcss/forms";

// Tokens are generated from the Stitch export: python3 tools/design_audit.py tokens --write
const tokens = JSON.parse(readFileSync(new URL("../design/tokens.json", import.meta.url), "utf-8"));

// The export names the Google Fonts families; the site self-hosts the variable versions.
const selfHosted = { Sora: "Sora Variable", Inter: "Inter Variable" };
const fontFamily = Object.fromEntries(
  Object.entries(tokens.fontFamily).map(([key, [first, ...rest]]) => [key, [selfHosted[first] ?? first, first, ...rest]]),
);

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,mjs,ts,md}"],
  theme: {
    extend: {
      colors: {
        ...tokens.colors,
        // Navy values the export typed straight into class names, promoted to tokens.
        navy: { 950: "#060e20", 900: "#081226", 850: "#091734", 800: "#0d1e44", card: "#0f2249", footer: "#071329", deep: "#050e1d" },
      },
      fontFamily,
      fontSize: tokens.fontSize,
      borderRadius: tokens.borderRadius,
      spacing: tokens.spacing,
    },
  },
  plugins: [forms],
};
