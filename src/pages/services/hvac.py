"""Step-5 rollout — remaining pages as data objects (README copy formulas)."""
from layout import components as T
from data import business as D
from pages.services.shared import call, steps, detail, sub, pillset, SPEED_FAQ, geo, sec, tbl, qa, COST_ROW

FURN_PILLS = [("Overview", "/furnace-heating"), ("Installation", "/furnace-installation"), ("Repair", "/furnace-repair")]
AC_PILLS = [("Overview", "/air-conditioning"), ("Installation", "/ac-installation"), ("Repair", "/ac-repair")]
HP_PILLS = [("Overview", "/heat-pump"), ("Installation", "/heat-pump-installation"), ("Repair", "/heat-pump-repair")]
IAQ_PILLS = [("Overview", "/indoor-air-quality"), ("Solutions", "/indoor-air-quality-solutions"),
             ("Importance", "/importance-iaq"), ("FAQ", "/iaq-faq")]

HVAC_CRUMB = ("Heating & Air", "/services")

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
                        "Parts and labor warranties have both run out")])),
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
             "cleaning when there is visible mold growth, vermin, or enough dust and debris "
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
            ["In this order: control the source, then filter, then purify. Sealing a moldy "
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
                       ("Visible mold near a register or crawlspace",
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
# The sub-page hero chips come from components.SUB_CHIPS, not from this file,
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
                       ("Mold and mildew spores",
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
