# The Book of Chance — Website Prototype v0.1

**Status:** Working static-site prototype. Not a live public publication or an active pre-order system.

A minimal, responsive digital home for *The Book of Chance* by H, built from the actual approved covers and illustrated manuscript. No frameworks, analytics, remote fonts, user accounts or paid services are needed to run the website.

## What's included

| Area | Implemented |
| --- | --- |
| Home | Book introduction, **actual** Light and Dark covers, three parts, prominent reading/download actions |
| Read | **Full illustrated manuscript**, all 12 readings, original parables, front/back matter and six figure captions; individual shareable chapter URLs |
| Reader preferences | Light/dark theme, adjustable font size, local reading progress, local bookmarks, previous/next chapter links |
| Reader directory | Contents grouped by part, title/full-text search (from generated local index), resume-reading action |
| Downloads | Final *candidate* Light/Dark EPUB files plus Light/Dark illustrated PDF **reader proofs**; no sign-up |
| Physical edition | Two cover choices with a local-only preference and clear future print campaign explanation |
| About | Confluent Humanism, intellectual influences, H, and a discreet, accurate Fellowship note |

There is **no live interest form** and no user email information is collected. The print page cannot take a reservation or payment. It only saves the selected cover on the visitor's own device.

## Run it locally

The pages use normal static directory links (`read/arrival/`) and a local JSON search index. Use a local web server rather than opening `index.html` directly from the file system.

From inside the extracted project directory:

```bash
python -m http.server 8000
```

Then open **http://localhost:8000** in your browser. Node users can alternatively run `npx serve .` if they already have that tooling.

## Upload to GitHub Pages

1. Create a public GitHub repository for the site.
2. Extract this ZIP **and upload the contents of the `Book_of_Chance_Website_Prototype_v0.1` folder into the repository root**. The `index.html`, `assets/`, `read/`, `downloads/`, `print/`, `about/` and `files/` directories should be at the top level.
3. In **Settings → Pages**, select *Deploy from a branch*, your default branch, and the repository **root**. (Exact labels may differ.)
4. Open the published URL and test reader links, images, downloads and search. All internal links use relative paths and therefore work on a project URL such as `username.github.io/repo-name/`.
5. If adding a custom domain later, configure DNS, HTTPS and the domain name separately.

This is a static site; **GitHub Pages will not process email submissions or payments**. Connect an approved interest-registration provider later if you want real sign-ups.

## Editing the book and rebuilding chapter pages

The complete book source is at `source/manuscript.md` (copied verbatim from the illustrated standalone manuscript v0.11). The chosen source covers and artwork are in `source/covers/` and `source/artwork/`.

To regenerate the static chapter pages and web-optimised images after updating the Markdown:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_site.py
```

The generator retains the complete reading prose and six approved illustration/context pairings, and updates the local search index. It **does not regenerate the EPUB or PDF files**; these are provided in `files/` and can be replaced with new independently verified publication files after a manuscript revision.

The website styling lives in `assets/site.css` and behaviour in `assets/site.js`. The site is dependency-free at runtime. The generator is specifically mapped to the current 24-section manuscript structure; update the section mapping if a later edition adds or removes chapters.

## What requires completion before a public launch

- Choose and add final legal/copyright and contact information, if required, and confirm author rights in the text, images and covers.
- Complete independent ebook device/accessibility checks, EPUBCheck if distributing through retailers, and a final accessible **digital PDF** export. The existing PDFs are labelled reader proofs on purpose.
- Decide whether the site will later include a real interest form, and publish a privacy notice for the data it collects before enabling submissions. A privacy notice is **not yet needed for a backend that does not exist**; there is currently no analytics or remote form service.
- Confirm the eventual paperback print costs, threshold, deadline, refund policy and shipping arrangements **before** accepting money.
- Test the site in desktop and mobile browsers, including reader controls, actual EPUB/PDF downloads and assistive technologies.
- Add a contact route or support email once there is a real, maintained address.
- Consider a formal declaration of the book's edition/date once the public release is approved.

## Privacy and reader independence

- No accounts, cookies, analytics, web tracking or external content requests are included.
- Theme, font size, bookmarks and reading progress use **localStorage on the device only**. The site does not send that data anywhere.
- All foundational teachings are accessible without payment or membership.
- The Fellowship is mentioned discreetly as a proposed community, not as a sign-up requirement or functioning service.

**Editorial source:** *Book_of_Chance_Illustrated_Manuscript_v0.11.md*, approved Light and Dark covers, and EPUB candidate v1.0. PDF proof files are derived from the v0.11 illustrated paperback reader previews.
