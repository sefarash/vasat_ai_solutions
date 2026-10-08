import { business } from "../data/facts.js";

export const GET = () =>
  new Response(`User-agent: *\nAllow: /\n\nSitemap: ${business.url.replace(/\/$/, "")}/sitemap.xml\n`, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
