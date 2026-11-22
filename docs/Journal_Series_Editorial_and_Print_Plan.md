# The Book of Chance — Reflection Journal Series
## Editorial identity, edition map and print development plan · v0.9 · 22 November 2026

### Publishing principle
These are *companion publications* to **The Book of Chance**, by **H**. They are not devotionals, tests, scorecards or membership requirements. The practices invite attention to circumstance, meaningful choice, dignity, uncertainty, mutual care and the five values of Confluent Humanism. No reader owes the Fellowship private journal entries or proof of participation.

This initial series is intentionally **three different books, not an unlimited range of minor variations**. The complete journal has two cover options because the foundational book has a Light and Dark edition; its interior is identical in both.

### Publication map

| PDF | Printed size and length | Best for | Contents |
|---|---|---|---|
| `The_Reflection_Journal_Fillable.pdf` | 6 × 9 in, 48 pages | Readers wanting all practices | Five Reflection of Chance entries; four Acts of Possibility; five weekly reflections; two Turning of Chance entries; four open pages; editorial pauses and closing |
| `The_Reflection_Journal_Dark_Fillable.pdf` | 6 × 9 in, 48 pages | Same complete practice, Dark cover | Same interior content as the Light Edition, verified page by page |
| `The_Daily_Reflection_Journal_Fillable.pdf` | 6 × 9 in, 40 pages | Personal noticing without a daily streak | Fourteen two-page reflections; two longer weekly reviews; four open pages |
| `The_Possibility_Journal_Fillable.pdf` | 6 × 9 in, 40 pages | Reflective voluntary service and practical care | Consent and boundaries note; twelve acts of possibility; three follow-up reflections; five open pages |
| `The_Reflection_Journal_Print_Layout_Proof.pdf` | 6 × 9 in, 48 pages | Early printing feasibility | An unfillable Light Edition layout study using ruled lines rather than PDF fields. **Not a print-ready master.** |

Three single-page fillable A4 worksheets remain available for readers who do not want a bound-style journal.

### Family resemblance to The Book of Chance

- **Cover hierarchy:** restrained small-caps series label; large serif title; thin divider; subtitle in italic serif; isolated H byline.
- **Visual motif:** delicate sweeping paths that cross and continue beyond the central meeting point. Dark ink, muted grey and blue are used in proportions consistent with the original Light/Dark book covers. The website's accepted circular emblem is *not modified*.
- **Editorial design:** warm-white pages, spacious margins, modest running heads, numbered entries, restrained rules and no generic decorative icons.
- **Interior logic:** each entry has a dated optional space and five prompts spread across two pages, plus a free-writing box; sections are introduced by short, nonprescriptive passages.
- **Reader control:** writing stays on the user's device, fields are optional, no completeness percentage or streak is displayed, and the reader can print or return to any entry without joining the Fellowship.

### Meaningful differences, not cosmetic editions

1. **Complete** is an introductory companion to the philosophy's principal reflective practices, including the longer *Turning of Chance*.
2. **Daily** offers many opportunities to notice immediate circumstances, choice and appreciation. Daily is a possible rhythm, never a duty.
3. **Possibility** turns reflection toward respectful help and shared opportunities, with explicit attention to consent, privacy, limits and the other person's independence.

The complete journal is the main recommendation for a new reader. The focused editions should be introduced to someone who wants a practice of a different depth or emphasis.

### Digital use

- Each released PDF contains real multiline AcroForm fields and can be edited and saved locally using a compatible PDF reader. Test an innocuous entry and save/reopen it before relying on a PDF reader for private content.
- Browser-integrated and phone PDF viewers may display text differently, decline to save form data, or limit the visible length of long answers.
- There is no server-side reflection storage; form responses are not sent to Formspree. PDF files download without registration or payment.
- Pages can also be printed and completed by hand; the dedicated print proof replaces fields with writing rules.
- No accessibility conformity certification has been performed. These PDFs are not tagged PDFs and should be tested with real assistive technology before making accessibility claims.

### Physical edition roadmap — not yet on sale

1. Determine the intended user and whether 48 or 40 pages are enough. A commercial *working* journal may benefit from 80–120 pages, using repeated two-page entries rather than adding filler.
2. Choose final printer, binding, trim, paper weight, opacity and required spine width; decide whether a 6 × 9 in trade journal is appropriate. Some printers require a minimum page count for a particular binding.
3. Rebuild an actual print interior with correct inside/outside margins, gutter, spine/creep allowance (if relevant), bleed and any required grayscale/CMYK specifications. Do not send fillable PDF form controls to a commercial printer.
4. Make separate wraparound covers for each title and cover edition, using printer-specific templates and accurate spine dimensions; avoid inventing ISBN/barcode details.
5. Obtain hardcopy proofs and check line contrast, handwriting space, readability, trim, page order, binding durability, ink consumption and cover feel.
6. Confirm production, fulfilment, taxes, returns, price and shipping before offering purchases or collecting money. Voluntary contributions to the Fellowship are **not** a prerequisite for accessing the free journals.

### Website and source maintenance

`python scripts/build_reflection_pdfs.py` regenerates the existing A4 worksheets and the v0.9 journal series. `python scripts/build_site.py` produces the website and applies `v09_enhancements.py` after previous overlays. `python scripts/audit_v09.py` checks the static paths and PDF structures. New releases must be added to `source/publications.json` without changing the site's accepted emblem or the private Formspree configuration.

The current release has **no live sale, purchase link, donation flow, community journal sharing or paid tier**.
