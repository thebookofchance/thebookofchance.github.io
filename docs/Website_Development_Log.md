# The Book of Chance — Website Development Log

**Maintained record:** Started 22 November 2026  
**Current release:** Website v0.7  
**Project:** https://thebookofchance.github.io/  
**Principle:** Publication first; the Fellowship grows through useful, voluntary participation rather than financial or social pressure.

## Release history

| Website version | Main work | Operational status |
|---|---|---|
| v0.3 | Complete online book, refreshed illustrations, approved Light/Dark editions, GitHub-root archive | Completed in earlier release |
| v0.4 | Fellowship landing page, growing Library catalogue, brand overhaul | Completed in earlier release |
| v0.4.2 | Accepted circular/intersecting-path emblem with evenly constructed diagonal lattice | **Preserve without redesign** |
| v0.5 | Separate Formspree interest forms for Fellowship and print editions; privacy notice | Founder reports forms working live; deployment credentials not inspected here |
| v0.6 | More persuasive Fellowship page, first-year development priorities, support concept, honesty about unlaunched services | Completed in earlier release |
| **v0.7** | Private reflection workspace; curated weekly question; three downloadable guides; Current Focus and roadmap; high-visibility Fellowship registration CTA; designed programme icons; homepage return paths; Library resources; discoverability metadata and sitemap | Built, source-checked and inline-browser interaction-tested; live deployment still to verify |

## v0.7 — Full change record

### 1. Fellowship registration is visible immediately

- Changed the **primary** button near the top of `/community/` to **Register interest**, linking directly to `#community-interest` on the same page.
- Kept a secondary invitation to learn about the Fellowship.
- Retained the existing Formspree fields, consent purposes and endpoint configuration. **The v0.7 ZIP does not include `assets/forms-config.js`.**
- No new membership accounts, donations or paid privileges are enabled.

### 2. Replaced three generic programme symbols

The Mentorship & guidance, Collaborative projects, and Practical support cards now use individual line-art SVG diagrams: a guidance path between two nodes, a shared network with a focal point, and a protective support motif. These are intentionally distinct while matching the original book's charcoal/blue style. The accepted site emblem and its asset files are unchanged.

### 3. Added `/reflect/` — a private reflection space

An interactive, usable reflection tool with three practices:

1. **The Reflection of Chance:** Circumstances, choice, learning and what might become possible.
2. **The Act of Possibility:** A small, consensual, achievable act that could expand another's options.
3. **A Week of Possibilities:** Weekly review of surprise, learning, contributions and intentions.

Important behaviour:
- Visitors write in normal browser text fields; the site does **not** send entries to a server or Formspree.
- Entries are not automatically stored; closing the tab loses unsaved work.
- Visitors can download their reflection as `.txt`, print/save it as PDF using their browser, or clear their answers.
- Switching templates or clearing entered answers requests confirmation.
- The editor works without registration, fee, login, analytics or additional libraries.
- Three plain-text worksheets are downloadable independently under `/files/reflection/`.

### 4. Added twelve rotating questions

- Twelve original reflection prompts are maintained in `source/reflection-prompts.json`.
- The featured question changes on each **Monday according to the reader's local calendar**, from a deterministic twelve-question cycle. The list then repeats; the site explicitly says it is a repeating curated archive, not newly authored weekly material.
- Visitors can examine all twelve prompts or explore the next prompt without waiting a week.
- To edit the questions, update `source/reflection-prompts.json` and regenerate the website using `scripts/build_site.py`.

### 5. Added `/focus/` — Current Focus, roadmap and potential support model

**Current focus (as of 22 Nov 2026):** Prepare a first moderated online Reflection Circle. This is a *planning goal*, not a scheduled meeting or operational service. It contains explicit prerequisites and a three-stage roadmap.

The page explains a **future voluntary, project-based support model**: set a tangible purpose, publish an itemised budget and oversight arrangements, respect restricted gifts, and report on results and unused funds. There is **no Donate button, payment form, fund-raised counter, or claim to registered charitable status**.

It also introduces **Chance Campaigns**, a deferred idea for externally vetted charities that might be chosen by a documented random draw *after* eligibility and donor restrictions have been decided. It is a conceptual illustration, not a functioning selection wheel. Financial/material assistance to members, should it ever be offered, must be handled separately and according to actual needs, not through chance selection.

**To update the current goal:** revise `focus_html` in `scripts/v07_enhancements.py`, including the last-reviewed date, then regenerate. Check the related homepage and Fellowship callouts too. Do not show invented progress figures or unapproved budgets.

### 6. Made the site useful to return to

- Added **Reflect** to the global main navigation and the footer.
- Added two prominent homepage pathways: the weekly reflection practice and the current development goal.
- Added real, downloadable resources to `/downloads/`, which previously only listed them as future work.
- Removed the now-published reflection guides from `source/publications.json`'s planned catalogue and recorded them as available resources.
- Added related links on the Fellowship page for pre-membership participation.
- Corrected stale homepage physical-book wording: interest registration is now offered, rather than promised for later.

### 7. Accessibility, privacy and discoverability

- Provided real labels, field descriptions, confirmation before destructive edits, keyboard-accessible controls and status announcements on the reflection page.
- Added a paragraph to the Privacy page distinguishing the local-only reflection editor from the Formspree forms.
- Added descriptive social-sharing Open Graph tags to the common site template, using the existing approved Light Edition cover photograph as the image.
- Added `sitemap.xml` and `robots.txt` for the site on GitHub Pages.
- Moved to a collapsible navigation earlier for narrower desktop and tablet widths to accommodate the seventh nav item.

## What deliberately was **not** added

- No fictitious testimonials, numerical progress bars or donation totals.
- No health-related fundraising appeal without an actual vetted beneficiary or authorised fiscal arrangement.
- No functioning charity raffle or Wheel of Chance before funding policy, safeguarding, rules and legal review.
- No paid membership tiers, influence or special access in exchange for money.
- No automated collection or public display of private reflections.
- No public user accounts, Discord link, made-up events calendar or empty social feed.
- No changes to the original book's twelve readings, six figures, EPUB/PDF files, or the accepted logo.

## Practical maintenance checklist

1. **Before deployment:** extract and upload the update ZIP's contents into the existing GitHub Pages repository, keeping all other files and `assets/forms-config.js` intact.
2. **After deployment:** use the published website in a private browser window to test both Formspree lists again, including delivery and email notices. Check that registration is only for adults 18+ and does not imply official membership.
3. **Every month or when something actually changes:** review `/focus/` and replace any outdated status/date; remove actions that are no longer relevant.
4. **Whenever a new publication is ready:** update the catalogue and publish the *real* resource, linking an actual download. Avoid future titles that imply published content.
5. **Before any fundraising:** get appropriate legal and accounting advice on NZ structure, payment processing, restricted-purpose accounting, beneficiary verification, policies, conflicts and public reporting. Do not claim tax deductibility or registered charity status unless established.
6. **Before active mentorship or practical assistance:** establish safeguarding, consent, eligibility, incident and privacy processes.
7. **For each new website version:** update this log, regenerate via `python scripts/build_site.py`, rerun automated link and source checks and visual tests, and package only changed or new files.

## Verification record for v0.7

- **33 HTML pages** generated (previously 31), including the book's unchanged 24 reader sections.
- **919 local links, anchors and image references** audited; no broken references detected.
- JavaScript syntax checked; EPUB ZIP integrity checked.
- Fifteen rendered page/viewport checks across desktop (1440px), tablet (820px) and mobile (390px) found no horizontal overflow or JavaScript exceptions.
- Reflection download, clear action, template switching, archive question selection, mobile navigation and the three custom icons passed browser interaction checks.
- Automated HTTP navigation to local `127.0.0.1` is **blocked by the test environment**. The visual and interaction checks above used fully inlined local assets to render the actual generated HTML inside Chromium. This provides good visual coverage but **does not replace testing the deployed site**.
- Formspree private submissions, real outgoing email delivery, third-party availability and public GitHub deployment were **not tested here**.

## Next responsible development priorities

1. Real reader testing across devices, accessibility technologies and EPUB/PDF reading apps.
2. A small, properly moderated first online Reflection Circle, after real consent and safety rules are ready.
3. A realistic operating budget and transparent funding/reporting governance **before** donations.
4. An editorial cadence for genuinely new H reflections or community updates, only when there is content worth sharing.
5. Later: vetted, consent-based membership/community infrastructure and any Chance Campaign selection rules.

*The site can remain useful without active membership: the book, worksheets and private reflection practice must stay accessible to everyone.*
