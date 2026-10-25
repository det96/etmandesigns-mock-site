# Logo concepts for Mid-State Plumbing, Inc.

Four refresh directions for an EtmanDesigns pitch. These are concepts only. They do not replace `assets/logo.png`, nothing here is deployed, and the business has not been contacted.

The company name on every lockup is exactly **Mid-State Plumbing, Inc.** There is no tagline, year, or claim. The orange bar in the panhandle is a pipe coupling, not a map of where they work.

Lockups use the site navy `#1a4a61` and safety orange `#E85D04`.

Wordmarks are outlined from Inter (SIL Open Font License). The SVG files do not need the font installed. Open any `.svg` from disk.

## How to look

- Full lockups: `logo-light.svg` on white, `logo-navy.svg` on navy. PNG previews are 1200px wide.
- Square icon: `icon.svg`, with `icon.png` at 512px. `icon-32.png` and `icon-16.png` are the same icon at those sizes.
- Side-by-side board: `comparison.png` (source layout in `comparison.html`).
- Header test, without changing the real logo: open `../index.html?logo=a` (or `b`, `c`, `d`). The query only swaps the header image.

## Concept A — State Line

A solid Florida silhouette, the shape already on their current logo, redrawn as a flat mark. An orange coupling sits in the panhandle so the mark reads as plumbing hardware rather than a tourism graphic.

## Concept B — Schematic

Right-angle pipe runs, one of them safety orange, with the same joint dots as the hero drawing on the concept site. It is the most literal “commercial construction plumbing” mark.

## Concept C — Monogram

A heavy MSP. M and P are block letters. The S is an orange pipe bend, so the monogram is also a fitting.

## Concept D — Field Badge

A chamfered square stamp, the kind of plate that shows up on a submittal or a truck door. Inside it is an orange pipe elbow and a joint.

## Recommendation

Use **Concept A, State Line**, in the header (`index.html?logo=a`).

They already identify as a Florida firm, and the current logo is the state. State Line keeps that recognition and makes it solid enough for a general-contractor bid set, a hard hat, and a small icon. The orange piece is a coupling, not a service-area line. Concept B is the one to show second if they want the logo and the website drawings to be the same picture. It is also the clearest of the four at 16px.

## Small-size check

Each icon was rendered at 32px and at 16px.

- State Line still reads as the state, with the orange coupling visible in the panhandle.
- Schematic still reads as two pipe runs, one orange.
- Monogram still reads as MSP. The counters get tight at 16px, which is expected for three letters.
- Field Badge still reads as a stamp with an elbow inside.

## Files

| Concept | Light | Navy | Icon | Header cut |
| --- | --- | --- | --- | --- |
| A State Line | `a-state-line/logo-light.svg` | `a-state-line/logo-navy.svg` | `a-state-line/icon.svg` | `a-state-line/logo-header.svg` |
| B Schematic | `b-schematic/logo-light.svg` | `b-schematic/logo-navy.svg` | `b-schematic/icon.svg` | `b-schematic/logo-header.svg` |
| C Monogram | `c-monogram/logo-light.svg` | `c-monogram/logo-navy.svg` | `c-monogram/icon.svg` | `c-monogram/logo-header.svg` |
| D Field Badge | `d-field-badge/logo-light.svg` | `d-field-badge/logo-navy.svg` | `d-field-badge/icon.svg` | `d-field-badge/logo-header.svg` |

`logo-header.svg` is the navy-header version with no background plate, so it can sit on `#1a4a61`. `build_logos.py` rebuilds the SVGs.
