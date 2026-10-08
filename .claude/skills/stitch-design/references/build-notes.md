# Build notes: what to replace from the export, and how

## Images

Every `<img>` in the export points at `lh3.googleusercontent.com/aida-public/...`. Those URLs belong to Stitch, can expire, and are AI-generated stand-ins.

- For a photo slot, ask the owner for a real photo first. The design's own copy promises real technicians, not stock.
- If the generated image is to be used as an interim, download it into `site/src/assets/` now (the URL may not last), and serve it through the framework's image pipeline so it gets width, height, modern formats and lazy loading. Tell the owner it is a generated image.
- Write alt text that describes the picture for someone who cannot see it. Decorative images get `alt=""`.
- The hero image is the likely largest-contentful-paint element: do not lazy-load it, and give it explicit dimensions.

## Logo

`design/logo.png` is 1536×1024, on a white background, with the wordmark included. The header sits on white, the footer on dark navy, so a white-background PNG cannot be used in the footer. Ask the owner for an SVG or a transparent PNG, and a light-on-dark variant. Until then, use the PNG only on light surfaces and crop nothing by hand. Also needed from the logo: a favicon and a 1200×630 social image.

## Icons

The export uses the Material Symbols icon font, loaded twice, and names icons as text inside a span. Shipping that font costs several hundred kilobytes for about 36 glyphs and shows raw words like `arrow_forward` while it loads. Use inline SVG for exactly the icons in the inventory, through one `Icon` component. Icons that only decorate get `aria-hidden="true"`.

## Tailwind

The export loads `cdn.tailwindcss.com` with the `forms` and `container-queries` plugins and an inline config. In the site, Tailwind is compiled at build time with the theme from `design/tokens.json`, so the same class names work. The CDN script must not appear in any built page.

## Fonts

Sora for headlines, Inter for body, per `code.html`. Load only the weights the page uses (the audit's inventory shows the export requests more than it needs), with `font-display: swap`. Self-hosting through the build is preferred over a Google Fonts link.

## Dark and light sections

Sections alternate. The dark sections use gradients between several near-identical navy hex values typed directly into class names. Promote those to two or three named tokens. Check contrast in both directions: gold text on white fails WCAG AA at body sizes, so on light sections gold is for borders, large display text and icons, and `gold-dark` is for small text.

## Structure and accessibility

- Exactly one `<h1>` per page, with the text from `data/pages.json`. Heading levels then descend without skipping.
- One `<header>`, one `<main>`, one `<footer>`. The export's fixed header needs a skip link and a working mobile menu (the export hides the nav below `xl` and provides no replacement).
- Every form field has a visible `<label>`, a `name`, the right `type` and `autocomplete`. The form is wired as `lead_form` in `data/site.json` describes (Netlify Forms, delivered by email); see the deploy skill's `references/netlify.md`.
- Honour `prefers-reduced-motion` for any animation carried over.

## Facts the business does not have

A `null` in `data/site.json` (phone, address) means there is none on purpose. The export shows a phone number in the header, the hero and the contact section, and an address block in the footer: leave those elements out and let the booking button and the contact email carry the call to action. Do not keep the design's number as a stand-in.

## Booking

Consultations are booked through the provider and URL in `booking` in `data/site.json`. Every "Book a Free Consultation" button links to that URL, opening in a new tab; an embedded scheduler is an option only if the owner asks, because the provider's embed script slows the page. While the URL is `TODO`, build the buttons from the data and report that they have no target yet.

## Links

The export has several `href="#"` links ("Explore HVAC", footer service links, legal links). Each one points to a real route from `data/pages.json`, becomes a booking link, or is removed. A link to a page that is not in the plan means the page needs planning first; see the `new-site-page` skill.
