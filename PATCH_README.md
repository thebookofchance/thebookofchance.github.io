# Website v0.12 — Update-only patch

**Purpose:** Add *Letters from H — No. 02: When Good Choices Lead to Bad Outcomes* to the existing website. Requires v0.11 as the starting point.

## Installation

1. Download and extract the v0.12 ZIP.
2. Upload only the files and folders inside the archive to the root of your existing GitHub Pages repository, preserving folder paths.
3. Choose **replace** for existing same-named files; **do not delete** other files or your working Formspree settings.
4. After GitHub Pages updates, verify `/letters/`, `/letters/when-good-choices-lead-to-bad-outcomes/`, the Library downloads and the two existing interest forms.
5. Review and approve Letter 002's content before regarding it as a final author-approved edition.

## Contents and boundaries

- New complete Letter 002 PDF, EPUB, source Markdown and custom vector/website cover.
- New full HTML reading page, updated homepage, Letters archive and Library.
- Updated metadata, sitemap, issue-aware publication scripts and editorial/QA/change documents.
- **No** logo changes, existing book/journal files, Formspree configuration, backend, membership activation, donations or fundraising.

## Important distinctions

The website documents label the Letter an **editorial candidate** pending H's approval. The PDF/EPUB/HTML are made available for review and potential deployment, but not declared formally released.

If you later edit Letter 002, update its canonical Markdown source and regenerate the PDF/EPUB with `python -c "import sys; sys.path.insert(0, 'scripts'); from build_letters import build_letter_002; build_letter_002()"` from the website root, then run the site builder. Normal site builds do not regenerate Letter 001's PDF or EPUB.
