---
name: seo-check
description: Runs this site's SEO and ship-readiness audit (tools/seo_check.py) over the built HTML - one H1, title and meta lengths, canonical, Open Graph tags, noindex where the plan says, sitemap and robots.txt, JSON-LD validity, broken links, dead anchors and href="#" placeholders, orphan pages, word count, alt text, leftovers from the Stitch export (Tailwind CDN, hot-linked images, fictional phone numbers), the booking link, and a match against the page plan - and prints a pass/fail table. Use whenever any page, component, template or data file of the Vasat AI Solutions site is edited or added, before any deploy, and when the owner says "check SEO", "audit the site", "is it ready to ship", "is the site OK", or asks why a page is not showing up in Google. Run it even after a small copy change; this project's own skills end by calling it.
---

# seo-check

The site's job is to be found by contractors searching for help and to turn the visit into a booked call. The audit turns that into a mechanical gate. It reads the **built** HTML, so it checks exactly what a crawler and a visitor receive, including mistakes introduced by templates.

What each row means and how to fix it: `references/checks.md`. Read it when a row fails and the fix is not obvious.

## Inputs

- Built output in `site/dist` (from `cd site && npm run build`). Before the new site exists, `--dir .` audits the legacy site in the repo root.
- `data/site.json` for the base URL and booking link, `data/pages.json` for the plan. `--base` overrides the URL; `--no-plan` skips the plan comparison for a one-off directory.

## Procedure

1. Build, then run:
   ```bash
   python3 tools/seo_check.py                 # site/dist against the plan
   python3 tools/seo_check.py --dir .         # the legacy live site
   python3 tools/seo_check.py --json /tmp/seo.json
   ```
   Exit 0 means no FAIL, 1 means at least one, 2 means there was nothing to audit.
2. Read the table. Each row is PASS, FAIL, WARN or SKIP, with the offending routes in the last column.
3. Fix every FAIL at its source: page and component files in `site/src`, titles, metas and H1s in `data/pages.json`, facts in `data/site.json`, sitemap and robots in the site config. Rebuild and re-run until no row fails.
4. WARN rows are reported to the owner by name. A `TODO` title is a WARN while building and becomes a blocker at deploy time (the deploy gate runs the plan in strict mode).
5. Give the owner the final table.

The audit does not measure speed. For performance, run Lighthouse in Chrome DevTools (mobile) on the home page and one inner page from a local preview of `site/dist`, and fix the largest item it names first: usually an unsized or oversized hero image, a render-blocking font or script.

## Definition of done

- No FAIL row for `site/dist` with the plan enabled.
- Every WARN reported to the owner, with what it is waiting on.
- If the tool itself was changed: it still passes on a known-good build and still fails the raw export. Copy `design/stitch/home/code.html` to an empty temporary folder as `index.html` and run with `--dir <folder> --no-plan`; the three `ship:` rows and the `href="#"` row must FAIL.

## Do not

- Do not edit files in `site/dist` to make a row pass; the next build erases it.
- Do not raise a limit or delete a check to get a clean table. Report the exception to the owner instead.
- Do not add `Disallow` lines to robots.txt to hide a noindex page. A crawler has to fetch the page to see the `noindex`.
- Do not treat a clean table as proof the copy is true. The audit cannot tell a real testimonial from an invented one; that is the claims step in `stitch-design`.
