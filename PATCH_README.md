# The Book of Chance — Website v0.14 (update-only patch)

This update addresses issues raised in the simulated cross-publication reader stress test.
It includes only files changed or added since the v0.13 website; it is not a fresh install.

## Install

1. Your GitHub repository should already contain v0.13.
2. Extract the ZIP and upload its contents into the **root** of the existing repository. Preserve folder paths.
3. Replace matching files. Do **not** delete unrelated files.
4. Verify the updated book and Letters online and download one PDF and one EPUB.
5. Confirm your existing forms still work, as this patch does not include form credentials.

## Edited content

- `source/manuscript.md` plus matching Book of Chance Light and Dark PDFs/EPUBs.
- The three Letters' canonical Markdown, online pages, PDF/EPUB exports and catalogue statuses.
- Four journal PDFs and three A4 sheets, focusing on privacy, pausing and shared-device instructions.
- Reader and Library copy, search index, relevant generation scripts, roadmap and editorial change log.

## Preserved

The official logo, original cover artwork, illustrations, membership/fundraising status and configured Formspree endpoints are not changed.

## Limitations

No human reader test was performed. The PDF forms passed programmatic save/reopen tests only, not multi-device or screen-reader certification. This is an editorial revision, not a claimed independently approved or fully accessibility-tested release.

See `docs/Editorial_Corrections_v0.14.md` for the detailed decisions, and `docs/Editorial_Corrections_v0.14_QA.json` for the machine-readable test results.
