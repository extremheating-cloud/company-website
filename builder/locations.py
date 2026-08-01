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

# Hero photo per location, from assets/cities/. One gap:
#   hamilton-county — no image in the set at all. Either shoot one or fall back to
#   the Cincinnati photo, since Hamilton County is the Cincinnati county.
# wc.jpg is West Carrollton (client-confirmed 2026-08-01) — the only filename in
# assets/cities/ that isn't already its slug.
HERO_OVERRIDES = {"west-carrollton": "wc"}   # slug -> assets/cities/<name>.jpg
NO_HERO = {"hamilton-county"}

def hero(slug):
    """Path under assets/ for a location's hero, or None if we don't have one."""
    if slug in NO_HERO:
        return None
    return f"cities/{HERO_OVERRIDES.get(slug, slug)}.jpg"
