import os
from layout import components as T
from data import business as D
from pages.company_shared import UPDATED, UPDATED_ISO, shell, section, prose_section

# ================================================================
# /specials — mockup 4d (full-width tier), copy verbatim
# ================================================================
T.PROMOS["spFinance"] = dict(cls="lav", t="Big job? Finance it.",
    d="Specials stack with monthly payment plans through our lenders.",
    lm="Financing Options →", href="/financing-options")
# All six offers are PLACEHOLDERS per the handoff — swap in live promotions
# by editing OFFERS below and re-running build.py. Keys: pill, value,
# (optional) valueSuffix, title, desc, foot, cta ("schedule" | href).
OFFERS = [
    {"pill": "HEATING &amp; AIR", "value": "$79", "title": "AC or Furnace Tune-Up",
     "desc": "Full seasonal inspection and tune-up. Regularly priced higher — X-Plan members get two a year included.",
     "foot": "Limited time", "cta": "schedule"},
    {"pill": "ANY SERVICE", "value": "$50 off", "title": "Any Repair Over $250",
     "desc": "HVAC or plumbing — take $50 off any qualifying repair when you mention this offer at booking.",
     "foot": "Limited time", "cta": "schedule"},
    # Replaced the placeholder "Up to $500 off a New Comfort System" card: it offered double
    # the Extreme Rewards give ($250) on the same job type, so a referred customer would have
    # seen the public special beat the referral they were just promised. Built from approved
    # Extreme Rewards numbers only — no invented promotional amount. If marketing wants a real
    # new-system special back here, it needs a confirmed figure and a deliberate position
    # against the $250 referral.
    {"pill": "REFERRALS", "value": f'{D.REWARDS["newSystem"]} off', "title": "When a Friend Refers You",
     "desc": f'New customers save {D.REWARDS["newSystem"]} on a new heating, cooling or plumbing system, or {D.REWARDS["everythingElse"]} on any other job of {D.REWARDS["everythingElseMin"]} or more. Name whoever sent you when you book.',
     "foot": "Always available", "cta": "/referral", "ctaLabel": "See Extreme Rewards"},
    {"pill": "PLUMBING", "value": "$99", "title": "Drain Clearing Special",
     "desc": "Single accessible drain cleared, with a camera check if the clog keeps coming back. Does not cover the home\u2019s main drain or sewer line.",
     "foot": "Limited time", "cta": "schedule"},
    {"pill": "NEW SYSTEMS", "value": "Free", "title": "Second Opinion on Replacement",
     "desc": "Told you need a whole new system? Get a no-pressure second look before you commit.",
     "foot": "Limited time", "cta": "schedule"},
    # "discounted service calls" implied a published rate this card cannot state.
    # "a reduced member service fee" is the same fact without the implication.
    {"pill": "MEMBERSHIP", "value": D.XPLAN["annual"], "valueSuffix": "/yr", "title": "Join X-Plan Maintenance",
     "desc": "Two tune-ups a year, 15% off repairs, priority scheduling, and a reduced member service fee.",
     "foot": "Always available", "cta": "/maintenance", "ctaLabel": "Join X-Plan"},
]

# Email signup panel (mockup 4d right column) — hidden until wired to an ESP.
# TODO: wire to the email service provider, then flip to True and rebuild.
SHOW_EMAIL_SIGNUP = False

def coupon(o):
    suffix = f'<span class="per">{o["valueSuffix"]}</span>' if o.get("valueSuffix") else ""
    if o["cta"] == "schedule":
        btn = f'<a class="xco-claim js-schedule" href="#" role="button">{o.get("ctaLabel", "Claim Offer")}</a>'
    else:
        btn = f'<a class="xco-claim" href="{o["cta"]}">{o.get("ctaLabel", "Claim Offer")}</a>'
    return f'''<div class="xco-coupon">
  <div class="pill">{o["pill"]}</div>
  <div class="val">{o["value"]}{suffix}</div>
  <div class="t">{o["title"]}</div>
  <div class="d">{o["desc"]}</div>
  <div class="foot"><span class="lbl">{o["foot"]}</span>{btn}</div>
</div>'''

def email_panel():
    return f'''<div class="xco-mail">
  <div class="t">Never miss a deal</div>
  <div class="d">Get seasonal offers in your inbox — no spam, just savings.</div>
  <form action="#" onsubmit="return false">
    <input type="email" placeholder="Email address" aria-label="Email address">
    <button type="submit">Sign Up</button>
  </form>
</div>'''

SPECIALS = {
    "breadcrumb": [("Home", "/"), ("Specials", "")],
    "h1": "HVAC and plumbing {X} in Dayton and Cincinnati",
    "h1Highlight": "specials",
    # No offer amount in the answer block on purpose: it is the most-cited passage on
    # the page and it should outlive the coupons. Amounts live in OFFERS and nowhere
    # else, so swapping a promotion is a data edit rather than a copy rewrite.
    "answer": ("These are the offers running right now on heating, cooling and plumbing work. "
               "One per household per visit, and you have to name it when you book. The "
               "discount then shows up in your quote, before anyone starts working."),
    # The old H1, demoted to the deck line.
    "intro": "Seasonal specials, extreme savings.",
    "heroChips": ["Updated Seasonally", "Mention at Booking", "Combine with Financing"],
    "redeem": {
        "h2": "How do I claim a special?",
        "steps": [
            {"title": "Pick your offer",
             "desc": "One offer per visit — choose the one that saves you the most."},
            {"title": "Mention it when you book",
             "desc": "Tell us on the phone or note it in the online scheduler — we attach it to your appointment."},
            {"title": "Savings applied on your invoice",
             "desc": "The discount shows up in your upfront quote — before any work begins."},
        ],
    },
    "fineNote": "Offers cannot be combined with other discounts unless noted. One offer per household per visit. Must be mentioned at the time of booking. Expiration dates and full terms are set per promotion.",
    # Column 2 names each offer by type rather than by price, so the table survives a
    # promotion swap. The only amounts are the two Extreme Rewards numbers, which are
    # the approved customer-facing pair.
    "table": {
        "eyebrow": "WHICH OFFER FITS",
        "h2": "Which offer saves the most on my job?",
        "id": "which-offer",
        "takeaway": "Only one offer applies per household per visit, so pick the one that "
                    "matches the job you're booking.",
        "caption": "Which offer fits which job",
        "columns": ["What you are booking", "Offer that usually fits", "How to claim it"],
        "rows": [
            ["A seasonal tune-up on one system", "The AC or furnace tune-up special",
             "Name it when you book"],
            ["A repair on an existing system", "The repair discount", "Name it when you book"],
            ["One accessible drain that will not clear", "The drain clearing special",
             "Name it when you book"],
            ["A replacement quote from another company", "The free second opinion",
             "Name it when you book"],
            ["Tune-ups you want every year, not once",
             "X-Plan membership, which includes two visits a year", "Join X-Plan"],
            ["A first job after a friend recommended us",
             f'Extreme Rewards: {D.REWARDS["newSystem"]} on a new system, '
             f'{D.REWARDS["everythingElse"]} on any other job of {D.REWARDS["everythingElseMin"]} or more',
             "Name your friend when you book"],
        ],
    },
    "faqEyebrow": "OFFER QUESTIONS",
    "faqH2": "What do people ask about the offers?",
    "faq": [
        {"q": "Do I need to print a coupon?",
         "a": "No. Name the offer on the phone, or in the note field when you book online, and "
              "we attach it to your appointment."},
        {"q": "Can I use more than one offer on the same visit?",
         "a": "One per household per visit. Offers don't combine with other discounts unless "
              "the offer says so."},
        {"q": "When does the discount get applied?",
         "a": "It's in your upfront quote, before any work begins, and it shows again on the "
              "invoice."},
        {"q": "Can I use a special with financing?",
         "a": 'Yes. The offer comes off the price, and '
              '<a href="/financing-options">monthly payments</a> cover the rest.'},
        {"q": "What if I forget to mention the offer?",
         "a": "Offers have to be named when the job is booked. We can't add one after the "
              "visit, so say it on the call."},
        {"q": "Is X-Plan a special or a membership?",
         "a": f'A membership, so it doesn\'t expire like the rest of these. '
              f'{D.XPLAN["annual"]} a year, or {D.XPLAN["monthly"]} a month per system. '
              f'<a href="/maintenance">Join X-Plan</a>.'},
    ],
}

def specials_hero(d):
    return f'''<div class="xsp-hero">
  {T.hero_mark()}
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      {T.chips(d["heroChips"])}
    </div>
  </div>
</div>'''

def specials_page(d, root_class):
    coupons = f'<div class="xco-coupons">{"".join(coupon(o) for o in OFFERS)}</div>'
    right = (email_panel() if SHOW_EMAIL_SIGNUP else "") + T.promo("spFinance")
    redeem = f'''{T.process(d["redeem"], eyebrow="HOW TO REDEEM")}
<div class="xco-finenote">{d["fineNote"]}</div>'''
    offers = section(
        "CURRENT OFFERS", "What specials are running right now?", coupons,
        sid="offers",
        lead=["Right now: seasonal tune-ups, repairs, "
              '<a href="/plumbing/clogged-drain">drain cleaning</a>, a free second opinion on a '
              "replacement quote, and X-Plan membership. These change with the season, so this "
              "page is always the current set."])
    combine = prose_section(
        "STACKING", "Can specials be combined with financing?",
        ['Yes. Take the offer off the price, then put the rest on a '
         '<a href="/financing-options">monthly payment</a>. Specials don\'t stack with each '
         'other, though: one offer per household per visit.'],
        sid="combine")
    members = prose_section(
        "MEMBERS", "Do X-Plan members get their own offers?",
        ["Yes. Members take 15% off every repair, get two seasonal visits included, get priority "
         "scheduling, and carry a 5-year warranty on qualified repairs. That's "
         f'{D.XPLAN["annual"]} a year, or {D.XPLAN["monthly"]} a month per system. '
         f'<a href="/maintenance">Join X-Plan</a>.',
         'Just booking a repair? <a href="/ac-repair">AC repair</a> and '
         '<a href="/furnace-installation">furnace installation</a> both take the offers above.'],
        sid="members")
    rotation = prose_section(
        "HOW OFTEN", "How often do the specials change?",
        ["Seasonally. Each offer carries its own end date and its own terms, so read the card "
         "before you book."],
        sid="rotation")
    body = f'''{specials_hero(d)}
<div class="xco-body">
  {offers}
  <div class="xco-split">
    <div>{redeem}</div>
    <div style="display:flex;flex-direction:column;gap:16px">{right}</div>
  </div>
  {combine}
  {T.table_section(d["table"])}
  {members}
  {rotation}
  {T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"])}
  {T.updated_line(UPDATED, UPDATED_ISO)}
</div>'''
    return shell(root_class, body)

def pages(root):
    return [(os.path.join(root, "pages", "company", "specials.html"), specials_page, SPECIALS, "xsp-specials")]
