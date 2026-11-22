# The Five Values — Editorial review and source alignment

**Identifier:** BOC-BKL-001  
**Version:** 1.0-RC1 · 22 November 2026  
**Status:** Complete **editorial candidate**; H's approval and live/e-reader checks still outstanding.  
**Authorial identity:** H · The Book of Chance companions

## Purpose and intended readers

A compact, illustrated introduction to the five values of Confluent Humanism for a reader who may not have read the foundational book. This is not a summary dressed up as a new publication: each value offers a distinct imagined situation, a practical distinction, an optional exercise and a question to carry. A concluding chapter explores tensions among values, especially consent, privacy and limits on giving.

**Length:** approximately 3,500 words; 17-page 6×9-inch PDF; reflowable EPUB; complete open web reading page. **Graphics:** six new original vector-backed conceptual illustrations in the interior and a seventh graphic for the cover. The design follows the established charcoal/white/blue paths motif but does not alter or reuse the official logo as decoration.

## Alignment with founding texts

| Value | Underlying charter position | Treatment in the booklet | Relevant book discussion |
|---|---|---|---|
| Hope | Open possibility without promising outcomes; compatible with grief and rest | Hope versus prediction; practical pathways; the absence of hope is no moral failure | Reading VII — Hope |
| Acceptance | Recognise what is and what cannot be controlled, without endorsing injustice | Acceptance versus approval; boundaries and active challenge to barriers | Reading VII — Hope; Reading VI — Reflection and Growth |
| Reflection | Consider circumstances, choices and learning without perfect streaks or compelled disclosure | Observation versus interpretation; privacy, rumination and mercy | Reading VI — Reflection and Growth |
| Growth | Intellectual, emotional, social and personal development, not productivity or status | Unlearning and listening; growth at the person's pace, with consent and rest | Reading VI — Reflection and Growth |
| Community | Shared opportunity, voluntary generosity, dignity in receiving and safeguarding | Reciprocal belonging, consent, non-transactional relationships, institutions and the living world | Readings VIII, IX and X |

The introductory four foundational statements follow the working charter. The philosophical assertion that chance is fundamental remains a **revisable conviction**, not a claim of scientific demonstration. Agency and ethics are not presented as conclusions mathematically derived from randomness. The five values are complementary, not a ranked or compulsory programme.

## Narrative and editorial decisions

- **Hope:** an imagined return to music after years away; no guaranteed restoration or compulsory optimism.
- **Acceptance:** an imagined inaccessible library entrance; acknowledging a barrier does not legitimise it.
- **Reflection:** an ambiguous quiet moment after a meeting; evidence is separated from inference.
- **Growth:** an imagined volunteer who learns to listen and decentralise authority; growth is not measured by output.
- **Community:** an imagined bicycle repair table; belonging does not depend on contribution.
- **Values in tension:** the limits of a person's health and energy, and privacy where shared stories might be requested for publicity; there is no artificial algorithm that ranks the values.

All fictional situations are explicitly called *invented* or *imagined* in the prose. They are neither testimonials nor verified historical events. No existing mentor, assistance fund, community gathering, registered charity or active fundraising mechanism is implied.

## Simulated editorial objections and responses

1. **“Is this just another motivational booklet?”** The text avoids automatic positive outcomes and includes uncertain choices, inaccessible systems, privacy, boundaries and collective responsibility. It welcomes critique.
2. **“Does acceptance justify oppression?”** No. The library illustration explicitly separates recognising a present barrier from endorsing it, and places responsibility on the institution.
3. **“Does community demand free labour or donations?”** No. The text says care is voluntary, personal capacity matters, and receiving help is legitimate; no membership or financial solicitation appears.
4. **“Could reflection encourage rumination?”** Its shadow is acknowledged; stopping, rest and support are legitimate responses.
5. **“Do people who cannot grow or feel hopeful become failures?”** The text repeatedly distinguishes values from rankings, achievement and moral worth.
6. **“Is it original?”** It is an editorial synthesis of established concerns, connected explicitly to the foundational book. It does not claim to invent reflection, practical wisdom or an ethic of care.

These are **simulated editorial checks, not observations of real readers**. Human reader testing is unavailable. We cannot infer actual accessibility, enjoyment or comprehension from these checks.

## Publication gates

| Gate | Finding |
|---|---|
| Source alignment | PASS — compared against current foundational manuscript, charter and house standard |
| Independent editorial purpose | PASS — new scenarios, questions and conflict section |
| Factual claims and fictional labelling | PASS for internally checkable claims — no specific external statistics or fabricated sources |
| Ethics/privacy | PASS in editorial review — voluntary practices, no guilt-based appeals |
| Proofreading and terminology | PASS in internal editorial pass — no human independent proofreader |
| Format/export | PASS — PDF (17 pages, text selectable), EPUB archive with 6 interior illustrations, full HTML |
| Local website routes/assets | PASS — see `Five_Values_QA_v0.15.json` |
| Founder approval | **PENDING** |
| Live GitHub/e-reader/accessibility devices | **PENDING** |
| Commercial physical printing | **NOT PREPARED** — PDF is a digital reader edition; margins, bleed and cover/spine must be separately proven |

## Source of truth and regeneration

`source/booklets/the-five-values.md` is the sole canonical manuscript. Run `python scripts/build_five_values.py` intentionally after editorial changes to regenerate the PDF/EPUB and cover/diagram assets. Then run `python scripts/build_site.py` to propagate the current manuscript to the web reading route and regenerate Library/home links. The ordinary site builder does **not** silently rewrite a previously produced PDF/EPUB.

## Release decision

**Recommended stage:** RC1 candidate ready for H's content/design approval. No claim of H sign-off, public release date, printer proof, independently validated scientific philosophy or real-reader pilot. The next intended book is *Conversations of Chance* after approval; the video project remains deferred until completion of the selected publications.
