# What each row checks and how to fix it

| Row | Fails when | Fix |
|---|---|---|
| on-page: exactly one `<h1>` | a page has none or several (the count is shown) | The H1 comes from `data/pages.json`. Section headings are `<h2>`. A logo or hero badge must not be an `<h1>`. |
| on-page: title ≤ 60 | missing or too long (length shown) | Edit the entry in `data/pages.json`, then `python3 tools/page_plan.py validate`. |
| on-page: meta ≤ 155 | missing or too long | Same file. Say who it is for, what they get, the next step. |
| on-page: titles are unique | two routes share a title | Each page needs its own keyword; see `new-site-page`. |
| on-page: lang and viewport | `<html lang>` or the viewport meta is missing | The base layout sets both. |
| on-page: canonical | missing, relative, or pointing at another URL | The base layout emits `business.url` + the route, without a trailing slash except for `/`. SKIP means no base URL is known. |
| social: og tags (WARN) | `og:title`, `og:description` or `og:image` missing | Base layout; the image is a 1200×630 file made from the logo. |
| indexing: noindex where the plan says | a `landing` or `utility` page is indexable, or a normal page is noindex | Layout reads `index` from the plan. |
| indexing: sitemap | no sitemap, an indexable page missing from it, or a noindex page listed | The sitemap is generated at build from the plan, filtered to `index: true`. |
| indexing: robots.txt | no robots.txt or no `Sitemap:` line with a full URL | Generated at build with the base URL. |
| indexing: robots does not Disallow noindex | a noindex route is disallowed | Remove the Disallow; the crawler must reach the page to read `noindex`. |
| schema: valid JSON-LD | an indexable page has none, or it does not parse, or an item has no `@type` | Layout emits it from `data/site.json`. Service pages add `Service` and `FAQPage`. |
| schema: home organization | the home page has no Organization, ProfessionalService, LocalBusiness or MarketingAgency with `name` and `url` | Emit one from `data/site.json`. Only include `telephone` and `address` once they are real, not `TODO`. |
| links: internal links resolve | a link points at a route with no built file | Fix the link, or plan and build the page. |
| links: #anchors | `href="#x"` with no `id="x"` on the page | Add the id to the section or fix the link. |
| links: no `href="#"` | placeholder links carried over from the design | Give each a real target or remove it. |
| links: no orphan | an indexable page has no link from another page | Link it from two relevant pages. |
| links: no link to /lp/ | an organic page links to a landing page | Remove it; only ads point at landing pages. |
| content: ≥ 150 words | a thin page (count shown; nav, header and footer text is not counted) | Write the page, or make it noindex if it is a utility page. |
| media: alt | an `<img>` has no `alt` attribute | Describe the image; decorative images get `alt=""`. |
| ship: Tailwind CDN | `cdn.tailwindcss.com` is loaded | Compile Tailwind at build time. |
| ship: hot-linked Stitch image | an image, script or stylesheet comes from `googleusercontent.com` | Download or replace the image; see `stitch-design`. |
| ship: 555 number | a `tel:` link uses a fictional number | Read the phone from `data/site.json`; if it is `TODO`, leave the phone link out. |
| ship: booking link | the home page has no link to `booking.url` (WARN while it is `TODO`) | The primary call to action uses it. |
| ship: retired booking page | a page still links to Calendly after booking moved to Google Calendar | Read the link from `data/site.json`; this is expected to fail on the legacy root site until cutover. |
| plan: every planned page is built | an entry in `data/pages.json` has no built page | Build it or remove the entry. |
| plan: every built page is planned | a page exists that the plan does not know | Add it with `page_plan.py add`. `/404` is exempt. |
| plan: title, meta, H1 match | the built text differs from the plan | The template must read these from the plan rather than typing its own. |
| plan: TODO (WARN) | a planned page still has `TODO` fields | Decide the keyword and write them; blocks a production deploy. |

## Known state of the legacy site

Running `--dir .` on the single-file site that is live today fails several rows (long home title and meta, no canonical, no sitemap, no robots.txt, no JSON-LD). Those are real gaps, and they are the redesign's to fix; they are not a reason to edit the legacy files unless the owner asks.
