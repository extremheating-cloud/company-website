"""Site-wide facts. One place to change a phone number, a price, or an address.

Before this file, the phone number was hardcoded in six source files and rendered on
303 pages; X-Plan pricing lived in five. That happened because the Framer components
could not import from the builder. Once everything renders from here, changing a
value is one edit.

Anything a customer could quote back at you belongs in this file, not inline in a
page. If you find yourself typing a price, a phone number or an address into a page
module, add it here instead.
"""

# ---------------------------------------------------------------- identity
COMPANY = "Extreme Heating, Air, Plumbing"
COMPANY_SHORT = "Extreme"
TAGLINE = "Comfort &amp; efficiency you can trust."
DOMAIN = "extremeheating.com"
SITE_URL = "https://www.extremeheating.com"

# Two legal entities under common ownership — see pages/company/terms.html.
ENTITY_HVAC = "Extreme Heating &amp; Cooling LLC"
ENTITY_PLUMBING = "Extreme Home Services LLC"

# ---------------------------------------------------------------- contact
PHONE_DISPLAY = "(844) 584-7399"
PHONE_TEL = "tel:18445847399"
PHONE_E164 = "+18445847399"

# Service areas, not storefronts, on every page except /contact.
OFFICES = [
    {"city": "Dayton", "label": "Beavercreek office",
     "street": "712 N Fairfield Rd", "locality": "Beavercreek", "region": "OH", "zip": "45434"},
    {"city": "Cincinnati", "label": "Mason office",
     "street": "5633 Tylersville Rd", "locality": "Mason", "region": "OH", "zip": "45040"},
]

# Client-confirmed 2026-08-01. 8-5 is when the OFFICE is staffed; emergency service
# genuinely runs around the clock. Keep these two facts distinct — collapsing them is
# what previously made the hours read as a contradiction of the 24/7 claim.
HOURS_STAFFED = "Monday – Friday, 8:00 AM – 5:00 PM"
HOURS_EMERGENCY = "24/7 — every day of the year"

SOCIAL = [
    ("Facebook", "https://www.facebook.com/ExtremeHeatingDayton"),
    ("Instagram", "https://www.instagram.com/extremeheating/"),
    ("YouTube", "https://www.youtube.com/@extremeheatingaircondition2902"),
    ("Google Reviews", "https://maps.app.goo.gl/G7H8dMEFgQLYoeoa7"),
]

# ---------------------------------------------------------------- proof points
# The brand rule is that a claim always travels with its proof point, so these are
# the approved wordings. Do not round or restate them.
GOOGLE_RATING = "4.9"
YEARS_LOCAL = "20+"
JOBS_COMPLETED = "25k+"
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
        "Member service calls: $77 vs $97 · $177 vs $197 after hours",
    ],
    "zeroRisk": ("100% of the investment of your X-Plan membership in consecutive years "
                 "is applied toward your end-of-life equipment replacement — up to "
                 "$2,500 or 10 years."),
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
