// Generated from the page plan: every page with index: true, nothing else.
import { business, plannedPages } from "../data/facts.js";

export const GET = () => {
  const base = business.url.replace(/\/$/, "");
  const urls = plannedPages
    .filter((p) => p.index)
    .map((p) => `  <url><loc>${base}${p.route === "/" ? "/" : p.route}</loc></url>`)
    .join("\n");
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
