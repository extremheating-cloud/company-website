"""Per-city content angles for the city x service pages.

WHY THIS EXISTS

Measured 2026-08-03, six-word-shingle Jaccard over visible <main> text:

    city x service pages   9.6% median unique text, 0.51-0.58 Jaccard
                           WITHIN a service family (all 39 heating pages
                           are 56% identical to each other)
    city overview pages   22.0% median unique

Every competitor audited beats that: Eco Plumbers 58-66%, McAfee 47.5%,
Butler 43-52%, Five Star 35.9%. It is the heaviest-weighted category in the
scoring and the one place we are last.

THE MECHANISM, COPIED FROM ECO PLUMBERS

Their Brookville and Montgomery AC pages score Jaccard 0.229. They do not do
per-city research to get there. They keep a library of substantive angles and
give each city a DIFFERENT SUBSET of them, so no two pages carry the same set:

    Brookville: warning signs / smart upgrades / cost of waiting / trust
    Montgomery: what the AC is telling you / when the fix is worth it /
                zoning systems / resale value

Same trade, different five sections. That is the whole trick, and it is worth
being honest about what it is: rotation raises uniqueness without making a page
more *local*. A Montgomery reader gets zoning and a Brookville reader gets cost
of waiting for no reason connected to their town.

So the rule here is that every angle must be independently worth reading. If a
section only exists to make a page look different from its neighbour, it is
padding, and padding on 234 pages is how a site earns a thin-content problem
instead of solving one. Each angle below answers a question a homeowner in this
market actually asks, and would earn its place on a single page with no
neighbours at all.

The genuinely local layer sits ELSEWHERE and stays there: LOCAL[slug]["svc"]
carries the researched permit, water and utility facts for the indexed ten, and
those still render first. This is the layer underneath, for the other twenty
cities and for depth on the ten.

[NEEDS: a Census API key (free, api.census.gov/data/key_signup.html). ACS table
 B25034, year structure built, keyed by place, would let each city's angle set
 be chosen by its actual housing stock rather than by hash - a 1950s Kettering
 ranch and a 2003 Springboro subdivision genuinely need different questions
 answered. That turns rotation into relevance. The API stopped serving keyless
 requests, so it is one free signup away.]
"""
import hashlib


def pick(slug, service, n=4):
    """A deterministic, stable subset of angles for one city and service.

    Ordering is by SHA1 of (slug, service, angle id) rather than random.shuffle:
    the same city gets the same sections on every build, so a rebuild never
    rewrites 234 pages and never churns the sitemap lastmod dates. Python's
    built-in hash() is salted per process and would do exactly that.
    """
    pool = ANGLES.get(service) or []
    if not pool:
        return []
    keyed = sorted(
        pool,
        key=lambda a: hashlib.sha1(
            f"{slug}|{service}|{a['id']}".encode()).hexdigest())
    # Ranking the whole pool and taking the top n is not a uniform draw over
    # combinations, and with 30 cities against 16 angles it collided once for real:
    # moraine and springfield drew an identical four for heating. The rotating start
    # point breaks that. It is still a pure function of (slug, service) — no dependence
    # on the city list, so adding a town later cannot reshuffle an existing one — and
    # two cities now have to match on both the ranking and the offset.
    start = int(hashlib.sha1(f"{slug}|{service}|offset".encode()).hexdigest(), 16)
    start %= len(keyed)
    return [keyed[(start + i) % len(keyed)] for i in range(min(n, len(keyed)))]


def coverage(slugs, service, n=4):
    """How evenly the pool is used, and whether any two cities got the same set.

    Called by the build's own check rather than trusted: an uneven pool means
    some sections render on thirty pages and others on two, which is the failure
    mode that turns rotation back into duplication.
    """
    sets = {s: tuple(a["id"] for a in pick(s, service, n)) for s in slugs}
    counts = {}
    for ids in sets.values():
        for i in ids:
            counts[i] = counts.get(i, 0) + 1
    dupes = len(sets.values()) - len(set(sets.values()))
    return counts, dupes


# ---------------------------------------------------------------------------
# The library.
#
# Every entry: an id that never changes (it seeds the ordering, so renaming one
# reshuffles that city's page), an h2 that may carry {C} for the city, and body
# copy in the site voice - second person, no self-naming, no dashes standing in
# for punctuation, a fact rather than an adjective wherever one exists.
#
# Sizing: pools of 10 give 210 distinct four-section combinations, which is
# comfortably more than the 39 cities and leaves room to add cities later.
# ---------------------------------------------------------------------------

ANGLES = {
    "heating": [
        {"id": "hx-crack",
         "h2": "How do I know if the heat exchanger is cracked?",
         "body": (
             "You mostly do not, which is why it gets checked rather than guessed at. "
             "A cracked heat exchanger can put combustion gas into the air you breathe "
             "while the furnace still appears to run normally. The signs worth calling "
             "about are a burner flame that flickers or turns yellow when the blower "
             "kicks on, soot around the burner compartment, and a carbon monoxide alarm "
             "that trips even once. A furnace with a confirmed crack gets shut off and "
             "red-tagged the same visit. That is not an upsell, it is the only legal "
             "answer, and any company that offers to keep running it is telling you "
             "something about how they work.")},

        {"id": "hx-shortcycle",
         "h2": "Why does my furnace turn on and off every few minutes?",
         "body": (
             "Short cycling. The furnace reaches its limit, shuts down, cools, and "
             "starts again, which burns more gas than running a full cycle would and "
             "wears the ignition components out early. The usual causes are a clogged "
             "filter starving the return, a flame sensor that needs cleaning, an "
             "oversized furnace that heats the thermostat faster than it heats the "
             "house, or a flue problem tripping the safety. The first is free to rule "
             "out yourself. If a new filter does not settle it within a day, the rest "
             "want a technician, because two of them are safety devices doing their job.")},

        {"id": "hx-cold-rooms",
         "h2": "One room never gets warm. Is the furnace the problem?",
         "body": (
             "Usually not. A furnace that satisfies the thermostat is doing what it was "
             "asked, and the room that stays cold is almost always a duct problem: a "
             "run that is too long or too small, a damper closed years ago and "
             "forgotten, a crushed flex duct in a joist bay, or a return that cannot "
             "pull enough air back for the supply to push. Adding return capacity fixes "
             "more of these houses than replacing the furnace does, and it costs a "
             "fraction of what a new system does. Ask for the airflow to be measured "
             "before anyone quotes you equipment.")},

        {"id": "hx-afue",
         "h2": "Is a 96% furnace worth the extra money over an 80%?",
         "body": (
             "It depends on what the swap actually involves, not on the badge. Going "
             "from 80% to 96% means the flue changes: a condensing furnace vents in PVC "
             "out a side wall and produces condensate that needs a drain, so the job "
             "grows beyond the equipment. In a house that already has a condensing "
             "furnace, the upgrade is straightforward and the gas saving is real. In a "
             "house venting up a masonry chimney shared with a water heater, taking the "
             "furnace off that chimney can leave the water heater venting badly, and "
             "that has to be solved as part of the same job.")},

        {"id": "hx-thermostat",
         "h2": "Will a smart thermostat actually cut my gas bill?",
         "body": (
             "Some, and less than the box claims. The saving comes from setbacks you "
             "would not have bothered with, not from the thermostat being clever. The "
             "bigger reason to care is what it tells you: run times, cycle counts and "
             "how long the house takes to recover. A furnace that used to run twelve "
             "minutes and now runs twenty-five is telling you something months before "
             "it fails. One caution for older systems, a two-stage or variable-speed "
             "furnace wired to a thermostat that cannot stage it will run on high heat "
             "permanently, which is worse than the thermostat you replaced.")},

        {"id": "hx-age",
         "h2": "My furnace is 18 years old and still works. Do I replace it?",
         "body": (
             "Not on age alone. Age changes the maths on the next repair rather than "
             "forcing a decision today. Once a furnace is past about fifteen years, the "
             "test is what a repair costs against what it buys you: a $200 fix on a "
             "system with five years left is money well spent, and the same $200 on one "
             "with a failing heat exchanger is not. What is worth doing before winter "
             "on a furnace that old is a real safety inspection, so a decision in "
             "January gets made with information rather than in a cold house at 9pm.")},

        {"id": "hx-filter",
         "h2": "How often should I actually change the filter?",
         "body": (
             "A one-inch filter every one to three months, sooner with pets or during "
             "any kind of remodel. A four or five-inch media filter every six to twelve "
             "months. The reliable test is holding it up to a light: if the light does "
             "not come through, it is restricting the return whatever the calendar says. "
             "The mistake worth avoiding is buying the densest filter on the shelf. A "
             "high-MERV filter in a system not designed for it starves the blower, and "
             "a starved blower on a furnace is how a heat exchanger cracks early.")},

        {"id": "hx-noheat-night",
         "h2": "The heat is out and it is the middle of the night. What now?",
         "body": (
             "Check three things before you call, because one of them fixes it more "
             "often than people expect. The furnace switch, which looks like a light "
             "switch on or near the unit and gets knocked off. The breaker. And the "
             "filter, if it has been in longer than you can remember. If none of those "
             "does it, call. The line is answered at any hour, and a house losing heat "
             "in an Ohio January is not a call worth putting off until morning, both "
             "for the house and for the pipes in it.")},

        # This slot used to answer "do you still work on boilers and radiators" with a
        # yes. We do not work on boilers or geothermal, client-corrected 2026-08-03. Oil
        # furnaces we do, and nothing on the site said so, so the honest version of this
        # angle is more useful than the wrong one was.
        {"id": "hx-oil",
         "h2": "Do you work on oil furnaces?",
         "body": (
             "Yes. There are fewer around than there once were, but plenty are still "
             "running in the older housing here, and they are a genuinely different "
             "service call from gas: a nozzle and electrodes rather than a burner "
             "assembly, a filter and a pump on the fuel side, and soot that has to be "
             "cleaned out rather than left. They want annual service more than a gas "
             "furnace does, because a neglected oil burner sooties up and loses "
             "efficiency long before it stops working. What we do not take on is "
             "boilers or geothermal, so if your heat is hydronic you want a hydronic "
             "specialist rather than us.")},

        {"id": "hx-two-systems",
         "h2": "Should the furnace and the air conditioner be replaced together?",
         "body": (
             "Not automatically, but there is a real reason it comes up. The indoor coil "
             "sits in the furnace cabinet and the two are matched as a system, so "
             "replacing one and keeping the other can leave you with a pairing that does "
             "not hit the efficiency either part was rated for. If both are near end of "
             "life, doing them together costs less than two separate jobs because it is "
             "one visit and one set of connections. If the air conditioner is eight "
             "years old and healthy, keep it and say so to anyone who tells you "
             "otherwise.")},
    ],

    "cooling": [
        {"id": "cx-warm-air",
         "h2": "The AC runs but the air is not cold. What causes that?",
         "body": (
             "Four things, in the order they turn up. A filter or coil blocked enough to "
             "starve airflow, which is the cheapest and most common. A failed capacitor, "
             "where the outdoor fan spins but the compressor does not. Low refrigerant, "
             "which is always a leak rather than something that gets used up. Or a "
             "frozen indoor coil, which looks like an airflow problem and often is one. "
             "Turning the system to fan-only for an hour to thaw a frozen coil before "
             "anyone arrives will not fix it, but it does let a technician find the "
             "actual cause instead of a block of ice.")},

        {"id": "cx-sizing",
         "h2": "Is a bigger air conditioner better?",
         "body": (
             "No, and this is the most expensive misunderstanding in the trade. An "
             "oversized unit cools the thermostat quickly, shuts off, and never runs "
             "long enough to pull moisture out of the air. The house hits the number and "
             "still feels clammy, which is the complaint that follows a great many new "
             "installations. Correct size comes from a heat gain calculation on your "
             "specific house: square footage, insulation, window area and orientation, "
             "ceiling height and duct condition. Matching the tonnage on the old label "
             "just repeats whatever mistake was made last time.")},

        {"id": "cx-r22",
         "h2": "My system uses R-22. Is it worth recharging?",
         "body": (
             "Usually not. R-22 has not been produced or imported in the United States "
             "since 2020, so what is left is reclaimed stock at a price that climbs every "
             "season. More to the point, refrigerant is not consumed. A system that is "
             "low has a leak, and paying for a recharge without finding the leak buys "
             "you the same conversation next summer at a higher price. On an R-22 system "
             "at fifteen-plus years, that money is usually better put against the "
             "replacement you are going to make anyway.")},

        {"id": "cx-humidity",
         "h2": "Why is the house humid even when the AC is running?",
         "body": (
             "Because cooling and dehumidifying are two different jobs and a system can "
             "do one without the other. Air conditioning pulls moisture out only while "
             "the coil is cold and air is moving across it for a sustained period. Short "
             "cycles from an oversized unit, a blower set too fast, or a thermostat set "
             "so the system barely runs will all leave you cool and damp. In a tighter "
             "newer house it can also be that there is simply more moisture indoors than "
             "the system was sized to remove, which is a dehumidification question rather "
             "than an air conditioning one.")},

        {"id": "cx-outdoor-unit",
         "h2": "How much clearance does the outdoor unit actually need?",
         "body": (
             "About two feet on all sides and five feet of clear space above, and it "
             "matters more than it looks. The condenser rejects heat into the air around "
             "it, so a unit boxed in by a fence, a deck or shrubs that have grown in over "
             "a few summers is re-breathing its own hot air and working harder for less "
             "cooling. Rinsing the coil with a garden hose from the inside out once a "
             "season, with the power off, is the one piece of maintenance a homeowner can "
             "genuinely do without risk.")},

        {"id": "cx-two-story",
         "h2": "Upstairs is hot and downstairs is cold. Do I need a second system?",
         "body": (
             "Not always, and it is worth exhausting the cheaper answers first. Heat "
             "rises, so a two-story house on one system fights that all summer. Before "
             "anyone quotes a second system, the questions are whether the upstairs "
             "returns can move enough air, whether the supply runs to the far bedrooms "
             "are the right size, and whether the ductwork can be zoned. Zoning an "
             "existing system solves a good share of these houses for a fraction of what "
             "a second system costs. If the ducts genuinely cannot support it, that is "
             "when the second system conversation is honest.")},

        {"id": "cx-seer",
         "h2": "Does a higher SEER2 rating pay for itself?",
         "body": (
             "It depends how long you are staying and how much you actually run it. In "
             "this climate the cooling season is real but not year-round, so the payback "
             "period on the top efficiency tier is longer than the brochure maths "
             "suggests. The tier worth paying for is usually the one that also brings a "
             "two-stage or variable-speed compressor, because that changes comfort as "
             "well as the bill: longer, gentler run times hold humidity down and even out "
             "the temperature between rooms in a way a single-stage unit cannot.")},

        {"id": "cx-noise",
         "h2": "The outdoor unit is making a noise it did not make before.",
         "body": (
             "The noise usually names the part. A hard electrical hum with the fan not "
             "turning points at a capacitor. A metallic screech on startup points at the "
             "compressor. A rattle that changes with fan speed is often a loose panel or "
             "debris in the cabinet, which is the one worth checking yourself with the "
             "power off. A hiss or a bubbling is refrigerant. What they have in common is "
             "that none of them improves on its own, and a capacitor caught early is a "
             "small repair while a compressor is a system decision.")},

        {"id": "cx-maintenance-timing",
         "h2": "When should the AC be serviced, and does it matter?",
         "body": (
             "Spring, before the first stretch of real heat, and the timing matters more "
             "than the visit does. Everyone discovers their air conditioner is broken in "
             "the same week, which is the week nobody has availability. A tune-up ahead "
             "of that finds the weak capacitor and the dirty coil while it is a "
             "scheduled visit rather than an emergency one. It also gives you a "
             "measurement to compare against next year, which is how a slow refrigerant "
             "leak gets caught before it takes the compressor with it.")},

        {"id": "cx-heat-pump-alt",
         "h2": "Should I be looking at a heat pump instead?",
         "body": (
             "Worth pricing alongside, particularly if the furnace is also near the end. "
             "A heat pump is an air conditioner that can run backwards, so it cools in "
             "summer exactly like the unit you are replacing and then covers a good part "
             "of the heating season too. In this climate it usually pairs with the "
             "existing gas furnace as a dual-fuel system, with the furnace picking up "
             "when it gets properly cold. The thing to check first is your electrical "
             "panel, because that is the surprise that turns up after the quote rather "
             "than before it.")},
    ],
}

# Plumbing gets a pool of 16 rather than 10, because it started worst: 0.551 Jaccard,
# 29.1% novel, and a 61.2% boilerplate floor on a 373-word median page. Four picked
# from 16 means two cities share ~1.0 section on average against heating's ~1.6, and
# the added words drop the boilerplate share at the same time. Both levers, one change.
ANGLES["plumbing"] = [
    {"id": "px-hardwater",
     "h2": "Is the water here hard enough to matter?",
     "body": (
         "Yes, across most of this area, and it is the reason so many water heaters "
         "fail early around here. Hard water leaves scale on the heating element and in "
         "the tank bottom, which insulates the burner from the water and makes the "
         "heater work longer for the same hot shower. You see it first on fixtures and "
         "glassware, then in a heater that takes longer to recover. Softening is worth "
         "pricing on its own merits, but the honest first step is finding out your "
         "actual grains per gallon rather than assuming, because it varies by supplier "
         "and some of them changed in the last few years.")},

    {"id": "px-wh-age",
     "h2": "How long should a water heater last?",
     "body": (
         "Eight to twelve years on a tank, longer on a tankless. What matters more than "
         "the number is how it fails: a heater at the end of its life usually goes by "
         "leaking from the tank itself, and a tank leak is not repairable. That is why "
         "it is worth knowing the age before it happens. The date is in the serial "
         "number on the label, and a photo of that label is a two-minute job that turns "
         "a future emergency into a planned replacement. If yours is in a finished "
         "basement or over living space, plan earlier rather than later.")},

    {"id": "px-tankless",
     "h2": "Is a tankless water heater worth it?",
     "body": (
         "It depends on the house more than on the technology. Tankless gives you hot "
         "water that does not run out and takes up far less room, and it lasts longer "
         "than a tank. Against that, it usually needs a larger gas line and different "
         "venting, so the install is a bigger job than a straight tank swap. It also "
         "wants descaling on a schedule in water as hard as ours, and skipping that is "
         "how people end up disappointed. If you are replacing in an emergency with no "
         "hot water in the house, a tank is usually the faster answer.")},

    {"id": "px-drain-repeat",
     "h2": "The same drain clogs every few months. Why?",
     "body": (
         "Because clearing a clog and fixing the cause are two different jobs. A cable "
         "punches a hole through the blockage and the water runs again, which is the "
         "right answer at 11pm. But if the same line backs up on a schedule, something "
         "structural is doing it: grease built up on the pipe wall, a belly where the "
         "line has settled, roots at a joint, or a fitting that was never right. A "
         "camera down the line answers it in one visit and stops you paying for the "
         "same drain three times a year.")},

    {"id": "px-roots",
     "h2": "Can tree roots really get into a sewer line?",
     "body": (
         "Routinely, and older neighborhoods see it most because the mature trees and "
         "the clay tile sewer lines arrived together. Roots do not break into a sound "
         "pipe. They find a joint that is already weeping and grow toward the water, "
         "then thicken until the line catches paper and grease. The signs are more than "
         "one fixture backing up at once, gurgling from a toilet when the washer "
         "drains, and a lawn that is greener in a line across the yard. Cutting them "
         "clears it; whether the line then needs lining or replacing is a camera "
         "question, not a phone one.")},

    {"id": "px-sump",
     "h2": "How do I know the sump pump will work when I need it?",
     "body": (
         "Test it rather than trusting it, because a sump pump sits idle for months and "
         "then has one job. Pour a bucket of water into the pit slowly and watch: the "
         "float should rise, the pump should start, the water should drop, and it should "
         "shut off cleanly without chattering. Do that in early spring and again before "
         "winter. The two failures worth planning for are a stuck float, which is "
         "cheap, and a power cut during the storm that needed the pump, which is what "
         "battery backup exists for.")},

    {"id": "px-frozen",
     "h2": "Which pipes actually freeze, and what stops it?",
     "body": (
         "The ones on exterior walls, in crawl spaces, in unheated garages, and the "
         "hose bibs outside. A pipe rarely bursts where it froze; the ice blocks the "
         "line and the pressure builds between that block and a closed tap, so the "
         "split happens somewhere else entirely. On a hard freeze, open the cabinet "
         "doors under sinks on outside walls and let a pencil-width trickle run from "
         "the furthest tap. Disconnect hoses in autumn, because a hose left on a bib is "
         "the single most common frozen-pipe call we take.")},

    {"id": "px-pressure",
     "h2": "The water pressure has dropped. Where do I start?",
     "body": (
         "First work out whether it is the whole house or one fixture, because that "
         "splits the problem in half. One fixture is almost always an aerator or a "
         "cartridge, and both are small jobs. Whole house points at the pressure "
         "regulator, a partly closed main valve, or galvanized supply pipe that has "
         "corroded closed from the inside over decades. That last one is common in "
         "pre-war houses and it is progressive, so pressure that has been slowly "
         "falling for years is telling you something different from pressure that "
         "dropped last week.")},

    {"id": "px-galvanized",
     "h2": "My house has old galvanized pipe. Does it all have to go?",
     "body": (
         "Not necessarily all at once. Galvanized supply line rusts from the inside, so "
         "the bore narrows over decades until flow suffers and the water runs brown "
         "after the house has sat empty. Whether it wants full repiping or a partial "
         "depends on how much has already been replaced by previous owners, which is "
         "usually more than people expect. A look at the exposed runs in the basement "
         "tells you a lot for free. Where repiping is the right answer, it is worth "
         "doing before a remodel rather than after.")},

    {"id": "px-leak-hidden",
     "h2": "The water bill jumped and nothing looks wet. What now?",
     "body": (
         "Read the meter with everything in the house off. If it is still moving, you "
         "have a leak on the pressurised side and it is running somewhere you cannot "
         "see, usually under a slab, behind a wall, or in the line between the meter "
         "and the house. Before assuming the worst, rule out the toilets: a flapper "
         "that is not seating will run silently and waste more water than most people "
         "believe. Put a few drops of food coloring in the tank and wait twenty "
         "minutes without flushing. Color in the bowl means you found it.")},

    {"id": "px-shutoff",
     "h2": "Do you know where your main shutoff is?",
     "body": (
         "It is the single most useful thing to know before you need it, and most "
         "people find out during the emergency. In this area it is usually where the "
         "line enters the basement or crawl space, often near the front of the house "
         "and close to the meter. Find it now, turn it to confirm it actually moves, "
         "and turn it back. A valve that has not been operated in twenty years can "
         "seize, and discovering that with water coming through a ceiling is a much "
         "worse time to learn it than a Saturday afternoon.")},

    {"id": "px-disposal",
     "h2": "What should never go down the garbage disposal?",
     "body": (
         "Grease first, and it is not close. It goes down warm and liquid and cools "
         "into a solid on the pipe wall a few feet along, then catches everything after "
         "it. After that: coffee grounds, eggshells, pasta and rice, and anything "
         "fibrous like celery or onion skins. A disposal that hums without turning is "
         "usually jammed rather than dead, and there is a hex socket on the underside "
         "for exactly that. If it is silent, check the reset button before assuming it "
         "needs replacing.")},

    {"id": "px-toilet-running",
     "h2": "A toilet that runs on and off by itself. Serious?",
     "body": (
         "It is called phantom flushing and it means water is escaping from the tank "
         "into the bowl, so the fill valve keeps topping it up. The culprit is nearly "
         "always the flapper, which hardens with age and stops sealing, and it is one "
         "of the cheapest parts in the house. It is worth fixing quickly rather than "
         "living with, because it runs continuously and quietly, and a running toilet "
         "shows up on the water bill at a scale that surprises people who assumed it "
         "was just a noise.")},

    {"id": "px-backflow",
     "h2": "Why does a plumber care about my outside taps and irrigation?",
     "body": (
         "Because of backflow. If pressure in the main drops, water can be pulled "
         "backwards out of a hose left in a pool, a bucket, or an irrigation line, and "
         "into the drinking water. That is why hose bibs have vacuum breakers and why "
         "irrigation systems need a backflow device, and why some of them are required "
         "to be tested. It is not a sales conversation, it is a code one, and it is "
         "worth knowing what you have before a home sale puts it on someone's list.")},

    {"id": "px-gas-smell",
     "h2": "What should I do if I smell gas?",
     "body": (
         "Leave, then call from outside. Do not switch anything on or off, including "
         "lights, and do not use the phone indoors, because a switch contact is an "
         "ignition source. Once you are out, call the gas utility's emergency line "
         "first: they will come and make it safe at no charge, and they will do it "
         "faster than anyone else. Call us after that for the repair. This is the one "
         "plumbing situation where the right first call is not to a plumber, and "
         "anyone who tells you otherwise is wrong.")},

    {"id": "px-remodel",
     "h2": "We are remodeling. When should the plumber be involved?",
     "body": (
         "Earlier than most people ask. Once a wall is open you can see what is behind "
         "it, and decisions about moving a stack, upsizing a supply run or replacing "
         "the last of the old pipe cost a fraction of what they cost after the drywall "
         "is back. It is also when permits and inspections are cheapest to handle, "
         "because they can be scheduled around the rest of the work rather than "
         "holding it up. A short conversation at the drawing stage tends to save "
         "arguments at the tiling stage.")},
]

# Heating and cooling grown from 10 to 16, matching plumbing. The plumbing result is
# why: same mechanism, same four-per-page, but a pool of 16 landed 54.8% novel against
# heating's 48.1%. Four from 16 means two cities share about one section instead of
# 1.6, so the pool size was carrying the difference, not the writing.
ANGLES["heating"] += [
    {"id": "hx-burning-smell",
     "h2": "The vents smell like burning dust when the heat first comes on.",
     "body": (
         "That one is usually nothing. Dust settles on the heat exchanger over a summer "
         "of not running, and the first few cycles in autumn burn it off. It should "
         "fade within an hour or two of running and not come back. What is not normal "
         "is a smell that persists past that, a sharp electrical or plastic smell at "
         "any point, or anything like rotten eggs. The last one is the additive put "
         "into natural gas so you can smell a leak, and it means leave the house and "
         "call the gas utility before you call anyone else.")},

    {"id": "hx-co-alarm",
     "h2": "Where should carbon monoxide alarms actually go?",
     "body": (
         "One on every floor, and one within about fifteen feet of each sleeping area, "
         "because the whole point is waking someone up. They do not need to be at floor "
         "level; carbon monoxide mixes with air rather than sinking. Keep them a few "
         "feet clear of the furnace itself so brief startup readings do not nuisance-"
         "trip them. Replace the units on the date printed on the back, because the "
         "sensor has a service life whether or not it has ever sounded. If one goes off "
         "and then stops, treat it as real and get the furnace checked.")},

    {"id": "hx-dry-air",
     "h2": "Why is the house so dry in winter, and does a humidifier help?",
     "body": (
         "Cold outdoor air holds very little moisture, so every air change your house "
         "makes in January swaps damp indoor air for dry. The furnace does not cause it, "
         "it just moves it around. What you notice is static, dry skin, and gaps opening "
         "in hardwood floors and trim that close again in summer. A whole-house "
         "humidifier plumbed into the ductwork handles it more evenly than portable "
         "units, and it wants a humidistat rather than a fixed setting, because running "
         "too wet in a cold snap puts condensation on the inside of your windows.")},

    {"id": "hx-tuneup",
     "h2": "What actually happens during a furnace tune-up?",
     "body": (
         "It should be a list of measurements, not a look. Combustion analysis at the "
         "flue, gas pressure at the manifold, temperature rise across the heat "
         "exchanger, amp draw on the blower and the inducer, flame sensor cleaned and "
         "its microamp signal read, safeties tested rather than assumed, and a look at "
         "the heat exchanger itself. Ask for the numbers afterwards. A visit that "
         "produces no readings gives you nothing to compare against next year, and "
         "year-on-year comparison is most of what a tune-up is actually for.")},

    {"id": "hx-cool-start",
     "h2": "Why does the furnace blow cool air when it first starts?",
     "body": (
         "Because the burners light before the blower does, on purpose. The furnace "
         "gives the heat exchanger thirty seconds or so to warm up before it moves air "
         "across it, so the first air out of the vents is whatever was sitting in the "
         "ducts. If the cool air lasts longer than a minute or two, or the blower runs "
         "without the burners ever lighting, that is different: it usually means the "
         "furnace tried to fire and a safety stopped it, and it will keep retrying "
         "until it locks out.")},

    {"id": "hx-closed-vents",
     "h2": "Should I close vents in rooms I do not use?",
     "body": (
         "No, and it is one of the most common ways people make a system worse while "
         "trying to save money. Your furnace moves a fixed amount of air. Closing vents "
         "does not reduce that, it raises the pressure in the ductwork, which pushes "
         "more air out through leaks in the ducts and makes the blower work against "
         "itself. On a high-efficiency furnace it can raise the temperature rise enough "
         "to trip the high limit. If some rooms genuinely need less heat, that is a "
         "balancing job at the dampers, not at the registers.")},
]

ANGLES["cooling"] += [
    {"id": "cx-drain",
     "h2": "There is water on the floor near the indoor unit.",
     "body": (
         "Almost always the condensate drain. Cooling pulls moisture out of the air and "
         "that water has to go somewhere, usually down a small PVC line to a floor "
         "drain or a pump. Algae builds up in that line over a season and blocks it, "
         "the pan overflows, and you find it as a wet patch or a ceiling stain if the "
         "unit is upstairs. Many systems have a float switch that shuts the cooling off "
         "rather than let the pan overflow, so an air conditioner that has stopped for "
         "no obvious reason in humid weather is worth checking there first.")},

    {"id": "cx-setback",
     "h2": "Is it cheaper to leave the AC at one temperature all day?",
     "body": (
         "No. This one persists because it sounds sensible, but a house loses heat to "
         "the outside in proportion to the difference between inside and out. Letting "
         "the house drift up while nobody is home narrows that gap for hours and the "
         "system spends less energy overall, even counting the longer run to pull it "
         "back down. The one caveat is size: a setback of more than a few degrees on an "
         "undersized system can mean it never quite catches up on the hottest days, "
         "which is a comfort problem rather than a cost one.")},

    {"id": "cx-fan-auto",
     "h2": "Should the fan be set to AUTO or ON?",
     "body": (
         "AUTO for most houses, most of the time. On ON the blower runs continuously, "
         "which does even out temperatures between rooms and keeps air moving through "
         "the filter. The catch in a humid climate is that when the compressor stops, "
         "moisture is still sitting on the indoor coil, and a fan that keeps running "
         "evaporates it straight back into the house. You get a cool, clammy result and "
         "a higher bill. If you want the air mixing benefit, a variable-speed blower on "
         "low is the version of this that does not fight the dehumidification.")},

    {"id": "cx-musty",
     "h2": "The air smells musty when the AC starts.",
     "body": (
         "That smell is biological growth on a coil that stays wet, and it is common in "
         "systems that short cycle or run with the fan permanently on. It is worth "
         "taking seriously rather than masking, because the air carrying it is the air "
         "the whole house breathes. The fixes go in order of cost: clear and treat the "
         "condensate drain, clean the coil properly rather than spraying it, correct "
         "whatever is keeping the coil wet, and only then look at UV or filtration. "
         "Starting at the last step is how people spend money and still smell it.")},

    {"id": "cx-annual-refrigerant",
     "h2": "I am told the system needs refrigerant every year. Is that normal?",
     "body": (
         "No. Refrigerant is not a consumable. It runs in a sealed loop and a correctly "
         "working system will hold the same charge for its whole life. A system that "
         "needs topping up annually has a leak, and adding refrigerant without finding "
         "it means paying every year for something escaping into the air. Ask for the "
         "leak to be found and quoted. Sometimes the answer is a repair worth making "
         "and sometimes it is a coil that costs enough to change the replacement "
         "conversation, but either way you should be told which.")},

    {"id": "cx-attic",
     "h2": "My air handler is in the attic. Does that change anything?",
     "body": (
         "It changes what a small problem costs you. An attic unit sits above finished "
         "ceilings, so a blocked condensate drain that would be a wet floor in a "
         "basement becomes a ceiling repair instead. Attics also run far hotter than "
         "the rest of the house, so duct leakage up there loses cooled air into the "
         "worst possible place and the insulation on those ducts matters more than it "
         "would elsewhere. Worth confirming there is a secondary drain pan with its own "
         "float switch under the unit, because that is the thing standing between a "
         "clog and your ceiling.")},
]
