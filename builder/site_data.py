"""Site-wide facts. One place to change a phone number, a price, or an address.

Before this file, the phone number was hardcoded in six source files and rendered on
303 pages; X-Plan pricing lived in five. That happened because the Framer components
could not import from the builder. Once everything renders from here, changing a
value is one edit.

Anything a customer could quote back at you belongs in this file, not inline in a
page. If you find yourself typing a price, a phone number or an address into a page
module, add it here instead.
"""

from urllib.parse import quote as _quote

# ---------------------------------------------------------------- identity
COMPANY = "Extreme Heating, Air, Plumbing"
COMPANY_SHORT = "Extreme"
TAGLINE = "Comfort &amp; efficiency you can trust."

# The canonical host. Verified 2026-08-02 against the live site:
#   http://extremeheating.com   308 -> https://extremeheating.com
#   https://extremeheating.com  308 -> https://www.extremeheating.com
# WWW wins. Every absolute URL on the site is built from CANONICAL_HOST.
#
# This file previously carried DOMAIN = "extremeheating.com" alongside
# SITE_URL = "https://www.extremeheating.com" with nothing saying which was the
# URL host. Whichever one a page module reached for decided whether its canonical
# pointed at a 200 or at a 308. They are now two named things with two jobs.
CANONICAL_HOST = "www.extremeheating.com"
SITE_URL = f"https://{CANONICAL_HOST}"

# The registrable domain, for the things that are NOT URLs: email addresses, the
# Google Business Profile, licence records, print. Building a URL out of this is
# the mistake this file used to invite — it is a bare domain, and a bare-domain
# canonical on 311 pages would point every one of them at a 308.
DOMAIN = "extremeheating.com"

# URL FORM: no trailing slash, except the homepage.
#
# Verified 2026-08-02: the live site serves /about at 200 and 308s /about/ to
# /about. Cloudflare Pages does the same with dir/index.html output. Keeping this
# form is what preserves parity with every currently-indexed URL and every
# backlink — do not "fix" it to trailing slashes.
#
# This is the ONE place a route becomes an absolute URL. canonical, og:url, the
# sitemap, llms.txt and the schema url all read from it, so they cannot drift
# apart, and if a host ever normalises the other way it is a single edit.
def canonical(path="/"):
    path = "/" + str(path).strip("/")
    return SITE_URL + ("/" if path == "/" else path)

def maps_dir(address, html=True):
    """A Google Maps directions link for a street address. The `dir` endpoint, not a
    name search — a search for the company name can land on the wrong pin or on a
    disambiguation list. `html=False` gives the raw URL for JSON-LD `hasMap`, where
    an escaped ampersand would be wrong."""
    amp = "&amp;" if html else "&"
    return f"https://www.google.com/maps/dir/?api=1{amp}destination={_quote(address)}"

# Two legal entities under common ownership — see pages/company/terms.html.
ENTITY_HVAC = "Extreme Heating &amp; Cooling LLC"
ENTITY_PLUMBING = "Extreme Home Services LLC"

# ---------------------------------------------------------------- contact
PHONE_DISPLAY = "(844) 584-7399"
PHONE_TEL = "tel:18445847399"
PHONE_E164 = "+18445847399"
EMAIL = "info@extremeheating.com"

# Ohio state licences. These are a trust and E-E-A-T signal and belong in the footer
# and in the LocalBusiness schema, not buried on one page. Until the About page's team
# section comes back after the photo shoot, the licences and the founding year are
# what the site's expertise signal actually rests on, so they are not decoration.
LICENSE_HVAC = "OH LIC #37179"
LICENSE_PLUMBING = "OH LIC #13557"

# Rendered form for the footer and any "licensed" claim that needs its proof point
# attached. One string so the two numbers can never be published in two orders.
LICENSES_LINE = f"HVAC {LICENSE_HVAC} &middot; Plumbing {LICENSE_PLUMBING}"

# ---------------------------------------------------------------- history
# Client-confirmed 2026-08-02. FOUNDED backs the "20+ years" proof point; MASON_OPENED
# is what makes the Cincinnati-metro presence a date rather than an assertion.
FOUNDED = 2004
MASON_OPENED = 2018

# Client-confirmed 2026-08-01. 8-5 is when the OFFICE is staffed; emergency service
# genuinely runs around the clock. Keep these two facts distinct — collapsing them is
# what previously made the hours read as a contradiction of the 24/7 claim.
HOURS_STAFFED = "Monday – Friday, 8:00 AM – 5:00 PM"
HOURS_EMERGENCY = "24/7 — every day of the year"

# The machine-readable half of HOURS_STAFFED, for openingHoursSpecification. Office
# nodes only: 24/7 emergency response is a service attribute, not premises hours, and
# claiming the building is open at 3am is the kind of thing a GBP audit catches.
HOURS_SPEC = {"dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              "opens": "08:00", "closes": "17:00"}

# ---------------------------------------------------------------- offices
# Four offices, client-confirmed 2026-08-02 — including Troy and Waynesville, which
# earlier drafts of the SEO deliverables marked UNCONFIRMED. The client confirmed both
# in writing on 2026-08-02; that supersedes the [NEEDS] flags in local-seo.md §3 and
# geo-contract.md §7.3. Do not re-suppress them.
#
# Every location routes to the same main number — the client's explicit instruction —
# so there is deliberately no per-office phone field. Do not add local DIDs here
# without the client saying so, however much a local number would help the map pack.
#
# `metro` is the marketing region and `locality` is the city in the postal address.
# They differ for Beavercreek (Dayton metro) and Mason (Cincinnati metro), and that gap
# is exactly the NAP inconsistency the /contact cards currently ship: a card headed
# "Dayton" with a Beavercreek address underneath. Head cards by `locality`; use `metro`
# in the supporting line.
#
# `geo` is None on all four on purpose. The coordinates must come from each Google
# Business Profile's own pin, not from geocoding the street address — a geocoded pin
# that disagrees with the one Google already holds is worse than no `geo` at all.
# [NEEDS: GBP pin lat/long, all four offices.] Schema emitters must skip `geo` while
# it is None rather than substituting anything.
#
# `page` is None where no location page exists yet. All four offices have one now:
# Waynesville was added to locations.py as a city page, and the footer names all four
# regardless — an office without a page renders as text rather than being dropped,
# which is what previously made the footer advertise three offices while /about,
# /contact and /locations all said four.
OFFICES = [
    {"slug": "beavercreek", "label": "Beavercreek office", "primary": True,
     "street": "712 N Fairfield Rd", "locality": "Beavercreek", "region": "OH",
     "zip": "45434", "county": "Greene", "metro": "Dayton",
     "geo": None, "page": "/locations/beavercreek"},
    {"slug": "mason", "label": "Mason office", "primary": False,
     "street": "5633 Tylersville Rd", "locality": "Mason", "region": "OH",
     "zip": "45040", "county": "Warren", "metro": "Cincinnati",
     "geo": None, "page": "/locations/mason"},
    {"slug": "troy", "label": "Troy office", "primary": False,
     "street": "2950 Stone Cir Dr", "locality": "Troy", "region": "OH",
     "zip": "45373", "county": "Miami", "metro": "Dayton",
     "geo": None, "page": "/locations/troy"},
    {"slug": "waynesville", "label": "Waynesville office", "primary": False,
     "street": "141 North St", "locality": "Waynesville", "region": "OH",
     # metro is None, not guessed. Waynesville sits between the two metros — Warren
     # County is Cincinnati's MSA, but the shop serves the Dayton side of it — and the
     # client has not said which way it is presented. A metro label is a marketing
     # decision, so it waits for the client rather than being inferred from a map.
     # [NEEDS: how Waynesville is presented — Dayton, Cincinnati, or Warren County.]
     "zip": "45068", "county": "Warren", "metro": None,
     "geo": None, "page": "/locations/waynesville"},
]

# Derived, so no page module has to rebuild an address string by hand. Every consumer
# — the /contact cards, the footer NAP, the location pages, the JSON-LD, llms.txt —
# reads one of these. That is the point: one written form, byte-for-byte, everywhere.
# A NAP audit compares the visible block against the JSON-LD on the same page, and a
# mismatch between them is machine-detectable.
#
# There is deliberately no `city` key. The old one held the metro for three offices and
# the town for the fourth, which is the ambiguity that put "Dayton" as a heading over a
# Beavercreek address on /contact. Pick `locality` or `metro` on purpose.
for _o in OFFICES:
    _o["oneline"] = f'{_o["street"]}, {_o["locality"]}, {_o["region"]} {_o["zip"]}'
    _o["citystate"] = f'{_o["locality"]}, {_o["region"]} {_o["zip"]}'
    _o["name"] = f'{COMPANY} — {_o["locality"]}'
    _o["hasMap"] = maps_dir(_o["oneline"], html=False)
    _o["directions"] = maps_dir(_o["oneline"])
    _o["hours"] = HOURS_STAFFED
    _o["hoursSpec"] = HOURS_SPEC
del _o

OFFICE_BY_SLUG = {o["slug"]: o for o in OFFICES}
OFFICE_PRIMARY = next(o for o in OFFICES if o["primary"])
assert sum(1 for o in OFFICES if o["primary"]) == 1, "exactly one primary office"

# Sitewide footer line under the primary NAP. Four full addresses on 311 pages reads as
# stuffing and muddies which office is primary; four links does the same job for the
# crawler and none of the damage.
# All four, including any without a location page — those carry href None and the
# footer renders them as plain text. Filtering them out instead left the footer
# advertising three offices while /about, /contact and /locations all said four,
# which is a NAP inconsistency a crawler and a customer both notice.
OFFICE_LINKS = [(o["locality"], o["page"]) for o in OFFICES]

SOCIAL = [
    ("Facebook", "https://www.facebook.com/ExtremeHeatingDayton"),
    ("Instagram", "https://www.instagram.com/extremeheating/"),
    ("YouTube", "https://www.youtube.com/@extremeheatingaircondition2902"),
    ("Google Reviews", "https://maps.app.goo.gl/G7H8dMEFgQLYoeoa7"),
]

# schema.org `sameAs` for the organisation node. Same URLs as the footer — profiles the
# company controls, which is what sameAs is for. Kept as a separate name so a future
# footer-only link (or a profile the company does not own) cannot leak into the graph.
SAME_AS = [u for _, u in SOCIAL]

# ---------------------------------------------------------------- proof points
# The brand rule is that a claim always travels with its proof point, so these are
# the approved wordings. Do not round or restate them.
GOOGLE_RATING = "4.9"

# 1,595 reviews, Birdeye-aggregated, client-approved for on-site display 2026-08-02.
# The count is the half that was missing: "4.9 stars" with no denominator is the shape
# of a claim, and a ratingValue with no reviewCount is an invalid AggregateRating.
#
# Because the aggregate is multi-source, describe it as "customer reviews", not "Google
# reviews" — REVIEW_SOURCE is the wording to use. Whether it belongs in JSON-LD at all
# is the schema workstream's call: self-serving LocalBusiness ratings are not eligible
# for rich results either way, and its real job is visible on-page proof next to the
# link to the Google profile in SOCIAL.
REVIEW_COUNT = "1,595"
REVIEW_COUNT_N = 1595
REVIEW_SOURCE = "customer reviews"

YEARS_LOCAL = "20+"
JOBS_COMPLETED = "25k+"
# The same number written out. "25k+" is right in a stat tile and wrong in a sentence,
# and wrong again in llms.txt, where a machine reading "25k+" may or may not parse it.
JOBS_COMPLETED_LONG = "25,000+"
SAME_DAY = "90%"

STATS = [
    (YEARS_LOCAL, "Years of service"),
    (JOBS_COMPLETED, "Jobs completed"),
    ("24/7", "Emergency service"),
    (SAME_DAY, "Same-day service"),
]

# ---------------------------------------------------------------- programs
# X-Plan pricing and member rates. Members pay DISCOUNTED service calls, never free —
# writing "$0" or "free" here would be wrong.
XPLAN = {
    "annual": "$249",
    "monthly": "$20.75",
    "monthlyNote": "per system",
    "perks": ["Priority Scheduling", "Reduced Service Fee",
              "15% Off All Repairs", "5-Year Repair Warranty"],
    "includes": [
        "Two Safety &amp; Performance Visits a Year",
        "Multi-Point Air Conditioner Tune-Up and Service",
        "Calibrate Refrigerant Charge up to 1 lb Included",
        "Heating System Safety Checkup and Service",
        "Detailed Evaluation and Efficiency Measurements",
        "Airflow Adjustments as Needed",
        "Thermostat Calibration and Configuration",
        "Professional Recommendations to Prolong Equipment Life",
    ],
    "detail": [
        "Both seasonal tune-ups included",
        "15% off repairs",
        "Priority scheduling",
        # Dispatch / service-call fees ARE publishable (client, 2026-08-02). The
        # no-advertised-rates rule covers repair and installation pricing, not these.
        # Two SEO deliverables (technical.md §7 phase 1, local-seo.md §0) call for
        # stripping this line; the client decision on 2026-08-02 supersedes both and it
        # stays. The one constraint that does apply: these numbers may appear in a
        # benefit list or a card body, never in an h1, an h2 or a hero.
        "Member service calls: $77 vs $97 · $177 vs $197 after hours",
    ],
    # Both accrual conditions have to survive any rewording: shell.n_xplan_service()
    # greps this string for "consecutive" and "$2,500" and drops the whole sentence from
    # the schema rather than publish half a promise. Keep both words literal.
    "zeroRisk": ("Stay a member in consecutive years and every dollar you have paid comes "
                 "off the cost of replacing that system at end of life, up to $2,500 or "
                 "10 years, whichever comes first."),
}

# Extreme Rewards is two numbers and nothing else.
REWARDS = {"newSystem": "$250", "everythingElse": "$100"}

LENDERS = ["GoodLeap", "Synchrony", "Wright-Patt Credit Union"]

# ---------------------------------------------------------------- navigation
# Lifted verbatim from the Framer DesktopHeader so the ported nav matches the live
# site exactly. Rows with `chips` render a sub-row of links in the mega-menu.
HVAC_CORE = [
    ("Air Conditioning", "Repair, replacement &amp; tune-ups", "/air-conditioning",
     [("Overview", "/air-conditioning"), ("Installation", "/ac-installation"),
      ("Repair", "/ac-repair")]),
    ("Furnace &amp; Heating", "Repairs, installs &amp; safety checks", "/furnace-heating",
     [("Overview", "/furnace-heating"), ("Installation", "/furnace-installation"),
      ("Repair", "/furnace-repair")]),
    ("Heat Pump", "Year-round efficiency", "/heat-pump",
     [("Overview", "/heat-pump"), ("Installation", "/heat-pump-installation"),
      ("Repair", "/heat-pump-repair")]),
    ("Duct Cleaning", "Airflow &amp; air balancing", "/duct-cleaning", []),
    ("Indoor Air Quality", "Filtration, UV &amp; humidity control", "/indoor-air-quality",
     [("Overview", "/indoor-air-quality"), ("Solutions", "/indoor-air-quality-solutions"),
      ("FAQ", "/iaq-faq")]),
]
HVAC_ADDITIONAL = [
    ("HVAC Maintenance Plans", "/maintenance", "X-PLAN"),
    ("HVAC Inspections", "/inspection", None),
    ("Thermostat Services", "/thermostat", None),
    ("Humidifier Services", "/humidifier", None),
]
PLUMB_CORE = [
    ("Clogged Drain", "Fast help for clogged &amp; slow drains", "/plumbing/clogged-drain", []),
    ("Water Heater", "Repair &amp; replacement for hot water", "/plumbing/water-heater/overview",
     [("Overview", "/plumbing/water-heater/overview"), ("Repair", "/plumbing/water-heater/repair"),
      ("Installation", "/plumbing/water-heater/installation")]),
    ("Sewer Line", "Inspection, repair &amp; cleaning", "/plumbing/sewer-line/overview",
     [("Overview", "/plumbing/sewer-line/overview"), ("Repair", "/plumbing/sewer-line/repair"),
      ("Cleaning", "/plumbing/sewer-line/cleaning")]),
    ("Sump Pump", "Protection against basement water", "/plumbing/sump-pump/overview",
     [("Overview", "/plumbing/sump-pump/overview"), ("Repair", "/plumbing/sump-pump/repair"),
      ("Installation", "/plumbing/sump-pump/installation")]),
    ("Gas Line", "Safe installation &amp; repair", "/plumbing/gas-line/overview",
     [("Overview", "/plumbing/gas-line/overview"), ("Repair", "/plumbing/gas-line/repair"),
      ("Installation", "/plumbing/gas-line/installation")]),
]
PLUMB_ADDITIONAL = [
    ("Emergency Plumbing", "/plumbing/emergency-plumbing", None),
    ("Leak Detection", "/plumbing/leak-detection", None),
    ("Water Treatment", "/plumbing/water-treatment", None),
    ("Toilet Repair", "/plumbing/toilet-repair", None),
]

# Top-level nav after the two mega-menus.
NAV_SIMPLE = [("Locations", "/locations"), ("Specials", "/specials"), ("About", "/about")]

FOOTER_COLUMNS = [
    ("HEATING &amp; AIR", [
        ("Cooling", "/air-conditioning"), ("Heating", "/furnace-heating"),
        ("Heat Pumps", "/heat-pump"), ("Duct Cleaning", "/duct-cleaning"),
        ("Indoor Air Quality", "/indoor-air-quality"), ("Maintenance Plans", "/maintenance")]),
    ("PLUMBING", [
        ("Drain Cleaning", "/plumbing/clogged-drain"),
        ("Water Heaters", "/plumbing/water-heater/overview"),
        ("Sump Pumps", "/plumbing/sump-pump/overview"),
        ("Leak Detection", "/plumbing/leak-detection"),
        ("Gas Lines", "/plumbing/gas-line/overview"),
        ("Water Treatment", "/plumbing/water-treatment")]),
    ("COMPANY", [
        ("About", "/about"), ("Specials", "/specials"), ("Locations", "/locations"),
        ("Financing", "/financing-options"), ("X-Plan Membership", "/maintenance")]),
]

# ---------------------------------------------------------------- footer data
# Google reads a footer as a sitewide NAP declaration. A phone-only footer on 311 pages
# throws that away. These four values are what the footer is missing today: the primary
# street address, the email, the licence numbers, and links to the other three offices.
#
# Deliberately the PRIMARY address only, not all four — 4 addresses x 311 pages is 1,244
# address instances, which reads as stuffing and leaves no office looking primary. The
# other three are reachable as links (OFFICE_LINKS) from every page, which is the part
# that actually matters for crawl.
#
# Plain HTML, no microdata. The machine-readable copy is the JSON-LD; emitting the same
# address twice in two vocabularies on one page is how the two drift.
FOOTER_NAP = {
    "name": COMPANY,
    "street": OFFICE_PRIMARY["street"],
    "citystate": OFFICE_PRIMARY["citystate"],
    "phoneDisplay": PHONE_DISPLAY,
    "phoneHref": PHONE_TEL,
    "email": EMAIL,
    "emailHref": f"mailto:{EMAIL}",
    "hoursStaffed": "Office staffed Mon–Fri, 8–5",
    "hoursEmergency": "Emergencies 24/7",
    "officesLabel": "Offices",
    "offices": OFFICE_LINKS,
}

# The bottom bar. "Licensed &amp; insured in Ohio" is a claim; these are its proof, and
# the brand rule is that the two travel together.
FOOTER_LEGAL = f"&copy; 2026 {COMPANY}. All rights reserved. &middot; {LICENSES_LINE}"
