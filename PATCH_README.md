# The Book of Chance — v0.25 Update Only

This ZIP contains **only new or changed files compared with v0.24**.

1. Extract into the root of the existing GitHub Pages repository (the folder that contains `index.html`).
2. Preserve directory structure and replace matching files.
3. Do **not** delete other files. Do not alter `assets/forms-config.js` or your existing form settings.
4. Allow GitHub Pages to publish, then test the Library shelf, Reading Room and Guided Reading Journey on both desktop and mobile.

## Included features

- New `/reader/` with nine titles, page/section indicators, contents, chapter navigation, font sizing and browser-local reading place.
- Revised `/downloads/` shelf styling and `Read in eReader` entries, preserving existing links and download files.
- Reading Paths moved into the homepage's primary actions and placed prominently at the top of the Library.
- No cover redesign, manuscripts, PDF/EPUB revisions, form changes or changes to literature release approvals.

**Source:** `scripts/v025_library_reader.py` generates the reader data and integration when the website is rebuilt. `source/resources/v025-reader-styles.css` contains the additive styling.

**Review status:** The new reader page is deliberately `noindex` while it presents the same copyrighted text available on the canonical reading pages. Existing candidate status labels stay unchanged.

See `docs/Website_v0.25_Reading_Room_and_Library_QA.md` for the local test results and limitations.
