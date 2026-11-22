# The Book of Chance Website — v0.9 update-only patch

**Upload these files to your existing GitHub Pages repository**, preserving the folders and replacing matching paths. Do not delete anything else from the repository. This is **not a full-site ZIP**.

## This update contains

- Refined 48-page **Reflection Journal**, now with matching Light and Dark editions (same interior)
- New 40-page **Daily Reflection Journal** and 40-page **Possibility Journal**, with distinct reflection practices
- Redesigned 48-page printer-oriented layout study (not a commercial print master)
- New cover previews under `assets/journals/`
- Updated `/downloads/`, `/reflect/`, homepage journal copy and journal collection catalogue
- PDF generation source, website overlay and automated verification script
- Publishing design / physical edition notes and website development log

## This update does NOT include or alter

- `assets/forms-config.js` or any Formspree identifiers
- The approved site logo and favicon
- The foundational book's EPUB, PDF, illustrations, cover images or manuscript
- Any other unchanged HTML pages

## After upload

1. Visit `/downloads/` and test all four journal buttons.
2. Visit `/reflect/` and verify that the journal feature and PDF worksheet links work.
3. Confirm that both Formspree lists still work and that the site logo is unchanged.
4. Open a new journal in a PDF reader with form support, type an innocuous sample entry, save, close and reopen it.
5. Check actual mobile/desktop display; only source-level/static verification is claimed for v0.9.

## Rebuild

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_reflection_pdfs.py
python scripts/build_site.py
python scripts/audit_v09.py
```

The journaling resources remain free and private by default. No paid hardcopies, donation flows or fundraising elements are added. The current print-oriented proof is not approved by any printer.
