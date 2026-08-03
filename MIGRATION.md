# Migration: off Framer to a self-hosted static site

**Status 2026-08-03: the port is done and the site is built. What remains is the DNS
cutover, which is the runbook at the bottom of this file.**

The analysis below is from 2026-08-01 and is kept as written, because it records what
was measured and why the decision was made. Do not re-derive it. Where a line has
since been actioned it is marked DONE rather than edited, so the original reasoning
stays legible.

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
| `assets/**` (107) | **DONE 2026-08-03.** Same-origin, jsDelivr retired. The commit pin became `ASSET_VERSION` as a `?v=` query, doing the same cache-busting job; `_headers` now caches assets immutable for a year because of it. |

Roughly 26 engineering hours. **All of the above is complete.**

## Output layout

Emit the standalone site to a **new `site/` directory** and leave `pages/` as the
Framer embeds. Both stay buildable from the same source during the transition, so
nothing breaks before cutover.

## Where to pick up — all done

1. ~~`builder/shell.py` — the document wrapper.~~ Done.
2. ~~Merge the three footers.~~ Done.
3. ~~Port the header.~~ Done, including the mega-menu.
4. ~~Homepage sections from the four `framer/homepage/*.tsx` files.~~ Done.
5. ~~Wire `build.py` to emit `site/`.~~ Done. 320 pages, 136 indexable, 169 redirects.

## Decisions already made

- Host on **Cloudflare Pages**. Not a VPS — a static site gains nothing from a server
  someone has to patch. **Still the plan.**
- Serve assets same-origin, drop jsDelivr. **Done 2026-08-03.**
- The client declined the interim fix (setting `<h1>` and schema inside Framer) in
  favour of doing the migration directly.

---

# Cutover runbook

Written 2026-08-03. Everything under "Already handled" is done and verified. Everything
after it needs a dashboard or a DNS record and cannot be done from this repo.

## Already handled in the build

Listed so you can tell what is covered, not because anything is needed.

- **Builds clean from a fresh clone.** Verified by cloning to an empty directory and
  building: output byte-identical to a local build, 320 pages. No untracked file is
  required.
- **No dependencies.** Every builder module is stdlib-only — verified by walking the
  AST of every import. Nothing to install, no lockfile.
- **`_redirects`** — all 169 rules, in the format Pages reads.
- **`_headers`** — hashed CSS/JS and versioned images immutable for a year, HTML
  must-revalidate, plus `X-Content-Type-Options` and `Referrer-Policy`.
- **Preview deployments cannot be indexed.** Pages builds every branch to a public
  `*.pages.dev` URL, and a second crawlable copy of a 320-page site competes with the
  real one. The build reads `CF_PAGES_BRANCH`: on any branch but `main` it writes a
  blanket-disallow `robots.txt` and adds `X-Robots-Tag: noindex, nofollow`. Inert
  locally and on any other host. Tested both ways.
- **All images same-origin**, so the repo can be private.
- **`site/` is gitignored** and built by Pages rather than committed.

## Build settings

Workers & Pages → Create → Pages → Connect to Git → this repo.

Set each field separately. They are four fields, not one value — pasting the whole
block into "Build command" makes the shell try to run a program called `Build`, which
fails in about a second. That happened on the first attempt.

    Framework preset:        None
    Build command:           python3 builder/build_site.py
    Build output directory:  site
    Root directory:          (leave blank)
    Production branch:       main

**Build output directory is the one that matters most.** Left blank, Cloudflare
publishes the whole repository: the root serves README.md, and the actual site ends up
at /site/. That also happened on the first attempt.

No environment variables are required. The builder is stdlib-only and uses no syntax
newer than Python 3.6 — verified, not assumed — so whatever Python the build image
ships with will run it. Setting PYTHON_VERSION is optional and only pins the build
against a future image change.

## Before DNS

1. **Deploy and open the `*.pages.dev` URL.** Walk the homepage, one service page, one
   city page, `/contact`, `/privacy`.
2. **Confirm the interactive parts.** Schedule button opens the wizard. Podium and
   Broccoli widgets appear. GTM, GA4, Ads and the Meta Pixel fire.
3. **Check the generated files** on the preview: `/robots.txt`, `/sitemap.xml`,
   `/llms.txt`, and follow one of the 169 redirects.
4. **Confirm the preview is not indexable** — its `/robots.txt` should say
   `Disallow: /`. If it does not, Pages is treating that branch as production.

## DNS cutover

5. **Lower TTL first** to 5 minutes, a few hours ahead, so rollback is fast.
6. **Add both custom domains** to the Pages project: `www.extremeheating.com` and
   `extremeheating.com`.
7. **Create the apex → www Redirect Rule.** The one thing that cannot live in this
   repo: Pages `_redirects` cannot match on hostname.

       If    hostname equals    extremeheating.com
       Then  Static redirect to https://www.extremeheating.com/${uri.path}
             Status 301, Preserve query string ON

   Every canonical, the sitemap and llms.txt point at `www`. Without this the apex
   serves a duplicate of the whole site.

## After

8. **Spot-check ten redirects live**, especially
   `/locations/<city>/furnace-heating → /heating`. Those rank today and 404 on Framer.
9. **Search Console.** Submit `https://www.extremeheating.com/sitemap.xml`. Skip
   "Change of address" — the domain is not changing.
10. **Re-run Lighthouse on the live domain.** Every performance figure we hold is from
    localhost, and the site now carries GTM, GA4, Google Ads, Meta Pixel, Broccoli,
    Podium and ServiceTitan. A competitor scores 22/100 on performance because of the
    last two vendors specifically. If it has dropped hard, the levers are deferring
    Podium until interaction and moving tags into GTM rather than loading them
    alongside it.
11. **Confirm caching.** `curl -I` a CSS file and an image; both should return
    `cache-control: public, max-age=31536000, immutable`.
12. **Check Google Ads number swapping** on the live domain. It matches the exact
    string `(844) 584-7399`; the four local office numbers are deliberately not
    swapped.

## Rollback

Keep Framer live but unpointed for a week. If something is wrong, revert the DNS
records; at a 5-minute TTL you are back within ten minutes. Do not cancel Framer until
a full week of Search Console shows no coverage errors.

## Known and accepted at launch

- **Cloudflare may serve its own robots.txt.** A managed Content Signals robots.txt
  was observed overriding the one the build generates, which would drop our AI-crawler
  policy and the sitemap reference. Check `/robots.txt` after deploying; ours begins
  `# https://www.extremeheating.com/robots.txt`. If Cloudflare's is winning, turn the
  managed file off under AI Crawl Control.
- **Per-deployment preview URLs have no valid certificate.** `*.pages.dev` covers one
  subdomain level, so `project.pages.dev` works and `hash.project.pages.dev` returns
  ERR_SSL_VERSION_OR_CIPHER_MISMATCH. Test on the plain project URL. Not a fault.
- **34 third-party stock images** on the plumbing pages are still hotlinked to iStock
  and Adobe. Licences are being acquired. They are the only images not on our origin
  and they break if those URLs change.
- **No `geo` coordinates** in the LocalBusiness schema, pending the GBP map pins.
- **20 dead legacy URLs want `410 Gone`**, which `_redirects` cannot express. They are
  deliberately absent rather than redirected to the homepage, because a blanket
  redirect reads as a soft 404.
