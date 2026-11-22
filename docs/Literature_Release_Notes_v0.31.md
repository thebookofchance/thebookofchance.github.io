# Literature digital release — v0.31

**Release approved by:** H, as confirmed in the project conversation on 23 November 2026.  
**Site baseline:** v0.30 production corrections.  
**Release date:** 23 November 2026.  
**Format:** Publicly available digital literature (HTML, PDF and EPUB), not commercial print editions.

## Scope

Nine published Library works: *The Book of Chance* (Light/Dark), three *Letters from H*, *The Five Values*, *Conversations of Chance*, *The Little Book of Possibilities*, *The Parables of Chance* and *A Beginner's Guide to Confluent Humanism*. The separate *Questions About Chance* FAQ is also released.

## Changes

- Removed misleading editorial-candidate/revision-awaiting-approval notices from the current public pages, PDF/EPUB release matter and publication metadata while preserving each work's philosophical content and original revision history.
- Recorded H's author approval, prepared release register with the current file hashes, and maintained H's byline and appropriate AI-assistance disclosures.
- Kept the approved cover art and every reader-facing download path. Existing filenames containing `Editorial_Proof` remain only for URL continuity and do not represent current publication status.
- Removed `noindex` from five formerly staged canonical publication/FAQ pages plus the Guided Reading Journey, and added these routes to the public sitemap.
- Retained `noindex` on `/reader/`, because it intentionally duplicates texts from canonical pages.
- Updated site-building code to reapply released status automatically after old generator stages, preventing reappearance of editorial-candidate labels on a fresh build.
- Made no changes to forms, private form endpoints, the privacy policy, pending Fellowship governance, donations or membership systems.

## Verification

See `docs/Literature_Release_QA_v0.31.json`: 45 HTML pages and 1,391 local-file link references inspected, 246 anchor links checked, zero broken links; eleven PDF/EPUB edition pairs passed structural checks; no old editorial-candidate language in current public literature; revised sitemap correct.

## Qualifications

H has approved the work for digital release and reports that the forms work. This is **not** a claim of PDF/UA certification, independent human editorial endorsement, legal clearance for commercial republication, or validation of a registered Fellowship. Further assistive-technology testing would improve accessibility assurance. The GitHub Pages deployment must still be checked after this patch is uploaded; search engines may take time to index new pages.
