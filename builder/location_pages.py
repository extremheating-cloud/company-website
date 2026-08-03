"""Location pages — design_handoff_location_pages (screens 5h, 5a-5g).

One template, 38 cities, 267 pages. Copy is verbatim from the mockup; the only
things that vary per city are the name, the metro, the neighbor-town list and the
hero photo. Everything else is shared, which is exactly how the handoff asks for it
("Build as a template, not 40 pages").

  5h  /locations                          hub
  5a  /locations/{city}                    overview
  5b-5g  /locations/{city}/{service}       six service pages

THE RULE THAT GOVERNS THESE PAGES: they are service areas, not storefronts. No
street address, no "get directions", no address schema — anywhere. The two real
offices live on /contact and stay there.
"""
import os
import template as T
import locations as L
import site_data as D
from company_pages import section, shell, slot_img

PHONE = T.PHONE_DISPLAY
METRO_BLURB = {
    "Dayton": "Dayton and the Miami Valley",
    "Cincinnati": "Cincinnati and the surrounding metro",
    "Counties": "southwest Ohio",
}

# ---------------------------------------------------------------- CSS
LOC_CSS = """
/* --------------------------- location pages (5a-5h) --------------------------- */
.xlc-grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}
.xlc-card{position:relative;border:1px solid var(--rule);border-radius:16px;padding:20px;
background:#fff;text-decoration:none;display:block;transition:box-shadow .15s ease,transform .15s ease}
.xlc-card:hover{box-shadow:0 12px 30px rgba(84,39,112,.12);transform:translateY(-2px)}
.xlc-card .t{font-weight:800;font-size:16.5px;color:var(--ink)}
.xlc-card .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:6px}
.xlc-card .lm{display:inline-block;margin-top:14px;font-weight:800;font-size:13.5px;color:var(--purple)}
.xlc-card:hover .lm{color:var(--green-dark)}
.xlc-new{position:absolute;top:14px;right:14px;background:var(--green);color:var(--ink);
font-size:10px;font-weight:800;letter-spacing:1.2px;border-radius:999px;padding:4px 9px}
.xlc-towns{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 24px;margin-top:20px}
.xlc-town{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--body)}
.xlc-town .c{width:18px;height:18px;flex:none;border-radius:50%;background:#3F852B;color:#fff;
font-size:10px;font-weight:800;display:grid;place-items:center}
.xlc-town a{color:var(--body);text-decoration:none}
.xlc-town a:hover{color:var(--purple)}
.xlc-note{font-size:13px;font-weight:600;color:var(--muted);margin-top:16px}
/* Descriptive cross-links out of a city page. Navigation, not a page section, so it
   takes an eyebrow and no H2 — the indexed hubs already run seven of those. */
.xlc-rel{margin-top:8px}
.xlc-rellinks{display:flex;flex-wrap:wrap;gap:8px 10px;margin-top:12px}
.xlc-rellinks a{display:inline-flex;align-items:center;min-height:36px;border:1px solid var(--rule);
border-radius:999px;padding:8px 15px;font-size:13.5px;font-weight:700;color:var(--body);
text-decoration:none;background:#fff}
.xlc-rellinks a:hover{color:var(--purple);border-color:var(--purple)}
.xlc-revs{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}
.xlc-rev{border:1px solid var(--rule);border-radius:16px;padding:20px;background:#fff}
.xlc-rev .stars{color:var(--stars);font-size:14px;letter-spacing:2px}
.xlc-rev .q{font-size:14px;line-height:1.6;font-weight:500;color:var(--body);margin-top:10px}
.xlc-rev .who{font-size:12.5px;font-weight:700;color:var(--ink);margin-top:14px}
.xlc-rev .who span{color:var(--muted);font-weight:600}
.xlc-dir{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-top:20px}
.xlc-dircol .lab{font-size:10.5px;font-weight:800;letter-spacing:1.6px;color:var(--purple);
padding-bottom:10px;border-bottom:1px solid var(--rule)}
.xlc-links{display:grid;grid-template-columns:repeat(2,1fr);gap:8px 16px;margin-top:14px}
.xlc-links a{font-size:13.5px;font-weight:600;color:var(--body);text-decoration:none}
.xlc-links a:hover{color:var(--purple)}
.xlc-metro{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff;
margin-top:20px}
/* Atlist embed. It sizes itself internally, so the wrapper owns the height and the
   iframe fills it — the same treatment the previous hub used. */
.xlc-map{width:100%;height:clamp(420px,55vw,640px);overflow:hidden;background:#F4F6F8;
border-bottom:1px solid var(--rule)}
.xlc-map iframe{width:100%!important;height:100%!important;display:block;border:0}
.xlc-metro .body{padding:20px;display:flex;flex-wrap:wrap;align-items:center;
justify-content:space-between;gap:12px 24px}
.xlc-metro .cta{display:inline-flex;align-items:center;justify-content:center;min-height:44px;
background:var(--green);color:var(--ink);font-weight:800;font-size:14px;padding:12px 20px;
border-radius:10px;text-decoration:none;white-space:nowrap}
.xlc-metro .cta:hover{background:var(--green-hover)}
.xlc-metro .eyebrow{font-size:10.5px;font-weight:800;letter-spacing:1.6px;color:var(--purple)}
.xlc-metro .t{font-style:italic;font-weight:900;font-size:22px;letter-spacing:-.4px;
color:var(--ink);margin-top:8px}
.xlc-metro .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:8px}
.xlc-metro .lm{display:inline-block;margin-top:14px;font-weight:800;font-size:13.5px;color:var(--green-dark)}
.xlc-zip{display:flex;gap:8px;margin-top:14px}
.xlc-zip input{flex:1;min-width:0;border:1px solid var(--rule);border-radius:10px;padding:12px 14px;
font-size:16px;font-weight:600;color:var(--ink);font-family:inherit}
.xlc-zip input:focus-visible{outline:3px solid #61BC47;outline-offset:2px}
.xlc-zipmsg{font-size:12.5px;font-weight:600;margin-top:10px;min-height:18px}
.xlc-zipmsg.ok{color:var(--promo-green)} .xlc-zipmsg.no{color:var(--body)}
.xlc-xp{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;
padding:32px 36px;color:#fff;margin-top:20px}
.xlc-xp .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--green-hover)}
.xlc-xp h3{margin-top:10px;font-style:italic;font-weight:900;font-size:26px;letter-spacing:-.5px}
.xlc-xp ul{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 24px}
.xlc-xp li{display:flex;gap:10px;font-size:14px;font-weight:600;color:rgba(255,255,255,.9)}
.xlc-xp li .c{width:18px;height:18px;flex:none;border-radius:50%;background:var(--green);
color:var(--ink);font-size:10px;font-weight:800;display:grid;place-items:center}
.xlc-xp .cta{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:15px;padding:13px 24px;border-radius:12px;min-height:44px;
text-decoration:none;margin-top:22px}
.xlc-xp .cta:hover{background:var(--green-hover)}
.xlc-xp .fine{font-size:11.5px;font-weight:600;color:rgba(255,255,255,.6);margin-top:12px}
/* --- page-specific ink CTA band (handoff: ink #0F172A band + 4px green-to-purple
   hairline). These pages emit .xsp-band, which had no styles at all — the markup was
   rendering unformatted. --- */
.xsp-band{background:var(--ink)}
.xsp-band-in{max-width:1280px;margin:0 auto;padding:34px 40px;display:flex;align-items:center;
justify-content:space-between;gap:18px 32px;flex-wrap:wrap}
.xsp-band .t{font-style:italic;font-weight:900;font-size:26px;letter-spacing:-.5px;color:#fff}
.xsp-band .d{font-size:14px;line-height:1.6;font-weight:500;color:rgba(255,255,255,.72);
margin-top:8px;max-width:64ch}
.xsp-band .btns{flex:none;display:flex;gap:10px}
.xsp-band .xsp-cta{white-space:nowrap}
.xsp-band::after{content:"";display:block;height:4px;
background:linear-gradient(90deg,var(--green),var(--purple))}

/* The overhanging booking card and the body clearance it needs now live in
   template.py / company_pages.py, so every page type gets the same treatment. */

@media (max-width:809px){
/* The hub's hero card is the town finder, not a booking CTA. .xsp-bookcol is
   display:none on a phone, which left /locations with no search box at all — the
   only input on the page. Show it inline instead, the way /maintenance keeps its
   pricing card, and drop the overhang since nothing is overhanging on mobile. */
.xsp-bookcol.zip{display:block;margin:24px 0 0}
.xsp-band-in{padding:26px 20px;flex-direction:column;align-items:flex-start;gap:16px}
.xsp-band .t{font-size:21px}
.xsp-band .btns{width:100%}
.xsp-band .xsp-cta{width:100%}
}
/* The NEW pill belongs to the headline, not the breadcrumb. Sitting flush under the
   crumbs it read as another nav item; the spacing now groups it with the H1 below. */
.xlc-pill{display:inline-block;background:var(--green);color:var(--ink);font-size:11px;
font-weight:800;letter-spacing:1.4px;border-radius:999px;padding:6px 12px;margin:26px 0 0}
.xlc-pill + .xsp-h1{margin-top:10px}
@media (max-width:809px){
.xlc-grid3,.xlc-revs{grid-template-columns:1fr;gap:12px}
.xlc-map{height:auto}
.xlc-map iframe{height:575px!important}
.xlc-towns,.xlc-dir,.xlc-xp ul{grid-template-columns:1fr;gap:10px}
.xlc-links{grid-template-columns:1fr 1fr}
.xlc-xp{padding:26px 22px;border-radius:20px}
}
"""

# ---------------------------------------------------------------- shared bits
def _stat_panel(stats):
    inner = "".join(f'<div><div class="n">{n}</div><div class="cap">{c}</div></div>'
                    for n, c in stats)
    return (f'<div class="xco-stats"><img class="mark" src="{T.X_MARK}" alt=""'
            f'{T.dim_attrs(T.X_MARK)} loading="lazy" decoding="async" '
            f'style="position:absolute;right:-70px;bottom:-60px;width:300px;opacity:.06;'
            f'transform:rotate(-8deg);filter:brightness(0) invert(1)">'
            f'<div class="grid">{inner}</div></div>')

def _band(title, sub, cta="call"):
    """Ink CTA band. `cta` is "call" or "schedule" per the handoff's per-page note."""
    btn = (T.schedule_btn("Schedule Service", "xsp-cta") if cta == "schedule"
           else f'<a class="xsp-cta" href="{T.PHONE_TEL}">Call {PHONE}</a>')
    return f'''<div class="xsp-band"><div class="xsp-band-in">
  <div><div class="t">{title}</div><div class="d">{sub}</div></div>
  <div class="btns">{btn}</div>
</div></div>'''

def _hero(city, crumbs, h1, hi, intro, chips, card, pill="", card_class="", ctas=True,
          answer=None):
    """ctas=False is for the hub, whose card is a search tool rather than a booking
    CTA and stays on screen at every width instead of handing off to a button pair.

    `answer` is the answer-first block. It renders as the first element after the H1,
    ahead of the intro, because that is the passage an engine lifts and because
    id="answer" is what speakable schema targets."""
    pill_html = f'<div class="xlc-pill">{pill}</div>' if pill else ""
    answer_html = T.answer_block({"answer": answer}) if answer else ""
    # The booking card is display:none under 810px, so without this pair a phone gets
    # a hero with no way to book — which is what all 267 location pages used to do.
    cta_html = f'''<div class="xsp-hero-ctas xsp-mb">
        {T.schedule_btn("Schedule Service", "xsp-cta")}
        <a class="xsp-cta-outline" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
      </div>''' if ctas else ""
    return f'''<div class="xsp-hero">
  {T.hero_mark()}
  <div class="xsp-hero-grid">
    <div>
      {T.crumbs(crumbs)}
      {pill_html}
      {T.h1(h1, hi)}
      {answer_html}
      <p class="xsp-intro">{intro}</p>
      {cta_html}
      {T.chips(chips)}
    </div>
    <div class="xsp-bookcol{" " + card_class if card_class else ""}">{card}</div>
  </div>
</div>'''

def _book(eyebrow, title, sub, label="Schedule Service", trust2="Local techs"):
    return T.booking_card({"eyebrow": eyebrow, "title": title, "sub": sub, "trust2": trust2},
                          schedule_label=label)

def _cards(eyebrow, h2, items, lead=None):
    """Service / capability card grid. items: (title, desc, href|None, pill|None).

    `lead` is the direct answer to an interrogative H2. Every question heading has to
    be followed by prose before a grid or a list, or the heading is a label rather than
    a question anything can quote."""
    out = []
    for t, d, href, pill in items:
        tag = f'<a class="xlc-card" href="{href}">' if href else '<div class="xlc-card">'
        end = "</a>" if href else "</div>"
        lm = f'<span class="lm">{pill[1]}</span>' if pill and len(pill) > 1 and pill[1] else ""
        new = '<span class="xlc-new">NEW</span>' if pill and pill[0] == "NEW" else ""
        out.append(f'{tag}{new}<div class="t">{t}</div><div class="d">{d}</div>{lm}{end}')
    inner = (T.paragraphs(lead) if lead else "") + f'<div class="xlc-grid3">{"".join(out)}</div>'
    return section(eyebrow, h2, inner)

def _checklist(eyebrow, h2, items, note=None):
    inner = "".join(f'<div class="xsp-check"><span class="c">✓</span>{i}</div>' for i in items)
    body = f'<div class="xsp-checks">{inner}</div>'
    if note:
        body += f'<div class="xlc-note">{note}</div>'
    return section(eyebrow, h2, body)

# ---------------------------------------------------------------- copy deck
# Verbatim from the mockup. {CITY} is the only substitution.
SERVICE_COPY = {
"heating": dict(
  nav="Heating", h1="{CITY} heating help, {X}", hi="extremely fast",
  intro="Furnace repair, replacement, and heat pumps from techs who've worked every kind of "
        "{METRO_ADJ} home — with a 24/7 line for the January no-heat call.",
  chips=["24/7 No-Heat Line", "Upfront Pricing", "All Makes &amp; Models"],
  bookEyebrow="{CITYU} HEATING",
  gridEyebrow="WHAT WE HANDLE", gridH2="Every way a {CITY} home stays warm.",
  cards=[("Furnace repair","Any brand, any age — diagnosed and quoted upfront before work begins."),
         ("Furnace installation","High-efficiency replacements sized to your home, not a sales quota."),
         ("Heat pumps","Heating and cooling in one system — great fit for Ohio's swing seasons."),
         ("Boilers &amp; radiators","Older {CITY} homes included — we know the quirks."),
         ("Heating tune-ups","Seasonal inspection and safety check — free twice a year on X-Plan."),
         ("Smart thermostats","Installed and configured so the schedule actually saves you money.")],
  sec2="decision",
  decEyebrow="REPAIR OR REPLACE?", decH2="We'll tell you the honest answer.",
  dec=[("Usually worth repairing","Under ~12 years old · single failed part · repair well under a "
        "third of replacement cost · heats evenly otherwise."),
       ("Usually worth replacing","15+ years with repeat repairs · cracked heat exchanger · bills "
        "creeping up · financing spreads the cost monthly.")],
  decNote="Either way you get a flat quote first — and a free second opinion on any replacement diagnosis.",
  promos=["locFinanceHeat","locXplan"],
  bandT="No heat tonight?", bandS="Don't wait it out with space heaters — the emergency line is answered 24/7.",
  photo="service/furnace-service.jpg", photoPos="50% 45%",
  photoAlt="A Trane furnace in a basement with its control panel open for service"),

"cooling": dict(
  nav="Cooling", h1="Keep your cool, {X}", hi="{CITY}",
  intro="AC repair, replacement, and ductless systems for humid Ohio summers — fixed right the "
        "first time, at a price you approve before we start.",
  chips=["90% Same-Day Service", "Upfront Pricing", "All Makes &amp; Models"],
  bookEyebrow="{CITYU} COOLING",
  gridEyebrow="WHAT WE HANDLE", gridH2="Every way a {CITY} home stays cool.",
  cards=[("AC repair","From weak airflow to total shutdowns — diagnosed and quoted upfront."),
         ("AC installation &amp; replacement","High-efficiency systems sized to your square footage and ductwork."),
         # No rebate claim: Extreme is not a registered utility trade ally, so "rebates
         # often available" is a promise the company cannot keep at the counter.
         ("Heat pumps","One system for summer and winter — sized for Ohio's swing seasons."),
         ("Ductless mini-splits","Room-by-room comfort for additions, sunrooms, and older homes."),
         ("AC tune-ups","Coils, refrigerant, and airflow checked before the first hot week."),
         ("Smart thermostats","Installed and configured so the schedule actually saves you money.")],
  sec2="checks",
  chkEyebrow="SIGNS IT'S STRUGGLING", chkH2="Call before it quits in July.",
  checks=["Warm air coming from the vents","Ice on the refrigerant lines",
          "Starts and stops every few minutes","House feels sticky even when cool",
          "Cooling bills creeping up","System is 15+ years old"],
  chkNote="Catching these early usually means a repair instead of a replacement.",
  promos=["locFinanceCool","locXplan"],
  bandT="AC quit during a heat wave?", bandS="The emergency line is answered 24/7 — nights, weekends, holidays.",
  photo="equipment/ruud-condenser.jpg", photoPos="50% 45%",
  photoAlt="A Ruud air conditioner installed beside a brick home"),

"plumbing": dict(
  nav="Plumbing", h1="Plumbing has come to {X}", hi="{CITY}", pill="NEW IN {CITYU}",
  intro="The same team you trust with your furnace now handles water heaters, drains, leaks, and "
        "sump pumps — with the same upfront pricing.",
  chips=["Licensed Plumbers", "Upfront Pricing", "90% Same-Day Service"],
  bookEyebrow="{CITYU} PLUMBING",
  gridEyebrow="WHAT WE HANDLE", gridH2="From the water heater to the sewer line.",
  cards=[("Water heaters","Repair and replacement, tank and tankless — same-day swaps in most cases."),
         ("Drain clearing","Cleared properly — with a camera check if the clog keeps coming back."),
         ("Leak repair","Found and fixed before it becomes a drywall and flooring problem."),
         ("Sump pumps","Repair, replacement, and battery backups before the spring storms."),
         ("Toilets &amp; fixtures","Running toilets, dripping faucets, and full fixture upgrades."),
         ("Sewer lines","Camera inspections, spot repairs, and full replacements — quoted upfront.")],
  sec2="purple",
  purpleEyebrow="NEW IN {CITYU}", purpleH2="Same trucks. Same standards. Now with pipes.",
  purple=[("Licensed","and insured plumbers on every job."),
          ("Same-day","water-heater swaps in most cases."),
          ("On camera","drain and sewer work you can see for yourself.")],
  promos=["locFinanceTankless","locXplanPlumb"],
  bandT="Water where it shouldn't be?", bandS="Shut off the main, then call — the emergency line is answered 24/7.",
  photo="equipment/ge-water-heater-install.jpg",
  photoAlt="A newly installed water heater connected in a basement"),

"maintenance": dict(
  # The {X} slot is the city token on every other service. Putting a slogan there
  # ("breakdowns away") gave all 38 maintenance pages the same H1 — with duct-cleaning
  # below, that was 76 pages sharing two headings. The slogan moves into the sentence
  # and the city goes back in the highlight.
  nav="Maintenance", h1="Tune-ups that keep breakdowns out of {X}", hi="{CITY}",
  intro="Seasonal furnace and AC maintenance for {CITY} homes — done right, documented for your "
        "warranty, and automatic if you're on the X-Plan.",
  chips=["Two Seasons, Two Tune-Ups", "Warranty-Valid Reports", "X-Plan Member Perks"],
  bookEyebrow="{CITYU} MAINTENANCE", bookTitle="Book before the season turns.",
  bookSub="Spring for cooling, fall for heating — spots fill fast at the season change.",
  bookLabel="Schedule a Tune-Up",
  sec1="checks",
  chkEyebrow="WHAT A TUNE-UP COVERS", chkH2="Not a once-over. A real inspection.",
  checks=["Burners &amp; heat exchanger inspection","Refrigerant &amp; coil check",
          "Electrical connections tightened","Blower &amp; motor performance",
          "Safety controls &amp; CO check","Thermostat calibration",
          "Filter check &amp; replacement guidance","Written report with photos"],
  sec2="xplan",
  promos=["locSpecialTuneUp","locFinanceAging"],
  bandT="Been a few years since a tune-up?",
  bandS="No judgment — a catch-up visit now beats a breakdown in January.", bandCta="schedule",
  photo="service/ac-contactor.jpg", photoPos="50% 45%",
  photoAlt="A worn, cobwebbed contactor found inside an air conditioner during service"),

"duct-cleaning": dict(
  # Same fix as maintenance above: "cleaner air" was a slogan sitting in the city slot.
  nav="Duct Cleaning", h1="Cleaner ducts, cleaner air in {X}", hi="{CITY}",
  intro="Whole-home duct cleaning with negative-pressure equipment — and before/after photos so "
        "you can see exactly what you paid for.",
  chips=["Before/After Proof", "Negative-Pressure Equipment", "Dryer Vents Too"],
  bookEyebrow="{CITYU} DUCT CLEANING", bookTitle="Most homes: one visit.",
  gridEyebrow="WHAT WE CLEAN", gridH2="The whole system — not just the vents you can see.",
  cards=[("Supply &amp; return ducts","The full run, agitated and vacuumed under negative pressure."),
         ("Registers &amp; grilles","Removed, washed, and re-seated — not just wiped around."),
         ("Blower compartment","Where dust cakes up and steals airflow from the whole house."),
         ("Dryer vents","A top cause of house fires — cleared end to end."),
         ("Sanitizing treatment","Optional fogging for odor and microbial growth after cleaning."),
         ("Before/after documentation","Camera photos inside your ducts, before we start and after we finish.")],
  sec2="checks",
  chkEyebrow="WHEN IT'S TIME", chkH2="Six signs your ducts are due.",
  checks=["Dust puffs when the system kicks on","Just finished a renovation",
          "Allergies worse indoors","Musty smell from the vents",
          "Past pest or rodent activity","Never cleaned in 5+ years"],
  chkNote="Not sure? We'll put a camera in first and show you — no cleaning you don't need.",
  promos=["locIaqCross","locXplan"],
  bandT="Not sure your ducts need it?",
  bandS="We'll look first with a camera and tell you straight — cleaning or not.", bandCta="schedule",
  photo="service/before-after-ducts.jpg", photoAlt="Before and after photos of cleaned ductwork"),

"indoor-air-quality": dict(
  nav="Indoor Air Quality", h1="Breathe easier, {X}", hi="{CITY}",
  intro="Filtration, purification, and humidity control for allergy season, dry winters, and "
        "everything the {METRO_ADJ} air brings inside.",
  chips=["Whole-Home Solutions", "Honest Recommendations", "Installed by Licensed Techs"],
  bookEyebrow="{CITYU} AIR QUALITY", bookTitle="Start with an assessment.",
  bookSub="We test first, then recommend — never the other way around.",
  gridEyebrow="SOLUTIONS", gridH2="Matched to your air, not a catalog.",
  cards=[("Whole-home media filters","Deep-media filtration that replaces the flimsy 1-inch filter."),
         ("Air purifiers &amp; UV lights","Neutralize allergens, odors, and microbial growth at the source."),
         ("Whole-home humidifiers","End static shocks, dry skin, and cracking trim in Ohio winters."),
         ("Dehumidifiers","Tame sticky summers and musty basements before mold moves in."),
         ("Fresh-air ventilation","ERVs bring filtered outdoor air in — without losing your heating or cooling."),
         ("IAQ testing &amp; monitors","Know what's actually in your air before spending a dollar fixing it.")],
  sec2="steps",
  stepsEyebrow="HOW IT WORKS", stepsH2="Test. Recommend. Install. Verify.",
  steps=[("Assess your air","Humidity, particulates, and ventilation measured room by room."),
         ("Recommend the right fix","Sometimes that's a $40 filter upgrade, not a $2,000 purifier — we'll say so."),
         ("Install and verify","Installed by licensed techs, then re-tested so you can see the difference.")],
  promos=["locDuctCross","locXplan"],
  bandT="Allergies worse inside than outside?",
  bandS="That's fixable — start with an air quality assessment.", bandCta="schedule",
  photo="equipment/muv-401h.jpg", photoAlt="Whole-home air purifier installed on a system"),
}

SERVICE_ORDER = ["heating", "cooling", "plumbing", "maintenance", "duct-cleaning", "indoor-air-quality"]

OVERVIEW_CARDS = [
    ("heating", "Heating", "Furnace repair, installs, heat pumps, and no-heat emergencies."),
    ("cooling", "Cooling", "AC repair, replacement, ductless, and seasonal tune-ups."),
    ("plumbing", "Plumbing", "Water heaters, drains, leaks, sump pumps — now in {CITY}."),
    ("maintenance", "Maintenance", "Seasonal tune-ups and the X-Plan membership that automates them."),
    ("duct-cleaning", "Duct Cleaning", "Whole-home duct and dryer-vent cleaning, with before/after proof."),
    ("indoor-air-quality", "Indoor Air Quality", "Filtration, purifiers, humidity control, and fresh-air ventilation."),
]

# ================================================================ local copy deck
# copy-locations.md, applied. Everything below is the material that makes the ten
# featured communities genuinely local rather than find-and-replace, and it is the
# mechanical test for indexation: a page that cannot fill these slots is not in
# locations.FEATURED and is not indexed.
#
# Sourcing rules that were applied to every string here:
#   * Nothing is invented. Where the research carried a [NEEDS] the sentence is
#     omitted, not guessed and not shipped with a bracket in it. Each omission is
#     recorded as a `# [NEEDS: ...]` comment beside the copy it belongs to.
#   * No radon mitigation service claim anywhere. The client does not do radon work,
#     so the Troy and Dayton radon hooks in the research are struck entirely rather
#     than softened into "context" — a page that mentions radon at all pulls radon
#     leads. See the summary note.
#   * No rebate or utility trade-ally claim. The utility paragraphs name who supplies
#     what and stop there.
#   * No service-call, dispatch or after-hours rate in any heading, hero or answer
#     block. The X-Plan member fee line stays where it already is, in the benefit
#     list rendered by T.xplan_panel(detail=True), which is a card body.
#   * Street addresses appear only on the three city pages that contain an office.
#
# Shared H2s. Slots 2, 3 and 7 of the seven-H2 hub outline; 3 is built per city from
# locations.OFFICE so the distance is real rather than a promise.
GEO_COVERED_H2 = "What heating, cooling and plumbing work do you do?"
def geo_covered(slug=None):
    """The 'what work do you do' answer, with each service linked.

    It is a list of services, so every item in it should be a way through to that
    service — unlinked, it names six things a reader might want and offers no route
    to any of them. On a city page the links go to that city's own service pages
    rather than the generic ones, which is the whole point of having 228 of them.

    Every city and county slug has all six service pages (38 x 6 = 228), so the
    slug alone is enough to build the URL; without one it falls back to the generic
    pages, which is what the /locations hub wants."""
    def link(text, city_svc, generic):
        href = f"/locations/{slug}/{city_svc}" if slug and city_svc else generic
        return f'<a href="{href}">{text}</a>'
    return (f'{link("Furnaces", "heating", "/furnace-heating")}, '
            f'{link("heat pumps", None, "/heat-pump")} and '
            f'{link("air conditioners", "cooling", "/air-conditioning")}: repair, replacement '
            f'and seasonal tune-ups. '
            f'{link("Duct and dryer-vent cleaning", "duct-cleaning", "/duct-cleaning")}, '
            f'{link("air quality equipment", "indoor-air-quality", "/indoor-air-quality")}, '
            f'and {link("plumbing", "plumbing", "/plumbing/services")} from the water heater '
            f'to the sewer line. Both trades, one number to call.')

# Kept for callers that want the plain sentence with no links.
GEO_COVERED = ("Furnaces, heat pumps and air conditioners: repair, replacement and seasonal "
               "tune-ups. Duct and dryer-vent cleaning, air quality equipment, and plumbing "
               "from the water heater to the sewer line. Both trades, one number to call.")
GEO_SPEED_H2 = "How fast can you get here if the heat is out?"
GEO_BOOK_H2 = "How do I book a visit?"
GEO_BOOK = ("Call " + PHONE + " and you get a person, or book online in about a minute. "
            "If it's no heat, no cooling in a heat wave, or water where it shouldn't be, call "
            "rather than booking. That goes straight to the 24/7 line.")

# The six service H1 patterns for the indexed pages. The noindexed tail keeps the
# branded H1s in SERVICE_COPY, which is part of what makes the two sets distinguishable.
GEO_SERVICE_H1 = {
    "heating": "Furnace repair and heating service in {X}",
    "cooling": "AC repair and air conditioning service in {X}",
    "plumbing": "Plumbers in {X}: repairs, water heaters and drains",
    "maintenance": "HVAC maintenance and tune-ups in {X}",
    "duct-cleaning": "Air duct cleaning in {X}",
    "indoor-air-quality": "Indoor air quality services in {X}",
}

# The shared scaffold headings on an indexed service page. SERVICE_COPY's own H2s are
# decks ("Not a once-over. A real inspection.", "Six signs your ducts are due.") and
# they are identical on all 38 pages of that service. On the ten indexed communities
# they become questions, which is what a heading has to be to get quoted. The tail
# keeps the branded decks, which is one more way the two sets read differently.
GEO_SCAFFOLD_H2 = {
 "heating":            {"gridH2": "What heating work do you handle?",
                        "decH2": "Should I repair my furnace or replace it?",
                        "book": "How do I book heating service in {C}?"},
 "cooling":            {"gridH2": "What cooling work do you handle?",
                        "chkH2": "How do I know my AC is on its way out?",
                        "book": "How do I book AC repair in {C}?"},
 "plumbing":           {"gridH2": "What plumbing work do you handle?",
                        "book": "How do I book a plumber in {C}?"},
 "maintenance":        {"chkH2": "What does a tune-up actually cover?",
                        "book": "How do I book a tune-up in {C}?"},
 "duct-cleaning":      {"gridH2": "What does a duct cleaning visit include?",
                        "chkH2": "How do I know if my ducts need cleaning?",
                        "book": "How do I book duct cleaning in {C}?"},
 "indoor-air-quality": {"gridH2": "What indoor air quality equipment can I get?",
                        "stepsH2": "How do I know it worked?",
                        "book": "How do I book an air quality assessment in {C}?"},
}
GEO_SERVICE_BOOK = ("Call " + PHONE + " and you get a person, or book online in about a "
                    "minute. If it's an emergency, no heat or water on the floor, call rather "
                    "than booking. That skips the next-day queue and goes straight to the 24/7 "
                    "line.")

# Answer-block verbs and scope sentences for the noindexed tail. The city name is the
# only thing that varies, which is the honest position: there is no local research for
# 28 more places and inventing it is worse than omitting it.
TAIL_VERB = {
    "heating": "repair and replace furnaces, heat pumps and boilers",
    "cooling": "repair and replace air conditioners, ductless systems included",
    "plumbing": "handle water heaters, drains, leaks and sewer lines",
    "maintenance": "tune up furnaces and air conditioners every season",
    "duct-cleaning": "clean supply ducts, returns, blower compartments and dryer vents",
    "indoor-air-quality": "install filtration, humidity control and ventilation equipment",
}
TAIL_SCOPE = {
    "heating": "Any brand, any age, diagnosed and quoted before we start.",
    "cooling": "Repairs, replacements and seasonal tune-ups, all priced before we start.",
    "plumbing": "Our plumbers are licensed in Ohio, license #13557.",
    "maintenance": "You get a written report and photos for your warranty records.",
    "duct-cleaning": "A camera goes into your ductwork before we quote anything.",
    "indoor-air-quality": "We measure humidity, particulates and ventilation before "
                          "recommending anything.",
}

LOCAL = {

# ---------------------------------------------------------------- 1. Dayton
"dayton": dict(
 alt="A street of pre-war houses in Dayton, Ohio",
 answer="We cover Dayton out of the Beavercreek office, about eight miles east. Heating, "
        "cooling and plumbing across Montgomery County, including all that pre-1940 "
        "housing. Most get handled the same day, and the emergency line never closes.",
 sections=[
  ("What HVAC problems do pre-1940 Dayton houses have?", [
   "Dayton has the oldest housing in the whole service area. About 38.2% of it was built "
   "before 1940 against a national figure of 13.5%, and the median house went up in 1951.",
   "That shows up on a service call in specific ways. Houses first heated by gravity furnaces "
   "and radiators, then converted to forced air later, usually got trunk lines squeezed into a "
   "basement joist bay that were never sized for the job. Plenty of them have one central "
   "return and nothing upstairs, which is why the second floor never balances no matter what "
   "the thermostat says. Block and stone foundations bring their own condensate and humidity "
   "questions with every equipment change."]),
  ("Which utility supplies water and gas in Dayton?", [
   "The City of Dayton Department of Water pulls from the Great Miami Buried Valley Aquifer "
   "and softens with lime at the plant. Electricity and gas come from two different companies "
   "here, which surprises people who moved from the Cincinnati side: AES Ohio does electric, "
   "CenterPoint Energy Ohio does gas. Two bills, two shut-off procedures."]),
  # [NEEDS: delivered hardness in grains per gallon from the City of Dayton Water Quality
  # Report. Third-party aggregators say 9 to 11 gpg; that range is not published here.]
  ("Who inspects plumbing permits in Dayton?", [
   "The city does, not the county. Public Health, Dayton &amp; Montgomery County runs plumbing "
   "inspection for Montgomery County but explicitly excludes Dayton, Centerville, Oakwood and "
   "Kettering. So a Dayton plumbing permit is a City of Dayton permit, and a contractor who "
   "assumes the county has it is going to the wrong counter."]),
  # [NEEDS: which City of Dayton division issues residential mechanical permits, plus its
  # address and portal.]
 ],
 table=dict(
  caption="Common problems in Dayton, Ohio homes and what to book",
  takeaway="We see the same short list of faults in Dayton's pre-1940 housing, and most of "
           "them trace back to ductwork that got retrofitted into a house built without any.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Upstairs never gets warm or cool", "One central return and no upstairs return path",
    "Heating or cooling assessment", "Book this week"),
   ("Furnace runs but registers barely blow",
    "Undersized trunk line retrofitted into a pre-war house", "Duct evaluation", "Book this week"),
   ("Basement smells musty after a system change",
    "Condensate draining into a block or stone foundation", "Plumbing visit", "Book this week"),
   ("Drain backs up repeatedly on one fixture",
    "Galvanised or cast-iron branch line common in pre-war stock",
    "Drain clearing with a camera check", "Book this week"),
   ("No heat, and the house is dropping", "Ignition, control board or gas valve failure",
    "Emergency heating call", "Call 24/7 now"),
   ("Water standing on the floor", "Supply line, water heater or sewer failure",
    "Emergency plumbing call", "Call 24/7 now"),
  ]),
 faq=[
  ("Do you work in Dayton proper, or only the suburbs?",
   "Dayton proper, not just the suburbs. We cover the whole city from the Beavercreek office, "
   "about eight miles east."),
  ("Can you put central air in a house that has radiators and no ductwork?",
   "Yes, though not with a conventional split system. Without duct runs you are looking at "
   "either a ductless system with wall or ceiling heads, or high-velocity small-duct equipment "
   "that fits through existing framing. Which one suits your house gets decided on site rather "
   "than over the phone."),
  ("My upstairs is always ten degrees off. Is that fixable without new equipment?",
   "Often, yes. In pre-1940 housing the usual cause is return air, not the furnace. Adding a "
   "return path upstairs or rebalancing what is already there fixes a lot of two-story houses "
   "that were about to get a new system they did not need."),
  ("Who do I call for a plumbing permit in the City of Dayton?",
   "The city, not the county. Public Health, Dayton &amp; Montgomery County runs plumbing "
   "inspection for Montgomery County but excludes Dayton, Centerville, Oakwood and Kettering. "
   "We pull the permit as part of the job."),
  ("Do you answer the phone at 2am?",
   "Yes. Someone picks up on " + PHONE + " at any hour, every day of the year — nights, "
   "weekends and holidays included."),
 ],
 links=[("heating and cooling in Kettering", "/locations/kettering"),
        ("the Beavercreek office", "/locations/beavercreek"),
        ("X-Plan maintenance membership", "/maintenance")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces, heat pumps and boilers in Dayton, including the "
          "gravity-furnace conversions and squeezed-in duct runs common in pre-1940 housing. "
          "Most get handled the same day, and we answer the no-heat line at any hour.",
   slots=[("What heating problems come with pre-war Dayton houses?", [
    "About 38.2% of Dayton's housing predates 1940. Many of those houses started on a gravity "
    "furnace with radiators and were converted to forced air later, and the conversion usually "
    "meant squeezing trunk lines into a basement joist bay that was never sized for the job. "
    "Radiator and boiler systems are still in service across the city, and they need a technician "
    "who has worked them rather than one who only knows sealed-combustion furnaces."])],
   faq=("Do you still work on boilers and radiators?",
        "Yes. Dayton has more of them than anywhere else we cover, because 38.2% of its housing "
        "was built before 1940 and the radiators stayed put through later conversions.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Dayton, ductless included. Houses built "
          "before 1940 usually have one central return and nothing pulling from upstairs, which "
          "limits what any AC can do. Most calls get handled the same day.",
   slots=[("Why will a bigger unit not fix a hot upstairs here?", [
    "Because the problem is usually return air rather than capacity. A lot of Dayton's pre-1940 "
    "stock has a single central return and nothing pulling from the second floor. Oversizing the "
    "condenser makes the system short cycle, which cools the thermostat's room faster and "
    "dehumidifies less. Adding a return path, or fitting a ductless head where no duct can reach, "
    "fixes more of these houses than a larger system does."])],
   faq=("My Dayton house has radiators and no ducts. Can I get air conditioning?",
        "Yes, with either a ductless system or high-velocity small-duct equipment routed through "
        "existing framing. A conventional split system needs duct chases that these houses were "
        "never built with.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Dayton. The city runs its "
          "own plumbing inspection, not the county's, so your permit comes from City Hall and "
          "we pull it. We answer the line at any hour.",
   slots=[("What is in Dayton's water supply?", [
    "The City of Dayton Department of Water draws from the Great Miami Buried Valley Aquifer and "
    "softens with lime at the plant. Pre-war houses in the city still have galvanised and "
    "cast-iron branch lines, which is why a drain that keeps clogging in the same spot usually "
    "needs a camera rather than another snake."]),
    # [NEEDS: delivered hardness from the City of Dayton Water Quality Report.]
    ("Who inspects plumbing work in Dayton?", [
    "The city. Public Health, Dayton &amp; Montgomery County runs plumbing inspection for the "
    "county but excludes Dayton, Centerville, Oakwood and Kettering. So your permit comes from "
    "the city, and we pull it as part of the job."])],
   faq=("The same drain clogs every few months. Why?",
        "In Dayton's pre-war housing that pattern usually means a galvanised or cast-iron branch "
        "line that has corroded down to a narrow channel. A camera inspection shows it in a few "
        "minutes and turns a recurring call into one repair.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners for Dayton homes twice a year. Older "
          "equipment in the city's pre-1940 housing gets the most out of a documented safety "
          "and performance check. X-Plan covers both visits for $249 a year.",
   slots=[("Why does maintenance matter more in older housing?", [
    "Because the failure modes are different. Equipment fighting undersized retrofitted ductwork "
    "runs hotter and longer than equipment in a house built around it, and heat exchangers in "
    "older gas furnaces are the single component nobody wants to find cracked in January. A "
    "seasonal safety check catches that during a visit rather than during a cold snap."])],
   faq=("Is a tune-up worth it on a 20-year-old Dayton furnace?",
        "Yes, mostly for the safety check. On equipment that old the visit is as much about the "
        "heat exchanger and the carbon monoxide reading as it is about efficiency, and it gives an "
        "honest read on how much life is left.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Dayton. Duct "
          "runs retrofitted into pre-1940 houses collect more than purpose-built ones, so a "
          "camera goes in before we quote. You get photos from before and after.",
   slots=[("What does the camera usually find in a Dayton house?", [
    "Retrofitted trunk lines threaded through basement joist bays, panned joist returns that were "
    "never sealed, and decades of construction dust from conversions and renovations. Older houses "
    "that have been through several owners and several remodels accumulate more than newer ones, "
    "which is why the camera goes in before the quote rather than after."])],
   faq=("My house is from the 1920s and has never had the ducts cleaned. Where do you start?",
        "With the camera. In housing that old the ductwork is usually a later addition, and the "
        "footage decides whether cleaning is worth doing or whether the runs need repair first.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation equipment in Dayton homes. "
          "A pre-1940 house with one central return cannot carry a dense filter, so we measure "
          "airflow, humidity and particulates before recommending anything.",
   # The research offered a Montgomery County radon average here. Struck: Extreme does not
   # perform radon mitigation, and a radon paragraph on an IAQ page produces radon leads.
   slots=[("What can a pre-war Dayton house actually carry?", [
    "Less filter than people expect, and more humidity control than they think. A house with one "
    "central return and retrofitted trunk lines is already running at higher static pressure than "
    "modern equipment likes, so a dense one-inch filter starves the blower and the symptoms look "
    "like a failing system. Airflow first, filtration second. Full basements with block or stone "
    "walls are usually the bigger win, and that is a dehumidification question."])],
   faq=("My filter made the house feel worse. Why?",
        "Almost certainly airflow. In Dayton's older housing a dense filter on a single undersized "
        "return restricts the blower. Measuring static pressure identifies it in one visit and "
        "decides which filter the house can carry.")),
 }),

# ---------------------------------------------------------------- 2. Cincinnati
"cincinnati": dict(
 alt="Hillside houses above the Ohio River in Cincinnati, Ohio",
 answer="We cover Cincinnati out of the Mason office, roughly 22 miles north of downtown. "
        "Heating, cooling and plumbing across Hamilton County, radiator houses with no ductwork "
        "included. Most get handled the same day, and the emergency line never closes.",
 sections=[
  ("Why do so many Cincinnati houses have no ductwork?", [
   "Because they were built for radiators. Roughly 40% of Cincinnati's housing predates 1939, and "
   "downtown runs older still. Steam and hot-water radiator systems were the standard, and a house "
   "heated that way has no duct chases at all. Adding cooling to one means either ductless heads or "
   "high-velocity small-duct equipment, and any contractor who quotes a conventional split system "
   "for a radiator house without walking it has not looked.",
   "Cincinnati's basin-and-hillside geography adds the second half of the story: walk-out "
   "foundations, tuck-under garages, and equipment sitting in a crawl space on the low side, where "
   "drainage and combustion air are a recurring problem rather than an occasional one."]),
  ("Does Cincinnati's climate change how a system is sized?", [
   "Yes, and this is the one place we work where it does. Hamilton County sits in IECC climate "
   "zone 4A, mixed-humid, while everything else we cover is zone 5A, cold. Cincinnati averages "
   "5,364 heating degree days on the NOAA 1991 to 2020 normals. A heat pump balance point or a "
   "furnace size that is right for a house in Mason is not automatically right for the same "
   "house 20 minutes south."]),
  # [VERIFY: the 4A designation mirrors the IECC 2012/2009 county table. Confirm against the
  # edition of the Residential Code of Ohio in force before the next content review.]
  ("Do I need a permit to replace a furnace in Cincinnati?", [
   "Yes, and this catches people out. The City of Cincinnati Department of Buildings &amp; "
   "Inspections requires a permit for new and replacement units, plus furnace add-ons, "
   "pre-fabricated fireplaces, wood stoves, metal chimney alterations and duct rework. Work has to "
   "comply with the Cincinnati Zoning Code, the Residential Code of Ohio and the Ohio Mechanical "
   "Code. The permit center is at 805 Central Ave, Suite 500. A quote that comes in noticeably low "
   "is worth a second look for exactly this reason."]),
 ],
 table=dict(
  caption="Common problems in Cincinnati, Ohio homes and what to book",
  takeaway="Most Cincinnati comfort complaints we get called out to trace back to one of three "
           "things: a house with no ducts, a hillside foundation, or equipment installed "
           "without a permit.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Radiators heat fine but there is no way to cool", "House built without duct chases",
    "Ductless or high-velocity assessment", "Plan ahead"),
   ("One radiator stays cold", "Air or sediment in a hot-water or steam loop",
    "Heating repair", "Book this week"),
   ("Furnace in a crawl space keeps shutting down",
    "Combustion air or condensate drainage on a hillside foundation", "Heating repair",
    "Book within days"),
   ("Musty smell in a tuck-under or walk-out level",
    "Standing water against a partially buried wall", "Plumbing and IAQ visit", "Book this week"),
   ("Previous install has no permit record",
    "Work done without a City of Cincinnati mechanical permit", "System inspection", "Plan ahead"),
   ("No heat overnight", "Ignition, control or gas supply failure", "Emergency heating call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Can I get air conditioning in a Cincinnati house with radiators and no ducts?",
   "Yes. Houses without ductwork take either a ductless system with individual heads or "
   "high-velocity small-duct equipment routed through existing framing. Both are common in "
   "Cincinnati's pre-1939 housing, which is roughly 40% of the city's stock."),
  ("Do I need a permit just to replace my furnace in Cincinnati?",
   "Yes. The City of Cincinnati Department of Buildings &amp; Inspections requires a mechanical "
   "permit for replacement units as well as new ones. We pull it as part of the job."),
  ("Is Cincinnati's climate different enough to change equipment sizing?",
   "Yes. Hamilton County sits in IECC climate zone 4A while the rest of our service area sits in "
   "zone 5A, and the city averages 5,364 heating degree days. The same house plan can want a "
   "different furnace size on either side of that line."),
  ("How hard is Cincinnati water?",
   "Greater Cincinnati Water Works reports about 125 mg/L at the Richard Miller plant and about "
   "138 mg/L at the Charles M. Bolton plant, which is roughly 7 to 8 grains per gallon. That is "
   "moderately hard and noticeably softer than the untreated groundwater north of the city."),
  ("How far is the nearest office?",
   "About 22 miles. We dispatch Cincinnati work from the Mason office, just north of the city."),
 ],
 links=[("the Mason office", "/locations/mason"),
        ("HVAC in West Chester Township", "/locations/west-chester"),
        ("heat pump systems", "/heat-pump")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces, boilers and heat pumps in Cincinnati. Roughly 40% of "
          "the city's housing predates 1939, and a lot of it still runs on steam or hot-water "
          "radiators. We answer the no-heat line at any hour.",
   slots=[("Does Cincinnati's climate zone change the furnace size?", [
    "It can. Hamilton County sits in IECC climate zone 4A while the rest of the service area sits "
    "in 5A, and Cincinnati averages 5,364 heating degree days on the NOAA 1991 to 2020 normals. A "
    "load calculation done for a house 30 miles north can oversize the equipment here, and an "
    "oversized furnace short cycles, wears faster and heats less evenly than a correctly sized one."])],
   faq=("My radiators are original. Is replacing them the only option?",
        "No. Steam and hot-water systems can be repaired and rebalanced, and in Cincinnati's "
        "pre-1939 housing they often outlast the boiler feeding them. Replacement becomes the "
        "conversation when the boiler is finished, not when a radiator is cold.")),
  "cooling": dict(
   answer="We repair and install air conditioning in Cincinnati, including ductless and "
          "high-velocity systems for houses with no ductwork. That covers equipment stuck in "
          "hillside crawl spaces and walk-out basements. Most calls get handled the same day.",
   slots=[("How do you cool a house that has no ducts?", [
    "Two ways. Ductless systems put an outdoor unit on one or more indoor heads, room by room, "
    "with no duct runs at all. High-velocity small-duct equipment uses flexible two-inch tubing "
    "that threads through existing framing, so the plaster mostly stays where it is. Which one fits "
    "depends on the layout, the ceiling heights and where an air handler can physically go, and "
    "that gets decided on site."])],
   faq=("My AC sits in a crawl space on the low side of the hill. Is that a problem?",
        "It is a common one in Cincinnati. Hillside foundations put equipment below grade where "
        "condensate drainage and combustion air are harder, and standing water around the unit "
        "shortens its life. It is fixable, and worth fixing before the equipment is.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Cincinnati. Greater "
          "Cincinnati Water Works supplies the city at roughly 7 to 8 grains per gallon, which is "
          "moderately hard. We answer the plumbing emergency line at any hour.",
   slots=[("How hard is Cincinnati's water?", [
    "Greater Cincinnati Water Works reports about 125 mg/L at the Richard Miller plant and about "
    "138 mg/L at the Charles M. Bolton plant, roughly 7 to 8 grains per gallon. That is softer than "
    "the untreated groundwater north of the city and soft enough that many Cincinnati houses run "
    "fine without a softener. It is not soft enough to ignore, and water heater scale still shows "
    "up on a ten-year-old tank."]),
    ("Who issues plumbing permits in Cincinnati?", [
    "The City of Cincinnati Department of Buildings &amp; Inspections, from the permit center at "
    "805 Central Ave, Suite 500. Work has to comply with the Cincinnati Zoning Code and the "
    "Residential Code of Ohio."])],
   faq=("My basement is a walk-out and it floods in heavy rain. Is that a plumbing job?",
        "Sometimes. On Cincinnati's hillside lots the usual causes are a failed or undersized sump "
        "pump, no battery backup, or drainage running toward a partially buried wall. A sump pump "
        "assessment answers it, and it is a cheaper visit than a finished basement.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners for Cincinnati homes, boilers and radiator "
          "systems included, along with equipment tucked into hillside crawl spaces. X-Plan "
          "covers two visits a year for $249.",
   slots=[("Do boilers need a different kind of tune-up?", [
    "Yes. A boiler service checks combustion, pressure, the expansion tank, the circulator and the "
    "relief valve, none of which exist on a forced-air furnace. In Cincinnati that matters more "
    "than anywhere else we work, because roughly 40% of the housing predates 1939 and a large "
    "share of it is still hydronic."])],
   faq=("Does a maintenance visit include the permit paperwork?",
        "No permit is needed for a tune-up. Permits come in on installation and replacement work, "
        "and the City of Cincinnati requires one for replacements as well as new units.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Cincinnati. "
          "Plenty of the city's older housing has no ductwork at all, so a camera goes in before "
          "anyone quotes you. You get photos from before and after.",
   slots=[("What if my Cincinnati house has no ducts to clean?", [
    "Then there is nothing to clean and nobody should be selling it. Radiator houses have no duct "
    "runs, and a house cooled by ductless heads has no trunk lines either. In those houses the air "
    "quality conversation is about filtration at the head, ventilation and humidity instead. Where "
    "ducts do exist in older Cincinnati housing they are usually a later retrofit, and the camera "
    "decides whether cleaning is worth doing."])],
   faq=("Someone quoted me for duct cleaning and my house has radiators. Should I be suspicious?",
        "Yes. A radiator house has no ductwork to clean. Ask to see the camera footage before "
        "agreeing to anything, on any house.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Cincinnati. A radiator "
          "house with no central duct path needs different equipment from a forced-air one, so "
          "we measure humidity, particulates and ventilation before recommending anything.",
   slots=[("How do you filter air in a house with no ductwork?", [
    "Not with a whole-home media filter, because there is no duct to put it in. In Cincinnati's "
    "radiator housing the options are filtration built into ductless heads, standalone units sized "
    "per room, and a ducted energy recovery ventilator run independently of the heating system for "
    "fresh air. Humidity is usually the bigger win in these houses, because a hillside basement and "
    "a hot-water system produce very different moisture behavior from a forced-air ranch."])],
   faq=("My hillside basement smells musty every summer. What fixes that?",
        "Usually dehumidification plus drainage, not filtration. Cincinnati's walk-out and partially "
        "buried foundations hold moisture against the wall, and a whole-home dehumidifier addresses "
        "the air while the drainage question gets answered separately.")),
 }),

# ---------------------------------------------------------------- 3. Beavercreek
"beavercreek": dict(
 alt="A residential street in Beavercreek, Ohio",
 # [NEEDS: confirm whether cities/beavercreek.jpg shows the office on N Fairfield Rd. If it
 # does, the alt becomes "The Extreme Heating, Air, Plumbing office on N Fairfield Rd in
 # Beavercreek, Ohio". Until confirmed the alt describes what can be verified.]
 answer="We work out of 712 N Fairfield Rd, right here in Beavercreek, covering Greene County "
        "for heating, cooling, air quality and plumbing. Most calls get handled the same day, "
        "and someone answers the emergency line at any hour.",
 sections=[
  ("What did the 2025 water change do to my softener?", [
   "Greene County Sanitary Engineering finished a $46 million expansion of the regional treatment "
   "plant in Beavercreek Township, adding a membrane and reverse-osmosis softening facility of "
   "roughly 20,000 square feet. The changeover ran January to March 2025 and took delivered "
   "hardness from 27 grains per gallon to about 8, for 18,092 accounts.",
   "If a house has a whole-home softener, it is almost certainly still set for 27 grain water. Left "
   "alone it over-softens, burns through salt, and pushes very low hardness water through the "
   "plumbing. Resetting it takes one visit."]),
  ("Does the softer water reach every address in Greene County?", [
   "No, and this is where street-by-street matters. Homes on private wells inside the same footprint "
   "never got the softened water at all, because the change happened at the county plant rather than "
   "in the ground. The county system covers Beavercreek, Beavercreek Township, Xenia Township, parts "
   "of Sugarcreek Township, Cedarville, Wilberforce, Shawnee Hills, and small parts of Kettering and "
   "Centerville. A well household on the same street as a county-supplied household needs different "
   "advice, and anyone giving the same answer to both is guessing."]),
  ("Who issues building permits in Beavercreek?", [
   "Greene County, not the city. The Greene County Department of Building Regulation at 667 "
   "Dayton-Xenia Rd handles residential and commercial permits for every city and village in the "
   "county except Fairborn, Xenia, Bowersville, Clifton, Cedarville and Yellow Springs. Inspections "
   "book through the iWorQ portal up to 3pm the previous working day. So Beavercreek is "
   "county-permitted while Fairborn and Xenia next door are not, which changes the schedule on a "
   "replacement job."]),
 ],
 table=dict(
  caption="Common problems in Beavercreek, Ohio homes and what to book",
  takeaway="Since early 2025, most of the Beavercreek plumbing calls we take come back to one "
           "thing: a softener still tuned for 27 grain water the county no longer delivers.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Water feels slippery and salt use jumped",
    "Softener still set for 27 grain water after the 2025 change", "Softener adjustment",
    "Book this month"),
   ("Water heater short on hot water", "Scale built up under decades of 27 grain water",
    "Water heater service", "Book this week"),
   ("Well household saw no change in hardness",
    "Private wells were excluded from the county softening project",
    "Water treatment assessment", "Plan ahead"),
   ("Fixtures still scaling after the change", "Existing scale does not dissolve on its own",
    "Plumbing visit", "Plan ahead"),
   ("Replacement job stalled waiting on inspection",
    "County inspections book by 3pm the previous working day", "Reschedule through the office",
    "Same week"),
   ("No heat or water on the floor", "Equipment or supply failure", "Emergency call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Where is the Beavercreek office?",
   "712 N Fairfield Rd, Beavercreek, OH 45434. Office staff are in " + D.HOURS_STAFFED_PROSE + ", "
   "5:00 PM, and the emergency line at " + PHONE + " is answered 24/7 every day of the year."),
  ("My water changed in early 2025. Do I still need a softener?",
   "Probably not at the same setting. Greene County Sanitary Engineering took delivered hardness "
   "from 27 grains per gallon to about 8 between January and March 2025. A softener still set for 27 "
   "grain water over-softens and wastes salt. It usually wants adjusting rather than removing."),
  ("I am on a well in Greene County. Did my water get softer too?",
   "No. The softening happened at the county treatment plant, so private wells inside the same area "
   "still draw untreated groundwater. Well households need their own treatment decision."),
  ("Does Beavercreek or Greene County issue my permit?",
   "Greene County. The Greene County Department of Building Regulation covers Beavercreek, along "
   "with every city and village in the county except Fairborn, Xenia, Bowersville, Clifton, "
   "Cedarville and Yellow Springs."),
  ("Do you serve the townships around Beavercreek?",
   "Yes. Beavercreek Township, Xenia Township and Sugarcreek Township are all inside the normal "
   "coverage area, dispatched from the same office on N Fairfield Rd."),
 ],
 links=[("water treatment and softeners", "/plumbing/water-treatment"),
        ("HVAC in Xenia", "/locations/xenia"),
        ("office addresses and hours", "/contact")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Beavercreek, from the office at 712 "
          "N Fairfield Rd. Replacement work gets permitted through Greene County rather than the "
          "city. We answer the no-heat line at any hour.",
   slots=[("Who permits a furnace replacement in Beavercreek?", [
    "Greene County, not the city. The Greene County Department of Building Regulation at 667 "
    "Dayton-Xenia Rd covers every city and village in the county except Fairborn, Xenia, "
    "Bowersville, Clifton, Cedarville and Yellow Springs. Inspections book through the iWorQ portal "
    "by 3pm the previous working day, which is worth knowing when a replacement has to happen "
    "before a cold snap."])],
   faq=("How close is the nearest technician to my Beavercreek house?",
        "The office is at 712 N Fairfield Rd in Beavercreek, so trucks covering the city start "
        "their day inside it.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Beavercreek, from the office at 712 N "
          "Fairfield Rd, and cover Beavercreek Township, Xenia Township and part of Sugarcreek "
          "Township too. Most calls get handled the same day.",
   slots=[("How does a Beavercreek replacement schedule around inspections?", [
    "Greene County inspections book through the iWorQ portal up to 3pm the previous working day. "
    "That sets the rhythm on a replacement job: the install happens, the inspection is booked the "
    "afternoon before, and the schedule works backwards from there. Fairborn and Xenia next door "
    "are outside the county program and run on their own timing, which is a common source of "
    "confusion for homeowners comparing quotes across town lines."])],
   faq=("Do you cover Beavercreek Township as well as the city?",
        "Yes, along with Xenia Township and parts of Sugarcreek Township, all dispatched from the "
        "same office on N Fairfield Rd.")),
  "plumbing": dict(
   h1="Plumbers in {X}: repairs, water heaters and softeners",
   answer="We handle water heaters, drains, leaks and softeners in Beavercreek, from the office "
          "at 712 N Fairfield Rd. Greene County cut delivered hardness from 27 grains per gallon "
          "to about 8 in early 2025. Plenty of softeners never got reset.",
   slots=[("What did the 2025 water change do to Beavercreek plumbing?", [
    "Greene County finished a $46 million plant expansion in Beavercreek Township, adding roughly "
    "20,000 square feet of membrane and reverse-osmosis softening. The transition ran January to "
    "March 2025 and took 18,092 accounts from 27 grains per gallon to about 8. A softener installed "
    "before that is still set for 27 grain water, so it over-softens and burns salt. Water heaters "
    "and fixtures scaled under decades of the old water are the installed base underneath all of it."]),
    ("Who issues a plumbing permit in Beavercreek?", [
    "Greene County, through the Department of Building Regulation at 667 Dayton-Xenia Rd, which "
    "covers Beavercreek along with most of the county."])],
   faq=("I am on a well in Greene County. Did my water change in 2025?",
        "No. The softening happened at the county treatment plant, so private wells still draw "
        "untreated groundwater. Well households need their own treatment decision and should ignore "
        "advice written for county-supplied neighbors.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Beavercreek, from the office at 712 N "
          "Fairfield Rd, and every visit ends with a written report and photos. X-Plan covers "
          "both visits for $249 a year.",
   slots=[("What does a Beavercreek tune-up check that others might not?", [
    "The humidifier, if there is one. Greene County's water changed in early 2025, and a whole-home "
    "humidifier pad and a softener are both calibrated for water that is no longer being delivered. "
    "A seasonal visit is the natural point to check both, because the technician is already at the "
    "equipment."])],
   faq=("Can I book a tune-up at the Beavercreek office in person?",
        "The office at 712 N Fairfield Rd is staffed " + D.HOURS_STAFFED_PROSE + ". Booking "
        "by phone on " + PHONE + " or online is faster.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Beavercreek, "
          "from the office at 712 N Fairfield Rd. A camera goes into your ductwork before we "
          "quote anything, and you get photos from before and after.",
   slots=[("What makes Beavercreek ductwork easier to clean?", [
    "Age and design. Beavercreek's housing is largely post-war suburban, built around forced-air "
    "systems rather than converted to them, so the trunk lines are purpose-built and reachable. "
    "That makes a negative-pressure clean straightforward compared with a pre-war house in Dayton "
    "where the ducts were threaded into a basement afterwards."])],
   faq=("Do you clean dryer vents on the same visit?",
        "Yes, end to end, on the same visit as the ductwork.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Beavercreek, from the "
          "office at 712 N Fairfield Rd. We measure humidity, particulates and ventilation in "
          "your house before recommending a thing.",
   slots=[("Why is whole-home equipment easy to fit in Beavercreek?", [
    "Because the ductwork is purpose-built. Beavercreek's post-war suburban housing was designed "
    "around forced air, so there is a real return plenum and a real supply trunk to mount a "
    "four-inch media filter, a humidifier or a UV lamp on. That is not true in Cincinnati's radiator "
    "houses or in Dayton's pre-war conversions, where the same equipment needs a different plan."])],
   faq=("My humidifier pad clogs constantly. Is that the water?",
        "Often. Greene County water was 27 grains per gallon until early 2025 and pads fitted for "
        "that water scale quickly. The change to about 8 grains alters the calculation, and the pad "
        "and softener are worth checking together.")),
 }),

# ---------------------------------------------------------------- 4. Mason
"mason": dict(
 alt="A residential street in Mason, Ohio",
 # [NEEDS: confirm whether cities/mason.jpg shows the office on Tylersville Rd.]
 answer="We work out of 5633 Tylersville Rd in Mason, open since 2018, covering Warren County "
        "homes for heating, cooling and plumbing. Most calls get handled the same day, and the "
        "emergency line never closes.",
 sections=[
  ("Why is so much Mason equipment failing at once?", [
   "Because so much of it went in at once. Mason built out through the 1990s and 2000s, which means "
   "a very large number of houses received their first condensing furnace and their first 10 to 13 "
   "SEER condenser somewhere between 1995 and 2008. That equipment is now 18 to 30 years old and "
   "reaching the end of its life on roughly the same schedule.",
   "The good news for Mason homeowners is the opposite of Dayton's situation: the ductwork in these "
   "houses is generally sound and correctly sized. It is the equipment that is tired, which usually "
   "makes for a clean swap rather than a rebuild."]),
  # [NEEDS: ACS DP04 year-structure-built distribution for Mason, to put a percentage on "a very
  # large number".]
  ("Where does Mason's water actually come from?", [
   "From Cincinnati. Mason's drinking water is supplied by Greater Cincinnati Water Works, not by "
   "Warren County Water &amp; Sewer and not from city wells, which puts Mason houses on roughly 7 to "
   "8 grains per gallon. Meanwhile the City of Mason owns and operates its own wastewater collection "
   "and treatment system. Water in from Cincinnati, sewer handled locally. That split matters when a "
   "job touches both sides, because the two systems answer to different people."]),
  ("Does Mason or Warren County issue the permit?", [
   "Mason. The City of Mason Engineering &amp; Building Department administers permits for work "
   "inside the city, including separate trade permits for mechanical and HVAC work. Mason is not on "
   "the Warren County building department, which is a common wrong assumption for contractors "
   "working across the county line."]),
  # [NEEDS: the exact mechanical permit application name, fee and typical turnaround, direct from
  # imaginemason.org.]
 ],
 table=dict(
  caption="Common problems in Mason, Ohio homes and what to book",
  takeaway="Most Mason calls we take come from equipment installed between 1995 and 2008 that "
           "has reached the end of its life, sitting on ductwork that is still perfectly fine.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Furnace over 18 years old, repairs stacking up",
    "First-generation condensing furnace from the 1995 to 2008 build-out",
    "Repair or replace assessment", "Plan ahead"),
   ("AC runs constantly and bills climb", "Original 10 to 13 SEER condenser near end of life",
    "Cooling assessment", "Book this month"),
   ("Condensate drain backing up", "Blocked trap on a high-efficiency furnace", "Heating repair",
    "Book this week"),
   ("Heat pump underperforms on cold nights",
    "Balance point set for zone 4A rather than Mason's zone 5A", "Heat pump evaluation",
    "Book this month"),
   ("Water heater scaling on city water",
    "Roughly 7 to 8 grain water from Greater Cincinnati Water Works", "Water heater service",
    "Plan ahead"),
   ("No cooling during a heat wave", "Compressor, capacitor or refrigerant failure",
    "Emergency cooling call", "Call 24/7 now"),
  ]),
 faq=[
  ("Where is the Mason office?",
   "5633 Tylersville Rd, Mason, OH 45040. It opened in 2018. Office staff are in " + D.HOURS_STAFFED_PROSE + ", "
   "8:00 AM to 5:00 PM, and the emergency line at " + PHONE + " is answered 24/7."),
  ("My Mason house was built in the late 1990s. Is the whole system due?",
   "Often the equipment is and the ductwork is not. Houses from Mason's 1995 to 2008 build-out "
   "generally have sound, correctly sized duct runs, so a replacement is usually an equipment swap "
   "rather than a rebuild. That is a cheaper job than the same age of house in Dayton."),
  ("Is Mason water the same as Cincinnati water?",
   "Yes. Mason is supplied by Greater Cincinnati Water Works, which reports roughly 7 to 8 grains "
   "per gallon. Warren County Water &amp; Sewer supplies other parts of the county on a different, "
   "softened supply."),
  ("Who issues an HVAC permit in Mason?",
   "The City of Mason Engineering &amp; Building Department, not Warren County. Mason runs its own "
   "trade permits for mechanical work."),
  ("Is Mason in the same climate zone as Cincinnati?",
   "No. Mason is IECC zone 5A and Cincinnati is zone 4A, about 20 minutes south. That difference can "
   "change a heat pump balance point or a furnace size on an otherwise identical house."),
 ],
 links=[("HVAC in West Chester Township", "/locations/west-chester"),
        ("HVAC in Cincinnati", "/locations/cincinnati"),
        ("heat pump systems", "/heat-pump")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Mason, from the office at 5633 "
          "Tylersville Rd. A lot of the equipment here went in between 1995 and 2008 and is "
          "wearing out now. The no-heat line never closes.",
   slots=[("Why is Mason equipment failing on a schedule?", [
    "Mason built out through the 1990s and 2000s, so a very large number of houses received their "
    "first condensing furnace inside a narrow window. That equipment is now 18 to 30 years old and "
    "reaching the end of its life together. The upside is the ductwork: houses from that era "
    "generally have sound, correctly sized duct runs, so a replacement is usually a clean equipment "
    "swap rather than a rebuild. Mason also sits in IECC climate zone 5A while Cincinnati, 20 "
    "minutes south, sits in 4A, so a load calculation borrowed from a Cincinnati job can size the "
    "furnace wrong."])],
   faq=("My Mason furnace is 22 years old but still running. Should I wait?",
        "That is a judgement call, and the repair-or-replace guidance on this page is the honest "
        "framing. On equipment that age the risk is a failure during the coldest week rather than a "
        "gradual decline, and a replacement planned in autumn costs less stress than one arranged "
        "in January.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Mason, from our Tylersville Rd office. "
          "Plenty of houses here still run the original 10 to 13 SEER condenser from the "
          "1995 to 2008 build-out. Most calls get handled the same day.",
   slots=[("Is it worth replacing a working 10 SEER condenser?", [
    "Sometimes, and the honest answer depends on the repair history rather than the rating alone. A "
    "10 to 13 SEER unit from Mason's build-out is at or past its service life, and the efficiency "
    "gap against current equipment is real. What tips the decision is a second repair in one season, "
    "a compressor fault, or R-22 refrigerant, which is no longer produced. A unit that has never "
    "failed and holds charge is not an emergency."])],
   faq=("Do you install ductless in Mason houses?",
        "Yes, though it comes up less here than in Cincinnati. Mason's build-out housing has real "
        "ductwork, so ductless is usually for an addition, a sunroom or a bonus room over the garage "
        "rather than for the whole house.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Mason, from our Tylersville Rd "
          "office. Your water comes from Greater Cincinnati Water Works at roughly 7 to 8 "
          "grains per gallon. We answer the line at any hour.",
   slots=[("Where does Mason's water and sewer actually come from?", [
    "Water comes in from Greater Cincinnati Water Works, not from Warren County Water &amp; Sewer "
    "and not from city wells, at roughly 7 to 8 grains per gallon. Wastewater is a different story: "
    "the City of Mason owns and operates its own collection and treatment system. Two different "
    "authorities on the two ends of the same house."]),
    ("Who issues a plumbing permit in Mason?", [
    "The City of Mason Engineering &amp; Building Department, which administers permits for work "
    "inside the city including separate trade permits. Mason is not on the Warren County building "
    "department."])],
   faq=("Do I need a water softener in Mason?",
        "Often not. Greater Cincinnati Water Works delivers roughly 7 to 8 grains per gallon, which "
        "is moderately hard rather than the untreated groundwater figures further north. Scale still "
        "builds on a water heater over ten years, so it is a preference question rather than a "
        "necessity.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Mason, from the office at 5633 "
          "Tylersville Rd. It matters most on the 1995 to 2008 equipment still running across "
          "the city. X-Plan covers two visits a year for $249.",
   slots=[("Does maintenance buy time on end-of-life equipment?", [
    "It buys some, and more importantly it buys warning. On the condensing furnaces and condensers "
    "Mason installed between 1995 and 2008, a seasonal visit measures the things that predict "
    "failure: capacitor values, refrigerant charge, blower amp draw and combustion. That turns a "
    "January no-heat call into an autumn replacement conversation, which is a cheaper, calmer "
    "version of the same event."])],
   faq=("Is X-Plan worth it on equipment that is nearly done?",
        "The accrual is the part that matters to you here. You build up 100% of what you pay in, "
        "across consecutive years, toward replacing the equipment when it finally goes. It is "
        "capped at $2,500 or 10 years, whichever comes first, and it follows you, not the "
        "house.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Mason, from "
          "the office at 5633 Tylersville Rd. A camera goes into your ductwork before we quote "
          "anything, and you get photos from before and after.",
   slots=[("What is usually in Mason ductwork?", [
    "Construction dust from the original build, then whatever twenty-five years of living added. "
    "Houses from the 1990s and 2000s have purpose-built duct runs with proper returns, so a "
    "negative-pressure clean reaches the whole system. The most common finding is a blower "
    "compartment that has never been opened, which quietly costs airflow across the entire house."])],
   faq=("My house is only 25 years old. Do the ducts need cleaning?",
        "Maybe not. The camera goes in first and the footage decides. Renovation work, pets and a "
        "system that has never had the blower compartment cleaned are the usual reasons a house that "
        "age is worth doing.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Mason, from the office at "
          "5633 Tylersville Rd. We measure humidity, particulates and ventilation in your house "
          "before recommending a thing.",
   slots=[("What fits a 1990s or 2000s Mason house?", [
    "Almost anything, which is the advantage of this housing stock. There is a real return plenum "
    "and a real supply trunk, so a four-inch media filter, a whole-home humidifier, a UV lamp or a "
    "ducted dehumidifier all mount without modification. The constraint here is rarely the ductwork. "
    "It is deciding which problem is actually being solved, which is why the measurement happens "
    "first."])],
   faq=("Should I upgrade the one-inch filter to a four-inch?",
        "In most Mason houses yes, because the ductwork can carry it. A thicker media filter catches "
        "more, lasts longer and puts less strain on the blower than a high-MERV one-inch does. The "
        "airflow gets checked before and after.")),
 }),

# ---------------------------------------------------------------- 5. Kettering
"kettering": dict(
 alt="A post-war ranch house on a residential street in Kettering, Ohio",
 answer="We cover Kettering from the Beavercreek office, about seven miles east. Heating, "
        "cooling and plumbing for the post-war ranches and split-levels that fill the city. "
        "Most get handled the same day, and the emergency line never closes.",
 sections=[
  ("What goes wrong in a 1950s ranch?", [
   "Kettering is the archetypal post-war Dayton suburb and its housing is dominated by 1950s and "
   "1960s ranches and split-levels. Sixty to seventy-five year old ductwork was sized for low-static "
   "equipment that no longer exists, so a modern blower pushing through it runs into resistance the "
   "original installer never planned for.",
   "Returns are the recurring problem: one or two of them for a whole house, which limits what a "
   "high-MERV filter can do without starving the system. Mechanical closets are small, equipment "
   "often sits in a crawl space or a half basement, and there is rarely room to grow."]),
  # [NEEDS: Kettering incorporation year and ACS median year structure built. Both belong on this
  # page as numbers.]
  ("Which water utility covers my street?", [
   "It depends which side of the line the house is on, and that is not a figure of speech. Most of "
   "Kettering runs on the Montgomery County and Dayton regional supply, but small parts of Kettering "
   "are Greene County Sanitary Engineering customers and went through the county's softening "
   "changeover in early 2025, when delivered hardness dropped from 27 grains per gallon to about 8. "
   "Two houses a few streets apart can need different softener advice for that reason alone."]),
  # [NEEDS: confirmed delivered hardness for the Montgomery County and Dayton regional supply.]
  ("Do plumbers have to register with the City of Kettering?", [
   "Yes, on top of the state license. Sub-trades are regulated by the Ohio Construction Industry "
   "Licensing Board, and Kettering additionally requires plumbers to register with the city. "
   "Kettering is also one of only four Montgomery County cities that runs its own plumbing "
   "inspection rather than using the county program.",
   "Building and mechanical permits go through the Access Kettering portal, and a permit is required "
   "to erect, install, enlarge, alter, repair, remove, convert or replace mechanical, gas, electrical "
   "or plumbing systems. Work done without one is subject to a stop-work order, a notice of "
   "violation, double permit fees, and removal of the work. That last part is worth knowing before "
   "accepting a quote that comes in suspiciously low."]),
 ],
 table=dict(
  caption="Common problems in Kettering, Ohio homes and what to book",
  takeaway="Most Kettering comfort complaints we see come back to return air rather than the "
           "furnace, because 1950s ranch ductwork was sized for equipment two generations gone.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("New high-MERV filter made airflow worse", "One or two returns for the whole house",
    "Duct and return evaluation", "Book this month"),
   ("Bedrooms at the end of the run stay cold",
    "60 to 75 year old ductwork sized for low-static equipment", "Heating assessment",
    "Book this month"),
   ("No space for a bigger air handler", "Original post-war mechanical closet",
    "Replacement planning visit", "Plan ahead"),
   ("Softener behaving oddly since early 2025",
    "Address is on the Greene County supply, which dropped to about 8 grains",
    "Softener adjustment", "Book this month"),
   ("Contractor quote with no permit mentioned",
    "Kettering requires a permit and charges double fees for skipping it", "Second opinion visit",
    "Before you sign"),
   ("No heat in a cold snap", "Ignition, control board or gas valve failure",
    "Emergency heating call", "Call 24/7 now"),
  ]),
 faq=[
  ("Why does my Kettering ranch have hot and cold rooms?",
   "Usually the returns. Kettering's 1950s and 1960s housing typically has one or two return paths "
   "for the whole house, and rooms at the end of a long supply run never catch up. Adding return "
   "capacity fixes more of these houses than replacing the furnace does."),
  ("Can I put a high-MERV filter in a 1950s house?",
   "Sometimes, but not always at the thickness people want. A four-inch media filter on a system "
   "with one undersized return can starve the blower. The filter decision follows the return-air "
   "decision, not the other way round."),
  ("Does Kettering require its own plumbing permit?",
   "Yes. Kettering is one of four Montgomery County cities that runs its own plumbing inspection "
   "rather than the county program, and plumbers must register with the city as well as holding a "
   "state license."),
  ("What happens if work is done in Kettering without a permit?",
   "The city can issue a stop-work order and a notice of violation, charge double permit fees, and "
   "require the work to be torn out. We pull permits as part of the job."),
  ("Is Kettering water the same as Dayton water?",
   "For most addresses, yes. Small parts of Kettering are supplied by Greene County Sanitary "
   "Engineering instead, and those houses went from 27 grains per gallon to about 8 during the "
   "county's early 2025 changeover."),
 ],
 links=[("HVAC in Centerville", "/locations/centerville"),
        ("HVAC in Dayton", "/locations/dayton"),
        ("indoor air quality equipment", "/locations/kettering/indoor-air-quality")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Kettering, about seven miles from "
          "the Beavercreek office, including the 1950s and 1960s ranches and split-levels that "
          "dominate the city. We answer the no-heat line at any hour, every day.",
   slots=[("What limits a new furnace in a 1950s Kettering ranch?", [
    "The ductwork it has to breathe through. Duct systems that old were sized for low-static "
    "equipment, and a modern high-efficiency blower meets resistance the original installer never "
    "planned for. There is usually one or two returns for the whole house, and the mechanical closet "
    "was built to hold a furnace two sizes smaller than what gets sold today. A load calculation and "
    "a static pressure reading before the quote saves an expensive mistake."])],
   faq=("Will a new furnace fix my cold back bedroom?",
        "Usually not on its own. In Kettering's post-war housing the cold room is normally a supply "
        "and return problem, and a new furnace pushing through the same undersized duct produces the "
        "same result at a higher price.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Kettering, about seven miles from the "
          "Beavercreek office. In a 1950s or 1960s ranch the limit is usually duct capacity "
          "rather than equipment size. Most calls get handled the same day.",
   slots=[("Why does a bigger condenser not fix a Kettering ranch?", [
    "Because the air cannot get there. Post-war duct systems in Kettering were sized for the "
    "equipment of the day, and adding capacity upstream does nothing about a return that cannot pull "
    "enough air back. An oversized system short cycles, removes less humidity, and leaves the house "
    "feeling clammy at the right temperature. Where a room genuinely cannot be reached, a single "
    "ductless head is often cheaper and better than rebuilding a duct run."])],
   faq=("Can I add air conditioning to a half-basement furnace setup?",
        "Usually yes. Kettering equipment often sits in a crawl space or half basement with limited "
        "room around it, so the coil and lineset routing get surveyed on site before a price is given.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Kettering. This is one of "
          "only four Montgomery County cities that runs its own plumbing inspection instead of "
          "the county program. We answer the emergency line at any hour.",
   slots=[("Which water supply covers a Kettering address?", [
    "Most of the city runs on the Montgomery County and Dayton regional supply, but small parts of "
    "Kettering are Greene County Sanitary Engineering customers and went through the January to "
    "March 2025 softening changeover, from 27 grains per gallon to about 8. Softener advice that is "
    "right on one side of that line is wrong on the other."]),
    ("Do plumbers need to be registered with the City of Kettering?", [
    "Yes. Sub-trades are regulated by the Ohio Construction Industry Licensing Board, and Kettering "
    "requires plumbers to register with the city on top of that. Permits go through the Access "
    "Kettering portal, and work done without one is subject to a stop-work order, a notice of "
    "violation, double permit fees and removal of the work."])],
   faq=("A contractor told me my Kettering job does not need a permit. Is that right?",
        "Kettering requires a permit to erect, install, enlarge, alter, repair, remove, convert or "
        "replace mechanical, gas, electrical or plumbing systems. Unpermitted work carries double "
        "permit fees and can be ordered removed, so it is worth a second opinion.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Kettering, about seven miles from the "
          "Beavercreek office, and every visit ends with a written report and photos. X-Plan "
          "covers both visits for $249 a year.",
   slots=[("What does a tune-up measure in an older Kettering house?", [
    "Static pressure, more than anywhere else. Equipment working against 60 to 75 year old ductwork "
    "runs at higher static than it was designed for, and that shows up as a hot blower motor, a "
    "short filter life and a system that never quite keeps up. A tune-up that measures it gives an "
    "honest read on whether the next spend belongs on equipment or on ducts."])],
   faq=("Does a tune-up need a Kettering permit?",
        "No. Permits apply to installation, alteration and replacement work, not to maintenance.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Kettering. "
          "Duct systems in the city's 1950s and 1960s housing are often 60 to 75 years old and "
          "have never been opened. You get photos from before and after.",
   slots=[("What does the camera find in a post-war Kettering house?", [
    "Panned joist bays used as returns, unsealed and open to the framing cavity, which is the most "
    "common finding in this housing type. Add sixty-plus years of dust and whatever a remodel left "
    "behind. The footage also answers a second question worth more than the cleaning: whether the "
    "return path is worth rebuilding, which is the fix behind most Kettering comfort complaints."])],
   faq=("My returns are just the space between the floor joists. Is that normal?",
        "It is normal for Kettering's post-war housing and it is not ideal. Panned joist bays pull "
        "air from the framing cavity as well as the room. The camera shows the condition, and "
        "sealing them is often a bigger improvement than the cleaning itself.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Kettering, about seven "
          "miles from the Beavercreek office. In 1950s housing the filter you can run is limited "
          "by return capacity, not preference, so we measure airflow first.",
   slots=[("Can a 1950s Kettering house take a high-MERV filter?", [
    "Sometimes, and sometimes only at a lower rating. A house with one or two returns and 60 to 75 "
    "year old ductwork is already running at higher static pressure than modern equipment likes. "
    "Dropping a dense filter into that starves the blower, which costs more comfort than the filter "
    "gains. The order of operations here is airflow first, filtration second, and a static pressure "
    "reading decides which filter the house can actually carry."])],
   faq=("My new filter made the house worse. Why?",
        "Almost certainly airflow. In Kettering's post-war housing a dense filter on a single "
        "undersized return restricts the blower, and the symptoms look like a failing system. "
        "Measuring static pressure identifies it in one visit.")),
 }),

# ---------------------------------------------------------------- 6. Centerville
"centerville": dict(
 alt="A residential street in Centerville, Ohio",
 # [NEEDS: confirm whether cities/centerville.jpg shows the Uptown stone district. If it does,
 # the alt becomes "Early limestone buildings in Uptown Centerville, Ohio".]
 answer="We cover Centerville from the Beavercreek office, about nine miles northeast. Heating, "
        "cooling and plumbing for the old stone Uptown and the subdivisions around it alike. "
        "Most get handled the same day, and the emergency line never closes.",
 sections=[
  ("Why does one town need two different approaches?", [
   "Because Centerville is two towns in one. It was founded in 1796, and its Uptown district holds "
   "Ohio's largest collection of early stone buildings, put up from locally quarried limestone, many "
   "of them on the National Register. Around that core sits a large late-twentieth-century suburban "
   "ring.",
   "Those are genuinely different jobs. In a limestone or timber structure, equipment placement, "
   "venting routes and duct runs are constrained by the building itself, and a lot of what would be "
   "routine elsewhere is not available. In the 1970s to 1990s subdivisions the systems are "
   "conventional forced air, now on their second or third replacement, where the constraint is the "
   "original equipment closet rather than the walls."]),
  ("Did the 2025 Greene County water change affect Centerville?", [
   "Parts of it. Most of Centerville is on the Montgomery County and Dayton regional supply, but "
   "small parts of the city are Greene County Sanitary Engineering customers and were inside the "
   "January to March 2025 softening changeover, when delivered hardness went from 27 grains per "
   "gallon to about 8. Those households have a softener still set for the old water. The rest of "
   "Centerville does not."]),
  ("Who inspects plumbing work in Centerville?", [
   "The city does. Centerville is one of only four Montgomery County cities excluded from the Public "
   "Health, Dayton &amp; Montgomery County plumbing program, alongside Dayton, Oakwood and "
   "Kettering. So a Centerville plumbing permit is a city permit."]),
  # [NEEDS: which authority issues residential building and mechanical permits in Centerville. The
  # health department exclusion only tells us about plumbing; do not assume the city handles both.]
 ],
 table=dict(
  caption="Common problems in Centerville, Ohio homes and what to book",
  takeaway="We work two very different housing types in Centerville, and the right answer in a "
           "limestone building from the 1800s is rarely the right answer in a 1980s subdivision.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Nowhere obvious to run a new flue or lineset",
    "Masonry walls in an early stone or timber structure", "On-site replacement survey",
    "Plan ahead"),
   ("Second or third system replacement due",
    "1970s to 1990s subdivision equipment at end of life", "Repair or replace assessment",
    "Plan ahead"),
   ("Softener acting up since early 2025",
    "Address is on the Greene County supply, now about 8 grains", "Softener adjustment",
    "Book this month"),
   ("Water heater underperforming", "Scale from years of harder water", "Water heater service",
    "Book this month"),
   ("Uneven temperatures upstairs", "Duct runs constrained by an older structure",
    "Duct evaluation", "Book this month"),
   ("No heat or water on the floor", "Equipment or supply failure", "Emergency call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Can you work on a historic stone house in Uptown Centerville?",
   "Yes. Centerville has Ohio's largest collection of early stone buildings and they need a survey "
   "before a quote, because venting routes, equipment placement and duct runs are limited by the "
   "structure. That visit happens before any number gets put on paper."),
  ("Does Centerville issue its own plumbing permit?",
   "Yes. Centerville is one of four Montgomery County cities excluded from the county's plumbing "
   "inspection program, so plumbing permits come from the city."),
  ("Did Centerville water get softer in 2025?",
   "Only for the parts of the city supplied by Greene County Sanitary Engineering. Those addresses "
   "went from 27 grains per gallon to about 8 between January and March 2025. The rest of "
   "Centerville is on the Montgomery County and Dayton regional supply and did not change."),
  ("How far away is the nearest technician?",
   "About nine miles. We dispatch Centerville work from the Beavercreek office."),
  ("Do you replace systems in 1980s subdivisions, or only repair them?",
   "Both. Houses from Centerville's 1970s to 1990s ring are typically on their second or third "
   "system, and the ductwork is usually reusable, which keeps a replacement to an equipment swap."),
 ],
 links=[("HVAC in Kettering", "/locations/kettering"),
        ("HVAC in Springboro", "/locations/springboro"),
        ("water treatment and softeners", "/plumbing/water-treatment")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Centerville, about nine miles from "
          "the Beavercreek office, across a town founded in 1796 and the late-twentieth-century "
          "ring around it. We answer the no-heat line at any hour, every day.",
   slots=[("How does the housing era change the heating job?", [
    "Substantially. In Centerville's early limestone and timber structures, venting routes, "
    "equipment placement and duct runs are set by the building, and a lot of what is routine "
    "elsewhere is simply not possible. In the 1970s to 1990s subdivisions around the historic core "
    "the systems are conventional forced air on their second or third replacement, where the "
    "constraint is the original equipment closet. Same city, two different surveys."])],
   faq=("Can you vent a modern high-efficiency furnace in an old stone house?",
        "It depends on the wall and the route, which is why these jobs get a survey before a price. "
        "Condensing furnaces need a sidewall or roof termination with specific clearances, and in a "
        "masonry structure that is the part that decides the job.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Centerville, about nine miles from the "
          "Beavercreek office, in the historic district and the 1970s to 1990s subdivisions "
          "alike. Most calls get handled the same day.",
   slots=[("Where does the condenser go on a historic property?", [
    "That is the first question on a Centerville job in the Uptown area, and it is answered on site. "
    "Masonry walls limit where a lineset can pass, clearances around the outdoor unit are tighter on "
    "older lots, and appearance matters on a property that may be on the National Register. In the "
    "subdivisions around the core none of that applies and the job is a standard replacement."])],
   faq=("Is a ductless system a good fit for an older Centerville house?",
        "Often, yes. Where duct runs cannot be routed through masonry, ductless heads cool room by "
        "room with only a small penetration for the lineset, which is usually the least invasive "
        "option available.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Centerville. This is one of "
          "four Montgomery County cities that inspects its own plumbing, so your permit comes "
          "from the city, not the county. The emergency line never closes.",
   slots=[("Did Centerville's water change in 2025?", [
    "For part of the city. Most of Centerville is on the Montgomery County and Dayton regional "
    "supply, but small parts are Greene County Sanitary Engineering customers and were inside the "
    "January to March 2025 softening changeover, when hardness went from 27 grains per gallon to "
    "about 8. Those households have a softener still set for the old water. The rest of the city "
    "does not."]),
    ("Who inspects plumbing in Centerville?", [
    "The city. Public Health, Dayton &amp; Montgomery County excludes Centerville, Dayton, Oakwood "
    "and Kettering from its county plumbing program, so a Centerville plumbing permit is a city "
    "permit."])],
   faq=("How do I find out which water utility serves my Centerville address?",
        "The bill answers it fastest. Greene County Sanitary Engineering customers saw hardness drop "
        "to about 8 grains per gallon in early 2025; Montgomery County and Dayton regional customers "
        "did not.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Centerville, about nine miles from the "
          "Beavercreek office, on historic properties and 1980s subdivisions alike. X-Plan covers "
          "two visits a year for $249.",
   slots=[("Why does maintenance matter on an older Centerville property?", [
    "Because replacement is harder here. When the equipment in a historic structure fails, the "
    "options are constrained by the building, and the survey takes longer than a subdivision swap. "
    "Keeping the current system healthy is worth more when the alternative is a complicated project "
    "rather than a same-week changeout."])],
   faq=("Do you service equipment in a house on the National Register?",
        "Yes. The work is the same; the planning is not. Anything that touches the structure gets "
        "discussed before it happens.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Centerville, "
          "about nine miles from the Beavercreek office. In the older parts of town the duct "
          "layout varies house to house, so we photograph every job before and after.",
   slots=[("Why does a Centerville quote start with a camera?", [
    "Because the duct layout is not predictable here. In a 1980s subdivision the runs are where you "
    "expect them. In an early stone or timber structure they were fitted around whatever the "
    "building allowed, so the camera maps the system before anyone quotes a price for cleaning it."])],
   faq=("Are the ducts in an old house even cleanable?",
        "Usually, though not always along the whole run. The footage shows where access exists and "
        "where it does not, and the quote covers what can actually be reached.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Centerville, about nine "
          "miles from the Beavercreek office. What suits a historic Uptown house and what suits a "
          "1990s subdivision are different, so we measure before recommending anything.",
   slots=[("What works in an old house that does not work in a new one?", [
    "Humidity control, mostly. Older Centerville structures leak more air, so they run dry in winter "
    "and the fix is a whole-home humidifier rather than a purifier. Newer subdivision housing holds "
    "moisture and stale air instead, which points toward dehumidification and ventilation. Same "
    "city, opposite problems, which is why the measurement comes before the recommendation."])],
   faq=("My old house has static shocks all winter. Is that fixable?",
        "Yes, and it is a humidity problem rather than an electrical one. A whole-home humidifier on "
        "the supply duct addresses it, and the target level gets set from a measurement rather than "
        "a guess.")),
        # [NEEDS: the winter humidity target range Extreme's technicians recommend.]
 }),

# ---------------------------------------------------------------- 7. West Chester
"west-chester": dict(
 alt="A subdivision street in West Chester Township, Ohio",
 answer="We cover West Chester Township from the Mason office, about seven miles east. "
        "Heating, cooling and plumbing for Ohio's most populous township. Most calls get "
        "handled the same day, and someone answers the emergency line at any hour.",
 sections=[
  ("Why is so much West Chester equipment failing together?", [
   "The growth curve explains it. West Chester went from 6,236 residents in 1960 to 12,795 in 1970, "
   "23,553 in 1980, 54,895 in 2000 and 65,242 in 2020. The build-out landed between 1980 and 2000, "
   "which produced a very large and very uniform cohort of houses whose equipment was installed or "
   "first replaced in the late 1990s and 2000s. That cohort is reaching end of life more or less "
   "together.",
   "Beckett Ridge, Olde West Chester, Wetherington, Maud, Port Union, Pisgah and Tylersville are all "
   "inside the same pattern, so a technician who has worked one subdivision recognizes the next one."]),
  ("Which utility supplies water in West Chester?", [
   "Butler County Water &amp; Sewer, not Greater Cincinnati Water Works and not the City of Mason. "
   "Butler County reports total hardness of 131 mg/L, about 7.7 grains per gallon, across a system "
   "that also covers Liberty, Fairfield, Hanover and Ross townships, Monroe and New Miami. Mason is "
   "seven miles away and on a different utility entirely, which is worth knowing before applying "
   "advice from one town to the other. Duke Energy Ohio supplies both gas and electricity here, so "
   "there is one bill and one shut-off rather than two."]),
  ("How long does a Butler County HVAC permit take?", [
   "Typically five to seven business days. West Chester is a township and does not run its own "
   "building department, so permits go to the Butler County Department of Development, Building "
   "&amp; Zoning at 130 High Street in Hamilton, through the Accela Citizen Portal. Butler County "
   "has a dedicated application and addendum specifically for HVAC replacement, which is unusual and "
   "genuinely useful: the paperwork for a straight equipment swap is its own form rather than a "
   "general construction permit."]),
 ],
 table=dict(
  caption="Common problems in West Chester Township, Ohio homes and what to book",
  takeaway="West Chester's 1980 to 2000 housing is reaching its first or second equipment "
           "replacement more or less together, on ductwork that is generally still fine to reuse.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Second repair on the same system this season",
    "Late 1990s or 2000s equipment at end of life", "Repair or replace assessment", "Plan ahead"),
   ("Neighbors all replacing systems the same year",
    "Subdivision built out 1980 to 2000 with equipment installed together",
    "Replacement planning visit", "Plan ahead"),
   ("Replacement job waiting on paperwork",
    "Butler County permits typically run five to seven business days",
    "Schedule around the permit window", "Same month"),
   ("Water heater scaling", "About 7.7 grain water from Butler County Water &amp; Sewer",
    "Water heater service", "Book this month"),
   ("Gas and electric both out", "Duke Energy Ohio supplies both fuels in this township",
    "Utility first, then service call", "Same day"),
   ("No cooling in a heat wave", "Compressor, capacitor or refrigerant failure",
    "Emergency cooling call", "Call 24/7 now"),
  ]),
 faq=[
  ("Is West Chester a city or a township, and does that change anything?",
   "It is a township, and it changes who issues the permit. West Chester does not run its own "
   "building department, so permits go to the Butler County Department of Development, Building "
   "&amp; Zoning at 130 High Street in Hamilton."),
  ("How long does a permit take for a system replacement in West Chester?",
   "Butler County typically turns permits around in five to seven business days, and it has a "
   "dedicated application and addendum for HVAC replacement. We handle the filing."),
  ("Is West Chester water the same as Mason water?",
   "No. West Chester is on Butler County Water &amp; Sewer at about 7.7 grains per gallon, while "
   "Mason seven miles away is supplied by Greater Cincinnati Water Works. Different utility, "
   "different water quality report."),
  ("Do you serve Beckett Ridge and Wetherington?",
   "Yes. Beckett Ridge, Olde West Chester, Wetherington, Maud, Port Union, Pisgah and Tylersville "
   "are all inside West Chester Township and inside the normal coverage area from the Mason office."),
  ("Why do so many West Chester houses need a system at the same time?",
   "Because they were built at the same time. The township went from 23,553 residents in 1980 to "
   "54,895 in 2000, so a very large group of houses received equipment inside a narrow window and is "
   "reaching end of life together."),
 ],
 links=[("HVAC in Mason", "/locations/mason"),
        ("HVAC in Cincinnati", "/locations/cincinnati"),
        ("financing a replacement system", "/financing-options")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in West Chester Township, about seven "
          "miles from the Mason office. Much of the equipment here went in during the late "
          "1990s and 2000s. We answer the no-heat line at any hour.",
   slots=[("How long does a Butler County replacement permit take?", [
    "Typically five to seven business days. West Chester is a township without its own building "
    "department, so permits go to the Butler County Department of Development, Building &amp; Zoning "
    "at 130 High Street in Hamilton, filed through the Accela Citizen Portal. Butler County has a "
    "dedicated application and addendum for HVAC replacement, which keeps a straight equipment swap "
    "out of the general construction queue. Planning a replacement before the first cold week rather "
    "than during it is the practical consequence."])],
   faq=("Why do my neighbors all seem to need a furnace at the same time?",
        "Because the houses were built at the same time. West Chester grew from 23,553 residents in "
        "1980 to 54,895 in 2000, so a large group of houses received equipment inside a narrow "
        "window and is reaching end of life together.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in West Chester Township, about seven miles "
          "from the Mason office. That covers Beckett Ridge, Olde West Chester, Wetherington, "
          "Maud, Port Union, Pisgah and Tylersville. Most calls get handled the same day.",
   slots=[("What is the advantage of a uniform housing stock?", [
    "Predictability. West Chester's build-out ran 1980 to 2000, so subdivisions share plans, "
    "equipment locations and duct layouts. A technician who has worked one house in Beckett Ridge "
    "has a good idea what is in the next one, which shortens diagnosis and makes a replacement quote "
    "more accurate before anyone opens a wall."])],
   faq=("Do you cover Beckett Ridge and Wetherington?",
        "Yes. Beckett Ridge, Olde West Chester, Wetherington, Maud, Port Union, Pisgah and "
        "Tylersville are all inside West Chester Township and inside the normal coverage area from "
        "the Mason office.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in West Chester Township. Your "
          "water comes from Butler County Water &amp; Sewer at about 7.7 grains per gallon. We "
          "answer the emergency line at any hour, every day.",
   slots=[("Which utility supplies West Chester water?", [
    "Butler County Water &amp; Sewer, which also covers Liberty, Fairfield, Hanover and Ross "
    "townships, Monroe and New Miami. Total hardness is 131 mg/L, about 7.7 grains per gallon. Mason "
    "seven miles east is on Greater Cincinnati Water Works instead, so water advice does not "
    "transfer between the two towns even though the drive is ten minutes."]),
    ("Who issues a plumbing permit in West Chester?", [
    "Butler County. The township does not run its own building department, so permits go to the "
    "Butler County Department of Development, Building &amp; Zoning at 130 High Street in Hamilton, "
    "through the Accela Citizen Portal."])],
   faq=("Is West Chester water hard enough to need a softener?",
        "At about 7.7 grains per gallon it is moderately hard. That is enough to scale a water "
        "heater over a decade and enough that many households choose to soften, and not so hard that "
        "it is a necessity. It is a preference call rather than a repair.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in West Chester Township, about seven miles "
          "from the Mason office. It matters most on the late 1990s and 2000s equipment still "
          "running here. X-Plan covers two visits a year for $249.",
   slots=[("Why does timing matter in a subdivision that ages together?", [
    "Because demand spikes together too. When a whole street's equipment reaches end of life in the "
    "same few years, the busiest weeks are the worst time to discover it. A seasonal visit measures "
    "the values that predict failure and turns an emergency into a planned replacement, which also "
    "means the Butler County permit window of five to seven business days is not sitting between a "
    "household and heat."])],
   faq=("Does a tune-up need a Butler County permit?",
        "No. Permits apply to installation and replacement work, not maintenance.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in West Chester "
          "Township. Housing built between 1980 and 2000 has purpose-built duct runs we can reach "
          "end to end. Every job gets photographed before and after.",
   slots=[("What is typical in West Chester ductwork?", [
    "Original construction dust, then whatever twenty to forty years added. Because the subdivisions "
    "share layouts, the findings repeat: the same trunk runs, the same return locations, and blower "
    "compartments that have never been opened. The camera still goes in first, because a house that "
    "had the work done five years ago does not need it again."])],
   faq=("How long does duct cleaning take in a typical West Chester house?",
        "Most are a single visit, including the dryer vent.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in West Chester Township, "
          "about seven miles from the Mason office. We measure humidity, particulates and "
          "ventilation in your house before recommending a thing.",
   slots=[("What does 1980s and 1990s construction need?", [
    "Filtration more often than ventilation. Houses from West Chester's build-out sit between the "
    "leaky older stock further north and the very tight construction going up now, so they are "
    "usually not sealed enough to trap stale air but are running one-inch filters that catch very "
    "little. A four-inch media filter on a real return plenum is the common upgrade, and the "
    "ductwork here can carry it."])],
   faq=("Should I add a UV light or a better filter first?",
        "The filter, in most West Chester houses. A media filter handles the particulates people "
        "actually notice. UV targets microbial growth on the coil, which is a different problem and "
        "a smaller one unless the coil shows it.")),
 }),

# ---------------------------------------------------------------- 8. Huber Heights
"huber": dict(
 alt="Brick homes on a residential street in Huber Heights, Ohio",
 answer="We cover Huber Heights from the Beavercreek office, about twelve miles southeast. "
        "That takes in the brick homes Huber Homes built between 1956 and 1992. Most get "
        "handled the same day, and the emergency line never closes.",
 sections=[
  ("Why does one contractor already know your floor plan?", [
   "Because most of Huber Heights came from one builder. Charles H. Huber started building in 1956, "
   "and Huber Homes put up 10,707 single-family houses and 2,258 multi-family units in the community "
   "between 1956 and 1992. The city's own motto is America's largest community of brick homes.",
   "The practical consequence is that a narrow set of plans repeats across thousands of houses: the "
   "same equipment locations, the same duct layouts, the same chase and closet dimensions. A "
   "technician who has worked a few hundred of them knows what is behind the wall before opening it, "
   "which shortens the diagnosis and takes most of the guesswork out of a replacement quote."]),
  # [NEEDS: three or four specifics from Extreme's own technicians about an original Huber home.
  # Original heating type, typical furnace or air handler location, duct material and sizing,
  # whether returns are ducted or panned joist bays, typical service panel capacity, whether the
  # original system was sized for a later A/C add-on. This is the highest-value page in the tree
  # and it is currently running on public history rather than field experience.]
  ("What did the Rip Rap Road softening project change?", [
   "Huber Heights runs its own municipal water system, drawing from the Great Miami Buried Valley "
   "Aquifer and treating at the Rip Rap Road Water Treatment Plant. An $11 million softening project "
   "cut total hardness from about 310 mg/L to about 120 mg/L, roughly 18 grains per gallon down to "
   "about 7. Any house with a softener installed before that project is still set for the old water, "
   "and it will be over-softening and burning salt until someone adjusts it."]),
  # [NEEDS: completion year of the Rip Rap Road softening project.]
  ("What does a plumbing permit cost in Huber Heights?", [
   "Huber Heights uses the county program rather than running its own inspection, so plumbing "
   "permits go to Public Health, Dayton &amp; Montgomery County at the Reibold Building, 117 S Main "
   "Street, Dayton. Its published fees are $45 for a new installation permit, $30 for a replacement "
   "installation permit, $14 per fixture or device, and $50 for sewer and water.",
   "A permit is required for installation, alteration or repair of plumbing, drainage or water "
   "supply systems, including replacement fixtures. There is a homeowner appliance application with "
   "affidavit for residential water heaters. Counter hours are Monday to Friday, 8:00 to 11:30 and "
   "12:30 to 4:00."]),
  # [NEEDS: whether the City of Huber Heights or Montgomery County Building Regulations issues
  # residential mechanical permits. The county covers townships; Huber Heights is a city.]
 ],
 table=dict(
  caption="Common problems in Huber Heights, Ohio homes and what to book",
  takeaway="The same faults repeat across Huber Heights because thousands of the houses share a "
           "builder, a date range and a floor plan.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Same fault the neighbor had last winter",
    "Shared floor plan and equipment layout across Huber Homes stock", "Heating assessment",
    "Book this week"),
   ("Original equipment closet too small for a swap",
    "Chase and closet dimensions repeated across the 1956 to 1992 build", "Replacement survey",
    "Plan ahead"),
   ("Softener over-softening since the plant upgrade",
    "Set for about 18 grain water, now receiving about 7", "Softener adjustment", "Book this month"),
   ("Water heater scaled and slow", "Years of pre-project hardness at about 310 mg/L",
    "Water heater service", "Book this month"),
   ("Replacing a water heater yourself",
    "County permit required, including for replacement fixtures", "Plumbing visit with permit",
    "Before the work"),
   ("No heat overnight", "Ignition, control or gas valve failure", "Emergency heating call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Have you worked on a house like mine in Huber Heights?",
   "Very likely the exact plan. Huber Homes built 10,707 single-family houses in the community "
   "between 1956 and 1992 from a narrow set of designs, so equipment locations and duct layouts "
   "repeat across thousands of addresses."),
  ("Do I need a permit to replace a water heater in Huber Heights?",
   "Yes. Public Health, Dayton &amp; Montgomery County requires a permit for installation, "
   "alteration or repair of plumbing systems, including replacement fixtures, and publishes a $30 "
   "replacement installation fee. There is also a homeowner appliance application with affidavit for "
   "residential water heaters."),
  ("Why is my softener suddenly using more salt?",
   "Because the water got softer and the softener did not. Huber Heights cut hardness from about 310 "
   "mg/L to about 120 mg/L with the Rip Rap Road softening project, and a unit still set for the old "
   "figure will over-soften."),
  ("Where does Huber Heights water come from?",
   "The city runs its own municipal system, drawing from the Great Miami Buried Valley Aquifer and "
   "treating at the Rip Rap Road Water Treatment Plant."),
  ("How far is the nearest technician?",
   "About twelve miles. We dispatch Huber Heights work from the Beavercreek office."),
 ],
 links=[("water heater repair", "/plumbing/water-heater/repair"),
        ("HVAC in Dayton", "/locations/dayton"),
        ("HVAC in Vandalia", "/locations/vandalia")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Huber Heights, about twelve miles "
          "from the Beavercreek office, including the 10,707 single-family homes Huber Homes "
          "built here between 1956 and 1992. We answer the no-heat line at any hour.",
   slots=[("Why does a Huber Heights diagnosis go faster?", [
    "Because the houses repeat. Huber Homes built 10,707 single-family houses and 2,258 multi-family "
    "units here between 1956 and 1992, from a narrow set of plans, which means the same equipment "
    "locations, chase dimensions and duct layouts recur across thousands of addresses. A technician "
    "who has worked several hundred of them knows the layout before opening anything."])],
   faq=("Have you worked on a house like mine?",
        "In Huber Heights, very likely the exact plan. 10,707 single-family houses here came from "
        "one builder between 1956 and 1992, so the floor plans repeat across whole neighborhoods.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Huber Heights, about twelve miles from the "
          "Beavercreek office, in the brick homes built between 1956 and 1992 and the newer "
          "construction around them. Most calls get handled the same day.",
   slots=[("Do original Huber homes have room for modern cooling?", [
    "The equipment closets and chases repeat across the stock, which makes the answer consistent "
    "rather than a surprise on the day. Where a coil or an air handler will physically fit is known "
    "before the survey rather than discovered during it, and that is the difference between an "
    "accurate quote and a revised one."])],
   # [NEEDS: tech confirmation on whether original Huber systems were sized for a later A/C add-on.
   # The paragraph above is deliberately general because that answer is missing.]
   faq=("My neighbor had the same fault last summer. Is that a coincidence?",
        "Probably not. Huber Heights houses share builder, date range and floor plan, so equipment "
        "ages and fails in patterns across a street rather than at random.")),
  "plumbing": dict(
   h1="Plumbers in {X}: repairs, water heaters and softeners",
   answer="We handle water heaters, drains, leaks and softeners in Huber Heights. The city "
          "treats its own water and softened it a few years back, from about 310 mg/L down to "
          "about 120. The plumbing line never closes.",
   slots=[("What did the Rip Rap Road project change?", [
    "Huber Heights treats its own water at the Rip Rap Road plant, drawing from the Great Miami "
    "Buried Valley Aquifer. The $11 million softening project took total hardness from about 310 "
    "mg/L to about 120 mg/L, roughly 18 grains per gallon down to about 7. A softener installed "
    "before that is still set for 18 grain water and is over-softening and wasting salt until it is "
    "adjusted."]),
    ("What does a Huber Heights plumbing permit cost?", [
    "Plumbing here goes to Public Health, Dayton &amp; Montgomery County, at the Reibold Building, "
    "117 S Main Street, Dayton. Its published fees are $45 for a new installation permit, $30 for a "
    "replacement, $14 per fixture or device, and $50 for sewer and water. A permit is required for "
    "installation, alteration or repair of plumbing systems, including replacement fixtures. There "
    "is a homeowner appliance application with affidavit for residential water heaters."])],
   faq=("Do I need a permit to swap a water heater myself in Huber Heights?",
        "Yes. Public Health, Dayton &amp; Montgomery County requires a permit for plumbing work "
        "including replacement fixtures, and publishes a homeowner appliance application with "
        "affidavit for residential water heaters.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Huber Heights, about twelve miles from "
          "the Beavercreek office, and every visit ends with a written report and photos. X-Plan "
          "covers both visits for $249 a year.",
   slots=[("What does a tune-up check in a Huber home?", [
    "The same short list, in the same places, which is the advantage of a repeating floor plan. The "
    "visit also catches the softener and humidifier question that came with the city's water change, "
    "because both are calibrated for water Huber Heights no longer delivers and both are within "
    "reach while the technician is already at the equipment."])],
   faq=("Is a tune-up worth it if the system is original to the house?",
        "On equipment that old the value is the safety check and an honest read on remaining life, "
        "more than efficiency. That is worth having before a cold snap rather than during one.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Huber Heights. "
          "Duct layouts repeat across the Huber Homes stock, so we know where the access points "
          "are before we get there. Every job gets photographed before and after.",
   slots=[("Why is a Huber Heights duct clean predictable?", [
    "Because the duct layout came off the same set of plans. Access points, trunk routing and "
    "register locations repeat across thousands of houses, so a negative-pressure clean can be "
    "planned rather than improvised. The camera still goes in first, and the footage still decides "
    "whether the job is worth doing on that specific house."])],
   faq=("Do you clean the dryer vent on the same visit?",
        "Yes, end to end, on the same visit.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Huber Heights, about "
          "twelve miles from the Beavercreek office. We measure humidity, particulates and "
          "ventilation in your house before recommending a thing.",
   slots=[("Will a whole-home filter fit in a Huber home?", [
    "The closet and chase dimensions repeat across the stock, so what fits in one house fits in the "
    "next. That means the answer is known before the visit rather than after it, including when the "
    "honest answer is that a four-inch media cabinet will not fit and a different filtration "
    "approach is needed."])],
   faq=("My humidifier pad keeps scaling. Will the water change help?",
        "It should. Huber Heights cut hardness from about 310 mg/L to about 120 mg/L, so a pad "
        "fitted before the project was sized for much harder water. Checking the humidifier and the "
        "softener together is the sensible order.")),
 }),

# ---------------------------------------------------------------- 9. Springboro
"springboro": dict(
 alt="A newer two-story neighborhood in Springboro, Ohio",
 answer="We cover Springboro from the Waynesville office, about eleven miles southeast. "
        "Heating, cooling and plumbing for a city that sits in two counties, Warren and "
        "Montgomery. Most get handled the same day, and the emergency line never closes.",
 sections=[
  ("Why does the answer change depending on the address?", [
   "Springboro straddles the Warren and Montgomery county line, and that is not trivia. It changes "
   "who inspects the work and who supplies the water, on the same city map. The City of Springboro "
   "runs its own state-certified Building Department at 320 W. Central Ave, and that covers building "
   "permits citywide. Plumbing is the split: the county plumbing departments handle it, and which "
   "county depends on which side of the line the house sits on."]),
  # [NEEDS: written confirmation from the Springboro Building Department, (937) 748-9791, covering
  # (a) the plumbing split as described and (b) whether a mechanical permit is required for a
  # like-for-like HVAC replacement. One aggregator claims a straight swap needs no permit there.
  # That contradicts Cincinnati and Kettering and is not published here.]
  ("Which water supply covers my side of the line?", [
   "On the Warren County side, Warren County Water &amp; Sewer, which finished nanofiltration "
   "membrane softening in 2022 and cut hardness by roughly 55%, down to about 8 grains per gallon "
   "across 30,000-plus customers. That means a softener installed before 2022 on that side of the "
   "city is still set for water that is no longer being delivered."]),
  # [NEEDS: the supplier and delivered hardness for the Montgomery County portion of Springboro.]
  ("What is different about newer Springboro housing?", [
   "Springboro's growth is concentrated in the 1990s through the 2010s, so the stock is newer, "
   "larger and more often two stories than anything else in the Dayton service area. Bigger "
   "two-story houses have a stack effect that a single system fights all year, which is why zoning "
   "and second-system conversations come up here far more than they do in Kettering or Dayton.",
   "Tighter modern construction also changes the ventilation question: these houses hold humidity "
   "and indoor air pollutants better than a 1950s ranch does, which is an argument for mechanical "
   "fresh air rather than for opening a window."]),
  # [NEEDS: ACS median household income, median home value and year-structure-built distribution.]
 ],
 table=dict(
  caption="Common problems in Springboro, Ohio homes and what to book",
  takeaway="Springboro's recurring problems come from two things: newer two-story houses, and a "
           "county line running through the middle of the city.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Upstairs runs hot while downstairs runs cold",
    "Stack effect in a larger two-story house on one system",
    "Zoning or second-system assessment", "Plan ahead"),
   ("Humidity stays high indoors in summer", "Tighter modern construction holding moisture",
    "Dehumidification assessment", "Book this month"),
   ("Stuffy air with no obvious cause", "Newer house with limited mechanical fresh air",
    "Ventilation assessment", "Book this month"),
   ("Softener behaving oddly on the Warren County side",
    "Set for pre-2022 hardness, now receiving about 8 grains", "Softener adjustment",
    "Book this month"),
   ("Confusion over which county inspects the work",
    "The city sits across the Warren and Montgomery line", "Ask the office before the job",
    "Before the work"),
   ("No heat or water on the floor", "Equipment or supply failure", "Emergency call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Which county am I in for permit purposes?",
   "It depends on the address. Springboro sits across the Warren and Montgomery county line, and "
   "plumbing is handled by the county departments while the City of Springboro runs its own building "
   "department at 320 W. Central Ave. We check the address before filing anything."),
  ("Did Springboro water get softer?",
   "On the Warren County side, yes. Warren County Water &amp; Sewer finished nanofiltration "
   "softening in 2022 and cut hardness by roughly 55%, to about 8 grains per gallon."),
  ("My two-story house never balances. Do I need two systems?",
   "Not always. Springboro's larger 1990s through 2010s houses often respond to zoning an existing "
   "system rather than adding a second one. Which one makes sense depends on the ductwork, and that "
   "is a survey, not a phone call."),
  ("Why is my newer house stuffier than my old one was?",
   "Tighter construction. Newer Springboro houses lose far less air through the shell, which is good "
   "for bills and bad for stale air and humidity. The fix is usually mechanical ventilation rather "
   "than a bigger system."),
  ("How far is the nearest office?",
   "About eleven miles. We dispatch Springboro work from the Waynesville office."),
 ],
 links=[("HVAC in Centerville", "/locations/centerville"),
        ("HVAC in Franklin", "/locations/franklin"),
        ("indoor air quality equipment", "/locations/springboro/indoor-air-quality")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Springboro, about eleven miles from "
          "the Waynesville office, including the larger two-story houses built across the city "
          "from the 1990s on. We answer the no-heat line at any hour, every day.",
   slots=[("Why does a two-story Springboro house never balance?", [
    "Stack effect. Warm air rises through a taller building envelope, so a single system fighting it "
    "heats the upper floor while the lower floor calls for more. Springboro's growth is concentrated "
    "in the 1990s through the 2010s, which produced more two-story houses than anywhere else on the "
    "Dayton side. Zoning an existing system usually costs less than a second system and solves the "
    "same complaint, and which one applies depends on the ductwork."])],
   faq=("Do I need two furnaces for a two-story house?",
        "Not usually. Zoning dampers on an existing system solve most Springboro balance complaints. "
        "A second system makes sense when the duct layout cannot be zoned or when a large addition "
        "changed the load.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Springboro, about eleven miles from the "
          "Waynesville office. Larger two-story houses here typically run hot upstairs and cold "
          "downstairs on a single system. Most calls get handled the same day.",
   slots=[("What fixes hot upstairs and cold downstairs?", [
    "Rarely a bigger condenser. In Springboro's larger two-story housing the complaint comes from "
    "stack effect and duct balance rather than capacity, and oversizing makes it worse by short "
    "cycling and removing less humidity. Zoning, damper adjustment and return placement address it "
    "directly, and a survey of the existing ductwork decides which combination applies."])],
   faq=("My upstairs is unusable in August. Is a second system the only answer?",
        "No. Zoning an existing system, adjusting dampers and adding return capacity fix most "
        "Springboro houses. A second system is the answer when the duct layout genuinely cannot be "
        "zoned.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Springboro. The city sits "
          "across the Warren and Montgomery county line, so plumbing permits go to two different "
          "county departments depending on your address. Emergency line answered at any hour.",
   slots=[("Which water supply covers a Springboro address?", [
    "On the Warren County side, Warren County Water &amp; Sewer, which completed nanofiltration "
    "membrane softening in 2022 and cut hardness by roughly 55% to about 8 grains per gallon for "
    "more than 30,000 customers. A softener installed before 2022 on that side is set for water that "
    "is no longer being delivered."]),
    ("Who inspects plumbing work in Springboro?", [
    "The county, and which county depends on the address. The City of Springboro runs its own "
    "state-certified Building Department at 320 W. Central Ave for building permits, while plumbing "
    "goes to the Warren or Montgomery County department."])],
   faq=("Which county handles my Springboro permit?",
        "It depends which side of the county line the address sits on. Springboro straddles the "
        "Warren and Montgomery line, and the address gets checked before anything is filed.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Springboro, about eleven miles from the "
          "Waynesville office. Even newer equipment needs documented annual service to keep the "
          "manufacturer warranty valid. X-Plan covers two visits a year for $249.",
   slots=[("Does newer equipment still need a tune-up?", [
    "Yes, and the warranty is the blunt reason. Most manufacturers require documented annual "
    "maintenance, and a claim on a system installed in the 2000s or 2010s can turn on whether there "
    "is a record. Every visit ends with a written report and photos for that purpose. Springboro's "
    "housing is newer than most of the service area, which makes this the page where warranty "
    "documentation matters most."])],
   faq=("My system is under warranty. Do I still need maintenance?",
        "Usually yes, to keep it valid. Manufacturers generally require documented annual service, "
        "and a written report with photos is what satisfies that requirement.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Springboro. "
          "Most of the city was built from the 1990s on, so the camera often shows your ductwork "
          "doesn't need cleaning. Every job gets photographed before and after.",
   slots=[("Does a newer Springboro house need duct cleaning?", [
    "Often not, and that is a real answer rather than a modest one. Ductwork installed in the 1990s "
    "or later, in a house that has not been renovated and has no pets, frequently comes back clean "
    "on camera. What does show up is construction debris left in the runs on newer builds and dryer "
    "vents that have never been cleared. The camera separates the two."])],
   faq=("My builder finished the house two years ago. Are the ducts dirty?",
        "Sometimes, and it is usually construction debris rather than accumulated dust. Drywall dust "
        "and offcuts left in the runs are common on new builds, and the camera finds them quickly.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Springboro, about eleven "
          "miles from the Waynesville office. Construction from the 1990s on is tighter and holds "
          "humidity and stale air, so we measure before recommending anything.",
   slots=[("Why is a newer house stuffier than an old one?", [
    "Because it leaks less. Springboro's 1990s through 2010s construction has a tight envelope, "
    "which is good for energy bills and bad for stale air and summer humidity. An older house "
    "exchanges air through its shell whether anyone wants it to or not. In a tighter house that "
    "exchange has to be built in, which is what an energy recovery ventilator does, and "
    "dehumidification handles the moisture side."])],
   faq=("Is opening a window enough?",
        "Not reliably, and not in July or January. In tighter Springboro construction a ducted "
        "energy recovery ventilator brings filtered outdoor air in without throwing away the heating "
        "or cooling, which a window does not.")),
 }),

# ---------------------------------------------------------------- 10. Troy
"troy": dict(
 alt="A residential street in Troy, Ohio",
 # [NEEDS: confirm what cities/troy.jpg shows. If it is the downtown public square the alt
 # becomes "The public square in downtown Troy, Ohio".]
 answer="We work out of 2950 Stone Cir Dr, right here in Troy, covering Miami County for "
        "heating, cooling and plumbing. Most calls get handled the same day, and the emergency "
        "line never closes.",
 sections=[
  ("Why does a Troy job need two permits?", [
   "Because two agencies split the work. The City of Troy contracts building permits out to the "
   "Miami County Building Department. A zoning permit comes from the City of Troy Planning "
   "Department at 100 S. Market Street and confirms the work complies with city zoning. The building "
   "permit, which covers construction, plumbing, electrical and mechanical, comes from Miami County. "
   "Two counters, one job. Nothing else in the service area works this way, and a contractor who has "
   "only worked Montgomery County will file in the wrong place."]),
  ("Where does Troy's water come from?", [
   "The city's own system. Troy pumps up to 4 million gallons a day from the Great Miami Buried "
   "Valley Aquifer through 116 miles of water main, 1,030 hydrants and three elevated storage tanks, "
   "Herrlinger, Stanfield and Barnhart, holding 3.5 million gallons between them."]),
  # [NEEDS: Troy's delivered hardness from the city's Consumer Confidence Report, and whether Troy
  # softens at the plant. Aquifer-sourced water is hard raw; the finished figure is not guessed.]
  ("Who supplies electricity to a Troy house?", [
   "AES Ohio. Troy does not run a municipal electric utility, even though several nearby Miami "
   "County communities do. It is worth checking whose grid a house is actually on before applying "
   "anything a neighboring town's homeowner was told about their own utility."]),
  # [NEEDS: confirm CenterPoint Energy Ohio supplies natural gas to Troy.]
  # The research also carried a Troy radon figure. Struck in full: Extreme does not perform radon
  # mitigation, and publishing the number invites work the company does not do.
 ],
 table=dict(
  caption="Common problems in Troy, Ohio homes and what to book",
  takeaway="Troy runs a permit process no other city we cover uses, and its water comes straight "
           "out of the buried valley aquifer.",
  columns=["What you're seeing", "Likely cause", "Service to book", "Urgency"],
  rows=[
   ("Permit filed with the wrong office",
    "City handles zoning, Miami County handles the building permit",
    "Ask the office before the job", "Before the work"),
   ("Older downtown house has no duct space", "Pre-war structure with no chases",
    "Ductless or high-velocity survey", "Plan ahead"),
   ("Water heater scaling early", "Untreated aquifer water is hard", "Water heater service",
    "Book this month"),
   ("Basement feels damp through the summer", "Limited ventilation below grade",
    "Dehumidification assessment", "Book this month"),
   ("Advice from a nearby town does not apply here",
    "Troy is on AES Ohio while some Miami County communities run municipal electric",
    "Ask the office before you sign", "Before the work"),
   ("No heat overnight", "Ignition, control or gas valve failure", "Emergency heating call",
    "Call 24/7 now"),
  ]),
 faq=[
  ("Where is the Troy office?",
   "2950 Stone Cir Dr, Troy, OH 45373. Office staff are in Monday to Friday, 8:00 AM to 5:00 PM, and "
   "the emergency line at " + PHONE + " is answered 24/7 every day of the year."),
  ("Do I need one permit or two in Troy?",
   "Two. The City of Troy issues the zoning permit from the Planning Department at 100 S. Market "
   "Street, and the Miami County Building Department issues the building permit covering "
   "construction, plumbing, electrical and mechanical work."),
  ("Who supplies electricity in Troy?",
   "AES Ohio. Troy does not have a municipal electric utility, unlike several nearby Miami County "
   "communities, which matters when checking what a utility program actually covers."),
  ("Where does Troy's drinking water come from?",
   "The City of Troy runs its own municipal system, pumping up to 4 million gallons a day from the "
   "Great Miami Buried Valley Aquifer through 116 miles of water main."),
  ("Do you cover the rest of Miami County from the Troy office?",
   "Yes. The Troy office at 2950 Stone Cir Dr covers Miami County and the I-75 corridor north, and "
   "the emergency line at " + PHONE + " is answered 24/7."),
 ],
 links=[("HVAC in Tipp City", "/locations/tipp"),
        ("HVAC in Vandalia", "/locations/vandalia"),
        ("office addresses and hours", "/contact")],
 svc={
  "heating": dict(
   answer="We repair and replace furnaces and heat pumps in Troy, from the office at 2950 Stone "
          "Cir Dr. A replacement here needs a city zoning permit and a county building "
          "permit. We pull both. The no-heat line never closes.",
   slots=[("Why does a Troy replacement need two permits?", [
    "Because the City of Troy contracts building permits out to Miami County. The zoning permit "
    "comes from the City of Troy Planning Department at 100 S. Market Street and confirms the work "
    "complies with city zoning. The building permit, covering construction, plumbing, electrical and "
    "mechanical, comes from the Miami County Building Department. Nothing else in the service area "
    "splits it this way, and a contractor who has only worked Montgomery County will file in the "
    "wrong place."])],
   faq=("How close is the nearest technician to Troy?",
        "The office is at 2950 Stone Cir Dr in Troy, so trucks covering the city and the rest of "
        "Miami County start their day inside it.")),
  "cooling": dict(
   answer="We repair and replace air conditioners in Troy, from the office at 2950 Stone Cir Dr, "
          "and cover Miami County and the I-75 corridor north. Most calls get handled the same "
          "day, and we answer the line at any hour.",
   slots=[("Who supplies electricity in Troy, and why does it matter?", [
    "AES Ohio. Troy does not run a municipal electric utility, even though several nearby Miami "
    "County communities do, and what a utility offers its own customers differs between them. "
    "Anyone comparing something a neighboring town's homeowner was told should check whose grid the "
    "house is actually on first."])],
   # [NEEDS: current AES Ohio residential HVAC programme details. No figure is published here, and
   # no trade-ally status is claimed.]
   faq=("Does the electric utility change anything about a new system in Troy?",
        "Only in what the utility itself offers. Troy is on AES Ohio, and several nearby Miami "
        "County towns run their own municipal electric utilities, so what applies a few miles away "
        "does not automatically apply here.")),
  "plumbing": dict(
   answer="We handle water heaters, drains, leaks and sewer lines in Troy, from the office at "
          "2950 Stone Cir Dr. The city pumps its own water out of the Great Miami Buried Valley "
          "Aquifer. We answer the line at any hour.",
   slots=[("Where does Troy's water come from?", [
    "The city's own system. Troy pumps up to 4 million gallons a day from the Great Miami Buried "
    "Valley Aquifer through 116 miles of water main and 1,030 hydrants, into three elevated storage "
    "tanks called Herrlinger, Stanfield and Barnhart, holding 3.5 million gallons between them."]),
    ("Who issues a plumbing permit in Troy?", [
    "Miami County. The City of Troy contracts building permits, which cover plumbing, out to the "
    "Miami County Building Department, while zoning permits come from the City of Troy Planning "
    "Department at 100 S. Market Street."])],
   faq=("Do I need a softener in Troy?",
        "That is a measurement rather than a rule of thumb. Troy runs its own municipal system off "
        "the Great Miami Buried Valley Aquifer, and a water test at the tap answers it for a "
        "specific address.")),
  "maintenance": dict(
   answer="We tune up furnaces and air conditioners in Troy, from the office at 2950 Stone Cir "
          "Dr, and every visit ends with a written report and photos. X-Plan covers both visits "
          "for $249 a year.",
   slots=[("Does a Troy tune-up need a permit?", [
    "No. The two-permit process in Troy applies to installation and replacement work, not to "
    "maintenance. A tune-up is a visit, not a construction job, and nothing goes to the City of Troy "
    "Planning Department or the Miami County Building Department for it."])],
   faq=("How far ahead should I book a tune-up in Troy?",
        "Spring for cooling and autumn for heating, before the first hot or cold week rather than "
        "during it. Those two windows fill fastest.")),
  "duct-cleaning": dict(
   answer="We clean supply ducts, returns, blower compartments and dryer vents in Troy, from the "
          "office at 2950 Stone Cir Dr. A camera goes into your ductwork before we quote "
          "anything, and every job gets photographed before and after.",
   slots=[("Does Troy's older housing change the job?", [
    "It changes what the camera finds. Troy has a substantial pre-war downtown and historic "
    "residential core alongside post-war and recent subdivision growth on the edges, so a job "
    "downtown and a job on the edge of town are different systems with different access. The footage "
    "decides the quote either way."])],
   # [NEEDS: ACS median year structure built and pre-1940 share for Troy.]
   faq=("Do you clean dryer vents in Troy?",
        "Yes, end to end, usually on the same visit as the ductwork.")),
  "indoor-air-quality": dict(
   answer="We install filtration, humidity control and ventilation in Troy, from the office at "
          "2950 Stone Cir Dr. We measure humidity, particulates and ventilation in your house "
          "before recommending a thing.",
   # The research proposed a radon-average section here. Struck: Extreme does not do radon work.
   slots=[("What does a Miami County basement usually need?", [
    "Moisture control before anything else. Troy's older housing has full basements below grade and "
    "the newer subdivisions on the edge of town are tighter than the stock downtown, so the same "
    "complaint has two different causes. A whole-home dehumidifier handles standing summer humidity, "
    "and a ducted energy recovery ventilator handles stale air in a tight house. Which one applies "
    "comes from the measurement, not from the age of the house alone."])],
   faq=("Do you test the air before recommending equipment?",
        "Yes. Humidity, particulates and ventilation get measured first and measured again after "
        "installation, so the difference is visible rather than asserted.")),
 }),
}

# Sanity: the copy deck and the indexed set are the same ten, and every one of them
# fills all six service slots. A page that cannot fill its local slots is not indexed,
# and this assert is what keeps that rule from drifting.
assert set(LOCAL) == L.FEATURED, (
    f"LOCAL and locations.FEATURED disagree: {set(LOCAL) ^ L.FEATURED}")
for _s, _d in LOCAL.items():
    assert set(_d["svc"]) == set(SERVICE_ORDER), f"{_s} is missing service copy"
    assert len(_d["sections"]) == 3, f"{_s} needs three local hub sections"
del _s, _d


# The homepage's real curated Google reviews, not invented placeholders. Each city
# shows three, rotated deterministically by its position in the list so 38 pages
# don't all repeat the same trio — the handoff warns specifically against pure
# find-replace pages. Same pool, different slice.
#
# To show the SAME three everywhere instead, return REVIEWS[:3] from city_reviews().
from reviews import REVIEWS

def city_reviews(slug, n=3):
    i = L.ALL.index(next(x for x in L.ALL if x[0] == slug))
    return [REVIEWS[(i * n + k) % len(REVIEWS)] for k in range(n)]

# ---------------------------------------------------------------- promos
T.PROMOS["locFinanceHeat"] = dict(cls="lav", t="New furnace, monthly payments",
    d="Finance a replacement through GoodLeap, Synchrony, or Wright-Patt Credit Union.",
    lm="Financing Options →", href="/financing-options")
T.PROMOS["locFinanceCool"] = dict(cls="lav", t="New AC, monthly payments",
    d="Finance a replacement through GoodLeap, Synchrony, or Wright-Patt Credit Union.",
    lm="Financing Options →", href="/financing-options")
T.PROMOS["locFinanceTankless"] = dict(cls="lav", t="Tankless upgrade, monthly payments",
    d="Water heaters and repiping qualify for financing through our lenders.",
    lm="Financing Options →", href="/financing-options")
T.PROMOS["locFinanceAging"] = dict(cls="lav", t="Aging system on borrowed time?",
    d="If a tune-up finds bigger trouble, replacements can be financed monthly.",
    lm="Financing Options →", href="/financing-options")
T.PROMOS["locXplan"] = dict(cls="mint", t="Never think about tune-ups again",
    d="X-Plan includes two a year, 15% off repairs, and priority scheduling.",
    lm="Explore X-Plan →", href="/maintenance")
T.PROMOS["locXplanPlumb"] = dict(cls="mint", t="X-Plan members skip the line",
    d="Priority scheduling and discounted service calls — plumbing visits included.",
    lm="Explore X-Plan →", href="/maintenance")
T.PROMOS["locSpecialTuneUp"] = dict(cls="mint", t="$79 tune-up special",
    d="One-time seasonal tune-up — see current offers before you book.",
    lm="See Specials →", href="/specials")

def _cross(city_slug, city, kind):
    """5f and 5g cross-link to each other within the same city."""
    if kind == "locIaqCross":
        return dict(cls="mint", t="Pair it with air quality",
                    d="Clean ducts plus filtration keeps the dust from coming right back.",
                    lm=f"{city} Air Quality →", href=f"/locations/{city_slug}/indoor-air-quality")
    return dict(cls="mint", t="Start with clean ducts",
                d="Filtration works best when the ductwork behind it isn't full of dust.",
                lm=f"{city} Duct Cleaning →", href=f"/locations/{city_slug}/duct-cleaning")

# ---------------------------------------------------------------- per-city data
def neighbors(slug, group, n=10):
    """The other towns in the same metro. This is the one genuinely per-city block on
    the page, and the handoff names it as what keeps these from being find-replace.

    Indexed communities sort first. That is the whole point of keeping the tail: link
    equity and topical signal flow toward the ten rather than around them in a circle.
    Order within each half is list order, which is the live Framer page-tree order.

    [NEEDS: lat/long or an adjacency table in builder/locations.py so this can be
    genuinely nearest-first rather than featured-first. The file already carries a TODO
    about adding ZIPs and it is the same missing data.]"""
    pool = {"Dayton": L.DAYTON, "Cincinnati": L.CINCINNATI, "Counties": L.COUNTIES}[group]
    others = [(s, nm) for s, nm in pool if s != slug]
    return sorted(others, key=lambda x: x[0] not in L.FEATURED)[:n]


def office_line(slug):
    """(office town, street or None, distance phrase or None) for an indexed city."""
    return L.OFFICE[slug]


def geo_speed(slug, long):
    """H2 3 on an indexed hub. Built from locations.OFFICE so the distance is the
    researched mileage rather than a response-time promise."""
    town, street, dist = office_line(slug)
    where = (f"start their day at the office on {street}, inside the city" if street
             else f"start their day at the {town} office, {dist}")
    return ("We answer the emergency line at any hour and handle 90% of calls the same day. "
            f"The trucks covering {long} {where}.")


def geo_serve(slug, long):
    """H2 1 on an indexed hub."""
    town, street, dist = office_line(slug)
    where = ("one of the towns we are actually based in" if street
             else f"a short run from the {town} office")
    return (f"Yes. {long} is {where}, so it gets covered every day rather than whenever "
            "someone happens to be passing. Both trades book through the same number, and we "
            "answer the emergency line whatever time it is.")


def _qa_section(h2, body):
    """One H2 question with its direct answer under it, no eyebrow. The location pages
    use the eyebrow for marketing labels; a question heading does not want one."""
    return T.content_section({"h2": h2, "body": body})


def _local_links(items):
    """Descriptive cross-links out of a city page. No eyebrow-plus-H2 wrapper, because
    these are navigation rather than a section of the page, and the hub already runs
    seven H2s. Anchor text always names the destination."""
    links = "".join(f'<a href="{href}">{anchor}</a>' for anchor, href in items)
    return ('<div class="xlc-rel"><div class="xsp-eyebrow purple">MORE FROM EXTREME</div>'
            f'<div class="xlc-rellinks">{links}</div></div>')

def metro_adj(group):
    return {"Dayton": "Miami Valley", "Cincinnati": "Cincinnati-area",
            "Counties": "southwest Ohio"}[group]

def fill(text, city, group):
    return (text.replace("{CITYU}", city.upper()).replace("{CITY}", city)
                .replace("{METRO_ADJ}", metro_adj(group)))

NO_TOWN_NOTE = ('<div class="xlc-note">Don&#39;t see your town? If you&#39;re close to one '
                'that&#39;s listed, call — if we can reach you, we will.</div>')

# ---------------------------------------------------------------- renderers
def _county_answer(slug, name):
    """The nine county overviews. Deliberately the thinnest page type on the site and
    noindexed by shell.noindex(): a county page is always a superset of its city pages,
    so it does one job, which is listing them. No county housing-stock copy — it would
    contradict the city pages underneath it."""
    kids = [nm for s, nm in L.ALL if s in L.COUNTY_CITIES.get(slug, [])]
    # Preble and Darke have no covered community with a page of its own, so they get a
    # coverage sentence instead of an invented town list.
    covered = (f" That includes {', '.join(kids[:-1])} and {kids[-1]}."
               if len(kids) > 1 else (f" That includes {kids[0]}." if kids else
                                      " Every town books through the same number."))
    return (f"We cover {name} for heating, cooling, air quality and plumbing.{covered} Most "
            "calls get handled the same day, and someone answers the emergency line at any hour.")


def _tail_answer(slug, city, group):
    """Answer block for a community with no local research behind it. The city name is
    the only thing that varies, and that is the honest position: there is no fact base
    for 28 more places and inventing one is worse than omitting it.

    [NEEDS: nearest office and approximate mileage for each of the 19 remaining cities.
    Until those are supplied this block names no office and claims no distance, because
    a wrong drive time is a broken promise rather than a thin page.]"""
    if group == "Counties":
        return _county_answer(slug, city)
    # A town that holds one of the four offices is not a page with no fact base — the
    # address is the fact, and it is client-confirmed. It gets named rather than being
    # given the same sentence as a town we only drive to.
    office = L.OFFICE.get(slug)
    if office and office[1]:
        return (f"Yes, and {city} is one of the four towns we work out of. The office is at "
                f"{office[1]}, so heating, cooling, air quality and plumbing all start from "
                "inside the village. One number books any of it, and someone answers the "
                "emergency line at any hour.")
    return (f"Yes, we cover {city}. Heating, cooling, air quality and plumbing all book through "
            "one number, most calls get handled the same day, and someone answers the emergency "
            "line at any hour.")


def _tail_routes(slug, group):
    """Upward and sideways links out of a noindexed page: the indexed metro parent plus
    one or two indexed neighbors. This is the reason these pages are kept at all."""
    metro = ("dayton" if group == "Dayton" else
             "cincinnati" if group == "Cincinnati" else None)
    names = dict(L.ALL)
    out = []
    if metro:
        out.append((f"{names[metro]} HVAC and plumbing services", f"/locations/{metro}"))
    for s in L.TAIL_LINKS.get(slug, []):
        out.append((f"HVAC in {L.long_name(s, names[s])}", f"/locations/{s}"))
    if group == "Counties":
        for s in L.COUNTY_CITIES.get(slug, [])[:3]:
            out.append((f"HVAC and plumbing in {L.long_name(s, names[s])}", f"/locations/{s}"))
    return out


def city_overview(city, slug, group):
    featured = slug in L.FEATURED
    long = L.long_name(slug, city)
    f = lambda t: fill(t, city, group)
    cards = []
    for s, label, desc in OVERVIEW_CARDS:
        pill = ("NEW", f"{city} {label.lower()} →") if s == "plumbing" else (None, f"{city} {label.lower()} →")
        cards.append((label, f(desc), f"/locations/{slug}/{s}", pill))
    towns = "".join(
        f'<div class="xlc-town"><span class="c">✓</span>'
        f'<a href="/locations/{ns}">{nn}</a></div>' for ns, nn in neighbors(slug, group))
    hero_img = T.cdn_asset(L.hero(slug))

    if featured:
        d = LOCAL[slug]
        # The seven-H2 outline. Slots 4, 5 and 6 are the local ones and are required
        # fields, which is what makes these ten non-duplicate by construction rather
        # than by good intentions.
        h1, hi = "HVAC and plumbing services in {X}", f"{long}, Ohio"
        answer = d["answer"]
        photo_alt = d["alt"]
        intro = ("Local techs who know " + metro_adj(group) + " homes, one number for both "
                 "trades, and most calls handled the same day.")
        # "{city}-Based Techs" was false on every city but the three that hold an
        # office — Kettering's badge said "Kettering-Based Techs" while its own body
        # copy said the work runs out of Beavercreek. The claim stays only where it
        # is true; everywhere else the chip falls back to a proof point that is.
        chips = [(f"{city} Office" if slug in D.OFFICE_BY_SLUG else "Locally Owned"),
                 "90% Same-Day Service", "24/7 Emergency Line"]
        sections = [
            # H2 1 doubles as the heading over the service card grid, so the grid stops
            # being an unlabelled block under a slogan. The slogan the grid used to
            # carry ("Everything your house throws at you.") was identical on 38 pages.
            _cards(f"SERVICES IN {city.upper()}",
                   f"Do you serve {long}, Ohio?", cards,
                   lead=geo_serve(slug, long)),
            _qa_section(GEO_COVERED_H2, geo_covered(slug)),
            _qa_section(GEO_SPEED_H2, geo_speed(slug, long)),
        ]
        for h2, body in d["sections"]:
            sections.append(_qa_section(h2, body))
        sections.append(T.table_section(dict(d["table"], eyebrow="WHAT WE SEE MOST",
                                             h2="Which problems come up most here?")))
        sections.append(_qa_section(GEO_BOOK_H2, GEO_BOOK))
        # Deliberately not "communities near {City}": the deck's own three local H2s
        # already name the city, and the contract caps that at two. The headings this
        # module owns give the budget back to the researched ones.
        sections.append(section("SERVICE AREA", "Which nearby communities are covered?",
            f'<div class="xlc-towns">{towns}</div>'
            f'<div class="xlc-note">Outside the list? Call — if we can reach you, we will.</div>'
            f'<div style="margin-top:20px">{T.photo_slot("", hero_img, photo_alt)}</div>'))
        sections.append(T.faq([{"q": q, "a": a} for q, a in d["faq"]], "COMMON QUESTIONS",
                              h2="Your questions, answered."))
        # The review pool carries no city attribution, so the heading makes no city
        # claim. [NEEDS: review excerpts tagged with the customer's city — tagging even
        # five per indexed metro turns the weakest block on the page into the strongest.]
        revs = "".join(
            f'<div class="xlc-rev"><div class="stars">★★★★★</div><div class="q">“{q}”</div>'
            f'<div class="who">{who}{f" <span>· {rc}</span>" if rc else ""}</div></div>'
            for q, who, rc in city_reviews(slug))
        sections.append(section("WHAT CUSTOMERS SAY", "What do customers say about the work?",
                                f'<div class="xlc-revs">{revs}</div>'))
        sections.append(_local_links(d["links"]))
    else:
        # The noindexed tail. It keeps serving users — the service children, the
        # neighbour list, the booking path — and is deliberately, visibly thinner:
        # a real answer block, then it routes into the indexed ten. No local facts,
        # because the research does not exist for these places.
        h1, hi = "Heating, air &amp; plumbing — {X}", f"right here in {city}"
        answer = _tail_answer(slug, city, group)
        # The stand-in photo (see locations.HERO_OVERRIDES) must not be captioned as
        # the town it is not.
        photo_alt = ("Warren County, Ohio, where the Waynesville office sits"
                     if slug == "waynesville" else
                     f"A residential street in {city}, Ohio")
        intro = (f"Local techs who know {metro_adj(group)} homes. One number, and most "
                 "calls handled the same day.")
        # "{city}-Based Techs" was false on every city but the three that hold an
        # office — Kettering's badge said "Kettering-Based Techs" while its own body
        # copy said the work runs out of Beavercreek. The claim stays only where it
        # is true; everywhere else the chip falls back to a proof point that is.
        chips = [(f"{city} Office" if slug in D.OFFICE_BY_SLUG else "Locally Owned"),
                 "90% Same-Day Service", "24/7 Emergency Line"]
        sections = [
            _cards(f"SERVICES IN {city.upper()}", f"What work is covered in {city}?", cards,
                   lead=geo_covered(slug)),
            section("SERVICE AREA", "Which nearby communities are covered?",
                f'<div class="xlc-towns">{towns}</div>'
                f'<div class="xlc-note">Outside the list? Call — if we can reach you, we will.</div>'
                f'<div style="margin-top:20px">{T.photo_slot("", hero_img, photo_alt)}</div>'),
            _qa_section(GEO_BOOK_H2, GEO_BOOK),
            _local_links(_tail_routes(slug, group)),
        ]

    body = f'''{_hero(city,
        [("Home", "/"), ("Locations", "/locations"), (city, "")],
        h1, hi, intro, chips,
        _book(f"SERVING {city.upper()}", "90% same-day service.",
              f"Techs dispatched across {METRO_BLURB[group]} — book online in about a "
              f"minute, or call and talk to a real person.", trust2=f"{city}-based techs"),
        answer=answer)}
<div class="xco-body">
  {"".join(sections)}
  {_stat_panel([("20+", f"years serving {METRO_BLURB[group]}"), ("4.9", "average customer rating"),
                ("90%", "same-day service"), ("24/7", "emergency service line")])}
</div>
{_band("No heat, no AC, or water where it shouldn't be?",
       f"The {city} line is answered 24/7 — nights, weekends, holidays.")}'''
    return shell(f"xsp-loc-{slug}", body, extra_css=LOC_CSS)

def city_service(city, slug, group, service):
    c = SERVICE_COPY[service]
    featured = slug in L.FEATURED
    long = L.long_name(slug, city)
    f = lambda t: fill(t, city, group)
    d = LOCAL[slug]["svc"][service] if featured else None

    if featured:
        # The indexed pages take the keyword H1 and the local slots. The tail keeps the
        # branded H1 from SERVICE_COPY, which is part of what makes the two sets tell
        # themselves apart at a glance.
        h1 = d.get("h1", GEO_SERVICE_H1[service])
        hi = f"{long}, Ohio"
        answer = d["answer"]
    else:
        h1, hi = f(c["h1"]), f(c["hi"])
        answer = (f"We {TAIL_VERB[service]} in {city}, Ohio. {TAIL_SCOPE[service]} Most calls "
                  "get handled the same day, and someone answers the emergency line at any hour.")

    # Heading picker: the interrogative form on the indexed ten, the branded deck on
    # the tail. `f` still runs over both so {CITY} substitution is unaffected.
    def hh(key):
        alt = GEO_SCAFFOLD_H2.get(service, {}).get(key) if featured else None
        return f(alt.replace("{C}", long)) if alt else f(c[key])

    left = []
    if c.get("sec1") == "checks" or (c.get("checks") and "cards" not in c):
        left.append(_checklist(f(c["chkEyebrow"]), hh("chkH2"), c["checks"], c.get("chkNote")))
    if "cards" in c:
        left.append(_cards(f(c["gridEyebrow"]), hh("gridH2"),
                           [(t, f(d2), None, None) for t, d2 in c["cards"]],
                           lead=(TAIL_SCOPE[service] if featured else None)))
    # The city slots. On heating/cooling/maintenance/duct-cleaning/IAQ that is one H2;
    # on plumbing it is two, water supply and permit authority. They go directly after
    # the shared "what we handle" grid so the local material is above the fold-ish
    # rather than buried under the promos.
    if featured:
        for h2, body in d["slots"]:
            left.append(_qa_section(h2, body))
    sec2 = c.get("sec2") if featured else None
    # The noindexed tail drops sec2 entirely. Every one of those blocks is shared copy
    # rendered identically on 38 pages, so cutting it from the suppressed set raises the
    # unique-to-boilerplate ratio on exactly the pages that need it and makes the tail
    # measurably thinner, which is the point of suppressing it.
    if sec2 == "decision":
        inner = "".join(f'<div class="xco-ccard"><span class="c">✓</span>'
                        f'<div class="t">{t}</div><div class="d">{d2}</div></div>'
                        for t, d2 in c["dec"])
        left.append(section(f(c["decEyebrow"]), hh("decH2"),
                            f'<div class="xco-2col">{inner}</div>'
                            f'<div class="xlc-note">{c["decNote"]}</div>'))
    elif sec2 == "checks" and "cards" in c:
        left.append(_checklist(f(c["chkEyebrow"]), hh("chkH2"), c["checks"], c.get("chkNote")))
    elif sec2 == "purple":
        items = "".join(f'<li><span class="c">✓</span><span><b>{t}</b> {d2}</span></li>'
                        for t, d2 in c["purple"])
        left.append(f'<div class="xlc-xp"><div class="eyebrow">{f(c["purpleEyebrow"])}</div>'
                    f'<h3>{f(c["purpleH2"])}</h3><ul>{items}</ul></div>')
    elif sec2 == "steps":
        left.append(T.process({"h2": hh("stepsH2"),
                               "steps": [{"title": t, "desc": d2} for t, d2 in c["steps"]]},
                              eyebrow=f(c["stepsEyebrow"])))
    elif sec2 == "xplan":
        # The shared panel, not a copy of it. X-Plan pricing and member rates live in
        # T.XPLAN, so a change there updates the hub, /maintenance and all 38 location
        # maintenance pages together. The member service-fee line inside XPLAN["detail"]
        # is a card body, which is where client decision 2026-08-02 allows it.
        left.append(T.xplan_panel(detail=True))

    # One city-specific FAQ per indexed service page, on top of everything the shared
    # scaffold already answers. The tail gets no FAQ block at all.
    if featured:
        # The contract caps the city name at two H2s per page. Plumbing is the only
        # service with two city slots, so on those pages naming the city a third time
        # in the booking heading would break it. Counted rather than hardcoded, because
        # not every city slot happens to name its city.
        book = GEO_SCAFFOLD_H2[service]["book"]
        named = sum(1 for h2, _ in d["slots"] if long in h2)
        left.append(_qa_section(
            book.replace(" in {C}", "").replace("{C}", long) if named >= 2
            else book.replace("{C}", long), GEO_SERVICE_BOOK))
        left.append(T.faq([{"q": d["faq"][0], "a": d["faq"][1]}], "COMMON QUESTIONS",
                          h2="Your questions, answered."))
        left.append(_local_links([
            (f"{long} HVAC and plumbing services", f"/locations/{slug}"),
            ("X-Plan maintenance membership", "/maintenance")]))
    else:
        left.append(_local_links(
            [(f"{city} HVAC and plumbing services", f"/locations/{slug}")]
            + _tail_routes(slug, group)))

    promos = []
    for p in c["promos"]:
        if p in ("locIaqCross", "locDuctCross"):
            key = f"{p}-{slug}"
            T.PROMOS[key] = _cross(slug, city, p)
            promos.append(key)
        else:
            promos.append(p)
    rail = {"photo": T.cdn_asset(c["photo"]), "photoAlt": c["photoAlt"],
            "photoPos": c.get("photoPos"), "promos": promos}
    left.append(T.mobile_inline_rail({"rail": rail}))
    # The photo goes to the top of the body on mobile, not inline with the promos.
    left.insert(0, T.mobile_photo(rail))

    body = f'''{_hero(city,
        [("Home", "/"), ("Locations", "/locations"), (city, f"/locations/{slug}"), (c["nav"], "")],
        h1, hi, f(c["intro"]), c["chips"],
        _book(f(c["bookEyebrow"]), c.get("bookTitle", "90% same-day service."),
              c.get("bookSub", "Book online in about a minute, or call and talk to a real person."),
              label=c.get("bookLabel", "Schedule Service"), trust2=f"{city}-based techs"),
        pill=f(c["pill"]) if c.get("pill") else "", answer=answer)}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {T.rail(rail)}
</div>
{_band(f(c["bandT"]), f(c["bandS"]), c.get("bandCta", "call"))}'''
    return shell(f"xsp-loc-{slug}-{service}", body, extra_css=LOC_CSS)

def hub():
    metros = []
    # The metro card names the metro itself, not whatever happens to sort first in the
    # list — L.CINCINNATI leads with Blue Ash, which is not the metro.
    # Atlist service-area maps, carried over from the previous hub — same embed IDs.
    # These are the client's own maps; the photo cards the mockup showed are replaced
    # by them at the client's direction.
    MAPS = {
        "dayton": ("d1e71909-39c0-4d7e-ab21-5d63f440a852", "Dayton service area map"),
        "cincinnati": ("010b1b45-cc77-4644-b0e8-8492892ea87b", "Cincinnati service area map"),
    }
    for label, slug, name, blurb in [
        ("DAYTON METRO", "dayton", "Dayton",
         "Kettering, Beavercreek, Centerville, Springboro, Huber Heights, and 15+ more communities."),
        ("CINCINNATI METRO", "cincinnati", "Cincinnati",
         "Mason, West Chester, Fairfield, Middletown, Blue Ash, and more communities."),
    ]:
        map_id, map_label = MAPS[slug]
        metros.append(f'''<div class="xlc-metro">
  <div class="xlc-map" aria-label="{map_label}">
    <iframe src="https://my.atlist.com/map/{map_id}?share=true"
      allow="geolocation \'self\' https://my.atlist.com" loading="lazy" scrolling="no"
      allowfullscreen title="{map_label}"></iframe>
  </div>
  <div class="body">
    <div><div class="eyebrow">{label}</div>
      <div class="t">{name} &amp; the surrounding area</div>
      <div class="d">{blurb}</div></div>
    <a class="cta" href="/locations/{slug}">{name} Service Area →</a>
  </div>
</div>''')
    cols = []
    for label, items in [("DAYTON METRO", L.DAYTON), ("CINCINNATI METRO", L.CINCINNATI),
                         ("COUNTIES WE COVER", L.COUNTIES)]:
        links = "".join(f'<a href="/locations/{s}">{n}</a>' for s, n in items)
        cols.append(f'<div class="xlc-dircol"><div class="lab">{label}</div>'
                    f'<div class="xlc-links">{links}</div></div>')
    zip_card = f'''<div class="xsp-book">
  <div class="eyebrow">FIND YOUR AREA</div>
  <div class="t">Are we in your neighborhood?</div>
  <div class="s">Type a town and we&#39;ll take you straight to its page.</div>
  <div class="xlc-zip">
    <input id="xlc-zip" type="text" inputmode="numeric" maxlength="30" placeholder="ZIP code or town name"
           aria-label="ZIP code or town name">
  </div>
  <div class="btns" style="margin-top:10px">
    <a class="xsp-btn-green" href="#" id="xlc-zipgo" role="button">Check My Area</a>
  </div>
  <div class="xlc-zipmsg" id="xlc-zipmsg" role="status" aria-live="polite"></div>
  <div class="trust"><span><span class="st">★</span> 4.9 average rating</span><span class="bar">|</span><span>24/7 emergency line</span></div>
</div>'''
    # The hub answer block and its H2 outline are copy-locations.md §1. Four offices,
    # one phone number, and the towns list underneath.
    hub_answer = ("We cover the Dayton and Cincinnati, Ohio metros for heating, cooling, air "
                  "quality and plumbing, working out of four offices: Beavercreek, Mason, Troy "
                  "and Waynesville. One number reaches all four, and the emergency line never "
                  "closes.")
    body = f'''{_hero("", [("Home", "/"), ("Locations", "")],
        "HVAC and plumbing service areas across {X}", "the Dayton and Cincinnati metros",
        "Find your community below. One phone number covers them all.",
        ["2 Metro Areas", f"{len(L.ALL)}+ Communities", "90% Same-Day Service"], zip_card,
        card_class="zip", ctas=False, answer=hub_answer)}
<div class="xco-body">
  {section("SERVICE AREAS", "Which Ohio metros do you cover?",
    T.paragraphs("The Dayton metro, the Cincinnati metro, and the counties wrapped around both. "
                 "Every town below has its own page. If yours isn't on the list but sits next "
                 "to one that is, the answer is usually yes, and one call settles it faster "
                 "than a map does.") + "".join(metros))}
  {T.content_section({"h2": "Where are the four offices?", "body":
    "Beavercreek at 712 N Fairfield Rd covers the Dayton side. Mason at 5633 Tylersville Rd "
    "covers the Cincinnati side. Troy at 2950 Stone Cir Dr covers Miami County and the I-75 "
    "corridor north. Waynesville at 141 North St sits between the two metros."})}
  {T.content_section({"h2": "Does one phone number reach all four offices?", "body":
    f"Yes. {PHONE} gets you dispatch for every town we cover, at any hour. There's no local "
    "number to hunt down and no cutoff time on the emergency line. The office itself is staffed "
    "Monday to Friday, 8:00 AM to 5:00 PM."})}
  {section("ALL COMMUNITIES", "Which communities have their own page?",
    T.paragraphs("Pick your town below and you land on its own page, with heating, cooling, "
                 "plumbing, maintenance, duct cleaning and air quality underneath it. A Kettering "
                 "plumbing question gets the Kettering plumbing page, not a generic one.")
    + f'<div class="xlc-dir">{"".join(cols)}</div>' + NO_TOWN_NOTE)}
  {T.content_section({"h2": GEO_BOOK_H2, "body": GEO_BOOK})}
  {_stat_panel([(f"{len(L.ALL)}+", "communities served"), ("4.9", "average customer rating"),
                ("90%", "same-day service"), ("24/7", "emergency service line")])}
</div>
{_band("Not sure if we cover you?",
       "One call settles it — and if we can't help, we'll point you to someone who can.")}'''
    return shell("xsp-locations", body + ZIP_JS, extra_css=LOC_CSS)

# The hub's lookup box. Emitted at the end of the hub body so the markup it binds to
# already exists — sitting it in the <style> block put it ahead of the input, and it
# bailed out silently every time.
#
# It matches town names, not ZIP codes: exact, then prefix, then contains. There is no
# ZIP data yet, so a five-digit entry gets the phone number rather than a guess about
# whether we serve someone. TODO: add ZIPs to builder/locations.py and match them here.
ZIP_JS = """
<script>
(function(){
  var root = document.currentScript.closest('.xhac-svc');
  if (!root) return;
  var box = root.querySelector('#xlc-zip'),
      go  = root.querySelector('#xlc-zipgo'),
      msg = root.querySelector('#xlc-zipmsg');
  if (!box || !go || !msg) return;

  var towns = {};
  root.querySelectorAll('.xlc-links a').forEach(function(a){
    towns[a.textContent.trim().toLowerCase()] = a.getAttribute('href');
  });

  function title(t){ return t.replace(/\\b\\w/g, function(c){ return c.toUpperCase(); }); }

  function check(){
    var v = (box.value || '').trim().toLowerCase().replace(/[.,]/g, '');
    if (!v){ msg.className = 'xlc-zipmsg no'; msg.textContent = 'Enter a town name to check.'; return; }

    var href = towns[v] || null, hits = [], k;
    if (!href){
      for (k in towns){ if (k.indexOf(v) === 0) hits.push(k); }
      if (!hits.length){ for (k in towns){ if (k.indexOf(v) > -1) hits.push(k); } }
      if (hits.length === 1) href = towns[hits[0]];
    }

    if (href){
      msg.className = 'xlc-zipmsg ok';
      msg.textContent = 'Yes - opening that page.';
      // the page is an embed, so navigate the top window, not the iframe
      try { window.top.location.href = href; } catch (e) { window.location.href = href; }
      return;
    }
    if (hits.length > 1){
      msg.className = 'xlc-zipmsg no';
      msg.textContent = 'Did you mean: ' + hits.slice(0, 4).map(title).join(', ') + '?';
      return;
    }
    msg.className = 'xlc-zipmsg no';
    msg.textContent = /^[0-9]{5}$/.test(v)
      ? 'We cannot match a ZIP yet - call (844) 584-7399 and we will tell you straight away.'
      : 'Not on the list - call (844) 584-7399. If we can reach you, we will.';
  }

  go.addEventListener('click', function(e){ e.preventDefault(); check(); });
  box.addEventListener('keydown', function(e){ if (e.key === 'Enter'){ e.preventDefault(); check(); } });
})();
</script>
"""

# ---------------------------------------------------------------- registry
def pages(root):
    out = [(os.path.join(root, "pages", "locations", "overview.html"),
            lambda d, rc: hub(), {}, "xsp-locations")]
    for group, items in L.GROUPS:
        for slug, city in items:
            d = os.path.join(root, "pages", "locations", slug)
            out.append((os.path.join(d, "overview.html"),
                        lambda _d, _rc, c=city, s=slug, g=group: city_overview(c, s, g),
                        {}, f"xsp-loc-{slug}"))
            for service in SERVICE_ORDER:
                out.append((os.path.join(d, f"{service}.html"),
                            lambda _d, _rc, c=city, s=slug, g=group, sv=service: city_service(c, s, g, sv),
                            {}, f"xsp-loc-{slug}-{service}"))
    return out
