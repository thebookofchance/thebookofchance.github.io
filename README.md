# The Book of Chance — Website v0.21

A static, GitHub Pages-ready website for the free illustrated *Book of Chance*, private reflection practices, downloadable resources, and the proposed Fellowship of Chance.

**Public site:** https://thebookofchance.github.io/  
**Website release:** v0.23 — introductory guide staging and Library refinement (22 November 2026)

## Site structure

| Destination | Purpose |
| --- | --- |
| `/` | Book-led homepage, weekly reflection entry and current focus |
| `/read/` | Entire book: twelve readings, sections, notes and original illustrations |
| `/reflect/` | Private guided reflection editor, weekly question rotation and offline guides |
| `/downloads/` | Book editions, three Letters, new Five Values illustrated booklet, four journal editions and fillable worksheets |
| `/booklets/the-five-values/` | Complete illustrated text of *The Five Values* with direct PDF and EPUB downloads |
| `/booklets/the-little-book-of-possibilities/` | Companion book on conditions and accessible opportunities |
| `/publications/conversations-of-chance/` | Twelve-discussion companion for individuals and groups |
| `/publications/parables-of-chance/` | Twelve original fictional parables; staged final copyedit candidate v0.2.1 |
| `/publications/beginners-guide-to-confluent-humanism/` | Nine-section Beginner’s Guide v0.2; 13-page PDF proof, EPUB and full HTML reader; editorial candidate |
| `/questions/` | Questions About Chance: 26 searchable answers across five themes, with free PDF/EPUB proof downloads; editorial candidate |
| `/letters/` | Three standalone philosophical Letters from H, with online reading and PDF/EPUB downloads |
| `/community/` | Proposed Fellowship, reasons to participate, future funding principles and a Fellowship interest form |
| `/focus/` | Current organisational development goal, roadmap, potential funding criteria and deferred Chance Campaigns |
| `/print/` | Planned physical editions and a **separate** print-interest form |
| `/about/` | Philosophy, book and author information |
| `/privacy/` | Formspree interest-list and private reflection privacy information |

## Honesty about what exists

- **Prepared digital content:** The complete free book, three Letters, the new Five Values illustrated companion, two book cover editions, private reflection workspace, reflection journals, a rotating archive of twelve questions and two interest registration forms (once the owner's Formspree endpoints are configured on the live site).
- **Not yet operating:** Formal Fellowship membership, active mentorship, local Fellowships, practical hardship assistance, scheduled events, charitable fundraising, payments, book orders or a real charity selection wheel.
- **Ordinary future membership is intended to be free.** Giving is voluntary and cannot purchase luck, influence or priority support.
- The founder reports that the two live Formspree interest forms work; private submissions and actual endpoint configuration were **not independently verified** in this release.
- Readers do not need to register or donate to read or use any current resource. The existing interest forms request adult (18+) confirmation for the Fellowship, while the reading site remains publicly accessible.

## Deploy update-only ZIPs

The `Book_of_Chance_Website_Update_Only_v0.15.zip` package contains changed and new files **only**. Extract it and upload its contents to the existing GitHub Pages repository, replacing files with the same paths and **without deleting other files**.

**Do not overwrite or publish private information.** `assets/forms-config.js` (the file containing your working Formspree endpoint identifiers and public contact email) has intentionally **not** been included or modified.

Check the accepted favicon/logo, both form flows and the `/reflect/` download feature after deployment.

## Edit and regenerate

- The canonical book source remains `source/manuscript.md`; do not edit generated `read/` pages directly.
- The available/planned publication catalogue is `source/publications.json`. It includes free practice guides, the first three Letters and The Five Values as editorial candidate.
- Weekly questions live in `source/reflection-prompts.json` and follow a repeating 12-week cycle starting Monday, 23 November 2026.
- The current goal, supporting page and homepage callouts are maintained through `scripts/v07_enhancements.py`.
- The site generator is `scripts/build_site.py`, which currently regenerates 38 HTML pages and the sitemap. It incorporates the publication integrations through v0.15, including `scripts/v015_five_values.py`.

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_site.py
python scripts/build_reflection_pdfs.py
python scripts/build_five_values.py  # only when manuscript changes; before build_site.py
```

The routine site generator does not alter existing PDF/EPUB editions, the original book illustrations, or accepted brand symbols. The separate booklet builder intentionally regenerates its own cover, diagrams, PDF and EPUB after a source revision. It also leaves existing form service configuration alone. Run a local web server (e.g. `python -m http.server 8000`) for normal browser testing outside a restricted environment.

## Project record

**`docs/Website_Development_Log.md`** is the canonical change log: all v0.8 additions, intentionally deferred features, testing boundaries and future maintenance instructions are recorded there.

`SITE_QA_REPORT.json` records the latest source checks and environmental limits. The inlined-browser visual tests passed across three sizes, but this does **not** replace checking the deployed website or testing live Formspree submissions.


## v0.8 reflection release

- The Reflect page includes three complete clickable cards, in-page shortcuts and a browser print/save-as-PDF editor.
- The Library now contains a **48-page complete journal** (Light/Dark) and two focused **40-page companion journals**, alongside three fillable A4 worksheets.
- `scripts/build_reflection_pdfs.py` generates the PDFs; `scripts/build_site.py` builds the website and then applies the v0.8 page enhancements.
- `scripts/audit_v08.py` checks the 33 pages, references, JavaScript syntax and form-field presence.
- The journal print-layout proof is an editorial sample, **not** approved for commercial print distribution.
- Existing Formspree endpoints, logo and book files must be preserved when applying the update-only ZIP.

See `docs/Website_Development_Log.md` and `docs/Reflection_Journal_Production_Notes.md`.

## v0.9 journal series

- Main complete Reflection Journal — **48 pages**, in **Light and Dark** cover editions, with identical interiors.
- The Daily Reflection Journal — **40 pages**, a focused personal reflection practice.
- The Possibility Journal — **40 pages**, focusing on voluntary support, consent and boundaries.
- Four fully fillable journal PDFs, plus three separate A4 fillable worksheets and a non-fillable print-layout study.
- `scripts/build_journal_series.py` contains the series' reproducible contents and vector cover treatment.
- `docs/Journal_Series_Editorial_and_Print_Plan.md` explains the series and printer readiness gates.
- Digital editions are free and **no physical journals are on sale**.

The patch preserves the approved logo and live Formspree configuration. The owner must merge changed files into the existing repository without deleting unrelated files.

## v0.10 publications system and Letters from H

- The proposed editorial house standard is `docs/Publications_Standard_v1.0_RC1.md` (also supplied as PDF); its principles are derived from the published *Book of Chance* manuscript and approved cover family, with clearly noted recommendations and unresolved editorial decisions.
- The publication roadmap is `docs/Publications_Roadmap_and_Progress.md`; the owner chose **one new publication at a time**, with YouTube/video work following completion of the recommended literature programme.
- `Letters from H` is now at `/letters/`, with issue 001, *On the People We Never Meet*, at `/letters/on-the-people-we-never-meet/`. The entire essay is available as HTML plus PDF and EPUB download.
- Canonical source: `source/letters/001-on-the-people-we-never-meet.md` and its metadata `source/letters/catalogue.json`. The generator `scripts/build_letters.py` creates EPUB, PDF and cover assets (requires Pandoc CLI, WeasyPrint and CairoSVG to rebuild); `scripts/v010_publications.py` integrates the website pages, homepage, Library and sitemap during `python scripts/build_site.py`.
- A new cover uses the original book's intersecting-line design language. It does **not** replace the approved site emblem or foundational book covers.
- The first Letter is an **editorial release candidate**, pending H's final approval and a real deployed-site/e-reader check.
- For GitHub, apply the `Book_of_Chance_Website_Update_Only_v0.10.zip` patch on top of the existing v0.9 site. It contains only changed/new paths; keep all others and retain your real `assets/forms-config.js`.


## v0.13 — Letters from H / 03

- Added `BOC-LFH-003`, **What Do We Owe to Strangers?**, from one canonical Markdown manuscript.
- Created an 11-page 6 × 9-inch PDF, reflowable EPUB and house-style cover with crossing and continuing paths.
- Integrated the whole text into a new route `/letters/what-do-we-owe-to-strangers/`, and refreshed the Library, homepage, archive and sitemap.
- The three-Letter opening collection is now prepared, but each issue remains an editorial candidate until H approves it and the deployed site is checked.
- Generators: `python scripts/build_letter_003.py` builds issue 003 deliberately; `python scripts/build_site.py` updates site pages and only makes issue assets if missing.
- Tests: `python scripts/build_five_values.py  # only when manuscript changes; before build_site.py`, plus the record in `docs/Letter_003_QA_Report.json`.
- The accepted logo, Formspree configuration, foundational book, journal files and previous Letters are unchanged.
- The next planned publication is **The Five Values**. Video/YouTube production remains deferred until the agreed literature programme is complete.

## New booklet, v0.15

The canonical source is `source/booklets/the-five-values.md`. Its 17-page PDF reader edition, EPUB and original illustrations are available under `files/booklets/` and `assets/booklets/`. The full text is on `/booklets/the-five-values/` with clearly clickable value navigation and direct download buttons.

This is **BOC-BKL-001 · 1.0-RC1** and awaits founder approval and live device review. The booklet's digital PDF is not a commercial print-ready interior. For editorial details see `docs/Five_Values_Editorial_Review_RC1.md`. YouTube/video development remains deferred until the literature plan is completed.


## Conversations of Chance · v0.16 update

The newly prepared **Conversations of Chance** discussion companion is presented as an editorial candidate, not a final H-approved publication. Its full HTML reader is at `publications/conversations-of-chance/`, with matching PDF and EPUB under `files/conversations/`; it is linked on the home page and in the Library. Rebuilds incorporate this page through `scripts/v016_conversations.py` after `v015_five_values.py`. The canonical Markdown manuscript is `source/conversations/conversations-of-chance.md`. The reader uses the established logo/theme system and is marked `noindex` until approved. No changes to the existing forms, paid services, member access, book manuscripts, journals or older publications are required.


## v0.19 — The Parables of Chance (editorial staging)

`publications/parables-of-chance/` presents the complete twelve-story fiction collection, PDF and EPUB proofs, and its established literary cover. `source/parables/the-parables-of-chance.md` is the editable canonical text. Run `python scripts/build_parables.py` only to rebuild its exports; normal site rebuilding uses `python scripts/build_site.py`, including the `v019_parables` integration. The stories are visibly fictional and do not imply working Fellowship services.

The v0.19 ZIP is an update-only patch: upload changed files over the current repository, preserving paths, and do not delete or replace existing unrelated content. Private and working form configuration is not included. This edition remains an editorial candidate, not a fully verified public release.


## v0.21 — A Beginner’s Guide to Confluent Humanism

The short introductory guide is now available as a complete HTML reader at
`publications/beginners-guide-to-confluent-humanism/`, with the reviewed v0.2
PDF and EPUB. It uses the approved-for-staging v0.1 visual cover without changes.
The homepage gives newcomers a short “Start here” link and makes the guide the
first item in the compact collection. The Library has nine titles (six books /
companions and three Letters), all searchable with the existing local-only
filter. The main book editions, journals and forms remain unchanged.

The canonical manuscript is `source/guides/beginners-guide-to-confluent-humanism.md`.
Regenerate the publication exports only when intended with
`python scripts/build_beginner_guide.py`; regenerate site HTML with
`python scripts/build_site.py`. The `v021_beginner_guide.py` stage runs after
v0.20 and does not enable any membership, payment or form changes.

The guide is a revised editorial candidate approved for website staging,
not independently approved as a final accessible release. Its page is set
to `noindex,follow` until formal release checks are completed.

## v0.23 — Questions About Chance

`questions/` provides a non-tracking, searchable FAQ with native expandable answers and five category filters. The FAQ has a proposed cover, 17-page PDF, EPUB, and canonical manuscript/structured data in `source/resources/`. Its status is editorial candidate and the page is `noindex,follow` until H approves the text and cover and remaining independent/accessibility checks are completed. Run `python scripts/build_questions_faq.py` only when intentionally regenerating the PDF/EPUB, then `python scripts/build_site.py` for HTML. No membership or donation service is activated.
