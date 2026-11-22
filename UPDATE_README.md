# The Book of Chance — Website Update Only v0.17

This ZIP contains **only additions or modified files** compared with the full
`thebookofchance.github.io-main.zip` repository you uploaded. There is no
full repository copy and there are no build cache files.

## Installation on GitHub

Extract the ZIP and upload its files into the **root of your existing website
repository**, keeping their relative directory names. Replace files with the
same path. Do NOT delete any other files. Your existing forms configuration
and the rest of your repository should be left untouched.

## Included improvements

- Publication visual design system guide, reusable cover generation script,
  and Conversations of Chance cover assets in SVG, PNG and WEBP.
- Rebuilt Conversations of Chance PDF (**53 pages**, including the cover) and
  EPUB (cover embedded).
- Updated homepage, Library and Conversations reading page.
- Updated publication-specific social cover metadata, source catalogue,
  build scripts, roadmap and site manifest.

## Notes

- Conversations of Chance remains an editorial candidate; this patch does
  not indicate human sign-off, print readiness, or live deployment checks.
- The historical v0.1 filename remains unchanged so existing download links
  continue to work; upload both revised files to replace those downloads.
- This patch was generated as a byte-for-byte difference against the
  repository ZIP provided by the user, excluding temporary build artifacts.

## Changed files

- MODIFIED: `SITE_CONTENT_MANIFEST.json`
- ADDED: `assets/publications/conversations-of-chance-cover.png`
- ADDED: `assets/publications/conversations-of-chance-cover.svg`
- ADDED: `assets/publications/conversations-of-chance-cover.webp`
- MODIFIED: `assets/site.css`
- MODIFIED: `booklets/the-five-values/index.html`
- ADDED: `docs/Publication_Visual_System_v1.0.md`
- MODIFIED: `docs/Publications_Roadmap_and_Progress.md`
- MODIFIED: `downloads/index.html`
- MODIFIED: `files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.epub`
- MODIFIED: `files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf`
- MODIFIED: `index.html`
- MODIFIED: `letters/on-the-people-we-never-meet/index.html`
- MODIFIED: `letters/what-do-we-owe-to-strangers/index.html`
- MODIFIED: `letters/when-good-choices-lead-to-bad-outcomes/index.html`
- MODIFIED: `publications/conversations-of-chance/index.html`
- ADDED: `scripts/build_conversations.py`
- MODIFIED: `scripts/build_site.py`
- ADDED: `scripts/publication_visual_system.py`
- MODIFIED: `scripts/v010_publications.py`
- MODIFIED: `scripts/v012_second_letter.py`
- MODIFIED: `scripts/v013_third_letter.py`
- MODIFIED: `scripts/v015_five_values.py`
- MODIFIED: `scripts/v016_conversations.py`
- MODIFIED: `source/publications.json`
