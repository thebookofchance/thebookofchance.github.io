# H Publications — Release Roadmap and Progress Register

**Updated:** 22 November 2026 · v0.24 (Guided Reading Journey staged; complete literature release review is next)  
**Sequence rule:** Develop and review **one publication at a time**. After completing the recommended literature programme, plan and launch the Fellowship's YouTube/video channel. No concurrent video production is assumed.

## Working order

| Order | Publication | Current stage | Approval to move on |
|---|---|---|---|
| 1.1 | **Letters from H · No. 01 — On the People We Never Meet** | Editorially refined to 1.0-RC2. HTML, PDF and EPUB prepared; human sign-off/live verification pending | H reviews text and visuals; deployed downloads checked |
| 1.2 | **Letters from H · No. 02 — When Good Choices Lead to Bad Outcomes** | Draft complete; 1.0-RC1 PDF, EPUB and web reading prepared; author/live approval pending | Text and design approved; live downloads verified |
| 1.3 | **Letters from H · No. 03 — What Do We Owe to Strangers?** | Full 1.0-RC1 editorial candidate prepared; HTML/PDF/EPUB complete; H approval and live verification pending | Review for fairness and publishable voice; check deployed downloads |
| 2 | **The Five Values** | **Editorial candidate 1.0-RC1 complete:** 3,500-word source, 17-page illustrated PDF, EPUB, full HTML reading page | H approves wording and visual design; deployed PDF/EPUB and page verified |
| 3 | **Conversations of Chance** | **Editorial candidate v0.1 prepared:** twelve discussions, 53-page PDF proof, EPUB and full HTML reader; H approval and live checks pending | H reviews wording, safeguarding boundaries and editorial quality; deployed formats verified |
| 4 | **The Little Book of Possibilities** | **Editorial candidate v0.2:** 12 chapters, approved cover, 42-page PDF proof and EPUB; manuscript approval and live checks pending | H reviews v0.2 text; independent human review, accessibility and live downloads verified |
| 5 | **The Parables of Chance** | **Final copyedit candidate v0.2.1:** twelve original stories, retained cover, 69-page PDF proof, EPUB and full online reader staged; author, external, accessibility and live checks pending | Obtain final H sign-off and independent reader feedback, verify specialist details and accessible downloads, test live deployment |
| 6 | **Fellowship YouTube / video channel** | **Deferred by owner** until above recommended publications are finished | Library programme complete; then plan content format, voice and distribution |

## Introductory resources

- **A Beginner’s Guide to Confluent Humanism (BOC-GDE-001):** v0.2 introductory companion staged on the website in v0.21: free 13-page PDF proof, EPUB and full nine-section HTML reader, with a cover consistent with the existing visual publishing system. Reader-simulation revisions completed; approved for web staging, not certified as a fully reviewed final release.
- **Questions About Chance (FAQ, BOC-FAQ-001):** 26-question, five-theme v0.3 editorial candidate, reviewed with simulated reader lenses and staged as an online searchable FAQ in website v0.23, with optional 17-page PDF and EPUB. H cover/text approval, independent reading, accessibility and live checks remain outstanding.
- **Guided Reading Journey:** v0.24 staged: eight themes, three verified text-specific stops per path, private optional progress, no account or personal-data collection; remains `noindex` pending review.
- **Fellowship Principles and Boundaries:** proposed public resource, not implemented.

The initial programme's *Letters from H* collection is intended to remain open to future occasional issues after the first three, but does not need to become a fixed weekly output commitment.

## Current source of truth

- Foundational text: `source/manuscript.md` (revised v0.14 editorial candidate).
- House standard: `docs/Publications_Standard_v1.0_RC1.md`.
- Journal-specific standard: `docs/Journal_Series_Editorial_and_Print_Plan.md`.
- Canonical letters: `source/letters/001-on-the-people-we-never-meet.md`, `source/letters/002-when-good-choices-lead-to-bad-outcomes.md` and `source/letters/003-what-do-we-owe-to-strangers.md`.
- Publication entries and statuses: `source/letters/catalogue.json` and `source/publications.json`.
- Letter generators: `scripts/build_letters.py` (issue-specific routines; prior issue assets are preserved by website builds).
- Site integration: `scripts/v010_publications.py`, `scripts/v012_second_letter.py` and `scripts/v013_third_letter.py`, called by `scripts/build_site.py`.

## Review protocol at the end of each publication

1. Read the entire work independent of the Fellowship website.
2. Verify foundation alignment and that major ideas are developed rather than duplicated.
3. Check specific citations, permissions, invented scenarios and unintended claims.
4. Review the cover and interior for readability, accessibility and house style.
5. Verify links, downloadable files, metadata and version number.
6. Record H's approval and the public release date (not automatically inferred from file creation).
7. Only then move to the next work.

## Issue 001 change record

**Added in v0.10:** a source-driven Letter in HTML, PDF and EPUB; a catalogue/archive page; a Library feature; a homepage introduction; a cover with intersecting charcoal/blue paths; a production generator; house standard; QA evidence and progress register.

**Preserved:** approved logo, cover editions of *The Book of Chance*, the entire book text, reflection journals, interest forms, membership status, fundraising boundaries and no-charge reading.

**Not completed:** independent human editorial review, live deployed website checks, e-reader compatibility on physical devices, certified PDF accessibility/assistive technology testing, rights/legal sign-off for a commercial print edition, and founder sign-off. No fundraising or member programme has been launched by this update.

## Issue 001 — v0.11 revision

Refined the first Letter without adding a new title or changing its core argument. The revised work is 1.0-RC2 (editorial candidate). The detailed editorial record is `docs/Letter_001_Editorial_Review_RC2.md`. No video production or second Letter has started.

## Issue 002 — v0.12 editorial candidate

The full essay **When Good Choices Lead to Bad Outcomes** (1.0-RC1) has been prepared as a freely readable HTML article, a 10-page 6×9-inch PDF and a reflowable EPUB. It distinguishes the reasonableness of a choice from its actual consequences; places limits on hindsight, pure intentions and imposed risk; and asks for listening, repair and learning after harm. It acknowledges the existing moral-luck debate (Nagel, Williams) without claiming originality for that debate. The two scenes are explicitly fictional.

The release expands the Letters catalogue and Library, features Letter 002 on the homepage, adds the stable route to the sitemap and preserves existing Letter 001 and all core publications. **No independent human review, author approval or live deployment check is claimed.** See `docs/Letter_002_Editorial_Review_RC1.md` and `docs/Letter_002_QA_Report.json`.


## Issue 003 — v0.13 editorial candidate

**What Do We Owe to Strangers?** is a complete ~2,170-word essay, 11-page 6 × 9-inch PDF, reflowable EPUB and web reading page. It explores basic duties of respect, special commitments, the practical limits of giving, consent, and the relationship between personal assistance and just institutions. The opening supermarket and directions scenes are identified as imagined.

The essay recognises the existing disputes about special obligations, beneficence and demandingness, with specific further-reading references, and avoids portraying the Fellowship as accepting donations or running hardship services. It is an **editorial candidate**, not a claim of founder sign-off.

The archive now lists three Letters. The homepage and Library link to issue 003 while issues 001 and 002 remain intact. The generator for issue 002 was also adjusted to avoid automatic regeneration of its already existing PDF/EPUB during ordinary website rebuilds. The next recommended text is **The Five Values**; YouTube remains deferred. See `docs/Letter_003_Editorial_Review_RC1.md` and `docs/Letter_003_QA_Report.json`.


## v0.14 — Targeted simulated-review corrections

Following the source-grounded simulated review, amended the foundational manuscript, all three Letters and the journal privacy/pause language. The Letter candidates are now RC3/RC2/RC2 respectively; the book retains its title and artwork but has a revised editorial text. No independent human reader testing is claimed. Completion of a technical audit is not proof of reader comprehension, accessibility or an H-approved final release. See `docs/Editorial_Corrections_v0.14.md` for passage-by-passage rationale and residual gates.

## v0.15 — The Five Values illustrated companion

**BOC-BKL-001 — The Five Values** is the next title prepared after the initial three Letters. The source manuscript is `source/booklets/the-five-values.md`, linked explicitly to the current book manuscript and the draft five-value charter. It contains six original vector/raster illustrations and a separate literary cover (seven graphics including cover). Its five sections use distinct fictional situations plus optional prompts; the concluding section addresses tensions among values. The booklet does not invent active Fellowship services or require payment, membership or private disclosure.

Production: `scripts/build_five_values.py` writes `files/booklets/The_Five_Values.pdf`, `files/booklets/The_Five_Values.epub` and web assets. `scripts/v015_five_values.py` provides website integration and is called after the three Letters. This new booklet is a full web reading page, PDF and EPUB, and a featured Library/Home publication. It is an **editorial candidate**, pending H approval and a live website / actual e-reader check.

**Next editorial manuscript to develop:** *The Little Book of Possibilities*, after review of the conversation guide. *The Parables of Chance* follows before YouTube/video development. H approvals and live checks remain separate publication gates.

## v0.16 — Conversations of Chance integrated discussion companion

**BOC-CNV-001 — Conversations of Chance: Twelve Discussions for an Uncertain Life** is a complete editorial candidate (v0.1, 22 November 2026) accompanying the twelve foundational readings. Each session includes an opening consideration, an explicitly invented dilemma, questions, voluntary private reflection, an Act of Possibility and a host note. The guide does not assert active Fellowship group services or require agreement, personal disclosure or financial participation.

Website: `publications/conversations-of-chance/` with site-wide header/footer and responsive typography. Formats: `files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf` (48-page reader proof) and `.epub`; editable source at `source/conversations/conversations-of-chance.md`. The homepage and Library point to this guide, and its 12 sections link to their relevant foundational reading pages.

**Outstanding:** founder editorial sign-off, reader testing with diverse backgrounds, live GitHub Pages link and interaction checks, device-based PDF/EPUB checks, publication metadata and final approval to index. This candidate is currently `noindex`, with its sitemap entry deferred. Creating this candidate before formal approval of *The Five Values* reflects the owner's direction to proceed through the planned literature, **not** retrospective approval of earlier titles. The subsequent planned title is *The Little Book of Possibilities*.


## The Little Book of Possibilities — v0.18 website integration

The accepted v0.1 cover was used unchanged. The substantially revised v0.2 manuscript, 42-page PDF proof, EPUB and full online reader are now represented in the website Library and homepage. The website displays editorial-candidate status; manuscript approval is **not** implied. The next planned title is *The Parables of Chance*. Independent human review, PDF accessibility tagging, e-reader testing, rights checks, and live deployment verification remain outstanding.

## v0.23 — Questions About Chance (review-stage website resource)

The FAQ is a separate **public reader resource**, not a tenth book. Its 26 source-grounded questions cover philosophical foundations, choice and fairness, daily practice, faith, and institutional safeguards. The v0.2 candidate underwent an AI-simulated review; seven targeted answers and the source/edition notes were revised to v0.3. The Council, membership and practical programmes remain proposals, not services. The FAQ page is staged at `/questions/` with search and five topic filters; PDF/EPUB are provided for offline reading. The cover is a concept awaiting H approval. `noindex,follow` remains until editorial release approval. A staged URL is publicly viewable if uploaded. Source: `source/resources/questions-about-chance.md`; data: `source/resources/questions-about-chance.json`; renderer: `scripts/v023_questions_faq.py`; exports: `scripts/build_questions_faq.py`. The **next** reader resource is the Guided Reading Journey, after the FAQ passes release review.
