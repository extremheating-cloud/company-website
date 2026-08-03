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
section only exists to make a page look different from its neighbor, it is
padding, and padding on 234 pages is how a site earns a thin-content problem
instead of solving one. Each angle below answers a question a homeowner in this
market actually asks, and would earn its place on a single page with no
neighbors at all.

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

# The remaining three services, 16 each, same shape as the first three.
#
# Two hard constraints held in this block. Radon does not appear anywhere in the IAQ
# pool: we do not do radon mitigation (client), and an air-quality page is exactly
# where a reader would assume otherwise if it were mentioned at all. And the duct
# pool opens by admitting when duct cleaning is not worth buying, because a page
# selling duct cleaning that will not say that is the reason the whole category has
# the reputation it does.
ANGLES["maintenance"] = [
    {"id": "mx-why-twice",
     "h2": "Why twice a year rather than once?",
     "body": (
         "Because heating and cooling are two different machines sharing a cabinet, and "
         "they fail at opposite ends of the year. A spring visit is about the "
         "condenser, the refrigerant charge and the condensate drain before the first "
         "heat wave. An autumn visit is about combustion, the heat exchanger and the "
         "safeties before the first hard freeze. Doing one visit in between gets you "
         "half of each at the wrong time of year. If you only ever do one, make it "
         "autumn: a no-cool night is uncomfortable and a no-heat night can freeze "
         "pipes.")},

    {"id": "mx-worth-it",
     "h2": "Does maintenance actually make equipment last longer?",
     "body": (
         "It makes early failure less likely, which is not quite the same claim and is "
         "the honest version. Most of what shortens a system's life is airflow: a "
         "starved return makes a furnace run hot and an air conditioner run cold, and "
         "both stress the parts that cost the most to replace. Maintenance catches the "
         "dirty coil, the failing capacitor and the sagging blower wheel while they are "
         "still small. What it cannot do is make a twenty-year-old system into a new "
         "one, and anyone promising that is selling something else.")},

    {"id": "mx-warranty",
     "h2": "Does my warranty require annual maintenance?",
     "body": (
         "Most manufacturer warranties do, and it is the part people find out about at "
         "the worst moment. The parts warranty on a new system typically requires "
         "documented annual service by a licensed contractor, and a compressor claim is "
         "exactly when someone asks for those records. Keep the invoices, or let "
         "whoever services it keep them for you. This is the single cheapest reason to "
         "maintain a system that is running perfectly well and does not feel like it "
         "needs anything.")},

    {"id": "mx-diy",
     "h2": "What can I do myself between visits?",
     "body": (
         "Four things, and they cover most of what goes wrong. Change the filter on a "
         "real schedule rather than when you remember. Keep two feet clear around the "
         "outdoor unit and rinse the coil from the inside out with a hose, power off, "
         "once a season. Pour a cup of vinegar down the condensate drain line in "
         "spring. And listen: a noise that is new is information, and the cheapest "
         "repair is always the one booked in the week you first noticed something "
         "rather than the month it finally stopped.")},

    {"id": "mx-numbers",
     "h2": "What should a tune-up leave me with?",
     "body": (
         "Numbers. Temperature rise across the furnace, static pressure in the "
         "ductwork, superheat and subcooling on the air conditioner, amp draws, and a "
         "combustion reading at the flue. Ask for them, and keep them. One year of "
         "readings tells you the system is fine today. Three years of readings tells "
         "you the compressor is drawing more than it used to and the refrigerant charge "
         "is drifting, which is the difference between replacing a part in April and "
         "replacing a system in July.")},

    {"id": "mx-skip-year",
     "h2": "I skipped a year. Does that matter?",
     "body": (
         "One skipped year is not a disaster, and nobody should pretend otherwise. What "
         "it costs you is the comparison: a technician arriving with no prior readings "
         "is looking at a snapshot rather than a trend. The two things worth checking "
         "sooner rather than later after a gap are the condensate drain, which blocks "
         "quietly and can overflow into a ceiling, and the flame sensor, which fouls "
         "gradually and eventually stops the furnace lighting on the first cold night "
         "of the year.")},

    {"id": "mx-new-system",
     "h2": "It is brand new. Does it need maintenance already?",
     "body": (
         "Yes, and for two reasons that have nothing to do with the equipment being "
         "worn. The first is the warranty, which usually requires it from year one. The "
         "second is that a new system's first year is when installation issues surface: "
         "a charge that was slightly off, a duct connection that has worked loose, a "
         "condensate line pitched wrong. Those are all cheap to correct early and "
         "expensive to discover after they have been quietly stressing the system for "
         "three summers.")},

    {"id": "mx-priority",
     "h2": "What does priority scheduling actually mean?",
     "body": (
         "It means you go ahead of non-members on the day everyone calls at once, which "
         "is the only day it matters. On an ordinary Tuesday in April, everybody gets "
         "same-day service and the distinction is invisible. On the first 95-degree "
         "afternoon of the summer, or the morning after the first hard freeze, the "
         "board fills before lunch. That is what the queue position is for. It is worth "
         "understanding that plainly rather than discovering it either way in July.")},

    {"id": "mx-bills",
     "h2": "Will maintenance lower my energy bill?",
     "body": (
         "A little, and less than most advertising implies. A dirty condenser coil or a "
         "clogged filter genuinely does cost you efficiency, and cleaning them recovers "
         "it. But a well-maintained fifteen-year-old system is still a fifteen-year-old "
         "system, and the savings are measured in percent rather than in halves. If "
         "your bill has jumped noticeably, maintenance is the right first call to find "
         "out why, but treat a large predicted saving with the same skepticism you "
         "would apply to any other number quoted before the work.")},

    {"id": "mx-cover",
     "h2": "Should I cover the outdoor unit for winter?",
     "body": (
         "Generally no. A heat pump must not be covered at all, because it runs all "
         "winter. An air conditioner does not need one either: the unit is built to sit "
         "outside, and a full wrap traps moisture against the metal and gives mice "
         "somewhere dry to nest in the wiring. If you want to keep leaves out of the "
         "top, a piece of plywood weighted on the fan grille does that without sealing "
         "the cabinet. Take it off before the first cooling call in spring.")},

    {"id": "mx-two-systems",
     "h2": "We have two systems. Do both need visits?",
     "body": (
         "Yes, and they usually need them at different times for different reasons. In "
         "most two-system houses one serves upstairs and one down, and the upstairs "
         "unit works considerably harder in summer while the downstairs one carries "
         "more of the winter. They also tend to be different ages, because they rarely "
         "fail together. Treat them as two pieces of equipment with two sets of "
         "readings rather than one appointment, because the older one is where the next "
         "decision is going to come from.")},

    {"id": "mx-what-fails",
     "h2": "What actually fails most, and would maintenance have caught it?",
     "body": (
         "Capacitors first, by a wide margin, then contactors, flame sensors and "
         "condensate blockages. All four are cheap parts and all four are checkable, "
         "which is the honest case for maintenance: a weak capacitor reads weak before "
         "it fails and gets replaced during a scheduled visit rather than on an "
         "emergency one at a different rate. What maintenance does not predict is a "
         "compressor or a heat exchanger failing outright, and no honest inspection "
         "will promise you it does.")},

    {"id": "mx-filter-vs",
     "h2": "If I change the filter religiously, is that enough?",
     "body": (
         "It is the most valuable thing you can do and it is not the whole job. The "
         "filter protects the blower and the coil from dust, which is why a neglected "
         "one causes so much downstream damage. What it does not touch is the outdoor "
         "coil, the refrigerant charge, the electrical connections that loosen with "
         "thermal cycling, the condensate path, or anything on the combustion side of a "
         "furnace. Think of the filter as the part you own and the rest as the part "
         "that needs instruments.")},

    {"id": "mx-timing",
     "h2": "When should I book, to avoid the rush?",
     "body": (
         "Late winter for the cooling visit and late summer for the heating one, which "
         "feels a season early and is exactly the point. Book in April and you are "
         "competing with everyone whose air conditioner just failed. Book in February "
         "and you get the appointment window you actually want. It also means a problem "
         "found in the tune-up gets fixed with time in hand, rather than becoming a "
         "decision made in a hot house with a technician standing there.")},

    {"id": "mx-old-system",
     "h2": "The system is old. Is maintenance throwing good money after bad?",
     "body": (
         "Not if it is buying you information. On a system past fifteen years, the "
         "purpose of a visit shifts: less about extending life and more about knowing "
         "where you stand before winter, so a replacement is a decision you make in "
         "September rather than one made for you in January. Ask directly for an "
         "assessment of how much life is realistically left. A straight answer to that "
         "is worth more than the tune-up itself.")},

    {"id": "mx-records",
     "h2": "What should I keep, and for how long?",
     "body": (
         "Keep the install paperwork for as long as you own the equipment: model and "
         "serial numbers, the install date, and the warranty registration. Keep service "
         "invoices for the life of the system, because that is the record a warranty "
         "claim asks for. Photograph the data plate on both the indoor and outdoor "
         "units once and keep it on your phone. When something fails on a Sunday, being "
         "able to read the model number out over the phone is the difference between a "
         "part on the truck and a part on order.")},
]

ANGLES["duct-cleaning"] = [
    {"id": "dx-honest",
     "h2": "Does duct cleaning actually do anything?",
     "body": (
         "Sometimes, and not always, and it is worth saying so before anyone books one. "
         "For a normal house with a decent filter and no particular history, cleaning "
         "the ducts is not going to transform your air or your energy bill, whatever "
         "the mailers say. Where it genuinely earns its money is after construction or "
         "a remodel, after any kind of pest or rodent activity, where there is visible "
         "dust discharging from the registers, or where the system has been running "
         "without a filter. If none of those apply, ask what the specific problem is "
         "that cleaning is meant to solve.")},

    {"id": "dx-how-know",
     "h2": "How do I know if my ducts actually need cleaning?",
     "body": (
         "Take a register cover off and look, and take a photo of what you see. Some "
         "settled dust on the bottom of the duct is normal in any house. What is not "
         "normal is a visible layer coating the sides, debris you can identify like "
         "drywall dust or insulation, anything that looks like nesting material, or a "
         "smell that turns up when the system starts and fades when it stops. Ask any "
         "contractor to show you inside your own ducts before quoting, and be wary of "
         "one who quotes without looking.")},

    {"id": "dx-proper",
     "h2": "What does a proper duct cleaning actually involve?",
     "body": (
         "Negative pressure and agitation, in that order. A vacuum unit is connected to "
         "the system so the whole duct run is under suction, and then each branch is "
         "agitated with brushes or air whips so what is stuck to the wall lets go and "
         "gets pulled out rather than blown further in. The furnace or air handler "
         "cabinet, the blower wheel and the coil are part of the job, because a clean "
         "duct feeding a filthy blower has not achieved much. Anything advertised as a "
         "quick vacuum at each register is not this.")},

    {"id": "dx-dryer",
     "h2": "Is the dryer vent worth doing at the same time?",
     "body": (
         "It is the one in this category with a genuine safety case, and it is often "
         "the more urgent of the two. Lint accumulates in the duct run rather than in "
         "the trap, and a restricted dryer vent is both a fire risk and the reason a "
         "load takes three cycles to dry. The signs are clothes still damp on a normal "
         "cycle, the outside of the dryer running hot, or a flap outside that no longer "
         "opens properly. Long runs and runs with several elbows need it more often "
         "than short straight ones.")},

    {"id": "dx-frequency",
     "h2": "How often should ducts be cleaned?",
     "body": (
         "There is no calendar answer, and any company giving you a fixed interval is "
         "guessing at your house. Condition drives it: pets, smokers, allergies, "
         "recent construction, and whether the system has been run without a filter all "
         "change the answer far more than time does. For most houses with none of "
         "those, the honest interval is longer than the industry advertises. Look "
         "inside a register every couple of years and let what you see decide it.")},

    {"id": "dx-allergies",
     "h2": "Will cleaning the ducts help my allergies?",
     "body": (
         "It can help, and it is rarely the whole answer, so it is worth setting the "
         "expectation before the money. Most household allergens are generated and "
         "circulated continuously rather than stored in ductwork, so cleaning removes a "
         "reservoir rather than the source. If allergies are the actual problem, "
         "filtration and humidity control usually move the needle further, and the "
         "sequence that makes sense is to fix the source first, improve the filtration "
         "second, and clean the ducts if there is a reason specific to your system.")},

    {"id": "dx-mold",
     "h2": "There is something that looks like mold in the ductwork.",
     "body": (
         "Stop and identify it before anyone cleans it. Growth in ductwork means "
         "moisture is getting in, and cleaning without fixing the moisture buys you a "
         "few months. The usual sources are an air conditioner coil that never dries "
         "out, a condensate problem, uninsulated metal duct sweating in a humid crawl "
         "space, or duct board that got wet. Cleaning is part of the answer, but the "
         "part that matters is finding out where the water is coming from, and that is "
         "a different conversation from a cleaning quote.")},

    {"id": "dx-remodel",
     "h2": "We are remodeling. Before or after?",
     "body": (
         "After, and it is one of the clearest cases for doing it at all. Drywall dust "
         "is fine, abrasive and gets everywhere, and a system running during "
         "construction pulls it straight into the return and distributes it through the "
         "house. If work is starting, cover the returns and change the filter far more "
         "often than usual while it is going on. Then clean once the dust-producing "
         "work is finished rather than partway through, or you will be paying for it "
         "twice.")},

    {"id": "dx-airflow",
     "h2": "Will cleaning improve my airflow?",
     "body": (
         "Only if the restriction is actually dust, which it usually is not. Weak "
         "airflow is far more often undersized returns, crushed flex duct, closed "
         "dampers, a dirty blower wheel or a filter too dense for the system. A blower "
         "wheel caked with dust genuinely does move less air and does get better after "
         "cleaning. Duct walls with a dusting on them do not restrict much. If airflow "
         "is the complaint, ask for static pressure to be measured, because that "
         "number tells you where the restriction really is.")},

    {"id": "dx-sanitizer",
     "h2": "Should I have the ducts sanitized or fogged?",
     "body": (
         "Be careful with this one. Spraying a biocide or a sealant into ductwork is "
         "sold as an add-on far more often than it is genuinely warranted, and you are "
         "putting a chemical into the path that feeds every room in your house. If "
         "there is confirmed growth, the answer is finding the moisture and removing "
         "the growth mechanically. Ask what specifically is being applied, why it is "
         "needed in your case, and what the label says about occupied spaces. A vague "
         "answer to any of those is your answer.")},

    {"id": "dx-rodents",
     "h2": "Something has been living in the ductwork.",
     "body": (
         "Then cleaning is genuinely warranted, and it is not the first step. The entry "
         "point has to be found and closed first, or you are cleaning a duct that gets "
         "reoccupied. Nesting material, droppings and the smell that comes with them do "
         "belong out of a system that blows into bedrooms, and this is the scenario "
         "where duct cleaning is unambiguously worth the money. Expect the job to "
         "include the return side, which is usually where they get in.")},

    {"id": "dx-newhouse",
     "h2": "We just bought the house. Is it worth doing now?",
     "body": (
         "It is one of the better times, for a reason that is more about information "
         "than dust. Nobody can tell you how the previous owners ran the system, "
         "whether the filter was changed, whether there was ever a pet or a smoker, or "
         "whether anything was built or demolished with the system running. Opening it "
         "up answers all of that, and a look inside a couple of registers before you "
         "commit to the full job will usually tell you whether it needs doing at all.")},

    {"id": "dx-before-after",
     "h2": "What should I ask to see afterwards?",
     "body": (
         "Before and after photographs of the same locations, including inside the "
         "trunk lines and the blower compartment rather than only the register boots. "
         "Any company doing this properly expects to be asked and will have them. Two "
         "photographs of a register cover prove very little. This is the simplest "
         "protection against paying for the version of this job that consists of a "
         "vacuum at each vent and an invoice, which is common enough in this trade to "
         "be worth guarding against.")},

    {"id": "dx-sealing",
     "h2": "Is duct sealing different from duct cleaning?",
     "body": (
         "Completely, and sealing is usually the one that saves money. Cleaning removes "
         "what is inside the ducts. Sealing closes the joints and seams that are "
         "leaking conditioned air into an attic, a crawl space or a wall cavity, which "
         "in a typical house is a meaningful share of what you paid to heat and cool. "
         "If your goal is a lower bill or rooms that never keep up, sealing and airflow "
         "are the conversation. If your goal is what is coming out of the registers, "
         "cleaning is.")},

    {"id": "dx-registers",
     "h2": "Can I just clean the vents myself?",
     "body": (
         "You can, and it is worth doing, as long as you know what it does and does "
         "not achieve. Pulling the register covers, washing them, and vacuuming as far "
         "into the boot as the hose reaches removes the dust you can see and the pet "
         "hair that collects right at the opening. What you cannot reach is the trunk "
         "line, the branch runs and the blower, which is where anything that actually "
         "matters accumulates. Treat it as housekeeping rather than as a substitute.")},

    {"id": "dx-smell",
     "h2": "There is a smell when the system starts up.",
     "body": (
         "The smell usually identifies itself. Dusty and hot for the first hour of "
         "heating season is normal. Musty on the cooling side points at a wet coil or a "
         "blocked condensate drain rather than at the ducts. Sharp and chemical, or "
         "anything like rotten eggs, means stop and call rather than investigate. A "
         "smell that is genuinely coming from the ductwork tends to be constant "
         "whenever air moves, not just at startup, and that distinction is worth making "
         "before paying to clean anything.")},
]

ANGLES["indoor-air-quality"] = [
    {"id": "ix-what-matters",
     "h2": "What actually affects the air in a house?",
     "body": (
         "Four things, roughly in order: moisture, ventilation, filtration and source "
         "control. Humidity that sits too high grows things and too low irritates "
         "everything. Ventilation decides whether what you generate indoors gets "
         "diluted or accumulates. Filtration catches particles, and only particles. "
         "Source control means the cooking, the cleaning products, the attached garage "
         "and the pets that put things into the air in the first place. Most air "
         "quality money gets spent on the third one when the answer was one of the "
         "other three.")},

    {"id": "ix-purifiers",
     "h2": "Do air purifiers actually work?",
     "body": (
         "The ones that move enough air through a good enough filter do, within the "
         "room they are in. That last part is where expectations go wrong: a portable "
         "unit sized for a bedroom does very little for a house. Whole-house media "
         "filtration built into the ductwork treats everything the system circulates, "
         "which is a different scale of job. Look for how much air a unit actually "
         "moves rather than the room size printed on the box, and be skeptical of "
         "anything whose main claim is ozone or ions.")},

    {"id": "ix-uv",
     "h2": "What do UV lights in the ductwork actually do?",
     "body": (
         "Two quite different jobs get sold under one name. A coil light aimed at the "
         "evaporator keeps growth off a surface that is wet for half the year, and that "
         "one has a straightforward case: it keeps a coil clean and it keeps the musty "
         "smell down. An air-stream light is meant to treat organizms as they pass, and "
         "air moves quickly, so contact time is short and the benefit is much harder to "
         "demonstrate. If someone is quoting UV, ask which of the two it is and what it "
         "is being asked to fix.")},

    {"id": "ix-humidity-high",
     "h2": "The house feels damp even with the AC running.",
     "body": (
         "Cooling removes moisture only while the coil is cold and air is moving across "
         "it. An oversized system satisfies the thermostat in short bursts and never "
         "runs long enough to dehumidify, which is how a house ends up cool and clammy. "
         "Above about 60% relative humidity you get the conditions for dust mites and "
         "mold regardless of how clean the house is. The fix is sometimes a "
         "dehumidifier and is often correcting why the system short cycles, so measure "
         "the humidity before buying equipment for it.")},

    {"id": "ix-humidity-low",
     "h2": "Everything is static and the wood floors are gapping.",
     "body": (
         "That is winter dryness, and it is a real air quality problem rather than an "
         "inconvenience. Cold outdoor air carries almost no moisture, so every air "
         "change in January leaves the house drier. Below about 30% relative humidity "
         "you get static, cracked skin, irritated airways and gaps opening in flooring "
         "and trim. A whole-house humidifier on a humidistat handles it more evenly "
         "than portable units. Do not simply run it high: too much moisture in a cold "
         "snap condenses on windows and inside exterior walls.")},

    {"id": "ix-merv",
     "h2": "Is a higher MERV filter always better?",
     "body": (
         "No, and this is the most common way people make things worse while trying to "
         "help. A denser filter catches more, and it also restricts more air, and a "
         "system designed around a one-inch filter can be starved by a high-MERV one "
         "dropped into the same slot. Starved airflow means a furnace running hot and "
         "an air conditioner freezing its coil. If you want serious filtration, the "
         "answer is a thicker media cabinet with far more surface area, not a denser "
         "filter in the existing gap.")},

    {"id": "ix-ventilation",
     "h2": "Can a house be too airtight?",
     "body": (
         "It can be too airtight without deliberate ventilation, which is not the same "
         "as saying tight houses are bad. A leaky old house ventilates by accident, "
         "expensively and unevenly. A tight modern one holds humidity, cooking "
         "byproducts and everything else indoors until something removes them on "
         "purpose. That is what mechanical fresh air is for, and it is why newer houses "
         "sometimes feel stuffy despite being far better built. The answer is "
         "controlled ventilation rather than deliberately making the shell leak.")},

    {"id": "ix-co",
     "h2": "What is the difference between CO and CO2 in a house?",
     "body": (
         "Carbon monoxide is the dangerous one and comes from incomplete combustion: "
         "furnaces, water heaters, fireplaces, a car in an attached garage. It has no "
         "smell and it needs alarms. Carbon dioxide is what people exhale, and while it "
         "is not toxic at household levels, a room where it climbs is a room that is "
         "not being ventilated, so it is a useful proxy for stale air. Alarms are for "
         "the first. The second is a ventilation question rather than a safety one.")},

    {"id": "ix-allergies",
     "h2": "What actually helps with allergies at home?",
     "body": (
         "In rough order of effect: keep humidity between about 35 and 50%, upgrade to "
         "real media filtration sized for the system rather than a denser one-inch "
         "filter, deal with the source where you can, and only then look at added "
         "equipment. Bedrooms matter more than the rest of the house because of how "
         "many hours are spent in them. Nothing here is dramatic on its own, and the "
         "combination usually is, which is the opposite of how air quality equipment "
         "tends to be sold.")},

    {"id": "ix-cooking",
     "h2": "Does cooking really affect indoor air that much?",
     "body": (
         "More than most people expect, particularly with gas. Cooking puts fine "
         "particles and combustion byproducts straight into the room, and a range hood "
         "that recirculates through a charcoal filter rather than venting outside does "
         "very little about it. Use the hood every time and check that it actually "
         "vents outdoors. If it does not, opening a window while cooking does more than "
         "any purifier will, and it costs nothing.")},

    {"id": "ix-basement",
     "h2": "The basement smells musty and it is spreading upstairs.",
     "body": (
         "Basements run cooler, so humid summer air condenses down there, and anything "
         "the air handler pulls in gets distributed to the whole house. Measure the "
         "relative humidity before doing anything else. Above about 60% the answer is "
         "dehumidification and finding where the water is coming from, not air "
         "freshening. Check the obvious sources first: grading and downspouts outside, "
         "an uninsulated cold-water line sweating, and a condensate drain that is "
         "discharging where it should not.")},

    {"id": "ix-pets",
     "h2": "We have pets. What actually helps?",
     "body": (
         "Filtration does real work here, because pet dander is a particle and "
         "particles are exactly what filters catch. A proper media cabinet is worth far "
         "more than a denser one-inch filter, and it also needs changing more often "
         "than the box says in a house with animals. Beyond that, the return grille is "
         "worth vacuuming regularly, because that is where hair collects, and a "
         "restricted return causes more problems than the hair itself ever would.")},

    {"id": "ix-testing",
     "h2": "Is it worth testing the air, and for what?",
     "body": (
         "Two measurements are cheap and genuinely useful: relative humidity and "
         "particulate. A basic hygrometer in a couple of rooms tells you more about "
         "your house than most paid assessments, because humidity drives so much of "
         "the rest. Beyond that, be careful what you are being sold. Broad "
         "contaminant panels tend to produce a list of things present in every house at "
         "levels nobody can interpret, and the result is usually a quote rather than an "
         "answer.")},

    {"id": "ix-newbuild",
     "h2": "Our house is new. Why does the air feel worse?",
     "body": (
         "Because it is tight and because it is new, and those are two separate "
         "effects. A well-sealed shell holds indoor moisture and cooking byproducts "
         "instead of leaking them away, so anything generated indoors stays longer. "
         "New materials also off-gas for months: flooring, cabinets, paint, adhesives "
         "and furniture. Ventilation is the answer to both, and in a new house that "
         "usually means using the mechanical ventilation that is already installed "
         "rather than adding equipment.")},

    {"id": "ix-whole-vs-portable",
     "h2": "Whole-house or portable? Which is the better buy?",
     "body": (
         "It depends whether the problem is a room or a house. A portable unit in a "
         "bedroom is a reasonable, cheap answer to one person's sleep. It is not a "
         "house solution, and buying five of them is worse value than doing it once in "
         "the ductwork. The catch with whole-house is that it only treats air while the "
         "system is running, so if yours cycles rarely in mild weather, a "
         "variable-speed blower on low changes what the equipment can actually do.")},

    {"id": "ix-ducts-cross",
     "h2": "Would cleaning the ducts fix this?",
     "body": (
         "Occasionally, and less often than it is sold for. Ductwork holds a reservoir "
         "of settled dust rather than generating anything, so cleaning helps most where "
         "there is a specific reason: construction dust, pest activity, or visible "
         "debris blowing from registers. For ordinary air quality complaints, humidity "
         "and filtration usually move further. If someone quotes duct cleaning as the "
         "answer to an air quality problem without looking inside your ducts first, "
         "that is worth questioning.")},
]

# City OVERVIEW pages. A different pool from the six service pools, because these pages
# are not about one trade: a tail overview had three H2s and 392 words, thinner than any
# service page. These angles are the whole-home, choosing-and-process questions a
# homeowner asks before they have decided what is even wrong, which is the job an
# overview page is actually doing.
#
# Keyed as "overview" and picked the same way. Deliberately no overlap in subject with
# the service pools: nothing here re-explains a furnace or a drain, because a reader
# who lands on the city page and wants that is one click from the page that does it.
ANGLES["overview"] = [
    {"id": "ox-choosing",
     "h2": "How do I check that a contractor is legitimate?",
     "body": (
         "Three things, and all three are quick. Ask for the Ohio license number and "
         "look it up rather than taking the sticker on the van as proof. Ask whether "
         "they carry liability insurance and workers' compensation, because if someone "
         "is hurt in your house and the answer is no, that becomes your problem. And "
         "ask who is actually coming: some companies subcontract the install to whoever "
         "is available. None of those questions are rude, and the reaction you get to "
         "asking them tells you almost as much as the answers.")},

    {"id": "ox-first-visit",
     "h2": "What actually happens on the first visit?",
     "body": (
         "You get an arrival window rather than a whole day. The technician diagnoses "
         "before quoting, which means the first part of the visit is finding out what "
         "is wrong rather than telling you what it costs. You hear the price and agree "
         "to it before any work starts. If the answer turns out to be a decision rather "
         "than a repair, you should get both options with what each one buys you, and "
         "you should not be asked to decide on the spot.")},

    {"id": "ox-emergency",
     "h2": "Is this an emergency, or can it wait until Monday?",
     "body": (
         "Call now, whatever the hour, for: no heat when it is genuinely cold, no "
         "cooling in a heat wave with anyone vulnerable in the house, water actively "
         "coming in, a sewage backup, or any smell of gas. Those get worse and some of "
         "them get expensive fast. It can usually wait for a scheduled slot if it is one "
         "room uncomfortable, a slow drain, a noise that has not changed, or a system "
         "that is working but not well. When you genuinely cannot tell, call and "
         "describe it, and expect a straight answer rather than a truck.")},

    {"id": "ox-before-arrival",
     "h2": "What should I do before the technician gets here?",
     "body": (
         "Clear a path to the equipment, and move anything you care about out of the "
         "way, because basements and utility closets accumulate. Put pets somewhere "
         "else, not because anyone minds them but because doors get propped open. Have "
         "the model and serial numbers handy if you can find them, or a photo of the "
         "data plate. And write down what you actually noticed and when: an "
         "intermittent fault that is not happening right now is diagnosed largely from "
         "what you can describe.")},

    {"id": "ox-permits",
     "h2": "Who pulls the permit, and does it matter?",
     "body": (
         "We do, and yes. A permit means an independent inspector looks at the gas, the "
         "venting and the electrical on work that can hurt you if it is wrong. Which "
         "authority issues it changes from town to town around here more than people "
         "expect, and a contractor who has only worked one county sometimes files in "
         "the wrong place. It also matters when you sell: unpermitted work on a system "
         "is the kind of thing that surfaces during a sale and gets negotiated against "
         "you.")},

    {"id": "ox-quotes",
     "h2": "How do I compare three quotes that are not comparable?",
     "body": (
         "Put them side by side on what is actually included rather than on the number "
         "at the bottom. Was a load calculation done, or was the size copied off the old "
         "label. Does the price include the permit, the inspection, hauling the old "
         "equipment away, and any duct or electrical work the job needs. What is the "
         "warranty on parts and on labor, and who honors each. A quote that is "
         "meaningfully cheaper is usually cheaper for a reason, and the reason is "
         "normally one of those lines missing.")},

    {"id": "ox-house-age",
     "h2": "Does the age of the house change what I should expect?",
     "body": (
         "Considerably, and it is the single most useful thing you can tell us on the "
         "phone. Pre-war housing tends to bring undersized returns from a later "
         "conversion, galvanized supply line closing up from the inside, and cast-iron "
         "drains. Mid-century ranches bring original ductwork sized for a smaller "
         "system than the one that is in there now. Newer construction brings tight "
         "shells that hold humidity, and equipment installed to a builder's budget "
         "reaching end of life all at once across a whole street.")},

    {"id": "ox-same-day",
     "h2": "What does same-day service actually mean in practice?",
     "body": (
         "That about nine calls in ten get handled the day they come in, and that the "
         "tenth is honest about it rather than promised and missed. The days it does "
         "not hold are predictable: the first hard freeze, the first properly hot week, "
         "and the morning after a storm, when everyone calls within the same few hours. "
         "That is what priority scheduling is for and it is the only time it matters. "
         "If a company promises same-day every day of the year, ask what happens on "
         "those three days.")},

    {"id": "ox-shutoffs",
     "h2": "What should every homeowner know how to turn off?",
     "body": (
         "Four things, and the time to find them is not during the emergency. The main "
         "water shutoff, usually where the line enters the basement or crawl space. The "
         "gas shutoff at the meter, and which way it turns. The breaker for the furnace "
         "or air handler. And the furnace switch itself, which looks like a light "
         "switch and gets knocked off more often than anything else on this list. Find "
         "all four this weekend and check that they actually move.")},

    {"id": "ox-two-trades",
     "h2": "Why does one company doing both trades matter?",
     "body": (
         "Mostly because of the problems that sit on the boundary and get passed back "
         "and forth. A humidifier tied into the ductwork is plumbing and HVAC. A "
         "condensate line that will not drain is both. A gas line feeding a furnace and "
         "a water heater is both. When those are split between two companies, the "
         "common outcome is each one telling you it is the other's job. One number for "
         "both is less about convenience than about the diagnosis not stopping at a "
         "boundary.")},

    {"id": "ox-buying-house",
     "h2": "We are buying here. What should we check before closing?",
     "body": (
         "Ages first: the data plate on the furnace, the air conditioner and the water "
         "heater will each tell you the year, and that is three replacement decisions "
         "with dates on them. Then ask whether the systems have service records, "
         "because a warranty on newer equipment usually depends on them. Then look for "
         "the things a general home inspection tends to note but not price: undersized "
         "returns, a water heater at the end of its life, and any sign that a system "
         "was replaced without a permit.")},

    {"id": "ox-warranty",
     "h2": "Who actually covers what when something fails?",
     "body": (
         "Two separate warranties, and people conflate them. The manufacturer covers "
         "parts, usually for a set number of years and usually only if the system was "
         "registered and has documented annual maintenance. The installer covers labor "
         "and workmanship, for a period they set. A failed part inside the parts "
         "warranty still means paying someone to fit it unless the labor warranty is "
         "live too. Ask for both terms in writing at the quote stage, not after.")},

    {"id": "ox-membership",
     "h2": "Is a maintenance membership worth it, or should I just pay per visit?",
     "body": (
         "Do the arithmetic on your own house rather than on the brochure. Two tune-ups "
         "a year at the published price is the baseline, and the membership adds a "
         "reduced service call, a discount on repairs and priority scheduling. If you "
         "have one system and it is newer, paying per visit is perfectly reasonable. If "
         "you have two systems, or older equipment, or the kind of house where a "
         "no-heat night is a real problem, the queue position tends to be worth more "
         "than the discount.")},

    {"id": "ox-seasonal",
     "h2": "What is worth doing before each season?",
     "body": (
         "Before heating season: change the filter, clear anything stacked against the "
         "furnace, test the carbon monoxide alarms, and disconnect the garden hoses. "
         "Before cooling season: rinse the outdoor coil with the power off, cut back "
         "whatever has grown within two feet of it, and pour a cup of vinegar down the "
         "condensate line. Both of those lists take under an hour and prevent a "
         "meaningful share of the calls we take at the start of each season.")},

    {"id": "ox-landlord",
     "h2": "We rent the place out. Does that change anything?",
     "body": (
         "It changes who needs to know what. Whoever holds the account should be the "
         "person who can approve work, or every visit stalls waiting for a phone call. "
         "It is worth agreeing in advance what a technician can proceed with without "
         "asking, because a no-heat call at 9pm on a Friday is a bad time to discover "
         "nobody can authorize a part. Keep the service records: they matter for the "
         "warranty and they matter when a tenant says something was never fixed.")},

    {"id": "ox-second-opinion",
     "h2": "I have been told I need a new system. Should I get another opinion?",
     "body": (
         "If the recommendation arrived without a diagnosis you understood, yes. A "
         "replacement recommendation should come with a specific reason: a cracked heat "
         "exchanger, a failed compressor, a repair quote approaching a third of "
         "replacement cost on a system past its expected life. Those are checkable. "
         "What is not a reason on its own is the age of the equipment, and a second "
         "opinion costs a service call against a decision that runs into thousands. "
         "Anyone confident in the first answer will not mind you getting it.")},
]
