# Netlify: how this site is hosted

## What is known

Confirmed with the Netlify CLI and by deploying:

- The Netlify project is `joyful-mochi-6d6b03`, connected to this GitHub repo, with the production domain from `data/site.json`.
- A push to `main` deploys to production automatically, in well under a minute.
- A pull request gets a deploy preview at `https://deploy-preview-<PR number>--joyful-mochi-6d6b03.netlify.app`. Netlify does not post a status check or a comment on the pull request, so do not wait for one: list the deploys instead (`netlify api listSiteDeploys --data '{"site_id":"<id>","per_page":5}'`; the id comes from `netlify api listSites`).
- The CLI is installed and logged in on the owner's machine, but this folder is not linked (`netlify link`), so pass the site id explicitly.
- Netlify cancels a build when nothing under `site/` changed ("no content change"). An empty commit, or a commit that only touches skills, tools or docs, does not produce a new deploy. To force one, change a file under `site/` or use "Trigger deploy" in the dashboard.
- Form detection was not active on the first preview (no form listed after the deploy). The owner enables it in the dashboard under Forms; a new deploy is needed afterwards for the form to register.

## Preview deploys

With Git-connected deploys: push the branch, open a pull request, and Netlify comments the preview URL (`deploy-preview-<n>--<site>.netlify.app`).

Manual, with the CLI, from a built tree:

```bash
cd site && npm run build
netlify deploy --dir=dist            # draft deploy; prints a unique preview URL, does not touch production
```

`netlify deploy --prod` publishes to production. It is run only on the owner's launch.

Netlify sends `X-Robots-Tag: noindex` on deploy-preview and draft URLs, so a preview is not indexed even though the pages themselves are indexable. That is why the post gate treats an index mismatch as a warning on a preview and a failure on production.

## Cutover: netlify.toml for the new site

The legacy config publishes `.`. The new site needs:

```toml
[build]
  base = "site"
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"
```

And the redirect rules change:

- Remove the catch-all `from = "/*" to = "/index.html" status = 200`. It was written for a single-page site; with real pages it turns every typo and every removed URL into a copy of the home page with status 200, which search engines treat as duplicate content and which hides broken links. The new site ships a real `404.html`, which Netlify serves automatically.
- The `/privacy-policy` and `/terms-of-service` rules are no longer needed if the new site builds those routes itself (`dist/privacy-policy/index.html`). Keep the URLs identical to today's so existing links keep working.
- Any URL that exists on the legacy site and not on the new one gets a 301 to its replacement.

Make this change in the same commit as the cutover so the old config never builds the new tree or the reverse.

## Forms

The consultation form uses Netlify Forms and leads are delivered by email. The `<form>` needs `data-netlify="true"`, the `name` from `lead_form.form_name` in `data/site.json`, a honeypot field for spam, and must be present in the static HTML at build time. Submissions appear under Forms in the dashboard.

The inbox that receives leads is set once by the owner in the dashboard (Forms → Form notifications → Add notification → Email notification). It is deliberately not in the repo, so a private address is never published. Netlify only detects the form after the first deploy that contains it, so the notification can be added only after the first preview deploy. The post-deploy form test in the deploy skill is what proves delivery.

## Rollback

Netlify keeps every deploy. Deploys → pick the last good production deploy → "Publish deploy". This is immediate and does not rebuild. Then revert the commit on `main`; otherwise the next push republishes the broken version. With auto publishing locked ("Stop auto publishing") the site stays on the chosen deploy until unlocked.
