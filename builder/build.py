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
    # The answer-first block. Entity, both metros and two stat tokens in 48 words, no
    # first person and no rates — this is the passage an engine lifts, so nothing in
    # it may need the rest of the page for context.
    "answer": ("Extreme Heating, Air, Plumbing repairs, replaces and tunes up residential "
               "air conditioners across the Dayton and Cincinnati, Ohio metros. Central air "
               "systems and heat pumps in cooling mode are covered on every major brand, "
               "whoever installed them. The company has completed 25,000+ jobs and offers "
               "90% same-day service."),
    "intro": "Repairs, replacements and tune-ups from the locally owned Extreme Team. Upfront pricing, clean workmanship, and cool air back fast.",
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
        "h2": "What are the signs an air conditioner is failing?",
        "items": [
            "Blowing warm or room-temp air",
            "Weak airflow in some rooms",
            "Turning on and off every few minutes",
            "Grinding, squealing, or rattling",
            "Water or refrigerant leaks",
            "Energy bills creeping up",
        ],
        "callout": f'Noticing more than one? Small AC problems become compressor problems. Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> before it gets expensive, or read what each symptom usually means on our <a href="/ac-repair">AC repair</a> page.',
    },
    "whatWeDo": {
        "h2": "What air conditioning services does Extreme offer in Dayton and Cincinnati?",
        "cards": [
            {"title": "AC Repair",
             "desc": "Same-day diagnostics and honest repair options for every make and model — approved by you before we start.",
             "href": "/ac-repair"},
            {"title": "AC Installation & Replacement",
             "desc": "Right-sized, high-efficiency systems installed clean — with flexible financing options.",
             "href": "/ac-installation"},
            {"title": "AC Tune-Ups & Maintenance",
             "desc": "Seasonal tune-ups that catch small issues early — included twice a year with X-Plan.",
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
                  "failed capacitor or contactor is a repair. An older system facing a "
                  "compressor or coil replacement is usually the point where a new unit "
                  "costs less over the years it has left."),
         # No dollar figures anywhere in this table, by design: the one-third rule of
         # thumb is client-approved, a published repair price is not.
         "table": {
             "caption": "Repair or replace an air conditioner: what Extreme Heating, Air, Plumbing weighs on a Dayton or Cincinnati service call.",
             "takeaway": ("Extreme Heating, Air, Plumbing recommends replacement over repair "
                          "when an air conditioner is past its expected service life and the "
                          "repair quote approaches a third of replacement cost."),
             "columns": ["Factor", "Repair usually makes sense when",
                         "Replacement usually makes sense when"],
             "rows": [
                 ["System age", "The air conditioner is under 10 years old",
                  "The air conditioner is past 12 to 15 years"],
                 ["Repair cost", "The quote is well under a third of replacement cost",
                  "The quote is at or above roughly a third of replacement cost"],
                 ["Breakdown history", "This is the first failure in several cooling seasons",
                  "This is the second or third service call in one season"],
                 ["Refrigerant", "The system uses a refrigerant still in production",
                  "The system uses R-22, which has not been produced or imported in the US since 2020"],
                 ["Energy bills", "Cooling bills are steady year over year",
                  "Cooling bills climb with no change in how the house is used"],
                 ["Comfort", "One room or one symptom is affected",
                  "Temperatures are uneven throughout the house"],
                 # Deliverable wrote "labour"; the rest of the site is US spelling.
                 ["Warranty", "Parts are still under manufacturer warranty",
                  "Parts and labor warranties have both run out"],
             ],
         }},
        {"h2": "How long does a central air conditioner last?",
         "body": ("Twelve to fifteen years is the normal working life for a central air "
                  "conditioner in this climate, and a maintained system reaches the top of "
                  "that range more often than a neglected one. Past fifteen, most homeowners "
                  "spend more on repairs than a replacement would have cost.")},
        {"h2": "Which air conditioner brands does Extreme service?",
         "body": ("Every major residential make and model, regardless of who installed them. "
                  "Our techs train across the systems common in Dayton and Cincinnati "
                  "housing, so a warranty repair on one brand and a twenty-year-old unit "
                  "from another brand both get handled.")},
    ],
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
    "sectionsTail": [
        {"h2": "How often should an air conditioner be serviced?",
         "body": ("Once a year, in spring, before the first stretch of ninety-degree weather. "
                  "A tune-up cleans the coil, checks refrigerant charge and tests the "
                  "electrical parts that fail first in heat. "
                  '<a href="/maintenance">X-Plan</a> members get two visits a year, one for '
                  "cooling and one for heating.")},
        {"h2": "How do I book AC service in Dayton or Cincinnati?",
         "body": (f'Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> or schedule online, and '
                  "you get an arrival window before the tech leaves the shop. Extreme "
                  "Heating, Air, Plumbing handles about 90% of service calls the same day, "
                  "with 24/7 emergency service when a house has no cooling in a heat wave.")},
    ],
    "faqEyebrow": "AC QUESTIONS",
    "faqH2": "What do homeowners ask before booking AC service?",
    "faq": [
        {"q": "Is it worth replacing an R-22 air conditioner?",
         "a": "Usually yes. R-22 has not been produced or imported in the United States since 2020, so a system that needs a recharge is paying for a shrinking reclaimed supply. If an R-22 unit needs a compressor or a coil, replacement almost always costs less over the years left in it."},
        {"q": "Can the air conditioner be replaced without replacing the furnace?",
         "a": "Yes, and often it should be. The indoor coil has to be matched to the new outdoor unit, so the furnace gets opened up either way. If the furnace is also near the end of its life, replacing both in one visit costs less than two separate jobs a few years apart."},
        {"q": "Do you offer emergency AC repair?",
         "a": "Yes. Extreme Heating, Air, Plumbing runs 24/7 emergency service across the Dayton and Cincinnati metros, every day of the year. Office phones are staffed Monday to Friday, 8:00 AM to 5:00 PM, and the emergency line never closes."},
        {"q": "Does X-Plan cover the air conditioner?",
         "a": "Yes. X-Plan includes two seasonal safety and performance visits a year, one of them a multi-point air conditioner tune-up with refrigerant charge calibration up to 1 lb included. Members also get 15% off all repairs and priority scheduling."},
        {"q": "How long does an air conditioner replacement take?",
         "a": "Most straight-swap replacements are a one-day job. Adding or reworking ductwork, moving the indoor unit, or changing system type adds time. Sizing and pricing for a replacement live on our <a href=\"/ac-installation\">AC installation</a> page."},
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
    # 47 words, three sentences, entity and both metros present, no first person.
    "answer": ("Extreme Heating, Air, Plumbing repairs, replaces and maintains residential "
               "heating, cooling and indoor air quality systems across the Dayton and "
               "Cincinnati, Ohio metros. Every major brand is covered, whoever installed it, "
               "under Ohio HVAC license #37179. The company has completed 25,000+ jobs since "
               "2004."),
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
    # Same breadcrumb gap as the HVAC hub — see the note there.
    "breadcrumb": [("Plumbing", "")],
    "h1": "Licensed plumbers serving {X} homes.",
    "h1Highlight": "Dayton & Cincinnati",
    # 49 words, three sentences. The Ohio plumbing licence number is the cheapest
    # checkable credibility signal a plumbing page has, and checkable is what makes a
    # passage citable. facts.md confirms OH LIC #13557.
    "answer": ("Extreme Heating, Air, Plumbing provides residential plumbing service across "
               "38 communities in the Dayton and Cincinnati, Ohio metros. Coverage includes "
               "drains, water heaters, sewer lines, sump pumps and gas lines, all performed "
               "under Ohio plumbing license #13557. The company offers 24/7 emergency "
               "service and 90% same-day service."),
    "intro": "Same trucks, same phone number, same people you already call about the furnace.",
    # PLACEHOLDER: the slot wants a plumber on the job and no such photo exists yet
    # (Block A of the shot list). A real branded van beats an empty grey box until
    # then — swap it when the session delivers.
    "photo": T.PHOTOS["vans"],
    "photoAlt": "Extreme Heating, Air, Plumbing service vans leaving the Beavercreek shop at the start of a work day",
    "coreH2": "What plumbing services does Extreme offer in Dayton and Cincinnati?",
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
    "h1": "Furnace repair in {X}, 24/7.",
    "h1Highlight": "Dayton & Cincinnati",
    # 55 words, four sentences. Both metros, the entity, and three approved stat
    # tokens; no first person, no rates, no response-time promise beyond the tokens.
    "answer": ("Extreme Heating, Air, Plumbing repairs gas and electric furnaces across the "
               "Dayton and Cincinnati, Ohio metros. No-heat calls are prioritized, and every "
               "repair is quoted flat before work begins and safety-checked afterward. The "
               "company offers 24/7 emergency service and 90% same-day service. Licensed and "
               "insured technicians handle every call, and 25,000+ jobs have been completed."),
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
         "body": ("Cold air from a running furnace usually means the burners are not lighting "
                  "or are shutting down early. The most common causes are a dirty flame "
                  "sensor, a failed ignitor, a blocked condensate drain on a high-efficiency "
                  "unit, or a thermostat left on Fan rather than Auto."),
         "h3s": [
             {"h3": "The thermostat check that costs nothing",
              "body": ('A <a href="/thermostat">thermostat</a> set to Fan runs the blower '
                       "constantly, whether the burners are lit or not, which feels exactly "
                       "like a furnace blowing cold air. Set it to Auto first. That single "
                       "switch ends a fair number of no-heat calls before anyone is "
                       "dispatched.")},
         ]},
        {"h2": "What can I check before calling for furnace repair?",
         "body": ("A handful of checks take about five minutes and fix a real share of "
                  "no-heat calls. If none of them work, the fault is inside the furnace and "
                  "needs a technician. None of them involve opening the gas train or the "
                  "burner compartment."),
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
                       "These are given away on purpose. Someone who fixes their own no-heat "
                       "call in five minutes tends to call Extreme Heating, Air, Plumbing "
                       "when the next one is not so simple."]},
         ]},
        {"eyebrow": "TRIAGE",
         "id": "emergency-or-wait",
         "h2": "Is this a 24/7 emergency or can it wait?",
         "body": ["Some furnace symptoms are a safety problem and some are a scheduling "
                  "problem. Gas smell, a sounding carbon monoxide alarm, and no heat with "
                  "outdoor temperatures below freezing are the three that should never wait "
                  "for morning.",
                  'If the house heats with a heat pump rather than a furnace, the symptoms '
                  'read differently — <a href="/heat-pump-repair">heat pump repair</a> covers '
                  'what each one usually means.'],
         "table": {
             "caption": "Furnace symptoms: what needs a 24/7 call and what can wait",
             "takeaway": ("Extreme Heating, Air, Plumbing treats a gas smell, a sounding "
                          "carbon monoxide alarm, and no heat below freezing as 24/7 "
                          "emergencies across the Dayton and Cincinnati metros."),
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
    # The decision card asks the repair-or-replace question; the table two blocks below
    # answers it. Both stay on this page rather than on /furnace-heating — see the
    # cannibalization note in handoff-build.md.
    "sectionsTail": [
        {"h2": "What does a furnace repair visit include?",
         "body": ("A technician diagnoses the failure, explains what failed in plain terms, "
                  "and prices the repair before touching it. Every repair ends with a full "
                  "safety check covering the heat exchanger, the venting, and carbon monoxide "
                  "readings, whether or not the original complaint was safety-related.")},
        {"eyebrow": "DECIDING",
         "id": "repair-or-replace",
         "h2": "Should I repair or replace my furnace?",
         "body": ("Two things settle it: how old the furnace is, and what a combustion safety "
                  "check finds at the heat exchanger. Under 15 years old with an intact heat "
                  "exchanger, repair usually wins. A cracked heat exchanger is never "
                  'repaired, and on a furnace of that age the <a href="/furnace-installation">'
                  "replacement</a> is the whole unit."),
         "table": {
             "caption": "Repair or replace a furnace: what decides it",
             "takeaway": ("Extreme Heating, Air, Plumbing replaces rather than repairs a "
                          "furnace once it is 15 years or older and the repair quote "
                          "approaches a third of replacement cost."),
             "columns": ["Factor", "Repair usually makes sense when",
                         "Replacement usually makes sense when"],
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
        {"h2": "How do I book furnace repair in Dayton or Cincinnati?",
         "body": (f'Furnace repair is booked by phone at <a href="{T.PHONE_TEL}">'
                  f'{T.PHONE_DISPLAY}</a> or online. The emergency line runs 24/7, every day '
                  "of the year, and no-heat calls are dispatched ahead of routine work. The "
                  "office is staffed Monday to Friday, 8:00 AM to 5:00 PM.")},
    ],
    "faqEyebrow": "FURNACE QUESTIONS",
    "faqH2": "What do homeowners ask before booking furnace repair?",
    "faq": [
        {"q": "Do you repair furnaces at night and on weekends?",
         "a": "Yes. Extreme Heating, Air, Plumbing runs 24/7 emergency service every day of the year across the Dayton and Cincinnati metros. No-heat calls in freezing weather are dispatched ahead of routine work."},
        {"q": "Do you repair all furnace brands?",
         "a": "Yes. Gas, electric, and high-efficiency furnaces from every major manufacturer, regardless of who installed the system."},
        {"q": "Is a yellow pilot flame dangerous?",
         "a": "It can be. A healthy burner flame burns blue. Yellow or flickering can signal incomplete combustion, which produces carbon monoxide. Switch the furnace off and have it checked before running it again."},
        {"q": "My furnace turns on and off every few minutes. What causes that?",
         "a": "Short cycling. The most common causes are a clogged air filter, a blocked return, a failing flame sensor, or a furnace that is oversized for the house. A clogged filter is the one a homeowner can rule out in a minute."},
        {"q": "Water is pooling under my furnace. Is that normal?",
         "a": "Not normal, but common on high-efficiency condensing furnaces. Those units produce condensate, and a blocked drain line or a failed condensate pump puts that water on the floor and usually shuts the furnace down on a safety switch."},
        {"q": "Can I keep running a furnace with a cracked heat exchanger?",
         "a": "No. A cracked heat exchanger can put combustion gases, including carbon monoxide, into the air the house breathes. A <a href=\"/inspection\">combustion safety check</a> is what confirms a crack, and the furnace should be shut off until it has been done. A cracked exchanger is replaced rather than repaired."},
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
