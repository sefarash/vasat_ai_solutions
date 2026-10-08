---
name: project-conventions
description: The rules every task in the Vasat AI Solutions website repo must follow - where things live (design/, data/, site/, tools/), business facts read from data/site.json and never typed into a page, no invented facts or testimonials, secrets handling, commit format, and "main is production, so nothing reaches main until the owner says launch". Use when starting any task in this repository, onboarding a new session, before the first edit or commit, when unsure where a file or a fact belongs, or when another skill says "follow project-conventions". Load it even for a one-line copy change; it is short, and the facts and launch rules are easy to break by accident.
---

# Project conventions

This repo is Vasat AI Solutions' own marketing website. It is being redesigned from a Stitch export; the old single-file site in the repo root is still what the public sees. The rules below exist so the redesign can be built next to the live site without leaking design filler, wrong facts or half-finished pages into production.

## Read first

1. Root `README.md` for the layout and the skills table.
2. `data/site.json` for every business fact (name, URL, phone, booking link, services, prices) and `data/pages.json` for the page plan.
3. `design/stitch/` if the task touches how anything looks. The `stitch-design` skill explains how to read it.

## Where things live

```
design/      the Stitch export and logo. Reference only: read it, never edit it, never serve it.
data/        site.json (facts) and pages.json (page plan). The only place a fact or a title is typed.
site/        the new website (Astro + Tailwind, static output in site/dist). Does not exist until the build starts.
tools/       deterministic Python scripts (stdlib only, Python 3.9). The gates below.
docs/        DEPLOY-LOG.md and the skills trigger test.
*.html, netlify.toml in the root    the legacy live site. Leave it working until cutover.
```

The repo also follows the WAT framework in `CLAUDE.md`: skills are the instructions, `tools/` are the scripts that do the work. Look in `tools/` before writing a new script, and run a tool rather than reasoning about what it would say.

Stack: Astro + Tailwind compiled at build time, static output on Netlify. This matches the client-site template this repo is modelled on. Ask before adding any other framework or library.

## Facts come from data/site.json

- A phone number, email, address, price, plan name, booking URL or service name appears in exactly one place: `data/site.json`. Templates import it. Why: the same fact shows up in the header, hero, footer, schema and legal pages, and five hand-typed copies drift.
- A value that starts with `TODO` is a placeholder. It is fine while building and blocks a production deploy. When you need a value that is `TODO`, ask the owner. Do not fill it with something plausible, and do not copy it from the design: the Stitch export's phone number, email, testimonials, customer names and statistics are generated filler.
- Titles, meta descriptions and H1s live in `data/pages.json`, not in page files.

## Nothing invented reaches a visitor

The design is full of confident, specific, made-up claims (named customers, percentages, integrations). Publishing a fabricated testimonial or statistic is a legal and reputational problem for a business that sells trust to contractors. Every claim on a page must be one the owner confirmed. `python3 tools/design_audit.py claims` lists the ones the design contains.

## Main is production

Netlify serves this repo's `main` branch at the URL in `data/site.json`. So:

- Redesign work happens on a branch. Do not commit to, merge into or push `main` unless the owner asked for exactly that.
- Nothing replaces the live site until the owner says **launch**. "Make it live", "ship it" or "deploy" inside a task description is a reason to ask, not a launch.
- Pages meant only for ads or for after a form submit (`type: landing` or `utility` in the plan) are `noindex` and stay out of the sitemap and the navigation.

## Secrets

- Secrets live in `.env` (gitignored) and are read from the environment. Never write a key, token or account ID into code, JSON, docs or a skill. `data/site.json` is for public facts only; a GA4 ID is public, an API key is not.
- `credentials.json`, `token.json`, `.env*`, `*.pem`, `*.key` stay untracked. Do not weaken `.gitignore`.

## Commits

Commit only when the owner asks. Follow the existing history: one plain imperative sentence saying what changed for a visitor or a maintainer, for example `Add public Terms of Service page with footer links and clean URL redirect`. Add the `Co-Authored-By` trailer on commits Claude authored. Never commit `node_modules`, `site/dist` or `.env`.

## Procedure for any task

1. Read the three "read first" items and decide where the change belongs.
2. Run the check before and after editing:
   ```bash
   python3 tools/check_conventions.py
   ```
3. Make the change. A new fact goes into `data/site.json` first, then is read from there.
4. If the change touches anything a visitor or a crawler sees, run the `seo-check` skill.
5. Report what changed, what was verified, and what is still `TODO` or unconfirmed.

## Definition of done

- `tools/check_conventions.py` has no FAIL (WARN rows for `TODO` are expected until launch).
- No fact typed into a page; no claim the owner has not confirmed.
- Nothing merged or pushed to `main` without the owner asking.

## Do not

- Do not edit anything under `design/`. A design change comes from a new Stitch export.
- Do not delete or restyle the legacy root HTML files before cutover; they are the live site.
- Do not put phone numbers, emails, prices or URLs into a skill file. Skills name the file to read.
- Do not create or overwrite a file in `workflows/` without asking (see `CLAUDE.md`).
