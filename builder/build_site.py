"""Build the self-hosted site into site/.

Run after build.py:   python3 build.py && python3 build_site.py
Or just:              python3 build_site.py     (it runs build.py first)

Takes every Framer embed in pages/, wraps it in a full HTML document with the header,
footer, meta and schema, and writes it to site/<route>/index.html so paths map to URLs
on any static host. pages/ is left alone — the embeds stay valid until cutover.

Alongside the pages it writes the four files that decide how the site is crawled:

    sitemap.xml   indexable routes only, absolute URLs from D.canonical()
    robots.txt    everything allowed, AI crawlers named explicitly
    _redirects    169 rules, the whole cutover map
    llms.txt      the plain-text fact sheet

Those four are the reason this module has guardrails that abort the build. Every
failure they catch is silent — a sitemap that quietly loses 168 URLs, a redirect
pointing at a 404, a noindex tag on the homepage — and none of them surface until
traffic has already gone. A build that stops is cheap; a month of that is not.
"""
import collections, hashlib, os, re, shutil, subprocess, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PAGES = os.path.join(ROOT, "pages")
SITE = os.path.join(ROOT, "site")

import shell, homepage, locations as L, site_data as D  # noqa: E402

# ---------------------------------------------------------------- routes
# route_for lives in shell.py so meta_for and this module cannot compute a route two
# ways. The local copy below is the fallback for a tree where that move has not landed
# yet; it is the same logic, not a second opinion.
def _route_for(rel):
    url = "/" + rel.replace(os.sep, "/").replace("\\", "/")
    # /locations/<city>/overview.html serves at /locations/<city>, but the plumbing
    # families genuinely live at /plumbing/<family>/overview — that is the live URL and
    # what every internal link points to. Only collapse the locations case.
    if url.startswith("/locations/") and url.endswith("/overview.html"):
        url = url[: -len("/overview.html")]
    elif url.endswith(".html"):
        url = url[: -len(".html")]
    # hvac/ and company/ are build-time grouping, not URL structure — the live site
    # serves those pages at the root. Prefix-anchored, not a global replace: a city
    # called "company" would otherwise lose a path segment from the middle of its URL.
    for prefix in ("/hvac/", "/company/"):
        if url.startswith(prefix):
            url = "/" + url[len(prefix):]
            break
    return "/" if url in ("", "/index") else url

route_for = getattr(shell, "route_for", None) or _route_for

# shell.noindex() is the single predicate: it writes the meta tag AND filters the
# sitemap, so the two cannot disagree. If it is not present yet, everything is treated
# as indexable — the same way document() treats a missing key. Failing open to
# indexable is recoverable; a sitewide noindex is not.
_noindex = getattr(shell, "noindex", None)
if _noindex is None:
    def _noindex(url):
        return False

def out_path(url):
    if url == "/":
        return os.path.join(SITE, "index.html")
    return os.path.join(SITE, url.strip("/"), "index.html")

# ---------------------------------------------------------------- redirects
# The cutover map. Every source is a URL that resolved on some previous incarnation of
# the site — Framer, the WordPress site before it, or the .asp site before that —
# and does not exist in this build. Sources verified against the live site and the
# Wayback CDX index 2026-08-02.
#
# 301, not 302, everywhere. Framer's own redirects are 308, which is equally permanent
# and equally fine, but mixing the two for no reason invites someone to "standardise"
# on 302 later and silently stop passing equity.
#
# Path-only. Cloudflare Pages cannot match on hostname in _redirects, so apex -> www is
# a zone Redirect Rule, not a line in this file.
#
# 20 further dead URLs are deliberately NOT here — /event, /image, /employment, /faqs,
# /insulation, the Bryant FAQ pages, the Flash movies and the rest. They have no
# honest target, and a blanket 301 to the homepage is read as a soft 404: it passes
# nothing and hides the problem from Search Console. They want 410 Gone, which
# _redirects cannot express, so they are a host-level task. See redirects.md.
#
# The four /blog rules are a STOPGAP. Redirecting an article to a service page is a
# topical mismatch that Google often treats as a soft 404, so it buys the user, not the
# ranking. If the three posts are ported to /blog/<slug>, delete those rules.
REDIRECTS = [
    # Live today on Framer, no route in the rebuild. All 9 return 200 right now.
    ("/schedule", "/contact"),
    ("/reviews", "/about"),
    ("/plumbing-calc", "/plumbing/water-heater/overview"),
    ("/archived/29-tune-up", "/specials"),
    ("/archived/49-tune-up", "/specials"),
    ("/archived/tax-credit", "/financing-options"),
    ("/blog/do-my-ducts-need-cleaning", "/duct-cleaning"),
    ("/blog/heat-pump-vs-furnace-ohio", "/heat-pump"),
    ("/blog/spring-ac-tune-up-checklist", "/maintenance"),

    # Location service rename. Two service slugs were renamed inside Framer
    # (furnace-heating -> heating, air-conditioning -> cooling) and no redirects
    # shipped, so these 404 in production TODAY while still ranking. Covers all 38
    # location slugs, not only the 14 with archive records: a redirect for a URL
    # that never existed costs nothing, a missing one costs a ranking page.
    # Cloudflare placeholders would collapse this to two rules; written out in full
    # so the map also works on a host without placeholder support.
    ("/locations/beavercreek/furnace-heating", "/locations/beavercreek/heating"),
    ("/locations/beavercreek/air-conditioning", "/locations/beavercreek/cooling"),
    ("/locations/bellbrook/furnace-heating", "/locations/bellbrook/heating"),
    ("/locations/bellbrook/air-conditioning", "/locations/bellbrook/cooling"),
    ("/locations/blue-ash/furnace-heating", "/locations/blue-ash/heating"),
    ("/locations/blue-ash/air-conditioning", "/locations/blue-ash/cooling"),
    ("/locations/butler-county/furnace-heating", "/locations/butler-county/heating"),
    ("/locations/butler-county/air-conditioning", "/locations/butler-county/cooling"),
    ("/locations/centerville/furnace-heating", "/locations/centerville/heating"),
    ("/locations/centerville/air-conditioning", "/locations/centerville/cooling"),
    ("/locations/cincinnati/furnace-heating", "/locations/cincinnati/heating"),
    ("/locations/cincinnati/air-conditioning", "/locations/cincinnati/cooling"),
    ("/locations/clark-county/furnace-heating", "/locations/clark-county/heating"),
    ("/locations/clark-county/air-conditioning", "/locations/clark-county/cooling"),
    ("/locations/darke-county/furnace-heating", "/locations/darke-county/heating"),
    ("/locations/darke-county/air-conditioning", "/locations/darke-county/cooling"),
    ("/locations/dayton/furnace-heating", "/locations/dayton/heating"),
    ("/locations/dayton/air-conditioning", "/locations/dayton/cooling"),
    ("/locations/englewood/furnace-heating", "/locations/englewood/heating"),
    ("/locations/englewood/air-conditioning", "/locations/englewood/cooling"),
    ("/locations/fairborn/furnace-heating", "/locations/fairborn/heating"),
    ("/locations/fairborn/air-conditioning", "/locations/fairborn/cooling"),
    ("/locations/fairfield/furnace-heating", "/locations/fairfield/heating"),
    ("/locations/fairfield/air-conditioning", "/locations/fairfield/cooling"),
    ("/locations/franklin/furnace-heating", "/locations/franklin/heating"),
    ("/locations/franklin/air-conditioning", "/locations/franklin/cooling"),
    ("/locations/greene-county/furnace-heating", "/locations/greene-county/heating"),
    ("/locations/greene-county/air-conditioning", "/locations/greene-county/cooling"),
    ("/locations/hamilton-county/furnace-heating", "/locations/hamilton-county/heating"),
    ("/locations/hamilton-county/air-conditioning", "/locations/hamilton-county/cooling"),
    ("/locations/huber/furnace-heating", "/locations/huber/heating"),
    ("/locations/huber/air-conditioning", "/locations/huber/cooling"),
    ("/locations/kettering/furnace-heating", "/locations/kettering/heating"),
    ("/locations/kettering/air-conditioning", "/locations/kettering/cooling"),
    ("/locations/lebanon/furnace-heating", "/locations/lebanon/heating"),
    ("/locations/lebanon/air-conditioning", "/locations/lebanon/cooling"),
    ("/locations/mason/furnace-heating", "/locations/mason/heating"),
    ("/locations/mason/air-conditioning", "/locations/mason/cooling"),
    ("/locations/miami-county/furnace-heating", "/locations/miami-county/heating"),
    ("/locations/miami-county/air-conditioning", "/locations/miami-county/cooling"),
    ("/locations/miamisburg/furnace-heating", "/locations/miamisburg/heating"),
    ("/locations/miamisburg/air-conditioning", "/locations/miamisburg/cooling"),
    ("/locations/middletown/furnace-heating", "/locations/middletown/heating"),
    ("/locations/middletown/air-conditioning", "/locations/middletown/cooling"),
    ("/locations/montgomery-county/furnace-heating", "/locations/montgomery-county/heating"),
    ("/locations/montgomery-county/air-conditioning", "/locations/montgomery-county/cooling"),
    ("/locations/moraine/furnace-heating", "/locations/moraine/heating"),
    ("/locations/moraine/air-conditioning", "/locations/moraine/cooling"),
    ("/locations/northgate/furnace-heating", "/locations/northgate/heating"),
    ("/locations/northgate/air-conditioning", "/locations/northgate/cooling"),
    ("/locations/oakwood/furnace-heating", "/locations/oakwood/heating"),
    ("/locations/oakwood/air-conditioning", "/locations/oakwood/cooling"),
    ("/locations/preble-county/furnace-heating", "/locations/preble-county/heating"),
    ("/locations/preble-county/air-conditioning", "/locations/preble-county/cooling"),
    ("/locations/riverside/furnace-heating", "/locations/riverside/heating"),
    ("/locations/riverside/air-conditioning", "/locations/riverside/cooling"),
    ("/locations/sharonville/furnace-heating", "/locations/sharonville/heating"),
    ("/locations/sharonville/air-conditioning", "/locations/sharonville/cooling"),
    ("/locations/springboro/furnace-heating", "/locations/springboro/heating"),
    ("/locations/springboro/air-conditioning", "/locations/springboro/cooling"),
    ("/locations/springfield/furnace-heating", "/locations/springfield/heating"),
    ("/locations/springfield/air-conditioning", "/locations/springfield/cooling"),
    ("/locations/tipp/furnace-heating", "/locations/tipp/heating"),
    ("/locations/tipp/air-conditioning", "/locations/tipp/cooling"),
    ("/locations/troy/furnace-heating", "/locations/troy/heating"),
    ("/locations/troy/air-conditioning", "/locations/troy/cooling"),
    ("/locations/vandalia/furnace-heating", "/locations/vandalia/heating"),
    ("/locations/vandalia/air-conditioning", "/locations/vandalia/cooling"),
    ("/locations/warren-county/furnace-heating", "/locations/warren-county/heating"),
    ("/locations/warren-county/air-conditioning", "/locations/warren-county/cooling"),
    ("/locations/west-carrollton/furnace-heating", "/locations/west-carrollton/heating"),
    ("/locations/west-carrollton/air-conditioning", "/locations/west-carrollton/cooling"),
    ("/locations/west-chester/furnace-heating", "/locations/west-chester/heating"),
    ("/locations/west-chester/air-conditioning", "/locations/west-chester/cooling"),
    ("/locations/xenia/furnace-heating", "/locations/xenia/heating"),
    ("/locations/xenia/air-conditioning", "/locations/xenia/cooling"),
    ("/locations/carrollton", "/locations/west-carrollton"),

    # Framer-era paths that already 404. /cooling currently 308s to / on the live
    # site, which is a soft-404 — repointed here at /air-conditioning.
    ("/cooling", "/air-conditioning"),
    ("/heating", "/furnace-heating"),
    ("/heat-pumps", "/heat-pump"),
    ("/company", "/about"),
    ("/service-areas", "/locations"),
    ("/services/comfort-club", "/maintenance"),
    ("/springboro", "/locations/springboro"),
    ("/beavercreek", "/locations/beavercreek"),
    # Direct, not via /archived/, so these do not become a two-hop chain.
    ("/29-tune-up", "/specials"),
    ("/49-tune-up", "/specials"),
    ("/tax-credit", "/financing-options"),
    ("/federal-tax-credit", "/financing-options"),
    ("/furnace-heating-repair", "/furnace-repair"),
    ("/heating-tune-up", "/maintenance"),
    ("/perfect-ac-tune-up", "/maintenance"),
    ("/full-hvac-system-replacement-special", "/specials"),
    ("/trane-promotion", "/specials"),
    ("/Trane_WIN-WIN", "/specials"),      # case-sensitive; the live host does not fold case
    ("/book-online/beavercreek", "/contact"),
    ("/book-online/mason", "/contact"),
    ("/book-online/troy", "/contact"),

    # Pre-Framer (WordPress) city landing pages.
    ("/beavercreek-ohio-heating-air-conditioning-repair", "/locations/beavercreek"),
    ("/bellbrook-ohio-heating-air-conditioning-repair", "/locations/bellbrook"),
    ("/centerville-ohio-heating-air-conditioning-repair", "/locations/centerville"),
    ("/dayton-ohio-heating-air-conditioning-repair", "/locations/dayton"),
    ("/englewood-ohio-heating-air-conditioning-repair", "/locations/englewood"),
    ("/franklin-ohio-heating-air-conditioning-repair", "/locations/franklin"),
    ("/huber-heights-ohio-heating-air-conditioning-repair", "/locations/huber"),
    ("/kettering-ohio-heating-air-conditioning-repair", "/locations/kettering"),
    ("/miamisburg-ohio-heating-air-conditioning-repair", "/locations/miamisburg"),
    ("/moraine-ohio-heating-air-conditioning-repair", "/locations/moraine"),
    ("/oakwood-ohio-heating-air-conditioning-repair", "/locations/oakwood"),
    ("/riverside-ohio-heating-air-conditioning-repair", "/locations/riverside"),
    ("/springboro-ohio-heating-air-conditioning-repair", "/locations/springboro"),
    ("/tipp-city-ohio-heating-air-conditioning-repair", "/locations/tipp"),
    ("/vandalia-ohio-heating-air-conditioning-repair", "/locations/vandalia"),
    ("/west-carrollton-ohio-heating-air-conditioning-repair", "/locations/west-carrollton"),
    ("/xenia-ohio-heating-air-conditioning-repair", "/locations/xenia"),

    # Pre-Framer product and company pages, including the .asp-era routes.
    ("/products", "/services"),
    ("/products/air-conditioning", "/air-conditioning"),
    ("/products/heating", "/furnace-heating"),
    ("/products/heat-pumps", "/heat-pump"),
    ("/products/indoor-air-quality", "/indoor-air-quality"),
    ("/products/controls", "/thermostat"),
    ("/controls", "/thermostat"),
    ("/heating-air-conditioning-products", "/services"),
    ("/heating-air-conditioning-products/air-conditioners", "/air-conditioning"),
    ("/heating-air-conditioning-products/furnaces", "/furnace-heating"),
    ("/heating-air-conditioning-products/heat-pumps", "/heat-pump"),
    ("/heating-air-conditioning-products/indoor-air-quality", "/indoor-air-quality"),
    ("/heating-air-conditioning-products/thermostats", "/thermostat"),
    ("/heating-air-conditioning-products/ductless-mini-splits", "/air-conditioning"),
    ("/about-us", "/about"),
    ("/meet-the-staff", "/about"),
    ("/testimonials", "/about"),
    ("/video-gallery", "/about"),
    ("/trucks", "/about"),
    ("/toys-for-tots", "/about"),
    ("/trane-soar-award", "/about"),
    ("/guarantees", "/about"),
    ("/contact-us", "/contact"),
    ("/contactus", "/contact"),
    ("/contact-2", "/contact"),
    ("/contactIndex.asp", "/contact"),
    ("/supportIndex.asp", "/contact"),
    ("/financing", "/financing-options"),
    ("/applyforfinancing", "/financing-options"),
    ("/coupons", "/specials"),
    ("/coupons/72-coupon2", "/specials"),
    ("/home", "/"),
    ("/index.asp", "/"),

    # Pre-Framer blog posts, retargeted at the closest service page.
    ("/when-to-replace", "/services"),
    ("/5-tips-to-lower-your-heating-bills", "/furnace-heating"),
    ("/5-ways-to-stay-cool-this-summer-in-dayton-ohio", "/locations/dayton/cooling"),
    ("/air-conditioning-installation-know-purchasing", "/ac-installation"),
    ("/air-conditioning-replacement-installation", "/ac-installation"),
    ("/air-conditioning-repair-maintenance", "/ac-repair"),
    ("/top-seven-reasons-choose-extremes-one-hour-installation-new-air-conditioner",
     "/ac-installation"),
    ("/blog/enhancing-indoor-air-quality-5-effective-strategies", "/indoor-air-quality"),
    ("/blog/how-professional-ac-installation-can-improve-energy-efficiency", "/ac-installation"),
    ("/blog/hvac-cold-weather-tips", "/furnace-heating"),
    ("/blog/top-signs-air-conditioner-needs-replaced", "/ac-installation"),

    # Pre-existing. /refer 404s on the live site today, so this one is pre-emptive.
    ("/refer", "/referral"),
]

def write_redirects(routes):
    """_redirects, for hosts that read one (Cloudflare Pages, Netlify).

    The three assertions are the whole point of generating this rather than hand-keeping
    a static file. Each catches a defect that produces a 404 or a redirect chain in
    production and nothing at all in the build log.
    """
    seen, dupes = set(), set()
    for src, _ in REDIRECTS:
        dupes.add(src) if src in seen else seen.add(src)
    if dupes:
        raise SystemExit(f"ABORT: duplicate redirect sources: {sorted(dupes)}")

    dead = sorted({dst for _, dst in REDIRECTS if dst not in routes})
    if dead:
        raise SystemExit(f"ABORT: redirects point at routes that do not exist: {dead}")

    # A source that the site actually serves is a rule that can never fire, and it
    # means the map has gone stale against the build.
    shadowed = sorted({src for src, _ in REDIRECTS if src in routes})
    if shadowed:
        raise SystemExit(f"ABORT: redirect sources that are real pages: {shadowed}")

    # A chain costs a hop and dilutes what the 301 passes. There should be none.
    sources = {src for src, _ in REDIRECTS}
    chains = sorted({f"{s} -> {d}" for s, d in REDIRECTS if d in sources})
    if chains:
        raise SystemExit(f"ABORT: redirect chains: {chains}")

    # Aligned to the 95th-percentile source, not the longest — one 75-character legacy
    # URL would otherwise indent all 169 lines past it. The few that overrun just wrap.
    width = min(max(len(src) for src, _ in REDIRECTS) + 2, 56)
    lines = ["# Generated by builder/build_site.py — do not hand-edit.",
             "# Source map: scratchpad seo/redirects.csv, verified against the live site",
             "# and the Wayback CDX index 2026-08-02. 301 throughout.",
             "#",
             "# Path-only: Cloudflare Pages cannot match a hostname here, so apex -> www",
             "# is a zone Redirect Rule, not a line in this file.",
             ""]
    for src, dst in REDIRECTS:
        # ljust is a no-op once a source runs past `width`, which silently glued three
        # long legacy paths to their destination and made those lines parse as two
        # fields — so three URLs 404ed instead of redirecting. The separator has to be
        # unconditional; the padding is only cosmetic.
        lines.append(f"{src.ljust(width - 1)} {dst}  301")
    with open(os.path.join(SITE, "_redirects"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(REDIRECTS)

# ---------------------------------------------------------------- robots.txt
# Policy decision, and the reasoning is specific to this business rather than a general
# position: Extreme's content is marketing copy about furnace repair in Ohio. It has no
# licensing value, no syndication revenue and nothing behind a subscription, so there is
# nothing to protect by blocking — while the client's stated top priority is being the
# local business AI engines name. Blocking is a rational trade for a publisher whose
# articles are the product. Here it is a pure loss.
#
# Training crawlers and search crawlers are DIFFERENT BOTS WITH DIFFERENT NAMES. Both
# are allowed here. If the client ever wants a middle position, the coherent one is to
# block GPTBot / CCBot / Google-Extended (training) and keep OAI-SearchBot /
# ChatGPT-User / PerplexityBot / Claude-SearchBot (retrieval, and the only ones that
# produce a linked citation). Conflating the two is how a site accidentally removes
# itself from the channel it was trying to win.
#
# No Disallow anywhere, and specifically not on the noindexed city+service pages.
# A page blocked in robots.txt is never fetched, so its noindex is never read, and the
# URL can still be indexed title-only from internal links. Blocking and noindexing are
# opposites, not degrees of the same thing.
ROBOTS = """\
# https://www.extremeheating.com/robots.txt
# Extreme Heating, Air, Plumbing — Dayton & Cincinnati, Ohio
#
# Policy: all reputable crawlers, including AI training and AI search agents,
# are welcome on all public content. We want to be the source AI answers cite
# for heating, cooling and plumbing questions in the Dayton and Cincinnati metros.
#
# Note: pages under /locations/ that carry a noindex meta tag are intentionally
# left crawlable. Disallowing them would prevent the noindex from being read.

User-agent: *
Allow: /

# ---- OpenAI ----
# GPTBot        — training / index crawler
# OAI-SearchBot — ChatGPT search index (citation eligibility)
# ChatGPT-User  — live fetch when a user's prompt triggers browsing
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# ---- Anthropic ----
# ClaudeBot        — crawler
# Claude-SearchBot — search index
# Claude-User      — live user-triggered fetch
# Claude-Web       — legacy agent, retained for completeness
User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-Web
Allow: /

# ---- Perplexity ----
User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# ---- Google ----
# Google-Extended governs Gemini training and grounding.
# It does NOT govern AI Overviews, which follow normal Googlebot indexing
# and snippet controls.
User-agent: Google-Extended
Allow: /

# ---- Common Crawl ----
# Not an engine. A public dataset that many models train from.
User-agent: CCBot
Allow: /

# ---- Microsoft / Copilot ----
User-agent: bingbot
Allow: /

Sitemap: {sitemap}

# Human- and agent-readable summary of this site:
# {llms}
"""

def write_robots():
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(ROBOTS.format(sitemap=D.canonical("/sitemap.xml"),
                              llms=D.canonical("/llms.txt")))

# ---------------------------------------------------------------- llms.txt
# Ship it, but with the expectations set correctly: no major consumer AI engine has
# committed to reading llms.txt, published analysis finds no correlation with citation
# rate, and Google has said publicly that it ignores it. It is here because it costs an
# hour, because the agent/IDE ecosystem does read it, and because half its value is
# internal — it forces every publishable fact into one file where drift is visible.
# Do not promise the client citation lift from it.
#
# Indexed, canonical pages only. Listing the noindexed city+service pages here would
# contradict the indexation decision in the same breath as making it.
#
# Constraints this file already obeys — do not break them on edit:
#   - No service-call, dispatch or diagnostic rate appears. Those are publishable in a
#     benefit list on the site; in a machine-readable fact sheet an AI engine will
#     restate them as "the price", stripped of the membership context.
#   - The X-Plan accrual appears once, with BOTH conditions in the same sentence.
#   - Extreme Rewards is two numbers plus the terms line. No tiers, no thresholds.
#   - The review count is "customer reviews", not "Google reviews" — it is a Birdeye
#     aggregate across sources.
#   - No technician names, roles or credentials. The About team section was removed
#     pending a photo shoot; expertise attribution rests on the company, the two Ohio
#     licences and the founding date.
#   - No radon, and no rebate or utility trade-ally claim. Neither is a service the
#     company offers or a status it holds.
LLMS_SERVICES = """\
## Heating & cooling

- [Air conditioning]({u}/air-conditioning): Repair, replacement and tune-ups for residential air conditioning.
- [AC repair]({u}/ac-repair): Diagnosis and repair of residential air conditioning systems, with 24/7 emergency availability.
- [AC installation]({u}/ac-installation): Replacement and new installation of residential air conditioning systems.
- [Furnace & heating]({u}/furnace-heating): Furnace repair, replacement and safety checks.
- [Furnace repair]({u}/furnace-repair): Diagnosis and repair of gas and electric furnaces, with 24/7 emergency availability.
- [Furnace installation]({u}/furnace-installation): Furnace replacement and new installation.
- [Heat pumps]({u}/heat-pump): Heat pump service for year-round heating and cooling.
- [Heat pump repair]({u}/heat-pump-repair): Diagnosis and repair of residential heat pumps.
- [Heat pump installation]({u}/heat-pump-installation): Heat pump replacement and new installation.
- [Thermostat services]({u}/thermostat): Thermostat replacement, calibration and configuration.
- [Humidifier services]({u}/humidifier): Whole-home humidifier installation and service.
- [HVAC inspections]({u}/inspection): Heating and cooling system inspections.
- [HVAC maintenance plans]({u}/maintenance): The X-Plan membership — see below.
- [All services]({u}/services): Index of every heating, cooling and plumbing service.

## Indoor air quality

- [Indoor air quality]({u}/indoor-air-quality): Filtration, UV and humidity control for residential HVAC systems.
- [Indoor air quality solutions]({u}/indoor-air-quality-solutions): Comparison of available indoor air quality equipment.
- [Indoor air quality FAQ]({u}/iaq-faq): Common homeowner questions about indoor air quality.
- [Why indoor air quality matters]({u}/importance-iaq): Background on residential indoor air quality.
- [Duct cleaning]({u}/duct-cleaning): Air duct cleaning and air balancing.

## Plumbing

- [Plumbing services]({u}/plumbing/services): Overview of residential plumbing services.
- [Emergency plumbing]({u}/plumbing/emergency-plumbing): 24/7 response for burst pipes, major leaks and other plumbing emergencies.
- [Clogged drains]({u}/plumbing/clogged-drain): Drain cleaning for clogged and slow drains.
- [Water heaters]({u}/plumbing/water-heater/overview): Tank and tankless water heater service.
- [Water heater repair]({u}/plumbing/water-heater/repair): Diagnosis and repair of gas, electric and tankless water heaters.
- [Water heater installation]({u}/plumbing/water-heater/installation): Water heater replacement and new installation.
- [Sewer lines]({u}/plumbing/sewer-line/overview): Sewer line inspection, repair and cleaning.
- [Sewer line repair]({u}/plumbing/sewer-line/repair): Repair and replacement of residential sewer lines.
- [Sewer line cleaning]({u}/plumbing/sewer-line/cleaning): Clearing blocked and slow sewer lines.
- [Sump pumps]({u}/plumbing/sump-pump/overview): Sump pump service for basement water protection.
- [Sump pump repair]({u}/plumbing/sump-pump/repair): Diagnosis and repair of residential sump pumps.
- [Sump pump installation]({u}/plumbing/sump-pump/installation): Sump pump replacement and new installation.
- [Gas lines]({u}/plumbing/gas-line/overview): Gas line installation, repair and safety work.
- [Gas line repair]({u}/plumbing/gas-line/repair): Repair of residential natural gas lines.
- [Gas line installation]({u}/plumbing/gas-line/installation): New gas line installation for appliances and outdoor equipment.
- [Leak detection]({u}/plumbing/leak-detection): Locating hidden water leaks in residential plumbing.
- [Toilet repair]({u}/plumbing/toilet-repair): Repair and replacement of residential toilets.
- [Water treatment]({u}/plumbing/water-treatment): Water softening, filtration and treatment systems.
"""

def _llms_service_areas():
    """Featured communities get a linked line each; the rest are named, not linked.

    Generated from the SAME featured set the noindex predicate reads, so the pages this
    file points an engine at are exactly the pages that are indexed. Typing the ten out
    here would be a second copy of a list that already exists in two places.

    The non-featured cities and the nine counties are named without links on purpose.
    Their pages exist and are crawlable, but they are noindexed, and inviting an engine
    to treat them as canonical destinations would contradict that decision in the same
    file that states it.
    """
    u = D.SITE_URL
    names = dict(L.ALL)
    featured_set = getattr(shell, "FEATURED", None) or getattr(L, "FEATURED", set())
    featured = [s for s, _ in L.ALL if s in featured_set]
    counties = {s for s, _ in L.COUNTIES}
    office_by_page = {o["page"]: o for o in D.OFFICES if o["page"]}

    out = ["## Service areas", "",
           f"- [All service areas]({u}/locations): Index of all {len(L.ALL)} communities "
           "and counties served across the Dayton and Cincinnati metros."]
    for slug in featured:
        page = f"/locations/{slug}"
        office = office_by_page.get(page)
        line = f"- [{names[slug]}, OH]({u}{page})"
        if office:
            line += f": Office location - {office['oneline']}."
        out.append(line)

    rest = [names[s] for s, _ in L.ALL if s not in set(featured) and s not in counties]
    if rest:
        out += ["", "Also serving, in Ohio: " + ", ".join(rest) + "."]
    county_names = [n for s, n in L.COUNTIES if s not in set(featured)]
    if county_names:
        out += ["", "Counties served: " + ", ".join(county_names) + "."]

    # Offices without a location page still need to be findable. Waynesville has no
    # entry in locations.py, so without this it appears nowhere on the site at all.
    orphans = [o for o in D.OFFICES if not o["page"]]
    if orphans:
        out += ["", "Additional office locations: "
                + "; ".join(o["oneline"] for o in orphans) + "."]
    return "\n".join(out) + "\n"

def llms_txt():
    u = D.SITE_URL
    offices = " | ".join(o["oneline"] for o in D.OFFICES)
    # Wrapped at write time rather than hand-broken: the values are interpolated, so a
    # hand-broken blockquote goes ragged the first time a number gains a digit.
    # Second person, and only the facts that answer "who are you and how fast do you
    # get here". The founding year, the job count and the rating are not dropped — they
    # are stated once each further down, under Company, instead of stacked in one
    # 45-word sentence that names the business twice. The name is the H1 above.
    summary = textwrap.fill(
        "Locally owned heating, cooling and plumbing company for the Dayton and "
        f"Cincinnati, Ohio metros, in business since {D.FOUNDED}. We finish roughly "
        f"{D.SAME_DAY} of jobs the same day and answer the emergency line at any hour. "
        "You get the price before work starts.",
        width=86, initial_indent="> ", subsequent_indent="> ")
    head = f"""\
# {D.COMPANY}

{summary}

Phone: {D.PHONE_DISPLAY} (24/7)
Email: {D.EMAIL}
Offices: {offices}
Office hours: {D.HOURS_STAFFED}. Emergency service: {D.HOURS_EMERGENCY}.
Service area: {len(L.ALL)} communities and counties across the Dayton and Cincinnati, Ohio metros.
Trades: heating, cooling, indoor air quality, and residential plumbing.
Licenses: HVAC {D.LICENSE_HVAC}; plumbing {D.LICENSE_PLUMBING}.
Legal entities: {D.ENTITY_HVAC.replace("&amp;", "&")} (HVAC), {D.ENTITY_PLUMBING} (plumbing).
Pricing: a flat number, quoted before we start.
"""
    programs = f"""\
## Membership, offers and financing

- [X-Plan maintenance membership]({u}/maintenance): {D.XPLAN["annual"]} a year, or {D.XPLAN["monthly"]} a month {D.XPLAN["monthlyNote"]}. You get two seasonal safety and performance visits, 15% off every repair, priority scheduling, a lower service-call fee that also applies after hours and on holidays, and a 5-year warranty on qualified repairs. Stay a member in consecutive years and every dollar you have paid comes off the cost of replacing that system at end of life, up to $2,500 or 10 years, whichever comes first. The credit follows you, not the house.
- [Extreme Rewards referral program]({u}/referral): Refer a friend and whatever they save, you earn. They save {D.REWARDS["newSystem"]} on a new heating, cooling or plumbing system, or {D.REWARDS["everythingElse"]} on everything else, and you get the same amount on a Visa gift card. New customers only. Name them when the job is booked, and we send your reward within 90 days of finishing the job.
- [Current specials]({u}/specials): Whatever we're running right now.
- [Financing options]({u}/financing-options): Monthly payment plans through {", ".join(D.LENDERS[:-1])} and {D.LENDERS[-1]}.
"""
    company = f"""\
## Company

- [About]({u}/about): Locally owned and operated since {D.FOUNDED}, with {D.JOBS_COMPLETED_LONG} jobs behind us. The Mason office opened in {D.MASON_OPENED}.
- [Contact]({u}/contact): Phone, office addresses and hours.
- [Reviews]({dict(D.SOCIAL)["Google Reviews"]}): {D.GOOGLE_RATING}-star average across {D.REVIEW_COUNT} {D.REVIEW_SOURCE}.

## Optional

- [Terms]({u}/terms): Terms of service, program terms and legal entity information.
"""
    return "\n".join([head, LLMS_SERVICES.format(u=u), _llms_service_areas(),
                      programs, company])

def write_llms():
    text = llms_txt()
    # The one claim class that must never reach a machine-readable fact sheet.
    for bad in ("$77", "$97", "$177", "$197", "radon", "rebate", "trade ally"):
        if bad.lower() in text.lower():
            raise SystemExit(f"ABORT: llms.txt contains a prohibited claim: {bad!r}")
    with open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(text)

# ---------------------------------------------------------------- sitemap
# Pages whose absence would be catastrophic and quiet. Cheap to check, and it also
# regression-guards the three pages the live Framer sitemap was missing entirely
# (/furnace-installation, /furnace-repair, /terms).
MUST_INDEX = ("/", "/about", "/contact", "/locations", "/services", "/specials",
              "/maintenance", "/air-conditioning", "/furnace-heating",
              "/furnace-installation", "/furnace-repair", "/terms",
              "/plumbing/services", "/locations/dayton", "/locations/cincinnati")

# ---------------------------------------------------------------- cache headers
# Cloudflare Pages reads this. It only matters because the extracted CSS is named by
# the hash of its own contents: a change ships a new filename, so the old one can be
# cached forever without any risk of serving stale styles. Without this the browser
# revalidates on every navigation and the extraction buys far less than it should.
#
# HTML is deliberately NOT cached long. A stale page is a wrong phone number or a
# wrong price sitting in someone's browser, and this site publishes both.
def write_headers():
    text = """\
# Generated by builder/build_site.py — do not hand-edit.

# Content-hashed filenames. Safe to cache forever; a change is a new URL.
/assets/css/*
  Cache-Control: public, max-age=31536000, immutable

/assets/js/*
  Cache-Control: public, max-age=31536000, immutable

# Images are not content-hashed, so a day, not a year.
/assets/*
  Cache-Control: public, max-age=86400

# HTML must revalidate: prices and phone numbers live in it.
/*
  Cache-Control: public, max-age=0, must-revalidate
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
"""
    with open(os.path.join(SITE, "_headers"), "w", encoding="utf-8") as f:
        f.write(text)

def write_sitemap(written):
    """Indexable routes only.

    A URL that is both submitted in the sitemap and carries a noindex tag is a Search
    Console error on every one of them, and it is the most common way a deliberate
    noindex gets read as a bug and then "fixed" by someone six months from now. The
    SAME predicate writes the tag and filters this list, so the two cannot disagree.
    """
    all_urls = sorted(set(written))
    indexable = [u for u in all_urls if not _noindex(u)]
    suppressed = len(all_urls) - len(indexable)

    # Guardrail. The failure this exists to catch is silent and would not surface until
    # traffic vanished: a bad FEATURED list, a renamed slug or a changed URL shape
    # suppressing far more than intended.
    #
    # shell exports the expected count, computed from the same data its predicate
    # reads, so the guardrail cannot disagree with the tag it is guarding. Recomputing
    # it here from locations.py would be a second opinion, which is the whole failure
    # mode. The fallback only exists for a tree where shell has not landed it yet.
    expected = getattr(shell, "NOINDEX_EXPECTED", None)
    if expected is None and getattr(L, "FEATURED", None) is not None:
        expected = (len(L.ALL) - len(L.FEATURED)) * len(L.SERVICES)
    if expected is None:
        if suppressed:
            raise SystemExit(f"ABORT: {suppressed} pages noindexed but neither "
                             "shell.NOINDEX_EXPECTED nor locations.FEATURED exists, so "
                             "the count cannot be checked.")
    elif suppressed != expected:
        raise SystemExit(f"ABORT: {suppressed} pages noindexed, expected {expected}. "
                         "Check locations.FEATURED and shell.noindex before shipping.")

    for must in MUST_INDEX:
        if must not in indexable:
            raise SystemExit(f"ABORT: {must} is not in the sitemap.")

    # <lastmod> from the same ledger shell.py stamps dateModified from, so the sitemap
    # and the schema on the page can never claim two different dates for one URL. The
    # ledger is keyed on a content hash, so a date only moves when the page's own
    # content actually changed — a rebuild that changes nothing leaves every date
    # alone, which is the property that makes lastmod worth sending at all. A sitemap
    # that restamps today on all 136 URLs every deploy teaches Google to ignore it.
    ledger = getattr(shell, "DATES", None)
    if ledger is None:
        try:
            import json
            with open(os.path.join(HERE, "content_dates.json"), encoding="utf-8") as f:
                ledger = json.load(f)
        except (OSError, ValueError):
            ledger = {}

    def _lastmod(u):
        rec = ledger.get(u) or {}
        d = rec.get("modified") or rec.get("published")
        return f"<lastmod>{d}</lastmod>" if d else ""

    missing = [u for u in indexable if not _lastmod(u)]
    if missing:
        print(f"  ! {len(missing)} indexable URLs have no date in the ledger, "
              f"e.g. {missing[:3]}")
    urls = "".join(f"<url><loc>{D.canonical(u)}</loc>{_lastmod(u)}</url>"
                   for u in indexable)
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>'
                f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    return indexable, suppressed

# ------------------------------------------------------- shared CSS extraction
# Measured before writing this: the site ships 19.92 MB of CSS across 320 documents,
# and 18.45 MB of that is two byte-identical blocks repeated on 320 and 274 pages.
# A sub page like /furnace-repair is 107 KB, of which 66 KB is CSS that every other
# sub page also carries. The bytes are not the whole cost — that CSS is re-parsed from
# scratch on every navigation, because an inline <style> cannot be cached.
#
# Extracting the shared blocks to hashed files under /assets/css/ makes them
# immutable-cacheable: one download, then zero on every page after it. Page-specific
# CSS (the homepage's own block, for instance) stays inline, because a file fetched
# once and never reused is a round trip for nothing.
#
# The hash is the filename, so a CSS change ships a new URL and no stale cache can
# survive it. Order is preserved exactly: links are emitted in the order the blocks
# appeared in the document, all hoisted into <head>, so the cascade is unchanged.
CSS_SHARED_MIN_PAGES = 20        # below this, an extra request costs more than it saves
_STYLE_RE = re.compile(r'(?is)<style[^>]*>(.*?)</style>')

def _extract_shared_css(docs):
    """docs: {url: html}. Returns (docs, files, saved_bytes)."""
    counts = collections.Counter()
    for html in docs.values():
        for css in set(_STYLE_RE.findall(html)):     # set: one vote per page
            counts[css] += 1
    shared = {css: hashlib.sha1(css.encode()).hexdigest()[:12]
              for css, n in counts.items() if n >= CSS_SHARED_MIN_PAGES}
    if not shared:
        return docs, {}, 0

    files = {f"{h}.css": css for css, h in shared.items()}
    saved = sum(len(css) * (counts[css] - 1) for css in shared)

    out = {}
    for url, html in docs.items():
        links = []
        def repl(m):
            css = m.group(1)
            h = shared.get(css)
            if h is None:
                return m.group(0)                     # page-specific: leave inline
            href = f"/assets/css/{h}.css"
            if href not in links:
                links.append(href)
            return ""
        stripped = _STYLE_RE.sub(repl, html)
        if links:
            tags = "".join(f'<link rel="stylesheet" href="{u}">' for u in links)
            # Into <head>, at the point the first block used to sit.
            stripped = stripped.replace("</head>", tags + "</head>", 1)
        out[url] = stripped
    return out, files, saved

# ---------------------------------------------------------------- 404
# Cloudflare Pages serves /404.html for any unmatched path, with a real 404 status.
# Without it the 10 orphaned live URLs and every mistyped link land on Cloudflare's
# own unbranded page. Noindexed because Pages also makes the file reachable at /404
# with a 200, and it is written outside `written` so it never enters the sitemap.
def write_404():
    body = f'''<section class="xsp-sec"><div class="xsp-wrap">
<h1>That page isn't here anymore.</h1>
<p class="xsp-intro">The link may be old, or we may have moved it. If your heat is out
or there's water where it shouldn't be, don't go hunting for a page — call
<a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>. Someone answers 24/7, every day of the
year.</p>
<p><a href="/">Home</a> &middot; <a href="/services">All services</a> &middot;
<a href="/locations">Service areas</a> &middot; <a href="/contact">Contact</a></p>
</div></section>'''
    meta = {"url": "/404", "nav": "", "noindex": True,
            "title": f"Page not found | {D.COMPANY}",
            "description": "That page has moved or no longer exists."}
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(shell.document(meta, body))

# ---------------------------------------------------------------- build
def main():
    # regenerate the embeds first so site/ can never be built from stale input
    subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True,
                   stdout=subprocess.DEVNULL)
    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(SITE, exist_ok=True)

    written = []
    # Documents are held in memory until every one exists, because the shared-CSS pass
    # needs to know how many pages carry a given block before it can decide whether
    # extracting it is worth a request. 320 documents is ~34 MB — fine to hold, and it
    # is the only way the decision can be made on evidence rather than a guess.
    docs = {}

    # --- homepage: authored directly, not an embed ---
    # homepage.META has no "noindex" key and document() reads it with .get(), so the
    # homepage and every future hand-authored page default to indexable. Fails open.
    docs["/"] = shell.document(homepage.META, homepage.homepage())
    written.append("/")

    # --- every generated page ---
    for root, _, files in os.walk(PAGES):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, name), PAGES)
            html = open(os.path.join(root, name), encoding="utf-8").read()
            url = route_for(rel)
            meta = shell.meta_for(rel, html)
            meta["url"] = url
            meta["nav"] = "/" + url.split("/")[1] if url != "/" else ""
            meta["noindex"] = _noindex(url)
            body = shell._strip_embed(html)
            docs[url] = shell.document(meta, body)
            written.append(url)

    before = sum(len(h) for h in docs.values())
    docs, css_files, css_saved = _extract_shared_css(docs)
    if css_files:
        css_dir = os.path.join(SITE, "assets", "css")
        os.makedirs(css_dir, exist_ok=True)
        for fname, css in css_files.items():
            with open(os.path.join(css_dir, fname), "w", encoding="utf-8") as f:
                f.write(css)
        after = sum(len(h) for h in docs.values())
        print(f"  shared CSS: {len(css_files)} file(s), "
              f"{sum(len(c) for c in css_files.values())/1024:.0f} KB cached once; "
              f"HTML {before/1024/1024:.1f} -> {after/1024/1024:.1f} MB "
              f"({css_saved/1024/1024:.1f} MB of duplication removed)")

    for url, html in docs.items():
        dest = out_path(url)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)

    # --- schedule wizard bundle ---
    # Built by `npm run build:schedule` and committed to assets/js/, because site/ is
    # generated and gitignored. Missing bundle is a warning, not a failure: the loader
    # in chrome.py falls back to /contact if the script 404s.
    src_js = os.path.join(ROOT, "assets", "js", "schedule.js")
    if os.path.exists(src_js):
        os.makedirs(os.path.join(SITE, "js"), exist_ok=True)
        shutil.copy2(src_js, os.path.join(SITE, "js", "schedule.js"))
    else:
        print("  ! assets/js/schedule.js missing — run: npm run build:schedule")

    # --- favicons ---
    # Served same-origin rather than from the CDN: the browser requests /favicon.ico
    # on every page load whether or not it is declared, and it was 404ing on all 307.
    # og-default.jpg rides along here for the same reason: shell.py names it at the
    # site root, and it was 404ing on the handful of pages that render no content
    # image of their own — so those pages shared with no preview card at all.
    for src_name, dest_name in (("logo-icon.ico", "favicon.ico"),
                                ("apple-touch-icon.png", "apple-touch-icon.png"),
                                ("og-default.jpg", "og-default.jpg")):
        src = os.path.join(ROOT, "assets", "brand", src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(SITE, dest_name))
        else:
            print(f"  ! assets/brand/{src_name} missing")

    # --- assets, same-origin ---
    # Copied unconditionally so that flipping template.ASSET_BASE from the jsDelivr URL
    # to "/assets" is a one-line change that cannot break the site. Today the pages
    # still reference the CDN, so this tree is unreferenced weight (~13 MB in a
    # gitignored directory) — cheap insurance against a half-landed migration.
    # print/ is excluded: press-resolution artwork nobody requests over HTTP.
    assets_src = os.path.join(ROOT, "assets")
    if os.path.isdir(assets_src):
        shutil.copytree(assets_src, os.path.join(SITE, "assets"), dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("print", "*.afdesign"))

    write_404()

    routes = set(written)
    n_redirects = write_redirects(routes)
    indexable, suppressed = write_sitemap(written)
    write_robots()
    write_llms()
    write_headers()

    print(f"site/ built — {len(written)} pages, {len(indexable)} indexable, "
          f"{suppressed} noindexed, {n_redirects} redirects")
    return written

if __name__ == "__main__":
    main()
