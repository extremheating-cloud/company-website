from pages.services.shared import call, steps, detail, sub, pillset, SPEED_FAQ, geo, sec, tbl, qa, COST_ROW

WH_PILLS = [("Overview", "/plumbing/water-heater/overview"), ("Repair", "/plumbing/water-heater/repair"), ("Installation", "/plumbing/water-heater/installation")]
SEW_PILLS = [("Overview", "/plumbing/sewer-line/overview"), ("Repair", "/plumbing/sewer-line/repair"), ("Cleaning", "/plumbing/sewer-line/cleaning")]
SUMP_PILLS = [("Overview", "/plumbing/sump-pump/overview"), ("Repair", "/plumbing/sump-pump/repair"), ("Installation", "/plumbing/sump-pump/installation")]
GAS_PILLS = [("Overview", "/plumbing/gas-line/overview"), ("Repair", "/plumbing/gas-line/repair"), ("Installation", "/plumbing/gas-line/installation")]

PLUMB_CRUMB = ("Plumbing", "/plumbing/services")

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
