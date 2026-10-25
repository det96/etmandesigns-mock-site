# Ethan Clark Air Conditioning — concept redesign

Private pitch mock-up for EtmanDesigns (David Etman). This is not the live site, it is not deployed, and it does not use analytics.

Preview it the way David will: double-click `index.html` so it opens in desktop Chrome (`file://`). No build step and no network fonts. Syne and Outfit are self-hosted in `fonts/` under the SIL Open Font License (see the OFL text files beside the fonts).

The page sends `noindex, nofollow`. Do not turn on GitHub Pages for this folder.

## Facts used

Taken from the brief and from the public pages on [ethanclark.com](https://ethanclark.com/) (home and about) in October 2026:

- Ethan Clark Air Conditioning, Houston HVAC, since 1987
- Joseph started the company in 1987. Second-generation history, Stratford High School HVAC training, full time in 1990, shop downtown off I-10 in the mid-1990s, residential shift inside the loop, service manager in 1998, Melissa as office manager
- Texas Air Conditioning License TACLA 26626E
- 1320 Rothwell Street, Houston, Texas 77002
- (713) 236-1119 — call `tel:+17132361119`, text `sms:+17132361119`
- ethanclarkac@gmail.com
- 5.0 from 173 Google reviews (shown in the hero; quotes are not invented)
- Service list, “why call or text” lines, brand names, card names, service-area cities, and the texting consent line are copied from the current site

The narrator on the current about page is not named there, so this concept does not add a name.

## Placeholders to fill

- [ ] **Google review quotes (3 cards).** Each card says “Customer review to be added from Google”. Paste real Google text only. Do not write or paraphrase reviews.
- [ ] **Recheck the rating before anything public.** The hero shows 5.0 and 173 Google reviews from this brief. Update both if Google has changed.
- [ ] **Shop photo.** Labeled “Shop photo to be added”. Use a real photo of the downtown shop. No stock photos of people.
- [ ] **Second photo.** Labeled “Photo to be added”. Team or job photo from the client, or remove the frame.
- [ ] **Hours.** Contact row says “Hours to be confirmed”. The current site does not list hours.
- [ ] **Map.** The contact block says “Map to be added”. Drop in a static map image or an embed for 1320 Rothwell St, Houston, TX 77002.
- [ ] **Which email is public.** This concept uses `ethanclarkac@gmail.com` as specified for the pitch. The live privacy policy and terms (updated May 26, 2026) list `eclarkac@gmail.com`. Confirm before launch.
- [ ] **Service-area list.** The nine “City of …” names are copied from ethanclark.com. Confirm they are still right. Do not add cities that are not on that list.
- [ ] **Request form.** Marked “Demo only”. It does not submit, store, or send. Wire a real handler later, or keep it as a call-to-call until then.
- [ ] **Logo.** The header mark is a stand-in. Replace it if the shop has a logo file.
- [ ] **Favicon.** `favicon.svg` and `favicon.png` match the stand-in mark. Swap both if the logo changes.
- [ ] **Privacy policy and terms.** Footer links go to the current live pages. Write new ones if this design replaces ethanclark.com.
- [ ] **Videos and articles (optional).** The current site has a videos page and an articles page. They are not repeated here.
- [ ] **Do not invent** prices, awards, guarantees, response times, review counts, or extra service areas. The “why call” lines are the shop’s own wording, including “workman's compensation” and “You know the price before the work starts.”
- [ ] **Card brands.** Discover, Mastercard, American Express, and Visa are named from the current site’s card-logo description. Artwork is not included.
- [ ] **Texting consent.** The call-now band repeats the current site’s SMS notice. Keep it if the text link stays.

## Files

- `index.html` — the page
- `styles.css` — layout and the ice / Houston-sun theme
- `script.js` — menu, demo form, scroll fade-ins, and in-page smooth scrolling
- `favicon.svg`, `favicon.png`
- `fonts/` — Syne and Outfit, plus their OFL licenses
