# H Publications — Release Roadmap and Progress Register

**Updated:** 22 November 2026 · v0.10  
**Sequence rule:** Develop and review **one publication at a time**. After completing the recommended literature programme, plan and launch the Fellowship's YouTube/video channel. No concurrent video production is assumed.

## Working order

| Order | Publication | Current stage | Approval to move on |
|---|---|---|---|
| 1.1 | **Letters from H · No. 01 — On the People We Never Meet** | Complete editorial candidate. HTML, PDF and EPUB prepared; human sign-off/live verification pending | H reviews text and visuals; deployed downloads checked |
| 1.2 | **Letters from H · No. 02 — When Good Choices Lead to Bad Outcomes** | Planned; not drafted | Issue 001 approved |
| 1.3 | **Letters from H · No. 03 — What Do We Owe to Strangers?** | Planned; not drafted | Issue 002 approved; distinct ethical argument from issue 001 |
| 2 | **The Five Values** | Proposed 10–15-page illustrated beginner booklet | Three Letters complete; editorial concept signed off |
| 3 | **Conversations of Chance** | Proposed guide to twelve optional facilitated discussion sessions | The Five Values published; safeguarding and facilitation boundaries reviewed |
| 4 | **The Little Book of Possibilities** | Proposed 40–60-page accessible companion | Discussion guide published; original contribution distinguished from main book |
| 5 | **The Parables of Chance** | Proposed illustrated fiction collection, approx. 60–90 pages | Other publications complete; each story labelled as fiction; rights reviewed |
| 6 | **Fellowship YouTube / video channel** | **Deferred by owner** until above recommended publications are finished | Library programme complete; then plan content format, voice and distribution |

The initial programme's *Letters from H* collection is intended to remain open to future occasional issues after the first three, but does not need to become a fixed weekly output commitment.

## Current source of truth

- Foundational text: `source/manuscript.md` (v0.12 source, no changes).
- House standard: `docs/Publications_Standard_v1.0_RC1.md`.
- Journal-specific standard: `docs/Journal_Series_Editorial_and_Print_Plan.md`.
- Letter source: `source/letters/001-on-the-people-we-never-meet.md`.
- Publication entries and statuses: `source/letters/catalogue.json` and `source/publications.json`.
- First letter generator: `scripts/build_letters.py`.
- Site integration: `scripts/v010_publications.py` called from `scripts/build_site.py`.

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
