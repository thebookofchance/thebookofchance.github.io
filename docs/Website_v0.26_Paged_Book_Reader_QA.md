# The Book of Chance — v0.26 Paged Book Reader and QA

**Scope:** Improve the existing `/read/<section>/` reading pages in response to reader feedback. The v0.25 multi-publication `/reader/` remains available and unchanged.

## User-reported problem

Readers found the narrow 2 px progress bar at the top of original Book of Chance chapters hard to see. It disappeared as they scrolled, and readers did not know what page they were on. They wanted to turn pages rather than scroll a long article.

## Implemented

- Removed the original scroll-progress bar from all 24 web sections of *The Book of Chance*.
- Added one viewport-sized reading page at a time with a paper-like layout.
- Added persistent **Page X of Y** and **section percentage** text at the bottom of the reading panel. Progress increases when a page is turned; it does not use scroll distance.
- Next/previous buttons turn pages and move to adjacent sections at section boundaries.
- Readers can also use left/right arrow keys, Page Up/Down, and horizontal touch swipes.
- Preserved A−/A+ font sizing, chapter bookmarks, the existing Table of Contents, dark mode and navigation.
- Saved the last page of each section only in the current browser's local storage, with no login or remote transmission. Page numbers adapt to viewport size and font size, so they are **web pages**, not canonical printed edition page references.
- Left all 24 original chapter bodies in the HTML. Without JavaScript the text remains readable in the existing scrolling layout.
- Preserved all source manuscripts, publication statuses, PDF and EPUB files, approved artwork, and form configuration.
- Added a build-stage module `scripts/v026_book_paging.py`; generated pages and CSS/JS reproduce after the normal site rebuild.

## Local verification

- 24/24 generated book sections tested at **1440 × 900**, **390 × 844** and **320 × 710**; the introduction and longer reading tested at **900 × 850** as well.
- Checked visible page count, non-scrolling body, absence of horizontal overflow, no oversized illustrated figures, no unexpected JavaScript errors, and content still present in the reading body.
- Introduction: **4 pages at desktop**, **6 at 390 px mobile**, **8 at 320 px mobile**. Page counts vary based on typography and device dimensions.
- Long reading *Arrival*: **7 pages at desktop**, **11 at 390 px mobile**, **15 at 320 px mobile** in the tested conditions.
- Verified next/previous page controls, text-size re-pagination, per-section position restoration using a mocked same-device storage implementation, dark mode, mobile navigation, and keyboard page turning.
- Confirmed no-JavaScript fallback leaves all the source text accessible by scrolling.
- Validated `assets/book-pages.js` and `assets/site.js` with `node --check`.
- Rebuilt the site with `python scripts/build_site.py` and confirmed all 24 paged sections and exactly one v0.26 CSS ruleset are generated.

## Remaining live checks

This is a **local browser verification**, not an audit of the hosted GitHub Pages site. After deployment, test the chapter page-turn and section-transition links, saved reading position across a reload, image loading, desktop/mobile browser differences, keyboard focus and voice/screen-reader experience on actual devices. In particular, local browser security restrictions required inlining the website files for testing; the reader's storage was mocked to test restoration. No formal accessibility certification is claimed.

## Release status

This interface update does **not** approve any editorial candidate, remove publication disclosures, alter indexing flags, or substitute for the scheduled literature approval review.
