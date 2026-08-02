# Migration: off Framer to a self-hosted static site

Status as of 2026-08-01. Analysis is done and the decision is made — build it. No port
code written yet; this file records what was measured so none of it is re-derived.

Full write-up, including the launch plan and hosting recommendation:
<https://claude.ai/code/artifact/3a572da6-bc8f-457c-ae26-25f8e6c8629c>

## Why

Framer serves each embed inside a `srcdoc` iframe, and the crawler does not credit
that content to the page. Measured against the live site:

| page | `<h1>` | headings | copy inside iframes |
| --- | --- | --- | --- |
| `/` | 1 | 7 | 75,326 chars |
| `/air-conditioning` | 0 | 0 | 91,648 chars |
| `/locations/dayton` | 0 | 0 | 147,178 chars |
| `/locations/kettering` | 0 | 0 | 111,261 chars |

On `/locations/dayton` there is 41x more content inside iframes than on the page, and
what sits outside is mostly the nav menu. Title, meta description and canonical are
fine; the body is not there. No `ld+json` anywhere.

Page weight, live vs. what the builder already produces:

| | Framer today | self-hosted |
| --- | --- | --- |
| `/locations/dayton` | 52 KB gzipped (322 KB raw) | ~12 KB gzipped (50 KB raw) |
| `/air-conditioning` | 40 KB gzipped (271 KB raw) | ~9 KB gzipped (39 KB raw) |
| external `<script>` | 10 | 0 |
| iframes | 8-9 | 0 |

## Responsiveness: nothing to do

Tested eight page types at 390px. **Zero horizontal overflow on all of them.** The 306
generated pages carry their own breakpoints (eleven `@media` rules in the shared CSS)
and need no work. Framer was never handling their responsiveness — it was hosting a
self-contained document that handles it internally.

The only gap is the header and footer, which exist as three variants each and are
swapped by Framer per breakpoint. They carry zero media queries because they never
needed any.

## What each file needs

| File | Action |
| --- | --- |
| `builder/shell.py` | **New.** Full `<html>` document: head, title, meta description, canonical, OG tags, `LocalBusiness` + `areaServed` schema, header, footer. This is where the SEO fix lands. |
| `framer/footer/*.html` x3 | **Merge to one.** Markup is identical between desktop and tablet; mobile differs by 5 lines (a shortened service-area list). Mobile adds 11 CSS rules, tablet adds 3. Wrap those in media queries and keep one file. |
| `framer/header/DesktopHeader.tsx` | **Port to HTML/CSS.** 808 lines. Drop `addPropertyControls`, inline the Theme import. Mega-menu is the fiddly part. |
| `framer/header/MobileHeader.tsx` | **Port and merge** with desktop — 86% shared. |
| `framer/header/TabletHeader.tsx` | **Delete.** 52 lines that re-export DesktopHeader with one prop flipped. Becomes a media query. |
| `framer/theme.tsx` | **Fold into `template.py`.** Its tokens already exist there as CSS variables. |
| `framer/schedule/ContactFlowDialog.tsx` | **Done — unchanged.** All 2,816 lines import only React, no Framer runtime. `src/schedule/mount.tsx` is the `createRoot()` entry; esbuild bundles both to `assets/js/schedule.js` (59KB gzipped), loaded on demand the first time a Schedule button is used. |
| `framer/schedule/OpenContactDialog.tsx` | **Delete at cutover.** Framer Override glue; the CustomEvent it wraps already works natively. Still referenced by the live Framer site, so it stays until that site is retired. |
| `framer/homepage/*.tsx` x4 | **Port to the builder.** Hero, AboutFaqReviews, XPlan, Brands. Already CSS-in-template-literal, the same shape `template.py` uses. |
| `builder/build.py` | Emit `index.html` so paths map to URLs on a static host. |
| `pages/**` (310) | **No change.** Regenerated with the new shell. |
| `assets/**` (107) | **No change**, but serve same-origin instead of jsDelivr — that retires the commit pins and the 12-hour branch-cache workaround. |

Roughly 26 engineering hours.

## Output layout

Emit the standalone site to a **new `site/` directory** and leave `pages/` as the
Framer embeds. Both stay buildable from the same source during the transition, so
nothing breaks before cutover.

## Where to pick up

1. `builder/shell.py` — the document wrapper. Start here; everything else hangs off it.
2. Merge the three footers (easiest, already HTML — see the diffs above).
3. Port the header. The nav data is at the top of `DesktopHeader.tsx` as
   `HVAC_CORE`, `HVAC_ADDITIONAL`, `PLUMB_CORE`, `PLUMB_ADDITIONAL` — lift verbatim.
4. Homepage sections from the four `framer/homepage/*.tsx` files.
5. Wire `build.py` to emit `site/`, then serve locally and compare against Framer.

## Decisions already made

- Host on **Cloudflare Pages**. Not a VPS — a static site gains nothing from a server
  someone has to patch.
- Serve assets same-origin, drop jsDelivr.
- The client declined the interim fix (setting `<h1>` and schema inside Framer) in
  favour of doing the migration directly.
