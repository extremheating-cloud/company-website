import os
from layout import components as T
from data import business as D
from pages.company_shared import PHOTOS, UPDATED, UPDATED_ISO, shell, section, prose_section, slot_img

# ================================================================
# /contact — mockup 4b (rail tier), copy verbatim
# ================================================================
# "same-day in most cases" was a response-time promise, and it is not one of the
# approved proof tokens. The approved wording is "90% same-day service"; anything
# looser reads as a guarantee the dispatcher cannot keep.
T.PROMOS["contactCall"] = dict(cls="lav", t="Need help right now?",
    # "Skip the form" pointed at a form that is not on the page — /contact books
    # through the scheduling wizard, and there is no <form> element anywhere on it.
    # The real alternative being offered is not typing it all out.
    d="Rather not type it all out? A real person answers, day or night.",
    lm=f"Call {T.PHONE_DISPLAY} →", href=T.PHONE_TEL)
T.PROMOS["contactXplan"] = dict(cls="mint", t="X-Plan members skip the line",
    d="Priority scheduling, two tune-ups a year, and 15% off repairs.",
    lm="Explore X-Plan →", href="/maintenance")

def contact_card():
    # The 4.9 average is a Birdeye aggregate across the platforms customers post on,
    # not a Google-only figure. The trust row used to call it a Google rating, which a
    # competitor or a rater can check in thirty seconds. D.REVIEW_SOURCE is the
    # approved wording, and the count is the half that was missing: a rating with no
    # denominator is the shape of a claim rather than a claim.
    return f'''<div class="xsp-book">
  <div class="eyebrow">CONTACT US</div>
  <div class="xco-phone"><a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a></div>
  <div class="s">Office staffed {D.HOURS_STAFFED_SHORT} · emergencies 24/7.</div>
  <!-- THE line the A2P reviewer has to be able to read. One plainly readable
       statement that a specific number accepts texts, on the page a reviewer opens
       first. Do not turn this into a button; the href of a button is not something a
       human reviewer can be relied on to inspect, and without this sentence opt-in
       path 1 in the registration ("published on our website") is simply false. -->
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

# Per-office presentation only. The addresses themselves live in business.OFFICES
# and are read from there — two copies of an address in one repo is the NAP problem
# starting at home.
#
# Troy and Waynesville have no exterior photograph yet. Those two cards ship
# text-only rather than with an empty photo slot: a grey placeholder box on a
# location card signals the premises may not exist, which is worse than a smaller
# card. [NEEDS: exterior photographs of the Troy and Waynesville offices.]
OFFICE_PHOTOS = {
    # 65% pushes the crop down onto the sign so the 712 street number stays in
    # frame — it is the thing that makes this read as a location card.
    "beavercreek": {"src": PHOTOS["beavercreek"], "pos": "50% 65%",
                    "alt": f"An {D.COMPANY} service van at the Beavercreek office sign on North Fairfield Road"},
    "mason": {"src": PHOTOS["mason"],
              "alt": f"The {D.COMPANY} office building on Tylersville Road in Mason, Ohio"},
}

def location_card(o):
    """One office card. Headed by `locality`, which is the city in the postal address
    directly beneath it. The cards used to be headed by metro — a card headed "Dayton"
    over a Beavercreek address is a NAP inconsistency, and it is exactly the pattern
    citation-matching services flag."""
    photo = OFFICE_PHOTOS.get(o["slug"])
    img = slot_img("xco-loc-img", photo, "") if photo else ""
    # Most offices describe themselves by metro. Waynesville is not a metro shop — the
    # client's answer to "how is it presented" was that it is the plumbing hub — so it
    # carries an explicit descriptor instead. An office with neither still renders
    # nothing rather than a guessed region.
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
    """The parseable copy of the office list. The cards carry the photos and the
    directions links; this carries the same four addresses in a shape an engine can
    lift whole. County comes from business, not from a coverage guess — dispatch
    boundaries per office are still unconfirmed and are not published here."""
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
    # The answer-first block. No phone number in it, per geo-contract §2.2 — which is
    # a genuinely odd rule on a contact page. The number sits immediately below it in
    # the booking card, in the first H2 answer, and in the FAQ.
    "answer": ("We book heating, cooling and plumbing service across the Dayton and Cincinnati "
               "metros, out of four Ohio offices that all route to one line. The office is open "
               "weekdays 8 to 5, and emergencies are answered 24/7."),
    # The old H1, demoted to the deck line.
    "intro": "Get in touch with the Extreme Team.",
    # "Same-Day in Most Cases" was a response-time promise. 90% same-day service is the
    # approved proof token and it is a number, which is the point.
    "heroChips": [f"{D.SAME_DAY} Same-Day Service", "24/7 Emergency Line", "Dayton &amp; Cincinnati"],
    # Addresses are NOT stored here. All four offices come from business.OFFICES, which
    # is client-confirmed 2026-08-02 and is also what the footer, the location pages and
    # the JSON-LD read. One written form, byte for byte, everywhere — a NAP audit compares
    # the visible block against the schema on the same page and a mismatch is
    # machine-detectable. See OFFICE_PHOTOS above for the per-card presentation.
    #
    # Hours confirmed by the client 2026-08-01, and now read from business. 8-5 weekdays
    # is when the OFFICE is staffed; emergency service really does run around the clock.
    # Keep these two rows distinct if this table is ever edited — collapsing them is what
    # produced the contradiction with the 24/7 claims on the other 34 pages.
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
        # PLACEHOLDER at the client's direction until dispatcher photos are shot —
        # this is a van shot standing in for an office/dispatch image. Swap it for
        # shot B3 (dispatcher at the desk) when the session delivers. The alt text
        # describes what is actually in the frame, not what the slot wants.
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
