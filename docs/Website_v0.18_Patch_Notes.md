# Book of Chance Website — v0.18 update-only patch

**Edition:** 22 November 2026  
**New publication:** *The Little Book of Possibilities*, editorial candidate v0.2

This patch adds the book to the homepage and Library, creates a complete online reader, and supplies the approved cover (SVG/PNG/WEBP), the 42-page PDF reading proof, the EPUB, and source materials. It extends the established visual publishing system without replacing the foundational book or the previous publications.

## How to install

Extract the update-only ZIP and upload **its contents** into the root of your existing GitHub Pages repository. Maintain the existing relative folder structure. Replace files with matching paths; keep every unrelated existing file.

This is a patch against the previous website update (v0.17). **Do not delete any files or re-upload the full website as a replacement.** The `assets/forms-config.js` and accepted logos were not changed.

## Paths to check after deployment

- `/` — newest companion feature
- `/downloads/` — new Library card and downloads
- `/booklets/the-little-book-of-possibilities/` — complete online reader
- `/files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.pdf`
- `/files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.epub`

## Editorial status

The book cover is approved. The manuscript remains an **editorial candidate** awaiting the author's sign-off, independent human reading and formal accessibility checks. The new HTML page carries `noindex,follow`, as with earlier unapproved editorial candidates. The Fellowship's proposed services have not been represented as operational.

## Build and verification

- Canonical manuscript: `source/booklets/the-little-book-of-possibilities.md`
- Source-driven site integration: `scripts/v018_possibilities.py` (wired into `scripts/build_site.py`)
- PDF/EPUB reproduction script: `scripts/build_possibilities.py`; it verifies the approved cover hash rather than regenerating artwork
- Integration checks: `docs/Website_v0.18_Possibilities_QA.json`

Live deployment checks and physical-device ebook compatibility should be completed after uploading.
