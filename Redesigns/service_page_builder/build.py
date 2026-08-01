"""Build service pages from data objects. Run: python3 build.py [--check]"""
import os, sys
import template as T

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
HVAC = os.path.join(ROOT, "HVAC Service Pages")
PLUMB = os.path.join(ROOT, "Plumbing Service Pages")

PAGES = []  # (path, builder, data, root_class)

import json
_INV = json.load(open(os.path.join(os.path.dirname(__file__), "image_inventory.json")))

def old_img(page_rel, idx=0):
    """First (or nth) CDN image from the pre-redesign version of a page."""
    imgs = _INV.get(page_rel, [])
    return imgs[idx] if idx < len(imgs) else None

# ================================================================
# /air-conditioning — mockup 2a (desktop) / 2b (mobile), copy verbatim
# ================================================================
AIR_CONDITIONING = {
    "trade": "hvac",
    "breadcrumb": [("Heating & Air", "/services"), ("Air Conditioning", "")],
    "h1": "Fast, honest {X} in Dayton & Cincinnati.",
    "h1Highlight": "AC service",
    "intro": "Repairs, replacements, and tune-ups from the locally owned Extreme Team — upfront pricing, clean workmanship, and cool air back fast.",
    "heroChips": ["4.9 on Google", "90% Same-Day Service", "24/7 Emergency"],
    "bookingCard": {
        "eyebrow": "BOOK AC SERVICE",
        "title": "Get a tech to your door.",
        "sub": "Upfront pricing before any work begins.",
    },
    "symptoms": {
        "eyebrow": "IS YOUR AC ACTING UP?",
        "h2": "Signs it's time to call.",
        "items": [
            "Blowing warm or room-temp air",
            "Weak airflow in some rooms",
            "Turning on and off every few minutes",
            "Grinding, squealing, or rattling",
            "Water or refrigerant leaks",
            "Energy bills creeping up",
        ],
        "callout": f'Noticing more than one? Small AC problems become compressor problems — call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> before it gets expensive.',
    },
    "whatWeDo": {
        "h2": "Repair, replace, or maintain — we handle it all.",
        "cards": [
            {"title": "AC Repair",
             "desc": "Same-day diagnostics and honest repair options for every make and model — approved by you before we start.",
             "href": "/contact"},
            {"title": "AC Installation & Replacement",
             "desc": "Right-sized, high-efficiency systems installed clean — with flexible financing options.",
             "href": "/financing-options"},
            {"title": "AC Tune-Ups & Maintenance",
             "desc": "Seasonal tune-ups that catch small issues early — included twice a year with X-Plan.",
             "href": "/maintenance"},
        ],
    },
    "process": {
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or schedule online — we confirm your arrival window fast, with same-day service in most cases."},
            {"title": "Diagnose & quote upfront",
             "desc": "Your tech walks you through what's wrong and your options — flat, upfront pricing you approve first."},
            {"title": "Fixed right, guaranteed",
             "desc": "Clean workmanship, tested before we leave, and backed by our satisfaction guarantee."},
        ],
    },
    "faqEyebrow": "AC QUESTIONS",
    "faq": [
        {"q": "How fast can you get here?",
         "a": "In most cases, same day. About 90% of our calls are handled the day you reach out, and 24/7 emergency service is available for no-cool situations in extreme heat."},
        {"q": "Should I repair or replace my AC?",
         "a": "If your system is under 10 years old and the repair is minor, repair usually wins. Past 12–15 years with a major failure — like a compressor — replacement often costs less over time. We'll give you both numbers upfront, no pressure."},
        {"q": "How often does my AC need a tune-up?",
         "a": "Once a year, ideally in spring before the cooling season. X-Plan members get two seasonal tune-ups a year — one for cooling, one for heating — plus priority scheduling."},
        {"q": "Do you service all brands?",
         "a": "Yes — every major make and model, regardless of who installed it. Our techs receive ongoing training across all common residential systems."},
    ],
    "rail": {
        "photo": "https://cdn.jsdelivr.net/gh/extremheating-cloud/extreme-assets@main/images/descriptive/ac-repair.jpg?v=2",
        "photoAlt": "Extreme technician servicing an air conditioner",
        "promos": ["financing", "xplan"],
    },
    "related": [
        {"title": "Heat Pump Services", "href": "/heat-pump"},
        {"title": "Duct Cleaning", "href": "/duct-cleaning"},
        {"title": "Indoor Air Quality", "href": "/indoor-air-quality"},
    ],
}
PAGES.append((os.path.join(HVAC, "air-conditioning.html"), T.detail_page, AIR_CONDITIONING, "xsp-air-conditioning"))

# ================================================================
# /services — mockup 2c (HVAC hub), copy verbatim
# ================================================================
HVAC_HUB = {
    "eyebrow": "OUR HVAC SERVICES",
    "h1": "Every comfort system, {X}.",
    "h1Highlight": "one Extreme Team",
    "intro": "Heating, cooling, air quality, and maintenance for Dayton & Cincinnati homes — explore every service below, or just tell us what's wrong.",
    # Replaced ac-install.jpg: that photo's condenser carries a visible CARRIER badge,
    # so the HVAC hub was advertising a competitor's equipment. This is a real Ruud
    # unit from a job, badge legible, no service stickers in frame.
    "photo": T.PHOTOS["ruudHeatPump"],
    "photoPos": "50% 40%",
    "photoAlt": "A Ruud condenser installed at a Dayton-area home",
    "coreH2": "Comfort solutions for every season.",
    "core": [
        {"title": "Air Conditioning", "desc": "AC repair, replacement, and tune-ups.", "href": "/air-conditioning"},
        {"title": "Furnace & Heating", "desc": "Furnace repairs, installs, and safety checks.", "href": "/furnace-heating"},
        {"title": "Heat Pump", "desc": "Year-round efficiency with heat pump systems.", "href": "/heat-pump"},
        {"title": "Duct Cleaning", "desc": "Duct cleaning and air balancing.", "href": "/duct-cleaning"},
        {"title": "Indoor Air Quality", "desc": "Filtration, UV, and humidity control.", "href": "/indoor-air-quality"},
    ],
    "additionalLabel": "X-PLAN & ADDITIONAL SERVICES",
    "additional": [
        {"title": "Maintenance Plans", "badge": "X-PLAN", "desc": "Bi-annual tune-ups and priority service.", "href": "/maintenance"},
        {"title": "HVAC Inspections", "desc": "Full-system checks for peace of mind.", "href": "/inspection"},
        {"title": "Thermostat Services", "desc": "Smart thermostat install and setup.", "href": "/thermostat"},
        {"title": "Humidifier Services", "desc": "Whole-home humidity done right.", "href": "/humidifier"},
    ],
    "panel": "xplan",
    "cross": [
        {"cls": "lav", "t": "Interested in financing?",
         "d": "Flexible payment options that fit your budget.",
         "lm": "Learn More", "href": "/financing-options"},
        {"cls": "mint", "t": "Need a plumber instead?",
         "d": "Drains, water heaters, sump pumps, and more.",
         "lm": "Plumbing Services", "href": "/plumbing/services"},
    ],
}
PAGES.append((os.path.join(HVAC, "services.html"), T.hub_page, HVAC_HUB, "xsp-hvac-hub"))

# ================================================================
# /plumbing/services — 2c template with README swaps (copy formulas)
# ================================================================
PLUMB_HUB = {
    "eyebrow": "OUR PLUMBING SERVICES",
    "h1": "Every drain and drop, {X}.",
    "h1Highlight": "one Extreme Team",
    "intro": "Drains, water heaters, sump pumps, and gas lines for Dayton & Cincinnati homes — explore every service below, or just tell us what's wrong.",
    # PLACEHOLDER: the slot wants a plumber on the job and no such photo exists yet
    # (Block A of the shot list). A real branded van beats an empty grey box until
    # then — swap it when the session delivers.
    "photo": T.PHOTOS["vans"],
    "photoAlt": "Extreme service vans heading out on calls",
    "coreH2": "Reliable help for your home plumbing systems.",
    "core": [
        {"title": "Clogged Drain", "desc": "Fast help for clogged and slow drains.", "href": "/plumbing/clogged-drain"},
        {"title": "Water Heater", "desc": "Repair, replacement, and tankless upgrades.", "href": "/plumbing/water-heater/overview"},
        {"title": "Sewer Line", "desc": "Inspection, repair, and cleaning.", "href": "/plumbing/sewer-line/overview"},
        {"title": "Sump Pump", "desc": "Protection against basement water issues.", "href": "/plumbing/sump-pump/overview"},
        {"title": "Gas Line", "desc": "Safe installation and repair for gas piping.", "href": "/plumbing/gas-line/overview"},
    ],
    "additionalLabel": "ADDITIONAL SERVICES",
    "additional": [
        {"title": "Emergency Plumbing", "desc": "24/7 help when water won't wait.", "href": "/plumbing/emergency-plumbing"},
        {"title": "Leak Detection", "desc": "Find and repair hidden leaks fast.", "href": "/plumbing/leak-detection"},
        {"title": "Water Treatment", "desc": "Filtration and conditioning for cleaner water.", "href": "/plumbing/water-treatment"},
        {"title": "Toilet Repair", "desc": "Running, clogged, or leaking — fixed right.", "href": "/plumbing/toilet-repair"},
    ],
    "panel": "xplan",
    "cross": [
        {"cls": "lav", "t": "Interested in financing?",
         "d": "Flexible payment options that fit your budget.",
         "lm": "Learn More", "href": "/financing-options"},
        {"cls": "mint", "t": "Need HVAC instead?",
         "d": "Heating, cooling, and air quality from the same team.",
         "lm": "HVAC Services", "href": "/services"},
    ],
}
PAGES.append((os.path.join(PLUMB, "services.html"), T.hub_page, PLUMB_HUB, "xsp-plumbing-hub"))

# ================================================================
# /furnace-repair — mockup 2d (sub-page tier), copy verbatim
# ================================================================
FURNACE_REPAIR = {
    "trade": "hvac",
    "breadcrumb": [("Heating & Air", "/services"), ("Furnace & Heating", "/furnace-heating"), ("Repair", "")],
    "h1": "Fast, safe {X} — day or night.",
    "h1Highlight": "furnace repair",
    "intro": "No heat is an emergency in an Ohio winter. We diagnose fast, price upfront, and repair every make and model — 24/7.",
    "scheduleLabel": "Schedule Repair",
    "pillNav": {
        "label": "FURNACE & HEATING",
        "items": [
            {"label": "Overview", "href": "/furnace-heating", "active": False},
            {"label": "Installation", "href": "/furnace-installation", "active": False},
            {"label": "Repair", "href": "/furnace-repair", "active": True},
        ],
    },
    "symptoms": {
        "eyebrow": "NO HEAT?",
        "h2": "Watch for these warning signs.",
        "items": [
            "Blowing cold or lukewarm air",
            "Short cycling on and off",
            "Yellow or flickering burner flame",
            "Burning or musty smells",
            "Banging or scraping sounds",
            "Heating bills creeping up",
        ],
        "safety": True,
        "callout": f'<b>Safety first:</b> smell gas or suspect carbon monoxide? Leave the house first, then call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> — 24/7.',
    },
    "process": {
        "h2": "A repair visit without surprises.",
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or schedule online — no-heat calls get priority, with same-day service in most cases."},
            {"title": "Diagnose & quote upfront",
             "desc": "We test the system, explain what failed, and price the fix before any work begins."},
            {"title": "Fixed right, safety-checked",
             "desc": "Every repair ends with a full safety check — heat exchanger, venting, and CO included."},
        ],
    },
    "decision": {
        "title": "Repair or replace?",
        "desc": "If your furnace is 15+ years old and the repair is major, replacement often wins on cost. We'll give you both numbers — no pressure.",
        "linkLabel": "Furnace Installation →",
        "href": "/furnace-installation",
    },
    "faqEyebrow": "FURNACE QUESTIONS",
    "faq": [
        {"q": "Do you repair furnaces nights and weekends?",
         "a": "Yes — no-heat emergencies don't keep business hours, and neither do we. 24/7 emergency furnace repair across Dayton and Cincinnati."},
        {"q": "Do you repair all furnace brands?",
         "a": "Yes — gas, electric, and high-efficiency models from every major manufacturer, regardless of who installed it."},
        {"q": "Is a yellow pilot flame dangerous?",
         "a": "It can be. A healthy flame burns blue; yellow or flickering can signal incomplete combustion, which can produce carbon monoxide. Turn the furnace off and have it checked before running it again."},
    ],
    "bookingCard": {
        "eyebrow": "BOOK FURNACE REPAIR",
        "title": "No heat? We're on it.",
        "sub": "Priority dispatch for no-heat calls.",
        "trust2": "24/7 emergency",
    },
    "rail": {
        "promos": ["xplanSub"],
        "photo": old_img("HVAC Service Pages/furnace-repair.html"),
        "photoAlt": "Extreme technician repairing a furnace",
    },
    "siblings": {
        "label": "FURNACE & HEATING",
        "items": [
            {"title": "Furnace & Heating Overview", "href": "/furnace-heating"},
            {"title": "Furnace Installation", "href": "/furnace-installation"},
            {"title": "Thermostat Services", "href": "/thermostat"},
        ],
    },
}
PAGES.append((os.path.join(HVAC, "furnace-repair.html"), T.sub_page, FURNACE_REPAIR, "xsp-furnace-repair"))

# ================================================================
# /plumbing/water-heater/overview — mockup 2e (detail + pill nav), verbatim
# ================================================================
WATER_HEATER_OVERVIEW = {
    "trade": "plumbing",
    "breadcrumb": [("Plumbing", "/plumbing/services"), ("Water Heater Services", "")],
    "h1": "Hot water, {X}.",
    "h1Highlight": "back fast",
    "intro": "Repair, replacement, and tankless upgrades for every water heater — from the same Extreme Team you trust with your comfort.",
    "heroChips": ["4.9 on Google", "Same-Day Replacement", "Licensed Plumbers"],
    "bookingCard": {
        "eyebrow": "BOOK WATER HEATER SERVICE",
        "title": "Get a plumber to your door.",
        "sub": "Upfront pricing before any work begins.",
    },
    "pillNav": {
        "label": "WATER HEATER SERVICES",
        "items": [
            {"label": "Overview", "href": "/plumbing/water-heater/overview", "active": True},
            {"label": "Repair", "href": "/plumbing/water-heater/repair", "active": False},
            {"label": "Installation", "href": "/plumbing/water-heater/installation", "active": False},
        ],
    },
    "symptoms": {
        "eyebrow": "IS IT FAILING?",
        "h2": "Signs your water heater is on its way out.",
        "items": [
            "No hot water, or it runs out fast",
            "Rusty or metallic-smelling water",
            "Popping or rumbling from the tank",
            "Water pooling around the base",
            "Pilot light won't stay lit",
            "Tank is 10+ years old",
        ],
        "callout": f'Tank leaking? Shut off the water supply, then call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> — leaks only get worse.',
    },
    "whatWeDo": {
        "h2": "Repair it, replace it, or go tankless.",
        "cards": [
            {"title": "Water Heater Repair",
             "desc": "Elements, thermostats, valves, pilot issues — diagnosed fast and priced before we start.",
             "href": "/plumbing/water-heater/repair"},
            {"title": "Water Heater Installation & Replacement",
             "desc": "Right-sized tank replacements, installed clean — often the same day, with financing options.",
             "href": "/plumbing/water-heater/installation"},
            {"title": "Tankless Water Heaters",
             "desc": "Endless hot water and lower energy use — we'll tell you honestly if tankless fits your home.",
             "href": "/plumbing/water-heater/installation"},
        ],
    },
    "process": {
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or schedule online — no-hot-water calls get priority dispatch."},
            {"title": "Diagnose & quote upfront",
             "desc": "Repair vs. replace laid out honestly, with flat pricing you approve first."},
            {"title": "Hot water, guaranteed",
             "desc": "Installed to code, tested at every tap, and the old unit hauled away."},
        ],
    },
    "faqEyebrow": "WATER HEATER QUESTIONS",
    "faq": [
        {"q": "Can you replace my water heater the same day?",
         "a": "Usually, yes. We stock common tank sizes and can install the same day in most cases — so you're not going a week without hot water."},
        {"q": "Tank or tankless — which is right for my home?",
         "a": "Tanks cost less upfront and suit most homes; tankless costs more to install but delivers endless hot water and lower energy bills. We'll walk you through both honestly — no upsell."},
        {"q": "How long do water heaters last?",
         "a": "Tank units typically last 8–12 years; tankless can reach 20 with maintenance. Past the 10-year mark, replacement is usually smarter than a major repair."},
        {"q": "What size water heater do I need?",
         "a": "It depends on your household — a family of four typically needs a 40–50 gallon tank. We size it to your actual hot water use, not a guess."},
    ],
    "rail": {
        # Carried over from the old page (hotlinked stock preview) — replace
        # with a licensed copy on the extreme-assets CDN when available.
        "photo": "https://media.istockphoto.com/id/1487523781/photo/tankless-water-heater-connected-to-recirculator.jpg?s=612x612&w=0&k=20&c=VedTUMp5wz-1hlZ2q395jWE8rjiI1LlCWOfnscc0Gac=",
        "photoAlt": "Tankless water heater installation",
        "promos": ["scheduleFast", "specials"],
    },
    "related": [
        {"title": "Clogged Drain", "href": "/plumbing/clogged-drain"},
        {"title": "Sump Pump Services", "href": "/plumbing/sump-pump/overview"},
        {"title": "Leak Detection", "href": "/plumbing/leak-detection"},
    ],
}
PAGES.append((os.path.join(PLUMB, "water-heater", "overview.html"), T.detail_page, WATER_HEATER_OVERVIEW, "xsp-water-heater"))

# ================================================================
# Step-5 rollout — remaining pages from rollout.py data objects
# ================================================================
import rollout
# maintenance.html is now built from mockup 3a below — drop the interim version
del rollout.HVAC_PAGES["maintenance.html"]

# ================================================================
# /maintenance — mockup 3a (X-Plan membership page), copy verbatim
# ================================================================
MAINTENANCE_3A = {
    "breadcrumb": [("Heating & Air", "/services"), ("X-Plan Maintenance", "")],
    "h1": "Never think about {X} again.",
    "h1Highlight": "tune-ups",
    # Leads with Zero Risk Investment per programs.md — it is the only benefit
    # competitors don't also offer. Both conditions (consecutive years, $2,500 or
    # 10 years) must appear wherever the accrual is stated.
    "intro": "X-Plan is our maintenance membership, and it pays you back: 100% of the investment of your X-Plan membership in consecutive years is applied toward your end-of-life equipment replacement — up to $2,500 or 10 years. Along the way, two visits a year, 15% off all repairs, and priority scheduling.",
    "heroChips": ["2 Tune-Ups a Year", "15% Off Repairs", "Priority Scheduling"],
    "benefits": {
        "h2": "One membership, six ways it pays off.",
        "cards": [
            {"t": "100% back toward your next system",
             "d": "Every dollar of your membership in consecutive years is applied toward end-of-life equipment replacement — up to $2,500 or 10 years, whichever comes first."},
            {"t": "Two seasonal tune-ups a year",
             "d": "AC in spring, furnace in fall — we call you to schedule, not the other way around."},
            {"t": "15% off every repair",
             "d": "HVAC and plumbing repairs alike — member pricing, automatically."},
            {"t": "Priority scheduling",
             "d": "Members move to the front of the line — even in peak season."},
            {"t": "5-year warranty on repairs",
             "d": "Five times the standard coverage on parts and labor we install."},
            {"t": "Discounted service calls",
             "d": "$77 instead of $97 during business hours — $177 instead of $197 for emergencies."},
        ],
    },
    "useCases": {
        "h2": "Made for homeowners who'd rather not think about it.",
        "cards": [
            {"t": "Your system is 5+ years old",
             "d": "This is when small issues start compounding. Twice-a-year checks catch them while they're still cheap."},
            {"t": "You just bought a new system",
             "d": "Manufacturer warranties require documented annual maintenance — X-Plan keeps you covered without the calendar reminders."},
            {"t": "You've had a surprise breakdown before",
             "d": "The worst repairs happen on the worst days. Priority scheduling and discounted service calls take the sting out."},
        ],
    },
    "value": {
        "h2": "Most members come out ahead in year one.",
        "stats": [
            {"n": "2×", "cap": "tune-ups included — booked separately, they'd cost more than the membership alone."},
            {"n": "15%", "cap": "off one mid-size repair typically covers the rest."},
            {"n": "$20", "cap": "off every service call — including emergencies, when timing is worst."},
        ],
    },
    "process": {
        "h2": "Join once. We handle the rest.",
        "steps": [
            {"title": "Join online or by phone",
             "desc": "Pick yearly or monthly billing, and we'll set your membership up on the spot."},
            {"title": "We schedule your tune-ups",
             "desc": "We reach out each spring and fall to book your visits around your calendar."},
            {"title": "You save automatically",
             "desc": "Member pricing, priority dispatch, and the 5-year repair warranty apply from day one."},
        ],
    },
    "faqEyebrow": "X-PLAN QUESTIONS",
    "faq": [
        {"q": "How does the Zero Risk Investment work?",
         "a": "100% of what you pay for X-Plan in consecutive years is applied toward replacing your equipment at the end of its life — up to $2,500 or 10 years, whichever comes first. Membership years have to be consecutive, and the credit follows you rather than the property."},
        {"q": "What happens if I let my membership lapse?",
         "a": "The Zero Risk Investment builds on consecutive years, so a gap in membership interrupts it. If you're thinking about pausing, call us first and we'll walk through what it means for your balance."},
        {"q": "Does the 15% discount cover plumbing repairs too?",
         "a": "Yes — member pricing applies to HVAC and plumbing repairs alike, automatically."},
        {"q": "What happens at a tune-up visit?",
         "a": "A full system inspection and safety check: capacitor, relay, and thermostat testing, compressor amp draws, drain line cleaning, a pressure check, and light coil cleaning."},
    ],
    "joinBand": {
        "bold": "Ready to stop worrying about breakdowns?",
        "rest": f"Join X-Plan in one call — {T.PHONE_DISPLAY}.",
    },
}
PAGES.append((os.path.join(HVAC, "maintenance.html"), T.xplan_page, MAINTENANCE_3A, "xsp-maintenance"))

def _slug(fname):
    return fname.replace(".html", "").replace("/", "-")

# Pages whose legacy inventory image is replaced by real Extreme photography.
# These win over old_img(); everything else keeps whatever the old page carried.
PHOTO_OVERRIDES = {
    # The legacy heatpump.jpg is a generic stock condenser. This is an actual Ruud
    # heat pump from a job, badge legible — right equipment and right brand for the
    # one page on the site that is specifically about heat pumps.
    "HVAC Service Pages/heat-pump.html": {
        "photo": T.PHOTOS["ruudHeatPump"],
        "photoPos": "50% 40%",
        "photoAlt": "A Ruud heat pump installed at a Dayton-area home",
    },
    # The legacy furnace-install.jpg is 379px and, on the page selling new installs,
    # shows a dirty OLD furnace. This is a real Ruud air handler from a job.
    "HVAC Service Pages/furnace-installation.html": {
        "photo": T.PHOTOS["ruudInstall"],
        "photoPos": "50% 55%",
        "photoAlt": "A newly installed Ruud air handler in a Dayton-area home",
    },
}

def _wire_image(data, rel):
    """Attach the page's own legacy image (CDN or carried-over stock)."""
    override = PHOTO_OVERRIDES.get(rel)
    if override:
        data["rail"].update(override)
        return data
    img = old_img(rel)
    if img and "Logo" not in img:
        data["rail"]["photo"] = img
    return data

for fname, data in rollout.HVAC_PAGES.items():
    rel = f"HVAC Service Pages/{fname}"
    PAGES.append((os.path.join(HVAC, fname), T.detail_page,
                  _wire_image(data, rel), f"xsp-{_slug(fname)}"))

for fname, data in rollout.HVAC_SUBS.items():
    rel = f"HVAC Service Pages/{fname}"
    PAGES.append((os.path.join(HVAC, fname), T.sub_page,
                  _wire_image(data, rel), f"xsp-{_slug(fname)}"))

for fname, data in rollout.PLUMB_PAGES.items():
    rel = f"Plumbing Service Pages/{fname}"
    PAGES.append((os.path.join(PLUMB, fname), T.detail_page,
                  _wire_image(data, rel), f"xsp-{_slug(fname)}"))

for fname, data in rollout.PLUMB_FAMILIES.items():
    rel = f"Plumbing Service Pages/{fname}"
    builder = T.detail_page if fname.endswith("overview.html") else T.sub_page
    PAGES.append((os.path.join(PLUMB, *fname.split("/")), builder,
                  _wire_image(data, rel), f"xsp-{_slug(fname)}"))

# ---------------- company pages (4a-4d) — Other pages/ ----------------
import company_pages
PAGES.extend(company_pages.pages(ROOT))

# ---------------- Extreme Rewards referral page — Other pages/ ----------------
import referral
PAGES.extend(referral.pages(ROOT))

# ---------------- Terms of Service & Limited Warranty — Other pages/ ----------------
import terms
PAGES.extend(terms.pages(ROOT))

# ---------------------------------------------------------------- build
def main():
    for path, builder, data, root_class in PAGES:
        html = builder(data, root_class)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(html)
        print(f"wrote {os.path.relpath(path, ROOT)}  ({len(html):,} bytes)")

if __name__ == "__main__":
    main()
