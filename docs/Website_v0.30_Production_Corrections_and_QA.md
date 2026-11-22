# The Book of Chance — Production Corrections and QA v0.30

**Date:** 23 November 2026  
**Baseline:** Reconstructed v0.28 website and the Literature Release Readiness Audit v0.29  
**Scope:** Production repairs only. All publication text, status labels, author review notes and existing search-engine restrictions are deliberately preserved.

## Delivered corrections

### 1. Approved main-book cover
- The newly approved **braided trajectories** cover is the canonical **Light Edition** front.
- The existing **Dark Edition** cover remains unchanged as the second visual choice. This avoids inventing an unapproved dark counterpart.
- The Light Edition source cover, website WebP/JPEG derivatives, embedded EPUB front cover and PDF front cover are updated to match.
- The main book's two PDFs are regenerated directly from their semantic HTML sources as single documents. This removes the need to stitch a separate untagged cover into the PDF.

### 2. PDF production and metadata
- All **11 PDF editions** have been rebuilt from the source manuscript/layout pipeline, not by layering an image over the previous PDF front page. No old cover text remains extractable beneath those new front covers.
- All 11 have H as the PDF author, useful document titles and the `en-NZ` document language. The seven previously missing author fields are corrected.
- WeasyPrint 68.0 generated **tagged PDF/UA-1 export candidates** with a PDF structure tree, marked-content designation and XMP PDF/UA-1 identifier. All 11 passed structural tag checks and include cover artwork from the approved library.
- The main-book PDFs now have **113 pages**, rather than 114: an unnecessary parity blank page was eliminated. Text-extraction checks found no manuscript word loss (21,583 tokenised words before and after in the two main-book PDFs). Other editions preserve their existing PDF page counts.

**Accessibility qualification:** Structural PDF tags and an XMP identifier do **not** establish that the files are fully accessible or that PDF/UA compliance has been independently certified. No formal veraPDF validation or hands-on NVDA, VoiceOver or TalkBack reading-order testing was completed. Those remain release gates. The existing HTML and EPUB alternatives remain available.

### 3. Reproducible approved-cover builds
- Added `source/approved_cover_assets_v030.json`, holding SHA-256 hashes of all eleven canonical front covers.
- Added `scripts/approved_cover_assets.py` to verify the cover inputs before export; individual publication builders now consume these covers rather than regenerate older artwork.
- Updated the Letter 01–03, Five Values, Conversations, Possibilities, Parables, Beginner's Guide, FAQ and main-book build scripts. The legacy Conversations visual-system entry point now refuses to overwrite the approved cover.
- Added `scripts/pdf_release_metadata.py` and `scripts/verify_literature_production_v030.py` for reproducible metadata and QA verification.

### 4. Website navigation and cover descriptions
- Corrected the obsolete Library **Reading Paths** shortcut in its source generator, so a standard website rebuild preserves the working `/journey/` link.
- Refined cover alternative-text descriptions in the relevant source templates to reflect the large H lettering on *Letters from H* and the approved FAQ cover.
- Corrected the main Light cover's declared image width for its current proportions.

## Verification results

| Test | Result |
|---|---|
| PDF/EPUB edition pairs | **11 / 11 found** |
| PDF author metadata | **11 / 11 = H** |
| Tagged PDF structure and PDF/UA-1 export identifier | **11 / 11 found** (not certification) |
| Stale extractable cover-page text | **0 / 11** |
| EPUB integrity and embedded cover-pixel match | **11 / 11 passed** |
| Public website HTML files scanned | **45** |
| Public internal references checked | **1,615** |
| Broken public references | **0** |
| Public anchor references checked | **246** |
| Broken public anchors | **0** |
| Canonical manuscript Markdown files modified | **0** |
| Publication `editorial candidate` / `noindex` statuses changed | **0** |
| Standard website rebuild | **Passed** |

The updated covers were visually checked in a contact sheet showing all eleven PDF front covers. No obvious clipping or missing cover artwork was found in those previews. The PDF/EPUB text matching is a structural comparison rather than an independent literary or specialist rereading.

## Remaining release gates

1. Conduct actual screen-reader and ebook-device tests, and obtain an independent PDF/UA conformance assessment if these PDFs are to be advertised as accessible PDFs.
2. Final title-specific editorial approval and any independent human/specialist review required by the release checklist.
3. Live GitHub Pages and real interest-form submission tests after deployment.
4. Only after the release gates are addressed, update publication proof labels, source end matter, `noindex`, metadata and sitemap entries through a separate, explicitly approved release patch.

## Update-only ZIP installation

Extract the v0.30 ZIP at the root of the existing GitHub repository over **v0.28**, preserving folder structure and replacing matching files. **Do not delete unchanged repository files.** The patch includes no form configuration. It is not a full-site export.

A fresh build can be run with `python scripts/build_site.py`. To inspect the production metadata and cover registry, run `python scripts/verify_literature_production_v030.py` in a development environment with the listed Python dependencies. Individual publication-build scripts remain available for future intentional re-export.
