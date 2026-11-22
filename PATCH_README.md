# The Book of Chance — Website v0.16 · Update-only patch

**Base required:** v0.15 already installed in your existing GitHub Pages repository. This ZIP includes only the files added or changed for *Conversations of Chance*. It is not a complete website.

## Install

1. Open the ZIP and copy its **contents** to the **root** of the same repository that currently contains v0.15, preserving folder paths. Do not replace the repository with the extracted folder or delete files omitted from this patch.
2. Allow GitHub Pages to deploy, then visit `publications/conversations-of-chance/`.
3. Confirm the new feature appears on the homepage and in the Library at `downloads/#conversations-of-chance`.
4. Open and download both formats: `files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf` and `files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.epub`.
5. Check the site's existing theme toggle, mobile navigation, original book, Letters, journals, **The Five Values**, and both existing interest forms in the live deployment.

## What's changed

- **Conversations of Chance**, BOC-CNV-001: twelve original discussions linked to each of the twelve readings of *The Book of Chance*. Complete public HTML reader, 48-page PDF reader proof, EPUB and editable canonical source.
- New v0.16 page uses the existing website's header, footer, Library navigation, fonts, CSS variables, light/dark styling and original brand asset (it **does not** introduce a replacement logo).
- New homepage feature, dedicated Library section, publication catalogue entry, updated Library count and navigation shortcut.
- Updated build integration (`scripts/v016_conversations.py`, plus call from `scripts/build_site.py`), manifest, progress register, development log and QA report.

## Publication status

This is **editorial candidate v0.1**, not H-approved final writing or verified public release. The page is accessible to readers once deployed but carries a `noindex,follow` tag and is **not yet listed in the sitemap** to avoid presenting the editorial candidate as an approved publication. Remove `noindex` and add the URL to `sitemap.xml` after editorial approval.

The Fellowship's Council, membership service, mentoring, hardship assistance, donation programmes and official Local Fellowships are not represented as operational.

## What this patch intentionally does not touch

- No changes to `assets/forms-config.js`, the accepted site brand assets, the master *Book of Chance* manuscript, existing Letters, the Five Values manuscript, PDFs/EPUBs of earlier works, reflection journals or the other existing pages.
- No fundraising, subscriptions, membership applications or new tracking scripts.
- No deletion of previous content. If the **earlier stand-alone v0.16** ZIP was already uploaded, this integrated patch updates the same `publications/conversations-of-chance/` reader and uses canonical downloads under `files/conversations/`; the old duplicate files in the publication folder can remain harmlessly until you choose to clean them up.

## Tested and still to verify

Verified locally: source and generated HTML contain 12 discussions; PDF has 48 pages; EPUB package integrity; download paths; site links into the established reading routes; and desktop/mobile inlined-Chromium layout without horizontal overflow. **Not verified:** your actual GitHub Pages deployment, operation of site JavaScript in the full repository, all browser/reader variants, Formspree delivery or external human/editorial review. The provided v0.15 package was itself an **update-only ZIP**, so files from earlier baseline versions were not available for a complete local site smoke test.

See `docs/Conversations_of_Chance_QA_v0.16.json` and `docs/Publications_Roadmap_and_Progress.md`.
