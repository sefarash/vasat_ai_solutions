# Vasat AI Solutions — website

The marketing website for Vasat AI Solutions, hosted on Netlify. It is being redesigned from a Stitch export. Until cutover, the public site is the single-file site in the repo root.

## Layout

```
design/      Stitch export (stitch/DESIGN.md, stitch/<screen>/code.html + screen.png), logo.svg, logo.png, generated tokens.json. Reference only.
data/        site.json (business facts) and pages.json (page plan: route, keyword, title, meta, H1)
site/        the new website: Astro + Tailwind, static output in site/dist
tools/       deterministic checks and generators (Python 3.9, standard library only)
docs/        DEPLOY-LOG.md, SKILLS-TRIGGER-TEST.md
.claude/skills/   project skills (below)
index.html, privacy-policy.html, terms-of-service.html, netlify.toml    the legacy live site
```

## Running the new site

```bash
cd site
npm install
npm run dev        # local preview at http://localhost:4321
npm run build      # static output in site/dist
cd .. && python3 tools/seo_check.py
```

Needs Node 20.3 or newer. Home page copy lists live in `site/src/data/home.js`; facts and the page plan are read through `site/src/data/facts.js`. The logo in `site/src/assets/logo.svg` is `design/logo.svg` with the white background path removed and the canvas cropped.

## The rules in one paragraph

Facts are typed once, in `data/site.json`, and read from there. Titles, metas and H1s are typed once, in `data/pages.json`. The design is a reference: its phone number, testimonials, statistics and customer names are filler and do not ship unless the owner confirms them. `main` is production, so the redesign is built on a branch and reviewed on a preview, and nothing goes live until the owner says "launch".

## Tools

| Tool | What it does |
|---|---|
| `python3 tools/check_conventions.py [--strict]` | Secrets, `TODO` placeholders, facts hard-coded in `site/src`, Stitch leftovers |
| `python3 tools/design_audit.py tokens\|inventory\|claims\|all [--screen home] [--write]` | Reads the Stitch export: tokens and DESIGN.md conflicts, section and asset inventory, copy that states a fact |
| `python3 tools/page_plan.py validate\|keyword\|add\|list` | Validates the page plan, checks a keyword is free, adds a page |
| `python3 tools/seo_check.py [--dir <path>] [--no-plan]` | SEO and ship-readiness audit of built HTML, pass/fail table |
| `python3 tools/deploy_gate.py pre \| post <url> \| log <url> "<note>"` | Gates before and after a deploy; appends to the deploy log |

## Skills

Project skills live in `.claude/skills/<name>/SKILL.md`. Each has a description that decides when it loads, a procedure, a definition of done and a "do not" list. `CLAUDE.md` points every session at `project-conventions` first.

| Skill | What it does | Loads when | Tool |
|---|---|---|---|
| `project-conventions` | The rules every task must follow: where things live, facts from `data/site.json`, nothing invented, main is production | starting any task, before the first edit or commit, unsure where something belongs | `check_conventions.py` |
| `stitch-design` | Turns the Stitch export into real pages: tokens, conflicts, sections as components, asset replacement, the claims gate, side-by-side check | building or restyling any page or section, "match the design", a new design file arrives | `design_audit.py` |
| `new-site-page` | Adds, splits, merges or removes a page through the page plan | "add a service / industry / landing page", "make a page for X", changing a title or meta | `page_plan.py` |
| `seo-check` | Runs the audit on the built site and fixes failures at the source | any site file is edited, before a deploy, "is it ready to ship" | `seo_check.py` |
| `deploy` | Pre gate, preview, launch, post gate, rollback, log | deploy, ship, go live, launch, preview link, roll back, touching `main` or `netlify.toml` | `deploy_gate.py` |

Triggering test (three requests that should load each skill, two that should not): `docs/SKILLS-TRIGGER-TEST.md`.

Modelled on the skills in the Appliance World Repair client repo. That repo's voice-agent, Google Ads, lead-API and client-report skills are not copied here because this repo has no voice, ads or API code; add them when that work starts.
