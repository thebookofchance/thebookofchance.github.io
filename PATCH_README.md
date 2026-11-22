# Book of Chance — website v0.5 update-only patch

This ZIP contains only changed/new files. It updates an existing v0.4 website with the accepted v0.4.2 logo already applied. It does NOT include the manuscript, covers, EPUBs, PDFs, or any older book assets.

## What has been built
- Fellowship adult interest form (email, optional pseudonym, explicit consent; not official membership).
- Physical-book interest form (email, Light/Dark, intended copies, optional country, separate explicit consent; not an order or reservation).
- Separate privacy notice and no shared subscription between lists.
- Error/success messaging that only claims success when Formspree responds successfully.
- Both submit buttons default to DISABLED. The site does not collect personal information until you activate the endpoint and public contact email.

## Activate (requires your action)
1. With H's dedicated email account, create TWO SEPARATE forms at https://formspree.io/ — one for Fellowship interest and one for print interest.
2. Review the service's current terms and the project's privacy notice, including any overseas data handling. Confirm it is appropriate for your audience and privacy obligations.
3. Edit `assets/forms-config.js`: provide `contactEmail` (the actual H-owned public contact email), `fellowshipEndpoint` and `printEndpoint` from your Formspree dashboard. Example endpoint shape: `https://formspree.io/f/XXXXXXXX` (do not copy this placeholder!).
4. Upload the PATCH files to the existing GitHub Pages repository root, preserving their folder structure. Replace only matching paths; do not delete other files.
5. Test each form with a real test email. Verify the result actually appears in its own Formspree account/form, confirmation displays only after success, privacy requests go to the right address, and wrong/blocked requests show errors. Check at mobile widths and in light/dark theme.
6. Confirm that no preview content overpromises member services, books, dates or print targets. Do not open paid pre-orders using these forms.

## No server, no secret keys
`assets/forms-config.js` is public on GitHub Pages. Put public form endpoint URLs in it, never an API secret or password. Formspree will store response submissions independently from GitHub; this site does not store personal data in source files. Review Formspree's account security, spam protection and submission/retention settings.

## Privacy and consent
- These lists are strictly separate; consent is required individually.
- Fellowship interest is 18+ initially. Optional display names may be pseudonyms.
- The print list requests no delivery address and does not charge or reserve stock.
- The privacy notice is a draft requiring H's factual review before forms are activated. In particular, consider cross-border handling under New Zealand privacy law.

## Source generator
`scripts/build_site.py` has been updated to preserve the accepted emblem and regenerate these pages and the privacy notice. It does not update the digital books. If re-running the generator, review all generated pages before deploying.

## Validation
Static HTML links, form labels, age and consent checkboxes, default disabled state, JS syntax and configuration gate have been checked. No live provider submission was conducted because H has not supplied connected form endpoints; browser/device tests remain to be completed.
