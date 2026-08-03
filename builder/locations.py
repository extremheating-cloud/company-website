"""Location pages — the /locations tree.

Data only. No renderers yet: the pages under pages/locations/ are placeholders, and
this is the list they were generated from. When the real templates are written, they
build from here so the set stays in one place instead of across 266 files.

Slugs are the live Framer URLs, which is why a couple read short: Huber Heights is
/huber and Tipp City is /tipp. Do not "fix" those without changing the routes and
adding redirects.
"""

# Each location gets an overview plus one page per service.
# TODO (client): plumbing is listed here because it is coming; the live site has
# five service pages per location today. Drop "plumbing" from SERVICES if the
# location pages ship before the plumbing line does.
SERVICES = [
    ("heating", "Heating"),
    ("cooling", "Cooling"),
    ("maintenance", "Maintenance"),
    ("duct-cleaning", "Duct Cleaning"),
    ("indoor-air-quality", "Indoor Air Quality"),
    ("plumbing", "Plumbing"),
]

# (slug, display name). Order matches the live Framer page tree.
DAYTON = [
    ("dayton", "Dayton"),
    ("beavercreek", "Beavercreek"),
    ("bellbrook", "Bellbrook"),
    ("centerville", "Centerville"),
    ("englewood", "Englewood"),
    ("fairborn", "Fairborn"),
    ("franklin", "Franklin"),
    ("huber", "Huber Heights"),
    ("kettering", "Kettering"),
    ("miamisburg", "Miamisburg"),
    ("moraine", "Moraine"),
    ("oakwood", "Oakwood"),
    ("riverside", "Riverside"),
    ("springboro", "Springboro"),
    ("tipp", "Tipp City"),
    ("springfield", "Springfield"),
    ("troy", "Troy"),
    ("vandalia", "Vandalia"),
    ("waynesville", "Waynesville"),
    ("west-carrollton", "West Carrollton"),
    ("xenia", "Xenia"),
]

CINCINNATI = [
    ("blue-ash", "Blue Ash"),
    ("cincinnati", "Cincinnati"),
    ("fairfield", "Fairfield"),
    ("sharonville", "Sharonville"),
    ("lebanon", "Lebanon"),
    ("middletown", "Middletown"),
    ("mason", "Mason"),
    ("northgate", "Northgate"),
    ("west-chester", "West Chester"),
]

COUNTIES = [
    ("butler-county", "Butler County"),
    ("montgomery-county", "Montgomery County"),
    ("miami-county", "Miami County"),
    ("clark-county", "Clark County"),
    ("greene-county", "Greene County"),
    ("hamilton-county", "Hamilton County"),
    ("preble-county", "Preble County"),
    ("darke-county", "Darke County"),
    ("warren-county", "Warren County"),
]

# metro label -> list, in the order the /locations page presents them
GROUPS = [
    ("Dayton", DAYTON),
    ("Cincinnati", CINCINNATI),
    ("Counties", COUNTIES),
]

ALL = DAYTON + CINCINNATI + COUNTIES

# ---------------------------------------------------------------- indexation
# The ten communities that carry genuinely local, indexed city+service pages.
# Everywhere else keeps its city+service pages for users and internal linking,
# noindexed rather than competing with each other on near-identical copy.
#
# Selection is metros.md §1, scored on population, market value, office proximity and
# existing rank. Two office towns anchor themselves (Beavercreek, Mason, Troy) and a
# third anchors an office with no page of its own (Springboro anchors Waynesville), so
# all four offices have an indexed page within ~12 miles.
#
# Near misses, kept noindexed and promotable later: Springfield (Clark County, ~28 mi,
# further than a same-day claim should stretch), Middletown, Fairborn, Lebanon.
# The nine COUNTIES pages stay noindexed too — a county page is always a superset of
# its city pages and is the likeliest source of duplicate-content dilution.
#
# shell.py reads this via getattr(L, "FEATURED", ()) and derives both the noindex
# predicate and the count build_site.py asserts against, so this is the only place the
# set is defined. shell.FEATURED_FALLBACK is a stale copy that only applies if this
# name disappears; it lists middletown where metros.md §1 chose huber.
#
# [NEEDS: client sign-off on this exact ten.]
FEATURED_ORDER = [
    "dayton", "cincinnati",                  # metro anchors, both already rank
    "beavercreek", "mason", "troy",          # communities with an office in them
    "kettering", "centerville", "huber",     # Montgomery County
    "springboro",                            # Warren/Montgomery, anchors Waynesville
    "west-chester",                          # Butler County, largest township in Ohio
]
FEATURED = set(FEATURED_ORDER)

_slugs = {s for s, _ in ALL}
assert FEATURED <= _slugs, f"FEATURED has slugs with no page: {FEATURED - _slugs}"
assert len(FEATURED) == 10, f"FEATURED must be exactly ten, got {len(FEATURED)}"
del _slugs

# Where the display name in ALL is a short form. Used in H1s, answer blocks and body
# copy on the indexed pages; the nav label and the card grids keep the short form.
LONG_NAME = {
    "west-chester": "West Chester Township",
    "huber": "Huber Heights",
    "tipp": "Tipp City",
}

def long_name(slug, fallback):
    return LONG_NAME.get(slug, fallback)

# Which office covers an indexed community, as (office town, street or None, distance
# phrase or None). The street is populated ONLY where the office is physically inside
# that city — Beavercreek, Mason and Troy. Every other page names its office by town
# and never by street, so 35 pages cannot dilute the three real NAP records.
#
# Distances are the approximate mileages in metros.md. Nothing here is estimated.
# [NEEDS: nearest office and approximate mileage for the 19 noindexed cities. Until
# those are supplied their copy names no office and claims no distance.]
OFFICE = {
    "dayton":       ("Beavercreek",  None,                  "about eight miles east"),
    "cincinnati":   ("Mason",        None,                  "roughly 22 miles north"),
    "beavercreek":  ("Beavercreek",  "712 N Fairfield Rd",  None),
    "mason":        ("Mason",        "5633 Tylersville Rd", None),
    "troy":         ("Troy",         "2950 Stone Cir Dr",   None),
    "kettering":    ("Beavercreek",  None,                  "about seven miles east"),
    "centerville":  ("Beavercreek",  None,                  "about nine miles northeast"),
    "huber":        ("Beavercreek",  None,                  "about twelve miles southeast"),
    "springboro":   ("Waynesville",  None,                  "about eleven miles southeast"),
    "waynesville":  ("Waynesville",  "141 North St",        None),
    "west-chester": ("Mason",        None,                  "about seven miles east"),
}

# The routing layer. Every noindexed city page links to its indexed metro parent and
# one or two indexed neighbours, so the tail feeds the ten instead of competing with
# them. Assignments are copy-locations.md §6.2 — geography, not invention.
TAIL_LINKS = {
    "bellbrook":       ["beavercreek"],
    "fairborn":        ["beavercreek"],
    "xenia":           ["beavercreek"],
    "oakwood":         ["kettering"],
    "moraine":         ["kettering"],
    "west-carrollton": ["kettering"],
    "riverside":       ["kettering"],
    "miamisburg":      ["centerville"],
    "vandalia":        ["huber"],
    "englewood":       ["huber"],
    "tipp":            ["huber", "troy"],
    "springfield":     ["troy"],
    "franklin":        ["springboro"],
    "waynesville":     ["springboro"],
    "lebanon":         ["mason", "springboro"],
    "fairfield":       ["west-chester"],
    "middletown":      ["west-chester"],
    "northgate":       ["west-chester"],
    "blue-ash":        ["mason"],
    "sharonville":     ["mason"],
}

# Which of our covered communities sit in each county. Sourced from metros.md; a
# county with no covered community in the list gets no city sentence rather than an
# invented one. Slugs only, so the display name never has to be repeated.
COUNTY_CITIES = {
    "montgomery-county": ["dayton", "kettering", "centerville", "huber"],
    "greene-county":     ["beavercreek", "xenia"],
    "warren-county":     ["mason", "springboro", "lebanon", "franklin", "waynesville"],
    "butler-county":     ["west-chester", "fairfield", "middletown"],
    "hamilton-county":   ["cincinnati", "blue-ash", "sharonville"],
    "miami-county":      ["troy", "tipp"],
    "clark-county":      ["springfield"],
    "preble-county":     [],
    "darke-county":      [],
}

# Hero photo per location, from assets/cities/. Every location has one.
#
#   west-carrollton  wc.jpg is West Carrollton (client-confirmed 2026-08-01) — the
#                    only filename in assets/cities/ that isn't already its slug
#   hamilton-county  reuses the Cincinnati photo (client-confirmed 2026-08-01);
#                    Hamilton County is the Cincinnati county, so it is the same
#                    place rather than a stand-in. It is the one image used twice —
#                    if the two pages ever appear together, shoot a second frame.
HERO_OVERRIDES = {                           # slug -> assets/cities/<name>.jpg
    "west-carrollton": "wc",
    # Stand-in, and the alt text says so rather than claiming the frame is the
    # village. [NEEDS: a photo of Waynesville, or of the office on North St.]
    "waynesville":     "warren-county",
    "hamilton-county": "cincinnati",
}

def hero(slug):
    """Path under assets/ for a location's hero. Every location has one."""
    return f"cities/{HERO_OVERRIDES.get(slug, slug)}.jpg"
