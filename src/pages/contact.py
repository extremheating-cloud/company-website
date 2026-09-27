import os
from layout import components as T
from data import business as D
from pages.company_shared import PHOTOS, UPDATED, UPDATED_ISO, shell, section, prose_section, slot_img

T.PROMOS["contactCall"] = dict(cls="lav", t="Need help right now?",
    d="Rather not type it all out? A real person answers, day or night.",
    lm=f"Call {T.PHONE_DISPLAY} →", href=T.PHONE_TEL)
T.PROMOS["contactXplan"] = dict(cls="mint", t="X-Plan members skip the line",
    d="Priority scheduling, two tune-ups a year, and 15% off repairs.",
    lm="Explore X-Plan →", href="/maintenance")

def contact_card():
    # Birdeye aggregate across platforms, not a Google rating: never label it "on Google".
    # .xco-sms is A2P opt-in path 1, quoted verbatim in the carrier filing: readable text, not a button.
    return f'''<div class="xsp-book">
  <div class="eyebrow">CONTACT US</div>
  <div class="xco-phone"><a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a></div>
  <div class="s">Office staffed {D.HOURS_STAFFED_SHORT} · emergencies 24/7.</div>
  <div class="xco-sms">Call <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>
    &middot; Text <a href="{D.SMS_HREF}">{D.SMS_DISPLAY}</a></div>
  <div class="btns">
    {T.schedule_btn("Schedule Service")}
    {T.call_btn(f"Call {T.PHONE_DISPLAY}")}
    {T.text_btn()}
  </div>
  <div class="trust"><span><span class="st">★</span> {D.GOOGLE_RATING} from {D.REVIEW_COUNT} reviews</span><span class="bar">|</span><span>{D.YEARS_LOCAL} years local</span></div>
</div>'''

def contact_hero(d):
    return f'''<div class="xsp-hero">
  {T.hero_mark()}
  <div class="xsp-hero-grid">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas xsp-mb">
        {T.schedule_btn("Schedule Service", "xsp-cta")}
        <a class="xsp-cta-outline" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
      </div>
      {T.chips(d["heroChips"])}
    </div>
    <div class="xsp-bookcol">{contact_card()}</div>
  </div>
</div>'''

def book_cards(d):
    cards = f'''<div class="xco-2col">
  <div class="xco-bcard">
    <span class="xsp-glyph"><i></i><i></i></span>
    <div class="t">Schedule online</div>
    <div class="d">Hit Schedule Service and pick a time that works. It takes about a minute, and it stays open when the office is closed.</div>
    <a class="xsp-cta js-schedule" href="#" role="button">Schedule Online</a>
  </div>
  <div class="xco-bcard">
    <span class="xsp-glyph"><i></i><i></i></span>
    <div class="t">Call the office</div>
    <div class="d">Talk to a real person. The emergency line is answered 24/7, including nights, weekends and holidays.</div>
    <a class="plink" href="{T.PHONE_TEL}">{T.PHONE_DISPLAY} →</a>
  </div>
</div>'''
    return section("BOOK A VISIT", "How do I book a service visit?", cards, sid="book",
                   lead=["Two ways: call "
                         f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>, or use the online '
                         "scheduler. Both land in the same dispatch, and a real person picks up "
                         "the phone after hours and on weekends. "
                         '<a href="/maintenance">X-Plan members get priority scheduling</a>.'])

# Addresses come only from business.OFFICES; a second copy here is a NAP mismatch waiting to happen.
OFFICE_PHOTOS = {
    # 65% keeps the 712 street number on the sign in frame.
    "beavercreek": {"src": PHOTOS["beavercreek"], "pos": "50% 65%",
                    "alt": f"An {D.COMPANY} service van at the Beavercreek office sign on North Fairfield Road"},
    "mason": {"src": PHOTOS["mason"],
              "alt": f"The {D.COMPANY} office building on Tylersville Road in Mason, Ohio"},
}

def location_card(o):
    # Headed by locality, not metro, so it matches the postal address beneath it (NAP).
    photo = OFFICE_PHOTOS.get(o["slug"])
    img = slot_img("xco-loc-img", photo, "") if photo else ""
    label = o.get("descriptor") or (f'Our {o["metro"]}-area shop' if o.get("metro") else "")
    metro = f'<div class="meta">{label}</div>' if label else ""
    page = (f'<a href="{o["page"]}" class="alt">{o["locality"]} service area →</a>'
            if o.get("page") else "")
    return f'''<div class="xco-loc">
  {img}
  <div class="xco-loc-body">
    <div class="t">{o["locality"]}</div>
    {metro}
    <div class="addr">{o["street"]}<br>{o["citystate"]}</div>
    <div class="addr hrs">{o["hours"]}</div>
    {f'<a class="tel" href="tel:{o["phone_e164"]}">{o["phone"]}</a>' if o.get("phone") else ""}
    <a href="{o["directions"]}">Get directions →</a>
    {page}
  </div>
</div>'''

def location_cards(d):
    cards = f'<div class="xco-2col">{"".join(location_card(o) for o in D.OFFICES)}</div>'
    lead = [
        'We work out of four Ohio shops. Beavercreek covers the Dayton side, Mason covers '
        'Cincinnati, and Troy and Waynesville fill in Miami and Warren counties between them.',
        f'One number reaches all four: <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>, and it is '
        'the line answered at any hour. Each shop also takes calls direct on its own local '
        'number, listed on its card below.',
    ]
    return section("VISIT US", "Where are your offices?", cards,
                   lead=lead, sid="offices")

def offices_table():
    return T.table_section({
        "eyebrow": "OFFICES AT A GLANCE",
        "h2": "Which office is closest to me?",
        "id": "offices-table",
        "takeaway": f"All four Ohio offices route to the same number, {D.PHONE_DISPLAY}.",
        "caption": "Our four Ohio office addresses",
        "columns": ["Office", "Street address", "County", "Office hours"],
        "rows": [[o["locality"], o["oneline"], f'{o["county"]} County', o["hours"]]
                 for o in D.OFFICES],
    })

def hours_table(d):
    rows = []
    for row in d["hours"]:
        em = ' em' if row.get("em") else ""
        rows.append(f'<div class="row{em}"><span>{row["label"]}</span><span>{row["value"]}</span></div>')
    return section("HOURS", "When are you open?",
                   f'<div class="xco-hours">{"".join(rows)}</div>',
                   sid="hours",
                   lead=[f"The office is staffed {D.HOURS_STAFFED}. The emergency line runs "
                         "separately, around the clock, every day of the year including "
                         "holidays, so the office being shut does not mean nobody picks up."])

CONTACT = {
    "breadcrumb": [("Home", "/"), ("Contact", "")],
    "h1": "Contact {X} Heating, Air, Plumbing",
    "h1Highlight": "Extreme",
    # No phone number in the answer block (geo-contract §2.2).
    "answer": ("We book heating, cooling and plumbing service across the Dayton and Cincinnati "
               "metros, out of four Ohio offices that all route to one line. The office is open "
               "weekdays 8 to 5, and emergencies are answered 24/7."),
    "intro": "Get in touch with the Extreme Team.",
    "heroChips": [f"{D.SAME_DAY} Same-Day Service", "24/7 Emergency Line", "Dayton &amp; Cincinnati"],
    # Keep staffed and emergency hours as separate rows; merging them contradicts the 24/7 claims.
    "hours": [
        {"label": "Staffed office", "value": D.HOURS_STAFFED},
        {"label": "Emergency service", "value": D.HOURS_EMERGENCY, "em": True},
    ],
    "faqEyebrow": "CONTACT QUESTIONS",
    "faqH2": "What else do people ask before calling?",
    "faq": [
        {"q": "What's your phone number?",
         "a": f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>. One number for heating, cooling '
              "and plumbing, reaching all four Ohio offices, and the only line staffed around "
              "the clock. Each office also has its own local number if you would rather dial "
              "one in your own area code."},
        {"q": "Where is the Beavercreek office?",
         "a": f'{D.OFFICE_BY_SLUG["beavercreek"]["oneline"]}, in Greene County.'},
        {"q": "Where is the Mason office?",
         "a": f'{D.OFFICE_BY_SLUG["mason"]["oneline"]}, in Warren County.'},
        {"q": "Can I book online instead of calling?",
         "a": "Yes. The scheduler holds the same appointment slots the office books by phone, "
              "and it stays open when we're closed."},
        {"q": "Do you serve my town?",
         "a": 'Most likely. We cover nine Ohio counties between the two metros, and the '
              '<a href="/locations">service area page lists every community</a>.'},
        {"q": "Is there an email address?",
         "a": f'Yes. <a href="mailto:{D.EMAIL}">{D.EMAIL}</a> handles anything that can wait. '
              "If it can't wait, call instead. That line is answered 24/7."},
    ],
    "rail": {
        # TODO: placeholder van shot; swap for B3 (dispatcher at the desk) once it's shot.
        "photo": PHOTOS["vans"],
        "photoAlt": f"{D.COMPANY} service vans heading out on calls",
        "promos": ["contactCall", "contactXplan"],
    },
}

def contact_wait():
    return prose_section(
        "BEFORE WE ARRIVE", "What should I do while I wait for a technician?",
        ["Shut the system off at the thermostat if it's short-cycling, tripping a breaker, or "
         "smells like something is burning. For a water leak, close the valve at the fixture, "
         "or the main shutoff if that valve won't hold.",
         "If you smell gas, get everyone out of the house first and call the gas utility from "
         "outside before you call anyone else."],
        sid="while-you-wait")

def contact_emergency():
    return prose_section(
        "AFTER HOURS", "Is emergency service available at night and on weekends?",
        ["Yes, every day of the year. No heat, no cooling, no hot water, a burst pipe or the "
         f"smell of gas all get a truck moving, and {D.SAME_DAY} of calls are handled the same "
         "day.",
         'Planning a replacement instead of reacting to a breakdown? '
         '<a href="/financing-options">Financing</a> runs through three lenders, and '
         '<a href="/locations/dayton">Dayton</a> and '
         '<a href="/locations/cincinnati">Cincinnati</a> each have their own service page.'],
        sid="emergency")

def contact_page(d, root_class):
    left = [
        T.mobile_photo(d["rail"]),
        book_cards(d),
        hours_table(d),
        location_cards(d),
        offices_table(),
        contact_wait(),
        contact_emergency(),
        T.mobile_inline_rail(d),
        T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"]),
        T.updated_line(UPDATED, UPDATED_ISO),
    ]
    body = f'''{contact_hero(d)}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {T.rail(d["rail"])}
</div>'''
    return shell(root_class, body)

def pages(root):
    return [(os.path.join(root, "pages", "company", "contact.html"), contact_page, CONTACT, "xsp-contact")]
