# The Book of Chance — Website v0.7

A static, GitHub Pages-ready website for the free illustrated *Book of Chance*, private reflection practices, downloadable resources, and the proposed Fellowship of Chance.

**Public site:** https://thebookofchance.github.io/  
**Website release:** v0.7 (22 November 2026)

## Site structure

| Destination | Purpose |
| --- | --- |
| `/` | Book-led homepage, weekly reflection entry and current focus |
| `/read/` | Entire book: twelve readings, sections, notes and original illustrations |
| `/reflect/` | Private guided reflection editor, weekly question rotation and offline guides |
| `/downloads/` | Free Light/Dark EPUB and PDF editions, plus three downloadable templates |
| `/community/` | Proposed Fellowship, reasons to participate, future funding principles and a Fellowship interest form |
| `/focus/` | Current organisational development goal, roadmap, potential funding criteria and deferred Chance Campaigns |
| `/print/` | Planned physical editions and a **separate** print-interest form |
| `/about/` | Philosophy, book and author information |
| `/privacy/` | Formspree interest-list and private reflection privacy information |

## Honesty about what exists

- **Available today:** The complete free book, two cover editions, private reflection workspace, three text templates, a rotating archive of twelve questions and two interest registration forms (once the owner's Formspree endpoints are configured on the live site).
- **Not yet operating:** Formal Fellowship membership, active mentorship, local Fellowships, practical hardship assistance, scheduled events, charitable fundraising, payments, book orders or a real charity selection wheel.
- **Ordinary future membership is intended to be free.** Giving is voluntary and cannot purchase luck, influence or priority support.
- The founder reports that the two live Formspree interest forms work; private submissions and actual endpoint configuration were **not independently verified** in this release.
- Readers do not need to register or donate to read or use any current resource. The existing interest forms request adult (18+) confirmation for the Fellowship, while the reading site remains publicly accessible.

## Deploy update-only ZIPs

The `Book_of_Chance_Website_Update_Only_v0.7.zip` package contains changed and new files **only**. Extract it and upload its contents to the existing GitHub Pages repository, replacing files with the same paths and **without deleting other files**.

**Do not overwrite or publish private information.** `assets/forms-config.js` (the file containing your working Formspree endpoint identifiers and public contact email) has intentionally **not** been included or modified.

Check the accepted favicon/logo, both form flows and the `/reflect/` download feature after deployment.

## Edit and regenerate

- The canonical book source remains `source/manuscript.md`; do not edit generated `read/` pages directly.
- The available/planned publication catalogue is `source/publications.json`. It includes three downloadable practice guides as available resources.
- Weekly questions live in `source/reflection-prompts.json` and follow a repeating 12-week cycle starting Monday, 23 November 2026.
- The current goal, supporting page and homepage callouts are maintained through `scripts/v07_enhancements.py`.
- The site generator is `scripts/build_site.py`, which regenerates all 33 HTML pages and the sitemap. Its source reflects v0.7 additions.

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_site.py
python scripts/audit_v07.py
```

The generator does not generate or modify ebook editions, original artwork or the approved brand symbols. It also leaves existing form service configuration alone. Run a local web server (e.g. `python -m http.server 8000`) for normal browser testing outside a restricted environment.

## Project record

**`docs/Website_Development_Log.md`** is the canonical change log: all v0.7 additions, intentionally deferred features, testing boundaries and future maintenance instructions are recorded there.

`SITE_QA_REPORT.json` records the latest source checks and environmental limits. The inlined-browser visual tests passed across three sizes, but this does **not** replace checking the deployed website or testing live Formspree submissions.
