# The Book of Chance — Website Update-Only v0.24

**Base:** The existing v0.23 website with Questions About Chance.  
**Update:** Guided Reading Journey — a source-driven navigation resource for newcomers.  
**Patch type:** Add/replace only. Do not delete existing website files.

## Install on GitHub Pages

1. Extract this ZIP locally.
2. Upload the **contents** of the extracted folder to the root of the existing `thebookofchance.github.io` repository. Keep folder paths exactly as supplied. Do not upload a separate parent folder.
3. Replace files with matching names. Do **not** delete any other files.
4. Commit and allow GitHub Pages to redeploy.
5. Visit `/journey/`, choose a theme, follow its three readings, mark one as explored, reset it, switch themes, and test dark mode and mobile navigation.
6. Verify the links in the homepage, Library, Beginner's Guide, FAQ and main book contents. Confirm the forms and all existing books still work on the live site.

## Contents of the update

- `journey/index.html`: responsive, cover-led Guided Reading Journey with eight themes and 24 verified stops.
- `source/resources/guided-reading-journey.json`: editable theme and reading route catalogue.
- `scripts/v024_reading_journey.py`: reproducible website integration and chapter-anchor validator.
- `assets/journey.js`: temporary page-only progress, route selection, reset and deep links. No answers stored or sent.
- `assets/site.css`: scoped styles for the new reading journey.
- Quiet discovery links added to the homepage, Library, Beginner's Guide, FAQ and main book contents.
- Updated website/roadmap metadata, QA documentation and release-approval checklist.

## What this patch does not do

- It does **not** rewrite literature, PDF/EPUB exports, approved covers, founding documents, the form configuration or any membership/financial policies.
- It does **not** remove editorial-candidate or proof labels, or index draft publications. The new journey is also staged `noindex,follow` until release review.
- It does **not** introduce accounts, a quiz, scores, analytics, new storage or an external API.

## Next, as agreed

Perform the **per-publication release approval audit** described in `docs/Literature_Release_Approval_Checklist_v0.24.md`. Only change a given work's editorial-candidate notes, search indexing, edition labels and publication metadata after its actual editorial, cover, accessibility and live tests are complete and H has approved it.

## Rebuild and audit

```bash
python scripts/build_site.py
python scripts/audit_journey_v024.py
```

Live GitHub Pages and interest-form behaviour must be tested after deployment; local build and simulated browser checks are not substitutes for live verification.
