# Website v0.24 — Guided Reading Journey development and QA

**Date:** 22 November 2026  
**Base:** Website v0.23 *Questions About Chance*  
**Scope:** One new navigational reader resource, quiet discovery links, a source-driven build module and a small CSS/JS layer. No literature text was edited.

## Design and content

- Eight independent reading paths: Begin with the ideas; Uncertainty and hope; Fairness and circumstance; Choices and consequences; Learning and growth; Connection and generosity; The wider living world; Belief and the unknown.
- Each path has three direct links to **specific** existing reading pages, chapters, stories or FAQ questions, plus an optional private reflection prompt.
- The source catalogue is `source/resources/guided-reading-journey.json`. All 24 destinations and chapter/answer fragments are verified against generated pages during build.
- No scoring, registration, questionnaire, user profile, external API, analytics or browser-storage of route selections or progress. Checkmarks last only while the page remains loaded, and reset upon refresh. Opening a reading in a labelled new tab allows the path to remain open.
- On browsers without JavaScript, all eight route sections remain readable and ordinary anchor links continue to work.
- All linked literature keeps its existing editorial-candidate or final-source status; the journey itself is staged with `noindex,follow` and excluded from the sitemap until the wider release review.

## Test record (local and automated)

| Test | Result |
| --- | --- |
| Eight paths, twenty-four targeted destinations and HTML anchors | Passed build validation |
| Whole-site static HTML references, paths and section anchors | **44 HTML files / 1,550 internal references / zero missing** |
| JS and Python syntax | Passed (`node --check`, Python compile) |
| Browser route selection and deep-link logic | Route selection passed; inlined-browser rendering tested (direct local navigation blocked by environment) |
| Progress toggle, reset, choose another route | Passed |
| No-JavaScript fallback | Eight routes remain visible, tested |
| Mobile menu and theme toggle | Passed at 1440, 900, 390 and 320 px viewports |
| Responsive overflow | None at the four viewports tested |
| Existing Library filters and FAQ content | Passed regression tests |
| Site rebuild from canonical sources | Passed |
| Live GitHub Pages deployment and interest-form delivery | **Not tested; owner/deployment verification required** |
| Independent accessibility/screen-reader/e-reader testing | **Outstanding** |

## Files and maintenance

- `journey/index.html` — generated page (do not edit as primary source)
- `source/resources/guided-reading-journey.json` — canonical path selection and copy
- `scripts/v024_reading_journey.py` — integration, anchor validation and HTML rendering
- `assets/journey.js` — optional local progress/state enhancements
- `assets/site.css` — scoped responsive styling
- `scripts/audit_journey_v024.py` — site-wide path and anchor validation
- `scripts/build_site.py` — runs v024 following v023
- Homepage, Library, original book contents, FAQ and Beginner's Guide receive short, relevant links

**Run:** `python scripts/build_site.py`, then `python scripts/audit_journey_v024.py`. Exported books and the original canonical texts are unaffected.

## Release stage and next task

Staging does **not** constitute final literature approval. Proceed with the complete per-title audit in `docs/Literature_Release_Approval_Checklist_v0.24.md` before removing any editorial-candidate labels or `noindex` flags, and verify the new site on live GitHub Pages after deploying the update-only ZIP.
