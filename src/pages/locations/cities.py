# Slugs are the live Framer URLs (huber, tipp); renaming one needs a route change and a redirect.

# TODO: drop plumbing if the location pages ship before the plumbing line does.
SERVICES = [
    ("heating", "Heating"),
    ("cooling", "Cooling"),
    ("maintenance", "Maintenance"),
    ("duct-cleaning", "Duct Cleaning"),
    ("indoor-air-quality", "Indoor Air Quality"),
    ("plumbing", "Plumbing"),
]

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

GROUPS = [
    ("Dayton", DAYTON),
    ("Cincinnati", CINCINNATI),
    ("Counties", COUNTIES),
]

ALL = DAYTON + CINCINNATI + COUNTIES

# head.py reads FEATURED by name and silently falls back to a stale copy if it is renamed.
# TODO: client sign-off on this exact ten.
FEATURED_ORDER = [
    "dayton", "cincinnati",
    "beavercreek", "mason", "troy",
    "kettering", "centerville", "huber",
    "springboro",
    "west-chester",
]
FEATURED = set(FEATURED_ORDER)

_slugs = {s for s, _ in ALL}
assert FEATURED <= _slugs, f"FEATURED has slugs with no page: {FEATURED - _slugs}"
assert len(FEATURED) == 10, f"FEATURED must be exactly ten, got {len(FEATURED)}"
del _slugs

LONG_NAME = {
    "west-chester": "West Chester Township",
    "huber": "Huber Heights",
    "tipp": "Tipp City",
}

def long_name(slug, fallback):
    return LONG_NAME.get(slug, fallback)

# Street only where the office is inside that city; a street anywhere else dilutes the real NAP records.
# TODO: nearest office and mileage for the 19 noindexed cities.
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

HERO_OVERRIDES = {
    "west-carrollton": "wc",
    # TODO: stand-in until there is a Waynesville photo; its alt text says so.
    "waynesville":     "warren-county",
    "hamilton-county": "cincinnati",
}

def hero(slug):
    return f"cities/{HERO_OVERRIDES.get(slug, slug)}.jpg"
