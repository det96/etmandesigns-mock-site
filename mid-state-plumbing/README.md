# Mid-State Plumbing — concept redesign

This is a pitch concept for EtmanDesigns (David Smith’s Houston web design studio). It is **not** the official Mid-State Plumbing website, and it is not published.

The page is meant to be shown to the contractor. Unknown details are designed blanks (“To be added”, “Featured project”, “Project photo”, “Office map”). Fill each one with a confirmed fact after the conversation.

Search engines are asked to skip the page (`noindex, nofollow`). Nothing here is deployed.

## How to open it

1. Open the `mid-state-plumbing` folder.
2. Double-click `index.html`.
3. It loads from disk (`file://`) in a browser. Desktop Chrome on Windows is the setup this was built for.

No server, install, or build step. Fonts are system fonts (Segoe UI and the usual fallbacks). Images and styles use relative paths. The script is a plain file, not an ES module.

In-page links glide to the section and sit below the sticky header. That glide still runs when Windows reports reduced motion, because Chrome turns off CSS smooth scrolling in that mode.

The bid form is a demonstration. It does not send email, save a file, or contact Mid-State Plumbing. Submitting it only shows what you typed, on this page.

Careers buttons open the live posting and the live application PDF on `mid-stateplumbing.net`. Those two links need a network connection. The rest of the page does not.

## Sources (fetched 25 October 2026)

Their current logo, kept for the before view: [https://mid-stateplumbing.net/logo.png](https://mid-stateplumbing.net/logo.png) → `assets/logo.png`.

The concept page itself uses **Concept A, State Line** in the header and the footer. Both bars are navy, so the image is the reversed lockup `logo-concepts/a-state-line/logo-header.svg` (no extra background plate). The favicon is that concept’s icon: the SVG, a 32px PNG, and a 180px apple-touch icon. Open the file from disk; the icon links are relative.

During the pitch, `index.html?logo=original` puts `assets/logo.png` back in the header, the footer, and the favicon. `?logo=b`, `?logo=c`, and `?logo=d` still preview the other concepts. `?logo=a` is the same as opening the page with no flag.

Colors taken from that page’s CSS:

| Hex | Where it appears on the current site |
| --- | --- |
| `#2c5f7c` | Links, headings accent, gradient start, info-rule |
| `#1a4a61` | Dark heading color, link hover, gradient end |
| `#e8f4f8` | Highlight panels |
| `#333333` | Body text |
| `#555555` | Secondary text |

The logo file is a white wordmark and a pipe drawn in about `#185878` (sampled from the PNG) on a transparent background. It is shown on `#1a4a61` so the wordmark stays visible.

The concept adds one accent, safety orange `#E85D04`, for buttons, rules, icons, and the hero pipe drawing. Button labels use `#1A1208` so the type stays readable on that orange. Small orange text on light backgrounds uses `#C2410C`. Highlights on navy use `#FFB07A`. There is no stock photograph. The hero drawing and the project thumbnails are original SVG line art, not pictures of Mid-State’s work. The hero labels that drawing “Schematic. Not a project photo.”

Hours, receptionist line, appointment note, phone, address, and the careers posting (including pay, requirements, benefits, and the application link) are taken from [https://mid-stateplumbing.net/](https://mid-stateplumbing.net/) and [https://mid-stateplumbing.net/careers.html](https://mid-stateplumbing.net/careers.html). The application file linked from that page is [https://mid-stateplumbing.net/english-application.pdf](https://mid-stateplumbing.net/english-application.pdf).

Also used, as given for this concept: the office is in DeBary, Florida, north of Orlando, and the buyers are general contractors. The company does commercial construction plumbing only.

## Placeholders to fill

On the page these read as tidy pills (“To be added”), photo frames, or the title “Featured project”. Replace each one with a real fact. Do not leave a pill in place of a number you have not confirmed.

### Three project cards (each card)

- **Featured project** — the real project name. The 01 / 02 / 03 marks are layout slots, not project numbers.
- **Project photo** — a photograph of that project. The blueprint drawing is a stand-in, not their work. The “Commercial” tag only repeats that they do commercial construction.
- **Project type** — building or project type
- **Location** — where that project is
- **Client** — general contractor or client, only if they are willing to be named

### Capabilities

- **Other systems** — plumbing systems beyond water supply, waste, and vent, if they want them listed
- **Typical project size** — the size range they want to show

### Why GCs choose us (stat band)

These sit where a number would go. They read “To be added”. Nothing here is counted or animated.

- **Years in business**
- **Projects completed**
- **Crew size** — the careers posting’s two-person crew is that one job, not a company headcount
- **References**

Years in business, crew size, and references are the same blanks as on the prequalification sheet.

### Prequalification sheet

- **License #**
- **Insurance**
- **Bonding**
- **Years in business**
- **Safety certifications** — company credentials. OSHA 10 or 30 on the careers section is only a preferred qualification for the job applicant, not a company certification.
- **References**
- **Crew size** — the careers posting describes a two-person crew for that one job. That is not a company headcount.
- **Service area** — the office is in DeBary, north of Orlando. Anything beyond that is still open.
- **Contact name** — who a general contractor should ask for. No team names were added.

### Contact

- **Email**
- **Office map**

## Left off on purpose

No testimonials, star ratings, client logos, project statistics, “years in business” figure, license number, bonding claim, or crew-size claim. Those were not on the current site, so they are not written as if they were. Add them in the slots above when they are real.
