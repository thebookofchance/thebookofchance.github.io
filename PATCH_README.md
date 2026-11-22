# The Book of Chance — v0.20 UPDATE ONLY

**Required base:** v0.19 website with *The Parables of Chance* integrated.
**Format:** Changed/new files only. Do not replace the whole repository.

## Install on GitHub Pages

1. Extract `Book_of_Chance_Website_Update_Only_v0.20.zip`.
2. Copy the contents of the ZIP directly into the **root** of your existing GitHub repository, preserving the paths. Replace matching files, but do not delete other files.
3. Commit the changes and let GitHub Pages deploy. Do not change the configured branch or publishing directory.
4. Check `/` and `/downloads/` on the live site with a hard refresh, then test on a phone.

The patch **does not include** `assets/forms-config.js`, original publication files, manuscripts, the theme script, or any interest-list endpoints.

## What changed

- Homepage: replaced five full-width book promotions with one compact, cover-led literary collection.
- Library: an index of all **eight publications**, including the foundational book, four additional book-length works and three Letters.
- Library browsing: local-only search by title/theme; filter All, Books or Letters. Journals and worksheets remain below the catalogue with prominent navigation shortcuts.
- Improved light/dark subtle text contrast and keyboard-visible filter controls.
- Removed the outdated placeholder for future readings from the Library.
- Preserved all existing publication reader routes, PDF/EPUB links, bookmarks, core book editions, and all legacy anchor targets.
- Rebuild-safe `scripts/v020_library_refinement.py` stage. Unapproved candidate pages remain `noindex` and excluded from `sitemap.xml`.

## Manual checks after deployment

- Home navigation and link to the Library, and all five small cover cards.
- Library search for “strangers” and an unmatched term, then All / Books / Letters filters.
- Jump from Library shortcuts to the foundational book, Letters, journals and worksheets.
- Mobile menu, light/dark toggle, and reading pages on both light and dark themes.
- At least one PDF and EPUB download in a real browser/device.
- Reflection workspace and the existing two interest forms, including consent and successful provider response, **only through an authorised test**.
- Confirm whether editorial candidate status and `noindex` are still intended before promoting the titles publicly.

## Limitations

Local browser interactions and layout were tested using injected HTML/CSS/JS because direct navigation to the local server was blocked by the testing environment. **This is not verification of the deployed GitHub Pages website or of Formspree delivery.** The patch does not mark any publication as formally approved.

See `docs/Website_v0.20_Refinement_and_QA.md` for details.
