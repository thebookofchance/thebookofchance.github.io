# Book of Chance Website v0.7 — Changed-files patch

This is **not** a complete website export. It contains **only files created or modified since v0.6**.

## Install on GitHub Pages

1. Extract the ZIP locally.
2. Upload **the contents** (including folders such as `read`, `reflect`, `focus`, `assets`, `source`, `docs` and `scripts`) to the root of your *existing* `thebookofchance.github.io` repository.
3. Overwrite files with matching names. **Do not delete any other files already in the repository.**
4. Keep the existing `assets/forms-config.js` from your working live site. **It is intentionally not in this ZIP.**
5. When GitHub Pages finishes publishing, test Home, Reflect, Fellowship, Library and Current Focus, and test the two existing registration forms.

## Most important changes

- Fellowship registration CTA now visible in the first screen.
- Three programme-card icons redesigned in a consistent line-art style.
- `reflect/` provides a private reflection editor, a 12-question weekly cycle and three downloadable practice sheets.
- `focus/` explains the current organisational goal, roadmap and deferred chance-based charity campaign concept.
- Home and Library direct readers to usable activities and resources.
- Sitewide navigation, social metadata and sitemap updated.
- `docs/Website_Development_Log.md` records changes, decisions, status and future maintenance tasks.

## What isn't included

Book manuscripts, PDF/EPUB editions, cover files, logo, image assets and **Formspree endpoints** have not been changed or included.

There is **no active donation campaign**, paid membership or live charity wheel. The Fellowship remains in development; ordinary membership is intended to be free.

## Testing

The local source passed 919 link and asset checks and 15 inlined Chromium visual tests. Automated HTTP navigation to localhost was blocked by the test environment; the deployed website and live form delivery still need checking.

Full change history and next steps: `docs/Website_Development_Log.md`.
