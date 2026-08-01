# Extreme Heating, Air &amp; Plumbing — website

Everything for extremeheating.com lives here: the images the live site loads, the
generator that builds its pages, and the Framer components. One repo, one place to
look.

The site itself is built in **Framer**. The HTML in `pages/` is embeds that get
pasted into Framer by hand; `framer/` holds the code components that live alongside
them.

## Layout

```
assets/     images served to the live site, by subject
  brand/        Extreme logos, X mark, van
  brands/       manufacturer logos (Trane, Ruud, Daikin)
  cities/       city and county photos
  equipment/    real installed equipment from jobs
  locations/    offices, vans, community events
  print/        brochure and member guide artwork
  service/      service and topic imagery
  team/         technician portraits

pages/      generated HTML embeds — do not hand-edit
  company/      about, contact, financing-options, specials, referral, terms
  hvac/
  plumbing/

framer/     hand-maintained Framer code components
  header/  footer/  homepage/  schedule/  theme.tsx

builder/    the Python generator
design/     mockups and design handoff docs
```

## Rebuilding

```bash
cd builder && python3 build.py
```

Regenerates all 39 pages into `pages/`. Standard library only, no dependencies.

Generated HTML is committed alongside its source on purpose: it is pasted into
Framer by hand, so the built output is what actually ships and its diffs are what
need reviewing.

Inside `builder/`:

- `template.py` — shared CSS and JS, the asset URLs, the page renderers
- `build.py` — the page registry; each page is `(path, builder, data, root_class)`
- `company_pages.py`, `referral.py`, `terms.py` — the non-service pages
- `rollout.py` — service-page data

## Three things that will bite you

**Assets are commit-pinned, and that is deliberate.** jsDelivr caches the
branch-to-commit resolution for 12 hours, so replacing a file in place does *not*
change what the site serves — a `?v=` query string doesn't help and the purge API
doesn't clear it. After pushing new or changed images, set `ASSET_COMMIT` in
`builder/template.py` to the new SHA (`git rev-parse HEAD`) and rebuild.

**This repo is public because jsDelivr cannot serve a private one.** That is the
only reason. Keep credentials out of it; local machine config lives in `.claude/`
and is gitignored.

**In-page anchors don't use `scrollIntoView`.** In a Framer embed the iframe is
sized to its content, so it has nothing to scroll and the jump must move the parent
page. Cross-frame `scrollIntoView` ignores the iframe's offset in the parent and
lands short by exactly that much, and `behavior: "smooth"` silently does nothing
across the boundary. `template.py` computes the absolute position and drives the
parent's scroll directly. Cross-page links like `/terms#financing` also put the hash
on the *parent* URL, which the embed never sees — the script reads it from the
parent on load.

## Asset naming

Lowercase, hyphenated, no spaces. A space has to be percent-encoded in every URL
that references it and is a recurring source of broken images. Never overwrite an
existing filename with different content unless you also update the pin.

## Brand

The design system, voice, and the X-Plan / Extreme Rewards program facts live in the
`extreme-brand` skill, not here. Two rules that come up constantly: never set
`#61BC47` green as text on white (use `#3F852B`), and never state the X-Plan accrual
without both conditions — consecutive years, capped at $2,500 or 10 years.
