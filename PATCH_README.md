# The Book of Chance — Website v0.10 Update Only

**Base required:** the v0.9 website (with any subsequent working Formspree endpoint settings preserved).

## What this patch adds

- A proposed **Book of Chance Publications Standard v1.0-RC1** in Markdown and PDF.
- A detailed publications release order and progress register, including the owner's one-at-a-time sequence and deferral of videos/YouTube until the literature programme is complete.
- **Letters from H** index at `letters/`.
- **Letter No. 01 — On the People We Never Meet**, complete web edition + 10-page PDF and EPUB + original cover.
- New promotional blocks for this first Letter on the Library and homepage, new styles and sitemap routes.
- Source manuscripts, metadata, reproducible publication build scripts and a documented release QA report.

**No required user account or payment:** the whole Letter is readable on the website and downloadable for free. The Letter does not represent a launched fundraising, Fellowship membership or charitable programme.

## Installation

1. Unzip the update.
2. Upload the files and folders *inside* the ZIP to the same paths in your GitHub Pages repository, replacing only matching files.
3. **Do not delete other website files.** Do not replace your live `assets/forms-config.js`; it is intentionally excluded.
4. Check `/letters/`, `/letters/on-the-people-we-never-meet/`, homepage and Library on desktop and mobile.
5. Download/open the PDF and EPUB on at least one real device. Confirm both interest forms still work.
6. Review and approve the editorial standard and Letter before treating version 1.0 as formally released. The files are staged at an editorial candidate status.

## Safeguards

- The approved circular website emblem and both original book covers and manuscripts are unmodified.
- The four journals, original reader downloads and both Formspree lists remain unchanged.
- No donation button, membership payment, charity wheel or book preorder was added.
- Direct local-browser navigation was blocked in the build environment; a 12-case inlined-browser layout review at 1365/768/390 px passed. Live deployment and device checks remain pending.

## Maintaining the publication series

Edit `source/letters/001-on-the-people-we-never-meet.md` (not the generated HTML). Then run:

```bash
python scripts/build_site.py
```

The generator builds the Letter PDF/EPUB/cover and both series pages as part of the regular website build. Rebuilding PDFs/EPUBs locally requires the Python packages in `scripts/requirements.txt` plus the **Pandoc command-line application** on the PATH. Website visitors need none of these tools. Publication standards, status, version and future titles are recorded under `docs/` and `source/letters/catalogue.json`.
