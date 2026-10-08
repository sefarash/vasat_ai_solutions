---
name: new-site-page
description: The procedure for adding, splitting, merging or removing a page on the Vasat AI Solutions website - a service page (/services/<slug>), an industry page (/industries/<slug>), an ad landing page (/lp/<slug>) or a utility page such as /thank-you - by checking the keyword is free, adding the service or industry to data/site.json, adding the page to the plan in data/pages.json with tools/page_plan.py, writing unique copy, linking it from two existing pages and running the SEO audit. Use when the owner asks to add a service, an industry or trade, a landing page for a campaign, "make a page for X", when a link in the design points at a page that does not exist yet (the "Explore HVAC" style links), when deciding whether a keyword deserves its own page, or when changing any page's title, meta description or H1. Do not hand-write a title tag or create a page file first; follow this instead.
---

# new-site-page

A page on this site starts as an entry in the page plan, not as a file. `data/pages.json` holds the route, type, primary keyword, title, meta description and H1 of every page; the templates in `site/` render from it, and the SEO audit fails any built page that is missing from the plan or disagrees with it. Planning first is what stops two pages from competing for the same search and stops titles drifting past their limits.

Copy guidance by page type: `references/content-brief.md`. Read it before writing the page.

## Inputs

- What the page is for and its type: `service`, `industry`, `landing` (ads only, noindex) or `utility` (thank-you, 404; noindex).
- The keyword it should own, in the words a contractor would type. If the owner gave a Search Console query, that is the keyword to check.
- Real material for the page: what the service includes, the price from `data/site.json`, a real example or result. Ask for what is missing; a page built from the design's filler fails the claims rule in `project-conventions`.

## Procedure

1. **Check the keyword is free.**
   ```bash
   python3 tools/page_plan.py keyword "ai voice agent for hvac contractors"
   ```
   `TAKEN` (exit 1) means a page already owns it: improve that page instead. A `note:` line means an existing page uses the same words; a new page is justified only when the search intent differs (a different service, a different trade), not for a rewording.

2. **Add the fact, if it is new.** A new service or industry is added to the `services` or `industries` list in `data/site.json` (slug, name, and for a service its price). The plan check refuses a `/services/<slug>` or `/industries/<slug>` route whose slug is not there. Prices and names come from the owner.

3. **Add the page to the plan.** Dry run first:
   ```bash
   python3 tools/page_plan.py add --route /industries/hvac --type industry \
     --keyword "ai marketing for hvac contractors" \
     --title "AI Marketing for HVAC Contractors | Vasat AI Solutions" \
     --meta "<70-155 characters that say who it is for, what they get and the next step>" \
     --h1 "<contains the keyword, differs from the title>" --dry-run
   ```
   The tool validates the whole plan with the new entry and writes nothing if any row fails. Limits: title ≤ 60 characters, meta 70–155, the keyword's words in both title and H1, nothing duplicated across pages. `landing` and `utility` pages are set to noindex automatically.

4. **Write the page** in `site/src` using the existing template for its type and the components built from the design (`stitch-design` skill). Copy is written for this page, not adapted by swapping a noun in another page. Facts are read from `data/site.json`.

5. **Link it from at least two existing pages** (not counting the header or footer menus): for a service, from the home page's services section and one related service or industry page; for an industry, from the home page's industries section and one service page. A landing page gets no internal links at all; only ads point at it.

6. **Build and audit.**
   ```bash
   cd site && npm run build && cd .. && python3 tools/seo_check.py
   ```
   The page must appear under "every planned page is built", and no row may FAIL. Hand the page to the owner with its keyword and the two pages that link to it.

**Changing a title, meta or H1** is steps 3 and 6 only: edit the entry in `data/pages.json`, run `python3 tools/page_plan.py validate`, rebuild, audit.

**Merging or removing a page**: remove its entry from the plan, delete its page file, add a 301 redirect from the old URL to the page that replaces it in `netlify.toml`, and fix the links the audit then reports as broken.

## Definition of done

- `page_plan.py keyword` showed the keyword free, or the owner accepted the different-intent argument.
- `page_plan.py validate` has no FAIL.
- The page's copy is its own and every fact in it is confirmed.
- Two existing pages link to it (none, for a landing page).
- `seo_check.py` has no FAIL on the built site.

## Do not

- Do not type a `<title>` or meta description into a page file; they come from the plan.
- Do not create one page per city or per keyword variation with the same copy. Near-duplicate pages hurt the pages that already rank.
- Do not link to a `/lp/` page from the navigation, the footer, the sitemap or any organic page.
- Do not add a service to the site that the owner does not sell yet. The design shows services that are not in `data/site.json`; that is a question for the owner, not a page to build.
