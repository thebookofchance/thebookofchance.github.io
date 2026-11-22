# Book of Chance — Update Only v0.23: Questions About Chance

**Base:** Existing v0.22 website (public vocabulary update)
**Patch type:** Add/replace only; do not delete other repository files.

## Installation

Extract this ZIP into the **root of your existing** `thebookofchance.github.io` repository. Preserve folder paths and replace matching files. Do **not** upload a containing parent folder or overwrite your current form settings. Commit/push the changed files and verify GitHub Pages deployed.

## What changed

- New `questions/` reader page for *Questions About Chance*, with 26 questions in five themes, local-only search, expandable answers, and PDF/EPUB links.
- Original FAQ revised to editorial candidate v0.3, with a simulated reader review and explicit RC2 source references.
- Proposed editorial cover (not yet H-approved) in three web/print formats; 17-page PDF and EPUB proof.
- Quiet links from homepage, Library, About and the Beginner's Guide. **The Library still counts nine books/essays; the FAQ is a separate reader resource.**
- Canonical FAQ Markdown/JSON, reproducible scripts and updated roadmap, source manifest and QA report.

## Not changed

No changes to `assets/forms-config.js`, the existing publication PDFs or EPUBs, private journal responses, registration, donations, membership policies, logo, or main book covers. No new analytics or external search service.

## Staging status

The FAQ is visible to anyone with the URL once uploaded; `noindex,follow` only requests search engines not to index it. It is *not* access control. H wording/cover approval, independent human reading, accessibility testing and live verification are pending. Proposed Council, membership, mentorship, charity and hardship assistance have **not** launched.

## Post-deployment quick check

1. Visit `/questions/`, open Question 7, try searches for `prayer` and `donations`, select `Faith` and `Fellowship` filters, then clear.
2. Check PDF and EPUB downloads open and the guide/Library/Home/About links resolve.
3. Try narrow mobile width, keyboard Tab/Enter, and dark mode.
4. Confirm the site shows correct proposed-service status and that the existing forms still work, without submitting sensitive information as a test.
5. Do not remove `noindex` or describe the cover as approved until formal sign-off.

## Builders

```bash
python scripts/build_questions_faq.py  # only if FAQ manuscript changes
python scripts/build_site.py           # regenerate HTML from sources
```
