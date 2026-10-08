---
name: stitch-design
description: How to turn the Stitch design export in design/stitch (DESIGN.md, a code.html and screen.png per screen, plus design/logo.png) into real pages in site/ - reading the tokens, resolving where DESIGN.md and code.html disagree, building section by section as components, replacing Stitch-hosted images, icon fonts and the Tailwind CDN, and gating every piece of design copy that states a fact. Use whenever the task is to build, rebuild, restyle or "match the design" for any page or section, when the owner mentions Stitch, the new design, the mockup, the brand update, colours, fonts, spacing or the logo, when a new design file or screen is added, and when something "doesn't look like the design". Use it before writing any markup or CSS for this site, even for one section.
---

# stitch-design

The design arrives as a Stitch export: a rendered page (`code.html`), a thumbnail (`screen.png`) and a design-system description (`DESIGN.md`). The export is a picture of the goal, not code to ship. It loads Tailwind from a CDN, hot-links images from Google's servers, uses an icon font, has links that go nowhere, and its copy is filled with invented customers and numbers. This skill is the path from that picture to production pages.

Details that are only sometimes needed are in `references/`:
- `references/source-of-truth.md` — the known conflicts between DESIGN.md and code.html, and what wins.
- `references/build-notes.md` — images, logo, icons, fonts, dark and light sections, accessibility.

## Inputs

- The screen to build: a folder under `design/stitch/` containing `code.html` (currently `home`).
- `data/site.json` for facts and `data/pages.json` for the page's title, meta and H1.
- Answers from the owner for every item the claims report lists. Without them the section is built with the claim removed, not with the filler.

## Procedure

1. **Audit the screen.** Run it, do not eyeball the HTML:
   ```bash
   python3 tools/design_audit.py all --screen home
   ```
   `tokens` shows the palette, fonts and radius and every DESIGN.md conflict. `inventory` lists sections in order, headings, images, icons and form fields. `claims` lists the copy that states a fact.

2. **Settle the conflicts before building.** `code.html` is what was rendered and approved, so it wins by default. If a conflict changes the look of the whole site (body font, corner radius), say so to the owner once and proceed with `code.html` unless told otherwise. See `references/source-of-truth.md`.

3. **Generate the tokens and wire them into Tailwind.**
   ```bash
   python3 tools/design_audit.py tokens --write      # writes design/tokens.json
   ```
   The site's Tailwind theme is built from `design/tokens.json`. Keep the token names from the export (`primary`, `gold`, `surface-container`, `headline-lg`, `space-xl`) so class names in `code.html` keep their meaning. Hex values that the export uses repeatedly inside class names (the audit lists them) become named tokens rather than being pasted again.

4. **Build one section at a time, in inventory order.** Each section is a component in `site/src/components/`, fed by props or by `data/site.json`. For each one:
   - Take structure and class names from `code.html`; that is the fastest route to fidelity.
   - Replace every fact with a value read from `data/site.json`.
   - Replace every image, icon and font as described in `references/build-notes.md`.
   - Give every `href="#"` a real target or remove the link.
   Repeated markup (service cards, industry cards, testimonial cards, steps) becomes one component rendered from a list, not five pasted blocks.

5. **Gate the copy.** For each line in the claims report, one of three things happens: the owner confirmed it and it ships as written; it is replaced by a fact from `data/site.json`; or it is removed. A testimonial ships only with a real customer's consent. A section whose content is all filler (the testimonials block, the stats strip, the fake dashboard card) is either rebuilt from real material or left out; say which in the report.

6. **Check the result against the design.** `screen.png` is a 333 px wide thumbnail, too small to compare against. Instead, open `design/stitch/<screen>/code.html` and the built page in a browser at 390 px and 1440 px wide and compare section by section: spacing, type sizes, colours, the dark and light rhythm, hover states, the mobile menu. Use the Playwright or Chrome tools to take both screenshots. Differences that came from steps 4 and 5 (real images, removed claims) are expected; list them.

7. **Run the gates.**
   ```bash
   python3 tools/check_conventions.py
   cd site && npm run build && cd .. && python3 tools/seo_check.py
   ```
   The `ship:` rows fail on anything from the export that must not go live.

## Adding a new screen or an updated export

Put the new export in `design/stitch/<screen>/` with `code.html` and `screen.png`, keep the old folder until the page built from it is replaced, and re-run step 1. If the new export changes tokens, regenerate `design/tokens.json` and rebuild; never hand-edit the generated file.

## Definition of done

- Every section in the inventory is built, or deliberately left out with the reason reported.
- Tokens come from `design/tokens.json`; no colour or font is typed by hand in a component.
- Every claims item is confirmed, replaced or removed, and the report says which.
- Side-by-side comparison done at both widths, differences listed.
- `check_conventions.py` and `seo_check.py` show no FAIL.

## Do not

- Do not copy `code.html` into the site wholesale. It will pass a glance and fail every gate.
- Do not edit files under `design/`. They are the record of what was approved.
- Do not keep the Tailwind CDN script, a `googleusercontent.com` image URL or the Material Symbols font link.
- Do not ship design copy because it "sounds right". If the owner has not confirmed it, it is not a fact.
- Do not redesign. Where the export is ambiguous or broken, pick the closest reading and report it rather than inventing a new look.
