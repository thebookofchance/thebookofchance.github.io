# The Book of Chance — Website v0.15 · Update-only patch

**Base required:** v0.14 already deployed to your GitHub repository. This package is not a full website. It contains only new or changed files, and does not contain your existing Formspree configuration.

## Installation

1. Extract this ZIP locally.
2. Upload its **contents** into the repository's existing root directory, preserving folders.
3. Replace matching files; **do not delete other existing website files**.
4. After GitHub Pages updates, test `booklets/the-five-values/`, the PDF and EPUB buttons, the Library card, and the new homepage link on mobile and desktop.
5. Confirm the logo and both Formspree registration forms still operate as they did before.

## What's new

- **The Five Values**, BOC-BKL-001, 1.0-RC1: ~3,500-word standalone introductory booklet by H.
- Complete open HTML reader with five-value jump navigation and clear PDF/EPUB download buttons.
- 17-page illustrated PDF, reflowable EPUB, original fine-line graphics and literary cover.
- Booklet featured on homepage and in the Library, catalogue and sitemap.
- Source, rebuild scripts, editorial review, quality report and updated development log/roadmap.

## Preserved

The original book (both editions), all three Letters, all journals/worksheets, agreed website emblem, and `assets/forms-config.js` remain **byte-identical** to v0.14. Formal Fellowship membership and donations remain closed; this release does not add fundraising.

## Important limitations

This is an **editorial candidate** pending H approval. It has been checked for source agreement, local link integrity, PDF layout and EPUB package structure. The website was visually smoke-tested using an **inlined Chromium render**, because the environment blocks direct local file navigation. We have not verified actual live hosting, mobile ebook readers, certified PDF accessibility or responses from human readers. The 6×9-inch PDF is a reader edition, not a commercial print-ready master.

See `docs/Five_Values_Editorial_Review_RC1.md` and `docs/Five_Values_QA_v0.15.json`.
