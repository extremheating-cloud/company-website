"""Step-5 rollout — remaining pages as data objects (README copy formulas)."""
import template as T
import site_data as D

TEL, PH = T.PHONE_TEL, T.PHONE_DISPLAY

def call(text):
    return text.replace("{tel}", f'<a href="{TEL}">{PH}</a>')

STEP1 = {"title": "Book in minutes", "desc": "Call or schedule online — we confirm your arrival window fast, with same-day service in most cases."}
STEP2 = {"title": "Diagnose & quote upfront", "desc": "We walk you through what's wrong and your options — flat, upfront pricing you approve first."}

def steps(last_title, last_desc, step1=None, step2=None):
    return {"steps": [step1 or STEP1, step2 or STEP2, {"title": last_title, "desc": last_desc}]}

def detail(slug, crumb_parent, name, h1, hl, intro, chips, book_eyebrow, book_title,
           sym_eyebrow, sym_h2, symptoms, callout, wwd_h2, cards, process_,
           faq_eyebrow, faqs, related, img=None, pills=None, promos=None, safety=False):
    d = {
        "breadcrumb": [crumb_parent, (name, "")],
        "h1": h1, "h1Highlight": hl, "intro": intro, "heroChips": chips,
        "bookingCard": {"eyebrow": book_eyebrow, "title": book_title,
                        "sub": "Upfront pricing before any work begins."},
        "symptoms": {"eyebrow": sym_eyebrow, "h2": sym_h2, "items": symptoms,
                     "callout": call(callout), "safety": safety},
        "whatWeDo": {"h2": wwd_h2, "cards": cards} if cards else None,
        "process": process_, "faqEyebrow": faq_eyebrow, "faq": faqs,
        "rail": {"photo": img, "photoSlot": True, "photoLabel": "PHOTO — TECH ON THE JOB",
                 "promos": promos or ["financing", "xplan"]},
        "related": related,
    }
    if pills:
        d["pillNav"] = pills
    if not cards:
        d.pop("whatWeDo")
    return d

def sub(crumbs, h1, hl, intro, pills, sym_eyebrow, sym_h2, symptoms, callout,
        process_, decision, faq_eyebrow, faqs, book_eyebrow, book_title, book_sub,
        sib_label, sibs, img=None, alt=None, imgPos=None, safety=False,
        schedule_label="Schedule Service", promo="xplanSub", trust2="20+ years local"):
    return {
        "breadcrumb": crumbs, "h1": h1, "h1Highlight": hl, "intro": intro,
        "scheduleLabel": schedule_label,
        "pillNav": pills,
        "symptoms": {"eyebrow": sym_eyebrow, "h2": sym_h2, "items": symptoms,
                     "callout": call(callout), "safety": safety},
        "process": process_, "decision": decision,
        "faqEyebrow": faq_eyebrow, "faq": faqs,
        "bookingCard": {"eyebrow": book_eyebrow, "title": book_title, "sub": book_sub, "trust2": trust2},
        "rail": {"promos": [promo], "photo": img, "photoAlt": alt, "photoPos": imgPos},
        "siblings": {"label": sib_label, "items": sibs},
    }

def pillset(label, items, active):
    return {"label": label, "items": [
        {"label": l, "href": h, "active": l == active} for l, h in items]}

FURN_PILLS = [("Overview", "/furnace-heating"), ("Installation", "/furnace-installation"), ("Repair", "/furnace-repair")]
AC_PILLS = [("Overview", "/air-conditioning"), ("Installation", "/ac-installation"), ("Repair", "/ac-repair")]
HP_PILLS = [("Overview", "/heat-pump"), ("Installation", "/heat-pump-installation"), ("Repair", "/heat-pump-repair")]
IAQ_PILLS = [("Overview", "/indoor-air-quality"), ("Solutions", "/indoor-air-quality-solutions"),
             ("Importance", "/importance-iaq"), ("FAQ", "/iaq-faq")]
WH_PILLS = [("Overview", "/plumbing/water-heater/overview"), ("Repair", "/plumbing/water-heater/repair"), ("Installation", "/plumbing/water-heater/installation")]
SEW_PILLS = [("Overview", "/plumbing/sewer-line/overview"), ("Repair", "/plumbing/sewer-line/repair"), ("Cleaning", "/plumbing/sewer-line/cleaning")]
SUMP_PILLS = [("Overview", "/plumbing/sump-pump/overview"), ("Repair", "/plumbing/sump-pump/repair"), ("Installation", "/plumbing/sump-pump/installation")]
GAS_PILLS = [("Overview", "/plumbing/gas-line/overview"), ("Repair", "/plumbing/gas-line/repair"), ("Installation", "/plumbing/gas-line/installation")]

HVAC_CRUMB = ("Heating & Air", "/services")
PLUMB_CRUMB = ("Plumbing", "/plumbing/services")

SPEED_FAQ = {"q": "How fast can you get here?",
    "a": "In most cases, same day — about 90% of our calls are handled the day you reach out, with 24/7 emergency service when it can't wait."}
BRANDS_FAQ = {"q": "Do you service all brands?",
    "a": "Yes — every major make and model, regardless of who installed it."}

# ======================================================================
# HVAC details
# ======================================================================
HVAC_PAGES = {}

HVAC_PAGES["furnace-heating.html"] = detail(
    "furnace-heating", HVAC_CRUMB, "Furnace & Heating",
    "Reliable heat, {X}.", "all winter long",
    "Furnace repairs, installations, and safety checks from the locally owned Extreme Team — upfront pricing and warm air back fast.",
    ["4.9 on Google", "90% Same-Day Service", "24/7 Emergency"],
    "BOOK HEATING SERVICE", "Get a tech to your door.",
    "FURNACE TROUBLE?", "Signs it's time to call.",
    ["Blowing cold or lukewarm air", "Short cycling on and off", "Yellow or flickering burner flame",
     "Burning or musty smells", "Banging or scraping sounds", "Heating bills creeping up"],
    "<b>Safety first:</b> smell gas or suspect carbon monoxide? Leave the house first, then call {tel} — 24/7.",
    "Repair, replace, or maintain — we handle it all.",
    [{"title": "Furnace Repair", "desc": "Fast diagnosis and honest repair options for every make and model — 24/7 for no-heat calls.", "href": "/furnace-repair"},
     {"title": "Furnace Installation", "desc": "Right-sized, high-efficiency furnaces installed clean — with flexible financing options.", "href": "/furnace-installation"},
     {"title": "Heating Tune-Ups", "desc": "Seasonal safety checks that catch small issues early — included twice a year with X-Plan.", "href": "/maintenance"}],
    steps("Fixed right, safety-checked", "Every visit ends with a full safety check — heat exchanger, venting, and CO included."),
    "HEATING QUESTIONS",
    [SPEED_FAQ,
     {"q": "Should I repair or replace my furnace?",
      "a": "Under 12 years old with a minor issue, repair usually wins. Past 15 years with a major failure, replacement often costs less over time. We'll give you both numbers — no pressure."},
     BRANDS_FAQ,
     {"q": "How often should my furnace be serviced?",
      "a": "Once a year, ideally in fall before the heating season — it keeps efficiency up and catches safety issues early."}],
    [{"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Heat Pump Services", "href": "/heat-pump"},
     {"title": "Thermostat Services", "href": "/thermostat"}],
    pills=pillset("FURNACE & HEATING", FURN_PILLS, "Overview"), safety=True)

HVAC_PAGES["heat-pump.html"] = detail(
    "heat-pump", HVAC_CRUMB, "Heat Pump Services",
    "Year-round comfort from {X}.", "one system",
    "Heat pump repair, installation, and tune-ups for Dayton & Cincinnati homes — efficient heating and cooling with upfront pricing.",
    ["4.9 on Google", "90% Same-Day Service", "24/7 Emergency"],
    "BOOK HEAT PUMP SERVICE", "Get a tech to your door.",
    "HEAT PUMP ACTING UP?", "Signs it's time to call.",
    ["Not heating or cooling like it used to", "Ice building up on the outdoor unit", "Running constantly or short cycling",
     "Grinding, rattling, or squealing", "Blowing the wrong temperature air", "Energy bills creeping up"],
    "Noticing more than one? Small heat pump problems become compressor problems — call {tel} before it gets expensive.",
    "Repair, replace, or maintain — we handle it all.",
    [{"title": "Heat Pump Repair", "desc": "Fast diagnostics for every make and model — approved by you before we start.", "href": "/heat-pump-repair"},
     {"title": "Heat Pump Installation", "desc": "Right-sized, high-efficiency systems installed clean — with flexible financing options.", "href": "/heat-pump-installation"},
     {"title": "Heat Pump Tune-Ups", "desc": "Twice-a-year checkups keep efficiency high — included with X-Plan.", "href": "/maintenance"}],
    steps("Fixed right, guaranteed", "Clean workmanship, tested before we leave, and backed by our satisfaction guarantee."),
    "HEAT PUMP QUESTIONS",
    [SPEED_FAQ,
     {"q": "Do heat pumps work in Ohio winters?",
      "a": "Yes — modern cold-climate heat pumps heat efficiently well below freezing, and dual-fuel setups pair a heat pump with a furnace for the coldest snaps."},
     {"q": "Should I repair or replace my heat pump?",
      "a": "Under 10 years old with a minor issue, repair usually wins. Past 12–15 years with a compressor-level failure, replacement often costs less over time."},
     BRANDS_FAQ],
    [{"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"},
     {"title": "Indoor Air Quality", "href": "/indoor-air-quality"}],
    pills=pillset("HEAT PUMPS", HP_PILLS, "Overview"))

HVAC_PAGES["duct-cleaning.html"] = detail(
    "duct-cleaning", HVAC_CRUMB, "Duct Cleaning",
    "Cleaner air starts {X}.", "in your ducts",
    "Professional duct cleaning and air balancing for Dayton & Cincinnati homes — better airflow, less dust, upfront pricing.",
    ["4.9 on Google", "Locally Owned", "Upfront Pricing"],
    "BOOK DUCT CLEANING", "Get a tech to your door.",
    "DUSTY HOUSE?", "Signs your ducts need attention.",
    ["Dust returns right after cleaning", "Musty smells when the system runs", "Uneven airflow between rooms",
     "Allergies acting up indoors", "Visible dust at the vents", "Ducts never professionally cleaned"],
    "Remodeling dust, pets, or allergies? Call {tel} and we'll tell you honestly whether cleaning will help.",
    "Cleaning, balancing, and sealing — done right.",
    [{"title": "Duct Cleaning", "desc": "Truck-powered cleaning that pulls dust and debris from the whole duct system.", "href": "/contact"},
     {"title": "Air Balancing", "desc": "Even out hot and cold rooms with airflow measurement and adjustment.", "href": "/contact"},
     {"title": "Dryer Vent Cleaning", "desc": "Faster dry times and less fire risk — often same visit.", "href": "/contact"}],
    steps("Cleaner air, guaranteed", "Before-and-after photos of your ducts, and everything left spotless."),
    "DUCT QUESTIONS",
    [SPEED_FAQ,
     {"q": "How often should ducts be cleaned?",
      "a": "Every 3–5 years for most homes — sooner after a remodel, with shedding pets, or if allergies flare indoors."},
     {"q": "Will duct cleaning help my allergies?",
      "a": "It can — removing built-up dust, dander, and debris reduces what recirculates. Pair it with filtration for the biggest improvement."}],
    [{"title": "Indoor Air Quality", "href": "/indoor-air-quality"},
     {"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Humidifier Services", "href": "/humidifier"}])

# Duct cleaning is the one service where the result is invisible until you look
# inside the duct, so the page carries the proof: a real before/after frame from a
# job, and the crew's own walkthrough video.
HVAC_PAGES["duct-cleaning.html"]["media"] = [
    {"eyebrow": "BEFORE & AFTER",
     "h2": "See what a difference it can make.",
     "sub": "The same run of ductwork, photographed before the crew started and after "
            "they finished.",
     "photo": T.cdn_asset("service/before-after-ducts.jpg"),
     # 50% 70% is the 16:9 band that keeps both BEFORE and AFTER labels in frame; a
     # centred crop cuts them off.
     "photoPos": "50% 70%",
     "photoAlt": "The same length of ductwork before and after cleaning: heavy dust "
                 "coating the surfaces on the left, bare metal on the right",
     "caption": "A duct run from a Dayton-area home."},
    {"eyebrow": "HOW WE DO IT",
     "h2": "Watch a duct cleaning, start to finish.",
     "sub": "Truck-powered equipment, every supply and return run, and the ducts "
            "photographed before we leave.",
     "video": "E_cZVpgYvIw",
     "videoTitle": "Extreme Heating - Duct Cleaning - How We Do It!"},
]

HVAC_PAGES["thermostat.html"] = detail(
    "thermostat", HVAC_CRUMB, "Thermostat Services",
    "Smarter comfort, {X}.", "one tap away",
    "Smart thermostat installation, setup, and troubleshooting — get more comfort and lower bills from the system you already own.",
    ["4.9 on Google", "Locally Owned", "Upfront Pricing"],
    "BOOK THERMOSTAT SERVICE", "Get a tech to your door.",
    "THERMOSTAT TROUBLE?", "Signs it's time to call.",
    ["Blank or unresponsive display", "Temperature doesn't match the setting", "System won't turn on or off",
     "Short cycling on and off", "Wi-Fi or app won't connect", "Rooms never feel right"],
    "Thermostat acting up? It's often the cheapest fix in HVAC — call {tel} before assuming the worst.",
    "Install, program, and troubleshoot — any brand.",
    [{"title": "Smart Thermostat Install", "desc": "Nest, Ecobee, Honeywell and more — wired, mounted, and connected right.", "href": "/contact"},
     {"title": "Setup & Programming", "desc": "Schedules, sensors, and app setup tuned to how your home actually runs.", "href": "/contact"},
     {"title": "Thermostat Repair", "desc": "Wiring faults, compatibility issues, and replacements — diagnosed fast.", "href": "/contact"}],
    steps("Working right, explained", "We test heating and cooling cycles and walk you through the controls before we leave."),
    "THERMOSTAT QUESTIONS",
    [SPEED_FAQ,
     {"q": "Which smart thermostat should I buy?",
      "a": "It depends on your system's wiring and staging. We'll recommend one that actually works with your equipment — and install it right the first time."},
     {"q": "Can a new thermostat lower my bills?",
      "a": "Yes — smart schedules and occupancy sensing typically trim 8–12% off heating and cooling costs."}],
    [{"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"},
     {"title": "HVAC Inspections", "href": "/inspection"}])

HVAC_PAGES["humidifier.html"] = detail(
    "humidifier", HVAC_CRUMB, "Humidifier Services",
    "Whole-home humidity, {X}.", "done right",
    "Whole-home humidifier installation and service — end dry winter air, static shocks, and cracked wood floors.",
    ["4.9 on Google", "Locally Owned", "Upfront Pricing"],
    "BOOK HUMIDIFIER SERVICE", "Get a tech to your door.",
    "DRY AIR PROBLEMS?", "Signs your home needs humidity help.",
    ["Static shocks all winter", "Dry skin, lips, and sinuses", "Cracking wood floors or furniture",
     "Gaps opening in trim and doors", "Waking up congested", "Humidity readings below 30%"],
    "Dry air is hardest on homes in an Ohio winter — call {tel} and we'll size the right solution.",
    "Install, service, and balance — whole-home.",
    [{"title": "Humidifier Installation", "desc": "Bypass, fan-powered, or steam — matched to your home and furnace.", "href": "/contact"},
     {"title": "Humidifier Service", "desc": "Pad replacement, cleaning, and tune-ups to keep output steady.", "href": "/contact"},
     {"title": "Dehumidification", "desc": "Summer moisture control for basements and whole homes.", "href": "/indoor-air-quality"}],
    steps("Comfort, dialed in", "We set target humidity by season and show you how to adjust it."),
    "HUMIDIFIER QUESTIONS",
    [SPEED_FAQ,
     {"q": "What humidity should my home be?",
      "a": "30–50% depending on season — low enough to avoid window condensation in winter, high enough to stay comfortable."},
     {"q": "Do whole-home humidifiers need maintenance?",
      "a": "Yes — an annual pad change and cleaning keeps them working and sanitary. We handle it during X-Plan tune-ups."}],
    [{"title": "Indoor Air Quality", "href": "/indoor-air-quality"},
     {"title": "Duct Cleaning", "href": "/duct-cleaning"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"}])

HVAC_PAGES["inspection.html"] = detail(
    "inspection", HVAC_CRUMB, "HVAC Inspections",
    "Know your system, {X}.", "before it surprises you",
    "Full-system HVAC inspections for peace of mind — home purchases, seasonal checkups, and honest second opinions.",
    ["4.9 on Google", "Locally Owned", "Upfront Pricing"],
    "BOOK AN INSPECTION", "Get a tech to your door.",
    "WHY INSPECT?", "When an inspection pays for itself.",
    ["Buying or selling a home", "System is 10+ years old", "Bills higher than last year",
     "Comfort varies room to room", "No service records on file", "Second opinion on a big quote"],
    "Want eyes on it before you commit? Call {tel} — we'll tell you what's real and what can wait.",
    "Checked bumper to bumper.",
    [{"title": "Full-System Inspection", "desc": "Heating, cooling, ductwork, and safety — documented with photos.", "href": "/contact"},
     {"title": "Pre-Purchase Checks", "desc": "Know what you're buying before you close — with repair estimates.", "href": "/contact"},
     {"title": "Second Opinions", "desc": "A big repair quote deserves a second set of eyes — no pressure, just numbers.", "href": "/contact"}],
    steps("A report you can act on", "Findings in plain English, prioritized by safety, urgency, and cost."),
    "INSPECTION QUESTIONS",
    [SPEED_FAQ,
     {"q": "What does an HVAC inspection include?",
      "a": "Combustion safety, refrigerant performance, electrical checks, airflow, and ductwork condition — documented with photos and plain-English findings."},
     {"q": "Is an inspection the same as a tune-up?",
      "a": "No — an inspection documents condition; a tune-up services the equipment. X-Plan includes both, twice a year."}],
    [{"title": "Maintenance Plans", "href": "/maintenance"},
     {"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"}])

HVAC_PAGES["indoor-air-quality.html"] = detail(
    "indoor-air-quality", HVAC_CRUMB, "Indoor Air Quality",
    "Breathe easier {X}.", "at home",
    "Filtration, purification, and humidity control for Dayton & Cincinnati homes — cleaner air from the team you already trust.",
    ["4.9 on Google", "Locally Owned", "Upfront Pricing"],
    "BOOK AIR QUALITY HELP", "Get a tech to your door.",
    "AIR FEELING OFF?", "Signs your air quality needs attention.",
    ["Allergies flare up indoors", "Dust builds up fast", "Lingering odors or stale air",
     "Too humid in summer, too dry in winter", "Mold or musty smells", "Everyone sleeps better away from home"],
    "Air quality problems compound quietly — call {tel} and we'll find the source, not just the symptom.",
    "Filter it, purify it, balance it.",
    [{"title": "Air Quality Solutions", "desc": "Filtration, UV purification, and ventilation matched to your home.", "href": "/indoor-air-quality-solutions"},
     {"title": "Why IAQ Matters", "desc": "What indoor air actually carries — and what it does to sleep and health.", "href": "/importance-iaq"},
     {"title": "IAQ Questions", "desc": "Straight answers on filters, purifiers, humidity, and more.", "href": "/iaq-faq"}],
    steps("Cleaner air, measured", "We verify results with before-and-after readings — not promises."),
    "AIR QUALITY QUESTIONS",
    [SPEED_FAQ,
     {"q": "What actually improves indoor air?",
      "a": "Source control first, then filtration, then purification — in that order. We'll tell you what your home actually needs, not a package."},
     {"q": "Do UV purifiers work?",
      "a": "Against biological growth on coils and airborne microbes, yes — when sized and placed correctly. They're not a fix for dust."}],
    [{"title": "Duct Cleaning", "href": "/duct-cleaning"},
     {"title": "Humidifier Services", "href": "/humidifier"},
     {"title": "Air Conditioning", "href": "/air-conditioning"}],
    pills=pillset("INDOOR AIR QUALITY", IAQ_PILLS, "Overview"))

# X-Plan page — restyled to tokens, membership content kept
HVAC_PAGES["maintenance.html"] = detail(
    "maintenance", HVAC_CRUMB, "X-Plan Maintenance",
    "Never think about {X} again.", "tune-ups",
    "The X-Plan: two seasonal tune-ups a year, priority scheduling, 15% off repairs, and a 5-year repair warranty — $249/year or $20.75/month.",
    ["4.9 on Google", "Priority Scheduling", "15% Off Repairs"],
    "JOIN X-PLAN", "Membership starts today.",
    "EVERY VISIT INCLUDES", "What your tune-up covers.",
    ["Full system inspection & safety check", "Capacitor, relay & thermostat testing", "Compressor amp draws",
     "Drain line cleaning", "Pressure check", "Light coil cleaning"],
    "Questions about membership or billing? Call {tel} — we'll walk you through it.",
    "Membership that pays for itself.",
    [{"title": "Priority Scheduling", "desc": "Members go to the front of the line — especially during heat waves and cold snaps.", "href": "/contact"},
     {"title": "15% Off Repairs", "desc": "Every repair, every visit — plus a reduced service fee.", "href": "/contact"},
     {"title": "5-Year Repair Warranty", "desc": "Our work, guaranteed five times longer than the industry standard.", "href": "/contact"}],
    steps("Covered, year-round", "We schedule your spring and fall visits automatically — you don't lift a finger."),
    "X-PLAN QUESTIONS",
    [{"q": "How fast can members get service?",
      "a": "Members get priority scheduling — during busy seasons that's often the difference between same-day and next-week."},
     {"q": "What does X-Plan cost?",
      "a": "$249 a year, or $20.75 a month — including both seasonal tune-ups, 15% off repairs, a reduced service fee, and the 5-year repair warranty."},
     {"q": "Does X-Plan cover both heating and cooling?",
      "a": "Yes — one tune-up each for the heating and cooling seasons, covering your full system."}],
    [{"title": "HVAC Inspections", "href": "/inspection"},
     {"title": "Air Conditioning", "href": "/air-conditioning"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"}])

# ---- HVAC sub-pages (2d pattern) ----
HVAC_SUBS = {}

HVAC_SUBS["furnace-installation.html"] = sub(
    [HVAC_CRUMB, ("Furnace & Heating", "/furnace-heating"), ("Installation", "")],
    "A new furnace, {X}.", "installed right",
    "Right-sized, high-efficiency furnaces installed clean and to code — with honest sizing math and flexible financing.",
    pillset("FURNACE & HEATING", FURN_PILLS, "Installation"),
    "TIME TO REPLACE?", "Signs a new furnace makes sense.",
    ["Furnace is 15+ years old", "Repairs are getting frequent", "Bills climbing year over year",
     "Some rooms never get warm", "Yellow burner flame or soot", "Major component failure"],
    "Not sure repair vs. replace? Call {tel} — we'll give you both numbers, no pressure.",
    steps("Installed clean, tested hot", "Code-compliant gas, venting, and electrical — commissioned and walked through before we leave.",
          step2={"title": "Sized & quoted upfront", "desc": "A real load calculation — not a guess — with flat pricing and financing options."}),
    {"title": "Repair or replace?",
     "desc": "If your furnace is under 12 years old and the fix is minor, repair usually wins. We'll lay out both paths honestly.",
     "linkLabel": "Furnace Repair →", "href": "/furnace-repair"},
    "INSTALLATION QUESTIONS",
    [{"q": "How fast can you install a new furnace?",
      "a": "Usually within a day or two of your estimate — and same-week in most cases, even in season."},
     {"q": "What size furnace do I need?",
      "a": "It depends on your home's real heat loss — we run a load calculation instead of matching the old label."},
     {"q": "Is financing available?",
      "a": "Yes — flexible monthly options on qualifying systems. We'll show you payment scenarios with your quote."}],
    "BOOK AN ESTIMATE", "Free replacement estimates.", "Honest numbers, no pressure.",
    "FURNACE & HEATING",
    [{"title": "Furnace & Heating Overview", "href": "/furnace-heating"},
     {"title": "Furnace Repair", "href": "/furnace-repair"},
     {"title": "Thermostat Services", "href": "/thermostat"}],
    schedule_label="Schedule Estimate")

HVAC_SUBS["indoor-air-quality-solutions.html"] = sub(
    [HVAC_CRUMB, ("Indoor Air Quality", "/indoor-air-quality"), ("Solutions", "")],
    "Air quality solutions {X}.", "that actually work",
    "Filtration, UV purification, ventilation, and humidity control — matched to your home's actual problems, not a package.",
    pillset("INDOOR AIR QUALITY", IAQ_PILLS, "Solutions"),
    "WHAT WE SOLVE", "Match the fix to the problem.",
    ["Dust & dander — media filtration", "Odors & VOCs — carbon + ventilation", "Microbes & mold — UV purification",
     "Dry winter air — whole-home humidifier", "Humid summers — dehumidification", "Stale air — fresh-air ventilation"],
    "Not sure which applies to your home? Call {tel} — we diagnose before we recommend.",
    steps("Installed & measured", "Solutions installed clean, then verified with before-and-after readings.",
          step2={"title": "Assess & recommend", "desc": "We test your air and match solutions to the actual problem — no bundles you don't need."}),
    {"title": "Start with an air quality check",
     "desc": "A short assessment tells us whether filtration, purification, or humidity control will move the needle for your home.",
     "linkLabel": "IAQ Overview →", "href": "/indoor-air-quality"},
    "SOLUTIONS QUESTIONS",
    [{"q": "How fast can solutions be installed?",
      "a": "Most filtration and UV installs happen in a single visit — often the same week you call."},
     {"q": "Which filter rating should I use?",
      "a": "The highest MERV your system can handle without choking airflow — we'll check yours before recommending."},
     {"q": "Do I need a whole-home system?",
      "a": "Not always. Sometimes a filter upgrade and duct sealing beat an expensive purifier. We'll tell you honestly."}],
    "BOOK AIR QUALITY HELP", "Cleaner air starts here.", "Assessment and upfront pricing first.",
    "INDOOR AIR QUALITY",
    [{"title": "IAQ Overview", "href": "/indoor-air-quality"},
     {"title": "Why IAQ Matters", "href": "/importance-iaq"},
     {"title": "IAQ FAQ", "href": "/iaq-faq"}])

HVAC_SUBS["importance-iaq.html"] = sub(
    [HVAC_CRUMB, ("Indoor Air Quality", "/indoor-air-quality"), ("Importance", "")],
    "Why indoor air {X}.", "matters",
    "Indoor air is often 2–5× more polluted than outdoor air — here's what that means for your sleep, health, and home.",
    pillset("INDOOR AIR QUALITY", IAQ_PILLS, "Importance"),
    "WHAT'S IN YOUR AIR?", "What indoor air carries.",
    ["Dust, dander & pollen", "VOCs from cleaners & furnishings", "Excess humidity feeding mold",
     "Dry air irritating sinuses", "Cooking & combustion byproducts", "Microbes recirculating through ducts"],
    "Concerned about what your family breathes? Call {tel} for an honest air quality assessment.",
    steps("Fixed at the source", "We treat causes — filtration, ventilation, humidity — not just symptoms.",
          step2={"title": "Test & explain", "desc": "We measure what's actually in your air and walk you through the results."}),
    {"title": "See the solutions",
     "desc": "From filtration to humidity control — match the right fix to what your air actually carries.",
     "linkLabel": "Air Quality Solutions →", "href": "/indoor-air-quality-solutions"},
    "IAQ QUESTIONS",
    [{"q": "How quickly can you assess our air?",
      "a": "Usually within a few days — the assessment itself takes under an hour in most homes."},
     {"q": "Does indoor air really affect sleep?",
      "a": "Yes — particulates, CO2 buildup, and humidity extremes all measurably disrupt sleep quality."},
     {"q": "Is my home too new to have air problems?",
      "a": "Newer, tighter homes often trap more pollutants, not fewer — ventilation matters more, not less."}],
    "BOOK AN ASSESSMENT", "Know what you're breathing.", "Measured, explained, and priced upfront.",
    "INDOOR AIR QUALITY",
    [{"title": "IAQ Overview", "href": "/indoor-air-quality"},
     {"title": "Air Quality Solutions", "href": "/indoor-air-quality-solutions"},
     {"title": "IAQ FAQ", "href": "/iaq-faq"}])

HVAC_SUBS["iaq-faq.html"] = sub(
    [HVAC_CRUMB, ("Indoor Air Quality", "/indoor-air-quality"), ("FAQ", "")],
    "Air quality questions, {X}.", "answered straight",
    "The questions homeowners actually ask about filters, purifiers, humidity, and duct cleaning — answered without the sales pitch.",
    pillset("INDOOR AIR QUALITY", IAQ_PILLS, "FAQ"),
    "QUICK ANSWERS", "The short version.",
    ["Filters: highest MERV your system allows", "UV: great for coils, not for dust", "Humidity: keep it 30–50%",
     "Duct cleaning: every 3–5 years", "Ventilation: tight homes need it most", "Odors: find the source first"],
    "Have a question that isn't here? Call {tel} — real answers from real techs.",
    steps("Solved, not sold", "If the honest answer is a $40 filter, that's what we'll tell you.",
          step2={"title": "Ask us anything", "desc": "Describe what you're noticing — we'll narrow the cause fast."}),
    {"title": "Dig into the details",
     "desc": "The full breakdown of what's in indoor air and which solutions match which problems.",
     "linkLabel": "Why IAQ Matters →", "href": "/importance-iaq"},
    "AIR QUALITY FAQ",
    [{"q": "How fast can you help with an air quality problem?",
      "a": "Assessments usually within days; most solutions install in a single visit."},
     {"q": "What's the single best upgrade for air quality?",
      "a": "For most homes: a properly-sized media filter, checked seasonally. It outperforms most gadgets."},
     {"q": "Does duct cleaning improve air quality?",
      "a": "It helps when ducts are genuinely dirty — after remodels, with pets, or if never cleaned. We'll look first and tell you honestly."}],
    "STILL HAVE QUESTIONS?", "Ask a real tech.", "No pressure, no pitch — just answers.",
    "INDOOR AIR QUALITY",
    [{"title": "IAQ Overview", "href": "/indoor-air-quality"},
     {"title": "Air Quality Solutions", "href": "/indoor-air-quality-solutions"},
     {"title": "Why IAQ Matters", "href": "/importance-iaq"}])

# ======================================================================
# Plumbing details (no pill nav)
# ======================================================================
PLUMB_PAGES = {}

PLUMB_PAGES["clogged-drain.html"] = detail(
    "clogged-drain", PLUMB_CRUMB, "Clogged Drain",
    "Clogged drains, {X}.", "cleared fast",
    "From slow sinks to backed-up main lines — cleared fast by licensed plumbers with upfront pricing.",
    ["4.9 on Google", "Same-Day Service", "Licensed Plumbers"],
    "BOOK DRAIN SERVICE", "Get a plumber to your door.",
    "DRAIN TROUBLE?", "Signs it's more than a slow sink.",
    ["Water backing up in tubs or sinks", "Gurgling from drains or toilet", "Sewage smells indoors",
     "Multiple slow drains at once", "Water around floor drains", "Clogs that keep coming back"],
    "Multiple drains backing up at once? That's a main-line warning — call {tel} before it becomes a mess.",
    "Cleared, cleaned, and diagnosed.",
    [{"title": "Drain Clearing", "desc": "Augers and hydro-jetting to clear the clog — not just poke a hole in it.", "href": "/contact"},
     {"title": "Camera Inspection", "desc": "See what's really down there — roots, grease, or a bigger sewer issue.", "href": "/plumbing/sewer-line/overview"},
     {"title": "Preventive Cleaning", "desc": "Scheduled cleanings for clog-prone lines before they back up.", "href": "/contact"}],
    steps("Cleared and verified", "We run water, confirm full flow, and tell you what caused it — so it doesn't repeat."),
    "DRAIN QUESTIONS",
    [SPEED_FAQ,
     {"q": "Why does my drain keep clogging?",
      "a": "Repeat clogs usually mean buildup or damage deeper in the line — a camera inspection finds the real cause."},
     {"q": "Are chemical drain cleaners safe?",
      "a": "We don't recommend them — they damage pipes and rarely clear the real blockage. Mechanical clearing is safer and lasts."}],
    [{"title": "Sewer Line Services", "href": "/plumbing/sewer-line/overview"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Toilet Repair", "href": "/plumbing/toilet-repair"}],
    promos=["scheduleFast", "specials"])

PLUMB_PAGES["emergency-plumbing.html"] = detail(
    "emergency-plumbing", PLUMB_CRUMB, "Emergency Plumbing",
    "Plumbing emergencies, {X}.", "handled 24/7",
    "Burst pipes, backups, and no-water emergencies — real 24/7 response from licensed local plumbers.",
    ["4.9 on Google", "24/7 Response", "Licensed Plumbers"],
    "EMERGENCY? BOOK NOW", "We're on our way.",
    "IS IT AN EMERGENCY?", "Call now if you see these.",
    ["Water you can't shut off", "Sewage backing up indoors", "Burst or frozen pipe",
     "No water to the house", "Water heater leaking fast", "Gas smell near appliances"],
    "<b>Safety first:</b> for gas smells, leave the house before calling {tel}. For water, shut the main valve if you can reach it safely.",
    "Stabilize, fix, and prevent.",
    [{"title": "Emergency Response", "desc": "Nights, weekends, and holidays — a real plumber, not a call center promise.", "href": "/contact"},
     {"title": "Burst Pipe Repair", "desc": "Fast isolation and repair to stop damage from spreading.", "href": "/plumbing/leak-detection"},
     {"title": "Backup Clearing", "desc": "Sewage backups cleared and sanitized — and the cause identified.", "href": "/plumbing/clogged-drain"}],
    steps("Fixed and protected", "We fix the emergency, then show you how to prevent the next one.",
          step1={"title": "Call any hour", "desc": "24/7 dispatch — we triage on the phone and get a plumber moving."}),
    "EMERGENCY QUESTIONS",
    [{"q": "How fast can you get here in an emergency?",
      "a": "Emergency calls get priority dispatch around the clock — we'll give you a real arrival window when you call, not a whole-day guess."},
     {"q": "What should I do while I wait?",
      "a": "Shut the nearest valve (or the main), move valuables clear, and don't run water to affected drains. We'll talk you through it on the phone."},
     {"q": "Do emergencies cost more?",
      "a": "After-hours dispatch differs from standard visits, but pricing is still flat and upfront — approved by you before work starts."}],
    [{"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Clogged Drain", "href": "/plumbing/clogged-drain"},
     {"title": "Water Heater Services", "href": "/plumbing/water-heater/overview"}],
    promos=["scheduleFast", "specials"], safety=True)

PLUMB_PAGES["leak-detection.html"] = detail(
    "leak-detection", PLUMB_CRUMB, "Leak Detection",
    "Hidden leaks, {X}.", "found fast",
    "Electronic leak detection that finds the problem without tearing up your home — then fixes it with upfront pricing.",
    ["4.9 on Google", "Non-Invasive", "Licensed Plumbers"],
    "BOOK LEAK DETECTION", "Get a plumber to your door.",
    "SUSPECT A LEAK?", "Signs water is going somewhere it shouldn't.",
    ["Water bill jumped without reason", "Meter runs with everything off", "Damp spots on walls or ceilings",
     "Musty smells or mold patches", "Warm spots on the floor", "Sound of running water at night"],
    "Leaks only get bigger — call {tel} before a drip becomes drywall.",
    "Find it, fix it, verify it.",
    [{"title": "Electronic Detection", "desc": "Acoustic and thermal tools pinpoint leaks behind walls and under slabs.", "href": "/contact"},
     {"title": "Leak Repair", "desc": "Targeted repairs with minimal opening — priced before we cut.", "href": "/contact"},
     {"title": "Repipe Options", "desc": "For aging systems that keep leaking, honest whole-home repipe numbers.", "href": "/contact"}],
    steps("Fixed and verified", "We pressure-test after repair and confirm the meter sits still."),
    "LEAK QUESTIONS",
    [SPEED_FAQ,
     {"q": "Can you find a leak without opening walls?",
      "a": "Usually, yes — acoustic and thermal detection narrows it to inches before we open anything."},
     {"q": "How do I check if I have a leak?",
      "a": "Turn everything off and watch your water meter for 15 minutes. If it moves, call us."}],
    [{"title": "Emergency Plumbing", "href": "/plumbing/emergency-plumbing"},
     {"title": "Sewer Line Services", "href": "/plumbing/sewer-line/overview"},
     {"title": "Water Treatment", "href": "/plumbing/water-treatment"}],
    promos=["scheduleFast", "specials"])

PLUMB_PAGES["toilet-repair.html"] = detail(
    "toilet-repair", PLUMB_CRUMB, "Toilet Repair",
    "Toilet trouble, {X}.", "fixed right",
    "Running, clogged, leaking, or rocking — toilets repaired or replaced by licensed plumbers with upfront pricing.",
    ["4.9 on Google", "Same-Day Service", "Licensed Plumbers"],
    "BOOK TOILET REPAIR", "Get a plumber to your door.",
    "TOILET ACTING UP?", "Signs it needs a pro.",
    ["Runs constantly or randomly", "Clogs keep coming back", "Water around the base",
     "Rocks or shifts when used", "Weak or incomplete flush", "Tank refills on its own"],
    "A running toilet can waste 200 gallons a day — call {tel} and stop paying for it.",
    "Repair, replace, or upgrade.",
    [{"title": "Toilet Repair", "desc": "Fill valves, flappers, seals, and clogs — fixed in one visit, priced first.", "href": "/contact"},
     {"title": "Toilet Replacement", "desc": "Efficient new models installed clean — old unit hauled away.", "href": "/contact"},
     {"title": "Leak Sealing", "desc": "Base and tank leaks stopped before they rot the floor.", "href": "/plumbing/leak-detection"}],
    steps("Fixed and flush-tested", "We test repeatedly, check for leaks, and leave the bathroom spotless."),
    "TOILET QUESTIONS",
    [SPEED_FAQ,
     {"q": "Repair or replace my toilet?",
      "a": "Repairs win for valves and seals; replacement wins for cracked bowls, constant clogs, or pre-1994 water hogs. We'll price both."},
     {"q": "Why does my toilet keep running?",
      "a": "Usually a worn flapper or fill valve — a fast, inexpensive fix that pays for itself in water savings."}],
    [{"title": "Clogged Drain", "href": "/plumbing/clogged-drain"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Water Heater Services", "href": "/plumbing/water-heater/overview"}],
    promos=["scheduleFast", "specials"])

PLUMB_PAGES["water-treatment.html"] = detail(
    "water-treatment", PLUMB_CRUMB, "Water Treatment",
    "Better water, {X}.", "from every tap",
    "Softeners, filtration, and reverse osmosis for Dayton & Cincinnati homes — matched to your water, not a sales quota.",
    ["4.9 on Google", "Free Water Testing", "Licensed Plumbers"],
    "BOOK WATER TESTING", "Get a plumber to your door.",
    "HARD WATER SIGNS?", "What your water is telling you.",
    ["White scale on fixtures", "Spots on dishes and glass", "Dry skin and dull laundry",
     "Metallic taste or odor", "Appliances failing early", "Cloudy or off-color water"],
    "Curious what's in your water? Call {tel} — we test first and recommend second.",
    "Soften, filter, or purify.",
    [{"title": "Water Softeners", "desc": "End scale buildup and protect your appliances — sized to your usage.", "href": "/contact"},
     {"title": "Whole-Home Filtration", "desc": "Cleaner water at every tap — chlorine, sediment, and odor removed.", "href": "/contact"},
     {"title": "Reverse Osmosis", "desc": "Bottle-quality drinking water from your kitchen tap.", "href": "/contact"}],
    steps("Installed and tested", "We verify results at the tap and set up simple maintenance.",
          step2={"title": "Test & recommend", "desc": "A real water test drives the recommendation — city or well."}),
    "WATER QUESTIONS",
    [SPEED_FAQ,
     {"q": "City water or well — does it matter?",
      "a": "Yes — city water usually needs chlorine and hardness treatment; wells vary widely and need testing first."},
     {"q": "Will a softener make water taste salty?",
      "a": "No — properly set softeners add far less sodium than people expect, and an RO tap removes it entirely for drinking."}],
    [{"title": "Water Heater Services", "href": "/plumbing/water-heater/overview"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Clogged Drain", "href": "/plumbing/clogged-drain"}],
    promos=["scheduleFast", "specials"])

# ---- Plumbing multi-child families ----
def family_overview(folder, name, h1, hl, intro, pills, sym_eyebrow, sym_h2, symptoms,
                    callout, wwd_h2, cards, last_step, faqs, related, safety=False, img=None):
    return detail(folder, PLUMB_CRUMB, name, h1, hl, intro,
        ["4.9 on Google", "Same-Day Service", "Licensed Plumbers"],
        f"BOOK {name.upper()}", "Get a plumber to your door.",
        sym_eyebrow, sym_h2, symptoms, callout, wwd_h2, cards,
        steps(last_step[0], last_step[1]),
        f"{name.split()[0].upper()} QUESTIONS", faqs, related,
        pills=pills, promos=["scheduleFast", "specials"], safety=safety, img=img)

PLUMB_FAMILIES = {}

PLUMB_FAMILIES["sewer-line/overview.html"] = family_overview(
    "sewer-line", "Sewer Line Services",
    "Sewer problems, {X}.", "solved for good",
    "Camera inspections, repairs, and cleaning for main sewer lines — real diagnosis before anyone digs.",
    pillset("SEWER LINE SERVICES", SEW_PILLS, "Overview"),
    "SEWER TROUBLE?", "Signs your main line is struggling.",
    ["Multiple drains backing up", "Sewage smells inside or out", "Gurgling toilets",
     "Soggy patches in the yard", "Clogs that keep returning", "Older home with clay pipes"],
    "Sewage backing up indoors? Stop running water and call {tel} — that's a main-line emergency.",
    "Inspect it, clean it, or repair it.",
    [{"title": "Sewer Repair", "desc": "Spot repairs and replacements — trenchless options where possible.", "href": "/plumbing/sewer-line/repair"},
     {"title": "Sewer Cleaning", "desc": "Hydro-jetting that scours the line clean — roots, grease, and all.", "href": "/plumbing/sewer-line/cleaning"},
     {"title": "Camera Inspection", "desc": "See exactly what's wrong before spending a dollar on digging.", "href": "/plumbing/sewer-line/repair"}],
    ("Fixed with proof", "Camera-verified before and after — you see exactly what you paid for."),
    [SPEED_FAQ,
     {"q": "Do you have to dig up my yard?",
      "a": "Not always — camera inspection tells us first, and trenchless repair handles many failures without excavation."},
     {"q": "Why do my drains keep backing up?",
      "a": "Recurring whole-house backups usually mean roots, bellies, or breaks in the main line — a camera finds which."}],
    [{"title": "Clogged Drain", "href": "/plumbing/clogged-drain"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Sump Pump Services", "href": "/plumbing/sump-pump/overview"}])

PLUMB_FAMILIES["sump-pump/overview.html"] = family_overview(
    "sump-pump", "Sump Pump Services",
    "Dry basements, {X}.", "guaranteed",
    "Sump pump repair, replacement, and battery backups — protection that works the night the storm hits.",
    pillset("SUMP PUMP SERVICES", SUMP_PILLS, "Overview"),
    "PUMP WORRIES?", "Signs your basement is at risk.",
    ["Pump runs constantly or never", "Grinding or rattling noises", "Pit fills faster than it empties",
     "Pump is 7+ years old", "No battery backup", "Musty basement smells"],
    "Storm season doesn't wait — call {tel} before the next heavy rain tests your pump.",
    "Repair, replace, and back up.",
    [{"title": "Sump Pump Repair", "desc": "Switches, floats, and check valves — fixed before the next storm.", "href": "/plumbing/sump-pump/repair"},
     {"title": "Sump Pump Installation", "desc": "Right-sized pumps installed clean — with high-water alarms.", "href": "/plumbing/sump-pump/installation"},
     {"title": "Battery Backups", "desc": "Power fails in the same storms that flood — backups keep pumping.", "href": "/plumbing/sump-pump/installation"}],
    ("Tested under load", "We flood-test the pit and verify the full cycle before we leave."),
    [SPEED_FAQ,
     {"q": "How long do sump pumps last?",
      "a": "About 7–10 years. Past that, replacement before failure beats a flooded basement after."},
     {"q": "Do I really need a battery backup?",
      "a": "If your basement is finished or storms knock out your power — yes. It's the cheapest flood insurance you can buy."}],
    [{"title": "Leak Detection", "href": "/plumbing/leak-detection"},
     {"title": "Sewer Line Services", "href": "/plumbing/sewer-line/overview"},
     {"title": "Emergency Plumbing", "href": "/plumbing/emergency-plumbing"}])

PLUMB_FAMILIES["gas-line/overview.html"] = family_overview(
    "gas-line", "Gas Line Services",
    "Gas work, {X}.", "done safely",
    "Gas line installation, repair, and appliance hookups — licensed, pressure-tested, and code-compliant every time.",
    pillset("GAS LINE SERVICES", GAS_PILLS, "Overview"),
    "GAS CONCERNS?", "When to call a licensed pro.",
    ["Rotten-egg smell anywhere", "Hissing near gas appliances", "Dead grass over the gas line",
     "New appliance needs a hookup", "Old or corroded piping", "Pilot lights that won't stay lit"],
    "<b>Safety first:</b> smell gas? Leave the house first — don't flip switches — then call {tel} and your utility.",
    "Install, repair, and connect.",
    [{"title": "Gas Line Repair", "desc": "Leaks located, repaired, and pressure-tested — safety-first, always.", "href": "/plumbing/gas-line/repair"},
     {"title": "Gas Line Installation", "desc": "New runs for ranges, dryers, grills, and generators — to code.", "href": "/plumbing/gas-line/installation"},
     {"title": "Appliance Hookups", "desc": "Safe connections with proper shutoffs and leak checks.", "href": "/plumbing/gas-line/installation"}],
    ("Tested and certified", "Every job ends with a pressure test and leak check — documented."),
    [{"q": "How fast can you respond to a gas concern?",
      "a": "Suspected leaks get priority dispatch — and if you smell gas now, leave first and call from outside."},
     {"q": "Can you add a gas line for my grill or range?",
      "a": "Yes — sized, run, and tested to code, with a proper shutoff at the appliance."},
     {"q": "Who handles permits?",
      "a": "We do — permits and inspection scheduling are part of the job."}],
    [{"title": "Emergency Plumbing", "href": "/plumbing/emergency-plumbing"},
     {"title": "Water Heater Services", "href": "/plumbing/water-heater/overview"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"}],
    safety=True)

def plumb_sub(folder, child, name_parent, parent_href, pills, active, h1, hl, intro,
              sym_eyebrow, sym_h2, symptoms, callout, process_, decision, faqs,
              book_eyebrow, book_title, book_sub, sibs, safety=False, schedule_label="Schedule Service"):
    return sub(
        [PLUMB_CRUMB, (name_parent, parent_href), (active, "")],
        h1, hl, intro, pillset(pills[0], pills[1], active),
        sym_eyebrow, sym_h2, symptoms, callout, process_, decision,
        f"{active.upper()} QUESTIONS", faqs, book_eyebrow, book_title, book_sub,
        pills[0], sibs, safety=safety, schedule_label=schedule_label, promo="scheduleFast")

PLUMB_FAMILIES["water-heater/repair.html"] = plumb_sub(
    "water-heater", "repair", "Water Heater Services", "/plumbing/water-heater/overview",
    ("WATER HEATER SERVICES", WH_PILLS), "Repair",
    "Water heater repair, {X}.", "priced upfront",
    "Elements, thermostats, valves, and pilot problems — diagnosed fast and fixed the same day in most cases.",
    "NO HOT WATER?", "Common failures we fix daily.",
    ["No hot water at all", "Runs out faster than it used to", "Pilot light won't stay lit",
     "Popping or rumbling sounds", "Lukewarm at every tap", "Breaker trips on electric units"],
    "No hot water this morning? Call {tel} — repairs get priority dispatch.",
    steps("Hot water, same day", "Most repairs finish in one visit — tested at the tap before we go.",
          step1={"title": "Book in minutes", "desc": "No-hot-water calls get priority dispatch."}),
    {"title": "Repair or replace?",
     "desc": "If the tank itself leaks or the unit is 10+ years old, replacement usually wins. We'll price both honestly.",
     "linkLabel": "Water Heater Installation →", "href": "/plumbing/water-heater/installation"},
    [{"q": "How fast can you fix my water heater?",
      "a": "Same day in most cases — no-hot-water calls get priority, and we stock common parts on the truck."},
     {"q": "Is it worth repairing an older unit?",
      "a": "Past 10 years, usually not — a failing tank often leaks next. We'll give you repair and replace numbers side by side."},
     {"q": "Gas and electric — do you fix both?",
      "a": "Yes — tank and tankless, gas and electric, every major brand."}],
    "BOOK WATER HEATER REPAIR", "No hot water? We're on it.", "Priority dispatch for no-hot-water calls.",
    [{"title": "Water Heater Overview", "href": "/plumbing/water-heater/overview"},
     {"title": "Water Heater Installation", "href": "/plumbing/water-heater/installation"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"}],
    schedule_label="Schedule Repair")

PLUMB_FAMILIES["water-heater/installation.html"] = plumb_sub(
    "water-heater", "installation", "Water Heater Services", "/plumbing/water-heater/overview",
    ("WATER HEATER SERVICES", WH_PILLS), "Installation",
    "A new water heater, {X}.", "often same-day",
    "Right-sized tank and tankless installations — to code, tested at every tap, old unit hauled away.",
    "TIME TO REPLACE?", "Signs a new unit makes sense.",
    ["Tank is 10+ years old", "Rusty water from hot taps", "Water pooling at the base",
     "Repairs getting frequent", "Never enough hot water", "Thinking about tankless"],
    "Replacing before failure beats a flooded utility room — call {tel} for honest numbers.",
    steps("Installed and hauled away", "Set to code, tested at every tap, and the old unit gone when we leave.",
          step2={"title": "Sized & quoted upfront", "desc": "Sized to your household's real hot-water use — flat pricing with financing options."}),
    {"title": "Tank or tankless?",
     "desc": "Tanks cost less upfront; tankless delivers endless hot water and lower bills. We'll lay out both for your home honestly.",
     "linkLabel": "Water Heater Overview →", "href": "/plumbing/water-heater/overview"},
    [{"q": "Can you install a water heater the same day?",
      "a": "Usually — we stock common tank sizes, so most replacements happen the day you approve the quote."},
     {"q": "What size should I get?",
      "a": "A family of four typically needs 40–50 gallons; we size to your actual usage, not a guess."},
     {"q": "Is financing available?",
      "a": "Yes — flexible monthly options on qualifying installations."}],
    "BOOK AN INSTALLATION", "Same-day replacement, most cases.", "Free estimates with honest sizing.",
    [{"title": "Water Heater Overview", "href": "/plumbing/water-heater/overview"},
     {"title": "Water Heater Repair", "href": "/plumbing/water-heater/repair"},
     {"title": "Water Treatment", "href": "/plumbing/water-treatment"}],
    schedule_label="Schedule Estimate")

PLUMB_FAMILIES["sewer-line/repair.html"] = plumb_sub(
    "sewer-line", "repair", "Sewer Line Services", "/plumbing/sewer-line/overview",
    ("SEWER LINE SERVICES", SEW_PILLS), "Repair",
    "Sewer repair, {X}.", "with proof",
    "Camera-diagnosed sewer repairs — trenchless where possible, dug only where necessary, verified after.",
    "BROKEN LINE?", "Signs your sewer needs repair, not just cleaning.",
    ["Backups return after cleaning", "Soggy or sunken yard patches", "Sewage smells outside",
     "Foundation cracks near the line", "Camera shows breaks or bellies", "Clay pipe with root intrusion"],
    "Repeat backups mean the line itself is failing — call {tel} for a camera look before it collapses.",
    steps("Repaired and re-scoped", "We camera the line after repair so you see exactly what you paid for.",
          step2={"title": "Camera first, quote second", "desc": "No guesswork — you see the break before we price the fix."}),
    {"title": "Repair or clean?",
     "desc": "If the pipe is intact but clogged, hydro-jetting may be all you need — at a fraction of repair cost.",
     "linkLabel": "Sewer Cleaning →", "href": "/plumbing/sewer-line/cleaning"},
    [{"q": "How fast can you repair a sewer line?",
      "a": "Camera diagnosis usually same or next day; most repairs complete within days, not weeks."},
     {"q": "Is trenchless repair really possible?",
      "a": "Often, yes — pipe bursting and lining fix many failures without excavating the yard."},
     {"q": "Will insurance cover it?",
      "a": "Sometimes — we document everything with camera footage to support your claim."}],
    "BOOK SEWER REPAIR", "Backups keep returning?", "Camera-first diagnosis, honest pricing.",
    [{"title": "Sewer Line Overview", "href": "/plumbing/sewer-line/overview"},
     {"title": "Sewer Cleaning", "href": "/plumbing/sewer-line/cleaning"},
     {"title": "Clogged Drain", "href": "/plumbing/clogged-drain"}],
    schedule_label="Schedule Repair")

PLUMB_FAMILIES["sewer-line/cleaning.html"] = plumb_sub(
    "sewer-line", "cleaning", "Sewer Line Services", "/plumbing/sewer-line/overview",
    ("SEWER LINE SERVICES", SEW_PILLS), "Cleaning",
    "Sewer cleaning that {X}.", "actually lasts",
    "Hydro-jetting scours the full pipe wall clean — roots, grease, and scale — not just a hole through the clog.",
    "SLOW EVERYTHING?", "Signs your main line needs cleaning.",
    ["Whole-house drains run slow", "Gurgling after flushing", "Grease-heavy kitchen line",
     "Roots found on camera", "Annual backups like clockwork", "Never been jetted"],
    "Snaking pokes a hole; jetting cleans the pipe — call {tel} to break the backup cycle.",
    steps("Scoured and scoped", "Post-cleaning camera pass confirms a clean pipe wall, end to end.",
          step2={"title": "Jet, don't just poke", "desc": "High-pressure water scours the full diameter — roots, grease, and scale."}),
    {"title": "Cleaning or repair?",
     "desc": "If the camera shows breaks or bellies, cleaning alone won't hold — we'll show you the footage and price both.",
     "linkLabel": "Sewer Repair →", "href": "/plumbing/sewer-line/repair"},
    [{"q": "How fast can you jet my line?",
      "a": "Usually same or next day — and backups get priority."},
     {"q": "How long does hydro-jetting last?",
      "a": "Years for most homes — grease-heavy or root-prone lines benefit from scheduled maintenance jetting."},
     {"q": "Is jetting safe for old pipes?",
      "a": "We camera first — if the pipe is too fragile, we'll tell you before jetting, not after."}],
    "BOOK SEWER CLEANING", "Break the backup cycle.", "Camera-verified clean, upfront price.",
    [{"title": "Sewer Line Overview", "href": "/plumbing/sewer-line/overview"},
     {"title": "Sewer Repair", "href": "/plumbing/sewer-line/repair"},
     {"title": "Clogged Drain", "href": "/plumbing/clogged-drain"}])

PLUMB_FAMILIES["sump-pump/repair.html"] = plumb_sub(
    "sump-pump", "repair", "Sump Pump Services", "/plumbing/sump-pump/overview",
    ("SUMP PUMP SERVICES", SUMP_PILLS), "Repair",
    "Sump pump repair, {X}.", "before the storm",
    "Floats, switches, check valves, and clogs — repaired and flood-tested before the next heavy rain.",
    "PUMP PROBLEMS?", "Failures we fix before they flood.",
    ["Pump won't turn on", "Runs but doesn't move water", "Cycles constantly",
     "Stuck or jammed float", "Rattling or grinding", "Pit overflows in storms"],
    "A pump that's acting up will fail on the worst night — call {tel} before the forecast turns.",
    steps("Flood-tested before we go", "We fill the pit and verify full cycles — not just a hum.",
          step1={"title": "Book in minutes", "desc": "Storm-season calls get priority — don't wait for the radar."}),
    {"title": "Repair or replace?",
     "desc": "Pumps past 7 years or with motor failures are usually smarter to replace — often with a backup added.",
     "linkLabel": "Sump Pump Installation →", "href": "/plumbing/sump-pump/installation"},
    [{"q": "How fast can you repair my sump pump?",
      "a": "Same day in most cases — and priority when storms are in the forecast."},
     {"q": "Why does my pump run constantly?",
      "a": "Usually a stuck float, failed check valve, or an undersized pump — all fixable, all testable in one visit."},
     {"q": "Should I test my own pump?",
      "a": "Yes — pour a bucket of water in the pit each spring. If it doesn't cycle cleanly, call us."}],
    "BOOK PUMP REPAIR", "Storm coming? We're on it.", "Priority dispatch in storm season.",
    [{"title": "Sump Pump Overview", "href": "/plumbing/sump-pump/overview"},
     {"title": "Sump Pump Installation", "href": "/plumbing/sump-pump/installation"},
     {"title": "Emergency Plumbing", "href": "/plumbing/emergency-plumbing"}],
    schedule_label="Schedule Repair")

PLUMB_FAMILIES["sump-pump/installation.html"] = plumb_sub(
    "sump-pump", "installation", "Sump Pump Services", "/plumbing/sump-pump/overview",
    ("SUMP PUMP SERVICES", SUMP_PILLS), "Installation",
    "Sump pumps installed {X}.", "storm-ready",
    "Right-sized primary pumps and battery backups — installed clean, alarmed, and tested under load.",
    "TIME TO UPGRADE?", "When installation beats another repair.",
    ["Pump is 7+ years old", "Basement is finished", "Power fails in storms",
     "Pit too small or shallow", "No high-water alarm", "History of close calls"],
    "The best time to upgrade is before the water table rises — call {tel} for honest sizing.",
    steps("Tested under load", "We flood-test the full system — primary, backup, and alarm — before we leave.",
          step2={"title": "Sized & quoted upfront", "desc": "Pump capacity matched to your pit, discharge, and water table."}),
    {"title": "Add a battery backup?",
     "desc": "Storms that flood basements also knock out power — a backup keeps pumping when the grid doesn't.",
     "linkLabel": "Sump Pump Overview →", "href": "/plumbing/sump-pump/overview"},
    [{"q": "How fast can you install a sump pump?",
      "a": "Most installations happen within a day or two — same-week even in storm season."},
     {"q": "What size pump do I need?",
      "a": "Depends on your pit, discharge height, and water table — we size it to real conditions, not a shelf label."},
     {"q": "How long do battery backups run?",
      "a": "Quality backups pump intermittently for 24+ hours — enough to outlast most outages."}],
    "BOOK AN INSTALLATION", "Storm-ready, guaranteed.", "Free estimates with honest sizing.",
    [{"title": "Sump Pump Overview", "href": "/plumbing/sump-pump/overview"},
     {"title": "Sump Pump Repair", "href": "/plumbing/sump-pump/repair"},
     {"title": "Leak Detection", "href": "/plumbing/leak-detection"}],
    schedule_label="Schedule Estimate")

PLUMB_FAMILIES["gas-line/repair.html"] = plumb_sub(
    "gas-line", "repair", "Gas Line Services", "/plumbing/gas-line/overview",
    ("GAS LINE SERVICES", GAS_PILLS), "Repair",
    "Gas leaks fixed {X}.", "safely, fast",
    "Suspected leaks located, repaired, and pressure-tested by licensed pros — safety-first at every step.",
    "SMELL GAS?", "Take these signs seriously.",
    ["Rotten-egg smell indoors or out", "Hissing near lines or appliances", "Dead grass over buried line",
     "Higher gas bills without cause", "Pilot lights failing repeatedly", "Headaches or dizziness at home"],
    "<b>Safety first:</b> smell gas now? Leave the house — don't flip switches — then call {tel} and your utility from outside.",
    steps("Repaired, tested, documented", "Every repair ends with a pressure test and leak check — documented for your records.",
          step1={"title": "Call from safety", "desc": "Suspected leaks get priority dispatch — we coordinate with your utility."}),
    {"title": "Aging gas lines?",
     "desc": "Corroded or undersized lines fail again — sometimes a new run is the safer, cheaper answer.",
     "linkLabel": "Gas Line Installation →", "href": "/plumbing/gas-line/installation"},
    [{"q": "How fast do you respond to gas leaks?",
      "a": "Priority dispatch, around the clock — but leave the house first and call from outside."},
     {"q": "How do you find a gas leak?",
      "a": "Electronic detection and pressure testing locate leaks precisely — including buried lines."},
     {"q": "Can I keep using other appliances?",
      "a": "Not until the system is tested safe — we'll tell you exactly what's usable and when."}],
    "SUSPECTED LEAK?", "Leave first. Then call.", "Priority dispatch for gas concerns.",
    [{"title": "Gas Line Overview", "href": "/plumbing/gas-line/overview"},
     {"title": "Gas Line Installation", "href": "/plumbing/gas-line/installation"},
     {"title": "Emergency Plumbing", "href": "/plumbing/emergency-plumbing"}],
    safety=True, schedule_label="Schedule Repair")

PLUMB_FAMILIES["gas-line/installation.html"] = plumb_sub(
    "gas-line", "installation", "Gas Line Services", "/plumbing/gas-line/overview",
    ("GAS LINE SERVICES", GAS_PILLS), "Installation",
    "New gas lines, {X}.", "run to code",
    "Ranges, dryers, grills, fire pits, and generators — new gas runs sized, installed, and tested to code.",
    "ADDING GAS?", "What we run lines for.",
    ["Gas range or cooktop", "Clothes dryer conversion", "Outdoor grill or fire pit",
     "Standby generator", "Garage heater", "Pool or spa heater"],
    "Planning a project? Call {tel} early — a right-sized line saves headaches later.",
    steps("Connected and certified", "Pressure-tested, leak-checked, and inspected — with permits handled.",
          step2={"title": "Sized & quoted upfront", "desc": "BTU load calculated across appliances so everything runs right."}),
    {"title": "Upgrading appliances too?",
     "desc": "If old lines are corroded or undersized, we'll flag it during the estimate — before it's a problem.",
     "linkLabel": "Gas Line Repair →", "href": "/plumbing/gas-line/repair"},
    [{"q": "How fast can you run a new gas line?",
      "a": "Most residential runs are done in a day once permits clear — we handle the paperwork."},
     {"q": "Do I need a permit?",
      "a": "Yes for most gas work — and we pull it, schedule inspection, and close it out for you."},
     {"q": "Can you convert my dryer or range to gas?",
      "a": "Yes — line, shutoff, and safe hookup, tested before first use."}],
    "BOOK AN ESTIMATE", "Project-ready gas runs.", "Permits and inspection handled.",
    [{"title": "Gas Line Overview", "href": "/plumbing/gas-line/overview"},
     {"title": "Gas Line Repair", "href": "/plumbing/gas-line/repair"},
     {"title": "Water Heater Services", "href": "/plumbing/water-heater/overview"}],
    schedule_label="Schedule Estimate")

# ================================================================
# AC and heat pump sub-pages — the same Overview / Installation / Repair split the
# furnace family already had. Before these existed, the "AC Repair" and "Heat Pump
# Installation" cards on the two overview pages pointed at /contact and
# /financing-options, so a reader clicking a service name landed on a form.
# ================================================================
AC_CRUMB_PARENT = ("Air Conditioning", "/air-conditioning")
HP_CRUMB_PARENT = ("Heat Pump Services", "/heat-pump")

HVAC_SUBS["ac-repair.html"] = sub(
    [HVAC_CRUMB, AC_CRUMB_PARENT, ("Repair", "")],
    "Cool air back — {X}.", "usually the same day",
    "A dead AC in an Ohio July is an emergency. We diagnose fast, quote flat before any "
    "work starts, and repair every make and model — with the emergency line answered 24/7.",
    pillset("AIR CONDITIONING", AC_PILLS, "Repair"),
    "AC NOT COOLING?", "Signs it's time to call.",
    ["Blowing warm or room-temp air", "Outdoor unit runs, house stays hot",
     "Ice on the refrigerant lines or coil", "Turning on and off every few minutes",
     "Grinding, buzzing, or rattling", "Water pooling around the indoor unit"],
    "Ice on the lines or a burning smell? Shut the system off and call {tel} — running it "
    "that way is how a repair turns into a replacement.",
    steps("Fixed right, tested cold",
          "We verify the repair with gauges and a temperature split before we leave, and back "
          "it with our satisfaction guarantee."),
    {"title": "Repair or replace?",
     "desc": "Under 12 years old with a minor fault, repair usually wins. Older than that, or "
             "a failing compressor, and we'll put both numbers in front of you.",
     "linkLabel": "AC Installation →", "href": "/ac-installation"},
    "AC REPAIR QUESTIONS",
    [SPEED_FAQ,
     {"q": "Do you repair every brand?",
      "a": "Yes — every major make and model, whoever installed it."},
     {"q": "Will I know the price before you start?",
      "a": "Yes. You get a flat price for the repair before any work begins, and nothing "
           "happens until you approve it."},
     {"q": "My AC is old — is a repair worth it?",
      "a": "Often, yes. We'll tell you what the repair costs and what a replacement costs, "
           "and leave the decision to you — with a free second opinion on any replacement "
           "diagnosis."}],
    "BOOK AC REPAIR", "Cool air, fast.", "Upfront pricing before any work begins.",
    "AIR CONDITIONING",
    [{"title": "Air Conditioning Overview", "href": "/air-conditioning"},
     {"title": "AC Installation", "href": "/ac-installation"},
     {"title": "Thermostat Services", "href": "/thermostat"}],
    img=T.PHOTOS["acContactor"], imgPos="50% 45%",
    alt="A worn, cobwebbed contactor found inside an air conditioner during a service call",
    schedule_label="Schedule Repair")

HVAC_SUBS["ac-installation.html"] = sub(
    [HVAC_CRUMB, AC_CRUMB_PARENT, ("Installation", "")],
    "A new AC, {X}.", "sized and installed right",
    "Right-sized, high-efficiency air conditioners installed clean and to code — honest "
    "sizing math, free replacement estimates, and flexible financing.",
    pillset("AIR CONDITIONING", AC_PILLS, "Installation"),
    "TIME TO REPLACE?", "Signs a new AC makes sense.",
    ["System is 12+ years old", "Repairs are getting frequent",
     "Still running on R-22 refrigerant", "Bills climbing year over year",
     "Some rooms never cool down", "Compressor or coil failure"],
    "Not sure whether to repair or replace? Call {tel} — we'll give you both numbers, no pressure.",
    steps("Installed clean, tested cold",
          "Line set, electrical, and charge done to code, then commissioned and walked through "
          "before we leave.",
          step2={"title": "Sized & quoted upfront",
                 "desc": "A real load calculation — not a guess off the old label — with flat "
                         "pricing and financing options."}),
    {"title": "Repair or replace?",
     "desc": "If the system is newer and the fault is minor, a repair is usually the better "
             "money. We'll lay out both paths honestly.",
     "linkLabel": "AC Repair →", "href": "/ac-repair"},
    "INSTALLATION QUESTIONS",
    [{"q": "How fast can you install a new AC?",
      "a": "Usually within a day or two of your estimate — and same-week in most cases, even "
           "in the middle of summer."},
     {"q": "What size system do I need?",
      "a": "That depends on your home's real heat gain, so we run a load calculation instead "
           "of matching whatever was there before."},
     {"q": "Is financing available?",
      "a": "Yes — flexible monthly options on qualifying systems. We'll show you payment "
           "scenarios along with the quote."},
     {"q": "Do I have to replace the furnace at the same time?",
      "a": "Not always. If your furnace is newer and the coil and blower match up, the AC can "
           "be replaced on its own — we'll tell you honestly which case you're in."}],
    "BOOK AN ESTIMATE", "Free replacement estimates.", "Honest numbers, no pressure.",
    "AIR CONDITIONING",
    [{"title": "Air Conditioning Overview", "href": "/air-conditioning"},
     {"title": "AC Repair", "href": "/ac-repair"},
     {"title": "Heat Pump Services", "href": "/heat-pump"}],
    img=T.PHOTOS["ruudCondenser"], imgPos="50% 45%",
    alt="A Ruud air conditioner installed beside a brick home",
    schedule_label="Schedule Estimate")

HVAC_SUBS["heat-pump-repair.html"] = sub(
    [HVAC_CRUMB, HP_CRUMB_PARENT, ("Repair", "")],
    "Heat pump repair, {X}.", "any season",
    "A heat pump works year-round, so a fault shows up as no heat in January or no cooling "
    "in July. We diagnose fast, price flat before any work, and repair every make and model.",
    pillset("HEAT PUMPS", HP_PILLS, "Repair"),
    "HEAT PUMP ACTING UP?", "Signs it's time to call.",
    ["Blowing cool air in heating mode", "Outdoor unit iced over",
     "Runs constantly but never catches up", "Turning on and off every few minutes",
     "Grinding, rattling, or squealing", "Backup heat running all the time"],
    "No heat at all, or an outdoor unit encased in ice? Call {tel} — the emergency line is "
    "answered 24/7.",
    steps("Fixed right, tested both ways",
          "We confirm the system heats and cools properly before we leave, and back the repair "
          "with our satisfaction guarantee."),
    {"title": "Repair or replace?",
     "desc": "A newer heat pump with a minor fault is usually worth repairing. A compressor or "
             "reversing valve failure on an older system is where replacement starts to win.",
     "linkLabel": "Heat Pump Installation →", "href": "/heat-pump-installation"},
    "HEAT PUMP REPAIR QUESTIONS",
    [SPEED_FAQ,
     {"q": "Why is my heat pump blowing cool air in winter?",
      "a": "A few minutes of cool air during a defrost cycle is normal. Constant cool air is "
           "not — that usually points to refrigerant, a reversing valve, or a failed defrost "
           "control, and it's worth a look before the backup heat runs your bill up."},
     {"q": "Is ice on the outdoor unit a problem?",
      "a": "A light frost that clears on its own is normal. A unit encased in ice, or one that "
           "never clears, is not — shut it off and call us."},
     BRANDS_FAQ],
    "BOOK HEAT PUMP REPAIR", "Get a tech to your door.", "Upfront pricing before any work begins.",
    "HEAT PUMPS",
    [{"title": "Heat Pump Overview", "href": "/heat-pump"},
     {"title": "Heat Pump Installation", "href": "/heat-pump-installation"},
     {"title": "Furnace & Heating", "href": "/furnace-heating"}],
    img=T.PHOTOS["acRepairGauges"], imgPos="50% 45%",
    alt="Gauges and a meter connected to the open control panel of an outdoor unit",
    schedule_label="Schedule Repair")

HVAC_SUBS["heat-pump-installation.html"] = sub(
    [HVAC_CRUMB, HP_CRUMB_PARENT, ("Installation", "")],
    "One system, {X}.", "heating and cooling",
    "Right-sized, high-efficiency heat pumps installed clean and to code — with honest sizing "
    "math, backup heat set up properly, and flexible financing.",
    pillset("HEAT PUMPS", HP_PILLS, "Installation"),
    "TIME TO REPLACE?", "Signs a new heat pump makes sense.",
    ["System is 12+ years old", "Repairs are getting frequent",
     "Backup heat runs constantly", "Bills climbing year over year",
     "Rooms never quite even out", "Compressor or reversing valve failure"],
    "Weighing a heat pump against a furnace and AC? Call {tel} — we'll price both and explain "
    "the trade-offs for your home.",
    steps("Installed clean, commissioned",
          "Charge verified, controls and backup heat configured, and a full walkthrough before "
          "we leave.",
          step2={"title": "Sized & quoted upfront",
                 "desc": "A real load calculation, a written quote, and financing options — "
                         "before anything is ordered."}),
    {"title": "Not ready to replace?",
     "desc": "If the system still has years in it, a repair or a tune-up may be the better "
             "money this season. We'll tell you which case you're in.",
     "linkLabel": "Heat Pump Repair →", "href": "/heat-pump-repair"},
    "INSTALLATION QUESTIONS",
    [{"q": "How fast can you install a heat pump?",
      "a": "Usually within a day or two of your estimate, and same-week in most cases."},
     {"q": "Will a heat pump keep up in an Ohio winter?",
      "a": "We size for your home's real heat loss and set the backup heat up to cover the "
           "coldest nights, so the system isn't relying on the heat pump alone when it can't "
           "keep up. Dual-fuel setups pair one with a furnace for exactly that reason."},
     {"q": "Is financing available?",
      "a": "Yes — flexible monthly options on qualifying systems, shown with your quote."},
     {"q": "Can a heat pump replace both my furnace and AC?",
      "a": "In many homes, yes — one outdoor unit handles both. Whether that's the right call "
           "depends on your ductwork, your insulation, and how your home loses heat, which is "
           "what the load calculation tells us."}],
    "BOOK AN ESTIMATE", "Free replacement estimates.", "Honest numbers, no pressure.",
    "HEAT PUMPS",
    [{"title": "Heat Pump Overview", "href": "/heat-pump"},
     {"title": "Heat Pump Repair", "href": "/heat-pump-repair"},
     {"title": "Air Conditioning", "href": "/air-conditioning"}],
    img=T.PHOTOS["ruudHeatPump"], imgPos="50% 40%",
    alt="A Ruud heat pump installed at a Dayton-area home",
    schedule_label="Schedule Estimate")

# ======================================================================
# GEO content layer
# ----------------------------------------------------------------------
# Everything below rewrites the page data built above: answer-first blocks,
# real H2/H3 body sections, decision tables, per-page FAQ headings and the
# visible last-updated line. It is applied as a second pass rather than
# threaded through detail()/sub()/plumb_sub() so the constructors above keep
# their positional signatures and a copy change stays a one-key edit.
#
# Rules held throughout, from the client decisions of 2026-08-02:
#   · No radon claims anywhere. The company does not do radon mitigation, so
#     the radon H2, the radon table row and the radon FAQ from the research
#     deliverables are dropped rather than softened.
#   · No rebate or utility trade-ally claims.
#   · Service-call and dispatch fees never appear in an h1, h2 or hero. They
#     are not used below at all.
#   · The repair-quote-approaching-a-third-of-replacement rule of thumb is
#     approved and is used in the decision tables.
#   · No team copy, no technician names, no author attribution. E-E-A-T leans
#     on the company, its two Ohio licences and its history.
#   · X-Plan accrual always carries BOTH conditions in one sentence:
#     consecutive years AND capped at $2,500 or 10 years.
# ======================================================================

UPDATED, UPDATED_ISO = "August 2, 2026", "2026-08-02"

# The hero chip used to read "4.9 on Google". The 1,595-review figure is a
# Birdeye aggregate pooling several platforms, so naming Google is a claim a
# competitor can disprove in a minute. The rating source comes off the chip
# and the count goes on.
REVIEW_CHIP = "4.9 from 1,595 reviews"


def sec(h2, body, h3s=None, table=None, sid=None, eyebrow=None):
    """One body section: an H2 question, its direct answer, optional H3
    sub-questions, optional table rendered inside the section."""
    s = {"h2": h2, "body": body}
    if h3s:
        s["h3s"] = [{"h3": h, "body": b} for h, b in h3s]
    if table:
        s["table"] = table
    if sid:
        s["id"] = sid
    if eyebrow:
        s["eyebrow"] = eyebrow
    return s


def tbl(caption, takeaway, columns, rows, h2=None, sid=None, eyebrow=None):
    t = {"caption": caption, "takeaway": takeaway, "columns": columns, "rows": rows}
    if h2:
        t["h2"] = h2
    if sid:
        t["id"] = sid
    if eyebrow:
        t["eyebrow"] = eyebrow
    return t


def qa(*pairs):
    return [{"q": q, "a": a} for q, a in pairs]


def geo(store, key, callout=None, **fields):
    """Apply the rewrite to one page. `callout` reaches into symptoms so a
    page can hand off to a sibling from its callout without restating it."""
    d = store[key]
    d.update(fields)
    if callout is not None:
        d["symptoms"]["callout"] = call(callout)
    if d.get("heroChips"):
        d["heroChips"] = [REVIEW_CHIP if c == "4.9 on Google" else c
                          for c in d["heroChips"]]
    d.setdefault("updated", UPDATED)
    d.setdefault("updatedISO", UPDATED_ISO)
    return d


# ---------------------------------------------------------------- shared rows
# The third-of-replacement-cost row is the same judgement on every
# repair-or-replace table, so it is written once. The age row never is: the
# threshold differs by equipment type and that difference is the point.
COST_ROW = ("Repair cost", "The quote is well under a third of replacement cost",
            "The quote is at or above roughly a third of replacement cost")
R22_ROW = ("Refrigerant", "The system runs on R-410A or another refrigerant still in production",
           "The system runs on R-22, which has not been produced or imported in the US since 2020")


# ======================================================================
# HVAC detail pages
# ======================================================================

geo(HVAC_PAGES, "furnace-heating.html",
    h1="Furnace and heating service in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Furnace repairs, installations and safety checks from the locally owned "
          "Extreme Team. Upfront pricing, and warm air back fast.",
    answer="No heat? We repair, replace and safety-check gas and electric furnaces across "
           "Dayton and Cincinnati, and the emergency line is answered at any hour. Every "
           "visit ends with a combustion and carbon monoxide check.",
    callout="<b>Safety first:</b> smell gas or suspect carbon monoxide? Leave the house "
            "first, then call {tel}. We answer 24/7.",
    sections=[
        sec("What heating work do you actually handle?",
            "Furnace repair, furnace replacement and seasonal safety checks, on gas or "
            "electric equipment from any manufacturer. We work on postwar Dayton furnaces "
            "and brand-new Warren County builds alike, and the parts for common no-heat "
            "faults ride on the truck."),
        sec("Should I repair or replace my furnace?",
            "Two things settle it: how old the furnace is, and whether the failure is a part "
            "or the heat exchanger. A twelve-year-old furnace with a bad ignitor is a repair. "
            "A twenty-year-old furnace with a cracked heat exchanger is a replacement, because "
            "that specific part is not safely repairable. Once you are replacing, "
            "<a href=\"/furnace-installation\">furnace installation</a> covers sizing and "
            "efficiency tiers.",
            sid="repair-or-replace",
            table=tbl("Repair or replace a furnace: what we weigh up on a no-heat call.",
                      "Once a furnace is past 15 years old and the repair quote gets near a "
                      "third of what a new one costs, we will tell you replacement is the "
                      "better money.",
                      ["What we look at", "Repair when",
                       "Replace when"],
                      [("System age", "The furnace is under 12 years old",
                        "The furnace is past 15 years"),
                       ("Heat exchanger", "The heat exchanger passes inspection with no cracks",
                        "The heat exchanger is cracked or has failed a combustion test"),
                       COST_ROW,
                       ("Breakdown history", "This is the first failure in several heating seasons",
                        "This is the second or third no-heat call in one winter"),
                       ("Efficiency", "The furnace already carries a mid or high AFUE rating",
                        "The furnace is an older low-AFUE unit and gas bills keep climbing"),
                       ("Comfort", "One room runs cool",
                        "Rooms never balance and the furnace runs almost constantly"),
                       ("Warranty", "Parts are still under manufacturer warranty",
                        "Parts and labour warranties have both run out")])),
        sec("What are the signs a furnace is failing?",
            "Cold or lukewarm air at the vents, short cycling, a yellow or flickering burner "
            "flame, burning or musty smells, banging and scraping sounds, and heating bills "
            "that climb without a colder winter behind them. A yellow flame and any smell of "
            "gas are safety issues, not comfort issues. What each symptom usually means is "
            "covered on our <a href=\"/furnace-repair\">furnace repair</a> page."),
        sec("How long does a gas furnace last?",
            "Fifteen to twenty years is the normal working life of a gas furnace, and annual "
            "servicing tends to push it toward the top of that range. Past twenty, the "
            "question stops being whether it will fail and becomes whether it fails in "
            "January."),
    ],
    sectionsTail=[
        sec("What does AFUE mean on a furnace?",
            "AFUE stands for Annual Fuel Utilization Efficiency, and it is the share of the "
            "gas a furnace turns into usable heat over a year. A 96 AFUE furnace puts 96% of "
            "its fuel into the house and sends the rest out the flue. Sizing and efficiency "
            "tiers are covered on our <a href=\"/furnace-installation\">furnace "
            "installation</a> page."),
        sec("How often should a furnace be serviced?",
            "Once a year, in fall, before the heating season starts. The visit is as much a "
            "safety check as a performance one: heat exchanger, venting, gas pressure and "
            "carbon monoxide all get looked at. The <a href=\"/maintenance\">X-Plan "
            "maintenance membership</a> covers that visit plus a cooling visit, scheduled "
            "automatically."),
        sec("Do you work on electric furnaces and air handlers?",
            "Yes, on any brand. Electric furnaces, air handlers and the "
            "<a href=\"/heat-pump\">heat pump and dual-fuel systems</a> that pair with them "
            "are all covered, whoever installed the equipment."),
        sec("How do I book heating service?",
            call("Call {tel} or schedule online. A no-heat call in a cold snap goes to the "
                 "emergency line, which runs every day of the year. We reach most homes the "
                 "same day, and a <a href=\"/inspection\">pre-purchase HVAC inspection</a> "
                 "books the same way.")),
    ],
    faqH2="What else do homeowners ask about furnaces?",
    faq=qa(
        ("What should I do if the furnace quits in the middle of the night?",
         call("Call {tel}. Someone answers at any hour. While you wait, check that the "
              "thermostat is set to Heat, that the breaker has not tripped, and that the "
              "furnace door switch is seated.")),
        ("Is a cracked heat exchanger repairable?",
         "No. A cracked heat exchanger lets combustion gases, including carbon monoxide, into "
         "the air the furnace blows through the house. The fix is a new heat exchanger or a "
         "new furnace, and on any furnace past about fifteen years the exchanger usually "
         "costs more than the unit is worth."),
        ("Why does my furnace smell like burning dust the first time it runs?",
         "That is dust burning off the heat exchanger after a summer of sitting idle, and it "
         "should clear within an hour. A smell that lingers, or one that is sharp or chemical "
         "rather than dusty, is worth a call."),
        ("Does a new furnace need new ductwork?",
         "Not usually. Existing ductwork gets tested for leakage and static pressure during "
         "the estimate, and it gets repaired or resized only when the numbers say it will "
         "choke the new furnace. Duct condition is measured, not assumed."),
        ("Does X-Plan include a furnace tune-up?",
         "Yes. X-Plan includes a heating system safety checkup and service as one of its two "
         "seasonal visits, along with efficiency measurements, airflow adjustments and "
         "thermostat calibration. Membership is $249 a year or $20.75 a month."),
    ))

geo(HVAC_PAGES, "heat-pump.html",
    h1="Heat pump service for {X}.", h1Highlight="Ohio winters",
    intro="Heat pump repair, installation and tune-ups for Dayton and Cincinnati homes. "
          "Efficient heating and cooling from one system, with upfront pricing.",
    answer="We install, repair and tune up heat pumps across Dayton and Cincinnati, on every "
           "major brand. A modern cold-climate unit will heat through an Ohio winter, and a "
           "dual-fuel setup hands off to your gas furnace on the worst nights.",
    callout="Noticing more than one? Small heat pump problems become compressor problems. "
            "Call {tel}, or see what each symptom usually means on our "
            "<a href=\"/heat-pump-repair\">heat pump repair</a> page.",
    sections=[
        sec("Do heat pumps work in Ohio winters?",
            ["Yes. A heat pump moves heat rather than making it, and modern cold-climate "
             "models keep producing heat well below freezing, which covers most of an Ohio "
             "winter. On the coldest days a heat pump either leans on backup heat or, in a "
             "dual-fuel system, hands the job to a gas furnace.",
             "We set dual-fuel systems to switch from the heat pump to your "
             "<a href=\"/furnace-heating\">gas furnace</a> at a chosen outdoor temperature, "
             "so whichever source is cheaper is the one running."]),
        sec("Which system fits best: heat pump, furnace or dual fuel?",
            "It comes down to what fuel the house already has and how cold it gets where it "
            "sits. All-electric homes and homes without a gas line usually land on a heat "
            "pump. Homes with a working gas line often do best on dual fuel, which uses the "
            "heat pump most of the year and the furnace in a cold snap.",
            sid="system-comparison",
            table=tbl("Heat pump, gas furnace with air conditioning, and dual fuel compared "
                      "for Dayton and Cincinnati homes.",
                      "If your house already has a gas line, dual fuel is usually what we "
                      "recommend: the heat pump covers mild weather and the furnace covers "
                      "the coldest days.",
                      ["Factor", "Heat pump", "Gas furnace + AC", "Dual fuel"],
                      [("Winter performance",
                        "Heats efficiently down to low outdoor temperatures, then leans on backup heat",
                        "Full heat output at any outdoor temperature",
                        "Heat pump handles mild and moderate cold, furnace takes the coldest days"),
                       ("Summer cooling", "Included in the same outdoor unit",
                        "Handled by a separate air conditioner",
                        "Included in the same outdoor unit"),
                       ("Fuel needed", "Electricity only", "Natural gas plus electricity",
                        "Natural gas plus electricity"),
                       ("Equipment count", "One outdoor unit, one indoor air handler",
                        "Furnace plus a separate condenser",
                        "Heat pump outdoor unit plus a gas furnace indoors"),
                       ("Backup heat",
                        "Electric resistance strips, or none on a cold-climate model with enough capacity",
                        "Not applicable", "The gas furnace is the backup"),
                       ("Best fit", "Homes with no gas line, and all-electric homes",
                        "Homes with very cold design temperatures and cheap gas",
                        "Homes with an existing gas line that want lower shoulder-season running costs"),
                       ("Operating cost", "Depends on the local electric rate",
                        "Depends on the local gas rate",
                        "Lowest of the three when the switchover point is set correctly")])),
        sec("What is a cold-climate heat pump?",
            "A cold-climate heat pump uses a variable-speed compressor that keeps producing "
            "usable heat at low outdoor temperatures instead of falling off a cliff near "
            "freezing. Standard models lose capacity earlier and lean harder on electric "
            "backup heat, which is the part that shows up on a January electric bill.",
            table=tbl("Standard and cold-climate heat pumps compared.",
                      "A cold-climate heat pump holds its heating capacity to a much lower "
                      "outdoor temperature than a standard model, which is what keeps electric "
                      "backup heat from running through an Ohio winter.",
                      ["Factor", "Standard heat pump", "Cold-climate heat pump"],
                      [("Compressor", "Single-stage or two-stage", "Variable-speed inverter"),
                       ("Heat output as it gets colder", "Falls off sooner, closer to freezing",
                        "Holds capacity to a much lower outdoor temperature"),
                       ("Backup heat use",
                        "Runs electric resistance heat often through an Ohio winter",
                        "Runs backup heat rarely, mostly in the coldest snaps"),
                       ("Comfort", "Noticeable temperature swings on cold days",
                        "Steadier supply air, longer run cycles"),
                       ("Best fit in this region",
                        "Shoulder-season heating with a gas furnace as the primary",
                        "Whole-winter heating, or dual fuel with a high switchover point")])),
        sec("What heat pump work do you handle?",
            "Repair, replacement and seasonal tune-ups on every major brand, plus dual-fuel "
            "conversions for homes that already have a gas furnace. We test in both heating "
            "and cooling mode, which matters because your heat pump runs about twice the "
            "hours an air conditioner does."),
    ],
    sectionsTail=[
        sec("What are the signs a heat pump is failing?",
            "Air that never reaches the set temperature, ice that stays on the outdoor unit "
            "after a defrost cycle, running constantly or short cycling, grinding or "
            "squealing, and a jump in the electric bill that usually means backup heat is "
            "running when it should not be. Each of those is diagnosed on our "
            "<a href=\"/heat-pump-repair\">heat pump repair</a> page."),
        sec("How long does a heat pump last?",
            "Twelve to fifteen years is normal, a little shorter than an "
            "<a href=\"/air-conditioning\">air conditioner</a> because a heat pump runs "
            "year-round instead of four months. Annual servicing matters more here than on "
            "any other system in the house for exactly that reason, which is what the "
            "<a href=\"/maintenance\">X-Plan maintenance membership</a> is built around."),
        sec("How do I book heat pump service?",
            call("Call {tel} or schedule online, and you get an arrival window up front. Most "
                 "calls are handled the same day, and a house with no heat gets the emergency "
                 "line at any hour. Replacement estimates book the same way, through "
                 "<a href=\"/heat-pump-installation\">heat pump installation</a>.")),
    ],
    faqH2="What else do homeowners ask about heat pumps?",
    faq=qa(
        ("Why is my heat pump covered in ice in winter?",
         "A light coat of frost is normal. Heat pumps run a defrost cycle every so often, and "
         "the outdoor unit steams and drips while it does. Ice that stays thick after a "
         "defrost cycle, or ice that encases the fan, is a fault worth a call."),
        ("What does emergency heat mean on my thermostat?",
         "Emergency heat shuts the heat pump off and runs the backup heat alone, which is the "
         "most expensive way to heat a house. It is meant for a broken heat pump, not for a "
         "cold day. If a <a href=\"/thermostat\">thermostat</a> is stuck in emergency heat, "
         "the system needs to be looked at."),
        ("Can a heat pump replace my furnace?",
         "In many Ohio homes, yes, and in homes with an existing gas line a dual-fuel setup "
         "usually makes more sense than removing the furnace. The deciding factors are the "
         "home's insulation, the electrical service, and whether the ductwork can carry the "
         "higher airflow a heat pump needs."),
        ("Are there federal tax credits for heat pumps in 2026?",
         "No. The Section 25C and 25D federal credits both expired on 31 December 2025. Any "
         "page still advertising a $2,000 federal heat pump credit is out of date."),
        ("Will a heat pump work with my existing ductwork?",
         "Sometimes, and it gets measured rather than assumed. Heat pumps move more air at a "
         "lower supply temperature than a furnace, so undersized returns show up as noise and "
         "cold spots. Static pressure gets tested during the estimate."),
    ))

geo(HVAC_PAGES, "duct-cleaning.html",
    h1="Air duct cleaning for {X}.", h1Highlight="Dayton &amp; Cincinnati homes",
    intro="Professional duct cleaning and air balancing for Dayton and Cincinnati homes. "
          "Better airflow, less dust, upfront pricing.",
    answer="We clean air ducts with truck-powered vacuum equipment, on every supply and return "
           "run in the house. Your ducts get photographed before and after, so you can see the "
           "difference instead of taking our word for it.",
    callout="Remodeling dust, pets, or allergies? Call {tel} and we'll tell you honestly "
            "whether cleaning will help.",
    sections=[
        sec("Is air duct cleaning actually worth the money?",
            ["Sometimes, and the honest answer depends on what is in the ducts. The EPA does "
             "not recommend cleaning ducts on a routine schedule, but it does recommend "
             "cleaning when there is visible mould growth, vermin, or enough dust and debris "
             "to be blown into the house. Those three conditions are the test.",
             "So we photograph the ducts before we start and again when we finish. You look "
             "at the pictures and decide for yourself whether the money did anything."]),
        sec("When does duct cleaning help, and when does it not?",
            "Cleaning removes what has built up inside the duct. It does not change how the "
            "duct was built, sealed or sized, so a house with leaky returns or an undersized "
            "trunk line will still have the same comfort problem after a spotless cleaning.",
            table=tbl("What duct cleaning fixes in a house, and what it does not.",
                      "Cleaning takes out the dust, debris and growth sitting in the ducts. It "
                      "will not fix a leak, a bad duct layout, or a return that is too small "
                      "for the system.",
                      ["What you are seeing", "What duct cleaning does", "What actually fixes it"],
                      [("Visible dust blowing from the vents",
                        "Removes the loose debris being picked up in the ducts",
                        "Duct cleaning, plus a better filter"),
                       ("Musty smell when the system starts",
                        "Removes biological growth and debris inside the ducts",
                        "Duct cleaning, plus finding the moisture source"),
                       ("One room never gets warm or cool",
                        "Nothing, unless the run is fully blocked",
                        "Air balancing, or duct repair and resizing"),
                       ("Dust settles again within days of dusting",
                        "Reduces what recirculates through the system",
                        "Duct cleaning, plus higher-efficiency filtration"),
                       ("Debris left from a remodel",
                        "Removes drywall dust and construction debris from the runs",
                        "Duct cleaning after the work is finished"),
                       ("Allergy symptoms indoors",
                        "Removes settled dust, dander and pollen from the ducts",
                        "Duct cleaning, plus filtration and source control"),
                       ("Dryer takes two cycles to dry a load",
                        "Nothing, that is a separate duct", "Dryer vent cleaning")])),
        sec("How often should air ducts be cleaned?",
            "Every 3 to 5 years suits most homes. Sooner if there are shedding pets, a recent "
            "remodel, a smoker in the house, or allergies that flare indoors and nowhere "
            "else. A house that has never had its ducts cleaned is usually worth a look "
            "regardless of the calendar."),
        sec("What do you actually clean?",
            "Every supply and return run, the main trunk lines, and the registers and grilles. "
            "The truck-powered vacuum pulls while a brush agitates the duct wall to release "
            "what is stuck to it. You get before and after photos, and the house is left the "
            "way we found it."),
    ],
    sectionsTail=[
        sec("Does duct cleaning help with allergies?",
            "It can. Removing built-up dust, dander and pollen reduces what the system "
            "recirculates, which is the part of the problem that lives in the ducts. Pairing "
            "it with <a href=\"/indoor-air-quality-solutions\">filtration and purification "
            "options</a> does more than either one alone, and source control does more than "
            "both."),
        sec("How do I book duct cleaning?",
            call("Call {tel} or schedule online. We will tell you whether cleaning is likely "
                 "to help before you book it, and the photos come with the job either way. If "
                 "<a href=\"/indoor-air-quality\">air quality work</a> or a "
                 "<a href=\"/humidifier\">whole-home humidifier</a> would do more for you, we "
                 "will price that on the same visit.")),
    ],
    faqH2="What else do homeowners ask about duct cleaning?",
    faq=qa(
        ("Does duct cleaning improve airflow?",
         "Only when the ducts were genuinely restricted. Heavy debris in a run does cut "
         "airflow, and removing it helps. A duct that is undersized or badly laid out will "
         "move exactly as much air after cleaning as before, which is an air balancing job "
         "instead."),
        ("Should ducts be cleaned after a remodel?",
         "Yes, once the work is finished. Drywall dust is fine enough to travel the whole duct "
         "system and it keeps recirculating for months. Cleaning before the last of the "
         "sanding is done just means doing it twice."),
        ("Do you clean dryer vents as well?",
         "Yes, and it is often done on the same visit. A clogged dryer vent shows up as "
         "clothes needing two cycles to dry, and it is a fire risk rather than an air quality "
         "one."),
        ("Will duct cleaning make the house less dusty?",
         "It cuts what the system blows back out, which is a real share of household dust but "
         "not all of it. Filtration and sealing the return side handle the rest, and we will "
         "tell you which one your house actually needs."),
        ("Is duct sealing the same as duct cleaning?",
         "No. Cleaning removes what is inside the duct. Sealing closes the gaps where "
         "conditioned air escapes into an attic or crawlspace before it ever reaches a room. "
         "A house can need one, both, or neither."),
    ))

geo(HVAC_PAGES, "indoor-air-quality.html",
    h1="Indoor air quality services for {X}.", h1Highlight="your home",
    intro="Filtration, purification and humidity control for Dayton and Cincinnati homes. "
          "Cleaner air from the team you already trust.",
    answer="Filtration, UV purification, ventilation and humidity control, aimed at whatever "
           "is actually wrong in your house. We find the source first. Nobody gets sold a "
           "package because it was next on the list.",
    callout="Air quality problems compound quietly. Call {tel} and we'll find the source, "
            "not just the symptom.",
    sections=[
        sec("How do I improve the air quality in my house?",
            ["In this order: control the source, then filter, then purify. Sealing a mouldy "
             "crawlspace does more than any purifier will, a better filter does more than a "
             "UV lamp, and the equipment only earns its keep once the first two are handled. "
             "Anyone selling the order backwards is selling equipment.",
             "So that is the order we work in: source, then filter, then purify. The hardware "
             "for each step sits side by side on our "
             "<a href=\"/indoor-air-quality-solutions\">filtration, UV and ventilation "
             "options</a> page."]),
        sec("What are the signs of poor indoor air quality?",
            "Allergies that flare indoors and settle outdoors, dust that returns within a day "
            "of cleaning, odours that linger, a house that is humid in summer and static-dry "
            "in winter, musty smells near returns, and everyone sleeping better away from "
            "home. Any one of those on its own means little. Four at once is a pattern, and "
            "<a href=\"/importance-iaq\">why indoor air quality matters</a> covers what is "
            "behind them."),
        sec("Which air quality problem does your home actually have?",
            "Different symptoms point at different sources, and the fix follows the source "
            "rather than the symptom. The table below is how a tech narrows it down on a "
            "first visit.",
            table=tbl("Indoor air quality symptoms and their usual sources.",
                      "We work backwards from the symptom, because the same complaint can come "
                      "from a cheap filter, a leaking return, or standing water under the "
                      "house.",
                      ["What you are noticing", "Likely source", "What usually fixes it"],
                      [("Dust returns within a day of cleaning",
                        "Low-efficiency filter, or return-side duct leaks",
                        "Higher-efficiency media filtration and duct sealing"),
                       ("Musty smell when the system starts",
                        "Biological growth on the evaporator coil or in the ducts",
                        "Coil cleaning, UV at the coil, duct cleaning"),
                       ("Humid, clammy air in summer",
                        "Oversized air conditioner short-cycling, or high infiltration",
                        "Correct sizing, or whole-home dehumidification"),
                       ("Static shocks and dry sinuses in winter",
                        "Very low indoor relative humidity",
                        "Whole-home humidifier sized to the house"),
                       ("Stale air, odours that will not clear",
                        "Not enough fresh-air ventilation in a tight house",
                        "Mechanical ventilation"),
                       ("Allergy symptoms indoors only",
                        "Pollen, dander and dust recirculating through the system",
                        "Filtration upgrade, duct cleaning, source control"),
                       ("Visible mould near a register or crawlspace",
                        "Standing water or a moisture path, not an air problem",
                        "Fix the moisture source first, then treat the air")])),
        sec("What can you install?",
            "Media filtration, UV purification at the coil, whole-home humidification and "
            "dehumidification, fresh-air ventilation, coil cleaning and "
            "<a href=\"/duct-cleaning\">duct cleaning</a>. All of it goes into the system you "
            "already own, and we take readings before and after instead of promising you a "
            "result."),
    ],
    sectionsTail=[
        sec("Do UV lights in HVAC systems work?",
            "Against biological growth on a wet evaporator coil, yes, when the lamp is sized "
            "and aimed correctly and the bulb gets replaced on schedule. Against dust, pollen "
            "and dander, no. Those are particles, and particles are a filter's job. Anyone "
            "selling UV as an allergy fix is overselling it. More of the same ground is "
            "covered in our <a href=\"/iaq-faq\">common filter and MERV questions</a>."),
        sec("What humidity should an Ohio home hold?",
            "Between 30 and 50% relative humidity. Nearer 30 to 35% in deep winter, because "
            "higher than that condenses on cold windows and does damage in the wall behind "
            "them. Nearer 45 to 50% in summer, which is dry enough that the house feels cool "
            "without overcooling it. A <a href=\"/humidifier\">whole-home humidifier "
            "installation</a> is what holds the winter end of that range."),
        sec("How do I book air quality help?",
            call("Call {tel} or schedule online. We find the source before recommending "
                 "equipment, and most calls are handled the same day. Filter and pad changes "
                 "come with the <a href=\"/maintenance\">X-Plan maintenance membership</a> "
                 "visits.")),
    ],
    faqH2="What else do homeowners ask about indoor air?",
    faq=qa(
        ("Where do you start when the whole house feels stuffy?",
         "With the return side and the filter, then humidity, then ventilation. A stuffy house "
         "is usually one sealed tighter than its ventilation was designed for. We take the "
         "readings before recommending anything."),
        ("Can indoor air quality be measured before and after?",
         "Yes. Temperature, relative humidity, static pressure and particulate readings all "
         "get taken on the visit, and again after the work. That is the only way to tell "
         "whether the money did anything."),
        ("Does an air purifier replace a good filter?",
         "No. A purifier and a filter do different jobs. The filter captures particles moving "
         "through the system, and the purifier targets biological growth and some gases. A "
         "purifier on top of a dirty filter accomplishes very little."),
        ("Does duct cleaning count as an air quality fix?",
         "It is one piece of one. Cleaning removes what has settled in the ducts, and "
         "filtration keeps new material from settling there again. They work better together "
         "than either does alone."),
        ("Does X-Plan include air quality checks?",
         "The two seasonal X-Plan visits include a detailed evaluation with efficiency "
         "measurements, airflow adjustments and thermostat calibration, and members get a "
         "discount on indoor air quality work and duct cleaning."),
    ))

geo(HVAC_PAGES, "maintenance.html",
    h1="X-Plan: the HVAC maintenance plan for {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Two seasonal tune-ups a year, priority scheduling, 15% off repairs, and a 5-year "
          "repair warranty. $249 a year or $20.75 a month.",
    answer="X-Plan costs $249 a year, or $20.75 a month. You get two seasonal tune-ups, 15% "
           "off every repair, a reduced service fee and a spot at the front of the line when "
           "the weather turns and everyone calls at once.",
    callout="Questions about membership or billing? Call {tel} and we'll walk you through it.",
    sections=[
        sec("What is X-Plan?",
            "A maintenance membership. It bundles the two tune-ups your system needs each year "
            "with member pricing on repairs, a longer repair warranty, and a place at the "
            "front of the line when the weather turns and the phones light up."),
        sec("What does it cost?",
            "$249 a year, or $20.75 a month per system. That covers both seasonal visits, 15% "
            "off every repair, a reduced service fee including after hours and holidays, "
            "priority scheduling, and a 5-year warranty on qualified repairs. Bigger "
            "replacements can run through <a href=\"/financing-options\">financing</a> "
            "instead."),
        sec("What happens on a tune-up visit?",
            "A full system inspection and safety check, capacitor, relay and thermostat "
            "testing, compressor amp draws, drain line cleaning, a pressure check, light coil "
            "cleaning, refrigerant charge calibration up to 1 lb, airflow adjustment and "
            "efficiency readings. One visit covers "
            "<a href=\"/air-conditioning\">your air conditioning</a>, the other covers "
            "<a href=\"/furnace-heating\">your furnace</a>."),
        sec("How does the Zero Risk Investment work?",
            "You accrue 100% of what you have paid in toward replacing the equipment when it "
            "reaches the end of its life, in consecutive years, capped at $2,500 or 10 years. "
            "It follows you, not the house. Consecutive is the word that matters: let the "
            "membership lapse and the clock starts over."),
    ],
    sectionsTail=[
        sec("Is X-Plan worth it compared with paying per visit?",
            "It depends on how often you would book a tune-up anyway. Two visits a year, at "
            "member pricing, plus 15% off any repair, is the arithmetic most members are "
            "running. Priority scheduling is what they mention in July.",
            table=tbl("X-Plan membership compared with paying per visit.",
                      "Membership gets you two seasonal visits a year, 15% off repairs and a "
                      "5-year repair warranty. None of those apply to a one-off service call.",
                      ["What you get", "X-Plan member", "Non-member"],
                      [("Seasonal safety and performance visits", "Two per year, included",
                        "Booked and billed individually"),
                       ("Repair pricing", "15% off all repairs", "Standard repair pricing"),
                       ("Service fee", "Reduced member rate, including after hours and holidays",
                        "Standard rate"),
                       ("Scheduling", "Extreme Priority Scheduling", "Standard scheduling"),
                       ("Repair warranty", "5-year warranty on qualified repairs",
                        "Standard warranty"),
                       ("Accrual toward the next system",
                        "100% of the membership investment in consecutive years, up to $2,500 or 10 years",
                        "None"),
                       ("Indoor air quality and duct cleaning", "Member discount",
                        "Standard pricing"),
                       ("Price", "$249 a year or $20.75 a month", "Priced per visit")])),
        sec("How often should HVAC equipment be serviced?",
            "Twice a year for a house with separate heating and cooling equipment: cooling in "
            "spring, heating in fall. Once a year is the bare minimum and it usually means "
            "skipping whichever season is further away. A "
            "<a href=\"/heat-pump\">heat pump</a> wants both visits, because it runs "
            "year-round."),
        sec("How do I join?",
            call("Call {tel} or sign up online, and we schedule the first visit on the same "
                 "call. After that we book both seasonal visits for you, so the membership "
                 "does not depend on you remembering it. Send us a neighbor and there is "
                 "<a href=\"/referral\">Extreme Rewards</a> too.")),
    ],
    faqH2="What else do members ask about X-Plan?",
    faq=qa(
        ("Does X-Plan cover both heating and cooling?",
         "Yes. One visit each season, covering the full system: a multi-point air conditioner "
         "tune-up in spring and a heating safety checkup in fall. Both are included in the "
         "$249 a year or $20.75 a month membership."),
        ("What if the house has two HVAC systems?",
         "The monthly price is per system, so a two-system house carries two memberships and "
         "gets two sets of seasonal visits."),
        ("Do members get a discount on repairs?",
         "Yes, 15% off all repairs, on every visit, plus a reduced member service fee that "
         "also applies after hours and on holidays. Qualified repairs carry a 5-year warranty."),
        ("Do I have to remember to book the visits?",
         "No. We schedule the spring and fall visits and call you to confirm the window."),
        ("What does the accrual actually pay for?",
         "You accrue 100% of what you have paid in toward end-of-life equipment replacement, "
         "in consecutive years, capped at $2,500 or 10 years. It applies when the equipment "
         "gets replaced, and a lapse restarts it. A full "
         "<a href=\"/inspection\">HVAC inspection</a> documents that the system has reached "
         "that point."),
    ))

geo(HVAC_PAGES, "inspection.html",
    h1="HVAC inspection for {X}.", h1Highlight="homes and home buyers",
    intro="Full-system HVAC inspections for home purchases, seasonal checkups, and honest "
          "second opinions.",
    answer="We open the equipment up and take readings: combustion safety, refrigerant, "
           "electrical, airflow, ductwork. It all gets photographed. You get the findings in "
           "plain English, sorted into what is unsafe, what is urgent, and what can wait.",
    callout="Want eyes on it before you commit? Call {tel} and we'll tell you what's real and "
            "what can wait.",
    sections=[
        sec("What does an HVAC inspection include?",
            "Combustion safety and carbon monoxide testing, refrigerant performance, "
            "electrical components, airflow and static pressure, and the condition of the "
            "ductwork. Everything gets photographed, and the report says what is a safety "
            "issue, what needs doing this year, and what can wait."),
        sec("What does an HVAC inspection cover that a home inspection does not?",
            "A home inspection is a visual, non-invasive look at the whole house, and its "
            "standards of practice specifically exclude taking equipment apart or testing "
            "refrigerant. An HVAC inspection opens the equipment and takes readings, which is "
            "where the expensive findings live.",
            table=tbl("A general home inspection compared with a dedicated HVAC inspection.",
                      "A home inspection tells you the equipment turns on. An HVAC inspection "
                      "tells you what shape the parts inside it are in.",
                      ["What gets checked", "General home inspection", "HVAC inspection"],
                      [("Does the system turn on and produce heat or cool air", "Yes", "Yes"),
                       ("Heat exchanger inspected for cracks",
                        "Not typically, the standards exclude disassembly",
                        "Yes, with the cabinet opened"),
                       ("Combustion and carbon monoxide testing", "Not typically",
                        "Yes, with a combustion analyzer"),
                       ("Refrigerant charge and pressures",
                        "Not typically, gauges are not attached",
                        "Yes, measured at the service ports"),
                       ("Electrical components tested under load", "Visual check only",
                        "Capacitors, contactors and amp draws measured"),
                       ("Airflow and static pressure", "Not typically",
                        "Measured across the system"),
                       ("Ductwork condition and leakage", "Visible sections only",
                        "Accessible runs inspected and photographed"),
                       ("Written findings", "Included in the whole-house report",
                        "Photo-documented and sorted by safety, urgency and cost"),
                       ("Repair estimate", "Not provided", "Provided")])),
        sec("Do I need an HVAC inspection before buying a house?",
            ["If the system is more than about ten years old, or if the seller has no service "
             "records, it pays for itself in one finding. A cracked heat exchanger or a "
             "failing compressor found before closing is a negotiation. Found after closing, "
             "it is a bill.",
             "The report is written to be shared. Photos, plain-English findings and a repair "
             "estimate are all in one document, so it can go straight to a realtor or into a "
             "repair request without translation."]),
        sec("How do I know if my heat exchanger is cracked?",
            ["You mostly cannot, from the outside, which is why it gets tested rather than "
             "guessed at. The warning signs are a yellow or flickering burner flame, soot "
             "around the burner compartment, a carbon monoxide alarm, and headaches or nausea "
             "that clear when everyone leaves the house.",
             "Any of those together with a smell of gas means leaving the building first and "
             "calling from outside. Someone answers at any hour, and "
             "<a href=\"/furnace-heating\">furnace and heating service</a> covers the repair "
             "once the house is safe."]),
    ],
    sectionsTail=[
        sec("Is an inspection the same as a tune-up?",
            "No. An inspection documents condition. A tune-up services the equipment. The two "
            "overlap on the testing, and they answer different questions: one tells you what "
            "shape the system is in, the other keeps it in shape. The "
            "<a href=\"/maintenance\">X-Plan maintenance membership</a> includes both, twice "
            "a year."),
        sec("How do I book an inspection?",
            call("Call {tel} or schedule online. If it is for a purchase, we work around your "
                 "closing date. Most calls are handled the same day, and the same visit can "
                 "pick up <a href=\"/air-conditioning\">air conditioning service</a>, "
                 "<a href=\"/duct-cleaning\">duct cleaning</a> or "
                 "<a href=\"/indoor-air-quality\">air quality work</a> if the findings point "
                 "that way.")),
    ],
    faqH2="What else do buyers and owners ask about inspections?",
    faq=qa(
        ("Can you inspect a system before I close on a house?",
         "Yes, and it is one of the most common reasons people book one. We schedule around "
         "inspection deadlines, and the report is written so it can go straight to your "
         "realtor or into a repair request."),
        ("Will you give a second opinion on another company's quote?",
         "Yes. Bring the quote. The inspection covers the same components, so you can compare "
         "the findings line by line. There is no obligation to have the work done by us."),
        ("What happens if the inspection finds a safety problem?",
         "You are told on the spot, before anything else in the report. Combustion and carbon "
         "monoxide findings come first, in plain English, with what needs to happen and how "
         "soon. Emergency service runs 24/7 if it cannot wait."),
        ("Can the report be shared with my realtor?",
         "Yes. Photos, findings and the repair estimate are in one document meant to be "
         "forwarded, which is the point of having it in writing."),
        ("How old does a system have to be to justify an inspection?",
         "About ten years is the usual line, or any age with no service records behind it. A "
         "newer system with a documented maintenance history rarely needs one outside of a "
         "home purchase."),
    ))

geo(HVAC_PAGES, "thermostat.html",
    h1="Smart thermostat installation and repair in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="Smart thermostat installation, setup and troubleshooting. More comfort and lower "
          "bills from the system you already own.",
    answer="We install, set up and repair thermostats of any brand, Nest and ecobee and "
           "Honeywell included. We check your wiring and staging before you buy anything, and "
           "run a heating and a cooling cycle before we leave.",
    callout="Thermostat acting up? It's often the cheapest fix in HVAC. Call {tel} before "
            "assuming the worst.",
    sections=[
        sec("What thermostat work do you handle?",
            "Installing and setting up smart, programmable and conventional thermostats, and "
            "figuring out why one has stopped driving the equipment. Any brand. We check "
            "compatibility against the system actually in your house first, then run a heating "
            "and a cooling cycle before leaving."),
        sec("Can a smart thermostat be installed without a C-wire?",
            ["Yes, in most homes. The C-wire carries continuous power, and smart thermostats "
             "need it. Where one was never run, the fix is either an adapter at the furnace "
             "board, repurposing an unused conductor in the existing cable, or running new "
             "thermostat wire. All three are routine.",
             "If your wall has no C-wire, we either add a power adapter at the furnace board "
             "or pull new thermostat cable. It is not a reason to give up on the thermostat "
             "you wanted."]),
        sec("Which smart thermostat works with my system?",
            "The thermostat has to match the equipment, not the other way round. Single-stage "
            "gas heat takes almost anything. Heat pumps, multi-stage equipment and zoned "
            "systems narrow the list quickly, and line-voltage electric heat rules most smart "
            "thermostats out entirely.",
            table=tbl("Thermostat compatibility by system type.",
                      "What you can install is decided by your equipment and the wiring already "
                      "at the wall, not by the feature list on the box.",
                      ["What you have", "What it means", "What can be installed"],
                      [("A C-wire already at the thermostat",
                        "Continuous power is available at the wall",
                        "Any mainstream smart thermostat"),
                       ("No C-wire, standard furnace",
                        "The thermostat has no steady power source",
                        "A smart thermostat, with a power adapter at the furnace board or new cable"),
                       ("Heat pump with auxiliary or emergency heat",
                        "The thermostat has to control the changeover and the backup heat",
                        "A heat pump capable smart thermostat, configured for the correct staging"),
                       ("Two-stage or variable-speed equipment",
                        "Extra conductors are needed to drive each stage",
                        "A multi-stage smart thermostat, wiring permitting"),
                       ("Millivolt or heat-only system",
                        "There is no 24-volt transformer to power a thermostat",
                        "A compatible millivolt thermostat, not a standard smart model"),
                       ("Line-voltage electric baseboard",
                        "The thermostat switches 120 or 240 volts directly",
                        "A line-voltage thermostat only"),
                       ("A zoned system with multiple thermostats",
                        "Each zone is driven through a zone control panel",
                        "Matched thermostats compatible with the existing panel")])),
        sec("Why is my thermostat not turning on the furnace?",
            "The common causes are a dead battery, a tripped breaker, a blown low-voltage fuse "
            "on the furnace board, a loose or corroded wire at the terminal, or a furnace door "
            "switch that is not seated. Check the battery and the breaker first, since neither "
            "costs anything to rule out. If the heat still will not run, "
            "<a href=\"/furnace-heating\">furnace and heating service</a> takes it from there."),
    ],
    sectionsTail=[
        sec("Can a new thermostat lower my energy bills?",
            "Some. The saving comes from schedules, setbacks and occupancy sensing rather than "
            "from the hardware itself, so it depends on how the house was being run before. A "
            "thermostat that is set and then ignored saves nothing, which is why the schedule "
            "gets built with you before we leave."),
        sec("How do I book thermostat service?",
            call("Call {tel} or schedule online. Most calls are handled the same day, and a "
                 "thermostat that has stopped driving the heat counts as a no-heat call. We "
                 "also check staging on <a href=\"/heat-pump\">heat pump service</a> visits "
                 "and during a full <a href=\"/inspection\">HVAC inspection</a>.")),
    ],
    faqH2="What else do homeowners ask about thermostats?",
    faq=qa(
        ("Is it more likely the thermostat or the furnace?",
         "The thermostat is the cheaper thing to rule out, so it gets checked first. A blank "
         "display usually points at power: batteries, a tripped breaker, or the low-voltage "
         "fuse on the furnace board. Heat that runs but never reaches the set temperature is "
         "usually not the thermostat."),
        ("Can you install a thermostat I already bought?",
         "Yes. Bring it out of the box and the compatibility check happens on the visit. If it "
         "turns out not to suit the equipment, you will hear that before anything gets wired."),
        ("Do smart thermostats work with heat pumps?",
         "Yes, provided the model supports heat pump staging and auxiliary heat, and it is "
         "configured for it. A heat pump thermostat set up as if it were a gas furnace will "
         "run backup heat far more than it should, which shows up on the electric bill."),
        ("What about a house with several thermostats?",
         "That is a zoned system, and the thermostats have to match the zone control panel "
         "already installed. Replacing one zone thermostat with a mismatched model is the "
         "usual cause of one room going haywire after a DIY swap."),
        ("Does a new furnace need a new thermostat?",
         "Not always, but a two-stage or variable-speed furnace can only run its extra stages "
         "if the thermostat can drive them. That gets checked during the installation estimate "
         "rather than discovered afterwards."),
    ))

geo(HVAC_PAGES, "humidifier.html",
    h1="Whole-home humidifier installation for {X}.", h1Highlight="Ohio winters",
    intro="Whole-home humidifier installation and service. End dry winter air, static shocks, "
          "and cracked wood floors.",
    answer="Static shocks, cracked trim, waking up congested. That is what an Ohio winter does "
           "to indoor air. We fit bypass, fan-powered and steam humidifiers, sized to your "
           "house, and set them to hold 30 to 40% through the heating season.",
    callout="Dry air is hardest on homes in an Ohio winter. Call {tel} and we'll size the "
            "right solution.",
    sections=[
        sec("Why is my house so dry every winter?",
            "Cold outdoor air holds very little moisture, and heating it makes the relative "
            "humidity indoors drop further. A leaky house pulls more of that dry air in, so "
            "the driest houses in a Dayton January are usually the oldest ones. Nothing about "
            "the <a href=\"/furnace-heating\">furnace</a> causes it."),
        sec("What humidity should a house hold in winter?",
            "Between 30 and 40% through most of the heating season, dropping toward 30% in a "
            "hard freeze. Higher than that condenses on cold window glass and does damage "
            "inside the wall behind it, which is why a whole-home humidifier is set by outdoor "
            "temperature rather than left on one number."),
        sec("Which whole-home humidifier type fits my furnace?",
            "Three types cover almost every house, and the choice comes down to how much "
            "moisture the house needs and how the heating system delivers air. Bypass units "
            "are the simplest. Steam units are the only ones that do not care whether the "
            "furnace is running.",
            table=tbl("Whole-home humidifier types compared.",
                      "We match the type to the size of your house and the kind of heating "
                      "system you have, not to whatever is on the van that day.",
                      ["Factor", "Bypass", "Fan-powered", "Steam"],
                      [("How it works", "Furnace airflow is routed across a wet pad",
                        "A built-in fan pushes air across the wet pad",
                        "Water is boiled and the vapour is injected into the supply duct"),
                       ("Moisture output", "Lowest of the three", "Higher than bypass",
                        "Highest, by a wide margin"),
                       ("Needs the furnace to be running",
                        "Yes, and it needs warm supply air",
                        "Yes, though it works with less airflow",
                        "No, it makes its own heat"),
                       ("Fit with a heat pump or air handler", "Poor, supply air is too cool",
                        "Workable in some systems",
                        "Best fit, and usually the only one that performs"),
                       ("Best fit", "Smaller, tighter homes with a gas furnace",
                        "Average homes with a gas furnace and limited duct space",
                        "Large homes, very dry homes, and heat pump systems"),
                       ("Maintenance", "Annual pad change and cleaning",
                        "Annual pad change and cleaning",
                        "Annual cylinder or canister service")])),
        sec("Is a whole-home humidifier better than portable units?",
            "For a whole house, yes. A portable unit humidifies one room, needs filling by "
            "hand, and gets turned off when it is inconvenient. A whole-home unit plumbs into "
            "the water supply, runs off the thermostat or its own control, and treats every "
            "room the ductwork reaches, which is also why "
            "<a href=\"/duct-cleaning\">air duct cleaning</a> is worth doing first if the "
            "ducts have never been cleaned."),
    ],
    sectionsTail=[
        sec("Do whole-home humidifiers need yearly maintenance?",
            "Yes, once a year. The evaporator pad or the steam canister gets replaced, the "
            "water panel and drain get cleaned, and the humidistat gets checked. Skipping it "
            "is how a humidifier turns into a mineral-clogged box that runs water down the "
            "drain and adds nothing to the air. "
            "<a href=\"/maintenance\">X-Plan maintenance membership</a> visits cover it."),
        sec("Does a humidifier help with dry skin and static?",
            "Static shocks stop almost immediately once indoor humidity gets back above about "
            "30%, because static needs dry air to build up. Dry skin, cracked lips and morning "
            "congestion generally ease as well. Wood floors and trim stop opening up at the "
            "seams, which is the expensive part."),
        sec("How do I book humidifier service?",
            call("Call {tel} or schedule online. We size the humidifier to your house before "
                 "quoting one, and most calls are handled the same day. Summer is the other "
                 "half of this problem, so "
                 "<a href=\"/indoor-air-quality-solutions\">whole-home dehumidification</a> "
                 "and wider <a href=\"/indoor-air-quality\">air quality work</a> get quoted "
                 "the same way.")),
    ],
    faqH2="What else do homeowners ask about humidifiers?",
    faq=qa(
        ("Will a humidifier cause condensation on my windows?",
         "It can, if the setting is too high for how cold it is outside. Condensation on the "
         "glass is the signal to turn the humidity down, not up. A humidistat that adjusts "
         "with outdoor temperature prevents most of it automatically."),
        ("Can a humidifier be added to a heat pump system?",
         "Yes, and a steam unit is usually the right choice. Heat pumps deliver cooler supply "
         "air than a gas furnace, so a bypass humidifier has too little heat to evaporate much "
         "water and underperforms all winter."),
        ("How often does the humidifier pad need changing?",
         "Once a heating season for most homes, and more often on very hard water. We handle "
         "the pad change and cleaning during X-Plan visits."),
        ("Does the humidifier run in summer?",
         "No. The water supply gets shut off and the damper closed at the end of the heating "
         "season, then opened again in fall. Leaving it running in summer adds moisture the "
         "air conditioner then has to remove."),
        ("Does X-Plan include humidifier service?",
         "The seasonal visits cover the humidifier along with the rest of the system, and "
         "members get 15% off any repair. Membership is $249 a year or $20.75 a month."),
    ))

# ======================================================================
# HVAC sub-pages
# ----------------------------------------------------------------------
# The sub-page hero chips come from template.SUB_CHIPS, not from this file,
# so the "4.9 on Google" correction cannot be made here. See the handoff.
# ======================================================================

geo(HVAC_SUBS, "ac-repair.html",
    h1="AC repair in {X}, day or night.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Cool air back, usually the same day. We diagnose fast, quote flat before any work "
          "starts, and repair every make and model, with the emergency line answered 24/7.",
    answer="AC out? We repair every make and model across Dayton and Cincinnati, most of them "
           "the same day. You get a flat price before we start, and the emergency line is "
           "answered at any hour.",
    sections=[
        sec("What happens on an AC repair visit?",
            "We diagnose before we quote. That means reading pressures, checking the "
            "temperature split at the supply and return, going over the electrical side, and "
            "finding the actual failure. Then you get a price, and nothing comes off the truck "
            "until you approve it. The <a href=\"/air-conditioning\">air conditioning "
            "overview</a> covers tune-ups and replacement.",
            h3s=[("What gets checked first",
                  "Refrigerant pressures, the contactor and capacitor, the condenser fan "
                  "motor, the blower, the condensate drain, and airflow across the evaporator "
                  "coil. Most calls that come in as \"the AC quit\" end at one of those six."),
                 ("What happens after the repair",
                  "We run the system and measure it. You get the temperature split at the "
                  "register confirmed before we leave, so the fix is verified rather than "
                  "assumed.")]),
        sec("Why is my air conditioner blowing warm air?",
            "Warm air from a running system usually means one of four things: a dirty or iced "
            "evaporator coil, low refrigerant from a leak, a failed capacitor stopping the "
            "compressor, or a <a href=\"/thermostat\">thermostat</a> calling for the fan "
            "without calling for cooling. The outdoor unit running is not proof the "
            "compressor is running.",
            h3s=[("When to shut the system off",
                  "Ice on the refrigerant line or the indoor coil means airflow or refrigerant "
                  "is wrong, and running the system that way is how a repair turns into a "
                  "compressor replacement. Switch the cooling off and leave the fan running so "
                  "the ice melts before anyone looks at it.")]),
        sec("Can someone come out today?",
            "Usually, yes. About nine calls in ten get handled the day you reach out, and the "
            "emergency line is answered at any hour. If you have no cooling in a heat wave, "
            "you go ahead of routine work."),
    ],
    table=tbl("Repair or replace an air conditioner: what decides it.",
              "Once a system is 12 years or older and the repair quote gets near a third of "
              "what a new one costs, replacement is usually the better money.",
              ["What we look at", "Repair when", "Replace when"],
              [("System age", "Under 12 years old", "12 years or older"),
               ("Failed part", "Capacitor, contactor, fan motor, or control board",
                "Compressor or evaporator coil"),
               COST_ROW, R22_ROW,
               ("Breakdown history", "First failure in several seasons",
                "Second or third service call in one summer"),
               ("Energy bills", "Steady year over year",
                "Climbing with no change in how the house is used"),
               ("Comfort", "One room or one symptom affected",
                "Uneven temperatures throughout the house")],
              h2="Should I repair or replace my air conditioner?", sid="repair-or-replace",
              eyebrow="REPAIR OR REPLACE"),
    sectionsTail=[
        sec("Is the repair covered by a warranty?",
            "Our work is backed by a satisfaction guarantee, and "
            "<a href=\"/maintenance\">X-Plan members</a> get a 5-year warranty on qualified "
            "repairs. If a part is still inside the manufacturer's warranty period, we handle "
            "it as warranty work, whoever installed the system. Once the age and the failed "
            "part point the other way, <a href=\"/ac-installation\">replacement</a> is the "
            "next page."),
        sec("How do I book AC repair?",
            call("Call {tel} or book online. The emergency line runs every day of the year. "
                 "For anything that is not urgent, the office is staffed Monday to Friday, "
                 "8:00 AM to 5:00 PM. If your outdoor unit is a heat pump rather than an air "
                 "conditioner, <a href=\"/heat-pump-repair\">heat pump repair</a> is the page "
                 "you want.")),
    ],
    faqH2="What else do homeowners ask about AC repair?",
    faq=qa(
        ("How fast can you get here?",
         "Usually the same day. About nine calls in ten are handled the day you reach out, and "
         "the emergency line is answered at any hour when it cannot wait."),
        ("Do you repair every brand?",
         "Yes, every major make and model, whoever installed it."),
        ("Will I know the price before you start?",
         "Yes. The repair is diagnosed first, then priced flat, and nothing is taken apart "
         "until the price is approved. No part is charged without approval first."),
        ("My AC is frozen over. Should I keep running it?",
         "No. Switch the cooling off and leave the fan running so the ice melts. Ice on the "
         "coil or the refrigerant line means airflow or refrigerant is wrong, and running the "
         "compressor through ice is a common cause of compressor failure."),
        ("My air conditioner is 14 years old. Is a repair still worth it?",
         "Sometimes. A capacitor or contactor on a 14-year-old system is usually worth fixing. "
         "A failed compressor or a leaking evaporator coil at that age is usually where "
         "replacement wins. You get both numbers, and the choice stays yours."),
    ))

geo(HVAC_SUBS, "ac-installation.html",
    h1="AC installation and replacement in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Right-sized, high-efficiency air conditioners installed clean and to code. Honest "
          "sizing math, free replacement estimates, and flexible financing.",
    answer="Comparing quotes? Ours starts with a load calculation on your house, not a match "
           "to the label on the old unit. You get the sizing math, a written price and "
           "financing options in one visit, free.",
    sections=[
        sec("What does an AC installation include?",
            "The outdoor condenser, the indoor evaporator coil, the line set connection, the "
            "electrical whip and disconnect, and the refrigerant charge. Your old equipment "
            "and refrigerant leave with the crew. The system gets commissioned and measured "
            "before anyone signs off on it. If yours still has years in it, "
            "<a href=\"/ac-repair\">a repair</a> is usually the better money.",
            h3s=[("What gets checked that most quotes skip",
                  "Line set condition, the size of the existing electrical circuit, condensate "
                  "drainage, and whether the return duct can move the air the new system "
                  "needs. A larger system on an undersized return is the most common reason a "
                  "new AC underperforms.")]),
        sec("What size air conditioner does my house need?",
            "Size comes from a heat gain calculation on the specific house: square footage, "
            "insulation, window area and orientation, ceiling height, and duct condition. "
            "Matching the tonnage on the old label repeats whatever mistake was made last "
            "time. An oversized system short cycles, and a Dayton summer still feels clammy at "
            # This sentence had been folded around the link phrase until it read
            # "whether to fix or repair or replace" and stopped meaning anything. The
            # link stays; the sentence is built around it now instead of through it.
            "the set temperature. Sizing only matters once you have settled the earlier "
            "question, which is whether to "
            "<a href=\"/ac-repair#repair-or-replace\">repair or replace the air conditioner</a> "
            "at all.",
            h3s=[("Why oversizing costs comfort",
                  "An oversized air conditioner cools the thermostat fast and shuts off before "
                  "it has pulled moisture out of the air. The house hits the set temperature "
                  "and still feels damp. The fix is right-sizing rather than more tonnage.")]),
    ],
    table=tbl("Single-stage, two-stage and variable-speed air conditioners compared.",
              "There are three grades to choose from, and where they differ most is how well "
              "they pull humidity out of the house in August.",
              ["Factor", "Single-stage", "Two-stage", "Variable-speed"],
              [("How it runs", "Full capacity or off", "High or low capacity",
                "Adjusts continuously across a wide range"),
               ("Temperature swing", "Largest swing between cycles",
                "Smaller swing between cycles", "Smallest swing, closest to the setpoint"),
               ("Summer humidity", "Shorter run times remove less moisture",
                "Longer low-stage runs remove more moisture",
                "Long low-speed runs dehumidify continuously"),
               ("Noise", "Loudest at every startup", "Quieter while in low stage",
                "Quietest, ramps up rather than starting hard"),
               ("Efficiency", "Lowest SEER2 ratings in the line", "Middle of the line",
                "Highest SEER2 ratings in the line"),
               ("Upfront cost", "Lowest of the three", "Middle of the three",
                "Highest of the three"),
               ("Best fit", "Like-for-like swap, light use, rental property",
                "Most Dayton and Cincinnati homes",
                "Two-story homes, humidity complaints, long cooling seasons")],
              h2="Single-stage, two-stage, or variable-speed: which one fits?",
              sid="stages", eyebrow="CHOOSING A SYSTEM"),
    sectionsTail=[
        sec("How long does a replacement take?",
            "Most are a single day. We usually install within a day or two of the estimate, "
            "same week even in the middle of summer. Adding ductwork, a new circuit or a new "
            "pad stretches it out. If you are open to it, price a "
            "<a href=\"/heat-pump-installation\">heat pump</a> alongside at the same time."),
        sec("Can I finance it?",
            "Yes, and a new air conditioner starts " + D.finance_line(D.FINANCE_AC, "an AC") +
            ". That is the best-case advertised payment rather than a quote for your house. "
            "Three lenders look at the application, GoodLeap, Synchrony and Wright-Patt Credit "
            "Union, and they set the rate and the term rather than us. You see the payment "
            "options next to the written quote, before anything is ordered. More on the "
            "<a href=\"/financing-options\">financing page</a>."),
        sec("How do I book an estimate?",
            call("Call {tel} or book online. Replacement estimates are free, and one visit "
                 "covers the load calculation, a written quote and your financing options. "
                 "Once the new system is in, the "
                 "<a href=\"/maintenance\">X-Plan membership</a> is what keeps it healthy.")),
    ],
    faqH2="What else do homeowners ask before replacing an AC?",
    faq=qa(
        ("What size air conditioner do I need?",
         "That comes from a load calculation on your house, not from the tonnage printed on "
         "the old unit. We run it as part of every free replacement estimate."),
        ("How fast can you install one?",
         "Usually within a day or two of the estimate, same week in most cases, heat wave or "
         "not. Most replacements are done in a single day."),
        ("Do I have to replace the furnace at the same time?",
         "Not always. If the furnace is newer and the blower and coil cabinet match the new "
         "outdoor unit, the air conditioner can be replaced on its own. If the furnace is near "
         "the end of its life, replacing both at once avoids paying twice for the same labor."),
        ("Is my old R-22 system worth keeping?",
         "Usually not. R-22 is no longer produced, so a system that leaks it becomes "
         "progressively more expensive to keep charged. Once an R-22 system needs a "
         "refrigerant repair, replacement is almost always the better money."),
    ))

geo(HVAC_SUBS, "furnace-installation.html",
    h1="Furnace installation and replacement in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Right-sized, high-efficiency furnaces installed clean and to code. Heat-loss sizing "
          "math, free estimates, and flexible financing.",
    answer="We size your furnace from a heat-loss calculation on the actual house, not from "
           "the rating plate on the old one. Estimates are free, and you leave the visit with "
           "a written number and payment options.",
    sections=[
        sec("What does a furnace installation include?",
            "Removing and disposing of the old furnace, the new one set and levelled, gas "
            "piping and shutoff, venting, electrical, condensate drainage on condensing "
            "models, and thermostat wiring. We commission it, check gas pressure and walk you "
            "through the whole thing before leaving. If yours still has years in it, "
            "<a href=\"/furnace-repair\">a repair</a> is the cheaper answer.",
            h3s=[("What changes when the furnace goes condensing",
                  "Moving from an 80% AFUE furnace to a 90%+ condensing model changes the "
                  "venting and adds a condensate drain. The old chimney or metal flue is no "
                  "longer used for the furnace, and PVC runs out through a sidewall instead. "
                  "If a water heater shared that chimney, it needs its own plan.")]),
        sec("What size furnace does my house need?",
            "Size comes from a heat-loss calculation: square footage, insulation, air sealing, "
            "window area, and duct condition. Ohio houses get replaced with oversized furnaces "
            "regularly, because the easy move is to match the old label. An oversized furnace "
            "short cycles, which wears it out early and still leaves the far rooms cold. "
            "Whether to <a href=\"/furnace-repair#repair-or-replace\">repair or replace a "
            "furnace</a> comes first."),
    ],
    table=tbl("Furnace efficiency tiers compared.",
              "There are three efficiency bands to pick from, and what changes between them in "
              "a real house is the venting, the drainage, and how evenly the heat arrives.",
              ["Factor", "80% AFUE", "90% to 95% AFUE", "96% AFUE and above"],
              [("Fuel converted to heat", "About 80 cents of every fuel dollar",
                "About 90 to 95 cents of every fuel dollar",
                "About 96 cents or more of every fuel dollar"),
               ("Venting", "Metal flue or a lined masonry chimney", "PVC through a sidewall",
                "PVC through a sidewall"),
               ("Condensate drain", "Not required", "Required", "Required"),
               ("Burner", "Single stage, larger temperature swings", "Often two stage",
                "Often modulating, smallest temperature swings"),
               ("Upfront cost", "Lowest of the three", "Middle of the three",
                "Highest of the three"),
               ("Best fit", "Like-for-like swap where no drain is available",
                "Most Dayton and Cincinnati replacements",
                "Owners staying in the home long term")],
              h2="Which AFUE efficiency tier is worth paying for?", sid="afue",
              eyebrow="EFFICIENCY TIERS"),
    sectionsTail=[
        sec("How long does a replacement take?",
            "Most are a single day. We usually install within a day or two of the estimate, "
            "same week even in season. Changing the venting route, adding a condensate pump or "
            "opening up ductwork runs longer. A "
            "<a href=\"/heat-pump-installation\">heat pump</a> is worth pricing beside another "
            "gas furnace while you are deciding."),
        sec("Can I finance it?",
            "Yes. A furnace and air conditioner replaced together start " +
            D.finance_line(D.FINANCE_FULL_SYSTEM, "a full system") + ", which is the best-case "
            "advertised payment for the pair rather than a quote for your house. GoodLeap, "
            "Synchrony and Wright-Patt Credit Union set the rate and the term rather than us, "
            "and you see the payment options with the written quote, before anything is "
            "ordered. More on the <a href=\"/financing-options\">financing page</a>."),
        sec("How do I book an estimate?",
            call("Call {tel} or book online. Estimates are free, and the visit covers the "
                 "heat-loss calculation, a written quote and financing options, with no "
                 "obligation to buy. Afterwards, the "
                 "<a href=\"/maintenance\">X-Plan membership</a> is what keeps the "
                 "manufacturer warranty intact.")),
    ],
    faqH2="What else do homeowners ask before replacing a furnace?",
    faq=qa(
        ("How fast can you install one?",
         "Usually within a day or two of the estimate, same week in most cases even in the "
         "middle of an Ohio winter. Most replacements are done in a single day."),
        ("What size furnace do I need?",
         "That comes from your home's actual heat loss, not from the rating plate on the old "
         "furnace. We run the heat-loss calculation as part of every free estimate."),
        ("Is a 96% AFUE furnace worth it over an 80%?",
         "Depends how long you plan to stay and whether your house can take a condensing "
         "furnace. A 96% unit turns about 96 cents of every fuel dollar into heat against "
         "about 80 cents, but it needs sidewall venting and a condensate drain, and not every "
         "basement has somewhere to put them."),
        ("Do I have to replace the air conditioner at the same time?",
         "Not always. The furnace and the indoor coil share a cabinet, so replacing both at "
         "once avoids paying twice for the same labor. If the air conditioner is newer and the "
         "coil matches the new blower, the furnace can be replaced on its own."),
    ))

geo(HVAC_SUBS, "heat-pump-repair.html",
    h1="Heat pump repair in {X}, any season.", h1Highlight="Dayton &amp; Cincinnati",
    intro="A heat pump works year-round, so a fault shows up as no heat in January or no "
          "cooling in July. We diagnose fast, price flat before any work, and repair every "
          "make and model.",
    answer="Before you call: light frost on the outdoor unit and a few minutes of cool air "
           "during a defrost cycle are normal. Anything past that, we repair in both heating "
           "and cooling mode, most of them the same day.",
    sections=[
        sec("Is ice on a heat pump normal in winter?",
            "Some of it is. A heat pump running in heating mode pulls heat out of outdoor air, "
            "which puts frost on the outdoor coil, and the unit runs a defrost cycle every so "
            "often to melt it. A light frost that clears on its own is the system working. The "
            "<a href=\"/heat-pump\">heat pump services overview</a> covers how the system is "
            "meant to behave through an Ohio winter.",
            h3s=[("When the ice is a real fault",
                  "Ice becomes a problem when the outdoor unit is encased in it, when a solid "
                  "sheet covers the top fan grille, or when the ice never clears through a "
                  "full day. That points at a failed defrost control, a stuck reversing valve, "
                  "low refrigerant, or a fan that has stopped turning."),
                 ("Do not chip ice off the coil",
                  "The coil fins and the refrigerant tubing sit right behind the ice. Chipping "
                  "at it punctures the coil and turns a defrost problem into a refrigerant "
                  "leak. Switch the system to emergency heat and let it thaw.")]),
        sec("Why is my heat pump blowing cool air?",
            "A few minutes of cool air during a defrost cycle is normal, because the system "
            "briefly reverses to melt the outdoor coil. Constant cool air in heating mode is "
            "not. That usually points at refrigerant, a reversing valve, or a failed defrost "
            "control."),
        sec("What does emergency heat mean on my thermostat?",
            "Emergency heat locks out the heat pump and runs the backup heat only. It is a "
            "temporary setting for when the heat pump has failed or is iced solid, not an "
            "efficiency mode. Electric backup heat is the most expensive heat in the house to "
            "run, so it is worth getting the heat pump looked at rather than leaving it on. In "
            "a dual-fuel home the backup is a gas furnace, which is "
            "<a href=\"/furnace-repair\">furnace repair</a> territory instead.",
            h3s=[("Backup heat running constantly is a symptom",
                  "Backup heat is meant to run on the coldest nights. If it runs most days "
                  "through a Dayton winter, the heat pump is either undersized, low on "
                  "refrigerant, or losing capacity, and the electric bill shows it before "
                  "anything else does. <a href=\"/thermostat\">Thermostat repair and "
                  "replacement</a> matters here too, because a thermostat configured as if the "
                  "system were a gas furnace will call the backup far more than it should.")]),
        sec("What happens on a repair visit?",
            "We test the system in both heating and cooling mode, because a heat pump fault "
            "often shows up in only one of them. Pressures, the reversing valve, the defrost "
            "board and the backup heat staging all get checked. You get a flat price and "
            "approve it before work starts. A system that runs year-round wants two seasonal "
            "visits, which is what <a href=\"/maintenance\">X-Plan</a> covers."),
    ],
    table=tbl("Repair or replace a heat pump: what decides it.",
              "Once a system is 12 years or older and the compressor or reversing valve has "
              "gone, replacement is usually the better money.",
              ["What we look at", "Repair when", "Replace when"],
              [("System age", "Under 12 years old", "12 years or older"),
               ("Failed part", "Capacitor, contactor, defrost board, or fan motor",
                "Compressor or reversing valve"),
               COST_ROW, R22_ROW,
               ("Backup heat use", "Runs only on the coldest nights",
                "Runs most of the winter because the heat pump cannot keep up"),
               ("Breakdown history", "First failure in several seasons",
                "Second or third call in one heating season"),
               ("Comfort", "One mode affected, heating or cooling",
                "Neither mode holds the set temperature")],
              h2="Should I repair or replace my heat pump?", sid="repair-or-replace",
              eyebrow="REPAIR OR REPLACE"),
    sectionsTail=[
        sec("How do I book heat pump repair?",
            call("Call {tel} or book online. The emergency line runs every day of the year, "
                 "and a heat pump that has stopped heating in freezing weather goes out as a "
                 "no-heat call. If the age and the failed part point at a new system, "
                 "<a href=\"/heat-pump-installation\">replacement</a> is quoted free.")),
    ],
    faqH2="What else do homeowners ask about heat pump repair?",
    faq=qa(
        ("How fast can you get here?",
         "Usually the same day. About nine calls in ten are handled the day you reach out, and "
         "the emergency line is answered at any hour when it cannot wait."),
        ("My heat pump is covered in ice. Is it broken?",
         "Not necessarily. Frost on the outdoor coil is normal in heating mode, and the unit "
         "runs a defrost cycle to clear it. A unit encased in ice, or one whose ice never "
         "clears through a full day, is a fault worth a service call."),
        ("Why is my heat pump blowing cool air in winter?",
         "A few minutes of cool air during a defrost cycle is normal. Constant cool air is "
         "not, and usually points at refrigerant, a reversing valve, or a failed defrost "
         "control. It is worth checking before the backup heat runs the electric bill up."),
        ("Should I leave the thermostat on emergency heat?",
         "Only until the heat pump is repaired. Emergency heat locks out the heat pump and "
         "runs electric backup heat alone, which is the most expensive heat in the house to "
         "run."),
        ("Why does my heat pump run almost constantly?",
         "Long run times are normal for a heat pump in cold weather, because it delivers heat "
         "at a lower temperature than a furnace does. Constant running that never reaches the "
         "set temperature is different, and usually means low refrigerant, a dirty coil, or an "
         "undersized system."),
        ("Do you service all heat pump brands?",
         "Yes. Every major make and model, regardless of who installed it."),
    ))

geo(HVAC_SUBS, "heat-pump-installation.html",
    h1="Heat pump installation in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Right-sized, high-efficiency heat pumps installed clean and to code. Heat-loss "
          "sizing, backup heat configured at commissioning, and flexible financing.",
    answer="We set both the capacity and the backup heat from a heat-loss calculation on your "
           "house, so the system is built around your coldest nights rather than an average "
           "one. We will price a dual-fuel setup against a straight heat pump.",
    sections=[
        sec("How is a heat pump sized for an Ohio winter?",
            "Sizing starts from the home's heat loss at the coldest outdoor temperature the "
            "local design data uses, not from the tonnage on the old unit. A heat pump sized "
            "only for the cooling load will lean on backup heat all winter. One sized for "
            "heating alone will short cycle every summer. If the existing system is not dead "
            "yet, <a href=\"/heat-pump-repair\">heat pump repair</a> may still be the better "
            "money this season."),
        sec("What backup heat does a heat pump need?",
            "Every heat pump in this climate is installed with a plan for the coldest nights. "
            "There are three configurations, and which one fits depends mostly on whether "
            "natural gas is already at the house. Where a gas furnace is worth keeping, "
            "<a href=\"/furnace-installation\">furnace installation</a> and the heat pump get "
            "quoted together as a dual-fuel system.",
            sid="backup-heat",
            table=tbl("Backup heat options on a residential heat pump.",
                      "Every heat pump we install gets its backup heat configured one of three "
                      "ways, and which one you want mostly depends on whether gas is already "
                      "at the house.",
                      ["Factor", "Electric backup heat", "Dual fuel, gas furnace backup",
                       "No backup heat"],
                      [("How the backup works",
                        "Electric resistance elements sit in the air handler",
                        "A gas furnace takes over below a set outdoor temperature",
                        "The heat pump carries the whole heating load"),
                       ("Existing gas service", "Not needed", "Required at the house",
                        "Not needed"),
                       ("Running cost on the coldest nights",
                        "Highest of the three, electric resistance heat is expensive",
                        "Lower, the furnace carries the coldest hours",
                        "Depends entirely on the unit's rated low-temperature capacity"),
                       ("Control setup", "Thermostat staging set at commissioning",
                        "A balance-point temperature set at commissioning", "None"),
                       ("Upfront cost", "Lowest of the three", "Highest of the three",
                        "Middle of the three"),
                       ("Best fit", "All-electric homes, and homes with no gas main",
                        "Homes with a gas furnace worth keeping",
                        "Well-insulated homes with a cold-climate rated unit")])),
        sec("Can a heat pump replace my furnace and air conditioner?",
            "In many homes, yes. One outdoor unit and one indoor coil handle both seasons, "
            "which is why a heat pump replaces two pieces of equipment with one. Whether it is "
            "the right call depends on the ductwork, the insulation, and whether gas is "
            "already at the house. The <a href=\"/heat-pump\">heat pump services overview</a> "
            "carries the full system comparison."),
        sec("What does the installation include?",
            "Removing and disposing of your old equipment, the outdoor unit set and levelled, "
            "the line set and electrical, the indoor air handler or coil, refrigerant charge "
            "verified by weight and subcooling, backup heat wired and staged, and the "
            "thermostat configured. We take commissioning readings before we leave."),
    ],
    sectionsTail=[
        sec("How long does a heat pump replacement take?",
            "Most residential heat pump replacements are a single-day job, and installation "
            "usually happens within a day or two of the estimate. A dual-fuel conversion that "
            "also replaces the furnace, or a job that adds an electrical circuit, runs into a "
            "second day."),
        sec("Can I finance it?",
            "Yes, and a heat pump starts " + D.finance_line(D.FINANCE_HEAT_PUMP, "a heat pump") +
            ", the best-case advertised payment rather than a quote for your house. GoodLeap, "
            "Synchrony and Wright-Patt Credit Union set the rate and the term rather than us, "
            "with payment options shown next to the written quote. More on the "
            "<a href=\"/financing-options\">financing page</a>. One thing to know: the Section "
            "25C and 25D federal tax credits both expired on 31 December 2025, so no number we "
            "give you leans on one. Afterwards, <a href=\"/maintenance\">X-Plan</a> covers the "
            "two seasonal visits a year-round system wants."),
    ],
    faqH2="What else do homeowners ask before installing a heat pump?",
    faq=qa(
        ("Will a heat pump keep up in an Ohio winter?",
         "It will, when it is sized for your home's actual heat loss and the backup heat is "
         "set up for the coldest nights. We set both from the heat-loss calculation rather "
         "than from the size of whatever is out there now."),
        ("What is a dual-fuel system?",
         "A heat pump paired with a gas furnace. The heat pump handles the mild and moderate "
         "hours, and the furnace takes over below a set outdoor temperature called the balance "
         "point. The changeover is automatic."),
        ("Can one heat pump replace both my furnace and my air conditioner?",
         "In many homes, yes. One outdoor unit handles heating and cooling. Whether it fits "
         "depends on the ductwork, the insulation, and how the house loses heat, which is what "
         "the load calculation measures."),
        ("How fast can you install a heat pump?",
         "Usually within a day or two of the estimate. Most residential replacements are "
         "completed in a single day, and a dual-fuel conversion that also replaces the furnace "
         "runs into a second."),
    ))

geo(HVAC_SUBS, "indoor-air-quality-solutions.html",
    h1="Whole-home air quality solutions for {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Filtration, UV purification, ventilation and humidity control, matched to your "
          "home's measured problem rather than sold as a package.",
    answer="Five kinds of equipment: media filtration, UV purification, humidifiers, "
           "dehumidifiers and fresh-air ventilation. Each one fixes a different problem, so we "
           "measure yours first and check the readings again afterwards.",
    sections=[
        sec("Which air quality equipment fixes which problem?",
            "Every piece of equipment on this page targets one thing well and most other "
            "things badly. A UV lamp is excellent against biological growth on a cold, wet "
            "evaporator coil and does nothing for dust. A media filter is the opposite. "
            "Matching the equipment to the complaint that prompted the call is most of the "
            "work, which is where <a href=\"/indoor-air-quality\">indoor air quality services "
            "in Dayton and Cincinnati</a> starts.",
            sid="equipment",
            table=tbl("Indoor air quality equipment: what each option targets.",
                      "There are five categories of equipment here and each one is aimed at a "
                      "different problem, which is why buying before you know the problem "
                      "usually disappoints.",
                      ["Option", "What it targets", "Where it installs", "Service interval"],
                      [("1-inch pleated filter", "Lint, larger dust, and coarse pollen",
                        "The return grille or the filter slot at the air handler",
                        "Changed every 1 to 3 months"),
                       ("4-inch or 5-inch media air cleaner",
                        "Fine dust, dander, and pollen, at a higher MERV without choking airflow",
                        "A cabinet added on the return side of the air handler",
                        "Changed every 6 to 12 months"),
                       ("UV lamp",
                        "Biological growth on the evaporator coil and in the drain pan",
                        "Inside the air handler, aimed at the coil",
                        "Lamp replaced about every 12 months"),
                       ("Carbon filtration",
                        "Cooking odors, smoke, and some volatile organic compounds",
                        "In the media cabinet or a dedicated section of return duct",
                        "Media replaced on the manufacturer's schedule"),
                       ("Whole-home humidifier",
                        "Dry winter air below 30% relative humidity",
                        "Mounted on or bypassed across the furnace, plumbed to a water line",
                        "Pad replaced each heating season"),
                       ("Whole-home dehumidifier",
                        "Summer humidity above 50%, and damp basements",
                        "Ducted alongside the air handler, or standalone in the basement",
                        "Filter checked twice a year"),
                       ("Fresh-air ventilation",
                        "Stale air and carbon dioxide buildup in tightly built homes",
                        "A dedicated duct from outdoors into the return",
                        "Damper and filter checked twice a year")])),
        sec("Do UV lights in an HVAC system work?",
            "Against biological growth on the evaporator coil and in the drain pan, yes, when "
            "the lamp is sized and aimed correctly. A cooling coil is cold and wet all summer, "
            "which is exactly where mold grows in a duct system. UV does not remove dust, "
            "dander, or pollen, so a UV lamp sold as an allergy fix is being sold for the "
            "wrong job. <a href=\"/importance-iaq\">Why indoor air quality matters</a> covers "
            "what indoor air actually carries."),
        sec("What MERV rating can my system handle?",
            "The highest one the duct system can move air through. A 1-inch slot on a "
            "residential furnace generally tops out around MERV 8 to 11. Pushing MERV 13 "
            "through a 1-inch filter raises static pressure, drops airflow, and can freeze the "
            "coil in summer or trip the high limit in winter. More of this ground is covered "
            "in the <a href=\"/iaq-faq\">indoor air quality FAQ</a>.",
            h3s=[("The upgrade that makes higher MERV safe",
                  "A 4-inch or 5-inch media cabinet has far more filter surface area, so it "
                  "holds a higher MERV at a lower pressure drop. That cabinet, rather than a "
                  "thicker filter in the same slot, is what makes MERV 13 realistic in a "
                  "house. A leaky return pulls unfiltered air in past all of it, which is why "
                  "<a href=\"/duct-cleaning\">air duct cleaning</a> and sealing come first.")]),
        sec("Do I need a whole-home humidifier or a dehumidifier?",
            "In the Dayton and Cincinnati metros, most homes need both at different times of "
            "year. Winter heating drives indoor relative humidity below 30%, which is what "
            "causes static, cracked trim, and dry sinuses. Summer pushes basements above 50%, "
            "which is where musty smells and mold start. "
            "<a href=\"/humidifier\">Whole-home humidifier services</a> cover the winter half.",
            h3s=[("The number to aim at",
                  "Indoor relative humidity between 30% and 50% is the range that keeps mold, "
                  "dust mites, and dry air problems all in check at once. Anything held above "
                  "60% for long enough feeds mold growth.")]),
    ],
    sectionsTail=[
        sec("How long does an air quality install take?",
            "Most filtration, UV, and humidifier installs are a single visit, often the same "
            "week as the call. A whole-home dehumidifier or a fresh-air ventilation duct is a "
            "longer job because it involves cutting into the duct system. Filter and pad "
            "changes at the seasonal visits come with the "
            "<a href=\"/maintenance\">X-Plan maintenance membership</a>."),
        sec("How do I book an air quality assessment?",
            call("An assessment is booked by phone at {tel} or online. The visit measures "
                 "humidity and airflow, checks the existing filtration and the duct system, "
                 "and produces a recommendation with upfront pricing before anything is "
                 "installed.")),
    ],
    faqH2="What else do homeowners ask about air quality equipment?",
    faq=qa(
        ("Which filter rating should I use at home?",
         "The highest MERV your system can move air through. A 1-inch slot generally tops out "
         "around MERV 8 to 11. MERV 13 needs a 4-inch or 5-inch media cabinet, and we measure "
         "static pressure before recommending one."),
        ("Do UV lights in HVAC systems really work?",
         "Against biological growth on the evaporator coil and in the drain pan, yes, when "
         "they are sized and aimed correctly. They do not remove dust, dander, or pollen, so a "
         "UV lamp is not an allergy fix on its own."),
        ("Do I need a whole-home system, or is a better filter enough?",
         "Often a filter upgrade plus sealing the return side of the ducts does more than an "
         "expensive purifier. Leaky returns pull dirty air in from basements and crawl spaces, "
         "past the filter entirely, which no purifier downstream can undo."),
        ("What humidity should my house hold?",
         "Between 30% and 50% relative humidity year round. Below 30% causes static and dry "
         "sinuses in winter. Above 60% for any length of time feeds mold and dust mites."),
        ("Can these be installed on my existing furnace?",
         "In most cases, yes. Media cabinets, UV lamps, humidifiers, and dehumidifiers all "
         "retrofit to existing residential systems. The duct layout and the space around the "
         "air handler decide what fits."),
    ))

geo(HVAC_SUBS, "importance-iaq.html",
    h1="Why indoor air quality matters in {X}.", h1Highlight="Ohio homes",
    intro="The EPA reports indoor air often carries 2 to 5 times the pollutant levels of "
          "outdoor air. Here is what that means for a house in this region.",
    answer="The EPA puts indoor pollutant levels at 2 to 5 times what is outside. The sources "
           "are all in the house, and a well-sealed modern home holds onto them longer. That is "
           "why a new build usually needs mechanical ventilation more than an old one does.",
    sections=[
        sec("Is indoor air really worse than outdoor air?",
            "Usually, yes. The EPA reports indoor pollutant levels commonly run 2 to 5 times "
            "higher than outdoor levels, and occasionally far higher during activities like "
            "painting or stripping floors. The sources are indoors, and a heated or cooled "
            "house is built to hold onto its air. That is the problem "
            "<a href=\"/indoor-air-quality\">indoor air quality services in Dayton and "
            "Cincinnati</a> is built around."),
        sec("What is actually in the air inside a house?",
            "Seven things account for most of what a homeowner notices, and each has a "
            "different source and a different fix. Adding equipment before finding the source "
            "is the expensive way to do this. Dust and leaky returns are the pair that "
            "<a href=\"/duct-cleaning\">air duct cleaning</a> addresses, and the carbon "
            "monoxide row is what an annual "
            "<a href=\"/inspection\">furnace safety inspection</a> exists to catch.",
            sid="pollutants",
            table=tbl("Common indoor air pollutants, their sources, and what reduces them.",
                      "Seven problems, seven different sources. The fix for each one starts "
                      "with removing the source rather than buying equipment to chase it.",
                      ["What is in the air", "Where it comes from", "What reduces it"],
                      [("Fine dust and dander",
                        "Skin, pets, carpet, and soil tracked in from outdoors",
                        "Higher-MERV media filtration and regular filter changes"),
                       ("Pollen",
                        "Outdoor air entering through doors, windows, and leaky return ducts",
                        "Media filtration, plus sealing the return side of the duct system"),
                       ("Mould and mildew spores",
                        "Damp basements, condensate pans, and humidity held above 60%",
                        "Dehumidification to 50% or below, plus fixing the water source"),
                       ("Volatile organic compounds",
                        "Paint, adhesives, cleaners, new furnishings, and new flooring",
                        "Source removal first, then carbon filtration and fresh-air ventilation"),
                       ("Carbon monoxide",
                        "Any combustion appliance that is cracked, back-drafting, or unvented",
                        "Annual combustion safety checks and working CO alarms on every level"),
                       ("Carbon dioxide buildup",
                        "People breathing inside a tightly sealed house with no fresh-air intake",
                        "Mechanical fresh-air ventilation"),
                       ("Dry air",
                        "Winter heating of outdoor air that holds very little moisture",
                        "A whole-home humidifier holding 30% to 40% through the heating season")])),
        sec("What are the signs of poor indoor air quality?",
            "Most of them come on slowly enough that a household stops noticing. Dust returns "
            "within a day of cleaning, allergies get worse indoors than out, one part of the "
            "house smells musty, windows fog up in winter, and everyone sleeps better away "
            "from home. The <a href=\"/iaq-faq\">indoor air quality FAQ</a> takes each of "
            "those apart."),
        sec("Does indoor air quality affect sleep and allergies?",
            "Particulates, carbon dioxide buildup, and humidity extremes all disturb sleep, "
            "and indoor allergen exposure runs for the eight or so hours a person is in bed "
            "with the door shut. A bedroom with the door shut, no supply airflow, and the only "
            "return grille out in the hallway is a version of this that ductwork fixes rather "
            "than equipment."),
    ],
    sectionsTail=[
        sec("Are newer homes safer for indoor air?",
            "Not automatically. A tighter house loses less energy and also exchanges less air "
            "with outside, so whatever is generated indoors stays longer. Newer construction "
            "usually needs mechanical fresh-air ventilation for the same reason it needs less "
            "heating."),
        sec("What actually improves indoor air quality at home?",
            "Source control comes first, then filtration and ventilation for whatever is left, "
            "then humidity control to hold the house between 30% and 50%. The order matters "
            "more than the brand on the equipment. Gear bought before the source is found "
            "usually moves a reading without changing how the house feels, which is why "
            "<a href=\"/indoor-air-quality-solutions\">indoor air quality solutions</a> are "
            "quoted after a measurement rather than before."),
    ],
    faqH2="What else do homeowners ask about indoor air?",
    faq=qa(
        ("Is the air inside my house worse than the air outside?",
         "Usually, yes. The EPA reports indoor pollutant levels commonly run 2 to 5 times "
         "higher than outdoor levels, because the sources are indoors and a heated or cooled "
         "house is built to hold its air."),
        ("What are the signs of poor indoor air quality?",
         "Dust that returns within a day of cleaning, allergies that are worse indoors than "
         "outdoors, a musty smell in one part of the house, windows that fog in winter, and "
         "sleeping better away from home."),
        ("Is my home too new to have air quality problems?",
         "No. Newer, tighter homes trap more of what is generated indoors, which is exactly "
         "why mechanical fresh-air ventilation matters more in new construction."),
        ("Does indoor air quality really affect sleep?",
         "Yes. Particulates, carbon dioxide buildup, and humidity extremes all disturb sleep, "
         "and a bedroom with the door shut concentrates all three for the hours someone is in "
         "it."),
        ("What is the single most useful thing to fix first?",
         "The source, then the filter. A correctly sized media filter changed on schedule, in "
         "a system whose return ducts are sealed, beats most add-on equipment. We will say so "
         "rather than quote you a purifier."),
    ))

geo(HVAC_SUBS, "iaq-faq.html",
    h1="Indoor air quality questions, {X}.", h1Highlight="answered straight",
    intro="Straight answers on MERV ratings, filter changes, winter humidity, UV lamps and "
          "duct cleaning, for homeowners in Dayton and Cincinnati.",
    answer="The short version: keep the house between 30% and 50% humidity, change a 1-inch "
           "filter every 1 to 3 months, and do not buy a UV lamp expecting it to help with "
           "dust. The longer version is below.",
    sections=[
        sec("What MERV rating should I use at home?",
            "The highest rating the duct system can move air through without a pressure "
            "penalty. In a standard 1-inch filter slot that is usually MERV 8 to 11. Going "
            "higher in the same slot drops airflow, which can freeze an evaporator coil in "
            "summer and trip a furnace high limit in winter. The cabinet upgrade that makes "
            "MERV 13 realistic is covered under "
            "<a href=\"/indoor-air-quality-solutions\">indoor air quality solutions</a>.",
            sid="merv",
            table=tbl("MERV ratings and what each one catches.",
                      "Go as high as your system's measured static pressure allows, which for "
                      "most houses around here means somewhere between MERV 8 and MERV 13.",
                      ["MERV rating", "What it captures", "Airflow risk on a home system",
                       "Typical use"],
                      [("MERV 1 to 4", "Lint, carpet fiber, and the largest dust",
                        "None, this is the lowest-resistance filter sold",
                        "Fiberglass throwaway filters, which protect the equipment rather than the air"),
                       ("MERV 5 to 8", "Dust, pollen, mold spores, and dust mite debris",
                        "Safe in nearly every residential system",
                        "The default 1-inch pleated filter"),
                       ("MERV 9 to 12", "Fine dust, pet dander, and most airborne allergens",
                        "Safe in a 4-inch media cabinet, restrictive in a 1-inch slot",
                        "Allergy households that have a media cabinet"),
                       ("MERV 13 to 16",
                        "Smoke, bacteria, and particles down to 0.3 microns",
                        "High risk in a 1-inch slot, needs a deep cabinet and measured static pressure",
                        "Only where the duct system has been measured first"),
                       ("HEPA", "99.97% of particles at 0.3 microns",
                        "Cannot be fitted inline on a standard residential air handler",
                        "A bypass unit, or a portable room unit")])),
        sec("How often should a furnace filter be changed?",
            "A 1-inch filter every 1 to 3 months, sooner with pets or during a remodel. A "
            "4-inch or 5-inch media filter every 6 to 12 months. The reliable test is holding "
            "it up to a light: if the light does not come through, the filter is done "
            "regardless of the calendar."),
        sec("What humidity should a house hold in winter?",
            "Between 30% and 40% through the heating season, and no higher than 50% at any "
            "time of year. Below 30% causes static, dry sinuses, and shrinking trim. Above 50% "
            "in a cold Ohio house puts condensation on the windows, and above 60% feeds mold. "
            "<a href=\"/humidifier\">Whole-home humidifier services</a> hold the bottom of "
            "that range through a Dayton January."),
        sec("Do UV lights in HVAC systems really work?",
            "Against biological growth on the evaporator coil and in the drain pan, yes, when "
            "they are sized and aimed correctly. They do not remove dust, dander, or pollen, "
            "because those are filtered out, not killed. A UV lamp sold as an allergy fix is "
            "sold wrong."),
    ],
    sectionsTail=[
        sec("Does duct cleaning improve indoor air quality?",
            "It helps when the ducts are genuinely dirty, which usually means after a remodel, "
            "in a house with pets, or in a system that has never been cleaned. It does not "
            "help a clean duct system, and it is no substitute for filtration. The honest "
            "version is to look at the ducts before quoting the work, which is how "
            "<a href=\"/duct-cleaning\">air duct cleaning</a> is booked here. "
            "<a href=\"/importance-iaq\">Why indoor air quality matters</a> covers what is in "
            "the air to begin with."),
        sec("How often should air ducts be cleaned?",
            "Every 3 to 5 years covers most homes, with construction dust, pets, or a known "
            "mold problem moving it sooner. A system with a proper media filter and sealed "
            "returns stays clean longer, because less gets in to begin with."),
        sec("How do I get a straight answer about my own house?",
            call("Call {tel} or book an assessment online. We measure humidity and airflow, "
                 "look at your filtration and ductwork, and give you a recommendation with a "
                 "price on it before anything gets installed. Wider "
                 "<a href=\"/indoor-air-quality\">air quality work</a> starts from the same "
                 "visit.")),
    ],
    faqH2="A few more, kept separate from the sections above.",
    faq=qa(
        ("What is the single best air quality upgrade for most homes?",
         "A properly sized media filter, changed on schedule, in a system whose return ducts "
         "are sealed. It beats most add-on equipment, and we will tell you that rather than "
         "quote you a purifier."),
        ("Does a portable air purifier do the same thing as a whole-home system?",
         "It cleans one room while it runs. A whole-home system treats every room the ductwork "
         "reaches, every time the blower runs. For a single bedroom, a portable unit is often "
         "the sensible answer."),
        ("Will a higher MERV filter damage my furnace?",
         "It can, in a 1-inch slot. Higher MERV in the same thickness raises static pressure "
         "and drops airflow, which strains the blower, can freeze the coil in summer, and can "
         "trip the furnace high limit in winter. A 4-inch cabinet is the fix."),
        ("How fast can you help with an air quality problem?",
         "Assessments are usually scheduled within a few days, and most filtration and UV "
         "installs are completed in a single visit."),
    ))

# ======================================================================
# Plumbing detail pages
# ----------------------------------------------------------------------
# Two things run through every plumbing page below.
#
# The Ohio plumbing licence number, OH LIC #13557 (facts.md, client-confirmed
# 2026-08-02), appears in at least one body passage on every page. It is the
# cheapest credibility signal available on a plumbing page and it is
# checkable, which is what makes it worth citing.
#
# SPEED_FAQ is not reused here. It put one identical answer on nine plumbing
# pages; each page now answers the speed question in its own terms.
# ======================================================================

LICENCE_LINE = "under Ohio plumbing license #13557"

geo(PLUMB_PAGES, "clogged-drain.html",
    h1="Drain cleaning and clogged drain repair in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="One slow drain is a clog. Three slow drains at once is your main line. Cleared fast "
          "by licensed plumbers, with upfront pricing.",
    answer="One stopped sink or a backed-up main line, we clear both, most of them the same "
           "day. Which machine we bring depends on what the camera shows in your pipe, not on "
           "what we happen to be carrying.",
    callout="Multiple drains backing up at once? That's a main-line warning. Call {tel} before "
            "it becomes a mess, or see what a "
            "<a href=\"/plumbing/sewer-line/overview\">camera inspection</a> finds.",
    sections=[
        sec("Why is my sink draining slowly?",
            "A single slow fixture is almost always local: hair and soap in a bathroom line, "
            "grease and food solids in a kitchen line. The blockage usually sits within a few "
            "feet of the trap. It clears with a hand auger or a small cable machine and rarely "
            "needs anything opened up."),
        sec("Why are several drains backing up at once?",
            ["When two or more fixtures back up together, especially on the lowest floor, the "
             "blockage is downstream of both of them in the main line. That is a different "
             "problem and a different machine. Running more water into the house makes it "
             "worse, so stop using the fixtures and get a camera in the line.",
             "When two fixtures go at once we treat it as a main-line problem and put a "
             "<a href=\"/plumbing/sewer-line/overview\">camera</a> in before any machine, "
             "because clearing blind on a main line is how people pay twice."],
            table=tbl("Drain symptoms and the service each one calls for.",
                      "The service should match what the pipe is actually doing, which is why "
                      "a camera goes in before a machine does on any clog that keeps coming "
                      "back.",
                      ["Symptom", "Likely cause", "Service to book"],
                      [("One bathroom sink drains slowly",
                        "Hair and soap buildup near the trap", "Drain clearing"),
                       ("Kitchen sink backs up after cooking",
                        "Grease coating the pipe wall", "Hydro jetting"),
                       ("Tub fills when the toilet flushes", "Main line partially blocked",
                        "Camera inspection, then main line clearing"),
                       ("Gurgling from drains across the house",
                        "Venting or main line restriction", "Camera inspection"),
                       ("Floor drain overflows in heavy rain",
                        "Storm water entering the sanitary line", "Sewer line inspection"),
                       ("Same drain clogs every few months",
                        "Root intrusion, a belly, or a broken pipe",
                        "Camera inspection, then sewer repair"),
                       ("Sewage odor indoors with no visible backup",
                        "Dry trap or a cracked line",
                        "Leak detection and camera inspection")])),
        sec("Snaking or hydro jetting: which one do I need?",
            "A cable auger punches a hole through the blockage and gets water moving again. "
            "Hydro jetting scours the whole pipe wall with high-pressure water and takes the "
            "grease and root hair with it. Snaking is faster and cheaper; jetting lasts far "
            "longer on lines that clog repeatedly, which is why "
            "<a href=\"/plumbing/sewer-line/cleaning\">maintenance jetting</a> is the answer "
            "on a line that backs up every year.",
            table=tbl("Cable snaking compared with hydro jetting.",
                      "If a drain has clogged more than once in a year, jetting is what we "
                      "will recommend. Snaking it again only clears a path through the same "
                      "buildup.",
                      ["Factor", "Cable snaking", "Hydro jetting"],
                      [("What it does", "Bores an opening through the blockage",
                        "Scours the full pipe diameter"),
                       ("Best on", "A one-off clog in a branch line",
                        "Grease, scale and root hair in a main line"),
                       ("Pipe condition needed",
                        "Works in most pipe, including fragile lines",
                        "Pipe must be sound; a camera check comes first"),
                       ("How long it holds", "Months, if buildup remains",
                        "Years in most homes"),
                       ("Typical visit length", "Under an hour",
                        "Longer, and usually camera-verified after"),
                       ("When it is the wrong call",
                        "Repeat clogs, where it treats the symptom",
                        "A collapsed or offset pipe, which needs repair")])),
    ],
    sectionsTail=[
        sec("Are chemical drain cleaners safe to use?",
            "We do not recommend them. Caustic cleaners sit on top of the blockage, generate "
            "heat, and damage older pipe and rubber seals while rarely clearing the actual "
            "obstruction. They also make the line dangerous for whoever opens it next. "
            "Mechanical clearing costs more and does not eat your plumbing."),
        sec("How do I stop the same drain clogging every year?",
            ["Repeat clogs in the same line mean something structural, not something you did. "
             "Roots find clay joints, grease builds on rough cast iron, and a sagging section "
             "holds water and solids. A camera pass finds which, and the fix ranges from "
             "scheduled maintenance jetting to a "
             "<a href=\"/plumbing/sewer-line/repair\">sewer repair</a>.",
             "So on any line that has clogged twice, we camera it before recommending "
             "anything, working " + LICENCE_LINE + "."]),
        sec("Can you clear my drain today?",
            call("Most drain calls get booked and cleared the same day, and a main line backup "
                 "moves up the list, because water already reaching the floor gets more "
                 "expensive every hour it sits. Call {tel}, and if it is already on the floor, "
                 "<a href=\"/plumbing/emergency-plumbing\">shut the main valve</a> first.")),
    ],
    faqH2="What else do homeowners ask about drains?",
    faq=qa(
        ("How fast can a plumber get here for a backed-up drain?",
         "Most drain calls are handled the same day, and a main line backup gets priority over "
         "a routine one."),
        ("Why does my drain keep clogging after it has been cleared?",
         "A cleared drain that clogs again within a year usually has a structural cause: tree "
         "roots at a pipe joint, a sagging section holding water, or a break. A camera "
         "inspection finds which one, and cleaning alone will not hold until it is fixed."),
        ("Is hydro jetting safe for old pipes?",
         "Not always, which is why a camera goes in first. Cast iron that has thinned or clay "
         "pipe with existing cracks can be damaged by high-pressure water, and in those cases "
         "we say so before jetting rather than after."),
        ("Does drain cleaning damage my pipes?",
         "Properly sized cable and jetting equipment does not damage sound pipe. Chemical "
         "drain cleaners do, and repeated use of them is one of the more common reasons an old "
         "line finally fails."),
        ("What should I do while I wait for a plumber?",
         "Stop running water anywhere in the house, including the dishwasher and washing "
         "machine, and keep people off the lowest-floor fixtures. If water is already on the "
         "floor, shut the main valve."),
    ))

geo(PLUMB_PAGES, "emergency-plumbing.html",
    h1="24/7 emergency plumber for {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro=call("Call {tel}. If you smell gas, leave the house first and call from outside."),
    answer="Someone picks up at 2 a.m., on a Sunday, on Christmas. Burst pipe, sewage backing "
           "up, no water, water heater emptying onto the floor: tell us what you are looking "
           "at and we will talk you through it while a plumber heads over.",
    callout="<b>Safety first:</b> for gas smells, leave the house before calling {tel}. For "
            "water, shut the main valve if you can reach it safely.",
    sections=[
        sec("What counts as a plumbing emergency?",
            "Water you cannot shut off, sewage coming up indoors, a "
            "<a href=\"/plumbing/leak-detection\">burst or frozen pipe</a>, no water to the "
            "house, a <a href=\"/plumbing/water-heater/repair\">water heater dumping onto the "
            "floor</a>, or a gas smell near an appliance. Anything on that list is worth a 2 "
            "a.m. call. Most other plumbing can wait until morning without costing you more.",
            table=tbl("What to call about immediately and what can wait.",
                      "If it is on the left-hand list, call now, whatever the hour. If it is "
                      "on the right, morning is fine and it will not cost you more.",
                      ["What you're seeing", "Call 24/7 now", "Can wait for business hours"],
                      [("Water you cannot stop",
                        "Yes, shut the main valve while you call", "Do not wait"),
                       ("Sewage backing up into the house",
                        "Yes, stop using all water", "Do not wait"),
                       ("Gas smell anywhere",
                        "Leave the house, then call from outside", "Do not wait"),
                       ("No water at any fixture", "Yes", "Do not wait"),
                       ("Water heater leaking steadily",
                        "Yes, shut its supply valve", "Do not wait"),
                       ("One slow or clogged drain", "Not urgent on its own",
                        "Yes, if no other fixture is affected"),
                       ("Running toilet or dripping faucet", "Not urgent", "Yes"),
                       ("Low water pressure at one fixture", "Not urgent", "Yes")])),
        sec("Where is my water shut-off valve?",
            ["In most Dayton and Cincinnati homes with a basement, the main shut-off is on the "
             "interior wall facing the street, within a few feet of where the pipe comes "
             "through the foundation, usually near the meter. Slab homes often have it in a "
             "utility closet or the garage. Turn it clockwise until it stops.",
             "If you cannot find it, say so when you call and we will walk you through it on "
             "the phone. Knowing where it is beats knowing anything else on this page."]),
        sec("What should I do while I wait for a plumber?",
            "Shut the nearest valve, or the main if you cannot find it. Move anything you care "
            "about off the floor. Stop running water into the affected drains, including "
            "appliances on a timer. Photograph the damage before you clean it up, because your "
            "insurer will ask."),
    ],
    sectionsTail=[
        sec("Can you come out at night or on a weekend?",
            "Yes. There are licensed plumbers on call, not an answering service taking a "
            "message until Monday. Whoever picks up can start talking you through the shut-off "
            "straight away, and the repair is done " + LICENCE_LINE + "."),
        sec("Do emergency calls cost more than a normal visit?",
            "Every job, at every hour, is quoted flat and approved by you before work begins. "
            "Nothing gets added to the invoice afterward. If the honest answer on the phone is "
            "that it can safely wait until morning, we will tell you that too."),
        sec("What are the most common winter plumbing emergencies here?",
            ["Frozen and burst supply lines dominate December through February in both metros, "
             "usually in an unheated crawl space, an exterior wall, or a garage line nobody "
             "thought about. The break itself often happens on the thaw, not the freeze, which "
             "is why the flood starts the afternoon it warms up.",
             "Sewage coming up indoors is the other winter call we get, and that one runs "
             "through <a href=\"/plumbing/sewer-line/cleaning\">sewer line cleaning</a>."]),
    ],
    faqH2="What else do people ask at 2 a.m.?",
    faq=qa(
        ("Is there a plumber open right now near me?",
         call("Yes. Someone answers at {tel} at any hour, any day, including holidays.")),
        ("What do I do if a pipe bursts?",
         "Shut the main water valve, then open a low faucet to drain the pressure out of the "
         "line. Kill the power to any circuit near standing water at the breaker, not at the "
         "switch. Then call, and photograph everything before you start cleaning."),
        ("What do I do if I smell gas?",
         "Get everyone out of the house first. Do not flip switches, unplug anything, or use a "
         "phone indoors. From outside, call your gas utility, then call a licensed plumber "
         "once the utility has cleared the property."),
        ("My basement is flooding and the sump pump is not running. What now?",
         "Check the breaker and the float first, because a jammed float is the most common "
         "cause. If the pit is still filling, call. "
         "<a href=\"/plumbing/sump-pump/repair\">A pump that fails during a storm</a> is an "
         "emergency and we dispatch on those at any hour."),
    ))

geo(PLUMB_PAGES, "leak-detection.html",
    h1="Hidden water leak detection in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Most people find a leak on the water bill before they find it on the floor. We find "
          "it without tearing up the house.",
    answer="Water is going somewhere and you cannot see it. We listen for it and look for its "
           "heat, so a leak under your slab or inside a wall gets narrowed to inches before "
           "anyone cuts anything open.",
    callout="Leaks only get bigger. Call {tel} before a drip becomes drywall.",
    sections=[
        sec("How do I know if I have a hidden leak?",
            ["Run the house dry: turn off every fixture and appliance that uses water, then "
             "watch the meter for fifteen minutes. If the dial moves at all, water is going "
             "somewhere. That test costs nothing and it is the first thing we will ask whether "
             "you tried.",
             "Do it before you call. If the dial moved, you have your answer and we can skip "
             "straight to finding where."]),
        sec("Why did my water bill double with no leak I can see?",
            "A leak that never reaches a visible surface still runs through the meter. The "
            "usual culprits are a "
            "<a href=\"/plumbing/toilet-repair\">toilet flapper passing water silently</a>, an "
            "irrigation line, a slab leak under the floor, or a service line between the meter "
            "and the house. All four are invisible and all four bill.",
            table=tbl("Leak symptoms, likely location, and how each is found.",
                      "Find your symptom in the left column. It usually names the location "
                      "before any equipment comes out of the van.",
                      ["Symptom", "Likely location", "How it's found", "Urgency"],
                      [("Bill jumped, nothing visible", "Toilet flapper or irrigation",
                        "Dye test, then meter isolation", "Low, but it bills daily"),
                       ("Warm spot on a floor", "Hot supply line under the slab",
                        "Thermal imaging", "High, slab leaks worsen"),
                       ("Damp drywall or a ceiling stain",
                        "Supply or drain line in the wall or above",
                        "Acoustic and moisture meter", "High"),
                       ("Running water sound at night", "Pressurized supply line",
                        "Acoustic listening", "High"),
                       ("Wet patch in the yard year-round", "Buried service line",
                        "Line tracing and acoustic", "High, and it undermines soil"),
                       ("Musty smell, no visible water",
                        "Slow leak behind a finished wall", "Moisture mapping",
                        "Medium, mold follows"),
                       ("Meter moves with the house valve shut",
                        "Between the meter and the house", "Line tracing",
                        "High, this one is on you")])),
        sec("Can you find a leak without opening walls?",
            "Usually. Acoustic listening equipment picks up pressurized water escaping a line "
            "through drywall, tile and concrete, and thermal imaging shows where a hot line is "
            "heating the floor above it. That narrows the search to inches, so when something "
            "is opened, it is one small access hole and not a wall."),
    ],
    sectionsTail=[
        sec("What is a slab leak and how bad is it?",
            ["A slab leak is a supply line failure under the concrete floor of a house built "
             "on a slab. Signs are a warm patch of floor, an unexplained bill, or the sound of "
             "running water with everything off. Left alone it saturates the soil under the "
             "foundation, which is the expensive part, not the pipe.",
             "We find it with thermal imaging first. No concrete gets opened until we know "
             "which foot of pipe we are opening it for."]),
        sec("What gets documented when a leak is found?",
            "The source and the moisture readings are photographed before the repair, and the "
            "line is pressure-tested afterward. That record is what a claim or a future buyer "
            "asks for, and it is produced whether or not anyone ends up needing it."),
        sec("How fast can a leak be found and fixed?",
            call("Detection is usually one visit, and most leaks get located and repaired in "
                 "the same appointment unless the fix means opening a slab or "
                 "<a href=\"/plumbing/services\">replacing a run of line</a>. Most calls are "
                 "handled the same day. Call {tel}, or "
                 "<a href=\"/plumbing/emergency-plumbing\">the emergency line</a> if water is "
                 "moving right now.")),
    ],
    faqH2="What else do homeowners ask about hidden leaks?",
    faq=qa(
        ("How do I check for a water leak myself?",
         "Turn off every fixture and appliance that uses water, then watch the meter for 15 "
         "minutes. If it moves, you have a leak. The test is free and it is the fastest answer "
         "you can get without anyone coming out."),
        ("Can you find a leak without cutting into my walls?",
         "In most cases, yes. Acoustic and thermal detection narrows a hidden leak to within a "
         "few inches before anything is opened, so a repair usually means one small access "
         "point rather than an exploratory demolition."),
        ("How much water does a hidden leak waste?",
         "A toilet flapper that passes water silently can waste about 200 gallons a day, which "
         "is why a bill can double with nothing visible anywhere in the house."),
        ("My water heater area is damp but the tank looks fine. Is that a leak?",
         "It can be condensation, a leaking T&amp;P valve, or the first sign of "
         "<a href=\"/plumbing/water-heater/repair\">a tank failing at the bottom seam</a>. All "
         "three look the same on the floor and only one of them is harmless, so it is worth a "
         "look before the tank opens up."),
        ("Do you repair the leak, or only find it?",
         "Both, " + LICENCE_LINE + ". The line gets pressure-tested after the repair, before "
         "anyone leaves."),
    ))

geo(PLUMB_PAGES, "toilet-repair.html",
    h1="Toilet repair and replacement in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Some of this is a ten-minute fix you can do yourself. We will tell you which.",
    answer="Running fill valve, clogs that keep coming back, water at the base, a bowl that "
           "rocks. Most of it is a single visit. Some of it is a ten-minute job you can do "
           "yourself, and we will say which is which.",
    callout="A running toilet can waste 200 gallons a day. Call {tel} and stop paying for it.",
    sections=[
        sec("Why does my toilet keep running?",
            ["Most of the time it is the flapper: the rubber seal at the bottom of the tank "
             "hardens, stops sealing, and lets water trickle into the bowl until the fill "
             "valve kicks back on. A flapper is inexpensive and takes about ten minutes. If a "
             "new flapper does not fix it, the fill valve is next.",
             "It is worth doing quickly. A toilet running non-stop can put about 200 gallons a "
             "day through your meter, so this is a bill problem more than a noise problem."]),
        sec("Is a running toilet a DIY job or a plumber job?",
            "If replacing the flapper fixes it, it is a DIY job and you should keep the money. "
            "Call a plumber when the leak is at the base, when the bowl rocks, when the tank "
            "is cracked, or when the flange under the toilet has failed. Those need the toilet "
            "pulled.",
            table=tbl("When a toilet is worth repairing and when it should be replaced.",
                      "Cracked porcelain, or a unit older than the 1994 efficiency standard, "
                      "and you are better off replacing it than buying parts for it.",
                      ["What we look at", "Repair when", "Replace when"],
                      [("What failed", "Flapper, fill valve, supply line or wax ring",
                        "Cracked tank or bowl"),
                       ("Age", "Post-1994 unit in good condition",
                        "Pre-1994 unit using well over 1.6 gallons per flush"),
                       ("Flush performance", "Strong flush, occasional clog",
                        "Weak flush that clogs weekly regardless of parts"),
                       ("Leak location", "Tank-to-bowl gasket or supply connection",
                        "Hairline crack in the porcelain"),
                       ("Rocking or movement", "Loose closet bolts",
                        "Rotted subfloor under the flange"),
                       ("Water usage", "Current efficient model",
                        "Old high-volume model on a metered supply"),
                       ("How many bathrooms it affects", "One fixture",
                        "Multiple original fixtures of the same age")])),
        sec("Why is water pooling around the base of my toilet?",
            "Water at the base is either condensation on the outside of the bowl in a humid "
            "bathroom, a failed wax ring under the toilet, or a crack. The wax ring is the "
            "common one and the fix means pulling the toilet, replacing the seal, and checking "
            "whether the subfloor underneath has started to soften after "
            "<a href=\"/plumbing/leak-detection\">a long-running leak</a>."),
    ],
    sectionsTail=[
        sec("Why does my toilet clog over and over?",
            "Repeat clogs in one toilet usually mean a weak-flushing low-flow model from the "
            "first generation of them, an object lodged in the trapway, or a partial blockage "
            "further down the branch line. If "
            "<a href=\"/plumbing/clogged-drain\">more than one fixture is slow</a>, the "
            "problem is not the toilet at all."),
        sec("What does a toilet replacement include?",
            "The old unit is disconnected, pulled and hauled away, the flange and subfloor are "
            "inspected before anything new goes down, a new wax ring and supply line go in, "
            "and the new toilet is set, leveled and flush-tested. Leaving the old toilet at "
            "the curb is not part of it."),
        sec("Can you fix a toilet the same day?",
            call("Usually. Toilet work is short enough that it often fits the day you book it, "
                 "and common flappers, fill valves, supply lines and wax rings ride on the "
                 "truck. Call {tel}, or "
                 "<a href=\"/plumbing/emergency-plumbing\">the emergency line</a> if the "
                 "overflow is already on the floor. Either way it is a "
                 "<a href=\"/plumbing/services\">licensed Ohio plumber</a> at your door.")),
    ],
    faqH2="What else do homeowners ask about toilets?",
    faq=qa(
        ("Should I repair or replace my toilet?",
         "Repair wins when a flapper, fill valve, supply line or wax ring has failed. "
         "Replacement wins when the porcelain is cracked, when the unit predates the 1994 "
         "efficiency standard, or when it clogs weekly no matter what parts go in."),
        ("How much water does a running toilet waste?",
         "A toilet that runs continuously can waste about 200 gallons a day. On a metered "
         "supply that shows up on the next bill, which is how most people discover it."),
        ("Can I fix a running toilet myself?",
         "Often, yes. A replacement flapper costs a few dollars and takes about ten minutes "
         "with the water shut off at the wall. If a new flapper does not stop it, the fill "
         "valve is the next part and that one is still homeowner-friendly."),
        ("Why does my toilet rock when I sit on it?",
         "Either the two closet bolts holding it to the floor have loosened, or the subfloor "
         "under the flange has gone soft from a long-running leak. The first is a five-minute "
         "fix and the second is a floor repair, so it is worth finding out which before it "
         "gets worse."),
        ("How fast can you get here for a toilet repair?",
         "Most calls are handled the same day, and a house down to one working bathroom gets "
         "moved up the list."),
    ))

geo(PLUMB_PAGES, "water-treatment.html",
    h1="Water softeners and whole-home filtration in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="Softeners, filtration and reverse osmosis, sized against a tested hardness figure "
          "rather than a sales quota.",
    answer="The water here comes out of limestone, so every municipal system around delivers "
           "at least 7 grains per gallon. We test what is actually coming out of your tap "
           "before recommending a softener, a filter or reverse osmosis.",
    callout="Curious what's in your water? Call {tel}. We test first and recommend second.",
    sections=[
        sec("How hard is the water in Dayton and Cincinnati?",
            "Every water system in this footprint pulls from limestone and dolomite formations "
            "or the Great Miami Buried Valley Aquifer, so the raw water is very hard before "
            "treatment. What comes out of your tap depends entirely on which utility you are "
            "on, and three of them changed within the last four years.",
            sid="hardness",
            # Restructured after the client read it and said it was confusing. It was:
            # Water system | Communities served | Hardness delivered | Recent change.
            # That asks a homeowner to know which utility they are on before they can
            # find their row, then hands them a number in grains per gallon with
            # nothing saying whether that is bad. The utility's project history had a
            # column of its own and the Dayton row's answer was "go read the report".
            # Now: find your town, see the number, read what it means. 7 gpg is the
            # standard threshold for "hard", so every row here is hard water — which
            # is the actual finding and is now impossible to miss.
            table=tbl("Water hardness by community, and what it means for your home.",
                      "Every municipal system across the Dayton and Cincinnati metros "
                      "delivers at least 7 grains per gallon, the point at which water "
                      "is classed as hard. The question is not whether your water is "
                      "hard, it is whether it is costing you anything.",
                      ["If you're in", "Your water runs", "What that means"],
                      [("<a href=\"/locations/beavercreek\">Beavercreek</a>, Beavercreek "
                        "Twp, Xenia Twp, Cedarville, parts of Kettering and Centerville",
                        "About 8 grains per gallon",
                        "Hard. Greene County cut it from 27 grains in early 2025, so "
                        "scale builds far slower than it used to."),
                       ("Dayton and the communities it supplies wholesale",
                        "About 7 to 8 grains per gallon",
                        "Hard. Lime softened at the Bolton plant."),
                       ("Cincinnati, most of Hamilton County, Mason",
                        "7 to 8 grains per gallon",
                        "Hard. Greater Cincinnati Water Works, steady for years."),
                       ("Franklin and the Renneker service area",
                        "About 8 grains per gallon",
                        "Hard. Warren County cut it by roughly 55% with nanofiltration "
                        "in 2022."),
                       ("Huber Heights",
                        "About 7 grains per gallon",
                        "Hard, at the low end. A new softening plant brought it down "
                        "from about 18 grains."),
                       ("West Chester, Liberty Twp, Fairfield, Monroe",
                        "About 7.7 grains per gallon",
                        "Hard. Butler County Water and Sewer, steady for years."),
                       ("A private well in Greene, Warren or Miami County",
                        "Varies widely",
                        "Test before you decide anything. None of the utility softening "
                        "projects changed well water.")])),
        sec("Do I need a water softener in Dayton?",
            ["Every municipal system in this footprint delivers at least 7 grains per gallon, "
             "which is the point at which water is normally classified as hard. Whether it is "
             "worth it for your house depends on what you are seeing: "
             "<a href=\"/plumbing/water-heater/installation\">scale on fixtures</a>, dishes "
             "that spot, <a href=\"/plumbing/water-heater/overview\">appliances failing "
             "early</a>, and laundry that comes out stiff.",
             "If you are seeing two or three of those, hardness is doing it. If you are seeing "
             "none of them, you may not need anything, and we will say so."]),
        sec("My water got softer in 2025. Does my softener still work?",
            ["If you are on Greene County water in Beavercreek, Beavercreek Township, Xenia "
             "Township, Cedarville, or parts of Kettering and Centerville, your supply went "
             "from 27 grains per gallon to about 8 in early 2025. A softener still programmed "
             "for 27 is now over-softening, burning through salt, and sending very "
             "low-hardness water through your pipes. It needs re-dialing, not replacing.",
             "That is an adjustment, not a new installation, and it is worth doing. Every bag "
             "of salt since early 2025 has been paying for hardness that is no longer "
             "there."]),
        sec("What is the difference between a softener, a filter and reverse osmosis?",
            "A softener removes calcium and magnesium, which is what causes scale. A "
            "whole-home filter removes chlorine, sediment and taste or odor problems at every "
            "tap. Reverse osmosis produces drinking-quality water at one fixture, usually the "
            "kitchen sink. They solve different problems and plenty of homes run two of them.",
            table=tbl("Water treatment options compared.",
                      "We size any of these from a tested hardness number and how much water "
                      "your household actually uses, not from the rating on the box.",
                      ["Factor", "Water softener", "Whole-home filtration", "Reverse osmosis"],
                      [("What it removes", "Calcium and magnesium hardness",
                        "Chlorine, sediment, taste and odor",
                        "Dissolved solids, most contaminants"),
                       ("Where it installs", "On the main line where water enters",
                        "On the main line where water enters",
                        "Under one sink, usually the kitchen"),
                       ("What it fixes",
                        "Scale, spotting, stiff laundry, early appliance failure",
                        "Chlorine smell, cloudy or discolored water",
                        "Drinking and cooking water quality"),
                       ("Service interval", "Salt refills, periodic setting check",
                        "Cartridge changes on a schedule",
                        "Membrane and filter changes on a schedule"),
                       ("Best fit", "Any home above 7 grains per gallon",
                        "Municipal supply with taste or odor complaints",
                        "Households buying bottled water"),
                       ("Well water",
                        "Requires testing first, iron changes the answer",
                        "Requires testing first",
                        "Common on wells after primary treatment")])),
    ],
    sectionsTail=[
        sec("Will softened water taste salty?",
            "No. A correctly set softener adds far less sodium than people expect, and the "
            "exchange happens on the calcium, not on the flavor. If sodium is a genuine "
            "concern for a household, a reverse osmosis tap removes it entirely for drinking "
            "and cooking."),
        sec("Does city water or well water change the recommendation?",
            ["Completely. Municipal supply in this area is predictable, hardness is published, "
             "and the treatment question is mostly about hardness and chlorine. Wells vary "
             "street by street and can carry iron, sulfur, bacteria or nitrates, none of which "
             "a softener addresses. Well homes get tested before anyone recommends equipment.",
             "One thing worth knowing if you are on a well in Greene County: the 2025 softening "
             "change was a utility project. It did not touch your water at all."]),
        sec("What does water treatment installation involve?",
            call("<a href=\"/contact\">A water test</a> comes first, then sizing against your "
                 "household's real usage rather than a box rating. Installation ties into the "
                 "main line with a bypass so the house still has water if the unit is "
                 "serviced, and the result is verified at the tap before anyone leaves. Call "
                 "{tel} to book it with "
                 "<a href=\"/plumbing/services\">licensed Ohio plumbers</a>, " + LICENCE_LINE + ".")),
    ],
    faqH2="What else do homeowners ask about hard water?",
    faq=qa(
        ("Is Dayton's water hard enough to need a softener?",
         "Dayton-area municipal water is lime softened and still lands in the hard range. "
         "Whether a softener is worth it for a specific home depends on the scale you are "
         "seeing, how appliances are holding up, and what a test measures."),
        ("Beavercreek water changed in 2025. Do I still need my softener?",
         "Greene County Sanitary Engineering cut delivered hardness from 27 grains per gallon "
         "to about 8 between January and March 2025. Most Beavercreek softeners still need to "
         "run, but at a much lower setting. Left on the old setting they over-soften and waste "
         "salt."),
        ("How hard is Mason's water?",
         "Mason is supplied by Greater Cincinnati Water Works rather than by Warren County, so "
         "Mason homes get 7 to 8 grains per gallon. Warren County customers a few miles away "
         "are on a different, separately softened supply."),
        ("Do you test water before recommending anything?",
         "Yes. A water test drives the recommendation, and on well water it is not optional, "
         "because iron, sulfur and bacteria all present as \"bad water\" and none of them are "
         "fixed by a softener."),
        ("How long does a water softener last?",
         "Well-maintained units commonly run 10 to 15 years. Resin exhaustion and control "
         "valve failure are the usual end points, and a unit running on a badly wrong hardness "
         "setting wears out sooner."),
    ))

# ======================================================================
# Plumbing families
# ======================================================================

geo(PLUMB_FAMILIES, "sewer-line/overview.html",
    h1="Sewer line inspection, cleaning and repair in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="Nobody should pay to dig up a yard on a guess. The camera goes in first, and the "
          "quote comes after the footage.",
    answer="Backups that keep coming back, a soggy patch of lawn, sewage smell outside. We put "
           "a camera the full length of your line first, and you watch the same screen we do "
           "before anything is quoted or dug.",
    callout="Sewage backing up indoors? Stop running water and call {tel}. "
            "<a href=\"/plumbing/emergency-plumbing\">That is an emergency</a> and it is "
            "handled around the clock.",
    sections=[
        sec("How do I know if my sewer line is broken?",
            ["The signal is repetition, not severity. Backups that return weeks after a "
             "cleaning, <a href=\"/plumbing/clogged-drain\">several fixtures slow at once</a>, "
             "sewage odor outside near the line, a patch of yard that stays soggy or greener "
             "than the rest, or a section of lawn that has sunk. One of those is worth a "
             "camera. Two is a broken line until proven otherwise.",
             "A backup that comes back within weeks of a cleaning is not a clog you got "
             "unlucky with. Something in the pipe is holding it, and cleaning it again will "
             "not change that."]),
        sec("What does a sewer camera inspection show?",
            "A camera pushed the length of the lateral shows exactly what a plumber is dealing "
            "with: root masses at pipe joints, a belly holding standing water, offset joints "
            "where the pipe has shifted, cracks, or a full collapse. It also shows the depth "
            "and the distance from the house, which is what determines whether a repair can be "
            "done trenchless.",
            table=tbl("Common sewer line findings and what each one calls for.",
                      "These are the seven things the camera usually turns up, and only two of "
                      "them mean digging.",
                      ["What the camera shows", "What caused it", "What it needs"],
                      [("Root mass at a pipe joint", "Tree roots entering a clay joint",
                        "Hydro jetting, then repair or lining at that joint"),
                       ("Standing water in a low section", "A belly from settled soil",
                        "Excavation and re-grading of that section"),
                       ("Offset at a joint", "Ground movement or a shifted pipe",
                        "Spot repair, or lining if the offset is small"),
                       ("Grease coating the full diameter", "Kitchen waste over years",
                        "Hydro jetting, then a maintenance schedule"),
                       ("Cracks along the pipe barrel", "Aged clay or cast iron",
                        "Trenchless lining, or replacement"),
                       ("Full collapse, camera cannot pass", "Structural failure",
                        "Excavation and replacement of that run"),
                       ("Clean, sound pipe with a soft blockage", "An ordinary clog",
                        "Cleaning, no repair required")])),
        sec("Who is responsible for the sewer lateral, me or the city?",
            "In most Ohio communities the homeowner owns and maintains the lateral from the "
            "house to the connection at the public main, including the portion under the "
            "street or the tree lawn. The exact boundary and any city assistance programs vary "
            "by municipality, so it is worth confirming with your own before work begins."),
        sec("Do you have to dig up my yard?",
            "Not always. Where the pipe is structurally sound enough to hold a liner, "
            "<a href=\"/plumbing/sewer-line/repair\">trenchless methods</a> repair from access "
            "points at each end and leave the lawn between them intact. Where the line has "
            "collapsed, dropped, or bellied, the ground has to be opened. The camera tells us "
            "which before anyone commits."),
    ],
    sectionsTail=[
        sec("What causes sewer line failure in older Dayton homes?",
            ["Age of the pipe, mostly. A large share of "
             "<a href=\"/locations/dayton\">Dayton's housing</a> predates 1940, and the "
             "laterals under those homes are clay tile or cast iron with mortared joints that "
             "roots find easily. Newer suburban stock in Beavercreek, Mason and West Chester "
             "is usually PVC and fails differently, more often from settling than from roots.",
             "If your house predates the war and still has its original lateral, roots are the "
             "first thing we look for. It is the most common finding on that vintage of "
             "pipe."]),
        sec("How much does sewer work cost?",
            "Sewer repair is the largest single plumbing project most homeowners will face, "
            "and the range is wide because depth, length and access change everything. Every "
            "job is quoted flat after the camera pass, with the footage available so you can "
            "see what you are paying to fix. Financing is available on larger sewer work."),
        sec("How do I book a sewer inspection?",
            call("Call {tel} or book online. If sewage is already backing up indoors, stop "
                 "running water anywhere in the house first, then call. Sewage indoors is an "
                 "emergency and it gets handled around the clock. Where the pipe is intact and "
                 "only loaded with grease or roots, "
                 "<a href=\"/plumbing/sewer-line/cleaning\">hydro jetting</a> is the cheaper "
                 "answer.")),
    ],
    faqH2="What else do homeowners ask about sewer lines?",
    faq=qa(
        ("What are the signs of a broken sewer line?",
         "Backups that return within weeks of a cleaning, multiple fixtures draining slowly at "
         "once, sewage odor outdoors near the line, a permanently soggy or unusually green "
         "patch of yard, and sunken ground along the line's path. Any two of those together "
         "justify a camera inspection."),
        ("Do I have to dig up the yard to fix a sewer line?",
         "Not necessarily. Trenchless lining and pipe bursting repair many failures from "
         "access points at each end, leaving the ground between them undisturbed. A collapsed "
         "or bellied line still needs excavation, and the camera inspection determines which "
         "case applies before anything is quoted."),
        ("Am I responsible for the sewer line under the street?",
         "In most Ohio communities the homeowner owns the lateral all the way to the "
         "connection at the public main, including the portion under the tree lawn or the "
         "street. The boundary and any city assistance program vary by municipality, so "
         "confirm with yours."),
        ("How often should a sewer line be inspected?",
         "Every few years is reasonable for a home with mature trees or clay pipe, and a "
         "camera inspection is worth doing before buying an older house. Homes with no history "
         "of backups and modern PVC laterals rarely need routine inspection."),
        ("How fast can you get a camera in the line?",
         "Most calls are handled the same day, and an active backup goes out ahead of a "
         "scheduled inspection."),
    ))

geo(PLUMB_FAMILIES, "sump-pump/overview.html",
    h1="Sump pump repair, replacement and battery backups in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="Storms that flood basements are usually the same storms that take the power out. "
          "That is the problem a backup exists to solve.",
    answer="A sump pump lasts 7 to 10 years and then fails during a storm, which is also when "
           "the power goes out. We repair, replace and add battery backups, and flood-test the "
           "pit through a full cycle before leaving.",
    callout="Storm season doesn't wait. Call {tel} before the next heavy rain tests your pump, "
            "or before <a href=\"/plumbing/emergency-plumbing\">a flooded basement</a> makes "
            "the decision for you.",
    sections=[
        sec("How long does a sump pump last?",
            ["Seven to ten years is the working range. A pump that is cycling constantly "
             "because the pit is undersized wears out at the short end of that; a pump in a "
             "dry basement that runs a few times a spring can go longer. Age alone is reason "
             "enough to consider "
             "<a href=\"/plumbing/sump-pump/installation\">replacing before a storm "
             "season</a>, because failure is not gradual.",
             "That is the argument for replacing on age rather than waiting for a warning you "
             "will not get. Pumps stop on the night the pit is fullest."]),
        sec("Do I need a sump pump in the Dayton area?",
            "Most homes here with a full basement have one, and full basements are the norm "
            "across older Dayton neighborhoods and most of the suburban stock. A high water "
            "table, clay soil that sheds water toward foundations, and heavy spring rain are "
            "all local. If your basement has a pit, it was put there for a reason."),
        sec("What are the signs my sump pump is failing?",
            "A pump that runs constantly, or one that never runs while the pit fills. Grinding "
            "or rattling instead of a clean hum. A pit that fills faster than the pump empties "
            "it. Visible rust or a float that sticks. Any pump past seven years with any of "
            "those is worth replacing before the forecast turns.",
            table=tbl("Sump pump types compared.",
                      "We size against your pit, how high the discharge has to lift and how "
                      "fast the water comes in, not against the horsepower on the box.",
                      ["Factor", "Pedestal pump", "Submersible pump", "Battery backup"],
                      [("Where the motor sits", "Above the pit on a shaft",
                        "Inside the pit, underwater", "Alongside the primary pump"),
                       ("Typical service life", "Often longer, motor stays dry",
                        "7 to 10 years", "Pump longer, battery shorter"),
                       ("Noise", "Audible, motor is in the open", "Quieter, water muffles it",
                        "Only runs when the primary cannot"),
                       ("Pit size needed", "Works in a narrow pit", "Needs a wider pit",
                        "Needs room for a second pump"),
                       ("Capacity", "Lower flow", "Higher flow",
                        "Intermittent, designed to outlast an outage"),
                       ("Power outage protection", "None", "None",
                        "This is the entire point of it"),
                       ("Best fit", "Narrow older pits, budget replacement",
                        "Most homes, finished basements",
                        "Any finished basement, any home that loses power in storms")])),
        sec("Do I really need a battery backup?",
            ["If the basement is finished, or if storms knock your power out, yes. The rain "
             "event that overwhelms a pit is frequently the same event that takes down the "
             "grid, and a primary pump with no electricity does nothing at all. A backup runs "
             "on its own battery and takes over automatically.",
             "It is the one piece of this that only matters on the worst night of the year, "
             "which is exactly why people skip it and then regret it."]),
    ],
    sectionsTail=[
        sec("Why does my sump pump run constantly?",
            "Usually one of four things: a float switch stuck in the on position, a failed "
            "check valve letting discharged water run back into the pit, a pit that is too "
            "small for the inflow, or a genuinely high water table after a wet stretch. "
            "<a href=\"/plumbing/sump-pump/repair\">The first three are repairs</a> and all "
            "are testable in one visit."),
        sec("How do I test my own sump pump?",
            call("Pour a five gallon bucket of water into the pit and watch. The float should "
                 "rise, the pump should start, the pit should empty, and the pump should shut "
                 "off cleanly without short-cycling. Do it every spring before storm season. "
                 "If any part of that sequence hesitates, call {tel} and a "
                 "<a href=\"/plumbing/services\">licensed Ohio plumber</a> will look at it, "
                 "working " + LICENCE_LINE + ". If the water is coming up through a floor "
                 "drain instead of the pit, that is "
                 "<a href=\"/plumbing/sewer-line/cleaning\">storm water in the sanitary "
                 "line</a> and a different job entirely.")),
    ],
    faqH2="What else do homeowners ask about sump pumps?",
    faq=qa(
        ("How long should a sump pump last before I replace it?",
         "About 7 to 10 years. Replacing on age rather than on failure is the cheaper path, "
         "because sump pumps fail during heavy rain and the cost of a flooded basement is not "
         "the pump."),
        ("Do I need a battery backup sump pump in Ohio?",
         "If the basement is finished or your power goes out during storms, yes. The same "
         "storms that fill a sump pit take down power lines, and a primary pump without "
         "electricity does nothing."),
        ("Why is my sump pump making a loud noise?",
         "Grinding usually means a failing motor or bearing, rattling often means a loose "
         "discharge pipe or a failed check valve, and a gulping sound at the end of each cycle "
         "is normal on some installations. Any new noise is worth a look before storm season."),
        ("Can I install a sump pump myself?",
         "A like-for-like swap is within reach for a confident homeowner, but sizing, "
         "discharge routing and check valve placement are where most DIY installs go wrong. A "
         "pump that is undersized or discharging into the wrong place fails at exactly the "
         "wrong time."),
        ("How often should a sump pump be serviced?",
         "Test it yourself each spring with a bucket of water, and have it inspected when the "
         "pump passes seven years or if the cycle sounds different. Battery backups also need "
         "their battery checked, which is the part people forget."),
    ))

geo(PLUMB_FAMILIES, "gas-line/overview.html",
    h1="Gas line installation, repair and appliance hookups in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="If you smell gas right now, stop reading. Leave the house and call your gas utility "
          "from outside.",
    answer="New runs for ranges, dryers, grills, garage heaters and standby generators, plus "
           "repairs on lines already in the ground. Every job is done " + LICENCE_LINE + ", "
           "permitted where your jurisdiction requires it, and pressure-tested at the end.",
    callout="<b>Safety first:</b> smell gas? Leave the house first, don't flip switches, then "
            "call your gas utility from outside. Call {tel} for the repair once the property "
            "is clear.",
    sections=[
        sec("Who is licensed to run a gas line in Ohio?",
            ["Gas piping is licensed work. Plumbing and HVAC contractors in Ohio are licensed "
             "at the state level through the Ohio Construction Industry Licensing Board, and "
             "many municipalities require a local contractor registration on top of that. "
             "We hold Ohio plumbing license #13557 and "
             "<a href=\"/services\">Ohio HVAC license #37179</a>.",
             "Both numbers are checkable, and you should check them, on anyone who quotes you "
             "gas work."]),
        sec("What should I do if I smell gas?",
            "Leave the building first, with everyone in it. Do not flip a light switch, unplug "
            "anything, use a phone indoors, or light a match. From outside and well away, call "
            "your gas utility's emergency line. Once the utility has made the property safe, "
            "call a licensed plumber to "
            "<a href=\"/plumbing/gas-line/repair\">locate and repair the leak</a>.",
            sid="smell-gas",
            table=tbl("Gas situations and the correct order of calls.",
                      "The gas utility makes a property safe and a licensed plumber repairs "
                      "the line, which is why a suspected gas leak means two calls in a fixed "
                      "order.",
                      ["What's happening", "Call first", "Then call"],
                      [("Strong gas smell indoors",
                        "Leave the house, then the gas utility from outside",
                        "Us, once the property is cleared"),
                       ("Faint smell near one appliance", "The gas utility, from outside",
                        "Us, for appliance connection and testing"),
                       ("Hissing from a buried line outdoors",
                        "The gas utility, from a distance", "Us, for the repair"),
                       ("Dead grass in a line over a buried gas line", "The gas utility",
                        "Us, for locating and repair"),
                       ("Pilot lights repeatedly going out", "Us",
                        "The utility, only if you can smell gas"),
                       ("<a href=\"/plumbing/gas-line/installation\">Adding a line for a new "
                        "appliance</a>", "Us", "No utility call needed")])),
        sec("Which utility supplies natural gas here?",
            ["In the Dayton metro, natural gas comes from CenterPoint Energy Ohio, which was "
             "Vectren until it was renamed in May 2021, while electricity comes separately "
             "from AES Ohio. In the Cincinnati metro, Duke Energy Ohio supplies both gas and "
             "electricity. The two metros are structured differently, which matters when you "
             "are outside the house looking up an emergency number.",
             "Worth putting the right one in your phone now, while nothing is wrong."]),
        sec("Do I need a permit for gas line work?",
            "Most new gas piping does, along with an inspection, and who issues it depends on "
            "where you live. Greene County permits Beavercreek but not Fairborn or Xenia, and "
            "the City of Dayton runs its own plumbing inspection separate from the county "
            "program. We pull the permit and close out the inspection as part of the job."),
    ],
    sectionsTail=[
        sec("What can a gas line be run for?",
            "Ranges and cooktops, clothes dryers, outdoor grills and fire pits, pool and spa "
            "heaters, garage and shop heaters, standby generators, and fireplace logs. Each "
            "has a different BTU demand, which is why a line sized for a dryer will not "
            "necessarily carry a generator on the same run, and why "
            "<a href=\"/plumbing/water-heater/installation\">a larger gas line for a tankless "
            "unit</a> is part of that conversation."),
        sec("How is a gas leak found?",
            call("Electronic gas detection equipment and a pressure test on an isolated "
                 "section. The pressure test is the part that matters: a section of pipe is "
                 "isolated, brought up to pressure, and watched, so a pass is measured rather "
                 "than sniffed. Every gas job we do ends with one, documented for your "
                 "records. Call {tel}, or "
                 "<a href=\"/plumbing/emergency-plumbing\">24/7 emergency plumbing</a> if "
                 "something is happening now.")),
    ],
    faqH2="What else do homeowners ask about gas lines?",
    faq=qa(
        ("Who is licensed to install a gas line in Ohio?",
         "Gas piping is licensed work, regulated by the Ohio Construction Industry Licensing "
         "Board, and many municipalities want a local contractor registration on top. We hold "
         "Ohio plumbing license #13557."),
        ("What do I do if I smell gas in my house?",
         "Leave immediately with everyone in the building. Do not touch light switches, unplug "
         "anything, or use a phone indoors. From outside, call your gas utility's emergency "
         "line, then call a licensed plumber once the property has been cleared."),
        ("Can you run a gas line to my grill?",
         "Yes. An outdoor grill or fire pit line is a common job. It is sized to the "
         "appliance's BTU demand, run with a shutoff at the connection point, pressure-tested, "
         "and permitted where required."),
        ("Do you handle the permit and the inspection?",
         "Yes. We pull the permit, schedule the inspection and close it out. Who issues it "
         "changes from one town to the next around here, which is part of why it is worth "
         "handing over."),
        ("How do you know a gas line is safe after a repair?",
         "Every gas job ends with a pressure test on the isolated section and an electronic "
         "leak check, and the result is documented for your records. A visual inspection alone "
         "is not a test."),
    ))

geo(PLUMB_FAMILIES, "water-heater/repair.html",
    h1="Same-day water heater repair in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="No hot water this morning is a today problem. It gets triaged on the phone before "
          "anyone is dispatched.",
    answer="Elements, thermostats, gas valves, thermocouples, pilots that will not stay lit: "
           "all of it repairable, usually the same day, with the common parts already on the "
           "truck. A tank leaking from its base is the exception, and that one needs replacing.",
    callout="No hot water this morning? Call {tel}. Repairs get priority dispatch.",
    sections=[
        sec("Why do I have no hot water?",
            "On a gas unit the usual causes are a pilot that will not stay lit, a failed "
            "thermocouple, or a gas valve that has quit. On an electric unit it is almost "
            "always a tripped high-limit reset, a burned-out upper element, or a failed "
            "thermostat. All four are same-visit repairs with parts on the truck. The "
            "<a href=\"/plumbing/water-heater/overview\">water heater services overview</a> "
            "covers tank and tankless side by side."),
        sec("Why does my hot water run out so fast?",
            ["Two likely causes. Scale on the tank bottom takes up volume that used to be "
             "water, which is common given "
             "<a href=\"/plumbing/water-treatment\">local water hardness</a>. Or the lower "
             "element on an electric unit has failed, leaving only the top of the tank "
             "heating. Both are diagnosable in one visit.",
             "We check both on the first visit, because there is no way to tell them apart "
             "from the outside and guessing wastes your morning."]),
        sec("My water heater is leaking. Is that repairable?",
            ["It depends entirely on where. Water from a fitting, the T&amp;P valve or the "
             "drain valve is a repair. Water seeping from the bottom of the tank itself is the "
             "steel shell failing, and no repair holds. Shut the cold supply valve above the "
             "unit and call, because a failing tank does not fail slowly for long.",
             "There is no patch for a failed tank shell. If someone offers you one, you are "
             "buying a few weeks."]),
    ],
    table=tbl("When a water heater is worth repairing and when it should be replaced.",
              "Past its expected life, or with a repair quote nearing a third of what a new "
              "one costs, and you are better off replacing it.",
              ["What we look at", "Repair when", "Replace when"],
              [("Age", "Under about 8 years old",
                "Past 10 years, near the end of an 8 to 12 year life"),
               ("What failed", "Thermostat, element, thermocouple, gas valve or T&amp;P valve",
                "The tank shell itself is seeping or rusted through"),
               COST_ROW,
               ("Failure history", "First fault the unit has had",
                "Second or third service call in a year"),
               ("Hot water capacity", "Full capacity once the fault is fixed",
                "Never enough hot water even when working"),
               ("Water quality", "Hot water runs clear",
                "Rusty hot water with clear cold water"),
               ("Efficiency", "Current unit still meets the household's needs",
                "Household has grown or wants tankless")],
              h2="Should I repair or replace my water heater?", sid="repair-or-replace",
              eyebrow="REPAIR OR REPLACE"),
    sectionsTail=[
        sec("Is a water heater repair covered by a warranty?",
            "Manufacturer warranties on tanks and parts vary by brand and by how the unit was "
            "registered, and we check yours before quoting. The repair itself is quoted flat "
            "and approved before any work starts, and it is carried out " + LICENCE_LINE + "."),
        sec("How do I book water heater repair?",
            call("Call {tel} or book online. If the tank is actively leaking, shut the cold "
                 "supply valve on top of the unit before you do anything else, then call. That "
                 "one turn is the difference between a wet floor and "
                 "<a href=\"/plumbing/emergency-plumbing\">a wet basement</a>. Where the tank "
                 "itself has gone, <a href=\"/plumbing/water-heater/installation\">plan on a "
                 "replacement</a>.")),
    ],
    faqH2="What else do homeowners ask when the hot water quits?",
    faq=qa(
        ("How fast can you fix my water heater?",
         "Usually the same day. No-hot-water calls get moved up, and common elements, "
         "thermostats, thermocouples and gas valves are already on the truck."),
        ("My water heater is leaking from the bottom. Can it be repaired?",
         "No. Water seeping from the base of the tank means the steel shell has failed, and "
         "there is no repair that holds once that happens. Shut the cold supply valve above "
         "the unit and plan on a replacement."),
        ("Is it worth repairing a water heater that is over ten years old?",
         "Usually not. A conventional tank lasts roughly 8 to 12 years, so a repair at eleven "
         "years buys time on a unit that is likely to fail again. We will price the repair and "
         "the replacement side by side so the comparison is yours to make."),
        ("Why won't my pilot light stay lit?",
         "The most common cause is a failed thermocouple, the small sensor that tells the gas "
         "valve the pilot is burning. It is an inexpensive part and a single-visit repair. A "
         "pilot that keeps going out can also point at a venting or draft problem, which is "
         "worth checking rather than relighting repeatedly."),
        ("Do you repair both gas and electric water heaters?",
         "Yes, gas and electric, tank and tankless, every major brand, regardless of who "
         "installed the unit."),
    ))

geo(PLUMB_FAMILIES, "water-heater/installation.html",
    h1="Water heater installation and replacement in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="Replacing a tank before it goes beats mopping a utility room after it does. Sized "
          "to your household, set to code, old unit hauled away.",
    answer="Tank or tankless, sized to what your household actually uses at its busiest. Set "
           "to code, tested at every tap, old unit hauled away. Common sizes are on the "
           "shelf, so most replacements finish the same day.",
    callout="Replacing before failure beats a flooded utility room. Call {tel} for honest "
            "numbers.",
    sections=[
        sec("When should I replace my water heater instead of repairing it?",
            "A tank past ten years, a unit leaking anywhere on the shell, rusty hot water, "
            "repeat repairs in a single year, or a household that has outgrown its capacity. "
            "Any one of those makes replacement the better money. Replacing ahead of a failure "
            "also means choosing the unit rather than taking what is in stock at 9 p.m. Where "
            "the fault is a part rather than the tank, "
            "<a href=\"/plumbing/water-heater/repair\">repairing it</a> is cheaper."),
        sec("What size water heater do I need?",
            ["Sizing works off peak demand. A household of one or two usually lands on 30 to "
             "40 gallons, three or four on 40 to 50, and five or more on 50 to 80 gallons or a "
             "tankless unit. Simultaneous showers, a large tub, or a high-flow shower head all "
             "push the number up.",
             "We size against that peak, not against whatever is being carried out. Plenty of "
             "houses have been living with an undersized tank for years without knowing it."]),
        sec("Should I switch to tankless?",
            "Tankless makes sense when you are running out of hot water, when the utility room "
            "space matters, or when the existing gas and venting are already being opened up. "
            "It costs more to install because it needs "
            "<a href=\"/plumbing/gas-line/installation\">a larger gas line</a> and dedicated "
            "venting. In a home with adequate hot water, a tank is usually the better value, "
            "and the <a href=\"/plumbing/water-heater/overview\">tank and tankless "
            "comparison</a> lays both out."),
        sec("What does a water heater installation include?",
            ["Draining and removing the old unit, checking the gas line, venting, electrical "
             "and water connections against current code, setting the new unit with a new "
             "expansion tank and shut-off where required, testing at every tap, and hauling "
             "the old heater away. We pull the permit where your jurisdiction requires one.",
             "All of it " + LICENCE_LINE + ", and none of it as a line item added after the "
             "fact."]),
    ],
    sectionsTail=[
        sec("How long does it take?",
            "A straight tank-for-tank swap is usually a few hours. A tankless conversion runs "
            "longer, because the gas line sizing, the venting and sometimes the electrical all "
            "change. Common tank sizes are stocked, so most replacements happen the day you "
            "approve the quote."),
        sec("Is financing available on a water heater replacement?",
            "Yes, on qualifying installations. A water heater rarely fails on a convenient "
            "week, so monthly options exist for exactly that reason. Current terms are on our "
            "<a href=\"/financing-options\">financing</a> page."),
        sec("Does hard water shorten the life of a new water heater?",
            "Yes, and it is worth planning around here. Every municipal system in the "
            "footprint delivers at least 7 grains per gallon, and that scale settles in the "
            "tank bottom and coats electric elements. Flushing the tank annually helps, and "
            "<a href=\"/plumbing/water-treatment\">a softener</a> helps more if the house does "
            "not already have one."),
    ],
    faqH2="What else do homeowners ask before replacing a water heater?",
    faq=qa(
        ("Can you install a water heater the same day?",
         "Usually. Common tank sizes are stocked, so a like-for-like swap often happens the "
         "day you approve the quote. Tankless conversions take longer, because the gas and the "
         "venting have to be changed first."),
        ("What size water heater does a family of four need?",
         "Most four-person households land on a 40 to 50 gallon tank. If two showers run at "
         "the same time most mornings, size up rather than down, because recovery rate is what "
         "people actually notice."),
        ("Do you haul away the old water heater?",
         "Yes. Removal and disposal of the old unit is part of every installation, not a line "
         "item added afterward."),
        ("Do I need a permit to replace a water heater in Ohio?",
         "It depends on the jurisdiction, and in this service area it genuinely varies. The "
         "City of Dayton runs its own plumbing inspection, and several neighboring communities "
         "issue their own permits. We check before the work and pull whatever is required."),
        ("What is an expansion tank and do I need one?",
         "It is a small tank that absorbs pressure when water heats and expands. Closed "
         "plumbing systems, which most newer installations are, require one to keep pressure "
         "off the T&amp;P valve and the heater itself. Where code calls for one, it goes in "
         "with the heater."),
    ))

geo(PLUMB_FAMILIES, "sewer-line/repair.html",
    h1="Sewer line repair and replacement in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="You see the break on the screen before you see a number on the quote. Trenchless "
          "where the pipe allows, excavation only where it does not.",
    answer="This is the biggest plumbing bill most people ever face, so the camera goes down "
           "your line first and the quote comes after the footage. Where the pipe can carry a "
           "liner, the lawn between the access points stays put.",
    callout="Repeat backups mean the line itself is failing. Call {tel} for a "
            "<a href=\"/plumbing/sewer-line/overview\">camera inspection</a> before it "
            "collapses.",
    sections=[
        sec("Can you repair a sewer line without digging up my yard?",
            "Often, yes. Trenchless repair works from access points at each end of the damaged "
            "run, pulling a liner through the existing pipe or bursting the old pipe outward "
            "while drawing new pipe in behind it. The lawn between the access points is left "
            "alone. Whether it applies depends on what the camera shows.",
            sid="trenchless",
            table=tbl("Trenchless sewer repair compared with open-cut excavation.",
                      "Wherever your pipe can carry a liner, we go trenchless. We dig only "
                      "when the line has collapsed, bellied or shifted too far to line.",
                      ["Factor", "Trenchless repair", "Open-cut excavation"],
                      [("Yard disruption",
                        "Two small access pits, lawn between them untouched",
                        "An open trench the length of the damaged run"),
                       ("When it works", "Pipe is continuous and holds its shape",
                        "Pipe has collapsed, bellied, or badly offset"),
                       ("Restoration afterward", "Backfill at the access points only",
                        "Regrading, reseeding, and any hardscape put back"),
                       ("Driveways and patios", "Usually crossed without breaking them",
                        "Concrete or paving over the line has to come up"),
                       ("Time on site", "Typically shorter", "Longer, and weather-dependent"),
                       ("Depth of line", "Handles deep runs without a deep trench",
                        "Deeper lines mean a wider, more expensive trench"),
                       ("What decides it", "The camera inspection, before any quote",
                        "The camera inspection, before any quote")])),
        sec("Should I repair the section or replace the whole line?",
            "One break in otherwise sound pipe is a spot repair. Multiple failures along the "
            "same run, or a lateral that is aged clay end to end, is a replacement, because "
            "fixing one joint in a line that is failing everywhere buys a season. The camera "
            "footage makes this an evidence question rather than an opinion.",
            sid="spot-or-full",
            table=tbl("When a sewer line is worth spot-repairing and when it should be "
                      "replaced.",
                      "If the camera shows the same failure repeating down the length of the "
                      "run, patching one spot buys a season. That is when we say replace.",
                      ["What we look at", "Spot repair when",
                       "Full replacement when"],
                      [("Number of defects", "One break or one root-intruded joint",
                        "Defects repeating along the whole run"),
                       ("Pipe material", "Sound PVC or newer pipe with local damage",
                        "Aged clay tile or corroded cast iron throughout"),
                       ("Backup history", "First failure in years",
                        "<a href=\"/plumbing/clogged-drain\">Repeat backups after "
                        "cleaning</a>, season after season"),
                       ("Grade", "Line runs true apart from the damaged spot",
                        "Multiple bellies holding standing water"),
                       ("Access", "Damage is reachable from one access point",
                        "Failures spread across the length of the lateral"),
                       ("Age of the house", "Newer construction with a localized issue",
                        "Pre-1940 stock with the original lateral in place"),
                       ("What the repair buys", "Years, on an otherwise good line",
                        "Another call next season")])),
        sec("What causes tree roots to get into a sewer line?",
            ["Roots follow moisture and enter at joints, not through sound pipe walls. Clay "
             "tile laterals with mortared joints, which is what most "
             "<a href=\"/locations/dayton\">pre-war Dayton homes</a> have, give them an "
             "opening every few feet. Once inside, roots grow in the nutrient-rich flow and "
             "build a mass that catches everything else moving through.",
             "So the repair that actually ends it is sealing or lining the joint they came "
             "through. Cutting the roots out just resets the clock."]),
    ],
    sectionsTail=[
        sec("How long does a sewer line repair take?",
            "A trenchless spot repair is often a single day once the diagnosis is done. A full "
            "excavated replacement depends on depth, length and what is on top of the line, "
            "and it takes longer if a driveway or a public right-of-way is involved. Permits "
            "and utility locates come before any digging."),
        sec("How do I get a sewer line quote?",
            call("Call {tel} or book a camera inspection online. The quote comes after the "
                 "footage, not before, and you watch the same screen the plumber does. Where "
                 "the pipe is sound and only loaded, "
                 "<a href=\"/plumbing/sewer-line/cleaning\">jetting</a> costs a fraction of a "
                 "repair. <a href=\"/financing-options\">Financing</a> is available on larger "
                 "sewer work.")),
    ],
    faqH2="What else do homeowners ask about sewer repair?",
    faq=qa(
        ("Can you fix my sewer line without tearing up the whole yard?",
         "In many cases, yes. Trenchless lining and pipe bursting repair a sewer lateral from "
         "small access points at each end, leaving the lawn between them intact. A collapsed "
         "or bellied line still requires excavation, and the camera inspection determines "
         "which applies before anything is quoted."),
        ("How long does a trenchless sewer repair last?",
         "A cured-in-place liner creates a jointless pipe inside the old one, which is what "
         "removes the root entry points that caused the failure. Manufacturers rate liners for "
         "decades of service."),
        ("What does a sewer camera inspection cost?",
         "Every sewer job is quoted flat and approved before work starts, including the "
         "inspection. The quote comes after the camera pass so the number is based on the "
         "pipe's actual condition rather than an estimate over the phone."),
        ("Can tree roots be killed instead of the pipe being repaired?",
         "Chemical root treatments and jetting clear a root mass and buy time, but the joint "
         "the roots came through is still open and they return. Where roots keep coming back "
         "to the same joint, sealing or lining that section is the repair that ends it."),
        ("Do I need a permit for sewer line work?",
         "Usually yes for excavation, plus a separate right-of-way permit if the work crosses "
         "a street or a tree lawn. We handle the permitting and the utility locates as part of "
         "the job."),
    ))

geo(PLUMB_FAMILIES, "sewer-line/cleaning.html",
    h1="Sewer line cleaning and hydro jetting in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="A snake makes a hole. A jetter cleans the pipe. They are not the same visit.",
    answer="Hydro jetting scours the full diameter of your pipe instead of boring a hole "
           "through the blockage, which is why it holds for years rather than months. A camera "
           "pass confirms the pipe can take it first.",
    callout="Snaking pokes a hole; jetting cleans the pipe. Call {tel} to break the backup "
            "cycle, or <a href=\"/plumbing/emergency-plumbing\">around the clock</a> if "
            "sewage is already indoors.",
    sections=[
        sec("Sewage is backing up in my basement. What do I do?",
            ["Stop running water anywhere in the house immediately, including the dishwasher "
             "and the washing machine, and keep everyone off the lowest-floor fixtures. Every "
             "gallon that goes down adds to what comes up. Then call. Sewage indoors is a "
             "health issue as well as a plumbing one and it gets dispatched around the clock.",
             "Someone answers at any hour for this one, and the plumber who turns up is "
             "working " + LICENCE_LINE + "."]),
        sec("What is hydro jetting and how is it different from snaking?",
            "A cable machine bores an opening through a blockage, which restores flow and "
            "leaves the buildup on the pipe wall. Hydro jetting pushes high-pressure water "
            "through a specialized nozzle that scours the full inside diameter, cutting root "
            "hair and stripping grease and scale. A cable restores flow, and a jetter restores "
            "the pipe.",
            table=tbl("Cable snaking and hydro jetting compared for main sewer lines.",
                      "If your main line has backed up more than once in a year, jetting is "
                      "what we will recommend. A cable restores flow; a jetter restores the "
                      "pipe.",
                      ["Factor", "Cable snaking", "Hydro jetting"],
                      [("What it removes", "An opening through the blockage",
                        "Roots, grease and scale from the full pipe wall"),
                       ("Result on the pipe wall", "Buildup remains",
                        "Pipe returned close to its original diameter"),
                       ("Best used for", "An emergency reopening to restore flow",
                        "Ending a cycle of repeat backups"),
                       ("Root intrusion", "Cuts what the head contacts",
                        "Cuts fine root hair the cable misses"),
                       ("Pipe condition required",
                        "Works in most pipe including fragile lines",
                        "Pipe must be sound, confirmed by camera first"),
                       ("How long results hold", "Months on a line with buildup",
                        "Years in most homes"),
                       ("Verification", "Flow test", "Camera pass after the cleaning")])),
        sec("How often should a sewer line be cleaned?",
            "Most homes never need scheduled cleaning. Homes with mature trees over a clay "
            "lateral, or <a href=\"/plumbing/clogged-drain\">a kitchen line carrying years of "
            "grease</a>, do better on a maintenance interval than on an emergency call. Where "
            "a line has been jetted once, the camera footage usually tells us whether it will "
            "need it again."),
        sec("Is hydro jetting safe for old pipes?",
            ["Not universally, which is why the camera goes in first. Thinned cast iron and "
             "cracked clay can be damaged by high-pressure water, and in those lines the "
             "honest recommendation is cleaning by cable and planning a repair. We say that "
             "before jetting rather than after, and the footage is there to back it up.",
             "That is the whole reason the "
             "<a href=\"/plumbing/sewer-line/overview\">camera</a> goes in first. High-pressure "
             "water belongs in a pipe someone has actually looked at."]),
    ],
    sectionsTail=[
        sec("Why does my basement floor drain back up when it rains?",
            "Heavy rain getting into a sanitary line usually means storm water is entering "
            "somewhere it should not: a cracked lateral, a downspout tied into the sanitary "
            "system, or a failed cleanout cap. Cleaning helps if the line is partly "
            "restricted, but the entry point is the actual problem and a camera finds it. "
            "<a href=\"/plumbing/sump-pump/repair\">A failed sump pump</a> produces the same "
            "wet basement from a different cause."),
        sec("How fast can you jet my line?",
            call("Most calls are handled the same day, and an active backup goes ahead of a "
                 "scheduled cleaning. Storms produce these calls in clusters within the same "
                 "afternoon, so calling earlier in the day gets you a better slot. Call "
                 "{tel}.")),
    ],
    faqH2="What else do homeowners ask about jetting?",
    faq=qa(
        ("Sewage is coming up in my basement floor drain. Who do I call?",
         call("Call a licensed plumber now, and stop using water in the house until one "
              "arrives. Someone answers at {tel} at any hour for this.")),
        ("How long does hydro jetting last?",
         "Years in most homes, because jetting removes the buildup instead of punching through "
         "it. Lines with continuing root intrusion or heavy grease loading do better on a "
         "maintenance schedule than on a wait-and-see basis."),
        ("Is hydro jetting safe for old pipes?",
         "It depends on the pipe, which is why a camera inspection comes first. Sound clay, "
         "cast iron and PVC all handle jetting. Thinned or cracked pipe does not, and in that "
         "case the recommendation is gentler cleaning and a repair plan."),
        ("Will cleaning fix a sewer line that keeps backing up?",
         "Only if the pipe is intact. Cleaning clears buildup, but it cannot fix a break, a "
         "belly, or an offset joint. If backups return after a proper jetting, "
         "<a href=\"/plumbing/sewer-line/repair\">the camera footage will show the structural "
         "cause</a>."),
        ("Can I use a store-bought drain product on a main line backup?",
         "No. Chemical products do not reach a main line blockage, they damage older pipe, and "
         "they make the line hazardous for the plumber who opens it. Mechanical cleaning is "
         "the only thing that works on a main."),
    ))

geo(PLUMB_FAMILIES, "sump-pump/repair.html",
    h1="Same-day sump pump repair in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Check the breaker and the float first. Then call, before the water reaches the "
          "floor.",
    answer="Stuck floats, failed switches, clogged intakes, dead check valves, burned-out "
           "motors. We fix all of it, usually the same day, and flood-test the pit through a "
           "full cycle before leaving. Storm-season calls are answered at any hour.",
    callout="A pump that's acting up will fail on the worst night. Call {tel} before the "
            "forecast turns.",
    sections=[
        sec("My sump pump is not turning on. What should I check first?",
            ["Two things, in this order. The breaker, because a pump that trips one is common "
             "and the reset is free. Then the float, because a float jammed against the pit "
             "wall or caught on the discharge pipe is the single most frequent cause of a pump "
             "that will not start. If both are fine, the switch or the motor has failed.",
             "We ask people to check those two before we dispatch, because often enough it "
             "saves them a service call entirely."]),
        sec("The pump runs but no water leaves the pit. Why?",
            "The impeller is clogged, the check valve has failed, or the discharge line is "
            "blocked or frozen. A pump that hums and moves nothing is doing the worst kind of "
            "work: burning its motor while the pit fills. Shut it off at the breaker if the "
            "pit is not rising fast, and call."),
        sec("Why does my sump pump run constantly?",
            "A stuck float leaves it on. A failed check valve lets the water it just pumped "
            "out drain straight back into the pit, so it pumps the same gallon repeatedly. An "
            "undersized pump or an undersized pit does the same thing for a different reason. "
            "All three are repairs and all three are diagnosable on one visit."),
    ],
    table=tbl("When a sump pump is worth repairing and when it should be replaced.",
              "Past about seven years, or with the motor itself gone, replacing beats "
              "repairing. The rest of the pump is the same age as the part that failed.",
              ["What we look at", "Repair when", "Replace when"],
              [("Age", "Under about 7 years", "Past 7 to 10 years, at or near end of life"),
               ("What failed", "Float, switch, check valve or a clogged intake",
                "Motor, impeller, or a seized shaft"),
               ("Failure history", "First problem the pump has had",
                "Second call on the same pump in a year"),
               ("Noise", "Normal running sound once the fault is fixed",
                "Grinding or a burning smell under load"),
               ("Basement finish", "Unfinished, low consequence if it fails again",
                "Finished, where a failure means real damage"),
               ("Backup protection", "Backup already installed and tested",
                "No backup, and <a href=\"/plumbing/sump-pump/installation\">replacement is "
                "the moment to add one</a>"),
               ("Pit and sizing", "Pit and pump correctly sized",
                "Pump cycling constantly because it is undersized")],
              h2="Should I repair or replace my sump pump?", sid="repair-or-replace",
              eyebrow="REPAIR OR REPLACE"),
    sectionsTail=[
        sec("How fast can someone get here when the pit is filling?",
            call("Most calls are handled the same day, and we "
                 "<a href=\"/plumbing/emergency-plumbing\">dispatch at any hour</a> on sump "
                 "pumps. Heavy rain brings these in clusters, so the earlier in a storm you "
                 "call {tel}, the better your slot. If water is already reaching the floor, "
                 "say so on the phone.")),
        sec("What should I do while I wait?",
            "Move anything that matters off the basement floor. If you have a wet-dry vac or a "
            "spare utility pump, start moving water. Do not stand in water near a running pump "
            "or any powered equipment, and if the water is approaching outlets or "
            "<a href=\"/furnace-repair\">a furnace</a>, kill the power to that area at the "
            "breaker. Water coming up through the floor drain rather than the pit is "
            "<a href=\"/plumbing/sewer-line/cleaning\">storm water entering the sanitary "
            "line</a>, which is a different job."),
    ],
    faqH2="What else do homeowners ask when a pump quits?",
    faq=qa(
        ("My sump pump quit and the pit is filling. How fast can you get here?",
         "Usually the same day, and we dispatch on pump failures at any hour. Heavy rain "
         "brings these calls in clusters, so calling early in a storm gets you a better "
         "slot."),
        ("Why is my sump pump not turning on?",
         "Check the breaker first, then the float. A tripped breaker and a float jammed "
         "against the pit wall or the discharge pipe account for most no-start calls, and both "
         "are free to check. If both are clear, the switch or the motor has failed."),
        ("Why does my sump pump make a loud noise?",
         "Grinding points at the motor or impeller, rattling usually means a loose discharge "
         "pipe or a failing check valve, and a hard bang when the pump shuts off is a check "
         "valve slamming. New noises are worth checking before the next heavy rain, not "
         "after."),
        ("Can a sump pump be repaired, or does it always get replaced?",
         "Floats, switches, check valves and clogged intakes are genuine repairs. Motor and "
         "impeller failures on a pump past seven years usually are not worth it, because the "
         "rest of the pump is the same age as the part that failed."),
        ("Should I test my own sump pump?",
         "Yes, every spring. Pour a five gallon bucket of water into the pit and confirm the "
         "float rises, the pump starts, the pit empties, and the pump shuts off cleanly. "
         "Anything that hesitates in that sequence is worth a service call before storm "
         "season."),
    ))

geo(PLUMB_FAMILIES, "sump-pump/installation.html",
    h1="Sump pump and battery backup installation in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="The week after a storm is when everyone calls. The week before is when it is cheap "
          "to fix.",
    answer="Primary pumps, battery backups and high-water alarms. We size against your pit, "
           "how high the discharge has to lift and how fast water comes in, rather than the "
           "horsepower on the box. An oversized pump short-cycles itself to death.",
    callout="The best time to upgrade is before the water table rises. Call {tel} for honest "
            "sizing.",
    sections=[
        sec("When is it time to replace a sump pump instead of repairing it?",
            "At about seven years, regardless of how it sounds. Also when the motor or "
            "impeller has failed, when the pump cycles constantly because it is undersized, "
            "when the basement is finished and the consequence of a failure has changed, or "
            "when there is no backup and the power goes out in storms. Where the fault is a "
            "float or a check valve, <a href=\"/plumbing/sump-pump/repair\">repairing it</a> "
            "is the cheaper call."),
        sec("What size sump pump do I need?",
            ["Not the biggest one on the shelf. Sizing works from three things: how much water "
             "the pit takes in during a real rain event, how high the discharge has to lift "
             "it, and how far it runs horizontally. An oversized pump short-cycles and wears "
             "out early. An undersized one loses the race.",
             "Those three numbers are what we work from, " + LICENCE_LINE + ". The horsepower "
             "on the label tells you almost nothing on its own."]),
        sec("What does a sump pump installation include?",
            ["The old pump comes out, the pit is cleaned of the silt and gravel that shortens "
             "pump life, the new pump is set with a new check valve and correctly routed "
             "discharge, a high-water alarm goes in, and the whole system is flood-tested "
             "through repeated full cycles before anyone leaves. Battery backups get tested on "
             "battery, not just on line power.",
             "That last bit matters. A backup that has only ever been tested plugged in has "
             "not been tested at all."]),
        sec("How does a battery backup sump pump work?",
            "A second pump sits above the primary in the same pit, wired to its own battery "
            "and charger. When the power fails or the primary cannot keep up, the backup "
            "starts on its own. Runtime depends on the battery and how often the pump has to "
            "cycle, which is why the battery is the part to check annually."),
    ],
    sectionsTail=[
        sec("Should I add a water alarm or a second pit?",
            "A high-water alarm is inexpensive and tells you a pump has stopped keeping up "
            "before the water reaches the floor. A second pit is a bigger conversation and "
            "belongs to homes with genuine inflow problems rather than pump problems. We will "
            "say which one you have. The "
            "<a href=\"/plumbing/sump-pump/overview\">sump pump services overview</a> covers "
            "the pump types side by side."),
        sec("Where does the discharge line go?",
            "Away from the foundation, and not into the sanitary sewer. Storm water dumped "
            "into a sanitary line is a common cause of "
            "<a href=\"/plumbing/sewer-line/cleaning\">basement backups during heavy rain</a> "
            "and it is prohibited in most local jurisdictions. Discharge routing is part of "
            "the install, including freeze protection on the exterior run."),
        sec("How long does the installation take?",
            call("A straight replacement in an existing pit is a few hours. Adding a battery "
                 "backup, replacing the discharge line or cutting a new pit takes longer. We "
                 "usually schedule within a day or two of the quote. Call {tel}, or see "
                 "<a href=\"/financing-options\">financing</a> on larger jobs. Every visit is "
                 "a <a href=\"/plumbing/services\">licensed Ohio plumber</a>.")),
    ],
    faqH2="What else do homeowners ask before installing a pump?",
    faq=qa(
        ("What does it cost to install a sump pump with a battery backup?",
         "Every installation is quoted flat and approved before work begins, after someone has "
         "seen the pit, the discharge run and the water table conditions. Those three "
         "variables change the answer enough that a number over the phone would not be "
         "honest."),
        ("How fast can you install a sump pump?",
         "Most get scheduled within a day or two of the quote. The week after a major storm is "
         "the exception, when every basement in the area calls at once."),
        ("Do I need a battery backup?",
         "If the basement is finished, or if your power goes out during storms, yes. Heavy "
         "rain events cause both the flooding and the outage, and a primary pump with no "
         "electricity does nothing at all."),
        ("How long do battery backups run during an outage?",
         "Runtime depends on the battery's capacity and how often the pump has to cycle, so a "
         "light rain outage lasts far longer than a downpour. Checking the battery once a year "
         "is the maintenance people skip and then regret."),
        ("Can you install a sump pump where there is no pit?",
         "Yes, though cutting a new pit into a concrete floor is a bigger job than replacing a "
         "pump in an existing one. It is worth doing where a basement has a genuine water "
         "problem, and worth talking through carefully before committing."),
    ))

geo(PLUMB_FAMILIES, "gas-line/repair.html",
    h1="Gas leak detection and gas line repair in {X}.",
    h1Highlight="Dayton &amp; Cincinnati",
    intro="If you smell gas, leave the building and call your gas utility from outside. Call "
          "us for the repair once the property is clear.",
    answer=["Smell gas right now? Leave the building and call your gas utility from outside. "
            "Come back to this page after. We locate and repair the leak once the property is "
            "clear, and every job ends with a documented pressure test."],
    callout="<b>If you smell gas right now:</b> get everyone out, including pets. Don't touch "
            "light switches, thermostats, garage door openers or appliance controls. Don't "
            "unplug anything or use a phone indoors. From outside and well away, call your gas "
            "utility's 24-hour emergency line, and once they have made the property safe, call "
            "{tel} for the repair. In the Dayton metro the gas utility is CenterPoint Energy "
            "Ohio; in the Cincinnati metro it is Duke Energy Ohio.",
    sections=[
        sec("What does a gas leak smell like?",
            ["Natural gas has no odor of its own. Utilities add mercaptan, which smells like "
             "rotten eggs or sulfur, precisely so a leak is detectable. If you smell that "
             "anywhere in or around the house, treat it as real. A faint smell near one "
             "appliance and a strong smell through a whole house are the same instruction: "
             "leave, then call.",
             "The smell is the safety system working. It is there so you get out, not so you "
             "can judge how bad it is from the hallway."]),
        sec("What are the signs of a gas leak besides the smell?",
            "Hissing near a line or appliance. A patch of dead or dying grass in a line over a "
            "buried gas line, with healthy lawn either side. "
            "<a href=\"/plumbing/water-heater/repair\">Pilot lights that will not stay lit</a>. "
            "A gas bill climbing with no change in usage. Headaches, dizziness or nausea that "
            "improve when people leave the house."),
        sec("Should I call the gas company or a plumber first?",
            ["The gas utility, always, and from outside the building. The utility's job is to "
             "make the property safe, shut off supply at the meter if needed, and confirm the "
             "area is clear. A licensed plumber's job is to locate and repair the line "
             "afterward. They are two different calls and the order is not interchangeable.",
             "Utility first, plumber second. Every time, no exceptions, even if you are "
             "certain you know where the leak is."]),
        sec("How is a gas leak located and repaired?",
            "Electronic gas detection equipment narrows the location, then the affected "
            "section is isolated and pressure-tested to confirm it. Buried lines are traced "
            "before anyone digs. The repair is made, the section is brought back up to "
            "pressure and held, and the result is documented before the gas is restored."),
    ],
    sectionsTail=[
        sec("Can I use my other gas appliances until the line is fixed?",
            "Not until the system has been tested and confirmed safe. A leak on one branch "
            "does not stay on one branch once supply is restored, and \"it seems fine\" is not "
            "a test. After the repair we tell you exactly what is usable and when, on the "
            "basis of the pressure test rather than an opinion."),
        sec("Why do old gas lines fail?",
            "Corrosion on buried steel, threaded joints that have loosened over decades of "
            "thermal cycling, and lines that were sized for a smaller appliance load than the "
            "house now carries. A line that has been repaired more than once is usually "
            "telling you that <a href=\"/plumbing/gas-line/installation\">a new run</a> is the "
            "cheaper answer."),
        sec("How quickly can someone come out?",
            call("Gas calls are answered at any hour and go ahead of routine work, on {tel}, "
                 "alongside <a href=\"/plumbing/emergency-plumbing\">emergency plumbing</a>. "
                 "That said, the utility call comes first and it comes from outside the "
                 "building, every time. Licensing and permits are covered on the "
                 "<a href=\"/plumbing/gas-line/overview\">gas line overview</a>.")),
    ],
    faqH2="What else do people ask about gas leaks?",
    faq=qa(
        ("I smell gas. What do I do right now?",
         "Leave the building immediately with everyone in it. Do not touch light switches, "
         "unplug anything, or use a phone indoors. From outside and well away, call your gas "
         "utility's emergency line. Call a licensed plumber for the repair only after the "
         "utility has cleared the property."),
        ("Do I call the gas company or a plumber?",
         "The gas utility first, from outside the building. The utility makes the property "
         "safe and shuts off supply if it needs to. A licensed plumber locates and repairs the "
         "line afterward. In the Dayton metro the gas utility is CenterPoint Energy Ohio; in "
         "the Cincinnati metro it is Duke Energy Ohio."),
        ("How do you find a gas leak?",
         "Electronic detection equipment narrows the location, and a pressure test on the "
         "isolated section confirms it. Buried lines are traced before any digging. The result "
         "is measured and documented, not judged by smell."),
        ("What documentation do I get after a gas repair?",
         "A pressure test record for the isolated section, plus the electronic leak check "
         "result. That is what an inspection or a future buyer asks for, and it is produced on "
         "every gas job."),
        ("Can a small gas leak wait until morning?",
         "No. Any detectable gas smell is a leave-now situation, at any hour. Gas calls are "
         "taken around the clock for exactly that reason."),
    ))

geo(PLUMB_FAMILIES, "gas-line/installation.html",
    h1="New gas line installation in {X}.", h1Highlight="Dayton &amp; Cincinnati",
    intro="Call before the patio is poured, not after. Moving a line later costs more than "
          "running it now.",
    answer="New runs for ranges, dryers, grills, fire pits, pool heaters, garage heaters and "
           "standby generators. Each one is sized to everything sharing that line, permitted "
           "where required, and pressure-tested before you use it.",
    callout="Planning a project? Call {tel} early. A right-sized line saves headaches later.",
    sections=[
        sec("Can you run a gas line to my grill?",
            "Yes, and it is one of the more common requests between April and August. An "
            "outdoor line is trenched or routed to the grill location, sized to the appliance, "
            "fitted with a shutoff and a quick-connect at the end, and pressure-tested. You "
            "stop hauling propane tanks to the hardware store."),
        sec("What appliances can a gas line be run for?",
            "Ranges and cooktops, clothes dryers, outdoor grills, fire pits, pool and spa "
            "heaters, garage and workshop heaters, standby generators, "
            "<a href=\"/plumbing/water-heater/installation\">tankless water heaters</a> and "
            "gas fireplace logs. The list matters less than the load: what each one demands "
            "determines how the pipe is sized.",
            sid="projects",
            table=tbl("Common residential gas line projects and what each one involves.",
                      "We size against everything sharing the line, not just the appliance you "
                      "are adding. That is the difference between a line that works and one "
                      "that starves.",
                      ["Project", "What it usually involves", "Permit typically required"],
                      [("Range or cooktop conversion",
                        "New branch from the nearest adequate line, shutoff at the appliance",
                        "Yes"),
                       ("Electric to gas dryer",
                        "New branch and shutoff, plus dryer venting check", "Yes"),
                       ("Outdoor grill or fire pit",
                        "Exterior run, buried or routed, with a quick-connect", "Yes"),
                       ("Pool or spa heater",
                        "Higher-demand run, often requiring an upsized line", "Yes"),
                       ("Garage or shop heater",
                        "Run to an unconditioned space, with clearances checked", "Yes"),
                       ("Standby generator",
                        "High-demand run, coordinated with the electrical install", "Yes"),
                       ("Tankless water heater",
                        "Usually an upsized line plus new venting", "Yes")])),
        sec("Why does the size of the gas line matter?",
            ["Because every appliance on a line shares the supply. A pipe sized for a range "
             "will starve a range and a generator running together, which shows up as low "
             "burner output, a generator that will not hold load, or an appliance that short "
             "cycles. Sizing is a calculation across everything on the run, done before the "
             "trench.",
             "We add up the BTU demand of every appliance on the line first, so that running "
             "two of them at once does not starve either."]),
        sec("Do I need a permit?",
            ["For most new gas piping, yes, and who issues it depends on where you are. Greene "
             "County permits <a href=\"/locations/beavercreek\">Beavercreek</a> while Fairborn "
             "and Xenia next door issue their own, and the City of Dayton runs its own "
             "plumbing inspection.",
             "We pull it and close out the inspection either way, so which side of a township "
             "line your house sits on is not your problem to work out."]),
    ],
    sectionsTail=[
        sec("Can you convert my range or dryer from electric to gas?",
            "Yes, provided the house has gas service and the existing line has capacity. The "
            "job is a new branch, a shutoff at the appliance, the connection, and "
            "<a href=\"/plumbing/gas-line/repair\">a pressure test</a> before first use. On a "
            "dryer conversion the venting gets checked at the same time, because gas dryers "
            "vent differently than electric."),
        sec("What does a gas line installation include?",
            call("Load calculation across the appliances on the run, permit application, "
                 "utility locates before any digging, pipe sized and installed to code, a "
                 "shutoff at every appliance, a pressure test on the completed run, the "
                 "inspection scheduled and closed out, and documentation of the test result "
                 "for your records. Most residential runs are a single day of work once the "
                 "permit is issued and the locates are marked. Call {tel}, see the "
                 "<a href=\"/plumbing/gas-line/overview\">gas line services overview</a>, or "
                 "check <a href=\"/financing-options\">financing</a> on larger projects.")),
    ],
    faqH2="What else do homeowners ask about new gas lines?",
    faq=qa(
        ("How much does it cost to run a gas line to a grill?",
         "Every gas line project is quoted flat and approved before work starts, after someone "
         "has seen the run, the distance and what the ground between looks like. Distance and "
         "access change the answer enough that a phone estimate would not be reliable."),
        ("Do I need a permit for a gas line?",
         "For most new gas piping, yes, and who issues it changes from one town to the next "
         "around here. Greene County permits Beavercreek, several neighboring communities "
         "issue their own, and the City of Dayton runs its own plumbing inspection. We pull it "
         "and close it out."),
        ("Can you run a gas line to a detached garage?",
         "Yes. It is a buried exterior run with utility locates first, sized to whatever is "
         "going in the garage, with a shutoff at the appliance and a pressure test on the "
         "completed line."),
        ("How long does a gas line installation take?",
         "Most residential runs are a single day of work once the permit is issued and the "
         "utility locates are marked. Locates are a required waiting period before any "
         "excavation and they cannot be skipped."),
        ("Will adding an appliance overload my existing gas line?",
         "It can, which is why load is calculated across everything on the run before anything "
         "is added. A line sized for one appliance will underperform when two draw at once, "
         "and that shows up as weak burners or a generator that will not hold."),
    ))


# ============================================================================
# Cost-intent sections on the installation pages
# ============================================================================
# "How much does a new furnace cost" is the highest-intent question in the trade
# and the one this site has never answered anywhere. It is also the question the
# blind reader review's price-shopper persona left over.
#
# We do not publish installed prices, and after checking, neither does the largest
# competitor in this market: two of geteco.com's cost pages, ~3,200 words each with
# "Cost" in the H1 and the URL, contain zero dollar figures between them (verified
# 2026-08-02 against the Wayback copies, their live edge now blocks us). Their 120
# cost URLs are a keyword play, not a disclosure. So the ranking value is in the
# page answering the question in the shape it gets asked, not in a number.
#
# What goes here is therefore drivers, not dollars: the things that actually move a
# quote, each one already established elsewhere on this site, plus how to get a real
# number. Every row below traces to approved copy on the page it sits on.
#
# [NEEDS: a financing payment example. /financing-options names GoodLeap, Synchrony
#  and Wright-Patt but publishes no APR, no term and no example payment, so one
#  cannot be written without inventing lender terms. A single "from $X/month on
#  approved credit" is a number a customer can act on and the only concrete figure
#  a competitor here publishes anything like.]
#
# All three pages already answer "what does the installation include", in more detail
# than anything added here would, so the cost block links the reader to that answer
# rather than restating it a second time on the same page.

_COST_H2 = "How much does {thing} cost in Dayton or Cincinnati?"

_COST_LEAD = (
    "There is no honest single number, and anyone who gives you one over the phone is "
    "guessing at your house. {lead} What we can do is tell you exactly what moves the "
    "figure, so the quote you get makes sense instead of arriving as a surprise.")

def _cost_section(thing, lead, rows, includes, anchor):  # includes: kept for the lead
    """A cost-intent block: the question in the shape it gets asked, an honest answer,
    the drivers in a table, and what the number covers."""
    return [
        {"eyebrow": "WHAT IT COSTS",
         "id": anchor,
         "h2": _COST_H2.format(thing=thing),
         "body": _COST_LEAD.format(lead=lead),
         "table": {
             "eyebrow": "PRICE DRIVERS",
             "caption": f"What moves the price of {thing}.",
             "takeaway": ("Sizing and ductwork move the number more than the badge on the "
                          "equipment does, and both are decided at the survey rather than "
                          "over the phone."),
             "columns": ["What we look at", "Which way it moves the price",
                         "How you can tell before we arrive"],
             "rows": rows,
         }},
    ]

_FURNACE_COST = _cost_section(
    "a new furnace",
    "A furnace swap in a house with sound ductwork and a 96% unit already vented is a "
    "different job from one that needs a new flue, a gas line reworked and a return "
    "added, and those two land nowhere near each other.",
    [
        ("Size, from a load calculation",
         "Both ways. Right-sizing sometimes lands smaller and cheaper than what is there",
         "If a room has never been warm, the old unit was probably sized off the label"),
        ("Efficiency tier",
         "Up front, down on the gas bill. 96% AFUE and above costs more to install",
         "A 96% unit vents in PVC out a side wall, an 80% goes up the chimney"),
        ("Venting and condensate",
         "Up, if you move from 80% to 96% and the flue and drain have to be rerun",
         "Going high-efficiency for the first time means new venting, every time"),
        ("Ductwork and return capacity",
         "Up, when the returns cannot move what the new furnace needs",
         "Rooms that never keep up, or a filter that whistles, both point at returns"),
        ("Gas and electrical",
         "Up, if the line or the circuit has to be reworked to code",
         "Older houses more often than newer ones. We check it on the survey"),
        ("Permit and inspection",
         "A fixed local cost, and it varies by town more than people expect",
         "We pull it and close it out either way. Never optional, never skipped"),
    ],
    "The furnace, the gas connection, the venting and the electrical, all code-compliant "
    "and commissioned before we leave, plus the permit and the inspection, and your old "
    "unit removed and taken away. You agree the price before any of it starts.",
    "furnace-cost")

_AC_COST = _cost_section(
    "a new air conditioner",
    "A straight condenser and coil swap on sound ductwork is a different job from one "
    "that needs a new line set, a new pad and a circuit run, and the gap between them is "
    "wide.",
    [
        ("Size, from a heat gain calculation",
         "Both ways. Matching the tonnage on the old label repeats the last mistake",
         "An oversized unit cools fast and leaves the house clammy"),
        ("Efficiency tier",
         "Up front, down on the summer bill",
         "Worth pricing both when you plan to stay in the house a while"),
        ("Ductwork and return capacity",
         "Up, and it is the most common reason a new system underperforms",
         "A larger system on an undersized return will disappoint you either way"),
        ("Line set, pad and disconnect",
         "Up, when the existing ones cannot be reused",
         "A line set that has carried R-22 usually cannot stay for a new refrigerant"),
        ("R-22 in the old system",
         "Up, because none of it carries over and the whole system is replaced",
         "R-22 has not been produced or imported in the US since 2020"),
        ("Permit and inspection",
         "A fixed local cost that changes from town to town",
         "We pull it and close it out. Never optional"),
    ],
    "The outdoor condenser, the indoor evaporator coil, the line set connection, the "
    "electrical whip and disconnect, and the refrigerant charge, with your old equipment "
    "removed and taken away. Permit and inspection included. You agree the price first.",
    "ac-cost")

_HP_COST = _cost_section(
    "a heat pump",
    "A heat pump replacing an air conditioner on an existing furnace is a different job "
    "from a full dual-fuel conversion with new controls, and the electrical is the part "
    "people do not see coming.",
    [
        ("Size, and the balance point",
         "Both ways. Sizing for an Ohio winter is not the same as sizing for July",
         "The balance point is where the backup takes over. It gets set, not guessed"),
        ("Dual-fuel or straight electric backup",
         "Dual-fuel costs more to set up and less to run when it is properly cold",
         "If you already have gas, dual-fuel is usually the cheaper system to live with"),
        ("Electrical service and circuit",
         "Up, and this is the one that surprises people on older panels",
         "A 60 or 100 amp panel is the thing to check before you fall for a quote"),
        ("Ductwork and return capacity",
         "Up. A heat pump moves more air for longer than a furnace does",
         "Ducts that were marginal on a furnace will be worse on a heat pump"),
        ("Controls and thermostat",
         "Up modestly. Dual-fuel needs a thermostat that can stage the two",
         "Your existing thermostat may not be able to run the system you are buying"),
        ("Permit and inspection",
         "A fixed local cost, varying by town",
         "We pull it and close it out. Never optional"),
    ],
    "The heat pump, the indoor coil or air handler, the line set connection, the "
    "electrical, and the controls set up for how the system actually runs here, with the "
    "old equipment removed. Permit and inspection included, price agreed before we start.",
    "heat-pump-cost")

for _key, _cost in (("furnace-installation.html", _FURNACE_COST),
                    ("ac-installation.html", _AC_COST),
                    ("heat-pump-installation.html", _HP_COST)):
    _d = HVAC_SUBS.get(_key)
    if not _d:
        continue
    # Ahead of the booking and financing questions, which is the order someone reads
    # in: what does it cost, what does that cover, then how do I pay for it.
    _d["sectionsTail"] = list(_cost) + list(_d.get("sectionsTail", []))
