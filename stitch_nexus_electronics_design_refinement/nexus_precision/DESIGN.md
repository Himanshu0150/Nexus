---
name: Nexus Precision
colors:
  surface: '#fbf9f9'
  surface-dim: '#dbdad9'
  surface-bright: '#fbf9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#efeded'
  surface-container-high: '#e9e8e7'
  surface-container-highest: '#e3e2e2'
  on-surface: '#1b1c1c'
  on-surface-variant: '#434654'
  inverse-surface: '#303031'
  inverse-on-surface: '#f2f0f0'
  outline: '#737685'
  outline-variant: '#c3c6d6'
  surface-tint: '#1555d1'
  primary: '#0650cc'
  on-primary: '#ffffff'
  primary-container: '#356ae6'
  on-primary-container: '#f9f7ff'
  inverse-primary: '#b3c5ff'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#525a65'
  on-tertiary: '#ffffff'
  tertiary-container: '#6b727e'
  on-tertiary-container: '#f5f7ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b3c5ff'
  on-primary-fixed: '#00174a'
  on-primary-fixed-variant: '#003ea6'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#dce3f1'
  tertiary-fixed-dim: '#c0c7d4'
  on-tertiary-fixed: '#151c26'
  on-tertiary-fixed-variant: '#404752'
  background: '#fbf9f9'
  on-background: '#1b1c1c'
  surface-variant: '#e3e2e2'
typography:
  display:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: '600'
    lineHeight: 64px
    letterSpacing: -0.03em
  display-mobile:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.025em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: -0.015em
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 3rem
  margin-sm: 1rem
  margin-md: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes an architectural, high-precision visual environment tailored for premium consumer technology and professional hardware. It channels functional industrial design lineages—reminiscent of Dieter Rams' Vitsoe principles and modern high-end industrial engineering—marrying absolute visual discipline with effortless digital commerce usability.

The target audience encompasses discerning technologists, creative professionals, and industrial enthusiasts who value structural clarity, tactile restraint, and authentic material fidelity over decorative visual noise. The interface avoids frivolous gradients, whimsical micro-interactions, or generic SaaS trends in favor of gallery-like presentation: expansive white surfaces, precise hairline delineations, and clinical typography. The user experience evokes confidence, mechanical precision, and quiet luxury.

## Colors

The palette relies on high-purity luminance with deliberate, disciplined anchor points. The canvas is predominantly clean white (`#FFFFFF`) framed by neutral stone surfaces (`#F3F4F6`), creating structural plane separation without relying on optical weight.

### Palette Architecture
- **Canvas Base (`#FFFFFF`):** Primary display plane for high-fidelity product rendering and high-contrast editorial space.
- **Surface Muted (`#F3F4F6`):** Secondary structural backplates, feature specs tables, and technical readouts.
- **Interactive Cobalt (`#356AE6`):** Reserved strictly for actionable highlights, focused states, and definitive purchase triggers. Never used decoratively.
- **Ice Highlight (`#EAF1FF`):** Soft optical wash used for active tab indicators, technical badges, and delicate selection backgrounds.
- **Charcoal Solid (`#242424`):** Hardware-grade dark neutral for primary buttons, high-priority navigation bars, and structural anchors.
- **Ink Primary (`#171717`):** Primary typographic ink offering stark legibility without the harshness of pure black.
- **Steel Secondary (`#737373`):** Descriptive metadata, technical labels, and inactive utility glyphs.
- **Hairline Divider (`#E5E5E5`):** Structural 1px boundary line establishing component grids.

### Feedback Signals
- **Success (`#16865C`):** Subdued spruce green denoting confirmed telemetry, stock availability, and checkout confirmation.
- **Warning (`#D97706`):** Precision amber for inventory alerts and system constraints.
- **Error (`#DC4545`):** Sharp crimson for form invalidation and operational errors.

## Typography

The typography is built entirely on `Inter` to deliver an uncompromising, neutral reading texture. Hierarchy is modulated through disciplined negative tracking (tighter letter spacing) on large displays and deliberate weight jumps between medium (`500`) and semi-bold (`600`) weights.

### Application Guidelines
- **Display & Large Headlines:** Tracked tight (`-0.02em` to `-0.03em`) to mimic swiss grid editorial titles. Used strictly for hero device titles and category introductions.
- **Body Text:** Standardized around a 15px baseline with comfortable 24px line height for technical device specifications, product essays, and checkout summaries.
- **Labels & Overlines:** Monospaced-like optical tightness using semi-bold uppercase tracking (`0.02em` to `0.04em`) at 11px and 12px for model numbers, hardware specs, status flags, and table headings.

## Layout & Spacing

The layout is anchored in an architectonic 12-column structural grid system that maintains rigorous vertical and horizontal alignments across viewport dimensions.

### Grid Framework & Viewports
- **Desktop (1280px+):** 12 columns, fixed maximum canvas container of 1440px, 48px outer margins (`margin`), 24px column gutters (`gutter`).
- **Tablet (768px – 1279px):** 8 columns, 32px outer margins (`margin-md`), 16px column gutters (`gutter-sm`).
- **Mobile (< 768px):** 4 columns, 16px outer margins (`margin-sm`), 12px column gutters.

### Spatial Rhythm
Layout elements respect strict multiples of 4px and 8px:
- `space-xs` (4px): Micro-gaps between badge iconography and typography labels.
- `space-sm` (8px): Internal paddings for compact technical chips and dense controls.
- `space-md` (16px): Standard form row gaps, button interior horizontal padding, and card interior spacing.
- `space-lg` (24px): Inter-card spacing within listing grids.
- `space-xl` (40px): Section breaks between product specifications and media modules.

## Elevation & Depth

This design system deliberately rejects heavy diffusion drop-shadows and blurred glass treatments. Visual hierarchy is established via physical surface boundaries, tonal layering, and microscopic hairline contrast.

### Spatial Depths
1. **Surface 0 (Ground Plane):** `#FFFFFF`. The global baseline plane for primary reading and primary card assets.
2. **Surface 1 (Inset Plane):** `#F3F4F6`. Used for technical parameter docks, peripheral configuration trays, and secondary comparison columns.
3. **Outlines & Boundaries:** Surfaces are compartmentalized using 1px crisp borders in `#E5E5E5`. When a surface must separate from another without border interruption, an ambient grounding contact shadow may be employed:
   - `elevation-card`: `0px 1px 2px rgba(0, 0, 0, 0.04), 0px 0px 0px 1px #E5E5E5`
   - `elevation-modal`: `0px 12px 32px -4px rgba(0, 0, 0, 0.08), 0px 0px 0px 1px #E5E5E5`
4. **State Depth:** On interactive card hover, elements do not physically "float" outward through blurred shadows; instead, borders transition from `#E5E5E5` to `#242424` or `#356AE6` with a micro 1px hairline displacement.

## Shapes

The geometry reflects machined precision. Roundedness is kept strictly understated between 4px and 6px, completely avoiding oval pill-shapes or bubbly contours.

### Corner Radius System
- **Base Elements (`rounded-sm` / 4px):** Form inputs, buttons, checkboxes, tooltips, segmented control segments, and small technical tags.
- **Containers (`rounded-md` / 6px):** Product cards, device specification modules, dialog boxes, and media viewports.
- **Exceptions:** No element—including floating action elements, chips, or system badges—may use fully circular (`9999px`) rounded caps. All geometries must retain deliberate structural architecture.

## Components

### Buttons
- **Primary Action:** Solid `#242424` background, `#FFFFFF` text, 4px border radius. 0 1px 2px rgba(0,0,0,0.05). Hover shifts background to `#171717`. Active state scales down imperceptibly (`scale(0.99)`).
- **Secondary Action:** `#FFFFFF` background, 1px `#E5E5E5` border, `#171717` text. Hover shifts border to `#242424`.
- **Accent Action:** Solid `#356AE6` background, `#FFFFFF` text. Reserved strictly for primary transactional paths (e.g., "Add to Bag", "Place Order"). Hover shifts to `#2A58C7`.
- **Ghost/Tertiary:** No background, `#171717` text, underlined with 1px `#E5E5E5` on focus/hover.

### Product & Spec Cards
- Framed with 1px `#E5E5E5` border, `#FFFFFF` background, 6px border radius.
- Imagery sits inside a dedicated top container bathed in `#F3F4F6` with subtle 4px inset padding.
- Technical parameters (e.g., "M3 Max / 36GB / 1TB") utilize 12px `#737373` font with high horizontal density.
- Hover states darken the perimeter border to `#171717` without upward shadow projection.

### Chips & Technical Filters
- Structured rectangular tags with 4px border radius.
- **Default State:** `#FFFFFF` background, 1px `#E5E5E5` border, `#737373` text.
- **Selected State:** `#EAF1FF` background, 1px `#356AE6` border, `#356AE6` text, weight `500`.

### Form Inputs & Selectors
- Height: 40px base. Background `#FFFFFF`, 1px border `#E5E5E5`, 4px border radius.
- Text: 14px `#171717`. Placeholder text: `#737373`.
- Focus state: Border transitions to `#356AE6` with a zero-distance outer ring `0 0 0 1px #356AE6`. No thick colored halos.

### Checkboxes & Radios
- Size: 16px square (checkbox) or circle (radio).
- Default: `#FFFFFF` fill with 1px `#E5E5E5` stroke.
- Checked: `#356AE6` fill with pure `#FFFFFF` geometric check icon or inner bullet.

### Technical Data Tables & Spec Modules
- Rows separated strictly by 1px `#E5E5E5` horizontal rules.
- Header row uses `#F3F4F6` background with uppercase 11px `#737373` tracking.
- Alternating rows avoid striped fills; white space and hairline rules define data parsing.