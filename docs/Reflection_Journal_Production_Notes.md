# The Reflection Journal — editorial and production record (v0.8)

## Purpose
A free, private reflection resource built on The Book of Chance's three existing practices. The journal is a companion, not an obligation, test of devotion, or required part of future Fellowship participation.

## Editions and files
- `files/reflection/The_Reflection_Journal_Fillable.pdf` — 28-page 6 × 9-inch digital fillable edition. Interactive PDF form fields are saved **on the user's device**. No server service is connected.
- `files/reflection/The_Reflection_Journal_Print_Layout_Proof.pdf` — identical interior sequence with ruled writing areas instead of interactive fields. **Not approved for commercial printing.**
- Three `*_Fillable.pdf` A4 one-page guides, with five reflective questions each and one date field.

## Design system
Charcoal (`#26313b`), blue (`#286cb8`), warm-white (`#fffefb`), muted grey (`#63717c`), open margins, conventional serif body/headlines and restrained sans-serif metadata. A geometric crossing-path motif complements but does not modify the accepted website emblem.

## Contents
Cover; introduction and usage/privacy notes; Part I: The Reflection of Chance (4 two-page entries); Part II: The Act of Possibility (3 two-page entries); Part III: A Week of Possibilities (4 two-page entries); closing reflection. 28 pages total. Prompts must stay in sync with the site's three web practices.

## PDF reader behaviour
Forms are standard AcroForm multiline text fields. Compatible desktop readers can fill and save them. Some browser, phone or preview apps may not support saving input or may render appearances differently. Readers should test with a harmless sample before trusting a private entry. Longer responses can be limited visually by fixed field size; users can start a fresh copy or use another journal entry. The browser editor instead prints a branded, non-fillable record through the browser's own "Save as PDF" function.

## Physical publication gates
A future paid hardcopy must never be presented as on sale until its printer format and terms have been confirmed. In particular: total page count/spine and binding eligibility; interior trim, margins and gutter; bleed/ink coverage; accessible and legible ruling; paper quality; cover wrap dimensions and spine; pricing, taxes and fulfillment; ISBN/barcode if appropriate; print samples; legal/quality reviews. Consider expanding the journal beyond 28 pages for a practical physical product.

## Rebuild instructions
`pip install -r scripts/requirements.txt`
`python scripts/build_reflection_pdfs.py`
`python scripts/build_site.py` (regenerates pages; v0.8 overlays are applied last)
Keep private Formspree settings and brand assets unmodified when deploying.
