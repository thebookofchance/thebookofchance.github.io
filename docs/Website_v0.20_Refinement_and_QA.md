# Website v0.20 — Focused Refinement & QA

**Prepared:** 22 November 2026  
**Baseline:** v0.19 Parables integration  
**Scope:** Homepage publication discovery, Library navigation, visual clarity and safe reproducibility.

## Intent and design boundaries

Retain the distinctive *The Book of Chance* brand, Light/Dark cover hero, long-form reading pages and free/no-account access. Make the expanding collection easier to scan without representing editorial candidates as approved publications. No video work or platform expansion was started.

## Implemented

### Homepage

- Replaced five consecutive full-width promotion strips for Parables, Possibilities, Conversations, Five Values and Letter 03 with a **single, six-cell** cover-led section: five linked titles and one Library call-to-action.
- Kept the opening hero, core reading sections, reflection practices, Fellowship content, and physical-book planning content.
- Kept edition and release-status cues visible rather than adding fabricated reviews, sales language or active institutional claims.

### Library

- Retained the distinctive foundational book Light/Dark edition display and its existing deep-link anchor.
- Replaced five large feature panels with a compact, searchable **eight-title index**: five books (including the foundational book) and three Letters.
- Added Books/Letters filter buttons with `aria-pressed`; a title/topic search that performs all filtering locally without network calls or saved personal data; accessible result count and empty state.
- Preserved legacy anchors (`#parables-of-chance`, `#little-book-of-possibilities`, `#conversations-of-chance`, `#five-values-booklet`, `#letters-from-h`) so existing links remain valid.
- Kept journal and worksheet sections fully intact, with shortcuts to each. Removed the outdated planned-further-readings placeholder.

### Accessibility and publication status

- Updated global `--subtle` text contrast token: light `#56636b` vs `#fafaf7` = **5.92:1**; dark `#aab8c2` vs `#141a20` = **8.63:1** (calculated colour contrast only).
- Added text-labelled controls, visible keyboard focus, explicit category state, and a reduced-motion style for new cards.
- Preserved release gates: Parables, Possibilities and Conversations retain `noindex,follow` and are **not included in the sitemap**. No editorial approval is inferred.
- Existing reader interfaces, manuscript and ebook exports, search of the foundational readings, reflection pages and form configuration were not modified.

## Verification completed

| Check | Evidence / result |
|---|---|
| Local static HTML scan | 42 HTML files, 1,101 internal link occurrences scanned |
| Missing internal targets | **0** |
| Missing internal section anchors | **0** |
| New Library cards | **8 total**, 5 Books and 3 Letters |
| Filter and topic search | Browser DOM/JavaScript tests passed, including empty search state |
| Mobile menu and light/dark control | Browser DOM/JavaScript tests passed |
| Responsive widths | 1440, 820, 390 and 320 px; no document-level horizontal overflow |
| Image references | All card covers present in repository |
| JavaScript syntax | `node --check` passed for site and Library code |
| Original publication downloads | Byte-for-byte unchanged against v0.19 |
| Existing form settings | Byte-for-byte unchanged against v0.19; excluded from patch |
| Candidate indexing | `noindex` and sitemap exclusion preserved |
| Build step | v0.20 applied after v0.19 by `scripts/build_site.py` |

The two generic HTML warnings from the static scan concern an **internal typesetting output**, `_build_parables/typeset.html`, which has multiple `h1` elements and no `<main>`; it is not a public site page.

## Testing limitations and next gates

The runtime blocked direct Chromium navigation to both the local HTTP server and filesystem URLs. A browser DOM/layout test was therefore run by injecting the same site HTML/CSS/JavaScript and embedded image assets into an `about:blank` page. This can check new responsive rules and interactions, but **cannot establish a full live deployment, cache behaviour, GitHub Pages routing, Lighthouse scores, HTTP response headers, or form submissions**. No Formspree test message was sent.

Before starting public video promotion: confirm the v0.20 deployment in a normal browser, run a real mobile/menu and dark-mode check, download a PDF and EPUB, verify both interest forms with authorised test submissions, finish independent accessibility checks, and decide whether to approve the editorial-candidate manuscripts and remove `noindex`.
