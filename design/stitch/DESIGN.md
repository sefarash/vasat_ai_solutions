---
name: Sovereign Synthesis
colors:
  surface: '#faf9ff'
  surface-dim: '#cfdaf8'
  surface-bright: '#faf9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8ff'
  surface-container-highest: '#d9e2ff'
  on-surface: '#111b31'
  on-surface-variant: '#444650'
  inverse-surface: '#263047'
  inverse-on-surface: '#edf0ff'
  outline: '#757681'
  outline-variant: '#c5c6d1'
  surface-tint: '#455c99'
  primary: '#001645'
  on-primary: '#ffffff'
  primary-container: '#0f2b66'
  on-primary-container: '#7e94d5'
  inverse-primary: '#b2c5ff'
  secondary: '#005ac2'
  on-secondary: '#ffffff'
  secondary-container: '#4d8eff'
  on-secondary-container: '#00285d'
  tertiary: '#251700'
  on-tertiary: '#ffffff'
  tertiary-container: '#3f2b00'
  on-tertiary-container: '#bf8e26'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001849'
  on-primary-fixed-variant: '#2c4480'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#ffdea8'
  tertiary-fixed-dim: '#f5be53'
  on-tertiary-fixed: '#271900'
  on-tertiary-fixed-variant: '#5e4200'
  background: '#faf9ff'
  on-background: '#111b31'
  surface-variant: '#d9e2ff'
typography:
  display-lg:
    fontFamily: Sora
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: Sora
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-xl:
    fontFamily: Sora
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Sora
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Sora
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: 0em
  title-md:
    fontFamily: Sora
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.01em
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-md:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.08em
  code-sm:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
spacing:
  gutter: 1.5rem
  gutter-mobile: 0.75rem
  margin: 2.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
  space-2xl: 4rem
---

## Brand & Style

This design system translates the dual essence of the brand mark—a sweeping dynamic union between human aspiration and cognitive intelligence—into a refined, razor-sharp digital language. It communicates enterprise-grade trustworthiness, precision, and forward-looking momentum. 

The aesthetic is characterized by high-contrast architectural minimalism: crystalline layouts, mathematically precise zero-radius surfaces, and luminous metallic amber cues embedded directly within an immaculate, light-first canvas anchored by deep cobalt and midnight navy. The design system eschews soft, generic SaaS conventions in favor of authoritative geometric structures, echoing the soaring wings and crisp triangular intersections of the identity.

## Colors

The color palette draws directly from the intersecting wings and core sphere of the visual identity:

- **Primary (`#0F2B66`)**: Deep Midnight Cobalt represents structural permanence, institutional confidence, and algorithmic intelligence. It serves as the primary ground for high-emphasis framing, navigation, and key typography.
- **Secondary (`#0062D2`)**: Electric Royal Blue captures energetic flow, user interaction, active states, and focal guidance across critical actions.
- **Tertiary (`#D4A038`)**: Warm Metallic Amber/Gold serves as a precious accent reflecting the central sphere and ascending apex. It denotes AI synthesis, intelligence breakthroughs, highlights, and specialized badges.
- **Neutral (`#071228`)**: Obsidian Ink is used for high-contrast legible prose, sharp hairline dividing grids, and dense data displays against neutral light grounds (`#F8FAFC` and `#FFFFFF`).

## Typography

The type pairing mirrors the technological duality of the mark:
- **Sora** brings geometric authority, wide letterforms, and sculpted vertices for headlines, evoking mathematical precision and visionary scale.
- **Space Grotesk** is chosen for body and micro-copy, providing a computational rhythm with legible horizontal metrics and technical character shapes that heighten the product's analytical pedigree.

Tracking is deliberately expanded on uppercase labels (`+0.08em`) to mirror the letterspacing present in secondary lockups, while display headlines remain tightly kerned to preserve structural solidity.

## Layout & Spacing

Layouts follow a rigid 12-column structural grid system on desktop (8-column on tablet, 4-column on mobile). Boundaries, partitions, and metrics favor geometric multiples of 8px.

Whitespace is clean, functional, and uncrowded. Structural lines are used intentionally to define content corridors and data-dense dashboards. Margin zones maintain breathing room, isolating high-value analytical workflows from ancillary controls.

## Elevation & Depth

Visual hierarchy does not rely on heavy, blurry drop shadows. Instead, the design system utilizes **tonal layering**, **crisp hairline borders**, and **tactile metallic edge accents**:

- **Level 0 (Canvas)**: Pristine white (`#FFFFFF`) or pale cool technical tint (`#F8FAFC`).
- **Level 1 (Sub-Surfaces & Panels)**: Grounded by 1px solid low-contrast hairline borders (`rgba(15, 43, 102, 0.12)`) without ambient shadow.
- **Level 2 (Interactive Floating Modules & Modals)**: Lifted via a directional, architectural shadow (`0 8px 24px -4px rgba(15, 43, 102, 0.12)`) combined with a 1px solid border.
- **High-Focus AI Highlights**: Emphasized panels leverage a 1px top highlight or left indicator border rendered in Warm Metallic Amber (`#D4A038`), echoing the gilded crest in the brand identity.

## Shapes

In strict alignment with the sharp, dynamic vertices found in the visual identity, all UI containers, buttons, cards, tags, and form fields adopt a **strict 0px border radius**. This zero-radius paradigm imparts an architectural, high-precision feel that sets the application apart from generic softened interfaces, conveying clinical exactitude and engineering rigor.

## Components

- **Buttons**: Strict rectangular blocks with 0px radius.
  - *Primary*: Deep Midnight Cobalt background (`#0F2B66`), white typography, 1px solid `#0F2B66` outline. Hover shifts background to Royal Blue (`#0062D2`).
  - *Secondary / Accent*: Amber metallic outline (`#D4A038`) with dark cobalt typography and transparent background; fills with `#D4A038` texturing on active state.
  - *Tertiary*: Flat text with an animated bottom hairline rule.
- **Input Fields**: Monolithic rectangular inputs framed with 1px border (`rgba(15, 43, 102, 0.2)`). Focus state transitions to a 1.5px solid Royal Blue border (`#0062D2`) with zero corner rounding.
- **Cards & Data Modules**: Zero-radius white surfaces bound by a 1px hairline border. Feature cards incorporate an optional 2px top perimeter band in either Deep Cobalt or Warm Amber to signify priority tier.
- **Chips & Tags**: Monospaced-styled rectangular tokens with 0px radius, low-saturation backgrounds (e.g., `#0F2B66` at 6% opacity), and bold, high-contrast labels in uppercase.
- **Checkboxes & Radios**: Square geometry for checkboxes with sharp checkmarks; diamond or faceted squares for radio indicators rather than circles, upholding the angular design system ethos.
- **Status Indicators & AI Insights**: Structured banners anchored by a gold accent tab (`#D4A038`) alongside monospace metric annotations to surface model inference states and execution telemetry.