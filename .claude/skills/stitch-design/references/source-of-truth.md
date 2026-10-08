# Which design file wins

The export has three descriptions of the same design and they disagree. Order of authority:

1. `design/stitch/<screen>/code.html` — the rendered page the owner looked at and approved.
2. `design/logo.png` — the brand mark; the palette is derived from it.
3. `design/stitch/DESIGN.md` — the design system written before the "brand update" screen was generated. Use it for intent (what gold accents mean, how hierarchy is built without heavy shadows) and where `code.html` is silent.

Run `python3 tools/design_audit.py tokens` for the current list. The conflicts found when the export was first imported:

| Topic | DESIGN.md says | code.html does | Build with |
|---|---|---|---|
| Body font | Space Grotesk | Inter | Inter |
| Headline font | Sora | Sora | Sora |
| Corner radius | strict 0 px everywhere | rounded-xl, rounded-2xl and pill shapes throughout | rounded, per the radius scale in `code.html` |
| Canvas | light-first | alternating dark navy and light sections | alternating, in inventory order |
| Primary colour | `#001645` | `#0f2b66` | `code.html` |
| Gold accent | `#D4A038` in prose | `gold #d4af37`, `gold-hover #c8922a` | `code.html` |
| About 20 other colour tokens | slightly different values | — | `code.html` |

These are large enough (font, radius) that the owner should hear about them once. If they prefer the DESIGN.md version of any row, that is a design decision: record it in this table and build to it.

Things neither file defines, where the build must choose and report the choice: focus styles, form error states, the mobile navigation's open state, the 404 page, and any page other than the screens that were exported (services, industries, legal). For those, extend the patterns the home screen already uses rather than introducing new ones.
