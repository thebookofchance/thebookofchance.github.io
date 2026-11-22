# Book of Chance Website Update v0.30 — Production Corrections

**Baseline:** Your existing v0.28 repository. This is an **update-only patch**.

## Installation
Extract the ZIP into the repository root, keeping folder structure and **replacing matching files**. Do not delete other repository files. No form config is included.

## Corrections
- New approved braided **Light Edition** cover in source, web thumbnails, PDF and EPUB. Existing Dark Edition cover remains in use.
- All 11 PDFs regenerated cleanly with author/title/language metadata and tagged PDF/UA-1 export structures; older cover text is not hidden underneath replacement images.
- Standalone publication builders now use hash-verified approved covers; older design generator functions are disabled.
- Corrected the persistent Reading Paths shortcut and updated cover alternative text in source templates.
- No manuscript or editorial-status changes. `noindex` and candidate notices remain in force.

**Note:** Tag generation is not a substitute for formal accessibility conformance checks or real screen-reader testing. See `docs/Website_v0.30_Production_Corrections_and_QA.md`.

**QA:** 11 PDF/EPUB pairs, 45 public HTML pages, 1,615 internal references and 246 anchors passed local structural tests. Live GitHub Pages verification remains outstanding.
