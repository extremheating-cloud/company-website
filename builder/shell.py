"""Full HTML documents for the self-hosted site: head, meta, indexation and JSON-LD.

The Framer build wraps each page's content in a `srcdoc` iframe, so the page itself
has a title and meta description and then no headings at all — measured on the live
site, `/locations/dayton` renders zero `<h1>` and 41x more copy inside iframes than
outside. This module is what fixes that: same content, in the document, where a
crawler reads it.

Three things live here, and each one has a rule that governs it.

1. **Titles and descriptions are authored data, not derived from the page.** A title
   is keyword-first copy for someone deciding whether to click; an H1 is brand voice
   for someone who already arrived. Deriving one from the other guarantees one of them
   is wrong, and before this module it was the title on all 311 routes — `/ac-repair`
   was titled "Cool air back — usually the same day." and did not contain the string
   "AC repair". Titles are now generated from a per-route keyword phrase through a
   length ladder, with `OVERRIDES` as the escape hatch.

2. **Structured data is read out of the rendered HTML, never passed in beside it.**
   Breadcrumb, FAQ, video and primary image are extracted from `body_html` with
   regexes. That makes schema/visible-content mismatch — the thing that earns a manual
   action — structurally impossible: delete an FAQ block and its `FAQPage` markup goes
   with it. It also avoids threading a parallel data path through six page modules
   that `build_site.py` would then throw away.

3. **Nothing is asserted that is not confirmed.** Unknown values are `None` and are
   pruned before output. A missing property costs a warning; a wrong one costs a
   citation cleanup across every aggregator that scraped it.

Output goes to site/, leaving pages/ as the Framer embeds so both stay buildable
until cutover.
"""
import atexit
import datetime as _dt
import hashlib
import html as _html
import json
import os
import re

import site_data as D
import locations as L
import chrome

HERE = os.path.dirname(os.path.abspath(__file__))

# Non-fatal problems worth seeing at the end of a build. Nothing in here stops the
# build; everything in here is a thing a human has to supply.
WARNINGS = []

def _warn(msg):
    if msg not in WARNINGS:
        WARNINGS.append(msg)

FONT = ("https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@"
        "0,400;0,500;0,600;0,700;0,800;0,900;1,800;1,900&display=swap")

BASE_CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:#0F172A;color-scheme:light;
font-family:"Montserrat","Montserrat Fallback",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial;
overflow-x:hidden}
img{max-width:100%}
main{display:block}
/* "Montserrat Fallback" is named here and in template.py's .xhac-svc stack but is not
   declared yet. An undeclared family is skipped by the browser, so this is inert until
   the metric-overridden @font-face lands (performance.md 7.2, which measured this
   site's CLS as fonts rather than unsized images). Naming it in both stacks now means
   that swap is one @font-face block and no stack edits. */
/* The header is sticky, so a hash link would otherwise land its target underneath
   it. The embed script measured this at jump time; standalone it is one rule. */
[id]{scroll-margin-top:96px}
:where(a,button,input,summary):focus-visible{outline:3px solid #61BC47;outline-offset:2px}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:#5F2980;padding:12px 18px;
font-weight:800;z-index:1000;border-radius:0 0 10px 0}
.skip:focus{left:0}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;
animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
"""

def _strip_embed(html):
    """The generated pages are Framer embeds: a <section class="xhac-svc"> carrying its
    own <style> and <script>. For the standalone site we keep all of it — the CSS and
    behaviour are the same — but the anchor script's cross-frame handling is dead
    weight without an iframe, so it is removed rather than left to no-op."""
    html = re.sub(r'\n?\s*<script>\s*\(\(\) => \{\s*const root = document\.currentScript'
                  r'.*?</script>', "", html, flags=re.S)
    return html.strip()


# ============================================================ URLs
# URL FORM: no trailing slash, except the homepage. Verified 2026-08-02 against the
# live site — /about serves 200 and /about/ 308s to /about, and Cloudflare Pages does
# the same with dir/index.html output. Keeping this form is what preserves parity with
# every currently-indexed URL and every backlink; do not "fix" it to trailing slashes.
#
# One function turns a route into an absolute URL, so canonical, og:url, the sitemap
# and every @id in the graph cannot drift apart.

def canonical(path="/"):
    """Absolute canonical URL for a route. Delegates to site_data.canonical() if that
    exists, so this file does not become a second definition of the host."""
    fn = getattr(D, "canonical", None)
    if callable(fn):
        return fn(path)
    p = "/" + str(path).strip("/")
    return D.SITE_URL + ("/" if p == "/" else p)


def route_for(rel):
    """The URL a generated file is served at. The single definition — `meta_for` and
    `build_site` both call this, so a route can never be computed two ways.

    hvac/ and company/ are build-time grouping, not URL structure; the live site
    serves those pages at the root. /locations/<city>/overview.html serves at
    /locations/<city>, but the plumbing families genuinely live at
    /plumbing/<family>/overview — that is the live URL and what every internal link
    points at. Only the locations case collapses. The prefix strips are anchored
    rather than global: a global .replace("/hvac/", "/") would also rewrite a route
    that merely contained the segment.
    """
    url = "/" + rel.replace(os.sep, "/").replace("\\", "/")
    if url.startswith("/locations/") and url.endswith("/overview.html"):
        url = url[: -len("/overview.html")]
    elif url.endswith(".html"):
        url = url[: -len(".html")]
    for prefix in ("/hvac/", "/company/"):
        if url.startswith(prefix):
            url = "/" + url[len(prefix):]
            break
    return "/" if url in ("", "/index") else url


# ============================================================ indexation
# The ten communities that get genuinely local, indexed city+service pages. Everywhere
# else keeps its city+service pages for users and internal linking, noindexed rather
# than competing with each other on near-identical copy. The nine county overviews go
# too: a county page is always a superset of its city pages and is the likeliest
# source of duplicate-content dilution.
#
# The list lives in locations.py when that file defines it; the copy here is a
# fallback so this module can never noindex the wrong set because another module was
# mid-edit.
FEATURED_FALLBACK = {
    "dayton", "cincinnati",                        # metro anchors
    "beavercreek", "mason", "troy",                # office communities
    "kettering", "centerville", "springboro",      # Dayton metro
    "west-chester", "middletown",                  # Cincinnati metro
}

_CITY_SLUGS = {s for s, _ in L.ALL}
_SERVICE_SLUGS = {s for s, _ in L.SERVICES}
_COUNTY_SLUGS = {s for s, _ in L.COUNTIES}

FEATURED = set(getattr(L, "FEATURED", ()) or FEATURED_FALLBACK)

# A sitewide noindex is the one failure mode that must be impossible, so the predicate
# is disabled outright unless the featured set is recognisably sane: every slug has a
# page, and the set is neither empty nor most of the site. A disabled predicate means
# pages that should have been suppressed get indexed — recoverable in an afternoon. A
# sitewide noindex is not.
NOINDEX_ENABLED = bool(FEATURED) and FEATURED <= _CITY_SLUGS and 5 <= len(FEATURED) <= 20
if not NOINDEX_ENABLED:
    _warn("shell.FEATURED is not a sane subset of locations.ALL "
          f"({sorted(FEATURED - _CITY_SLUGS)[:5]}) — noindex() is disabled and every "
          "page will be indexable. Fix locations.FEATURED before shipping.")

# What build_site.py should assert its suppressed count against. Computed from the
# same data the predicate reads, so the guardrail cannot disagree with the tag.
NOINDEX_EXPECTED = (((len(_CITY_SLUGS) - len(FEATURED)) * len(_SERVICE_SLUGS))
                    + len(_COUNTY_SLUGS)) if NOINDEX_ENABLED else 0


def noindex(url):
    """True for the pages that stay crawlable but out of the index.

    Two families, and nothing else:
      * /locations/<city>/<service> outside the ten featured communities  (168)
      * /locations/<county>                                                (9)

    DELIBERATELY FAILS CLOSED TO INDEXABLE. It returns True only when the URL is
    exactly two or three segments, the first is `locations`, and every remaining
    segment is a slug that exists in locations.py. A typo, a renamed slug, an empty
    FEATURED set or a future page at a new path therefore cannot noindex anything.

    The /locations hub, the 38 city overviews, every root service page and the whole
    /plumbing tree are unreachable from this function by construction.
    """
    if not NOINDEX_ENABLED:
        return False
    parts = [p for p in str(url).strip("/").split("/") if p]
    if not parts or parts[0] != "locations":
        return False
    if len(parts) == 2:
        return parts[1] in _COUNTY_SLUGS
    if len(parts) == 3:
        city, service = parts[1], parts[2]
        if city not in _CITY_SLUGS or service not in _SERVICE_SLUGS:
            return False
        return city not in FEATURED
    return False


# ============================================================ titles + descriptions
TITLE_MAX, DESC_MAX = 59, 155

# Longest brand suffix that still fits. Both strings are the canonical name or a clean
# prefix of it, so no fifth entity variant is introduced.
BRAND = [D.COMPANY, D.COMPANY_SHORT]
# Longest metro token that still fits, for non-city pages.
METRO = ["Dayton & Cincinnati, OH", "Dayton & Cincinnati", "Dayton, OH"]

_PHONE = D.PHONE_DISPLAY


def fit_title(cores, brand=None):
    """Longest (keyword phrase, metro token, brand suffix) combination that fits.

    Priority order is deliberate: degrade the keyword phrase BEFORE the metro token,
    and the metro token before the brand suffix — and never drop the brand. Looping
    these the other way costs five core pages their Cincinnati token for the sake of
    words like "Replacement", which Google already resolves as a synonym. A phrase
    that already names Extreme takes no suffix.
    """
    brand = BRAND if brand is None else brand
    templated = any("{M}" in c for c in cores)
    for m in (METRO if templated else [""]):
        for core in cores:
            c = core.replace("{M}", m)
            if "Extreme" in c:
                if len(c) <= TITLE_MAX:
                    return c
                continue
            for b in brand:
                t = f"{c} | {b}"
                if len(t) <= TITLE_MAX:
                    return t
    raise ValueError(f"no title fits within {TITLE_MAX} chars: {cores!r}")


# --- city pages -------------------------------------------------------------
CITY_TITLE = {
    "": ["HVAC & Plumbing in {C}, OH", "HVAC in {C}, OH"],
    "heating": ["Furnace Repair & Heating in {C}, OH", "Furnace Repair in {C}, OH"],
    "cooling": ["AC Repair & Installation in {C}, OH", "AC Repair in {C}, OH"],
    "maintenance": ["HVAC Tune-Ups & Maintenance in {C}, OH", "HVAC Maintenance in {C}, OH"],
    "duct-cleaning": ["Air Duct Cleaning in {C}, OH"],
    "indoor-air-quality": ["Indoor Air Quality in {C}, OH"],
    "plumbing": ["Plumbers in {C}, OH"],
}

# Four variants per service, selected by the city's index in locations.ALL, so
# adjacent city pages differ in sentence structure and not only in the substituted
# city name. Every one is city-bearing and ends in the phone number.
CITY_DESC = {
"": [
 "Furnace, AC and plumbing service for {C}, OH homes. 24/7 emergency line, upfront pricing, 90% same-day service. Call " + _PHONE + ".",
 "Local heating, cooling and plumbing in {C}, OH. Licensed and insured techs, upfront pricing, 24/7 emergency service. Call " + _PHONE + ".",
 "{C}, OH heating, cooling and plumbing from a locally owned team — over 20 years, 25k+ jobs, 24/7 service. Call " + _PHONE + ".",
 "HVAC and plumbing for {C}, OH: repairs, replacements and tune-ups. 4.9 stars, 90% same-day service. Call " + _PHONE + ".",
],
"heating": [
 "Furnace repair, replacement and heat pumps in {C}, OH. 24/7 no-heat line, upfront pricing, all makes and models. Call " + _PHONE + ".",
 "No heat in {C}, OH? Furnace repair and replacement from licensed techs, with a flat quote before work starts. Call " + _PHONE + ".",
 "{C}, OH furnace repair and installation. Every brand, every age, diagnosed and quoted upfront. 24/7 no-heat line. Call " + _PHONE + ".",
 "Heating repair and furnace installation for {C}, OH homes. 90% same-day service and upfront pricing, 24/7. Call " + _PHONE + ".",
],
"cooling": [
 "AC repair and installation in {C}, OH. Same-day in most cases, upfront pricing, every make and model. Call " + _PHONE + ".",
 "Air conditioner not cooling in {C}, OH? Repair, replacement and tune-ups with a flat quote before work starts. Call " + _PHONE + ".",
 "{C}, OH AC repair and replacement from licensed, insured techs. 90% same-day service and upfront pricing. Call " + _PHONE + ".",
 "Cooling repair and new AC installation for {C}, OH homes. Right-sized systems, upfront pricing, 24/7 line. Call " + _PHONE + ".",
],
"maintenance": [
 "Furnace and AC tune-ups in {C}, OH — two seasonal visits a year, written reports. X-Plan is $20.75/month. Call " + _PHONE + ".",
 "HVAC maintenance for {C}, OH homes: seasonal safety and performance checks with warranty-valid documentation. Call " + _PHONE + ".",
 "{C}, OH furnace and AC tune-ups done properly, not a once-over. X-Plan is $249/year or $20.75/month. Call " + _PHONE + ".",
 "Seasonal HVAC tune-ups in {C}, OH. Spring for cooling, fall for heating — or let X-Plan schedule both. Call " + _PHONE + ".",
],
"duct-cleaning": [
 "Whole-home air duct cleaning in {C}, OH. Negative-pressure equipment, dryer vents too, before/after photos. Call " + _PHONE + ".",
 "{C}, OH duct and dryer-vent cleaning with camera proof before and after. We look first and tell you straight. Call " + _PHONE + ".",
 "Air duct cleaning for {C}, OH homes — supply and return runs, registers, blower compartment, dryer vents. Call " + _PHONE + ".",
 "Dusty vents in {C}, OH? Whole-system duct cleaning with before/after photos and upfront pricing, no upsell. Call " + _PHONE + ".",
],
"indoor-air-quality": [
 "Indoor air quality for {C}, OH homes: filtration, UV purification, humidifiers and fresh-air ventilation. Call " + _PHONE + ".",
 "{C}, OH air purifiers, whole-home filters and humidity control. We test your air first, then recommend. Call " + _PHONE + ".",
 "Allergies worse indoors in {C}, OH? Whole-home filtration, purifiers and humidity control, installed right. Call " + _PHONE + ".",
 "Air quality assessment and whole-home filtration in {C}, OH. Honest recommendations from licensed techs. Call " + _PHONE + ".",
],
"plumbing": [
 "Plumbers in {C}, OH — water heaters, drains, leaks and sump pumps. Licensed, insured, upfront pricing, 24/7. Call " + _PHONE + ".",
 "{C}, OH plumbing from the team you already trust with your HVAC. Same-day water-heater swaps in most cases. Call " + _PHONE + ".",
 "Drain cleaning, water heaters and leak repair in {C}, OH. Licensed plumbers, flat quotes, 24/7 emergency line. Call " + _PHONE + ".",
 "Need a plumber in {C}, OH? Water heaters, clogged drains, sump pumps and sewer lines, priced upfront. Call " + _PHONE + ".",
],
}

# The ten indexed communities get hand-written overview descriptions carrying office
# and proof detail the template cannot. These are the pages that have to earn a click.
# Every fact here comes from site_data.py or the approved proof points.
CITY_DESC_OVERRIDE = {
 "dayton": "Heating, cooling and plumbing across Dayton, OH from a locally owned team — over 20 years, 25k+ jobs, 4.9 stars, 24/7 service.",
 "cincinnati": "HVAC and plumbing across Cincinnati, OH, dispatched from our Mason office. 24/7 emergency line and 90% same-day service.",
 "beavercreek": "Our Beavercreek office is at 712 N Fairfield Rd. Furnace, AC and plumbing service for Beavercreek, OH, with a 24/7 line.",
 "mason": "Our Mason office is at 5633 Tylersville Rd. Heating, cooling and plumbing for Mason, OH and the Cincinnati metro, 24/7.",
 "kettering": "Furnace, AC and plumbing service for Kettering, OH, dispatched from our Beavercreek office. 24/7 emergency line.",
 "centerville": "HVAC and plumbing for Centerville, OH homes — locally owned for over 20 years, 90% same-day service, upfront pricing.",
 "huber": "Heating, cooling and plumbing for Huber Heights, OH. 24/7 emergency line, 90% same-day service, upfront pricing.",
 "west-chester": "HVAC and plumbing for West Chester, OH, dispatched from our Mason office. 24/7 emergency line and upfront pricing.",
 "fairborn": "Furnace, AC and plumbing service for Fairborn, OH, dispatched from our Beavercreek office. 24/7 emergency line.",
 "springfield": "Heating, cooling and plumbing for Springfield, OH — locally owned for over 20 years, 24/7 emergency service.",
}

# --- the 45 non-city routes -------------------------------------------------
# route -> (title core variants richest-first, description)
CORE = {
"/": (["HVAC & Plumbing in {M}"],
 "Heating, cooling and plumbing for Dayton and Cincinnati homes. Over 20 years, 25k+ jobs, 24/7 emergency service, 90% same-day service."),
"/services": (["HVAC & Plumbing Services in {M}"],
 "Every heating, cooling and plumbing service we offer across Dayton and Cincinnati — repairs, replacements, tune-ups, drains, water heaters."),
"/locations": (["HVAC & Plumbing Service Area: {M}", "HVAC Service Area: {M}"],
 "38 communities across the Dayton and Cincinnati metros, one phone number. Find your town and see what we cover. Call " + _PHONE + "."),
"/specials": (["HVAC Specials & Coupons in {M}"],
 "Current offers on the heating, cooling and plumbing work you actually need in Dayton and Cincinnati. Mention the offer when you book."),
"/financing-options": (["HVAC Financing in {M}"],
 "Finance a new furnace, AC or heat pump through GoodLeap, Synchrony or Wright-Patt Credit Union. Monthly payments and free replacement estimates."),
"/about": (["About Extreme Heating, Air, Plumbing | Dayton, OH"],
 "Locally owned heating, cooling and plumbing for Dayton and Cincinnati for over 20 years — 25k+ jobs completed, 4.9 stars, licensed and insured."),
"/contact": (["Contact Us | Extreme Heating, Air, Plumbing"],
 "Call " + _PHONE + " or book online in about a minute. Beavercreek and Mason, OH offices, with emergency service answered 24/7."),
"/referral": (["Extreme Rewards Referral Program | Give $250, Get $250"],
 "Extreme Rewards: your friend saves $250 on a new heating, cooling or plumbing system or $100 on everything else, and you earn what they saved."),
"/terms": (["Terms of Service & Limited Warranty"],
 "Terms of service and limited warranty covering estimates, invoices and work performed by Extreme Heating & Cooling LLC and Extreme Home Services LLC."),

# --- HVAC detail ---
"/air-conditioning": (["Air Conditioning Services in {M}"],
 "AC repair, replacement and tune-ups across Dayton and Cincinnati. Upfront pricing, every make and model, and a 24/7 emergency line."),
"/furnace-heating": (["Heating & Furnace Services in {M}"],
 "Furnace repair, installation and safety checks for Dayton and Cincinnati homes. Upfront pricing, all makes and models, 24/7 no-heat line."),
"/heat-pump": (["Heat Pump Services in {M}"],
 "Heat pump repair, installation and tune-ups in Dayton and Cincinnati — how they actually perform in an Ohio winter, and what drives the cost."),
"/duct-cleaning": (["Air Duct Cleaning in {M}"],
 "Whole-home duct and dryer-vent cleaning for Dayton and Cincinnati, with camera photos before and after. Upfront pricing, no upsell."),
"/indoor-air-quality": (["Indoor Air Quality Services in {M}", "Indoor Air Quality in {M}"],
 "Whole-home filtration, UV purification, humidifiers and fresh-air ventilation for Dayton and Cincinnati homes. We test first, then recommend."),
"/maintenance": (["HVAC Maintenance Plans in {M}"],
 "Seasonal furnace and AC tune-ups, plus X-Plan membership at $249/year or $20.75/month — two visits a year, 15% off repairs, priority scheduling."),
"/inspection": (["HVAC Inspections in {M}"],
 "Full-system HVAC inspections across Dayton and Cincinnati — before a home purchase, before winter, or for an honest second opinion."),
"/thermostat": (["Thermostat Installation in {M}"],
 "Smart thermostat installation, setup and troubleshooting in Dayton and Cincinnati, including homes wired without a C-wire."),
"/humidifier": (["Whole-House Humidifiers in {M}"],
 "Whole-house humidifier installation and repair for Dayton and Cincinnati — end static shocks, dry skin and cracking trim in Ohio winters."),

# --- HVAC sub-pages ---
"/ac-repair": (["AC Repair in {M}"],
 "AC blowing warm? Air conditioner repair across Dayton and Cincinnati, every make and model, quoted flat before work starts. 24/7 line."),
"/ac-installation": (["AC Installation & Replacement in {M}", "AC Installation in {M}"],
 "New air conditioner installation across Dayton and Cincinnati — honest sizing math, high-efficiency options, free estimates and financing."),
"/furnace-repair": (["Furnace Repair in {M}"],
 "No heat is an emergency. Furnace repair across Dayton and Cincinnati, all makes and models, quoted flat before work starts. Answered 24/7."),
"/furnace-installation": (["Furnace Installation & Replacement in {M}", "Furnace Installation in {M}"],
 "New furnace installation across Dayton and Cincinnati — right-sized, installed to code, with efficiency options and monthly financing."),
"/heat-pump-repair": (["Heat Pump Repair in {M}"],
 "Heat pump not heating or cooling in Dayton or Cincinnati? Diagnosed fast and quoted flat — and we'll tell you when winter icing is normal."),
"/heat-pump-installation": (["Heat Pump Installation in {M}"],
 "Heat pump and dual-fuel installation across Dayton and Cincinnati, sized for Ohio winters with backup heat configured properly."),
"/indoor-air-quality-solutions": (["Whole-House Air Purifiers in {M}"],
 "UV lights, media filters, HEPA and air scrubbers compared side by side — what each one removes, and which fits your Ohio home."),
"/importance-iaq": (["Why Indoor Air Quality Matters in Your Home"],
 "Indoor air is often more polluted than the air outside. What that means for your sleep, allergies and home — and how to find out."),
"/iaq-faq": (["Indoor Air Quality FAQ: Filters, UV & Humidity"],
 "MERV ratings, filter changes, UV lights, winter humidity and duct cleaning — the questions homeowners actually ask, answered straight."),

# --- Plumbing ---
"/plumbing/services": (["Plumbers in {M}"],
 "Licensed plumbers across Dayton and Cincinnati — water heaters, drains, leaks, sewer lines and sump pumps, all priced upfront."),
"/plumbing/clogged-drain": (["Drain Cleaning in {M}"],
 "Drain cleaning across Dayton and Cincinnati — snaking or hydro jetting, with a camera check when a clog keeps coming back."),
"/plumbing/water-heater/overview": (["Water Heater Services in {M}"],
 "Tank, tankless or heat pump water heater? Compare cost, lifespan and hot-water capacity, then get it installed in Dayton or Cincinnati."),
"/plumbing/water-heater/repair": (["Water Heater Repair in {M}"],
 "No hot water? Water heater repair across Dayton and Cincinnati — leaks, pilot lights, thermostats and elements, same day in most cases."),
"/plumbing/water-heater/installation": (["Water Heater Installation in {M}"],
 "Water heater replacement across Dayton and Cincinnati — tank and tankless, sized right, installed the same day in most cases."),
"/plumbing/sewer-line/overview": (["Sewer Line Services in {M}"],
 "Sewer camera inspections, spot repairs and full replacements across Dayton and Cincinnati — see the problem before you pay to fix it."),
"/plumbing/sewer-line/repair": (["Sewer Line Repair in {M}"],
 "Trenchless and open-cut sewer line repair across Dayton and Cincinnati — what each does to your yard, and when trenchless is possible."),
"/plumbing/sewer-line/cleaning": (["Sewer Line Cleaning in {M}"],
 "Sewage backing up? Main sewer line cleaning and hydro jetting across Dayton and Cincinnati, with a camera check when we're done."),
"/plumbing/sump-pump/overview": (["Sump Pump Services in {M}"],
 "Sump pumps for Dayton and Cincinnati basements — pedestal, submersible and battery backup compared, plus when yours is due to be replaced."),
"/plumbing/sump-pump/repair": (["Sump Pump Repair in {M}"],
 "Sump pump quit with the pit filling? Repair across Dayton and Cincinnati, answered 24/7 through storms and quoted before we start."),
"/plumbing/sump-pump/installation": (["Sump Pump Installation in {M}"],
 "New sump pump and battery backup installation across Dayton and Cincinnati, sized for your basement and in before the spring storms."),
"/plumbing/gas-line/overview": (["Gas Line Services in {M}"],
 "Licensed gas line installation, repair and pressure testing across Dayton and Cincinnati, with permits and code handled properly."),
"/plumbing/gas-line/repair": (["Gas Line Repair in {M}"],
 "Smell gas? Leave the building and call the gas utility first. Then call us for licensed gas line repair in Dayton and Cincinnati."),
"/plumbing/gas-line/installation": (["Gas Line Installation in {M}"],
 "Gas lines run to grills, ranges, garage heaters and fire pits across Dayton and Cincinnati — permitted, pressure tested, priced upfront."),
    # 24/7 is a verified proof point and the whole value proposition of this page, so
    # it outranks the ", OH" suffix in the metro token. A single variant keeps it.
"/plumbing/emergency-plumbing": (["24/7 Emergency Plumbers in {M}"],
 "Burst pipe, no water or a flooding basement? A real person answers 24/7 across Dayton and Cincinnati. Call " + _PHONE + "."),
"/plumbing/leak-detection": (["Leak Detection in {M}"],
 "Water bill jumped with no puddle to show for it? Non-invasive leak detection for Dayton and Cincinnati homes — slab, supply and irrigation."),
"/plumbing/water-treatment": (["Water Softeners & Filtration in {M}", "Water Softeners in {M}"],
 "Water softeners and whole-house filtration for Dayton and Cincinnati — starting with how hard your water actually is."),
"/plumbing/toilet-repair": (["Toilet Repair & Installation in {M}", "Toilet Repair in {M}"],
 "Running, leaking or clogged toilet? Toilet repair and replacement across Dayton and Cincinnati, priced upfront before we start."),
}

# The escape hatch. Per-field, keyed by route: a page can override its title and keep
# the generated description, or the reverse. Deliberately empty — the generated set
# matches the approved copy exactly today, and an override that duplicates its
# generated value is a trap for whoever changes the generator next.
OVERRIDES = {}

_NAME_OF = dict(L.ALL)
_IDX_OF = {s: i for i, (s, _) in enumerate(L.ALL)}


def _resolve_meta(url):
    """{'title','description'} for a route, generated. Raises KeyError if unknown."""
    if url.startswith("/locations/"):
        parts = url.strip("/").split("/")          # ['locations', slug, svc?]
        slug = parts[1]
        svc = parts[2] if len(parts) > 2 else ""
        city = _NAME_OF[slug]
        if svc not in CITY_TITLE:
            raise KeyError(url)
        # City pages pin the SHORT suffix on all 266 so the brand token never flips
        # between siblings under one city — an early draft gave /locations/troy the
        # full name and /locations/troy/cooling the short one. The freed characters go
        # to the keyword phrase, which is what ranks.
        title = fit_title([v.replace("{C}", city) for v in CITY_TITLE[svc]],
                          brand=BRAND[1:])
        if svc == "" and slug in CITY_DESC_OVERRIDE:
            desc = CITY_DESC_OVERRIDE[slug]
        else:
            bank = CITY_DESC[svc]
            desc = bank[_IDX_OF[slug] % len(bank)].replace("{C}", city)
    else:
        cores, desc = CORE[url]
        title = fit_title(cores)
    return {"title": title, "description": desc}


def meta_for_route(url):
    """Route in, {'title','description','url','nav','noindex'} out.

    Budgets are asserted rather than estimated: a title over 59 characters or a
    description over 155 is a build error, not a thing to notice in Search Console
    three months later.
    """
    m = _resolve_meta(url)
    if url in OVERRIDES:
        m = dict(m, **OVERRIDES[url])
    assert len(m["title"]) <= TITLE_MAX, f"{url}: title {len(m['title'])} chars"
    assert len(m["description"]) <= DESC_MAX, f"{url}: description {len(m['description'])} chars"
    m["url"] = url
    m["nav"] = "/" + url.split("/")[1] if url != "/" else ""
    m["noindex"] = noindex(url)
    return m


def meta_for(rel_path, html=None):
    """Metadata for a generated embed, by route.

    `html` is accepted and ignored. It used to be the source of the title (the page's
    own H1) and of the description (the first intro paragraph, hard-sliced at 155
    characters mid-word). Both are now authored per route above; the parameter stays
    so `build_site.py` keeps working unchanged.
    """
    return meta_for_route(route_for(rel_path))


# ============================================================ structured data
# Site-level @ids. Everything else fragment-scopes off canonical(), so no path is ever
# concatenated onto SITE_URL directly and a change in URL form stays a one-line edit in
# site_data.canonical().
SITE = D.SITE_URL
ORG_ID = canonical("/") + "#organization"
WS_ID = canonical("/") + "#website"
LOGO_ID = canonical("/") + "#logo"

# Flip to False to keep office nodes off /locations/* entirely. Leaving them on is a
# deliberate call: the node's @id is {SITE}/contact#office-beavercreek and its address
# is Beavercreek, on a page whose Service.areaServed is Xenia. It names the office that
# dispatches there; it never claims a Xenia storefront. Without it, 307 pages assert a
# LocalBusiness with no address, which is the actual misrepresentation.
OFFICE_ON_SERVICE_AREA_PAGES = True

# 4.9 across 1,595 reviews (Birdeye, client-confirmed 2026-08-02). These two numbers
# move together. A ratingValue with no count is what Google discards outright, which is
# what the previous block did on all 311 pages — the 4.9 counted for nothing.
#
# site_data carries the count twice: REVIEW_COUNT ("1,595") is the display string and
# REVIEW_COUNT_N (1595) the integer. Only the integer is valid here — "1,595" with a
# thousands separator is a parse error and takes the whole aggregateRating down with
# it — so the digits are extracted rather than trusted, whichever constant is present.
REVIEW_COUNT = re.sub(r"\D", "", str(getattr(D, "REVIEW_COUNT_N", None)
                                     or getattr(D, "REVIEW_COUNT", "1595")))
RATING_VALUE = str(D.GOOGLE_RATING).strip()
if not (REVIEW_COUNT.isdigit() and int(REVIEW_COUNT) > 0
        and re.fullmatch(r"[1-5](\.\d)?", RATING_VALUE)):
    _warn(f"aggregateRating dropped: ratingValue={RATING_VALUE!r} "
          f"reviewCount={REVIEW_COUNT!r} will not parse. Both must be bare numbers.")
    RATING_VALUE = None

# Founded 2004; the Mason office opened 2018 (client-confirmed 2026-08-02).
FOUNDING_YEAR = str(getattr(D, "FOUNDED", "2004"))

# The Organization logo must be a stable, same-origin, dark-on-light image. chrome.LOGO
# is logo-white.png — a white wordmark on transparency, which Google renders on white —
# and every jsDelivr URL is pinned to ASSET_COMMIT, so an asset push would rewrite the
# logo URL on all 311 pages and Google would re-crawl a "new" image with no history.
# /apple-touch-icon.png is 180x180, already copied same-origin by build_site.py, and
# above Google's 112x112 floor. [NEEDS: a 512x512 dark-on-light logo-schema.png.]
SCHEMA_LOGO = getattr(D, "SCHEMA_LOGO", "/apple-touch-icon.png")
SCHEMA_LOGO_W = int(getattr(D, "SCHEMA_LOGO_W", 180))
SCHEMA_LOGO_H = int(getattr(D, "SCHEMA_LOGO_H", 180))

# Social preview. Pages fall back to their own primary image, which is a real photo and
# a better card than a letterboxed logo; this is the site-level default for the handful
# of pages that render no content image.
# [NEEDS: a 1200x630 og-default.jpg. assets/brand/ has none — van.png and logo-white.png
#  are both the wrong aspect ratio.]
OG_DEFAULT = getattr(D, "OG_IMAGE", "/og-default.jpg")

# Keyed by YouTube id. A video not in this registry is NOT marked up: a VideoObject
# without uploadDate is invalid and Google drops it, and a guessed date that disagrees
# with YouTube's own is worse than no markup at all.
#
# Every value here was read off the video's own YouTube page on 2026-08-02 — title,
# uploadDate and lengthSeconds from the watch page's own metadata, not estimated. Both
# maxresdefault.jpg thumbnails were confirmed 200. If a video is re-uploaded it gets a
# new id and drops out of this table, which is the correct failure mode.
VIDEOS = getattr(D, "VIDEOS", None) or {
    "E_cZVpgYvIw": {                      # /duct-cleaning
        "name": "Extreme Heating - Duct Cleaning - How We Do It!",
        "description": ("A short walk-through of how a home's ducts get cleaned — the "
                        "process, the equipment, and why it leaves a healthier home."),
        "uploadDate": "2022-04-19T09:36:27-07:00", "duration": "PT30S",
    },
    "lUjB1pt9yBw": {                      # homepage
        "name": "Extreme Heating & Air - Serving Dayton, Cincinnati and Troy",
        "description": ("Heating, cooling and plumbing for homes across Dayton, "
                        "Cincinnati and Troy, Ohio — repairs, replacements, ductwork "
                        "and indoor air quality, from licensed and insured technicians."),
        "uploadDate": "2025-08-29T10:52:07-07:00", "duration": "PT30S",
    },
}

# Which office dispatches where; anything unlisted falls to its metro's default.
# [NEEDS: client confirmation — drawn from drive time, not the dispatch board.]
OFFICE_FOR = getattr(D, "OFFICE_FOR", None) or {
    "troy": "troy", "tipp": "troy", "vandalia": "troy", "miami-county": "troy",
    "springboro": "waynesville", "franklin": "waynesville", "lebanon": "waynesville",
    "warren-county": "waynesville",
    "butler-county": "mason", "hamilton-county": "mason",
    "montgomery-county": "beavercreek", "greene-county": "beavercreek",
    "clark-county": "beavercreek", "darke-county": "beavercreek",
    "preble-county": "beavercreek",
}
DEFAULT_OFFICE = getattr(D, "DEFAULT_OFFICE", None) or {
    "Dayton": "beavercreek", "Cincinnati": "mason", "Counties": "beavercreek"}


def _office_id(o, i=0):
    return o.get("slug") or o.get("id") or o["locality"].lower().replace(" ", "-")


# All four offices are client-confirmed (facts.md, 2026-08-02), including Troy's street
# address — which supersedes the UNCONFIRMED marking in local-seo.md 3. Offices are
# still gated on a `confirmed` flag if site_data grows one, so a disputed address drops
# out of the graph rather than being guessed at.
_OFFICES = [dict(o, id=_office_id(o, i), hq=o.get("primary", o.get("hq", i == 0)),
                 confirmed=o.get("confirmed", True))
            for i, o in enumerate(D.OFFICES)]
OFFICE_IDS_LIVE = tuple(getattr(D, "OFFICE_IDS_LIVE", None)
                        or [o["id"] for o in _OFFICES])

# An office node's `url` has to be a page that exists. site_data gives each office a
# `page` of /locations/<slug>, but Waynesville has no entry in locations.ALL and so has
# no page — an office with no location page is a local-SEO hole in its own right.
_OFFICE_PAGES = {o["id"]: (o["page"] if str(o.get("page") or "").rsplit("/", 1)[-1]
                           in _CITY_SLUGS else None) for o in _OFFICES}
for _oid, _p in _OFFICE_PAGES.items():
    if _p is None:
        _warn(f"office '{_oid}' has no /locations/{_oid} page — its LocalBusiness node "
              "points at /contact instead. An office city with no location page is a "
              "gap independent of schema.")


def offices(ids=None):
    live = [o for o in _OFFICES if o["id"] in OFFICE_IDS_LIVE and o["confirmed"]]
    return [o for o in live if ids is None or o["id"] in ids]


def hq():
    return ([o for o in offices() if o["hq"]] or offices())[:1]


# --- text and output --------------------------------------------------------
def _t(s):
    """Copy authored for HTML -> a plain string fit for JSON.

    site_data and every page string carry HTML entities because they are written for
    HTML. Inside <script type="application/ld+json"> nothing is entity-decoded, so
    "Extreme Heating &amp; Cooling LLC" would reach Google with the literal five
    characters "&amp;" sitting in the middle of the company name.
    """
    if not s:
        return None
    s = re.sub(r"<[^>]+>", " ", str(s))
    s = _html.unescape(s)
    return re.sub(r"\s+", " ", s).strip() or None


def _prune(o):
    """Drop empty branches. json.dumps writes None as null, and a null value reads as
    'Invalid value' in the validator rather than as an omission."""
    if isinstance(o, dict):
        return {k: _prune(v) for k, v in o.items() if v not in (None, "", [], {})}
    if isinstance(o, list):
        return [_prune(v) for v in o if v not in (None, "", [], {})]
    return o


def _dump(graph):
    body = json.dumps({"@context": "https://schema.org", "@graph": _prune(graph)},
                      separators=(",", ":"), ensure_ascii=False)
    # json.dumps does not escape < > &. One "</script>" inside any description would
    # terminate the script element early and void the entire block.
    body = body.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    return '<script type="application/ld+json">' + body + "</script>"


# --- extractors: everything below is read out of the rendered page ----------
_CRUMBS = re.compile(r'<div class="xsp-crumbs"[^>]*>(.*?)</div>', re.S)
_CRUMB_I = re.compile(r'<a href="([^"]*)"[^>]*>(.*?)</a>|<span class="cur"[^>]*>(.*?)</span>', re.S)
_QA = re.compile(r'<div class="xsp-qa[^"]*">\s*<button[^>]*>\s*<span>(.*?)</span>'
                 r'\s*<span class="tog".*?</button>\s*<div class="a">(.*?)</div>\s*</div>', re.S)
_DETAILS = re.compile(r'<details[^>]*><summary[^>]*>(.*?)</summary><p>(.*?)</p></details>', re.S)
_YT = re.compile(r'youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})[^"]*"\s+title="([^"]*)"')
_IMG = re.compile(r'<img[^>]+src="([^"]+)"[^>]*\salt="([^"]+)"')
_ANSWER = re.compile(r'class="[^"]*\bxsp-answer\b|id="answer"')


def read_crumbs(html_):
    """[(name, absolute_url_or_None)] straight off the rendered trail, so schema and
    visible text match by construction. The site-wide separators live in
    <span class="sep"> and never reach a name."""
    m = _CRUMBS.search(html_)
    if not m:
        return []
    out = []
    for href, label, cur in _CRUMB_I.findall(m.group(1)):
        name = _t(label or cur)
        if name:
            out.append((name, canonical(href) if href else None))
    return out


def read_faq(html_):
    pairs = _QA.findall(html_) or _DETAILS.findall(html_)
    return [(_t(q), _t(a)) for q, a in pairs if _t(q) and _t(a)]


def read_video(html_):
    m = _YT.search(html_)
    return (m.group(1), _t(m.group(2))) if m else (None, None)


def read_image(html_):
    """First content image. Decorative marks all carry alt="" and are skipped by
    construction, so this needs no allow-list to maintain."""
    m = _IMG.search(html_)
    return (m.group(1), _t(m.group(2))) if m else (None, None)


# --- dateModified -----------------------------------------------------------
# Never the build timestamp. build_site.py rewrites all 311 pages on every run, so a
# build-time date tells Google 311 pages changed when one did — and a site that claims
# that every day is a site whose dates get discounted entirely. Hash the content
# instead and only move the date when the hash moves.
_DATES_PATH = os.path.join(HERE, "content_dates.json")
_dates = None
_dates_dirty = [False]

# The jsDelivr commit pin changes on every asset push and appears in ~30 image URLs per
# page. Normalising it out means a photo upload does not restamp 311 content dates.
_ASSET_PIN = re.compile(r"@[0-9a-f]{40}/")


def _load_dates():
    global _dates
    if _dates is None:
        try:
            with open(_DATES_PATH, encoding="utf-8") as f:
                _dates = json.load(f)
        except (OSError, ValueError):
            _dates = {}
    return _dates


def flush_dates():
    """Write the ledger back. Registered with atexit so it does not depend on a call
    site in build_site.py. Commit content_dates.json — an uncommitted ledger restamps
    every page as modified today on the next machine that builds."""
    if not _dates_dirty[0]:
        return
    try:
        with open(_DATES_PATH, "w", encoding="utf-8") as f:
            json.dump(_load_dates(), f, indent=1, sort_keys=True)
        _dates_dirty[0] = False
    except OSError as e:
        _warn(f"could not write {_DATES_PATH}: {e}")


atexit.register(flush_dates)


_UPDATED = re.compile(r'<p class="xsp-updated"[^>]*>.*?<time datetime="([^"]+)"', re.S)


def content_dates(url, body_html, page=None):
    """(datePublished, dateModified).

    dateModified resolves in three steps, in this order:

      1. The date in the page's own visible "Last updated" line, read back out of the
         rendered `<p class="xsp-updated"><time datetime="…">`. geo-contract 8.2 is
         non-negotiable that the visible date and the schema date must be the same
         date, and reading the rendered one is the only way that cannot drift.
      2. `page["updatedISO"]` — the same value template.py was handed, for a page that
         supplies the key without rendering the line.
      3. The content-fingerprint ledger below, which is geo-contract 8.2's own primary
         recommendation.

    What it is never is the build clock. build_site.py rewrites all 311 pages on every
    run, so a build-time date claims 311 pages changed when one did, and a site that
    claims that every day is a site whose dates get discounted entirely.

    datePublished has no rendered counterpart and is owned here: written once, on a
    route's first appearance, and never moved after.
    """
    digest = hashlib.sha1(
        _ASSET_PIN.sub("@ASSET/", body_html).encode("utf-8")).hexdigest()[:16]
    visible = _UPDATED.search(body_html)
    stated = (visible.group(1) if visible
              else (page or {}).get("updatedISO") or None)
    d = _load_dates()
    today = _dt.date.today().isoformat()
    rec = d.get(url)
    if rec is None:
        rec = d[url] = {"hash": digest, "published": today, "modified": today}
        _dates_dirty[0] = True
    elif rec.get("hash") != digest:
        rec["hash"] = digest
        rec["modified"] = today
        _dates_dirty[0] = True
    published, modified = rec.get("published", rec["modified"]), rec["modified"]
    if stated:
        modified = stated
        # dateModified must never precede datePublished. If the page states a date
        # earlier than the ledger's first sighting, the stated one is the truth about
        # the content and the ledger entry is just when this builder first saw it.
        published = min(published, stated[:10])
    return published, modified


# --- places -----------------------------------------------------------------
STATE = {"@type": "State", "name": "Ohio"}
_GROUP_OF = {s: g for g, items in L.GROUPS for s, _ in items}


def place(slug, name):
    kind = "AdministrativeArea" if slug in _COUNTY_SLUGS else "City"
    return {"@type": kind, "name": name, "containedInPlace": STATE}


COUNTIES_SERVED = [place(s, n) for s, n in L.COUNTIES]


def office_id_for(slug):
    return OFFICE_FOR.get(slug) or DEFAULT_OFFICE.get(_GROUP_OF.get(slug), "beavercreek")


# --- page typing ------------------------------------------------------------
SERVICE_PARENT = {}          # child route -> parent route
for _label, _desc, _href, _chips in D.HVAC_CORE + D.PLUMB_CORE:
    for _cl, _cu in _chips:
        if _cu != _href:
            SERVICE_PARENT[_cu] = _href

COMPANY_ROUTES = {"/about", "/contact", "/financing-options", "/specials", "/referral"}
LEGAL_ROUTES = {"/terms", "/privacy"}
WEBPAGE_TYPE = {"service-hub": "CollectionPage", "locations-hub": "CollectionPage",
                "/about": "AboutPage", "/contact": "ContactPage"}


def page_type(url):
    if url == "/":
        return "home"
    if url in ("/services", "/plumbing/services"):
        return "service-hub"
    if url == "/locations":
        return "locations-hub"
    if url.startswith("/locations/"):
        return "location-service" if url.count("/") == 3 else "location-overview"
    if url in LEGAL_ROUTES:
        return "legal"
    if url in COMPANY_ROUTES:
        return "company"
    if url in SERVICE_PARENT:
        return "service-sub"
    return "service-detail"


# --- nodes ------------------------------------------------------------------
WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
ALLWEEK = WEEK + ["Saturday", "Sunday"]

KNOWS_ABOUT = ["Air conditioning repair", "Air conditioning installation",
               "Furnace repair", "Furnace installation", "Heat pump repair",
               "Heat pump installation", "Air duct cleaning", "Indoor air quality",
               "Thermostat installation", "Whole-home humidifiers",
               "Water heater repair", "Water heater installation", "Drain cleaning",
               "Sewer line repair", "Sump pumps", "Gas line installation",
               "Leak detection", "Water treatment", "Emergency plumbing"]

ORG_DESCRIPTION = ("Locally owned heating, cooling and plumbing contractor serving the "
                   "Dayton and Cincinnati, Ohio metros. Founded in 2004, 25,000+ jobs "
                   "completed, about 90% of service calls handled the same day, and "
                   "24/7 emergency service.")


def _staffed(spec=None):
    # ISO 8601 24-hour. The D.HOURS_STAFFED display string ("Monday – Friday, 8:00 AM –
    # 5:00 PM", en dash and all) is silently ignored by every parser — build the array.
    spec = spec or getattr(D, "HOURS_SPEC", None) or {
        "dayOfWeek": list(WEEK), "opens": "08:00", "closes": "17:00"}
    return dict({"@type": "OpeningHoursSpecification"}, **spec)


def _emergency_cp():
    # 24/7 emergency cover is a contact channel, not office hours. Modelling it as
    # openingHoursSpecification puts "Open now" on a closed office at 2am and
    # contradicts the staffed hours printed in the footer.
    return {"@type": "ContactPoint", "contactType": "emergency",
            "telephone": D.PHONE_E164, "areaServed": "US-OH",
            "availableLanguage": "English",
            "hoursAvailable": {"@type": "OpeningHoursSpecification",
                               "dayOfWeek": list(ALLWEEK),
                               "opens": "00:00", "closes": "23:59"}}


def _addr(o):
    return {"@type": "PostalAddress", "streetAddress": o["street"],
            "addressLocality": o["locality"], "addressRegion": o["region"],
            "postalCode": o["zip"], "addressCountry": "US"}


def _geo(o):
    g = o.get("geo") or ({"latitude": o["lat"], "longitude": o["lng"]}
                         if o.get("lat") and o.get("lng") else None)
    return dict({"@type": "GeoCoordinates"}, **g) if g else None


def _maps_link(o):
    """Google Maps directions link for an office, or None if site_data has no builder.
    Unescaped — an &amp; inside a JSON-LD URL is a broken URL."""
    fn = getattr(D, "maps_dir", None)
    if not callable(fn):
        return None
    return fn(f"{o['street']}, {o['locality']}, {o['region']} {o['zip']}", html=False)


def _licences():
    return [{"@type": "PropertyValue", "name": "Ohio HVAC contractor licence",
             "propertyID": "OH-HVAC", "value": D.LICENSE_HVAC.split("#")[-1]},
            {"@type": "PropertyValue", "name": "Ohio plumbing contractor licence",
             "propertyID": "OH-PLUMBING", "value": D.LICENSE_PLUMBING.split("#")[-1]}]


def n_logo():
    return {"@type": "ImageObject", "@id": LOGO_ID,
            "url": canonical(SCHEMA_LOGO), "contentUrl": canonical(SCHEMA_LOGO),
            "width": SCHEMA_LOGO_W, "height": SCHEMA_LOGO_H, "caption": _t(D.COMPANY)}


def xplan_offers():
    # Annual and monthly only. D.XPLAN["detail"] carries the member service-call rates
    # and is never read here: those rates are publishable in a benefit list, but a
    # price in an Offer is a headline claim about what the company charges.
    def offer(kind, amount, unit):
        return {"@type": "Offer", "@id": canonical("/maintenance") + f"#xplan-{kind}",
                "name": f"X-Plan Membership — {kind}",
                "price": amount, "priceCurrency": "USD",
                "url": canonical("/maintenance"),
                "availability": "https://schema.org/InStock",
                "itemOffered": {"@id": canonical("/maintenance") + "#xplan"},
                "priceSpecification": {
                    "@type": "UnitPriceSpecification", "price": amount,
                    "priceCurrency": "USD",
                    "referenceQuantity": {"@type": "QuantitativeValue",
                                          "value": 1, "unitCode": unit}}}
    return [offer("annual", D.XPLAN["annual"].lstrip("$"), "ANN"),
            offer("monthly", D.XPLAN["monthly"].lstrip("$"), "MON")]


def n_org(rating=True, offers_=True):
    node = {
        "@type": "Organization", "@id": ORG_ID, "name": _t(D.COMPANY),
        # The "&" variant never appears in rendered copy; it exists in the wild and is
        # recorded here so the entity resolves rather than splitting in two.
        "alternateName": "Extreme Heating, Air & Plumbing",
        "legalName": _t(D.ENTITY_HVAC),
        "url": canonical("/"), "slogan": _t(D.TAGLINE),
        "description": ORG_DESCRIPTION,
        "foundingDate": FOUNDING_YEAR,
        "telephone": D.PHONE_E164, "email": D.EMAIL,
        # Both point at the ImageObject sitting at the top of the graph rather than
        # inlining it here, so the logo is one node with one @id, not two copies that
        # can drift.
        "logo": {"@id": LOGO_ID}, "image": {"@id": LOGO_ID},
        "address": _addr(hq()[0]) if hq() else None,
        # D.SAME_AS is the deliberately curated list — the profiles the company
        # controls — kept separate from D.SOCIAL so a future footer-only link cannot
        # leak into the graph. It includes the Google Business Profile short link,
        # which stays on the Organization rather than being assigned to one of four
        # offices on a guess.
        "sameAs": list(getattr(D, "SAME_AS", None)
                       or [u for _n, u in D.SOCIAL]),
        "areaServed": COUNTIES_SERVED,
        "identifier": _licences(),
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "customer service",
             "telephone": D.PHONE_E164, "email": D.EMAIL, "areaServed": "US-OH",
             "availableLanguage": "English", "hoursAvailable": _staffed()},
            _emergency_cp()],
        "knowsAbout": list(KNOWS_ABOUT),
    }
    if rating and RATING_VALUE:
        # ratingValue with no count is what Google discards outright. Both numbers are
        # bare, and worstRating is stated rather than left to the 1-5 default.
        node["aggregateRating"] = {
            "@type": "AggregateRating", "ratingValue": RATING_VALUE,
            "reviewCount": REVIEW_COUNT, "bestRating": "5", "worstRating": "1"}
    if offers_:
        node["makesOffer"] = xplan_offers()
    return node


def n_website():
    # No SearchAction: there is no site search, and a target template that 404s is a
    # fabricated capability that Google drops anyway.
    return {"@type": "WebSite", "@id": WS_ID, "url": canonical("/"),
            "name": _t(D.COMPANY), "publisher": {"@id": ORG_ID},
            "inLanguage": "en-US"}


def n_office(o, area=None):
    # @type is an array: HVACBusiness alone under-describes a company holding an Ohio
    # plumbing licence, both are LocalBusiness subtypes, and it is a real signal on
    # plumbing queries. No aggregateRating here — four offices x 1,595 asserts 6,380
    # reviews. The rating belongs once, on #organization.
    return {
        "@type": ["HVACBusiness", "Plumber"],
        "@id": canonical("/contact") + f"#office-{o['id']}",
        # site_data's per-office `name` is the canonical company name plus a branch
        # city, which keeps the four nodes distinguishable without introducing a name
        # variant. [NEEDS: the listing string exactly as the Google Business Profile
        # shows it — a name that differs from GBP by one character is a NAP mismatch,
        # and GBP wins if the two disagree.]
        "name": _t(o.get("gbpName") or o.get("name") or D.COMPANY),
        "branchCode": o["id"],
        "parentOrganization": {"@id": ORG_ID},
        "url": canonical(_OFFICE_PAGES.get(o["id"]) or "/contact"),
        "telephone": D.PHONE_E164, "email": D.EMAIL,
        "image": {"@id": LOGO_ID},
        "address": _addr(o),
        # [NEEDS: lat/lng from the GBP map pin. Do not geocode — a rooftop guess that
        #  lands 40m off contradicts the pin Google already trusts.] site_data carries
        # `geo` as None for all four, and None is pruned rather than substituted.
        "geo": _geo(o),
        # A directions link built from the confirmed street address: derived, not
        # guessed, and raw rather than HTML-escaped, because an &amp; inside a JSON-LD
        # URL is a broken URL. sameAs stays empty until per-office Google Business
        # Profile URLs arrive — a directions link is a map, not a profile.
        "hasMap": o.get("gbp") or o.get("hasMap") or _maps_link(o),
        "sameAs": [o["gbp"]] if o.get("gbp") else None,
        "openingHoursSpecification": [_staffed(o.get("hoursSpec"))],
        "contactPoint": _emergency_cp(),
        "areaServed": area if area is not None else [
            place(s, n) for s, n in L.ALL if office_id_for(s) == o["id"]],
        "identifier": _licences(),
    }


def n_webpage(page, body_html, faq, about=None, speakable=False):
    url = page["url"]
    can = canonical(url)
    base = WEBPAGE_TYPE.get(url) or WEBPAGE_TYPE.get(page_type(url), "WebPage")
    # An FAQ page gets ["WebPage","FAQPage"] on this same node rather than a second
    # node: one URL, one page entity.
    types = [base, "FAQPage"] if faq else base
    published, modified = content_dates(url, body_html, page)
    node = {
        "@type": types, "@id": can + "#webpage", "url": can,
        "name": _t(page["title"]), "description": _t(page["description"]),
        "isPartOf": {"@id": WS_ID}, "inLanguage": "en-US",
        "datePublished": published, "dateModified": modified,
    }
    if about:
        node["about"] = {"@id": about}
    if read_crumbs(body_html):
        node["breadcrumb"] = {"@id": can + "#breadcrumb"}
    if read_image(body_html)[0]:
        node["primaryImageOfPage"] = {"@id": can + "#primaryimage"}
    if speakable:
        # Emitted only where the page actually renders an answer-first block, so the
        # selector can never point at markup that is not there. Speakable has never
        # produced a visible rich result; it is a cheap assistant-layer hint and the
        # last 2% of the schema budget, not the first.
        node["speakable"] = {"@type": "SpeakableSpecification",
                             "cssSelector": ["h1", ".xsp-answer"]}
    if faq:
        node["mainEntity"] = [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    return node


def n_breadcrumb(can, trail):
    items = []
    for i, (name, url) in enumerate(trail, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        # `item` is absolute — a relative item is an error in Rich Results Test. The
        # final crumb renders as <span class="cur"> with no href, and omitting `item`
        # on the last element is explicitly allowed.
        if url and i < len(trail):
            it["item"] = url
        items.append(it)
    return {"@type": "BreadcrumbList", "@id": can + "#breadcrumb",
            "itemListElement": items}


def n_service(can, name, area, category, parent=None, desc=None):
    # No Offer here. An Offer needs price + priceCurrency, and repair and installation
    # pricing is not published. X-Plan is the one priceable item on the site.
    return {
        "@type": "Service", "@id": can + "#service",
        "name": name, "serviceType": name, "description": desc,
        "provider": {"@id": ORG_ID}, "url": can,
        "mainEntityOfPage": {"@id": can + "#webpage"},
        "category": category, "areaServed": area,
        "availableChannel": {
            "@type": "ServiceChannel",
            "servicePhone": {"@type": "ContactPoint", "telephone": D.PHONE_E164},
            "serviceUrl": canonical("/contact"), "availableLanguage": "English"},
        "isRelatedTo": {"@id": canonical(parent) + "#service"} if parent else None,
    }


def n_video(can, vid, title):
    v = VIDEOS.get(vid)
    if not v or not v.get("uploadDate"):
        _warn(f"video {vid}: no uploadDate in shell.VIDEOS — VideoObject omitted on "
              f"{can}. An undated VideoObject is invalid and Google drops it; supply "
              f"uploadDate and duration from YouTube Studio.")
        return None
    return {"@type": "VideoObject", "@id": f"{can}#video-{vid}",
            "name": _t(v.get("name") or title),
            "description": _t(v.get("description")),
            # hqdefault always exists; maxresdefault only above a source resolution, so
            # confirm it returns 200 before trusting it as the first entry.
            "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg",
                             f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
            "uploadDate": v["uploadDate"], "duration": v.get("duration"),
            # embedUrl only. contentUrl should point at a media file, and the watch page
            # is a document.
            "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "publisher": {"@id": ORG_ID},
            "mainEntityOfPage": {"@id": can + "#webpage"},
            "inLanguage": "en-US"}


def n_image(can, src, alt):
    return {"@type": "ImageObject", "@id": can + "#primaryimage",
            "url": src, "contentUrl": src, "caption": alt,
            "representativeOfPage": True}


def n_itemlist(can, name, rows, category="HVAC"):
    # Noindexed routes never enter a list: asking Google to crawl what you told it to
    # ignore is how a deliberate decision reads as a bug.
    rows = [(lbl, href) for lbl, href in rows if not noindex(href)]
    if not rows:
        return None
    return {"@type": "ItemList", "@id": can + "#list", "name": name,
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": lbl,
                 "item": {"@type": "Service", "@id": canonical(href) + "#service",
                          "name": lbl, "url": canonical(href),
                          "category": category, "provider": {"@id": ORG_ID}}}
                for i, (lbl, href) in enumerate(rows, 1)]}


def n_xplan_service():
    # The accrual sentence is used verbatim from D.XPLAN["zeroRisk"], which carries
    # both required conditions — consecutive years AND capped at $2,500 or 10 years.
    # Never truncate it to fit; drop it entirely rather than state half of it.
    accrual = _t(D.XPLAN["zeroRisk"])
    if accrual and not ("consecutive" in accrual and "$2,500" in accrual):
        _warn("XPLAN['zeroRisk'] no longer states both accrual conditions "
              "(consecutive years AND $2,500/10 years) — dropped from schema.")
        accrual = None
    return {"@type": "Service", "@id": canonical("/maintenance") + "#xplan",
            "name": "X-Plan Membership", "serviceType": "HVAC maintenance plan",
            "provider": {"@id": ORG_ID}, "url": canonical("/maintenance"),
            "description": accrual,
            "hasOfferCatalog": {
                "@type": "OfferCatalog", "name": "What X-Plan includes",
                "itemListElement": [
                    {"@type": "Offer",
                     "itemOffered": {"@type": "Service", "name": _t(x)}}
                    for x in D.XPLAN["includes"]]}}


def jsonld(page, body_html):
    """One <script type="application/ld+json"> carrying one @graph, for any page."""
    url = page["url"]
    pt = page_type(url)
    can = canonical(url)
    trail = read_crumbs(body_html)
    faq = read_faq(body_html)
    img_src, img_alt = read_image(body_html)
    vid, vtitle = read_video(body_html)
    speakable = bool(_ANSWER.search(body_html))
    # makesOffer points itemOffered at {SITE}/maintenance#xplan, and that node is only
    # emitted on the maintenance pages. Carrying the offers everywhere would leave a
    # dangling @id on the other 272 pages; carrying the X-Plan catalog everywhere would
    # add ~600 bytes to each. Google consolidates #organization across the site, so the
    # offers reach the entity from the 39 pages that describe them.
    xplan = url == "/maintenance" or url.endswith("/maintenance")

    # A rating on a legal page describes nothing, and makesOffer on /terms is noise.
    g = [n_logo(), n_org(rating=(pt != "legal"), offers_=xplan), n_website()]

    # --- which office(s) --------------------------------------------------
    if pt in ("home", "locations-hub") or url == "/contact":
        g += [n_office(o) for o in offices()]
    elif pt in ("location-overview", "location-service"):
        if OFFICE_ON_SERVICE_AREA_PAGES:
            slug = url.split("/")[2]
            for o in offices([office_id_for(slug)]):
                g.append(n_office(o))
    elif pt != "legal":
        g += [n_office(o) for o in hq()]

    # --- the page and its trail -------------------------------------------
    about = (can + "#service"
             if pt in ("service-detail", "service-sub",
                       "location-overview", "location-service") else ORG_ID)
    g.append(n_webpage(page, body_html, faq, about=about, speakable=speakable))
    if trail:
        g.append(n_breadcrumb(can, trail))
    if img_src:
        g.append(n_image(can, img_src, img_alt))
    if vid:
        node = n_video(can, vid, vtitle)
        if node:
            g.append(node)

    # --- what the page is about -------------------------------------------
    cat = "Plumbing" if ("/plumbing" in url or url.endswith("/plumbing")) else "HVAC"
    # The entity name comes from the breadcrumb tail, not the <h1>. The H1s are
    # marketing lines ("Smarter comfort, one tap away") and are useless as entity
    # names; the last crumb is already the clean label.
    tail = trail[-1][0] if trail else None

    if pt in ("service-detail", "service-sub"):
        g.append(n_service(can, tail or _t(page["title"]), COUNTIES_SERVED, cat,
                           SERVICE_PARENT.get(url), _t(page["description"])))
    elif pt in ("location-overview", "location-service"):
        slug = url.split("/")[2]
        city = _NAME_OF.get(slug, slug.replace("-", " ").title())
        name = (f"{tail} in {city}, OH" if pt == "location-service" and tail
                else f"Heating, cooling and plumbing in {city}, OH")
        g.append(n_service(can, name, [place(slug, city)], cat,
                           desc=_t(page["description"])))
        if pt == "location-overview":
            g.append(n_itemlist(can, f"Services in {city}, OH",
                                [(lbl, f"/locations/{slug}/{s}") for s, lbl in L.SERVICES]))
    elif pt == "service-hub":
        rows = ([(_t(t), h) for t, _d, h, _c in D.HVAC_CORE]
                + [(_t(t), h) for t, h, _p in D.HVAC_ADDITIONAL]) if url == "/services" else \
               ([(_t(t), h) for t, _d, h, _c in D.PLUMB_CORE]
                + [(_t(t), h) for t, h, _p in D.PLUMB_ADDITIONAL])
        g.append(n_itemlist(can, _t(page["title"]), rows, cat))
    elif pt == "locations-hub":
        # Only the indexed communities. The suppressed pages stay out of every list.
        g.append(n_itemlist(can, "Communities we serve",
                            [(n, f"/locations/{s}") for s, n in L.ALL
                             if s in FEATURED], "HVAC"))
    elif pt == "home":
        g.append(n_itemlist(can, "Heating, cooling and plumbing services",
                            [(_t(t), h) for t, _d, h, _c in D.HVAC_CORE + D.PLUMB_CORE]))

    if xplan:
        g.append(n_xplan_service())

    return _dump([n for n in g if n])


# ============================================================ compliance gate
# The one claim that must never ship half-stated. The accrual may only appear with BOTH
# conditions — consecutive years AND capped at $2,500 or 10 years — because a sliced
# version of that sentence becomes a dispute at the moment a customer is buying a
# system. Nothing generated here states it, so this is a tripwire rather than a filter.
# A dollar figure in a heading is only a problem when it is a fee. "$250" in the
# Extreme Rewards headline is a rebate the customer receives, and the constraint is
# about what the company charges to show up.
_HEADING_FEE = re.compile(
    r'<(h1|h2)[^>]*>(?:(?!</\1>).)*?'
    r'(?:(?:service call|dispatch|diagnostic|trip|after[- ]hours)'
    r'(?:(?!</\1>).){0,60}\$\s?\d'
    r'|\$\s?\d(?:(?!</\1>).){0,60}(?:service call|dispatch|diagnostic|trip fee))'
    r'(?:(?!</\1>).)*?</\1>', re.S | re.I)
# The accrual claim itself, not the mere mention of X-Plan. Naming the membership and
# its price is fine; promising that money comes back is the sentence with conditions.
_ACCRUAL = re.compile(r"appl(?:ied|ies)\s+toward|goes?\s+toward|credited\s+toward"
                      r"|100%\s+of\s+(?:the\s+)?(?:your\s+)?investment", re.I)


def audit(url, html):
    """Raises on the one thing that cannot be un-published by fixing it later."""
    head = html[:html.find("</head>")]
    m = re.search(r'<meta name="description" content="([^"]*)"', head)
    desc = m.group(1) if m else ""
    if _ACCRUAL.search(desc) and ("consecutive" not in desc or "$2,500" not in desc):
        raise SystemExit(f"ABORT {url}: meta description states the X-Plan accrual "
                         "without both conditions (consecutive years AND $2,500/10 years).")
    # Dispatch and service-call fees are publishable in a benefit list or a card body,
    # never in an h1, h2 or hero. Warn rather than abort: this is copy owned elsewhere.
    if _HEADING_FEE.search(html):
        _warn(f"{url}: a dollar figure appears inside an h1 or h2 — prices belong in "
              "body copy and benefit lists, not headings.")


# ============================================================ the document
def _esc(s):
    """Escape at the render boundary rather than storing entities in the data, so a
    quotation mark in a description cannot silently break the attribute it sits in."""
    return _html.escape(str(s), quote=True)


def document(page, body_html):
    """page: {url, title, description, nav?, noindex?}

    Title and description are resolved from the route table when the route is known, so
    a caller that passes a stale or H1-derived title cannot override the authored copy.
    """
    url = page["url"]
    can = canonical(url)

    try:
        authored = _resolve_meta(url)
        if url in OVERRIDES:
            authored = dict(authored, **OVERRIDES[url])
        title, desc = authored["title"], authored["description"]
    except (KeyError, ValueError):
        # An unknown route (a 404 page, a route added without its meta) keeps whatever
        # the caller supplied rather than failing the build.
        title, desc = page.get("title", D.COMPANY), page.get("description", "")
        _warn(f"{url}: no authored title/description — falling back to the caller's. "
              "Add the route to shell.CORE or shell.CITY_TITLE.")

    # noindex,follow — never bare noindex. These pages carry ~84 internal links each,
    # and the follow is how the ten indexed communities and the root service pages keep
    # receiving them. The canonical stays self-referential: cross-canonicalising to the
    # city overview would say "index that one instead" while noindex says "index none
    # of them", and Google resolves the contradiction arbitrarily.
    suppressed = page["noindex"] if "noindex" in page else noindex(url)
    robots = ('<meta name="robots" content="noindex,follow">\n' if suppressed
              else '<meta name="robots" content="index,follow,max-image-preview:large">\n')

    # Social preview: the page's own primary image beats a letterboxed logo, and it is
    # already the ImageObject in the graph. Width/height are only asserted for the
    # site-level default, whose dimensions are known.
    img_src, img_alt = read_image(body_html)
    if img_src:
        og_image = (f'<meta property="og:image" content="{_esc(img_src)}">\n'
                    f'<meta property="og:image:alt" content="{_esc(img_alt or title)}">\n')
    else:
        og_image = (f'<meta property="og:image" content="{canonical(OG_DEFAULT)}">\n'
                    '<meta property="og:image:width" content="1200">\n'
                    '<meta property="og:image:height" content="630">\n'
                    f'<meta property="og:image:alt" content="{_esc(D.COMPANY)}">\n')

    t, d = _esc(title), _esc(desc)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}<link rel="canonical" href="{can}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{_esc(_t(D.COMPANY))}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{can}">
<meta property="og:locale" content="en_US">
{og_image}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="theme-color" content="#5E2C7E">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>{BASE_CSS}{chrome.CSS}</style>
{jsonld(dict(page, title=title, description=desc), body_html)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{chrome.header(page.get("nav", ""))}
<main id="main">
{body_html}
</main>
{chrome.footer()}
{chrome.JS}
</body>
</html>
'''
    audit(url, html)
    return html
