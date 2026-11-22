# Cross-Publication Targeted Editorial Corrections — v0.14

**Date:** 22 November 2026  
**Basis:** Simulated_Reader_Test_Report_v1.0.md and Issue_Register_v1.0.csv  
**Scope:** Foundational book, Letters from H 01–03, four companion journal PDFs, three A4 worksheets and the relevant website pages.  
**Status:** Completed targeted internal editorial revision; **not** real-user testing or final founder approval.

## Editorial approach

These corrections address identified editorial risks without changing the philosophical position, five values, book title, illustrations, H byline or voluntary nature of all practices. The review was model-generated; possible simulated reader reactions are hypotheses, not recorded real opinions.

## Text edits by publication

### The Book of Chance
Reading IV gains a short positive explanation for favouring an open future; uncertainty, ontological indeterminacy and practical opportunity are distinguished. The determinism counterargument is more concise. Repeated crossing imagery is varied in one passage, without changing the core claim or ethical safeguards.

- Words (whitespace count): 20,653 → 20,793.
- Canonical source: `source/manuscript.md`.

### Letter 01 — On the People We Never Meet
Introduces a warm, ordinary picture of unseen work enabling everyday pleasures and an example of shared reference notes accumulating value. Condenses repeated cautions and makes the affirmative duties of accurate, careful contribution clearer.

- Words (whitespace count): 2,158 → 2,238.
- Canonical source: `source/letters/001-on-the-people-we-never-meet.md`.

### Letter 02 — When Good Choices Lead to Bad Outcomes
Clarifies two dimensions of responsibility (decision process and subsequent response), streamlines adjacent negative qualifications and adds a practical, compassionate follow-up example after a cancelled event. Removes a nonessential mention of Fellowship doctrine.

- Words (whitespace count): 1,912 → 1,915.
- Canonical source: `source/letters/002-when-good-choices-lead-to-bad-outcomes.md`.

### Letter 03 — What Do We Owe to Strangers?
Replaces another public-building accessibility example with an explanation about a confusing public-service notice. Removes the specific Fellowship funding paragraph and uses a generic ethical standard for accountable public giving. The checkout ending now offers warm, low-pressure possibilities rather than repeating defensive caveats.

- Words (whitespace count): 2,168 → 2,183.
- Canonical source: `source/letters/003-what-do-we-owe-to-strangers.md`.

## Journals and web-use privacy

- In all journal introductions, readers are told that they can pause or skip, that a saved PDF is private **only if its storage is private**, and that shared computers, backups and printed copies can expose sensitive responses.
- The first entry in each main journal now carries a short visible permission to skip a question or pause.
- All three single-page A4 PDFs now include shared-device/save-location advice.
- `/downloads/`, `/reflect/` and `/privacy/` repeat the important storage limitations without changing the existing form registrations. None of these resources requests private journal contents.

## Follow-up on every issue raised by the simulated stress test

| Issue | Disposition | Evidence / remaining limit |
|---|---|---|
| RT-01 Human reader evidence | **Not performed** | No real readers or fabricated outcomes. Pilot unavailable. No claims of observed comprehension, satisfaction or endorsement. |
| RT-02 Fundamental chance rationale | **Edited** | Reading IV adds a positive, qualified explanation. Remains a contested philosophical preference, not a scientific finding. |
| RT-03 Repeated imagery | **Edited** | Letter 03 replaces another staircase image with a language-access/service design example; Letter 01 gets more specific, positive scenes. Signature paths in the original book retained. |
| RT-04 Defensive caveat density | **Edited** | Several adjacent disclaimers consolidated, affirmative arguments strengthened. Consent and proportional duty safeguards preserved. |
| RT-05 Fellowship aside in Letter 03 | **Edited** | Explicit promotion/fundraising paragraph removed; general standards for accountable giving retained. |
| RT-06 Emotional variety | **Edited** | Letter 01 adds ordinary pleasure and reciprocity; Letter 02 emphasises useful follow-up; Letter 03 includes a warm checkout alternative. The texts remain sober by design. |
| RT-07 Journal device/accessibility compatibility | **Partially verified** | PDF field structure and simulated save/reopen passed. Real mobile readers and assistive technology were not tested. |
| RT-08 Introductory readability | **Deferred to next title** | *The Five Values* will serve as the accessible, plain-language entry point. No claim of youth/older-reader acceptance. |
| RT-09 Shared-device privacy | **Edited** | PDF introductions, A4 footers, Reflection and Library pages warn about private save locations, cloud backups and shared devices. |
| RT-10 Production, rights, founder approval | **Partially verified** | Automated integrity, source/web parity, page renders and local links checked; real deployment, rights confirmation, founder approval and accessibility certification remain open. |

## Automated and visual checks

- 37 generated website pages, 1021 local references, 0 broken.
- All seven publication PDFs (two book editions and three Letters among them) contain the revised text; all five corresponding EPUBs contain the same targeted passages and valid EPUB archives.
- Four journal editions and three worksheets have editable form fields; sample test values survived an in-memory save/reopen cycle in the local PDF engine.
- The 6 book images and explanatory captions remain present in each EPUB (plus one cover image).
- Selected cover, revised text, journal instruction and entry pages were rasterised and inspected for legibility and content placement.
- Accepted logo, original book cover assets and Formspree configuration were compared byte-for-byte with the previous site version and are unchanged.

## Limits and publication status

**No independent human reader testing can be claimed.** Simulated perspectives cannot reveal real emotional reactions, varied reading comprehension, disability access or usability on every device. The completed technical checks support a publication candidate, not a reader-validated final edition.

H/founder still needs to accept the final literary voice before changing editorial-candidate status. The revised PDFs and EPUBs are not printer-certified or PDF/UA-certified. Live GitHub Pages behaviour and real Formspree submissions were not rechecked in this revision.

These limits are documented rather than used as a reason to halt all further draft publications. The next planned text remains *The Five Values*. The organisation’s YouTube project remains deferred until the literature programme is completed.

## Canonical edition mapping

- The Book of Chance — revised manuscript in `source/manuscript.md`; Light and Dark book PDF/EPUB reader proofs regenerated from the same revised body.
- Letters from H, No. 01 — 1.0-RC3.
- Letters from H, No. 02 — 1.0-RC2.
- Letters from H, No. 03 — 1.0-RC2.
- Journal titles and form structures unchanged; privacy and agency instructions updated.

## Reproducibility

The source-of-truth files are the Markdown manuscripts and `source/letters/catalogue.json`. Rerun `python scripts/build_book_publications.py`, `python -c "import sys; sys.path.insert(0, 'scripts'); from build_letters import build, build_letter_002; build(); build_letter_002()"`, `python scripts/build_letter_003.py`, `python scripts/build_reflection_pdfs.py`, `python scripts/build_journal_series.py`, and finally `python scripts/build_site.py` when the relevant Python and Pandoc dependencies are installed. Publication assets should only be regenerated intentionally, not during an ordinary site rebuild.

### Source fingerprints

- `source/manuscript.md` SHA-256: `997a36f2aa8265129ea7ec8638a95783065c8fc7649f5505023a243f569384e9`
- `source/letters/001-on-the-people-we-never-meet.md` SHA-256: `21545952773c17e3f925e193f1fbe3f213b84019b604cb7da00df04ae3f0a262`
- `source/letters/002-when-good-choices-lead-to-bad-outcomes.md` SHA-256: `0143d795bd30fca5f46a90fe3d9dc90d1e2621b814179bf8015b8e51096c4144`
- `source/letters/003-what-do-we-owe-to-strangers.md` SHA-256: `e6621c9ad5ed4a24fecb0ff1d19f6788bd90707ee2439c8d440872ebd670832a`
