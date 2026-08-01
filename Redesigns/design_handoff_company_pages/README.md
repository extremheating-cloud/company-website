# Handoff: Extreme company pages (About · Contact · Financing · Specials)

## Overview
Four company/marketing pages for extremeheating.com in the approved redesign system (homepage + services handoffs). **Brand name is now "Extreme Heating, Air, Plumbing"** — use it in logo alt text, footer © line, meta titles, and anywhere the old "Extreme Heating & Air Conditioning" appears (the logo PNG itself still shows the old wordmark; swap the asset site-wide when the new logo file arrives).

| Screen | Page | Route |
|---|---|---|
| 4a | About | `/about` |
| 4b | Contact | `/contact` |
| 4c | Financing options | `/financing-options` |
| 4d | Specials | `/specials` |

## About the Design File
`Company Pages Mockups.dc.html` is a **design reference built in HTML** — intended look and behavior, NOT production code. Recreate in the existing codebase (`Header/`, `Footer/`, `Theme.tsx`, `ScheduleEngine/` conventions per the services handoff). Open in a browser with `support.js`, `image-slot.js`, `assets/` beside it; screens sit on a pannable canvas with monospace badges 4a–4d. Desktop 1280 only — **mobile stacks per screen 2b of the services handoff** (stacked hero CTAs, list-row conversions, pinned bottom Schedule/Call bar).

All four pages share the finalized frame: solid `#5E2C7E` header → purple-gradient hero (`150deg, #5E2C7E → #542770 45% → #3A1A4E`, x-mark watermark bled off right inside `overflow:hidden`) with breadcrumb, italic-900 46px H1 with one green phrase, intro, 3 glass chips → white body (`padding:56px 40px`) → ink `#0F172A` page-specific CTA band → 4px green→purple gradient hairline → dark footer CTA band → full footer (homepage handoff 3a/3b). Tokens: `design_handoff_homepage_redesign/README.md` is the source of truth.

## Page anatomy

### 4a About (`/about`) — full-width tier (no rail)
Hero grid `1fr 400px` with team-photo slot right (no booking card). Body:
1. **Our story** — split `1.1fr .9fr`: two paragraphs + photo slot (founders/first van).
2. **What we stand for** — 4 bordered cards (r16, X glyph 26px): honest pricing / home respected / fast / referrals.
3. **Stats panel** — purple gradient r24: `20+` years · `★ 4.9` · `90%` same-day · `24/7` (italic 900 30px + muted caption).
4. **Meet the team** — 4 headshot slots (h230 r14) + name/role captions. *Placeholder names/roles — fill with real staff.*
5. **Where we work** — Dayton + Cincinnati bordered cards → location pages.
CTA band = hiring ("Love the trade? So do we." → careers/`/contact`).

### 4b Contact (`/contact`) — rail tier
Hero card (overlap `-84px`) = **contact card**: eyebrow CONTACT US → phone italic-900 27px → hours line → green **Schedule Service** → purple **Call** → hairline trust row. **No contact form — scheduling runs through ScheduleEngine.** Left column:
1. **Book a visit** — 2 cards: Schedule online (green btn → ScheduleEngine) / Call the office (phone link).
2. **Visit us** — 2 location cards: map/storefront slot (h160) + address + "Get directions →" (Google Maps link). *Addresses are placeholders.*
3. **Hours** — bordered table rows; last row green `#EEF7EC` "Emergencies 24/7". *Confirm real office hours.*
Rail: office photo slot + "Need help right now? → tel:" (`#F4F1F8`) + X-Plan promo (`#EEF7EC` → `/maintenance`). CTA band = 24/7 emergency line.

### 4c Financing (`/financing-options`) — rail tier
Hero card = **apply card**: eyebrow FINANCING → "Apply in minutes." → green **Apply Online** (lender application link) → purple Call → "Secure application | No obligation". Left column:
1. **Why finance** — 4 check-circle cards (monthly payment / don't downgrade / keep savings / stacks with specials & rebates).
2. **What qualifies** — 6-item check-circle list (2-col).
3. **How it works** — steps 01–03 (quote → apply → approved & installed).
4. **Good to know panel** — purple gradient: Minutes / $0 down / No penalty stats + **OUR LENDERS chip row: GoodLeap · Synchrony · Wright-Patt Credit Union** + fine print ("subject to credit approval" — swap in current program rates/terms before ship).
5. **FAQ** — credit-score soft pull (open), imperfect credit, early payoff, combine with specials.
Rail: install photo slot + Specials promo (`#F4F1F8` → `/specials`) + X-Plan promo (`#EEF7EC` → `/maintenance`). CTA band = "repairs can be financed too".

**Lenders (client-confirmed): GoodLeap, Synchrony, Wright-Patt Credit Union.** Say "our lenders" (plural) — never "our lending partner". Get each lender's live application URL + current terms before build; don't invent APRs.

### 4d Specials (`/specials`) — full-width tier
Hero full-width (no card). Body:
1. **Current offers** — 3-col grid of coupon cards: dashed `1.5px #C4B5D4` border r16; category pill (`#F4F1F8`/`#542770`); italic-900 34px value; title; desc; footer row "Limited time" + green Claim btn (→ ScheduleEngine with offer noted). **All six offers shown are PLACEHOLDERS** ($79 tune-up, $50 off repair, $500 off system, $99 drain, free second opinion, X-Plan card) — swap in live promotions; build cards data-driven so marketing can rotate them.
2. **How to redeem** — steps 01–03 + fine-print paragraph (one offer per visit, mention at booking, terms per promotion).
3. Right column: **email signup panel** (purple gradient; wire to ESP or hide at launch) + Financing promo card (`#F4F1F8` → `/financing-options`).
CTA band = "Don't see a special for what you need?".

## URL & backlink map
Phone everywhere `tel:18445847399`, display "(844) 584-7399". Schedule CTAs → ScheduleEngine. Breadcrumbs: "Home" → `/`; current page green, unlinked. Header nav active state: About green on 4a, Specials green on 4d.
- 4a: location cards → `/locations` (or per-city pages); hiring band → careers target (confirm).
- 4b: Get directions → Google Maps place links; X-Plan promo → `/maintenance`.
- 4c: Apply Online → lender application (confirm which/aggregator); Specials promo → `/specials`; X-Plan promo → `/maintenance`.
- 4d: X-Plan coupon → `/maintenance`; Financing card → `/financing-options`; Claim Offer → ScheduleEngine.
- Inbound (already in other handoffs): every financing promo → `/financing-options`; specials promos → `/specials`; header Specials/About → these pages.

## Copy
Mockup text is the copy deck — paste verbatim, marketing reviews in staging. **Placeholders to replace:** street addresses + ZIPs (4b), office hours (4b), team names/roles (4a), founding-story specifics (4a — "20+ years" is approved; add real year only if client confirms), all specials offers (4d), lender terms/rates (4c). X-Plan facts if referenced: $249/yr, $20.75/mo per system; members pay discounted service calls ($77 vs $97 business hours, $177 vs $197 emergencies) — never "free".

## Implementation plan (ordered)
1. Reuse shared components from the services handoff (hero, rail, promo cards, steps, FAQ, emergency band, header/footer). New components: `StatsPanel`, `TeamGrid`, `LocationCard`, `HoursTable`, `CouponCard`, `LenderChips`, `EmailSignup`.
2. Build `/contact` first (smallest, unblocks nav) → `/financing-options` → `/specials` (data-driven offers) → `/about`.
3. Site-wide rename to "Extreme Heating, Air, Plumbing" (footer ©, alt text, titles/meta); logo asset swap when available.
4. QA: hrefs vs URL map, tel: constant, placeholders flagged with TODOs, mobile stacking + pinned bar per 2b, 44px targets.

## Files & assets
- `Company Pages Mockups.dc.html` — screens 4a–4d on one canvas.
- `support.js`, `image-slot.js` — mockup runtime only.
- `assets/logo-white.png` (old wordmark — replace), `assets/x-mark.png` (watermark; keep the "™" fragment on its right edge clipped off-screen). Montserrat 400–900 + italics via Google Fonts.
- Photos needed: team group (4a hero), founders/van (4a story), 4 headshots (4a), 2 storefront/map images (4b), office/dispatcher (4b rail), new install (4c rail).
