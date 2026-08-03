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
    return keyed[:n]


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

        {"id": "hx-boiler",
         "h2": "Do you still work on boilers and radiators?",
         "body": (
             "Yes, and there are more of them around here than people assume, "
             "particularly in the older housing stock closer to the river and in the "
             "pre-war neighbourhoods. A boiler is a different service call from a "
             "furnace: circulator pumps, expansion tanks, air in the loop and zone "
             "valves rather than blowers and burners. If your house has radiators and "
             "someone has quoted you for duct cleaning, that is a fair reason to get a "
             "second opinion, because there are no ducts to clean.")},

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
             "rises, so a two-storey house on one system fights that all summer. Before "
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
