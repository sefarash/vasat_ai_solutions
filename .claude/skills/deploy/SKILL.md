---
name: deploy
description: The deploy procedure for the Vasat AI Solutions website on Netlify - the pre gate (conventions, page plan, build, SEO audit, clean tree), a deploy preview for review, the cutover from the legacy root site to site/dist, the post gate against the live URL, rollback, and the deploy log. Use when the owner says deploy, ship, publish, push live, go live, launch, release, "put the new design up", "update the website", asks for a preview link, asks to roll back or what is currently live, or when a task would merge into or push the main branch. Also use before changing netlify.toml, redirects or the domain. A deploy to production happens only on the owner's explicit "launch"; everything before that is a preview.
---

# deploy

Netlify serves the `main` branch of this repo at the URL in `data/site.json`. Until cutover it publishes the repo root (the legacy single-file site). After cutover it builds `site/` and publishes `site/dist`. Every deploy is gated twice: before (pre: is the tree fit to ship) and after (post: is what the host serves what we built). The pre gate cannot see the host, and the post gate cannot see the source, so neither replaces the other.

Netlify commands, the `netlify.toml` change for cutover and rollback details: `references/netlify.md`.

## Inputs

- What is being deployed (a commit on a branch) and where: a **preview** or **production**.
- For production: the owner's "launch" for this specific change, in their words, in this conversation.

## Procedure

1. **Pre gate.**
   ```bash
   python3 tools/deploy_gate.py pre
   ```
   Runs the conventions check and the page plan in strict mode (a `TODO` fact or title is a FAIL here), builds `site/`, runs the SEO audit, and requires a clean, committed tree. Any FAIL is NO-GO for production. For a preview, FAILs that are only `TODO` placeholders may be accepted by the owner by name; anything else is fixed first.

2. **Preview.** Push the branch and open a pull request, or run a manual draft deploy (see the reference). Netlify returns a preview URL that is not the production domain. Run the post gate against it:
   ```bash
   python3 tools/deploy_gate.py post <preview-url>
   ```
   Give the owner the preview URL, the two gate tables and the list of design differences from the `stitch-design` comparison. Stop here unless the owner has said launch.

3. **Production**, only on "launch". Merge the reviewed branch into `main` (or publish the reviewed deploy in Netlify). The first production deploy of the redesign is the cutover and also needs the `netlify.toml` change in the reference, including removing the catch-all rewrite that currently makes every unknown URL return the home page.

4. **Post gate on production.**
   ```bash
   python3 tools/deploy_gate.py post <production-url-from-data/site.json>
   ```
   Every planned page returns 200 with the planned title, index flags match, the home page links to the booking URL, no Stitch leftovers, robots.txt and the sitemap are served, and an unknown URL returns 404. Then open the site on a phone and submit the consultation form once, marked as a test, and confirm the notification email arrived (leads are delivered by email; see `lead_form` in `data/site.json`). A FAIL means roll back, not fix forward on the live site.

5. **Log it.**
   ```bash
   python3 tools/deploy_gate.py log <url> "<what changed>"
   ```
   Appends the time, commit and note to `docs/DEPLOY-LOG.md`.

6. **Rollback.** In Netlify, publish the previous production deploy (instant, no rebuild), then revert the merge on `main` so the next push does not redeploy the problem. Run the post gate again and log the rollback.

## Definition of done

- Pre gate GO and post gate GO, both tables given to the owner verbatim.
- For production: the owner's launch is on record in the conversation, the form test arrived, and `docs/DEPLOY-LOG.md` has the line.
- For a preview: the owner has the URL and knows it is a preview.

## Do not

- Do not push or merge to `main` to "see how it looks". Use a preview.
- Do not deploy from an uncommitted tree; the log needs a commit to roll back to.
- Do not skip the post gate because the pre gate passed.
- Do not deploy to production with any `TODO` in `data/site.json` or `data/pages.json`, or with a claims item the owner has not confirmed.
- Do not change DNS, the custom domain or Netlify site settings as part of a deploy; those are separate decisions for the owner.
- Do not put a Netlify token in the repo, a skill or the deploy log.
