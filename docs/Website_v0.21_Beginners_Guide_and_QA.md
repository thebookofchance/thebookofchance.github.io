# Website v0.21 — Beginner's Guide integration and QA

**Prepared:** 22 November 2026  
**Required baseline:** v0.20 website  
**Scope:** Publication staging; no new operational community features

## Scope and changes

- Added *A Beginner's Guide to Confluent Humanism* v0.2 to the collection with a complete nine-section online reader, 13-page PDF, EPUB, and unchanged v0.1 cover artwork.
- The homepage now promotes the guide through a small link near the hero and a “Start here” catalogue card, replacing the third Letter's homepage promotion rather than lengthening the grid. That Letter remains available in the Library and its own reading page.
- The Library now has nine publications: six books/companions and three Letters. Search terms and Books/Letters filters are preserved and have updated counts, and “Start here” is added to Library section shortcuts.
- The guide page provides a responsive reading layout with desktop table of contents, mobile expandable contents, and direct PDF/EPUB links.
- Added canonical manuscript, catalogue entry, build script, and a rebuild-safe `v021_beginner_guide.py` stage.
- No changes to existing form configuration, readership restrictions, membership status or donations. Candidate publication is `noindex,follow` and omitted from sitemap pending final approval.

## Verification

| Check | Result |
|---|---|
| HTML pages in local tree | 43 total including internal typesetting HTML |
| Local HTML link occurrences scanned | 1,152 |
| Broken local targets | 0 |
| Invalid fragment anchors | 0 |
| Guide online heading sections | 11 anchors (introduction + nine numbered sections + edition note) |
| Guide EPUB | ZIP integrity passed; cover packaged |
| Guide PDF | 13 pages, selectable text, author metadata H |
| Source assets | PDF, EPUB and all three cover formats byte-for-byte identical to reviewed v0.2 package |
| Browser interaction tests | Local-only title search, Books/Letters filter, theme switching, mobile menu and guide mobile TOC passed |
| Responsive widths | 1440, 820, 390 and 320 px; no horizontal overflow |
| Rebuild | `python scripts/build_site.py` passed with guide stage v0.21 |

**Known static audit warnings:** two findings concern `_build_parables/typeset.html`, an internal PDF-layout source (multiple `h1` tags and no `<main>`). This is not a public website page.

## Release gate and limitations

- The guide is approved for **web staging** in this workflow, not certified as final for public promotion. It remains an editorial candidate with `noindex,follow`.
- Simulated reading review is not independent human review. Screen-reader and e-reader hardware testing remain outstanding; PDF is not accessibility tagged.
- Local Chromium tests used injected HTML/CSS/JavaScript due restrictions on local HTTP navigation. They confirm layout and in-page behaviour but not live GitHub Pages routing, caching, search-engine indexing, actual PDF/EPUB download responses or third-party form delivery.
- No form endpoints or privacy settings were modified. Submit a test form only when authorised and in a live browser.

## Deploy / review

Copy the update-only ZIP contents into the root of the existing v0.20 GitHub repository; replace matching paths, do **not** delete unchanged files. After deployment verify the homepage “Start here” link, `/downloads/` nine-item catalogue, the guide's complete reading page, PDF/EPUB downloads, menu and theme behaviour on a phone, and site forms separately if authorised.
