# The Book of Chance — Website v0.31

A static GitHub Pages website for the free literature of Confluent Humanism, optional private reflection resources and information about the *proposed* Fellowship of Chance.

**Public site:** https://thebookofchance.github.io/  
**Literature release:** 23 November 2026, author-approved by H.  
**Website update:** v0.31 — literature digital release, canonical indexing, release register.

## Published digital literature

The Library includes nine author-approved works: *The Book of Chance* (Light/Dark editions), the three *Letters from H*, *The Five Values*, *Conversations of Chance*, *The Little Book of Possibilities*, *The Parables of Chance*, and *A Beginner's Guide to Confluent Humanism*. *Questions About Chance* is an additional released reader FAQ. These works are free to read or download, and no belief or membership is required.

The `journey/` Guided Reading Journey has eight optional routes; the `reader/` interface provides paginated reading across the nine Library titles. The Reading Room remains `noindex` because it duplicates the canonical publication texts; the individual published literature pages, FAQ and Guided Reading Journey are indexable and in the sitemap.

## Main routes

- `/` — Homepage and starting points for reading
- `/downloads/` — Library catalogue and PDF/EPUB downloads
- `/reader/` — Paged eReader; device-local reading place
- `/read/` — Original book and its twelve readings
- `/letters/` — The three published Letters from H
- `/booklets/` and `/publications/` — Companion books and Guide
- `/questions/` — The searchable 26-question FAQ
- `/journey/` — Eight Guided Reading Journeys
- `/reflect/` — Optional private reflection resources
- `/community/`, `/focus/`, `/print/` — Future Fellowship plans and interest forms
- `/about/`, `/privacy/` — About and privacy information

## Scope and trust

- Author approval does **not** certify PDF/UA conformance, substitute for independent accessibility testing, or imply endorsement by external reviewers. Tagged PDFs, EPUBs and HTML alternatives are available.
- The Fellowship's Council, formal membership, mentorship, hardship programme, payments and charitable programmes are **not** operational. No such service is activated by publication release.
- The site owner's real form submission checks were reported as successful on 23 November 2026; this update does not change `assets/forms-config.js` and does not independently re-verify delivery.
- Earlier filenames containing `Editorial_Proof` are retained for URL continuity. The **contents and public labels** now identify these as approved digital editions.
- `docs/Literature_Release_Register_v0.31.json` records release identities and file hashes; `docs/Literature_Release_QA_v0.31.json` records local checks.

## Deploy the update-only ZIP

Extract `Book_of_Chance_Website_Update_Only_v0.31_Literature_Release.zip` at the **root** of your existing repository, preserving paths and replacing files with the same name. **Do not delete unrelated existing files.** The ZIP does not include the existing form configuration.

After GitHub Pages finishes deploying, verify the homepage and Library badges, at least one PDF/EPUB download, the FAQ and Reading Journey, a mobile eReader page, and your established forms. Search indexing is permitted by the site metadata but not immediate or guaranteed.

## Rebuilding the site

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_site.py
```

The standard generator applies `scripts/v031_release.py` at the end to preserve canonical release metadata and indexing. Approved cover assets are hash-checked through the existing production scripts. Regenerating a PDF/EPUB edition is a separate intentional operation and may change the exact registered file hash; update the release register if you do so.

## Historical project record (superseded status descriptions)

The following development notes document the earlier production stages. Any references to editorial-candidate status, planned releases or earlier website versions below are **historical** and do not override the current v0.31 release register.



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

## v0.25 reading room notes

- The Library offers an eReader launch option for nine titles alongside their existing HTML/PDF/EPUB editions. Content is extracted from existing public website readers by `scripts/v025_library_reader.py`; changes to canonical HTML are reflected when the site is rebuilt.
- Section pages use CSS columns computed for the current screen width and font size. **Page numbers are relative to the current section**; they will change when font size or viewport changes.
- Reading place and preferred text size are stored only in this browser, can be cleared, and are not transmitted to the website. All literature remains accessible without JavaScript using existing reading links.
- `reader/` is intentionally `noindex` to avoid competing with the canonical publication pages. It is excluded from the sitemap. Editorial-candidate labels for unfinished release checks remain in place.
- Cover images are unchanged. The new Library shelf backgrounds are a presentation treatment, not new cover artwork or founder approval of a new cover design.

### Website v0.26 — paged original Book of Chance readings

The original `read/<section>/` routes now have a page-by-page reading experience with a visible page count, keyboard/touch and next/previous controls, locally saved position and a non-JavaScript scrolling fallback. This does not change manuscript content, publication approval flags or the separate nine-book Reading Room. See `docs/Website_v0.26_Paged_Book_Reader_QA.md`. Build module: `scripts/v026_book_paging.py`; style/script source: `source/resources/v026-book-pages.*`.
