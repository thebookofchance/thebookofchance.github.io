# Publication Visual System v1.0

**Date:** 22 November 2026  
**Project:** The Book of Chance website and publication library  
**Status:** Working visual system for current and near-future publications

## Purpose

This document establishes a coherent visual publishing system for *The Book of Chance* and its companion works. The system is based on the existing visual language of the foundational book rather than replacing it with a separate brand.

## Core visual DNA

The system inherits five constant traits from *The Book of Chance*:

1. **Large areas of quiet space** — covers feel literary, restrained and contemplative.
2. **Serif-led titling** — title typography remains calm, formal and bookish rather than promotional.
3. **Fine path-lines** — thin charcoal and blue paths represent contingency, contact, divergence, shared routes and possibility.
4. **Blue as accent, not flood** — blue should guide the eye or emphasise one path, never dominate the cover.
5. **A clear author sign-off** — the byline "H" sits low on the cover, anchored by a thin blue rule.

## Publication families

### 1. Foundational works
For the main philosophical text and any future direct sequel.

- Use the most complete path-weave.
- Preserve the strongest sense of central crossing.
- Allow more visual weight to the title than to any series label.
- Current reference: *The Book of Chance* Light and Dark editions.

### 2. Companion booklets
For short, structured thematic companions such as *The Five Values*.

- Use a simplified path band or concept-led motif.
- Keep titles prominent and centred.
- Include the line `THE BOOK OF CHANCE · COMPANIONS` at the top.
- Covers should feel related to the foundational book without copying it exactly.

### 3. Conversation guides
For facilitated or self-guided discussion books such as *Conversations of Chance*.

- Use the companion label.
- Emphasise dialogue, crossing perspectives and plurality.
- Allow a slightly more dynamic path arrangement than booklet covers.
- Where useful, a subtle numerical signal may appear in the web presentation, but the cover itself remains literary first.

### 4. Letters from H
For standalone essay-length texts.

- Use the same palette and path logic in a simpler single-essay format.
- Each letter cover should feel like a family variation rather than a new brand.
- Social metadata should use the letter’s own cover rather than the main book cover.

### 5. Journals and worksheets
For practical reflective tools.

- Keep the same serif/sans relationship.
- Use quieter, more functional layouts.
- Maintain recognisable affinity with the main library without competing with book covers.

## Palette

- **Paper:** `#fbfbfa`
- **Ink:** `#26313B`
- **Muted text:** `#68747c`
- **Light line:** `#d8dfe2`
- **Accent blue:** `#286CB8`
- **Soft grey line:** `#8e959a`

These values may be adjusted slightly only when needed for print or export compatibility.

## Typography

- Primary literary face: Georgia / Liberation Serif / equivalent serif
- Supporting label face: Lato / Liberation Sans / equivalent sans-serif
- Titles should remain elegant and spacious, not compressed or ornamental.
- Subtitles should be quieter than titles and may be italic serif.

## Cover rules

- Default cover size: **1000 × 1500 px**
- Working format set: **SVG + PNG + WEBP**
- Every publication page should expose its own cover visually on-page.
- Every publication page should use its own cover (or future share card) for `og:image` instead of always falling back to the main book cover.

## Asset naming

- Main book: `assets/covers/`
- Companion booklets: `assets/booklets/`
- Discussion companions and future standalone publications: `assets/publications/`
- Letters: `assets/letters/`
- Journals: `assets/journals/`

Naming convention:
- `title-cover.svg`
- `title-cover.png`
- `title-cover.webp`

## Website presentation rules

- Home page features should prefer real cover art over abstract placeholders once a cover exists.
- Library sections should show recognisable publication objects, not only text banners.
- Publication landing pages should display the actual cover with consistent shadow and spacing.
- Editorial-candidate status may remain visible, but should not prevent a publication from having a proper cover.

## Implemented in this update

- Added a reusable helper script for cover rendering.
- Added a formal cover set for *Conversations of Chance*.
- Updated the home page, Library page and publication page to use the real cover.
- Updated publication metadata so companion and letter pages can use their own `og:image` values.

## Next recommended step

When *The Little Book of Possibilities* and *The Parables of Chance* are drafted, create their covers from this same system rather than designing them independently.
