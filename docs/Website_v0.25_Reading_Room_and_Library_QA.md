# Website v0.25 — Reading Room and Library Refinement

**22 November 2026 · Update-only patch over v0.24**  
**Status:** Locally tested; staging candidate, not independently live-verified.

## Why this update exists

Reader feedback identified four issues: (1) web reading felt like navigating disconnected pages without a clear page indicator, (2) the Library lacked the experience of an interactive online shelf, (3) Guided Reading Journey entry was difficult to discover, and (4) white covers against a white site created a visually monotonous catalogue.

## Delivered

- **Paginated Reading Room (`reader/`)**: one reading environment for the nine existing literature titles. Content is extracted at build time from their canonical website readers. There are 130 navigable *sections*, including 24 of the foundational book. Actual CSS column pagination calculates page counts at each viewport and text size. The interface displays `Page X of Y` and `Section X of Y`, with next/previous page controls, table of contents, title switcher, adjustable text size, keyboard pagination, responsive layout and links back to the original page.
- **Reading place**: section/page and font setting saved to this browser's local storage only, without accounts or remote data collection. A visible *Forget my reading place* control removes the selected title's saved position. No site analytics or reader activity is collected by the feature. Page numbers are **per section**, not fixed-print or total-book pagination; they change with display width and text size.
- **Library shelf (`downloads/`)**: nine existing publication cards now sit in a warmer, contrasting, six-tone neutral shelf presentation with readable covers, more depth and an explicit *Read in eReader* link. Cover image files remain **unchanged** and retain their original versions and approvals. Existing web reader, PDF and EPUB actions are preserved.
- **Reading Paths**: the Reading Journey is promoted in the homepage's primary action row and appears in a prominent dark Library entrance panel above the longer catalogue. Existing Journey content and links remain unchanged.
- **Resilient build**: `scripts/v025_library_reader.py` regenerates both the reader content and Library integration after the existing v0.24 build. The reader is tagged `noindex,follow` and excluded from the sitemap to avoid duplicate-content indexing. The site does not introduce a new publication or remove existing editorial-candidate labels.

## Validation performed

1. All nine titles and 130 sections loaded from canonical site HTML; a normalized-text comparison against each article or main-book section found no missing/modified textual content.
2. Local browser interactive tests at **1440, 900, 390 and 320 px**: page previous/next, longer-story pagination, section navigation, changing books and font size, desktop/mobile layouts, theme controls and Library category filtering. No horizontal overflow at these four widths.
3. A longer fiction chapter displayed **six pages** at desktop width, **twelve pages** at 390 px and **sixteen pages** at 320 px; actual CSS page movement was verified.
4. Simulated local-storage test: reading position saved on page turn; clearing a title's position removes it; a new page turn resumes saving. All nine title selectors loaded readable content.
5. Static repository audit: **45 HTML pages, 1,366 internal references, zero unresolved local destinations/anchors**; JavaScript syntax checked. Verified 19 bundled PDFs open, and 11 bundled EPUB archives have no corrupt members.
6. Rebuilt the website repeatedly with `scripts/build_site.py`. The reader stays `noindex`, is omitted from `sitemap.xml`, and all original nine catalogue entries remain present.

## Not changed / not claimed

- No canonical manuscripts, published text, original PDF or EPUB bytes, approved cover files, website form configuration, privacy practices, community status or donations changed.
- This is not an approval or reclassification of any editorial candidate. The founder's literature-review workflow continues separately.
- No independent cross-browser audit, screen-reader evaluation or real e-reader device compatibility test is claimed. CSS column layout may need a follow-up for edge cases involving unusually large illustrations or exceptionally long unbreakable links.
- Live GitHub Pages deployment, reader behaviour on external networks and the form submission endpoints have not been independently checked in this local pass.
- A complete visual redesign of the covers was deliberately deferred until the user has reviewed the literature and corresponding artwork. The shelf backgrounds alone are intended to address the immediate white-on-white presentation problem.

## Deployment

Overlay `Book_of_Chance_Website_Update_Only_v0.25.zip` onto an up-to-date **v0.24 repository** at its root. Keep existing files that are not in the patch. Do **not** delete publications or replace `assets/forms-config.js`.

After GitHub Pages deploys, verify `downloads/`, `reader/?book=book-of-chance`, `reader/?book=parables`, a longer paginated chapter on mobile, `journey/`, dark mode, and the two existing interest forms. Confirm no newly staged work appears in search engines before its review is complete.
