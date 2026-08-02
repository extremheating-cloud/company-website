"""Location pages — design_handoff_location_pages (screens 5h, 5a-5g).

One template, 38 cities, 267 pages. Copy is verbatim from the mockup; the only
things that vary per city are the name, the metro, the neighbour-town list and the
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
    return (f'<div class="xco-stats"><img class="mark" src="{T.X_MARK}" alt="" '
            f'style="position:absolute;right:-70px;bottom:-60px;width:300px;opacity:.06;'
            f'transform:rotate(-8deg);filter:brightness(0) invert(1)">'
            f'<div class="grid">{inner}</div></div>')

def _band(title, sub, cta="call"):
    """Ink CTA band. `cta` is "call" or "schedule" per the handoff's per-page note."""
    btn = (T.schedule_btn("Schedule Service", "xsp-cta js-schedule") if cta == "schedule"
           else f'<a class="xsp-cta" href="{T.PHONE_TEL}">Call {PHONE}</a>')
    return f'''<div class="xsp-band"><div class="xsp-band-in">
  <div><div class="t">{title}</div><div class="d">{sub}</div></div>
  <div class="btns">{btn}</div>
</div></div>'''

def _hero(city, crumbs, h1, hi, intro, chips, card, pill="", card_class="", ctas=True):
    """ctas=False is for the hub, whose card is a search tool rather than a booking
    CTA and stays on screen at every width instead of handing off to a button pair."""
    pill_html = f'<div class="xlc-pill">{pill}</div>' if pill else ""
    # The booking card is display:none under 810px, so without this pair a phone gets
    # a hero with no way to book — which is what all 267 location pages used to do.
    cta_html = f'''<div class="xsp-hero-ctas xsp-mb">
        {T.schedule_btn("Schedule Service", "xsp-cta js-schedule")}
        <a class="xsp-cta-outline" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
      </div>''' if ctas else ""
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid">
    <div>
      {T.crumbs(crumbs)}
      {pill_html}
      {T.h1(h1, hi)}
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

def _cards(eyebrow, h2, items):
    """Service / capability card grid. items: (title, desc, href|None, pill|None)."""
    out = []
    for t, d, href, pill in items:
        tag = f'<a class="xlc-card" href="{href}">' if href else '<div class="xlc-card">'
        end = "</a>" if href else "</div>"
        lm = f'<span class="lm">{pill[1]}</span>' if pill and len(pill) > 1 and pill[1] else ""
        new = '<span class="xlc-new">NEW</span>' if pill and pill[0] == "NEW" else ""
        out.append(f'{tag}{new}<div class="t">{t}</div><div class="d">{d}</div>{lm}{end}')
    return section(eyebrow, h2, f'<div class="xlc-grid3">{"".join(out)}</div>')

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
  chips=["Same-Day in Most Cases", "Upfront Pricing", "All Makes &amp; Models"],
  bookEyebrow="{CITYU} COOLING",
  gridEyebrow="WHAT WE HANDLE", gridH2="Every way a {CITY} home stays cool.",
  cards=[("AC repair","From weak airflow to total shutdowns — diagnosed and quoted upfront."),
         ("AC installation &amp; replacement","High-efficiency systems sized to your square footage and ductwork."),
         ("Heat pumps","One system for summer and winter — with rebates often available."),
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
  chips=["Licensed Plumbers", "Upfront Pricing", "Same-Day in Most Cases"],
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
  photo="equipment/ge-water-heater-install.jpg", photoAlt="A water heater installed by the Extreme Team"),

"maintenance": dict(
  nav="Maintenance", h1="Tune-ups that keep {X}", hi="breakdowns away",
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
  nav="Duct Cleaning", h1="Cleaner ducts, {X}", hi="cleaner air",
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
  cards=[("Whole-home media filters","Hospital-grade filtration that replaces the flimsy 1-inch filter."),
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
def neighbours(slug, group, n=10):
    """The other towns in the same metro. This is the one genuinely per-city block on
    the page, and the handoff names it as what keeps these from being find-replace."""
    pool = {"Dayton": L.DAYTON, "Cincinnati": L.CINCINNATI, "Counties": L.COUNTIES}[group]
    others = [(s, nm) for s, nm in pool if s != slug]
    return others[:n]

def metro_adj(group):
    return {"Dayton": "Miami Valley", "Cincinnati": "Cincinnati-area",
            "Counties": "southwest Ohio"}[group]

def fill(text, city, group):
    return (text.replace("{CITYU}", city.upper()).replace("{CITY}", city)
                .replace("{METRO_ADJ}", metro_adj(group)))

NO_TOWN_NOTE = ('<div class="xlc-note">Don&#39;t see your town? If you&#39;re close to one '
                'that&#39;s listed, call — if we can reach you, we will.</div>')

# ---------------------------------------------------------------- renderers
def city_overview(city, slug, group):
    f = lambda t: fill(t, city, group)
    cards = []
    for s, label, desc in OVERVIEW_CARDS:
        pill = ("NEW", f"{city} {label.lower()} →") if s == "plumbing" else (None, f"{city} {label.lower()} →")
        cards.append((label, f(desc), f"/locations/{slug}/{s}", pill))
    towns = "".join(
        f'<div class="xlc-town"><span class="c">✓</span>'
        f'<a href="/locations/{ns}">{nn}</a></div>' for ns, nn in neighbours(slug, group))
    revs = "".join(
        f'<div class="xlc-rev"><div class="stars">★★★★★</div><div class="q">“{q}”</div>'
        f'<div class="who">{who}{f" <span>· {rc}</span>" if rc else ""}</div></div>'
        for q, who, rc in city_reviews(slug))
    hero_img = T.cdn_asset(L.hero(slug))
    body = f'''{_hero(city,
        [("Home", "/"), ("Locations", "/locations"), (city, "")],
        "Heating, air &amp; plumbing — {X}", f"right here in {city}",
        f"Local techs who know {metro_adj(group)} homes. One number, same-day in most cases.",
        [f"{city}-Based Techs", "Same-Day in Most Cases", "24/7 Emergency Line"],
        _book(f"SERVING {city.upper()}", "Same-day in most cases.",
              f"Techs dispatched across {METRO_BLURB[group]} — book online in about a "
              f"minute, or call and talk to a real person.", trust2=f"{city}-based techs"))}
<div class="xco-body">
  {_cards(f"SERVICES IN {city.upper()}", "Everything your house throws at you.", cards)}
  {_stat_panel([("20+", f"years serving {METRO_BLURB[group]}"), ("4.9", "average Google rating"),
                ("90%", "of calls handled same-day"), ("24/7", "emergency service line")])}
  {section("SERVICE AREA", f"If you're near {city}, you're covered.",
    f'<div class="xlc-towns">{towns}</div>'
    f'<div class="xlc-note">Outside the list? Call — if we can reach you, we will.</div>'
    f'<div style="margin-top:20px">{T.photo_slot("", hero_img, f"{city}, Ohio")}</div>')}
  {section("WHAT NEIGHBORS SAY", "Neighbors put it better than we can.",
    f'<div class="xlc-revs">{revs}</div>')}
</div>
{_band("No heat, no AC, or water where it shouldn't be?",
       f"The {city} line is answered 24/7 — nights, weekends, holidays.")}'''
    return shell(f"xsp-loc-{slug}", body, extra_css=LOC_CSS)

def city_service(city, slug, group, service):
    c = SERVICE_COPY[service]
    f = lambda t: fill(t, city, group)
    left = []
    if c.get("sec1") == "checks" or (c.get("checks") and "cards" not in c):
        left.append(_checklist(f(c["chkEyebrow"]), f(c["chkH2"]), c["checks"], c.get("chkNote")))
    if "cards" in c:
        left.append(_cards(f(c["gridEyebrow"]), f(c["gridH2"]),
                           [(t, f(d), None, None) for t, d in c["cards"]]))
    sec2 = c.get("sec2")
    if sec2 == "decision":
        inner = "".join(f'<div class="xco-ccard"><span class="c">✓</span>'
                        f'<div class="t">{t}</div><div class="d">{d}</div></div>' for t, d in c["dec"])
        left.append(section(f(c["decEyebrow"]), f(c["decH2"]),
                            f'<div class="xco-2col">{inner}</div>'
                            f'<div class="xlc-note">{c["decNote"]}</div>'))
    elif sec2 == "checks" and "cards" in c:
        left.append(_checklist(f(c["chkEyebrow"]), f(c["chkH2"]), c["checks"], c.get("chkNote")))
    elif sec2 == "purple":
        items = "".join(f'<li><span class="c">✓</span><span><b>{t}</b> {d}</span></li>'
                        for t, d in c["purple"])
        left.append(f'<div class="xlc-xp"><div class="eyebrow">{f(c["purpleEyebrow"])}</div>'
                    f'<h3>{f(c["purpleH2"])}</h3><ul>{items}</ul></div>')
    elif sec2 == "steps":
        left.append(T.process({"h2": f(c["stepsH2"]),
                               "steps": [{"title": t, "desc": d} for t, d in c["steps"]]},
                              eyebrow=f(c["stepsEyebrow"])))
    elif sec2 == "xplan":
        # The shared panel, not a copy of it. X-Plan pricing and member rates live in
        # T.XPLAN, so a change there updates the hub, /maintenance and all 38 location
        # maintenance pages together.
        left.append(T.xplan_panel(detail=True))

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
        f(c["h1"]), f(c["hi"]), f(c["intro"]), c["chips"],
        _book(f(c["bookEyebrow"]), c.get("bookTitle", "Same-day in most cases."),
              c.get("bookSub", "Book online in about a minute, or call and talk to a real person."),
              label=c.get("bookLabel", "Schedule Service"), trust2=f"{city}-based techs"),
        pill=f(c["pill"]) if c.get("pill") else "")}
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
  <div class="trust"><span><span class="st">★</span> 4.9 on Google</span><span class="bar">|</span><span>24/7 emergency line</span></div>
</div>'''
    body = f'''{_hero("", [("Home", "/"), ("Locations", "")],
        "One Extreme Team, {X}", "all over southwest Ohio",
        "Heating, cooling, and plumbing across the Dayton and Cincinnati metros. Find your "
        "community below — one phone number covers them all.",
        ["2 Metro Areas", f"{len(L.ALL)}+ Communities", "Same-Day in Most Cases"], zip_card,
        card_class="zip", ctas=False)}
<div class="xco-body">
  {section("SERVICE AREAS", "Two metros, one team.", "".join(metros))}
  {section("ALL COMMUNITIES", "Every place we serve.",
    f'<div class="xlc-dir">{"".join(cols)}</div>' + NO_TOWN_NOTE)}
  {_stat_panel([(f"{len(L.ALL)}+", "communities served"), ("4.9", "average Google rating"),
                ("90%", "of calls handled same-day"), ("24/7", "emergency service line")])}
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
