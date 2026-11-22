# The Book of Chance — v0.26 Update Only

This ZIP contains **only new or changed files compared with v0.25**. It fixes the original *Read the book* experience shown in reader feedback: each chapter is now paginated rather than a continuous scroll.

## Installation

1. Extract this ZIP **into the root of your existing GitHub Pages repository**, where `index.html` lives.
2. Preserve the directory structure and replace the matching files.
3. **Do not delete** any other files. Do not change your existing `assets/forms-config.js` or contact/form settings.
4. Deploy on GitHub Pages, then open `/read/introduction/` and `/read/arrival/` to test on desktop and phone. Press Next/Previous, change text size, move to a new chapter and reload to confirm saved position.

## Changes

- Removes the top scrolling progress bar from all 24 original book chapter/section pages.
- Adds page-by-page navigation with a persistent **Page X of Y** label and per-page section progress; no whole-page scrolling in the interactive view.
- Preserves table of contents, original chapter links, text sizing, bookmarks and dark mode.
- Supports keyboard and touch, and retains a plain scrolling fallback when JavaScript is disabled.
- Keeps the existing multi-title Reading Room `/reader/` as-is.
- Adds `assets/book-pages.js` and the corresponding source/build styles/scripts so a site rebuild reproduces the changes.

**Not changed:** source texts, literature/approval status, PDF or EPUB editions, images, covers, reader publication count, forms and finance/community configuration.

Read `docs/Website_v0.26_Paged_Book_Reader_QA.md` for testing details and remaining live checks.
