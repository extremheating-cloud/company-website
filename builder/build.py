"""Build service pages from data objects. Run: python3 build.py [--check]"""
import os, re, sys
import template as T

# builder/ sits one level below the repo root. The generated pages go into pages/,
# mirroring the site's own URL structure.
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PAGES_DIR = os.path.join(ROOT, "pages")
HVAC = os.path.join(PAGES_DIR, "hvac")
PLUMB = os.path.join(PAGES_DIR, "plumbing")

PAGES = []  # (path, builder, data, root_class)

import json
_INV = json.load(open(os.path.join(os.path.dirname(__file__), "image_inventory.json")))

def old_img(page_rel, idx=0):
    """First (or nth) CDN image from the pre-redesign version of a page.

    The inventory stores whole URLs, and the ones pointing at our own repo carry the
    commit that was pinned when it was captured. Left alone, those pages ignore
    ASSET_COMMIT entirely — they kept serving bytes from an old commit while every
    other page moved to the new pin, so re-encoding or replacing one of those files
    would silently do nothing. Re-pin ours; leave third-party stock URLs alone.
    """
    imgs = _INV.get(page_rel, [])
    url = imgs[idx] if idx < len(imgs) else None
    if url and T.ASSET_REPO in url:
        url = re.sub(re.escape(T.ASSET_REPO) + r"@[0-9a-f]+/",
                     f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/", url)
    return url

# ================================================================
# /air-conditioning — mockup 2a (desktop) / 2b (mobile), copy verbatim
# ================================================================
AIR_CONDITIONING = {
    "trade": "hvac",
    "breadcrumb": [("Heating & Air", "/services"), ("Air Conditioning", "")],
    "h1": "Air conditioning service in {X}.",
    "h1Highlight": "Dayton & Cincinnati",
    # The answer-first block: 31 words, second person, no self-naming. This is the
    # passage an engine lifts, so it still stands alone — but it reads like something
    # a person would say. Entity, licences and job count live in the JSON-LD.
    "answer": ("AC out? We repair, replace and tune up central air and heat pumps across "
               "Dayton and Cincinnati — every major brand, whoever installed it. We handle "
               "most calls the same day."),
    "intro": "Repair, replacement and tune-ups, from a locally owned crew. You'll know the price before anything gets touched.",
    # The 1,595-review figure is a Birdeye aggregate pooling several platforms, so the
    # chip cannot say "on Google" — that is the one review claim a competitor can
    # disprove in thirty seconds. facts.md confirms 4.9 / 1,595 for on-site display.
    "heroChips": ["4.9 from 1,595 reviews", "90% Same-Day Service", "24/7 Emergency"],
    "bookingCard": {
        "eyebrow": "BOOK AC SERVICE",
        "title": "Get a tech to your door.",
        "sub": "Upfront pricing before any work begins.",
    },
    "symptoms": {
        "eyebrow": "IS YOUR AC ACTING UP?",
        "h2": "How do I know my AC is going out?",
        "items": [
            "Blowing warm or room-temp air",
            "Weak airflow in some rooms",
            "Turning on and off every few minutes",
            "Grinding, squealing, or rattling",
            "Water or refrigerant leaks",
            "Energy bills creeping up",
        ],
        "callout": f'Seeing more than one? Small AC problems turn into compressor problems. Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> before that happens, or see what each symptom usually means on our <a href="/ac-repair">AC repair</a> page.',
    },
    "whatWeDo": {
        "h2": "What kind of AC work do you handle?",
        "cards": [
            {"title": "AC Repair",
             "desc": "Same-day diagnostics on any make or model. You see the price and approve it before we start.",
             "href": "/ac-repair"},
            {"title": "AC Installation & Replacement",
             "desc": "Right-sized, high-efficiency systems, installed clean — with financing if you'd rather spread it out.",
             "href": "/ac-installation"},
            {"title": "AC Tune-Ups & Maintenance",
             "desc": "A seasonal tune-up catches the small stuff early — two a year come with X-Plan.",
             "href": "/maintenance"},
        ],
    },
    # The decision table and the lifespan/brand questions sit before Process; the two
    # "how do I actually book this" questions sit after it, in sectionsTail. Symptoms
    # and emergencies belong to /ac-repair and cost and sizing to /ac-installation —
    # every section that brushes one of those hands off with a link instead of
    # competing with it.
    "sections": [
        {"eyebrow": "DECIDING",
         "id": "repair-or-replace",
         "h2": "Should I repair or replace my air conditioner?",
         "body": ("Age and repair cost decide it, not the symptom. A newer system with a "
                  "failed capacitor or contactor is a repair. An older one facing a "
                  "compressor or coil is usually where a new unit costs you less over the "
                  "years it has left."),
         # No dollar figures anywhere in this table, by design: the one-third rule of
         # thumb is client-approved, a published repair price is not.
         "table": {
             "caption": "Repair or replace an air conditioner: what we weigh on a service call.",
             "takeaway": ("We'll point you to replacement when the system is past its "
                          "expected life and the repair quote is closing in on a third of "
                          "what a new one costs."),
             "columns": ["What we look at", "Repair when",
                         "Replace when"],
             "rows": [
                 ["System age", "Under 10 years old", "Past 12 to 15 years"],
                 ["Repair cost", "Well under a third of replacement cost",
                  "At or above roughly a third of replacement cost"],
                 ["Breakdown history", "First failure in several cooling seasons",
                  "Second or third call in one season"],
                 ["Refrigerant", "Uses a refrigerant still in production",
                  "Uses R-22, out of production in the US since 2020"],
                 ["Energy bills", "Cooling bills are steady year over year",
                  "Cooling bills climb with no change at home"],
                 ["Comfort", "One room or one symptom",
                  "Uneven temperatures throughout the house"],
                 # Deliverable wrote "labour"; the rest of the site is US spelling.
                 ["Warranty", "Parts are still under manufacturer warranty",
                  "Parts and labor warranties have both run out"],
             ],
         }},
        {"h2": "How long does a central air conditioner last?",
         "body": ("Twelve to fifteen years is normal in this climate, and a system that "
                  "gets maintained tends to reach the top of that range. Past fifteen, most "
                  "people spend more on repairs than a replacement would have cost.")},
        {"h2": "Do you work on my brand?",
         "body": ("Every major residential make and model, whoever installed it. Our techs "
                  "train across all of them, so a warranty repair on a new system and a "
                  "twenty-year-old unit from a different brand both get handled.")},
    ],
    "process": {
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or book online. You get an arrival window fast, and most calls are same day."},
            {"title": "Diagnose & quote upfront",
             "desc": "Your tech shows you what's wrong and what the options cost. You approve the price first."},
            {"title": "Fixed right, guaranteed",
             "desc": "Clean work, tested before we leave, backed by our satisfaction guarantee."},
        ],
    },
    "sectionsTail": [
        {"h2": "How often should an air conditioner be serviced?",
         "body": ("Once a year, in spring, before the first stretch of ninety-degree weather. "
                  "A tune-up cleans the coil, checks the refrigerant charge and tests the "
                  "electrical parts that fail first in heat. "
                  '<a href="/maintenance">X-Plan</a> members get two visits a year, one for '
                  "cooling and one for heating.")},
        {"h2": "How do I book AC service?",
         "body": (f'Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> or book online, and you '
                  "get an arrival window before the tech leaves the shop. We handle roughly "
                  "90% of calls the same day, and the emergency line is answered 24/7 when a "
                  "house has no cooling.")},
    ],
    "faqEyebrow": "AC QUESTIONS",
    "faqH2": "What should I know before booking AC service?",
    "faq": [
        {"q": "Is it worth replacing an R-22 air conditioner?",
         "a": "Usually. R-22 hasn't been produced or imported in the US since 2020, so a recharge means paying for a shrinking reclaimed supply. If the unit needs a compressor or a coil, replacing it costs less over the years it has left."},
        {"q": "Can I replace the AC without replacing the furnace?",
         "a": "Yes, and often you should. The indoor coil has to match the new outdoor unit, so the furnace gets opened either way. If it's also near the end, doing both in one visit costs less than two jobs a few years apart."},
        {"q": "Do you offer emergency AC repair?",
         "a": "Yes. The emergency line runs 24/7 across the Dayton and Cincinnati metros, every day of the year. The office is staffed Monday to Friday, 8:00 AM to 5:00 PM, and after that the emergency line picks up."},
        {"q": "Does X-Plan cover the air conditioner?",
         "a": "Yes. You get two seasonal visits a year, one of them a full AC tune-up with refrigerant charge calibration up to 1 lb included. Members also get 15% off repairs and priority scheduling."},
        {"q": "How long does an air conditioner replacement take?",
         "a": "Most straight swaps are a one-day job. Adding or reworking ductwork, moving the indoor unit, or changing system type adds time. Sizing and pricing live on our <a href=\"/ac-installation\">AC installation</a> page."},
    ],
    # The copy on this page was rewritten 2026-08-02. shell.py prefers this stated date
    # over its content-hash ledger, so it must move only when the copy actually does.
    "updated": "August 2, 2026",
    "updatedISO": "2026-08-02",
    "rail": {
        # Was a hardcoded @main URL with a ?v=2 cache-buster — the query string does
        # nothing on jsDelivr; the commit pin is what actually busts the cache.
        # service/ac-repair.jpg was stock (and the same frame as service/maintenance.jpg);
        # this is a real Extreme diagnostic — gauges and meter on an open condenser.
        "photo": T.PHOTOS["acRepairGauges"],
        "photoPos": "50% 45%",
        "photoAlt": "Refrigerant gauges and a multimeter connected to an open air conditioner control panel during a service call",
        "promos": ["financing", "xplan"],
    },
    "related": [
        {"title": "Heat Pump Services", "href": "/heat-pump"},
        {"title": "Duct Cleaning", "href": "/duct-cleaning"},
        {"title": "Indoor Air Quality", "href": "/indoor-air-quality"},
    ],
    # pillNav is attached after `import rollout` below — the pill set lives there.
}
PAGES.append((os.path.join(HVAC, "air-conditioning.html"), T.detail_page, AIR_CONDITIONING, "xsp-air-conditioning"))

# ================================================================
# /services — mockup 2c (HVAC hub), copy verbatim
# ================================================================
HVAC_HUB = {
    "eyebrow": "OUR HVAC SERVICES",
    # /services and /plumbing/services were the only two non-top-level pages on the
    # site rendering no breadcrumb trail, so they were also the only two with no
    # BreadcrumbList in their schema (shell.py reads the rendered trail, it does not
    # invent one). The data is here now; hub_hero() still has to render it —
    # see handoff-build.md.
    "breadcrumb": [("Heating & Air", "")],
    "h1": "Every comfort system, {X}.",
    "h1Highlight": "one Extreme Team",
    # 30 words, second person. The licence number and job count moved to the footer
    # and the JSON-LD, where they belong — nothing is lost to a crawler.
    "answer": ("Heating, cooling and air quality for homes across Dayton and Cincinnati. We "
               "repair, replace and maintain every major brand, whoever installed it, and you "
               "agree the price before work starts."),
    "intro": "Heating, cooling, air quality, maintenance. Browse below, or just tell us what's wrong and we'll work out which one it is.",
    # Replaced ac-install.jpg: that photo's condenser carries a visible CARRIER badge,
    # so the HVAC hub was advertising a competitor's equipment. This is a real Ruud
    # unit from a job, badge legible, no service stickers in frame.
    "photo": T.PHOTOS["ruudHeatPump"],
    "photoPos": "50% 40%",
    "photoAlt": "A Ruud condenser installed at a Dayton-area home",
    "coreH2": "What do you need looked at?",
    "core": [
        {"title": "Air Conditioning", "desc": "AC repair, replacement, and tune-ups.", "href": "/air-conditioning"},
        {"title": "Furnace & Heating", "desc": "Furnace repairs, installs, and safety checks.", "href": "/furnace-heating"},
        {"title": "Heat Pump", "desc": "Heat and cooling from one system.", "href": "/heat-pump"},
        {"title": "Duct Cleaning", "desc": "Duct cleaning and air balancing.", "href": "/duct-cleaning"},
        {"title": "Indoor Air Quality", "desc": "Filtration, UV, and humidity control.", "href": "/indoor-air-quality"},
    ],
    "additionalLabel": "X-PLAN & ADDITIONAL SERVICES",
    "additional": [
        {"title": "Maintenance Plans", "badge": "X-PLAN", "desc": "Two tune-ups a year and priority service.", "href": "/maintenance"},
        {"title": "HVAC Inspections", "desc": "A full-system check, top to bottom.", "href": "/inspection"},
        {"title": "Thermostat Services", "desc": "Smart thermostat install and setup.", "href": "/thermostat"},
        {"title": "Humidifier Services", "desc": "Fixes dry air in winter.", "href": "/humidifier"},
    ],
    "panel": "xplan",
    "cross": [
        {"cls": "lav", "t": "Need to spread the cost?",
         "d": "Monthly payment plans on the bigger jobs.",
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
    # Same breadcrumb gap as the HVAC hub — see the note there.
    "breadcrumb": [("Plumbing", "")],
    "h1": "Licensed plumbers serving {X} homes.",
    "h1Highlight": "Dayton & Cincinnati",
    # 31 words, second person. The Ohio plumbing licence number is still the cheapest
    # checkable credibility signal this page has — it now sits in the footer and in
    # LocalBusiness.hasCredential rather than mid-paragraph. facts.md: OH LIC #13557.
    "answer": ("Drains, water heaters, sewer lines, sump pumps and gas lines, for homes "
               "across Dayton and Cincinnati. Licensed plumbers, a price you agree before "
               "work starts, and an emergency line answered 24/7."),
    "intro": "Same trucks, same phone number, same people you already call about the furnace.",
    # PLACEHOLDER: the slot wants a plumber on the job and no such photo exists yet
    # (Block A of the shot list). A real branded van beats an empty grey box until
    # then — swap it when the session delivers.
    "photo": T.PHOTOS["vans"],
    "photoAlt": "Extreme Heating, Air, Plumbing service vans leaving the Beavercreek shop at the start of a work day",
    "coreH2": "What plumbing work do you do?",
    "core": [
        {"title": "Clogged Drain", "desc": "Fast help for clogged and slow drains.", "href": "/plumbing/clogged-drain"},
        {"title": "Water Heater", "desc": "Repair, replacement, and tankless upgrades.", "href": "/plumbing/water-heater/overview"},
        {"title": "Sewer Line", "desc": "Inspection, repair, and cleaning.", "href": "/plumbing/sewer-line/overview"},
        {"title": "Sump Pump", "desc": "Keeps the basement dry.", "href": "/plumbing/sump-pump/overview"},
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
        {"cls": "lav", "t": "Need to spread the cost?",
         "d": "Monthly payment plans on the bigger jobs.",
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
    "h1": "Furnace repair in {X}, 24/7.",
    "h1Highlight": "Dayton & Cincinnati",
    # 39 words, second person. Someone reads this at 9pm on a phone with no heat, so it
    # leads with their problem and reaches the 24/7 line inside one short paragraph.
    # Licences, job count and the entity name live in the JSON-LD and the footer.
    "answer": ("No heat? We repair gas and electric furnaces across Dayton and Cincinnati, "
               "and no-heat calls go out ahead of everything else. You get a flat price "
               "before we start, a safety check after, and an emergency line answered 24/7."),
    "intro": "No heat is an emergency in an Ohio winter. We diagnose fast, price upfront, and repair every make and model — 24/7.",
    # Sub pages default to SUB_CHIPS, which says "4.9 on Google". The 1,595-review
    # figure is a Birdeye aggregate, so the source is named accurately here instead.
    "heroChips": ["4.9 from 1,595 reviews", "Locally Owned", "24/7 Emergency"],
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
        # [NEEDS: the gas utility 24-hour emergency numbers for the Dayton and the
        # Cincinnati service areas. keywords.md flags them as must-not-guess, so the
        # sentence says "the gas utility" until they are confirmed.]
        "callout": f'<b>Safety first:</b> smell gas or suspect carbon monoxide? Leave the house first. Call the gas utility from outside, then call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>. The emergency line is answered 24/7.',
    },
    # Diagnosis questions before Process, the decision and booking questions after it.
    "sections": [
        {"h2": "Why is my furnace blowing cold air?",
         "body": ("Cold air from a running furnace usually means the burners aren't lighting, "
                  "or they're shutting down early. Most often it's a dirty flame sensor, a "
                  "failed ignitor, a blocked condensate drain, or a thermostat left on Fan "
                  "instead of Auto."),
         "h3s": [
             {"h3": "The thermostat check that costs nothing",
              "body": ('A <a href="/thermostat">thermostat</a> set to Fan runs the blower '
                       "constantly whether the burners are lit or not, which feels exactly "
                       "like a furnace blowing cold air. Flip it to Auto first. That one "
                       "switch ends a fair number of no-heat calls before anyone gets "
                       "dispatched.")},
         ]},
        {"h2": "What can I check before calling for furnace repair?",
         "body": ("A few checks take five minutes and fix a real share of no-heat calls. If "
                  "none of them work, the fault is inside the furnace and needs a tech. None "
                  "of them involve opening the gas train or the burner compartment."),
         "h3s": [
             # Rendered as one paragraph with ticked lines rather than a <ul>: nothing
             # in the page CSS styles a list, and an unstyled <ul> in the main column
             # picks up browser defaults that match nothing else on the page.
             {"h3": "The five-minute checklist",
              "body": ["✓ Thermostat set to Heat, set above room temperature, and set to Auto rather than Fan"
                       "<br>✓ Thermostat batteries, if it takes them"
                       "<br>✓ The furnace breaker at the panel, and the switch on the furnace itself, which looks like a light switch and gets flipped by accident"
                       "<br>✓ The air filter, held up to a light. A filter that blocks light will shut a furnace down on a high-limit trip"
                       "<br>✓ Supply registers and return grilles open and unblocked by furniture or rugs",
                       "We give these away on purpose. Someone who fixes their own no-heat "
                       "call in five minutes tends to call us when the next one isn't so "
                       "simple."]},
         ]},
        {"eyebrow": "TRIAGE",
         "id": "emergency-or-wait",
         "h2": "Is this a 24/7 emergency or can it wait?",
         "body": ["Some furnace symptoms are a safety problem and some are a scheduling "
                  "problem. A gas smell, a carbon monoxide alarm going off, and no heat "
                  "below freezing are the three that should never wait for morning.",
                  'If the house heats with a heat pump rather than a furnace, the symptoms '
                  'read differently — <a href="/heat-pump-repair">heat pump repair</a> covers '
                  'what each one usually means.'],
         "table": {
             "caption": "Furnace symptoms: what needs a 24/7 call and what can wait",
             "takeaway": ("A gas smell, a carbon monoxide alarm going off, and no heat below "
                          "freezing are 24/7 calls. Most of what's left on this list can "
                          "wait for business hours."),
             "columns": ["What you are seeing", "Call 24/7 now",
                         "Can wait for business hours"],
             "rows": [
                 ["Gas smell anywhere in the house",
                  "Yes. Leave the house first, then call from outside", "No"],
                 ["Carbon monoxide alarm sounding",
                  "Yes. Leave the house, call 911, then call for service", "No"],
                 ["No heat with outdoor temperatures below freezing", "Yes", "No"],
                 ["Yellow or flickering burner flame",
                  "Yes. Switch the furnace off first", "No"],
                 ["Water pooling at the base of a high-efficiency furnace",
                  "Yes, if the furnace has shut down", "Yes, if the furnace is still running"],
                 ["Furnace short cycling while the house stays warm", "No",
                  "Yes, book the next business day"],
                 ["Burning smell in the first hour of the heating season", "No",
                  "Yes, if it clears within an hour"],
                 ["Rattle or squeal with the heat still working", "No", "Yes"],
                 ["Heating bill climbing with no change in comfort", "No", "Yes"],
             ],
         }},
    ],
    "process": {
        "h2": "A repair visit without surprises.",
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or book online. No-heat calls get priority, and most are same day."},
            {"title": "Diagnose & quote upfront",
             "desc": "We test the system, tell you what failed, and price the fix before anything starts."},
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
    # The decision card asks the repair-or-replace question; the table two blocks below
    # answers it. Both stay on this page rather than on /furnace-heating — see the
    # cannibalization note in handoff-build.md.
    "sectionsTail": [
        {"h2": "What does a furnace repair visit include?",
         "body": ("Your tech finds the failure, explains it in plain terms, and prices the "
                  "repair before touching it. Every visit ends with a safety check — heat "
                  "exchanger, venting and carbon monoxide readings — whether or not that was "
                  "what you called about.")},
        {"eyebrow": "DECIDING",
         "id": "repair-or-replace",
         "h2": "Should I repair or replace my furnace?",
         "body": ("Two things settle it: how old the furnace is, and what a combustion safety "
                  "check finds at the heat exchanger. Under 15 with an intact exchanger, "
                  "repair usually wins. A cracked heat exchanger is never repaired, so at "
                  'that age the <a href="/furnace-installation">replacement</a> is the whole '
                  "unit."),
         "table": {
             "caption": "Repair or replace a furnace: what decides it",
             "takeaway": ("Once a furnace is 15 or older and the repair quote is closing in "
                          "on a third of replacement cost, we'll tell you to replace it."),
             "columns": ["What we look at", "Repair when",
                         "Replace when"],
             "rows": [
                 ["System age", "Under 15 years old", "15 years or older"],
                 ["Heat exchanger", "Intact and passing a combustion safety check",
                  "Cracked. A cracked heat exchanger is replaced, never repaired"],
                 ["Repair cost", "Well below a third of replacement cost",
                  "At or above roughly a third of replacement cost"],
                 ["Breakdown history", "First failure in several seasons",
                  "Second or third no-heat call in one winter"],
                 ["Efficiency", "Furnace is 90% AFUE or higher",
                  "Furnace is an older 60% to 70% AFUE model"],
                 ["Parts", "Still available and inside the manufacturer warranty",
                  "Obsolete, or out of warranty on parts and labor"],
                 ["Comfort", "One room or one symptom affected",
                  "Uneven heat throughout the house"],
             ],
         }},
        {"h2": "How do I book furnace repair?",
         "body": (f'Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> or book online. The '
                  "emergency line runs 24/7, every day of the year, and we send no-heat calls "
                  "out ahead of routine work. The office is staffed Monday to Friday, 8:00 AM "
                  "to 5:00 PM.")},
    ],
    "faqEyebrow": "FURNACE QUESTIONS",
    "faqH2": "What should I know before booking furnace repair?",
    "faq": [
        {"q": "Do you repair furnaces at night and on weekends?",
         "a": "Yes. The emergency line runs 24/7 across the Dayton and Cincinnati metros, every day of the year. In freezing weather we send no-heat calls out ahead of routine work."},
        {"q": "Do you repair all furnace brands?",
         "a": "Yes. Gas, electric and high-efficiency furnaces from every major manufacturer, whoever installed the system."},
        {"q": "Is a yellow pilot flame dangerous?",
         "a": "It can be. A healthy burner flame burns blue. Yellow or flickering can mean incomplete combustion, which produces carbon monoxide. Shut the furnace off and have it checked before you run it again."},
        {"q": "My furnace turns on and off every few minutes. What causes that?",
         "a": "That's short cycling. Usually a clogged air filter, a blocked return, a failing flame sensor, or a furnace that's oversized for the house. The filter is the one you can rule out in a minute."},
        {"q": "Water is pooling under my furnace. Is that normal?",
         "a": "Not normal, but common on high-efficiency condensing furnaces. They produce condensate, and a blocked drain line or a failed pump puts that water on the floor — usually tripping a safety switch and shutting the furnace down."},
        {"q": "Can I keep running a furnace with a cracked heat exchanger?",
         "a": "No. A crack can put combustion gases, including carbon monoxide, into the air your house breathes. A <a href=\"/inspection\">combustion safety check</a> is what confirms it, and the furnace should stay off until that's done. A cracked exchanger gets replaced, not repaired."},
    ],
    # Copy rewritten 2026-08-02. Move this only when the copy moves.
    "updated": "August 2, 2026",
    "updatedISO": "2026-08-02",
    "bookingCard": {
        "eyebrow": "BOOK FURNACE REPAIR",
        "title": "No heat? We're on it.",
        "sub": "Priority dispatch for no-heat calls.",
        "trust2": "24/7 emergency",
    },
    "rail": {
        "promos": ["xplanSub"],
        # Set here, not in PHOTO_OVERRIDES: this page is appended to PAGES directly
        # rather than through _wire_image(), so an override entry for it would never
        # be read. The stock frame it used to carry is replaced by a real job photo.
        "photo": T.PHOTOS["furnaceRepairOpen"],
        "photoPos": "50% 60%",
        "photoAlt": "An older gas furnace opened up during a repair call, burner compartment and flame sensor exposed",
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
    "intro": "Repair, replacement, and tankless upgrades for every water heater — from the same people who handle your heating and air.",
    # "4.9 on Google" was wrong here the same way it was wrong on the two pages above:
    # the 1,595-review figure is a Birdeye aggregate pooling several platforms, so it
    # cannot be attributed to Google. facts.md confirms 4.9 / 1,595 for display.
    "heroChips": ["4.9 from 1,595 reviews", "Same-Day Replacement", "Licensed Plumbers"],
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
             "desc": "Right-sized tanks, installed clean — often the same day, with financing if you need it.",
             "href": "/plumbing/water-heater/installation"},
            {"title": "Tankless Water Heaters",
             "desc": "Hot water that doesn't run out, and a lower bill — we'll tell you straight if it suits your house.",
             "href": "/plumbing/water-heater/installation"},
        ],
    },
    "process": {
        "steps": [
            {"title": "Book in minutes",
             "desc": "Call or book online. No-hot-water calls get priority dispatch."},
            {"title": "Diagnose & quote upfront",
             "desc": "Repair or replace, laid out straight, with a flat price you approve first."},
            {"title": "Hot water, guaranteed",
             "desc": "Installed to code, tested at every tap, and the old unit hauled away."},
        ],
    },
    "faqEyebrow": "WATER HEATER QUESTIONS",
    "faq": [
        {"q": "Can you replace my water heater the same day?",
         "a": "Usually, yes. We stock the common tank sizes, so most replacements go in the same day — you're not waiting a week for hot water."},
        {"q": "Tank or tankless — which is right for my home?",
         "a": "Tanks cost less upfront and suit most homes. Tankless costs more to install but gives you hot water that doesn't run out and a lower energy bill. We'll walk you through both and let you decide."},
        {"q": "How long do water heaters last?",
         "a": "Tank units usually last 8–12 years; tankless can reach 20 with maintenance. Past ten years, replacing beats a major repair most of the time."},
        {"q": "What size water heater do I need?",
         "a": "Depends on the household — a family of four usually needs 40 to 50 gallons. We size it to how much hot water you actually use, not a guess."},
    ],
    "rail": {
        # Carried over from the old page (hotlinked stock preview) — replace
        # with a licensed copy in this repo's assets/ folder when available.
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

# The AC overview is authored above, before rollout is imported, so its pill nav is
# attached here — same Overview / Installation / Repair bar the furnace and heat
# pump families carry. PAGES holds the dict by reference, so this still lands.
AIR_CONDITIONING["pillNav"] = rollout.pillset("AIR CONDITIONING", rollout.AC_PILLS, "Overview")

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
    "intro": "X-Plan is our maintenance membership, and it pays you back. Every dollar you spend on it in consecutive years goes toward replacing your system at the end of its life — up to $2,500 or 10 years. Plus two visits a year, 15% off repairs, and priority scheduling.",
    "heroChips": ["2 Tune-Ups a Year", "15% Off Repairs", "Priority Scheduling"],
    "benefits": {
        "h2": "One membership, six ways it pays off.",
        "cards": [
            {"t": "100% back toward your next system",
             "d": "Every dollar you pay in consecutive years goes toward end-of-life equipment replacement — up to $2,500 or 10 years, whichever comes first."},
            {"t": "Two seasonal tune-ups a year",
             "d": "AC in spring, furnace in fall — we call you to schedule, not the other way around."},
            {"t": "15% off every repair",
             "d": "HVAC and plumbing alike — member pricing, applied automatically."},
            {"t": "Priority scheduling",
             "d": "You go to the front of the line, even in peak season."},
            {"t": "5-year warranty on repairs",
             "d": "Five times the standard coverage on parts and labor we install."},
            {"t": "Discounted service calls",
             "d": "$77 instead of $97 during business hours — $177 instead of $197 for emergencies."},
        ],
    },
    "useCases": {
        "h2": "Made for people who'd rather not think about it.",
        "cards": [
            {"t": "Your system is 5+ years old",
             "d": "This is when small issues start compounding. Two checks a year catch them while they're still cheap."},
            {"t": "You just bought a new system",
             "d": "Manufacturer warranties want documented annual maintenance — this keeps you covered without the calendar reminders."},
            {"t": "You've had a surprise breakdown before",
             "d": "The worst repairs happen on the worst days. Priority scheduling and a cheaper service call take the sting out."},
        ],
    },
    "value": {
        "h2": "Most members come out ahead in year one.",
        "stats": [
            {"n": "2×", "cap": "tune-ups included — booked separately they'd cost more than the membership."},
            {"n": "15%", "cap": "off one mid-size repair usually covers the rest."},
            {"n": "$20", "cap": "off every service call, emergencies included, when the timing is worst."},
        ],
    },
    "process": {
        "h2": "Join once. We handle the rest.",
        "steps": [
            {"title": "Join online or by phone",
             "desc": "Pick yearly or monthly billing, and we'll set you up on the spot."},
            {"title": "We schedule your tune-ups",
             "desc": "We reach out each spring and fall and book around your calendar."},
            {"title": "You save automatically",
             "desc": "Member pricing, priority dispatch and the 5-year repair warranty apply from day one."},
        ],
    },
    "faqEyebrow": "X-PLAN QUESTIONS",
    "faq": [
        {"q": "How does the Zero Risk Investment work?",
         "a": "Everything you pay for X-Plan in consecutive years goes toward replacing your equipment at the end of its life — up to $2,500 or 10 years, whichever comes first. The years have to be consecutive, and the credit follows you, not the house."},
        {"q": "What happens if I let my membership lapse?",
         "a": "The Zero Risk Investment builds on consecutive years, so a gap interrupts it. If you're thinking about pausing, call us first and we'll walk through what it does to your balance."},
        {"q": "Does the 15% discount cover plumbing repairs too?",
         "a": "Yes — member pricing applies to HVAC and plumbing repairs alike, automatically."},
        {"q": "What happens at a tune-up visit?",
         "a": "A full system inspection and safety check: capacitor, relay and thermostat testing, compressor amp draws, drain line cleaning, a pressure check, and light coil cleaning."},
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
    # service/furnace-repair.jpg is stock (a technician in an unbranded blue shirt).
    # This is a real Extreme job. (/furnace-repair gets its own photo inline above —
    # that page never passes through _wire_image.)
    "HVAC Service Pages/furnace-heating.html": {
        "photo": T.PHOTOS["furnaceService"],
        "photoPos": "50% 45%",
        "photoAlt": "A Trane furnace in a basement with its control panel open for service",
    },
}

# Alt text for the rail photos, keyed by a distinctive piece of the image URL.
# rollout.py's detail()/sub() take a photo but never took an alt, so every page that
# got its image this way rendered alt="" — 25 pages whose lead content photo said
# nothing at all to a screen reader. Each line below was written after looking at the
# actual image, except where noted, where the stock title in the URL is the
# photographer's own description and the subject is unambiguous.
IMAGE_ALTS = {
    # Extreme's own photography
    "duct-cleaning-truck.jpg": "The Extreme air duct cleaning truck parked outside a home",
    "muv-401h.jpg": "A PremierOne MUV-401H UV air purifier with its lamp lit",
    # Licensed/carried-over stock — described from the image, not the page topic
    "furnace-repair.jpg": "A technician working inside an open gas furnace",
    "humidifier.jpg": "A whole-home humidifier and furnace in a basement utility area",
    "dirty-duct.jpg": "The inside of an air duct heavily coated with dust",
    "air-quality.jpg": ("Breakdown of indoor air pollutants: 35% particulate, "
                        "34% bioaerosols, 31% volatile organic compounds"),
    "sale.jpg": "A for-sale sign in the front yard of a two-storey house",
    "smart-thermostat.jpg": "A smart thermostat set from a phone app",
    "a-pipe-clogged": "Two cut sections of drain pipe, both clogged solid with grease",
    "worried-man-calling-plumber": "A man phoning for help under a leaking sink",
    "repairing-a-broken-pipe": "Gloved hands joining a broken pipe in a muddy trench",
    "backup-sump-pump": "A sump pump and float switch in a basement pit",
    "360_F_53961667": "A technician adjusting the thermostat dial on a water heater",
    "360_F_632498826": "A technician working on the valves of a wall-mounted water heater",
    "360_F_507146518": "A plumber installing an under-sink water filtration system",
    # From the stock title in the URL; subject unambiguous, image not opened
    "ceiling-with-multiple-utility-lines": "Gas, water and electrical lines running along a basement ceiling",
    "male-engineer-checking-boiler-system": "A technician checking a boiler system in a basement",
    "home-inspector-use-thermal-imager": "An inspector scanning for leaks with a thermal imaging camera",
    "pumping-out-household-septic-tank": "A septic tank being pumped out",
    "a-plumber-repairing-a-sump-pump": "A plumber repairing a sump pump in a flooded basement",
    "man-plumber-in-uniform-installing-toilet-bowl": "A plumber installing a toilet",
}

def _alt_for(url):
    for key, alt in IMAGE_ALTS.items():
        if key in url:
            return alt
    return None

def _wire_image(data, rel):
    """Attach the page's own legacy image (CDN or carried-over stock), with alt text."""
    override = PHOTO_OVERRIDES.get(rel)
    if override:
        data["rail"].update(override)
        return data
    img = old_img(rel)
    if img and "Logo" not in img:
        data["rail"]["photo"] = img
        alt = _alt_for(img)
        if alt and not data["rail"].get("photoAlt"):
            data["rail"]["photoAlt"] = alt
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

# ---------------- Location pages (5h, 5a-5g) — pages/locations/ ----------------
# 267 pages from one template: the hub, 38 city overviews, and 6 service pages each.
import location_pages
PAGES.extend(location_pages.pages(ROOT))

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
