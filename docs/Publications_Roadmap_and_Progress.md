# H Publications — Release Roadmap and Progress Register

**Updated:** 22 November 2026 · v0.14 (targeted editorial correction pass; no human reader pilot)  
**Sequence rule:** Develop and review **one publication at a time**. After completing the recommended literature programme, plan and launch the Fellowship's YouTube/video channel. No concurrent video production is assumed.

## Working order

| Order | Publication | Current stage | Approval to move on |
|---|---|---|---|
| 1.1 | **Letters from H · No. 01 — On the People We Never Meet** | Editorially refined to 1.0-RC2. HTML, PDF and EPUB prepared; human sign-off/live verification pending | H reviews text and visuals; deployed downloads checked |
| 1.2 | **Letters from H · No. 02 — When Good Choices Lead to Bad Outcomes** | Draft complete; 1.0-RC1 PDF, EPUB and web reading prepared; author/live approval pending | Text and design approved; live downloads verified |
| 1.3 | **Letters from H · No. 03 — What Do We Owe to Strangers?** | Full 1.0-RC1 editorial candidate prepared; HTML/PDF/EPUB complete; H approval and live verification pending | Review for fairness and publishable voice; check deployed downloads |
| 2 | **The Five Values** | Proposed 10–15-page illustrated beginner booklet | Three Letters complete; editorial concept signed off |
| 3 | **Conversations of Chance** | Proposed guide to twelve optional facilitated discussion sessions | The Five Values published; safeguarding and facilitation boundaries reviewed |
| 4 | **The Little Book of Possibilities** | Proposed 40–60-page accessible companion | Discussion guide published; original contribution distinguished from main book |
| 5 | **The Parables of Chance** | Proposed illustrated fiction collection, approx. 60–90 pages | Other publications complete; each story labelled as fiction; rights reviewed |
| 6 | **Fellowship YouTube / video channel** | **Deferred by owner** until above recommended publications are finished | Library programme complete; then plan content format, voice and distribution |

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
