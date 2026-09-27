# Extreme Heating, Air &amp; Plumbing — website

Everything for extremeheating.com lives here: the images the live site loads, the
generator that builds its pages, and the booking wizard. One repo, one place to look.

## Layout

```
build.py      run this — builds the whole site into site/
tags/         Google tags: head.html goes in <head>, body.html right after <body>.
              disabled/ is kept for rollback and never built.
src/          everything you edit
  data/         business facts, reviews, the tags loader, content dates
  layout/       header and footer, <head> and schema, shared page components
  pages/        one file per page; registry.py is the list of generated pages
    services/     hvac.py, plumbing.py
    locations/    page.py (the template), cities.py, angles.py
  scheduler/    the booking wizard, bundled into assets/js/schedule.js
assets/       images and built JS served to the live site
workers/      Cloudflare Worker for the bare extremeheating.com domain
reference/    not used by the site: old Framer components, mockups, original photos
site/         generated output, never edit (gitignored)
```

## Rebuilding

```bash
python3 build.py
```

Writes every page to `site/` with its sitemap, robots.txt, _redirects, llms.txt and
_headers. Standard library only. Page embeds are built into `.build/pages/` first
(gitignored). Preview with `python3 -m http.server 8800` from inside `site/`.
Cloudflare Pages runs `python3 builder/build_site.py`, a two-line shim for `build.py`.

The booking wizard has its own build:

```bash
npm install && npm run build:schedule
```

esbuild bundles `src/scheduler/` and React into `assets/js/schedule.js`. The bundle is
committed, so nothing on a server needs Node; rebuild it after editing the wizard.

## Three things that will bite you

**Assets are commit-pinned, and that is deliberate.** jsDelivr caches the
branch-to-commit resolution for 12 hours, so replacing a file in place does *not*
change what the site serves — a `?v=` query string doesn't help and the purge API
doesn't clear it. After pushing new or changed images, set `ASSET_COMMIT` in
`src/layout/components.py` to the new SHA (`git rev-parse HEAD`) and rebuild.

**This repo is public because jsDelivr cannot serve a private one.** That is the
only reason. Keep credentials out of it; local machine config lives in `.claude/`
and is gitignored.

**In-page anchors don't use `scrollIntoView`.** In a Framer embed the iframe is
sized to its content, so it has nothing to scroll and the jump must move the parent
page. Cross-frame `scrollIntoView` ignores the iframe's offset in the parent and
lands short by exactly that much, and `behavior: "smooth"` silently does nothing
across the boundary. `components.py` computes the absolute position and drives the
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
