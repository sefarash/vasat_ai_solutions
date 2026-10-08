# Skills triggering test

For each skill: three requests that should load it, two near-misses that should not, and the phrase in the description that decides it. "Routes to" names the skill (or none) that should load instead. Evaluated by reading each description as the router would; re-run this table after any description change.

## project-conventions
| Request | Should trigger | Why (description phrase) |
|---|---|---|
| "New session. What do I need to know before changing anything here?" | yes | "onboarding a new session" |
| "Where should the new phone number go so it shows up everywhere?" | yes | "when unsure where a file or a fact belongs" |
| "Commit what we have so far." | yes | "before the first edit or commit", commit format, main is production |
| "Write a Python function that formats a US phone number." | no | generic code, nothing about this repo. Routes to: none |
| "Explain what a Netlify redirect rule does." | no | general question, no change to this repo. Routes to: none |

## stitch-design
| Request | Should trigger | Why |
|---|---|---|
| "Build the hero section from the new design." | yes | "build … any page or section", "the new design" |
| "The services cards don't look like the mockup, the corners are wrong." | yes | "doesn't look like the design", "the mockup" |
| "I added another Stitch screen for the pricing page to the design folder." | yes | "when a new design file or screen is added" |
| "Add an industry page for roofing." | no | planning a page comes first; that procedure calls this skill at its build step. Routes to: new-site-page |
| "Make a new logo concept for us." | no | creating a design, not implementing the export. Routes to: none |

## new-site-page
| Request | Should trigger | Why |
|---|---|---|
| "We now also do Google Ads management, add that to the site." | yes | "asks to add a service" |
| "The 'Explore HVAC' button in the design goes nowhere, make that page." | yes | "a link in the design points at a page that does not exist yet" |
| "Shorten the home page title, it's getting cut off in Google." | yes | "changing any page's title, meta description or H1" |
| "Fix the typo in the second FAQ answer." | no | an edit to existing copy; audit afterwards. Routes to: seo-check |
| "Set up a Meta ads campaign for the HVAC offer." | no | running ads, not a site page. Routes to: none |

## seo-check
| Request | Should trigger | Why |
|---|---|---|
| "I changed the hero copy, can you check everything's still fine?" | yes | "whenever any page … is edited", "even after a small copy change" |
| "Is the new site ready to ship?" | yes | "is it ready to ship" |
| "Why isn't our services page showing up in Google?" | yes | "asks why a page is not showing up in Google" |
| "Which keywords should the HVAC page go after?" | no | planning, not auditing. Routes to: new-site-page |
| "Put the redesign on a preview link." | no | a deploy; its pre gate runs the audit itself. Routes to: deploy |

## deploy
| Request | Should trigger | Why |
|---|---|---|
| "Can I get a link to see the new design before it goes live?" | yes | "asks for a preview link" |
| "Launch the new site." | yes | "launch", "go live" |
| "The new version broke the form, put the old one back." | yes | "asks to roll back" |
| "Run the SEO audit on the build." | no | audit only, no deploy requested. Routes to: seo-check |
| "How do other agencies host their sites?" | no | general question. Routes to: none |
