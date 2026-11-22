# The Book of Chance — Website Prototype v0.4

**A GitHub Pages-ready static site** for the complete illustrated book, its free digital formats, and the developing Fellowship of Chance.

## What changed in v0.4

- **New faithful circular-lattice identity:** the large header and footer mark is based on the founding sketch (a circle crossed by straight diagonal paths), with restrained blue accents. The browser favicon, standalone vector, social/avatar-size image and header now use the same design. The mark is kept as editable SVG at `assets/logo-master.svg`.
- **Fellowship page:** `/community/` now explains the proposed community's purpose, values, genuine relationship-building, mentorship, collective projects, support priorities and the future Follower/Member/Senior Member structure. This is an inviting explanation **without pretending the community has already opened**.
- **Expandable library:** `/downloads/` is now a catalogue. The Book of Chance remains the featured available publication; future categories for reflections, guides and further writings are clearly labelled as **in development**, not available for download.
- **Catalogue source:** Edit `source/publications.json` to manage available and planned publication entries. Existing EPUB/PDF files are unchanged.
- **Navigation:** A clearly named *Fellowship* destination and a *Library* destination have been added to desktop and mobile menus, and the homepage now links to the community vision.
- The complete manuscript, 12 readings, all six book illustrations, covers, EPUBs and PDFs are **unchanged** from v0.3.

## Install on GitHub Pages

1. **Extract the ZIP**. It contains the site files at its top level (`index.html`, `assets/`, `community/`, `read/`, `downloads/`, `print/`, `about/`, `files/`, `source/`, `scripts/`).
2. Upload those files and folders into the **root** of your existing `TheBookOfChance` website repository, replacing older files with the same paths. Do **not** upload the ZIP itself or nest everything in another directory.
3. Wait for GitHub Pages to deploy, then open `https://thebookofchance.github.io/` and test the Fellowship and Library links. If the old favicon persists, force-refresh or test in a private browsing window; browsers cache icons aggressively.
4. Test at phone width and on desktop. The logo is now larger, and the navigation switches to a menu on smaller screens.

## Future publishing additions

`source/publications.json` includes the current book plus three future categories. To publish another work:

1. Place **real files** in `files/` and the real cover artwork in `assets/covers/` (or another stable asset path).
2. Add an `available` entry with title, subtitle, summary and edition file paths, following the existing example. The generator validates that referenced EPUB/PDF files exist.
3. Run `python -m pip install -r scripts/requirements.txt` once, then `python scripts/build_site.py` in the project root to rebuild the catalogue and site pages.
4. Don't list an unpublished work as downloadable. Keep plans under the `planned` group until actually released.

**Note:** `build_site.py` regenerates the static site pages from `source/manuscript.md`, its cover/artwork source files and `source/publications.json`. It does not remake EPUB/PDF files, change the manuscript or accept any user data.

## Important readiness boundaries

The site is a **prototype**, not an active Fellowship enrolment or fundraising service. There is **no member signup, live interest register, email collection, donation processor or paid pre-order form**. The future member spaces, mentorship services, Local Fellowships and support arrangements described on `/community/` have not launched. Members are intended to be adult (18+) with free registration when ready. The website remains open to readers of all ages without registration.

The book and its digital downloads remain freely accessible. PDFs are still labelled reader proofs because physical-print and final digital-accessibility checks are outstanding. Official Member registration, privacy policies, safeguarding and service procedures should be completed **before** a real signup form is added.

The local preference on `/print/` only records a cover choice in the visitor's browser; it is not a reservation.

## Local testing

Run a simple HTTP server from the extracted site root:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`. No framework, remote fonts, analytics, accounts or application server are required. Reading preferences are stored locally in the browser.

## Files worth knowing

| Path | Purpose |
| --- | --- |
| `index.html` | Book-led homepage, with a discreet link to the Fellowship |
| `community/index.html` | New Fellowship community overview |
| `downloads/index.html` | Expandable publication catalogue |
| `source/publications.json` | Data for available and planned publications |
| `assets/brand-mark.svg` | Clean symbol for use within the website |
| `assets/logo-master.svg` | Editable standalone emblem reference |
| `assets/favicon.svg` | Browser favicon |
| `assets/brand-avatar-512.png` | Large square icon for profiles and phone shortcuts |
| `scripts/build_site.py` | Rebuilds pages from the manuscript and catalogue |
| `SITE_QA_REPORT.json` | Automated checks and remaining limitations |

**Visual-browser testing remains a manual launch gate:** the browser automation runner in this environment is blocked from local pages. Static HTML, link, asset and JavaScript validation can still be completed.
