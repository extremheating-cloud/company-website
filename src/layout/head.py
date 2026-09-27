import atexit
import datetime as _dt
import hashlib
import html as _html
import json
import os
import re

from data import business as D
from pages.locations import cities as L
from data import tracking
from layout import header_footer
from layout import components as T

HERE = os.path.dirname(os.path.abspath(__file__))

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
/* must clear the sticky header; retune if its height changes */
[id]{scroll-margin-top:96px}
:where(a,button,input,summary):focus-visible{outline:3px solid #61BC47;outline-offset:2px}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:#5F2980;padding:12px 18px;
font-weight:800;z-index:1000;border-radius:0 0 10px 0}
.skip:focus{left:0}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;
animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
"""

def _strip_embed(html):
    # This regex must match the opening of components.script(); change the two together.
    html = re.sub(r'\n?\s*<script>\s*\(\(\) => \{\s*const root = document\.currentScript'
                  r'.*?</script>', "", html, flags=re.S)
    return html.strip()


# No trailing slash except "/": matches every indexed URL and backlink. Don't "fix" it.
def canonical(path="/"):
    fn = getattr(D, "canonical", None)
    if callable(fn):
        return fn(path)
    p = "/" + str(path).strip("/")
    return D.SITE_URL + ("/" if p == "/" else p)


def route_for(rel):
    # Only /locations/<city>/overview collapses; /plumbing/<family>/overview is the real live URL.
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


FEATURED_FALLBACK = {
    "dayton", "cincinnati",
    "beavercreek", "mason", "troy",
    "kettering", "centerville", "springboro",
    "west-chester", "middletown",
}

_CITY_SLUGS = {s for s, _ in L.ALL}
_SERVICE_SLUGS = {s for s, _ in L.SERVICES}
_COUNTY_SLUGS = {s for s, _ in L.COUNTIES}

FEATURED = set(getattr(L, "FEATURED", ()) or FEATURED_FALLBACK)

# A sitewide noindex must be impossible: the predicate is off unless FEATURED is a sane subset.
NOINDEX_ENABLED = bool(FEATURED) and FEATURED <= _CITY_SLUGS and 5 <= len(FEATURED) <= 20
if not NOINDEX_ENABLED:
    _warn("head.FEATURED is not a sane subset of cities.ALL "
          f"({sorted(FEATURED - _CITY_SLUGS)[:5]}) — noindex() is disabled and every "
          "page will be indexable. Fix locations.FEATURED before shipping.")

NOINDEX_EXPECTED = (((len(_CITY_SLUGS) - len(FEATURED)) * len(_SERVICE_SLUGS))
                    + len(_COUNTY_SLUGS)) if NOINDEX_ENABLED else 0


def noindex(url):
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


TITLE_MAX, DESC_MAX = 59, 155

BRAND = [D.COMPANY, D.COMPANY_SHORT]
METRO = ["Dayton & Cincinnati, OH", "Dayton & Cincinnati", "Dayton, OH"]

_PHONE = D.PHONE_DISPLAY


def fit_title(cores, brand=None):
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


CITY_TITLE = {
    "": ["HVAC & Plumbing in {C}, OH", "HVAC in {C}, OH"],
    "heating": ["Furnace Repair & Heating in {C}, OH", "Furnace Repair in {C}, OH"],
    "cooling": ["AC Repair & Installation in {C}, OH", "AC Repair in {C}, OH"],
    "maintenance": ["HVAC Tune-Ups & Maintenance in {C}, OH", "HVAC Maintenance in {C}, OH"],
    "duct-cleaning": ["Air Duct Cleaning in {C}, OH"],
    "indoor-air-quality": ["Indoor Air Quality in {C}, OH"],
    "plumbing": ["Plumbers in {C}, OH"],
}

CITY_DESC = {
"": [
 "Furnace, AC and plumbing in {C}, OH. You get a flat price before we start, and an emergency line answered at 2am. Call " + _PHONE + ".",
 "Heating, cooling or plumbing trouble in {C}, OH? Licensed, insured, local, and most calls get handled the same day. Call " + _PHONE + ".",
 "Over 20 years keeping {C}, OH homes warm, cool and running. Flat pricing, licensed techs, and the invoice matches. Call " + _PHONE + ".",
 "Repairs, replacements and tune-ups for {C}, OH homes. You'll know the price before we start. Most calls are same day. Call " + _PHONE + ".",
],
"heating": [
 "No heat in {C}, OH? We repair every furnace brand and age, quoted flat before we start, and the line is answered 24/7. Call " + _PHONE + ".",
 "Furnace repair and replacement in {C}, OH. We'll tell you what's wrong, what it costs, and whether it's worth fixing. Call " + _PHONE + ".",
 "Furnace out in {C}, OH? Licensed techs, a flat price up front, and most repairs finished the same day. Call " + _PHONE + ".",
 "Heating repair and furnace installs in {C}, OH. Every make and model, priced before we start, emergencies 24/7. Call " + _PHONE + ".",
],
"cooling": [
 "AC out in {C}, OH? We repair every make and model, most of them the same day, at a flat price you approve first. Call " + _PHONE + ".",
 "Air conditioner not cooling in {C}, OH? Repairs, replacements and tune-ups, quoted flat before we touch anything. Call " + _PHONE + ".",
 "AC repair and replacement for {C}, OH homes. Licensed, insured techs and a price you hear before the work starts. Call " + _PHONE + ".",
 "Cooling repair and new AC installs in {C}, OH. We size the system to your house and price it up front. Call " + _PHONE + ".",
],
"maintenance": [
 "Furnace and AC tune-ups in {C}, OH: two visits a year, a written report each time. X-Plan runs $20.75 a month. Call " + _PHONE + ".",
 "Keep your {C}, OH furnace and AC under warranty with seasonal checks, documented the way manufacturers ask for. Call " + _PHONE + ".",
 "Tune-ups for {C}, OH homes that are actually tune-ups, not a once-over. X-Plan is $249 a year or $20.75 a month. Call " + _PHONE + ".",
 "Spring for the AC, fall for the furnace. Book both {C}, OH visits yourself, or let X-Plan schedule them for you. Call " + _PHONE + ".",
],
"duct-cleaning": [
 "Duct cleaning in {C}, OH with negative-pressure equipment, dryer vents included, and photos before and after. Call " + _PHONE + ".",
 "We put a camera in your {C}, OH ducts first and show you what's in there. If they don't need cleaning, we'll say so. Call " + _PHONE + ".",
 "Whole-home duct cleaning for {C}, OH: every supply and return run, the registers, the blower, the dryer vent. Call " + _PHONE + ".",
 "Dust settling straight back onto your {C}, OH furniture? We clean the whole system and show you the difference. Call " + _PHONE + ".",
],
"indoor-air-quality": [
 "Filtration, UV purification, humidifiers and ventilation in {C}, OH. We test your air before we recommend anything. Call " + _PHONE + ".",
 "Air purifiers, whole-home filters and humidity control in {C}, OH. We measure your air first and tell you what it needs. Call " + _PHONE + ".",
 "Allergies worse inside your {C}, OH house than out? Whole-home filtration, purifiers and humidity control, fitted right. Call " + _PHONE + ".",
 "Not sure what you're breathing at home in {C}, OH? We'll test it, tell you straight, and only fit what helps. Call " + _PHONE + ".",
],
"plumbing": [
 "Plumbers in {C}, OH for water heaters, drains, leaks and sump pumps. Licensed, insured, and you hear the price first. Call " + _PHONE + ".",
 "The same team you'd call for the furnace, now for the pipes in {C}, OH. Most water heater swaps are same day. Call " + _PHONE + ".",
 "Drain cleaning, water heaters and leak repair in {C}, OH. Licensed plumbers, flat quotes, and an overnight line. Call " + _PHONE + ".",
 "Need a plumber in {C}, OH? Water heaters, clogged drains, sump pumps and sewer lines, all priced before we start. Call " + _PHONE + ".",
],
}

CITY_DESC_OVERRIDE = {
 "dayton": "We've kept Dayton, OH homes warm, cool and dry for over 20 years. Heating, cooling and plumbing, with the phone answered at 2am.",
 "cincinnati": "Heating, cooling and plumbing across Cincinnati, OH, run out of our Mason office. Most calls get handled the same day.",
 "beavercreek": "You'll find us at 712 N Fairfield Rd, so we're close by. Furnace, AC and plumbing for Beavercreek, OH, answered 24/7.",
 "mason": "You'll find us at 5633 Tylersville Rd. Heating, cooling and plumbing for Mason, OH and the rest of the Cincinnati metro.",
 "kettering": "Furnace, AC and plumbing for Kettering, OH, run out of our Beavercreek office nearby. You hear the price before we start.",
 "centerville": "HVAC and plumbing for Centerville, OH homes. Locally owned for over 20 years, and you hear the price before we start.",
 "huber": "Heating, cooling and plumbing for Huber Heights, OH. You get a flat price before we start, and an emergency line at 2am.",
 "west-chester": "HVAC and plumbing for West Chester, OH, run out of our Mason office. Flat pricing up front and a 24/7 emergency line.",
 "fairborn": "Furnace, AC and plumbing for Fairborn, OH, run out of our Beavercreek office. Emergencies answered any hour, any day.",
 "springfield": "Heating, cooling and plumbing for Springfield, OH. Locally owned for over 20 years, with an emergency line answered any hour.",
}

CORE = {
"/": (["HVAC & Plumbing in {M}"],
 "Heating, cooling and plumbing for homes across Dayton and Cincinnati. Over 20 years local, most calls same day, emergencies answered 24/7."),
"/services": (["HVAC & Plumbing Services in {M}"],
 "Every heating, cooling and plumbing job we take on across Dayton and Cincinnati: repairs, replacements, tune-ups, drains and water heaters."),
"/locations": (["HVAC & Plumbing Service Area: {M}", "HVAC Service Area: {M}"],
 "38 towns across the Dayton and Cincinnati metros, one number to call. Find yours and see what we cover. Call " + _PHONE + "."),
"/specials": (["HVAC Specials & Coupons in {M}"],
 "Current offers on the heating, cooling and plumbing work you actually need. Mention the one you want when you book and we'll apply it."),
"/financing-options": (["HVAC Financing in {M}"],
 "Spread a new furnace, AC or heat pump over monthly payments through GoodLeap, Synchrony or Wright-Patt Credit Union. Estimates are free."),
"/about": (["About Extreme Heating, Air, Plumbing | Dayton, OH"],
 "A locally owned heating, cooling and plumbing team that has served Dayton and Cincinnati for over 20 years and 25,000+ jobs."),
"/contact": (["Contact Us | Extreme Heating, Air, Plumbing"],
 "Call " + _PHONE + " or book online in about a minute. Offices in Beavercreek and Mason, OH, and someone picks up at any hour."),
"/referral": (["Extreme Rewards Referral Program | Give $250, Get $250"],
 "Send us a friend: they save $250 on a new heating, cooling or plumbing system or $100 on anything else, and you get whatever they saved."),
"/terms": (["Terms of Service & Limited Warranty"],
 "The terms and limited warranty covering our estimates, invoices and work, as Extreme Heating and Cooling Ltd and Extreme Home Services LLC."),
"/privacy": (["Privacy Policy"],
 "What we collect when you book a visit, who it goes to, how long we keep it, and how to ask us to delete it. Written from what the site actually does."),

"/air-conditioning": (["Air Conditioning Services in {M}"],
 "AC repair, replacement and tune-ups across Dayton and Cincinnati. Every make and model, a flat price before we start, and a 24/7 line."),
"/furnace-heating": (["Heating & Furnace Services in {M}"],
 "Furnace repair, installation and safety checks for Dayton and Cincinnati homes. Any make, any age, priced flat before we start. 24/7."),
"/heat-pump": (["Heat Pump Services in {M}"],
 "How a heat pump holds up in a real Ohio winter, what one costs, and what we do when yours needs repairing or replacing."),
"/duct-cleaning": (["Air Duct Cleaning in {M}"],
 "Whole-home duct and dryer-vent cleaning in Dayton and Cincinnati. We show you camera photos before and after, and we won't upsell you."),
"/indoor-air-quality": (["Indoor Air Quality Services in {M}", "Indoor Air Quality in {M}"],
 "Filtration, UV purification, humidifiers and fresh-air ventilation for Dayton and Cincinnati homes. We test your air before recommending."),
"/maintenance": (["HVAC Maintenance Plans in {M}"],
 "Seasonal furnace and AC tune-ups, or let X-Plan cover both visits a year plus priority scheduling and repair discounts, for $20.75 a month."),
"/inspection": (["HVAC Inspections in {M}"],
 "A full look at the heating and cooling system before you buy a house, before winter, or when you just want a second opinion."),
"/thermostat": (["Thermostat Installation in {M}"],
 "Smart thermostat installation, setup and troubleshooting across Dayton and Cincinnati, including older houses with no C-wire in the wall."),
"/humidifier": (["Whole-House Humidifiers in {M}"],
 "A whole-house humidifier ends the static shocks, dry skin and cracking trim that Ohio winters bring. Installed and repaired, priced up front."),

"/ac-repair": (["AC Repair in {M}"],
 "AC blowing warm? We repair every make and model across Dayton and Cincinnati, most of them the same day, at a flat price quoted first."),
"/ac-installation": (["AC Installation & Replacement in {M}", "AC Installation in {M}"],
 "Replacing an air conditioner in Dayton or Cincinnati? Honest sizing, efficiency options you can compare, free estimates and monthly payments."),
"/furnace-repair": (["Furnace Repair in {M}"],
 "No heat is an emergency, so we answer at 2am. Furnace repair across Dayton and Cincinnati, any make, quoted flat before we start."),
"/furnace-installation": (["Furnace Installation & Replacement in {M}", "Furnace Installation in {M}"],
 "A new furnace for your Dayton or Cincinnati home, sized right and installed to code. Compare efficiency levels and pay monthly if you'd rather."),
"/heat-pump-repair": (["Heat Pump Repair in {M}"],
 "Heat pump not heating or cooling? We diagnose it fast, quote it flat, and tell you honestly when winter icing is nothing to worry about."),
"/heat-pump-installation": (["Heat Pump Installation in {M}"],
 "Heat pumps and dual-fuel systems for Dayton and Cincinnati homes, sized for a real Ohio winter with the backup heat set up properly."),
"/indoor-air-quality-solutions": (["Whole-House Air Purifiers in {M}"],
 "UV lights, media filters, HEPA and air scrubbers side by side: what each one removes, and which one suits your house."),
"/importance-iaq": (["Why Indoor Air Quality Matters in Your Home"],
 "The air inside your house is often dirtier than the air outside. Here's what that does to your sleep and allergies, and how to find out."),
"/iaq-faq": (["Indoor Air Quality FAQ: Filters, UV & Humidity"],
 "MERV ratings, how often to change a filter, UV lights, winter humidity, duct cleaning. Straight answers to what homeowners ask us most."),

"/plumbing/services": (["Plumbers in {M}"],
 "Licensed plumbers across Dayton and Cincinnati for water heaters, drains, leaks, sewer lines and sump pumps. You hear the price first."),
"/plumbing/clogged-drain": (["Drain Cleaning in {M}"],
 "We snake or hydro jet the drain, and if the clog keeps coming back we put a camera down there to find out why."),
"/plumbing/water-heater/overview": (["Water Heater Services in {M}"],
 "Tank, tankless or heat pump? Compare what each costs, how long it lasts and how much hot water you get, then we'll install it."),
"/plumbing/water-heater/repair": (["Water Heater Repair in {M}"],
 "No hot water? We fix leaks, pilot lights, thermostats and elements across Dayton and Cincinnati, usually the same day you call."),
"/plumbing/water-heater/installation": (["Water Heater Installation in {M}"],
 "Replacing a water heater in Dayton or Cincinnati? Tank or tankless, sized for your household and usually installed the same day."),
"/plumbing/sewer-line/overview": (["Sewer Line Services in {M}"],
 "Camera inspections, spot repairs and full sewer replacements across Dayton and Cincinnati. You see the problem before you pay to fix it."),
"/plumbing/sewer-line/repair": (["Sewer Line Repair in {M}"],
 "Trenchless or open-cut sewer repair: what each one does to your yard, when trenchless is possible, and what we'd do at your house."),
"/plumbing/sewer-line/cleaning": (["Sewer Line Cleaning in {M}"],
 "Sewage backing up? We clear and hydro jet the main line across Dayton and Cincinnati, then camera it so you can see it's clear."),
"/plumbing/sump-pump/overview": (["Sump Pump Services in {M}"],
 "Pedestal, submersible or battery backup for your basement, how to tell when yours is near the end, and what replacing it involves."),
"/plumbing/sump-pump/repair": (["Sump Pump Repair in {M}"],
 "Pump quit with the pit filling up? We answer through the storm, come out to Dayton and Cincinnati basements, and quote before we start."),
"/plumbing/sump-pump/installation": (["Sump Pump Installation in {M}"],
 "A new sump pump and battery backup, sized for your basement and in before the spring storms hit Dayton and Cincinnati."),
"/plumbing/gas-line/overview": (["Gas Line Services in {M}"],
 "Gas line installation, repair and pressure testing by licensed plumbers, with the permits and code inspections handled for you."),
"/plumbing/gas-line/repair": (["Gas Line Repair in {M}"],
 "Smell gas? Get everyone out and call the gas utility first. Then call us for licensed gas line repair in Dayton or Cincinnati."),
"/plumbing/gas-line/installation": (["Gas Line Installation in {M}"],
 "Gas run out to a grill, range, garage heater or fire pit in Dayton or Cincinnati. Permitted, pressure tested and priced before we start."),
"/plumbing/emergency-plumbing": (["24/7 Emergency Plumbers in {M}"],
 "Burst pipe, no water, basement filling up? A real person picks up at 2am, anywhere in Dayton or Cincinnati. Call " + _PHONE + "."),
"/plumbing/leak-detection": (["Leak Detection in {M}"],
 "Water bill jumped and there's no puddle to explain it? We find slab, supply and irrigation leaks without tearing your house up first."),
"/plumbing/water-treatment": (["Water Softeners & Filtration in {M}", "Water Softeners in {M}"],
 "Hard water, iron stains, bad taste? We test your water first, then fit a softener or whole-house filter that matches it."),
"/plumbing/toilet-repair": (["Toilet Repair & Installation in {M}", "Toilet Repair in {M}"],
 "Running, leaking, or clogged for the third time this month? We repair and replace toilets across Dayton and Cincinnati, priced up front."),
}

OVERRIDES = {}

_NAME_OF = dict(L.ALL)
_IDX_OF = {s: i for i, (s, _) in enumerate(L.ALL)}


def _resolve_meta(url):
    if url.startswith("/locations/"):
        parts = url.strip("/").split("/")
        slug = parts[1]
        svc = parts[2] if len(parts) > 2 else ""
        city = _NAME_OF[slug]
        if svc not in CITY_TITLE:
            raise KeyError(url)
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
    return meta_for_route(route_for(rel_path))


SITE = D.SITE_URL
ORG_ID = canonical("/") + "#organization"
WS_ID = canonical("/") + "#website"
LOGO_ID = canonical("/") + "#logo"

OFFICE_ON_SERVICE_AREA_PAGES = True

# No aggregateRating: Google's review-snippet rules exclude self-collected reviews. Don't add it back.

FOUNDING_YEAR = str(getattr(D, "FOUNDED", "2004"))

# Must be same-origin and dark-on-light; the header's white logo vanishes on Google's white.
SCHEMA_LOGO = getattr(D, "SCHEMA_LOGO", "/apple-touch-icon.png")
SCHEMA_LOGO_W = int(getattr(D, "SCHEMA_LOGO_W", 180))
SCHEMA_LOGO_H = int(getattr(D, "SCHEMA_LOGO_H", 180))

OG_DEFAULT = getattr(D, "OG_IMAGE", "/og-default.jpg")

# Values read off each video's YouTube page; never guess an uploadDate.
VIDEOS = getattr(D, "VIDEOS", None) or {
    "E_cZVpgYvIw": {
        "name": "Extreme Heating - Duct Cleaning - How We Do It!",
        "description": ("A short walk-through of how a home's ducts get cleaned — the "
                        "process, the equipment, and why it leaves a healthier home."),
        "uploadDate": "2022-04-19T09:36:27-07:00", "duration": "PT30S",
    },
    "lUjB1pt9yBw": {
        "name": "Extreme Heating & Air - Serving Dayton, Cincinnati and Troy",
        "description": ("Heating, cooling and plumbing for homes across Dayton, "
                        "Cincinnati and Troy, Ohio — repairs, replacements, ductwork "
                        "and indoor air quality, from licensed and insured technicians."),
        "uploadDate": "2025-08-29T10:52:07-07:00", "duration": "PT30S",
    },
}

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


_OFFICES = [dict(o, id=_office_id(o, i), hq=o.get("primary", o.get("hq", i == 0)),
                 confirmed=o.get("confirmed", True))
            for i, o in enumerate(D.OFFICES)]
OFFICE_IDS_LIVE = tuple(getattr(D, "OFFICE_IDS_LIVE", None)
                        or [o["id"] for o in _OFFICES])

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


def _t(s):
    # Page copy carries HTML entities, and nothing inside JSON-LD is entity-decoded.
    if not s:
        return None
    s = re.sub(r"<[^>]+>", " ", str(s))
    s = _html.unescape(s)
    return re.sub(r"\s+", " ", s).strip() or None


def _prune(o):
    if isinstance(o, dict):
        return {k: _prune(v) for k, v in o.items() if v not in (None, "", [], {})}
    if isinstance(o, list):
        return [_prune(v) for v in o if v not in (None, "", [], {})]
    return o


def _dump(graph):
    body = json.dumps({"@context": "https://schema.org", "@graph": _prune(graph)},
                      separators=(",", ":"), ensure_ascii=False)
    # json.dumps leaves < > & alone; a "</script>" in any string would end the block.
    body = body.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    return '<script type="application/ld+json">' + body + "</script>"


# These regexes parse components.py markup; change them together.
_CRUMBS = re.compile(r'<div class="xsp-crumbs"[^>]*>(.*?)</div>', re.S)
_CRUMB_I = re.compile(r'<a href="([^"]*)"[^>]*>(.*?)</a>|<span class="cur"[^>]*>(.*?)</span>', re.S)
_QA = re.compile(r'<div class="xsp-qa[^"]*">\s*<button[^>]*>\s*<span>(.*?)</span>'
                 r'\s*<span class="tog".*?</button>\s*<div class="a">(.*?)</div>\s*</div>', re.S)
_DETAILS = re.compile(r'<details[^>]*><summary[^>]*>(.*?)</summary><p>(.*?)</p></details>', re.S)
_YT = re.compile(r'youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})[^"]*"\s+title="([^"]*)"')
_IMG = re.compile(r'<img[^>]+src="([^"]+)"[^>]*\salt="([^"]+)"')
_ANSWER = re.compile(r'class="[^"]*\bxsp-answer\b|id="answer"')


def read_crumbs(html_):
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
    m = _IMG.search(html_)
    return (m.group(1), _t(m.group(2))) if m else (None, None)


# Never the build clock (every build rewrites every page): the date moves only when the content hash does.
_DATES_PATH = os.path.normpath(os.path.join(HERE, "..", "data", "content_dates.json"))
_dates = None
_dates_dirty = [False]

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
    # Commit content_dates.json, or the next machine to build restamps every page as modified today.
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
        published = min(published, stated[:10])
    return published, modified


STATE = {"@type": "State", "name": "Ohio"}
_GROUP_OF = {s: g for g, items in L.GROUPS for s, _ in items}


def place(slug, name):
    kind = "AdministrativeArea" if slug in _COUNTY_SLUGS else "City"
    return {"@type": kind, "name": name, "containedInPlace": STATE}


COUNTIES_SERVED = [place(s, n) for s, n in L.COUNTIES]


def office_id_for(slug):
    return OFFICE_FOR.get(slug) or DEFAULT_OFFICE.get(_GROUP_OF.get(slug), "beavercreek")


SERVICE_PARENT = {}
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
    # A structured spec: parsers silently ignore the D.HOURS_STAFFED display string.
    spec = spec or getattr(D, "HOURS_SPEC", None) or {
        "dayOfWeek": list(WEEK), "opens": "08:00", "closes": "17:00"}
    return dict({"@type": "OpeningHoursSpecification"}, **spec)


def _emergency_cp():
    # A contact point, not opening hours: 24/7 hours would show a closed office as "Open now".
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
    # html=False: an &amp; inside a JSON-LD URL breaks it.
    fn = getattr(D, "maps_dir", None)
    if not callable(fn):
        return None
    return fn(f"{o['street']}, {o['locality']}, {o['region']} {o['zip']}", html=False)


def _licences():
    return [{"@type": "PropertyValue", "name": "Ohio HVAC contractor license",
             "propertyID": "OH-HVAC", "value": D.LICENSE_HVAC.split("#")[-1]},
            {"@type": "PropertyValue", "name": "Ohio plumbing contractor license",
             "propertyID": "OH-PLUMBING", "value": D.LICENSE_PLUMBING.split("#")[-1]}]


def n_logo():
    return {"@type": "ImageObject", "@id": LOGO_ID,
            "url": canonical(SCHEMA_LOGO), "contentUrl": canonical(SCHEMA_LOGO),
            "width": SCHEMA_LOGO_W, "height": SCHEMA_LOGO_H, "caption": _t(D.COMPANY)}


def xplan_offers():
    # Annual and monthly only; member service-call rates never go in an Offer.
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


def n_org(offers_=True):
    node = {
        "@type": "Organization", "@id": ORG_ID, "name": _t(D.COMPANY),
        "alternateName": "Extreme Heating, Air & Plumbing",
        "legalName": _t(D.ENTITY_HVAC),
        "url": canonical("/"), "slogan": _t(D.TAGLINE),
        "description": ORG_DESCRIPTION,
        "foundingDate": FOUNDING_YEAR,
        "telephone": D.PHONE_E164, "email": D.EMAIL,
        "logo": {"@id": LOGO_ID}, "image": {"@id": LOGO_ID},
        "address": _addr(hq()[0]) if hq() else None,
        "sameAs": list(getattr(D, "SAME_AS", None)
                       or [u for _n, u in D.SOCIAL]),
        "areaServed": COUNTIES_SERVED,
        "priceRange": "$$",
        "identifier": _licences(),
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "customer service",
             "telephone": D.PHONE_E164, "email": D.EMAIL, "areaServed": "US-OH",
             "availableLanguage": "English", "hoursAvailable": _staffed()},
            _emergency_cp()],
        "knowsAbout": list(KNOWS_ABOUT),
    }
    if offers_:
        node["makesOffer"] = xplan_offers()
    return node


def n_website():
    return {"@type": "WebSite", "@id": WS_ID, "url": canonical("/"),
            "name": _t(D.COMPANY), "publisher": {"@id": ORG_ID},
            "inLanguage": "en-US"}


def n_office(o, area=None):
    return {
        "@type": ["HVACBusiness", "Plumber"],
        "@id": canonical("/contact") + f"#office-{o['id']}",
        "name": _t(o.get("gbpName") or o.get("name") or D.COMPANY),
        "branchCode": o["id"],
        "parentOrganization": {"@id": ORG_ID},
        "url": canonical(_OFFICE_PAGES.get(o["id"]) or "/contact"),
        # Each office number matches its Google Business Profile; change both together.
        "telephone": o.get("phone_e164") or D.PHONE_E164, "email": D.EMAIL,
        "image": {"@id": LOGO_ID},
        "address": _addr(o),
        # Only from the GBP map pin; never geocode.
        "geo": _geo(o),
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
        if url and i < len(trail):
            it["item"] = url
        items.append(it)
    return {"@type": "BreadcrumbList", "@id": can + "#breadcrumb",
            "itemListElement": items}


def n_service(can, name, area, category, parent=None, desc=None):
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
        _warn(f"video {vid}: no uploadDate in head.VIDEOS — VideoObject omitted on "
              f"{can}. An undated VideoObject is invalid and Google drops it; supply "
              f"uploadDate and duration from YouTube Studio.")
        return None
    return {"@type": "VideoObject", "@id": f"{can}#video-{vid}",
            "name": _t(v.get("name") or title),
            "description": _t(v.get("description")),
            "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg",
                             f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
            "uploadDate": v["uploadDate"], "duration": v.get("duration"),
            "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "publisher": {"@id": ORG_ID},
            "mainEntityOfPage": {"@id": can + "#webpage"},
            "inLanguage": "en-US"}


def abs_img(src):
    # og:image and schema image URLs must be absolute; relative ones are silently dropped.
    if not src:
        return src
    return canonical(src) if src.startswith("/") else src


def n_image(can, src, alt):
    src = abs_img(src)
    return {"@type": "ImageObject", "@id": can + "#primaryimage",
            "url": src, "contentUrl": src, "caption": alt,
            "representativeOfPage": True}


def n_itemlist(can, name, rows, category="HVAC"):
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
    # Never truncate the accrual sentence; drop it rather than state one condition.
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
    url = page["url"]
    pt = page_type(url)
    can = canonical(url)
    trail = read_crumbs(body_html)
    faq = read_faq(body_html)
    img_src, img_alt = read_image(body_html)
    vid, vtitle = read_video(body_html)
    speakable = bool(_ANSWER.search(body_html))
    # makesOffer points at #xplan, which only the maintenance pages emit.
    xplan = url == "/maintenance" or url.endswith("/maintenance")

    g = [n_logo(), n_org(offers_=xplan), n_website()]

    if pt in ("home", "locations-hub") or url == "/contact":
        g += [n_office(o) for o in offices()]
    elif pt in ("location-overview", "location-service"):
        if OFFICE_ON_SERVICE_AREA_PAGES:
            slug = url.split("/")[2]
            for o in offices([office_id_for(slug)]):
                g.append(n_office(o))
    elif pt != "legal":
        g += [n_office(o) for o in hq()]

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

    cat = "Plumbing" if ("/plumbing" in url or url.endswith("/plumbing")) else "HVAC"
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
        g.append(n_itemlist(can, "Communities we serve",
                            [(n, f"/locations/{s}") for s, n in L.ALL
                             if s in FEATURED], "HVAC"))
    elif pt == "home":
        g.append(n_itemlist(can, "Heating, cooling and plumbing services",
                            [(_t(t), h) for t, _d, h, _c in D.HVAC_CORE + D.PLUMB_CORE]))

    if xplan:
        g.append(n_xplan_service())

    return _dump([n for n in g if n])


# Compliance gate: the X-Plan accrual never ships half-stated, and fees stay out of h1/h2.
_HEADING_FEE = re.compile(
    r'<(h1|h2)[^>]*>(?:(?!</\1>).)*?'
    r'(?:(?:service call|dispatch|diagnostic|trip|after[- ]hours)'
    r'(?:(?!</\1>).){0,60}\$\s?\d'
    r'|\$\s?\d(?:(?!</\1>).){0,60}(?:service call|dispatch|diagnostic|trip fee))'
    r'(?:(?!</\1>).)*?</\1>', re.S | re.I)
_ACCRUAL = re.compile(r"appl(?:ied|ies)\s+toward|goes?\s+toward|credited\s+toward"
                      r"|100%\s+of\s+(?:the\s+)?(?:your\s+)?investment", re.I)


def audit(url, html):
    head = html[:html.find("</head>")]
    m = re.search(r'<meta name="description" content="([^"]*)"', head)
    desc = m.group(1) if m else ""
    if _ACCRUAL.search(desc) and ("consecutive" not in desc or "$2,500" not in desc):
        raise SystemExit(f"ABORT {url}: meta description states the X-Plan accrual "
                         "without both conditions (consecutive years AND $2,500/10 years).")
    if _HEADING_FEE.search(html):
        _warn(f"{url}: a dollar figure appears inside an h1 or h2 — prices belong in "
              "body copy and benefit lists, not headings.")


def _esc(s):
    return _html.escape(str(s), quote=True)


def document(page, body_html):
    url = page["url"]
    can = canonical(url)

    body_html = T.autolink_phone(body_html)

    try:
        authored = _resolve_meta(url)
        if url in OVERRIDES:
            authored = dict(authored, **OVERRIDES[url])
        title, desc = authored["title"], authored["description"]
    except (KeyError, ValueError):
        title, desc = page.get("title", D.COMPANY), page.get("description", "")
        _warn(f"{url}: no authored title/description — falling back to the caller's. "
              "Add the route to head.CORE or head.CITY_TITLE.")

    # noindex,follow, never bare noindex: these pages pass internal links. Canonical stays self-referential.
    suppressed = page["noindex"] if "noindex" in page else noindex(url)
    robots = ('<meta name="robots" content="noindex,follow">\n' if suppressed
              else '<meta name="robots" content="index,follow,max-image-preview:large">\n')

    img_src, img_alt = read_image(body_html)
    if img_src:
        og_image = (f'<meta property="og:image" content="{_esc(abs_img(img_src))}">\n'
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
<link rel="preconnect" href="https://www.googletagmanager.com">
<style>{BASE_CSS}{header_footer.CSS}</style>
{jsonld(dict(page, title=title, description=desc), body_html)}
{tracking.HEAD}
</head>
<body>
{tracking.BODY_START}
<a class="skip" href="#main">Skip to content</a>
{header_footer.header(page.get("nav", ""))}
<main id="main">
{body_html}
</main>
{header_footer.footer()}
{header_footer.JS}
</body>
</html>
'''
    audit(url, html)
    return html
