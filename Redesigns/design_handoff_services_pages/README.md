# Handoff: Extreme Heating services pages

## Overview
New page system for all service content on extremeheating.com, matching the approved homepage redesign (see `design_handoff_homepage_redesign/`). Three page tiers:

1. **Services hub** — all-services listing per trade (`/services`, `/plumbing/services`).
2. **Service detail** — one core service, conversion-focused (e.g. `/air-conditioning`, `/plumbing/water-heater/overview`).
3. **Sub-page** — a leaner child of a detail page (e.g. `/furnace-repair`, `/plumbing/water-heater/repair`).

## About the Design Files
`Services Mockups.dc.html` is a **design reference built in HTML** — it shows intended look and behavior, it is NOT production code. Recreate the designs in the existing codebase using its routing and data patterns (see Target codebase structure below). Do not ship the mockup HTML. Open the file in a browser (keep `support.js`, `image-slot.js`, `assets/` beside it); screens sit on a pannable canvas with monospace badges.

**Approved screens (turns 3 + 2, top of canvas):**
- **3a** — X-Plan maintenance/membership page, desktop 1280 (`/maintenance`)
- **2a** — Service detail, desktop 1280 (Air Conditioning example)
- **2b** — Service detail, mobile 390 (same page)
- **2c** — HVAC services hub, desktop 1280
- **2d** — Sub-page, desktop 1280 (Furnace Repair; shows sibling pill nav)
- **2e** — Plumbing detail with sub-pages, desktop 1280 (Water Heater Overview)

Turn 1 (1a/1b/1c, lower on canvas) is exploration history — **ignore it**; 1b was explicitly rejected.

Rule of thumb: 2a/2b are the source of truth for the detail template (desktop/mobile); 2c for hubs; 2d for sub-pages; 2e for how detail + pill nav combine on plumbing overview pages; 3a for the X-Plan membership page. Mobile for 2c/2d/2e/3a was not mocked — stack per 2b's rules (see Mobile stacking below).

## Target codebase structure & file mapping
Repo layout (as provided by the client, July 2026). Service pages are per-route `.html` files; multi-child services are folders holding their sub-pages.

```
assets/
Footer/                      ← homepage handoff screens 3a/3b
Header/                      ← homepage handoff 2c/2d — use the solid #5E2C7E variant on all service pages
Homepage/                    ← homepage handoff 2a/2b
HVAC Service Pages/
  services.html              ← mockup 2c (HVAC hub)
  air-conditioning.html      ← mockup 2a (desktop) / 2b (mobile) — detail template
  furnace-heating.html       ← 2e pattern: detail + pill nav (Overview active; pills: Overview / Installation / Repair)
  furnace-installation.html  ← 2d pattern (Installation pill active)
  furnace-repair.html        ← mockup 2d (source of truth)
  heat-pump.html             ← detail template (rollout, step 6)
  duct-cleaning.html         ← detail template (rollout)
  thermostat.html            ← detail template (rollout)
  humidifier.html            ← detail template (rollout)
  inspection.html            ← detail template (rollout)
  indoor-air-quality.html    ← 2e pattern; pills: Overview / Solutions / Importance / FAQ
  indoor-air-quality-solutions.html, importance-iaq.html, iaq-faq.html
                             ← 2d pattern (respective pill active)
  maintenance.html           ← mockup 3a (X-Plan membership page) — every X-Plan promo/panel across the site links here
Plumbing Service Pages/
  services.html              ← 2c with the plumbing swaps (see Hub template)
  clogged-drain.html, emergency-plumbing.html, leak-detection.html,
  toilet-repair.html, water-treatment.html
                             ← detail template, no pill nav
  water-heater/              ← mockup 2e (overview — source of truth) + 2d pattern (repair, installation)
  sewer-line/                ← 2e (overview) + 2d (repair, cleaning)
  sump-pump/                 ← 2e (overview) + 2d (repair, installation)
  gas-line/                  ← 2e (overview) + 2d (repair, installation)
  apple.tsx                  ← unrelated to this work; leave untouched
ScheduleEngine/              ← booking flow — wire every "Schedule Service" CTA to this (see URL map)
Theme.tsx                    ← shared tokens; add/confirm the tokens from this handoff here
```

Build the shared section components following the same conventions as `Header/`, `Footer/`, and `Homepage/`, then apply them per file according to the tier mapping above. Routes map 1:1 to these file/folder names.

## Architecture: build 3 templates, not 25 pages
Every service page is one of the three tiers fed by a per-service data object. Suggested shape:

```ts
type ServicePageData = {
  trade: 'hvac' | 'plumbing';
  breadcrumb: {label: string; href: string}[];   // last item green, unlinked
  h1: string; h1Highlight: string;               // highlight = green italic span
  intro: string;
  heroChips: [string, string, string];
  bookingCard: {eyebrow: string; title: string; sub: string}; // detail tier only
  pillNav?: {label: string; items: {label: string; href: string; active: boolean}[]};
  symptoms: {eyebrow: string; h2: string; items: string[6]; callout: string}; // callout may be `safety` variant (ink bg, 2d)
  whatWeDo?: {h2: string; cards: {title: string; desc: string; href: string}[3]};
  process: {steps: {title: string; desc: string}[3]};
  faq: {q: string; a: string}[3-4];
  rail: {photoSlot: boolean; promos: Promo[2]};   // Promo = financing | xplan | scheduleFast | specials
  emergencyBand: {bold: string; rest: string};
  related: {title: string; href: string}[3];
};
```

Shared section components to build once (names indicative): `ServiceHero` (with optional `BookingCard` overlap), `PillSubNav`, `SymptomChecklist`, `WhatWeDoCards`, `ProcessSteps`, `ServiceFAQ`, `EmergencyBand`, `ServiceRail` (photo + 2 promo cards), `RelatedServices`, plus hub-only `CoreServiceGrid`, `AdditionalServiceRow`, `XPlanPanel`, `CrossLinkCards`. Header and Footer come from the homepage handoff (screens 2c/2d/3a/3b there) — header here is the **solid `#5E2C7E`** variant (not transparent-over-hero).

## Tier anatomy

### Detail template (2a desktop / 2b mobile)
Desktop, top→bottom: solid header → purple-gradient hero (breadcrumb; H1 46px italic 900 with green phrase; intro ≤520px; 3 glass chips) with **booking card** in a 360px right column, `margin-bottom:-84px` so it straddles into the white body → body grid `1fr 360px`, gap 48, padding 56px 40px → left column: SymptomChecklist → WhatWeDoCards → ProcessSteps → ServiceFAQ (first item open) → right rail (`padding-top:64px`): photo (h220 r14) + 2 promo cards → EmergencyBand (ink) → RelatedServices strip (`#F7F6FA`) → footer.
- Booking card: white, r16, `0 20px 50px rgba(15,23,42,.25)`, padding 24. Green eyebrow → title 800 18 → sub 13 → green Schedule btn (glow `0 6px 18px rgba(107,184,92,.35)`) → purple `#542770` Call btn → hairline → "★ 4.9 on Google | 20+ years local". If sticky-on-scroll is added later, cap with `position:sticky; top:16px` on the rail — optional enhancement, confirm with design owner.
- Checklist item: 18px circle `#6BB85C`, white ✓ 10px 800, label 13.5px 700 `#475569`; 2-col grid, gap `12px 24px`.
- Callout: `#EEF7EC`, r12, 13px 600 `#3D7A33`, bold phone inline.
- What-we-do card: 1px `#E7E7EA`, r16, padding 20, 30px X glyph, title 800 16.5, desc 13.5/1.55, "Learn more →" 800 13 purple.
- Process: number italic 900 25px `#542770` ("01/02/03", 44px col) + title 800 15 + desc 13.5.
- FAQ row: 1px `#E7E7EA` r14 padding 16px 18px; toggle circle 26px (open: `#542770` bg white "−"; closed: `#F4F1F8` purple "+"); answer 13.5/1.6 max 620px.
- EmergencyBand: `#0F172A`, padding 20px 40px; bold white 15px + muted 13px; green Call button right.

Mobile (2b): same order stacked at 390/padding 20; mobile header (logo h32 + 44px green ✆ + 44px outline hamburger); hero CTAs full-width stacked; diagonal cut 44px/55%; what-we-do and related become divider list-rows (`#F1F0F4`, → arrows); rail content flows inline after Process (photo → financing → X-Plan); **pinned bottom bar**: `rgba(15,23,42,.97)`, top hairline `rgba(255,255,255,.12)`, padding 10px 16px, green "Schedule" + outline "✆ Call" (flex 1 each, ≥44px) — sticky at viewport bottom on all mobile service pages.

### Hub template (2c)
Solid header → hero grid `1fr .9fr` (glass pill eyebrow; H1 44px; intro; green + outline CTAs; right: photo h280 r20 on green slash `rotate(-9deg) skewX(-16deg)` with 25%-white offset bar) → 84px diagonal cut → promise strip → CORE SERVICES 3×2 bordered-card grid (last cell = `#F4F1F8` "Not sure what you need?" phone card) → `#F7F6FA` X-PLAN & ADDITIONAL 4-card row (Maintenance Plans carries green `X-PLAN` badge `#EEF7EC`/`#4E9B41`) → X-Plan gradient panel (chips + $249/yr | $20.75/mo + Join X-Plan) → 2-col cross-link cards (Financing `#F4F1F8` purple / other-trade `#EEF7EC` green) → footer.
- Plumbing hub (`/plumbing/services`): same template. Core: Clogged Drain, Water Heater, Sewer Line, Sump Pump, Gas Line + "Not sure" card. Additional: Emergency Plumbing, Leak Detection, Water Treatment, Toilet Repair. Cross-links: "Need Plumbing Help Fast? → /contact" style promos swap to Financing + "Need HVAC instead? → /services". Skip the X-Plan panel or keep — X-Plan is HVAC-flavored; confirm with marketing (default: replace with Plumbing Specials band → /specials).

### Sub-page template (2d)
Solid header → **compact** hero (breadcrumb with parent; H1 42px; intro; Schedule Repair + Call Now; inline trust row "★ 4.9 · ◆ 20+ years · ◆ 24/7"; flat bottom, no diagonal, no booking-card overlap) → **pill sub-nav bar** (white, bottom hairline `#E7E7EA`; muted 10.5px group label + pills: active `#542770` bg white 800, inactive `#F4F1F8` purple 700, r999, padding 8px 16px) → body grid `1fr 360px` → left: SymptomChecklist (safety variant callout allowed: ink `#0F172A` bg, `#8FD481` "Safety first:" lead — used for gas/CO on furnace pages) → ProcessSteps → optional decision card ("Repair or replace?" bordered card with outline-purple link btn) → ServiceFAQ (3) → rail: **booking card at top** (no hero overlap) + X-Plan promo + sibling-links card → EmergencyBand → footer. RelatedServices strip optional — siblings already live in the rail.

### 2e (plumbing overview) = detail template + pill nav
Water Heater Overview proves the combo: detail anatomy (booking-card hero, rail, emergency band, related) with the pill bar (`Overview` active / Repair / Installation) directly under the hero. Use this for every plumbing service that has children (water heater, sewer line, sump pump, gas line) and for `/furnace-heating` and `/indoor-air-quality` on the HVAC side. Plumbing rail promos: "Need plumbing help fast? → Schedule" (`#F4F1F8`) + "Plumbing specials → View Specials" (`#EEF7EC`).

### X-Plan membership page (3a) = detail template, membership-flavored
`maintenance.html` reuses the detail anatomy with these swaps:
- **Pricing card** replaces the booking card (same position, hero overlap `-84px`): green eyebrow `X-PLAN MEMBERSHIP` → price row (italic 900 38px `$249` + `/ year` 700 14 `#475569`) → "or $20.75 / month · per system" → green **Join X-Plan** btn → purple Call btn → hairline → "Cancel anytime | No enrollment fee".
- Hero chips state the top 3 benefits (2 Tune-Ups a Year / 15% Off Repairs / Priority Scheduling) instead of trust stats.
- **Benefits grid** replaces SymptomChecklist: 6 bordered cards (r16, padding 18), each led by an 18px green check circle — two tune-ups · 15% off repairs · priority scheduling · 5-yr repair warranty · discounted service calls · warranty compliance.
- **Use-case cards** ("Is X-Plan for you?") use the what-we-do card pattern with X glyphs: system 5+ yrs old / new system warranty / past surprise breakdown.
- **Value panel** ("Does it pay for itself?"): purple gradient r24 panel, `#8FD481` eyebrow, 3-col stats — italic 900 26px white stat + 12.5px muted caption (2× / 15% / $20).
- ProcessSteps = Join → We schedule your tune-ups → You save automatically. FAQ first-open = multi-system pricing. Rail promos: "Questions before joining? → tel:" (`#F4F1F8`) + "Due for a tune-up now? → ScheduleEngine" (`#EEF7EC`). Emergency band becomes a **Join band** ("Ready to stop worrying about breakdowns?" + green Join X-Plan btn → anchor to pricing card / join flow).
- No pill nav, no related-services strip.

## URL & backlink map
One source of truth for hrefs. Phone everywhere: `tel:18445847399`, display "(844) 584-7399". "Schedule Service" CTAs open the ScheduleEngine booking flow (repo `ScheduleEngine/`); the mockups' `/contact` target is the fallback where ScheduleEngine isn't wired.

HVAC — hub `/services`; details: `/air-conditioning`, `/furnace-heating` (children `/furnace-installation`, `/furnace-repair`), `/heat-pump`, `/duct-cleaning`, `/indoor-air-quality` (children `/indoor-air-quality-solutions`, `/importance-iaq`, `/iaq-faq`); additional: `/maintenance` (X-Plan), `/inspection`, `/thermostat`, `/humidifier`.
Plumbing — hub `/plumbing/services`; details: `/plumbing/clogged-drain`, `/plumbing/water-heater/{overview|repair|installation}`, `/plumbing/sewer-line/{overview|repair|cleaning}`, `/plumbing/sump-pump/{overview|repair|installation}`, `/plumbing/gas-line/{overview|repair|installation}`; additional: `/plumbing/emergency-plumbing`, `/plumbing/leak-detection`, `/plumbing/water-treatment`, `/plumbing/toilet-repair`.
Cross-page: financing promos → `/financing-options` · X-Plan promos/panels → `/maintenance` · specials promos → `/specials` · "Not sure" card → `tel:` · locations → `/locations`.

Backlink rules per screen:
- Breadcrumbs link every ancestor (2a "Heating & Air" → `/services`; 2e "Plumbing" → `/plumbing/services`); current page is green, unlinked.
- Pill navs (2d/2e) link all siblings incl. Overview (parent page).
- What-we-do `Learn more →` targets the closest real page. 2e: Repair → `/plumbing/water-heater/repair`, Install → `/plumbing/water-heater/installation`, Tankless → `/plumbing/water-heater/installation`. 2a has no dedicated AC child pages yet — until they exist: Repair → `/contact`, Install → `/financing-options`, Tune-Ups → `/maintenance` (revisit if AC children are added).
- 2a related → `/heat-pump`, `/duct-cleaning`, `/indoor-air-quality`. 2e related → `/plumbing/clogged-drain`, `/plumbing/sump-pump/overview`, `/plumbing/leak-detection`. 2d rail siblings → `/furnace-heating`, `/furnace-installation`, `/thermostat`.
- 2c core grid → each detail URL above; additional row → `/maintenance`, `/inspection`, `/thermostat`, `/humidifier`; "Plumbing Services" cross-link → `/plumbing/services`; "View All" style links between hero/footer → the hub.
- 3a: breadcrumb "Heating & Air" → `/services`; Join X-Plan CTAs → membership signup flow (confirm target — ScheduleEngine or form); "Due for a tune-up now?" → ScheduleEngine; "Questions before joining?" → `tel:`.
- Emergency bands and all Call buttons → `tel:18445847399`.

## Copy
All headline/body/FAQ copy in the mockups is **final-intent draft in the brand voice — treat the mockup text as the copy deck** and paste it verbatim; marketing reviews in staging. Placeholders to replace: image drop-slots (real tech/job photos), "4.9" Google rating (wire to live source), X-Plan pricing ($249 / $20.75 — confirm current).

X-Plan facts (client-confirmed, use exactly): members pay **discounted** service-call rates, not $0 — **$77 instead of $97** during normal business hours, **$177 instead of $197** for emergencies. Never claim "no overtime charges" or free service calls. Unconfirmed draft claims to verify before ship: per-system pricing, additional-system discount, tune-up-credit-toward-membership, 15% applying to plumbing repairs.

Copy formulas for rolling out to services not mocked (write in the same voice, then have marketing review):
- H1: benefit-first, italic 900, one green phrase. Pattern: "Fast, honest {service} in Dayton & Cincinnati." / problem-flip like "Hot water, back fast."
- Intro: 1–2 sentences, ≤300 chars: what we do + upfront pricing/locally-owned proof.
- Symptoms: exactly 6, homeowner-observable, 3–6 words each; callout = urgency + phone (green tint), or safety variant (ink) when gas/CO/flood risk.
- What-we-do: 3 cards — repair / install-replace / maintain-or-specialty; desc ≤120 chars ending in a differentiator.
- Process: always the same 3 beats — Book in minutes / Diagnose & quote upfront / Fixed right, guaranteed (adapt last beat per service).
- FAQ: 3–4; first = speed ("How fast…?" — open by default); others = repair-vs-replace, brands/compatibility, service-specific.
- Emergency band: "{pain moment}?" bold + reassurance + call button ("No heat tonight?", "Cold shower this morning?").

## Design tokens
Base tokens (colors, Montserrat scale, buttons, radii, shadows, X glyph, slash, diagonal cut, watermark) are identical to `design_handoff_homepage_redesign/README.md` — that file remains the token source of truth. New/notable here:
- Solid header: `#5E2C7E` (hero gradient starts at the same value, so header blends into hero).
- Pill sub-nav: active `#542770`/white 800; inactive `#F4F1F8`/`#542770` 700; 12.5px, r999, padding 8px 16px; group label 10.5px 800 ls1.8 `#94A3B8`; bar hairline `#E7E7EA`.
- Booking card + sub-page rail card shadow: `0 20px 50px rgba(15,23,42,.25)` (hero overlap) / `0 12px 30px rgba(84,39,112,.12)` + 1px `#E7E7EA` (in-flow).
- Check circle: 18px `#6BB85C`, white ✓.
- Safety banner: `#0F172A` bg, r12, body `rgba(255,255,255,.85)` 13px 600, lead-in `#8FD481` 800, phone white 800.
- Watermark: always inside an `overflow:hidden` layer, bled off the right edge (the PNG has a cropped "™" fragment on its right side — never show it).
- Promo cards (rail + hub cross-links) reuse the mega-menu promo pattern: `#F4F1F8` purple / `#EEF7EC` `#3D7A33`, r14, padding 18px 20px.

## Interactions & state
- FAQ accordion: `openIndex: number | null`, default 0, one open.
- Pill nav: route-driven, no state.
- Booking card buttons: Schedule → `/contact`, Call → `tel:`. Hovers per homepage tokens (green btn → `#4E9B41` + white text on light bg / `#8FD481` on dark; purple btn → `#3E1C54`; cards → shadow `0 12px 30px rgba(84,39,112,.12)` + border `#D8CCE4`; links → green).
- Mobile pinned bar: fixed, always visible on service pages; respect safe-area inset.
- Header mega-dropdown/hamburger: as specified in the homepage handoff; on service pages the trade's nav item may show active green — optional, confirm.

## Implementation plan (ordered)
1. **Shared components** — build the section components listed under Architecture, styled from 2a/2d/2e (desktop) + 2b (mobile). Reuse homepage Header (solid variant) and Footer as-is.
2. **Detail template + AC page** — assemble `/air-conditioning` from 2a/2b data; verify booking-card overlap, rail, emergency band, mobile pinned bar.
3. **Hub pages** — `/services` from 2c; then `/plumbing/services` with the swaps noted above.
4. **Sub-page template** — `/furnace-repair` from 2d (pill nav, safety banner, decision card); then `/plumbing/water-heater/overview` from 2e to confirm detail+pillnav combo.
5. **X-Plan page** — `maintenance.html` from 3a (pricing card, benefits grid, use-case cards, value panel, join band). Confirm the Join CTA target and the unconfirmed program claims listed under Copy before shipping.
6. **Rollout** — remaining pages are data objects only: HVAC details (heat-pump, duct-cleaning, furnace-heating, indoor-air-quality + children, thermostat, humidifier, inspection) and plumbing (clogged-drain, sewer-line, sump-pump, gas-line + children, emergency-plumbing, leak-detection, water-treatment, toilet-repair). Write copy via the formulas; keep FAQ first-item = speed question.
7. **QA pass** — every href against the URL map; single `tel:` constant; breadcrumb/pill active states; no watermark "™" fragment visible; mobile 44px targets; FAQ keyboard toggle; Lighthouse on 2–3 representative pages.

Review checkpoints: after steps 2, 3, 4, and 5 in-browser before the step-6 rollout.

## Assets (in `assets/`)
Same three as the homepage bundle: `logo-white.png` (dark bgs only), `x-mark.png` (watermark — clip per token note), `van.png` (not used on these screens). Photo drop-slots need real photos: detail rail (tech at unit), hub hero (team/install), water-heater rail (install). Montserrat via Google Fonts, weights 400–900 + italics.

## Files
- `Services Mockups.dc.html` — all screens on one canvas (turn 2 = approved; turn 1 = history).
- `support.js`, `image-slot.js` — mockup runtime only; not part of the design.
- `README.md` — this file.
