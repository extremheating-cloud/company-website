# Extreme Heating, Air &amp; Plumbing — website source

Source for extremeheating.com. The site is built in **Framer**; the pages in this
repo are HTML embeds that get pasted into Framer by hand, plus the Framer code
components that live alongside them.

## Rebuilding

```bash
cd Redesigns/service_page_builder
python3 build.py
```

That regenerates all 39 pages into `HVAC Service Pages/`, `Plumbing Service Pages/`
and `Other pages/`. No dependencies beyond the standard library.

Generated HTML is committed alongside its source on purpose: it is pasted into
Framer by hand, so the built output is what actually ships and its diffs are what
need reviewing.

## Layout

| Path | What it is |
| --- | --- |
| `Redesigns/service_page_builder/` | the generator |
| `HVAC Service Pages/`, `Plumbing Service Pages/`, `Other pages/` | generated embeds — do not hand-edit |
| `Pages/`, `Header/`, `Footer/`, `ScheduleEngine/`, `Theme.tsx` | Framer code components, hand-maintained |
| `assets/` | local image assets |

Inside the generator:

- `template.py` — shared CSS and JS, the photo table, and the page renderers
- `build.py` — the page registry; every page is `(path, builder, data, root_class)`
- `company_pages.py` — /about, /contact, /financing-options, /specials
- `referral.py`, `terms.py` — /referral and /terms
- `rollout.py` — the service-page data

## Two things that will bite you

**Images are commit-pinned, and that is deliberate.** jsDelivr caches the
branch-to-commit resolution for 12 hours, so replacing a file in place does *not*
change what the site serves — a `?v=` query string doesn't help and the purge API
doesn't clear it. Photo URLs are built by `T.cdn_asset(path, commit)` against
[extreme-assets](https://github.com/extremheating-cloud/extreme-assets). When you
replace a photo, update the commit in `template.py`, don't just re-upload. Pins are
per file, so only the files that actually changed move.

**In-page anchors don't use `scrollIntoView`.** In a Framer embed the iframe is
sized to its content, so it has nothing to scroll and the jump has to move the
parent page. Cross-frame `scrollIntoView` ignores the iframe's own offset in the
parent and lands short by exactly that much, and `behavior: "smooth"` silently does
nothing across the boundary. `template.py` computes the absolute position and drives
the parent's scroll directly. Cross-page links like `/terms#financing` also put the
hash on the *parent* URL, which this document never sees — the script reads it from
the parent on load.

## Brand

Design system, voice, and the X-Plan / Extreme Rewards program facts live in the
`extreme-brand` skill, not here. Two rules that come up constantly: never set
`#61BC47` green as text on white (use `#3F852B`), and never state the X-Plan
accrual without both conditions — consecutive years, capped at $2,500 or 10 years.
