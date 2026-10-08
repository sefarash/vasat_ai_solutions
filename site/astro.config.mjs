import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";
import { readFileSync } from "node:fs";

// Business facts live in ../data/site.json; the canonical base URL is one of them.
const facts = JSON.parse(readFileSync(new URL("../data/site.json", import.meta.url), "utf-8"));

export default defineConfig({
  site: facts.business.url,
  trailingSlash: "never",
  build: { format: "file" },
  integrations: [tailwind({ applyBaseStyles: false }), icon()],
});
