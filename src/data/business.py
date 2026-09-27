from urllib.parse import quote as _quote

COMPANY = "Extreme Heating, Air, Plumbing"
COMPANY_SHORT = "Extreme"
TAGLINE = "Comfort &amp; efficiency you can trust."

# www is canonical; the apex 308s to it
CANONICAL_HOST = "www.extremeheating.com"
SITE_URL = f"https://{CANONICAL_HOST}"

# bare domain for email and print only; never build a URL from it
DOMAIN = "extremeheating.com"

# no trailing slash except the homepage; the live site 308s /about/ to /about
def canonical(path="/"):
    path = "/" + str(path).strip("/")
    return SITE_URL + ("/" if path == "/" else path)

def maps_dir(address, html=True):
    amp = "&amp;" if html else "&"
    return f"https://www.google.com/maps/dir/?api=1{amp}destination={_quote(address)}"

ENTITY_HVAC = "Extreme Heating and Cooling Ltd"
ENTITY_PLUMBING = "Extreme Home Services LLC"

PHONE_DISPLAY = "(844) 584-7399"
PHONE_TEL = "tel:18445847399"
PHONE_E164 = "+18445847399"
EMAIL = "info@extremeheating.com"

# must match the A2P registration exactly; printed as text only on /contact and /privacy
SMS_DISPLAY = "(937) 977-1464"
SMS_E164 = "+19379771464"

# no ?body=: some handsets drop the recipient when the separator is wrong
SMS_HREF = f"sms:{SMS_E164}"

SMS_ARIA = f"Text us at {SMS_DISPLAY}"

LICENSE_HVAC = "OH LIC #37179"
LICENSE_PLUMBING = "OH LIC #13557"

LICENSES_LINE = f"HVAC {LICENSE_HVAC} &middot; Plumbing {LICENSE_PLUMBING}"

FOUNDED = 2004
MASON_OPENED = 2018

HOURS_STAFFED = "Monday – Friday, 8:00 AM – 5:00 PM"
HOURS_EMERGENCY = "24/7 — every day of the year"

HOURS_STAFFED_PROSE = "Monday to Friday, 8:00 AM to 5:00 PM"
HOURS_STAFFED_SHORT = "Mon–Fri, 8–5"

# publishable in body copy and FAQ answers, never in an h1, h2 or hero
SERVICE_CALL = 97
SERVICE_CALL_EMERGENCY = 197
SERVICE_CALL_MEMBER = 77
SERVICE_CALL_MEMBER_EMERGENCY = 177
SERVICE_CALL_LINE = (f"Member service calls: ${SERVICE_CALL_MEMBER} vs ${SERVICE_CALL} "
                     f"&middot; ${SERVICE_CALL_MEMBER_EMERGENCY} vs "
                     f"${SERVICE_CALL_EMERGENCY} after hours")

SERVICE_CALL_FAQ = {
    "q": "What does it cost to get someone out?",
    "a": (f"${SERVICE_CALL} during business hours, ${SERVICE_CALL_EMERGENCY} nights, "
          f"weekends and holidays. That covers the trip and the diagnosis, and you hear "
          f"the repair price before anyone starts work, so nothing gets added after the "
          f"fact. X-Plan members pay ${SERVICE_CALL_MEMBER} and "
          f"${SERVICE_CALL_MEMBER_EMERGENCY}."),
}

# never add an APR, term or finance charge; keep "as low as" and FINANCE_QUALIFIER on every figure
FINANCE_AC = 49
FINANCE_HEAT_PUMP = 69
FINANCE_FULL_SYSTEM = 89
FINANCE_QUALIFIER = "with approved credit"

def finance_line(amount, thing):
    return f"as low as ${amount} a month {FINANCE_QUALIFIER}"

# office hours only; 24/7 emergency service is not premises hours
HOURS_SPEC = {"dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
              "opens": "08:00", "closes": "17:00"}

# geo stays None until the GBP pins are supplied; never geocode the street address
OFFICES = [
    {"slug": "beavercreek", "label": "Beavercreek office", "primary": True,
     "street": "712 N Fairfield Rd", "locality": "Beavercreek", "region": "OH",
     "zip": "45434", "county": "Greene", "metro": "Dayton",
     "phone": "(937) 431-7399", "phone_e164": "+19374317399",
     "geo": None, "page": "/locations/beavercreek"},
    {"slug": "mason", "label": "Mason office", "primary": False,
     "street": "5633 Tylersville Rd", "locality": "Mason", "region": "OH",
     "zip": "45040", "county": "Warren", "metro": "Cincinnati",
     "phone": "(513) 640-7399", "phone_e164": "+15136407399",
     "geo": None, "page": "/locations/mason"},
    {"slug": "troy", "label": "Troy office", "primary": False,
     "street": "2950 Stone Cir Dr", "locality": "Troy", "region": "OH",
     "zip": "45373", "county": "Miami", "metro": "Dayton",
     "phone": "(937) 426-7399", "phone_e164": "+19374267399",
     "geo": None, "page": "/locations/troy"},
    {"slug": "waynesville", "label": "Waynesville office", "primary": False,
     "street": "141 North St", "locality": "Waynesville", "region": "OH",
     # metro None on purpose: presented as the plumbing hub, not as either metro
     "zip": "45068", "county": "Warren", "metro": None,
     "descriptor": "Our plumbing hub",
     "phone": "(513) 897-2753", "phone_e164": "+15138972753",
     "geo": None, "page": "/locations/waynesville"},
]

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

OFFICE_PHONE_BY_TOWN = {o["locality"]: (o["phone"], "tel:" + o["phone_e164"])
                        for o in OFFICES if o.get("phone")}

def office_phone(town):
    return OFFICE_PHONE_BY_TOWN.get(town, (None, None))
OFFICE_PRIMARY = next(o for o in OFFICES if o["primary"])
assert sum(1 for o in OFFICES if o["primary"]) == 1, "exactly one primary office"

# keep offices with no page (href None renders as plain text); do not filter them out
OFFICE_LINKS = [(o["locality"], o["page"]) for o in OFFICES]

SOCIAL = [
    ("Facebook", "https://www.facebook.com/ExtremeHeatingDayton"),
    ("Instagram", "https://www.instagram.com/extremeheating/"),
    ("YouTube", "https://www.youtube.com/@extremeheatingaircondition2902"),
    ("Google Reviews", "https://maps.app.goo.gl/G7H8dMEFgQLYoeoa7"),
]

SAME_AS = [u for _, u in SOCIAL]

GOOGLE_RATING = "4.9"

REVIEW_COUNT = "1,595"
REVIEW_COUNT_N = 1595
# multi-source Birdeye aggregate: "customer reviews", never "Google reviews"
REVIEW_SOURCE = "customer reviews"

YEARS_LOCAL = "20+"
JOBS_COMPLETED = "25k+"
JOBS_COMPLETED_LONG = "25,000+"
SAME_DAY = "90%"

STATS = [
    (YEARS_LOCAL, "Years of service"),
    (JOBS_COMPLETED, "Jobs completed"),
    ("24/7", "Emergency service"),
    (SAME_DAY, "Same-day service"),
]

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
        SERVICE_CALL_LINE,
    ],
    # head.n_xplan_service() greps for "consecutive" and "$2,500"; keep both literal
    "zeroRisk": ("Stay a member in consecutive years and every dollar you have paid comes "
                 "off the cost of replacing that system at end of life, up to $2,500 or "
                 "10 years, whichever comes first."),
}

# never publish the $100 without its "$750 or more" minimum; the $250 has no minimum
REWARDS = {"newSystem": "$250", "everythingElse": "$100", "everythingElseMin": "$750"}

LENDERS = ["GoodLeap", "Synchrony", "Wright-Patt Credit Union"]

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

FOOTER_NAP = {
    "name": COMPANY,
    "street": OFFICE_PRIMARY["street"],
    "citystate": OFFICE_PRIMARY["citystate"],
    "phoneDisplay": PHONE_DISPLAY,
    "phoneHref": PHONE_TEL,
    "email": EMAIL,
    "emailHref": f"mailto:{EMAIL}",
    "hoursStaffed": f"Office staffed {HOURS_STAFFED_SHORT}",
    "hoursEmergency": "Emergencies 24/7",
    "officesLabel": "Offices",
    "offices": OFFICE_LINKS,
}

FOOTER_LEGAL = f"&copy; 2026 {COMPANY}. All rights reserved. &middot; {LICENSES_LINE}"
