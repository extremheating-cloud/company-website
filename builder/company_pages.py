"""Company pages — design_handoff_company_pages (screens 4a-4d).

/about · /contact · /financing-options · /specials, emitted to "pages/company/"
with the same embed conventions as the service pages.

Rewritten 2026-08-02 against scratchpad/seo/copy-company.md and local-seo.md §4:

  - Every page opens with an answer-first block (T.answer_block) as the first
    element after the <h1>, and closes with a visible "Last updated" line.
  - H2s are the questions a homeowner actually types, not slogans.
  - Each page carries one real <table> (T.table_section) so an engine that
    cannot parse a card grid can still cite the page.
  - /contact renders ALL FOUR offices from site_data.OFFICES. It used to
    hard-code two addresses, headed by metro ("Dayton") with a different city
    in the address beneath ("Beavercreek"). That mismatch is the NAP defect
    citation matchers trip over, and it is most of why Local SEO scored below
    the Framer site this replaces. Addresses live in ONE place now: site_data.

Facts come from site_data.py, which is the source of truth. Do not type an
address, a phone number, a licence number or a price into this file.
"""
import os
import template as T
import site_data as D

PHOTOS = T.PHOTOS  # real Extreme photography, commit-pinned — defined in template.py

# Visible "Last updated" stamp. Must match the schema dateModified for these
# routes; never stamp it from the build clock (geo-contract §8.2).
UPDATED = "August 2, 2026"
UPDATED_ISO = "2026-08-02"

# ---------------------------------------------------------------- CSS
COMPANY_CSS = """
/* ------------------------- company pages (4a-4d) ------------------------- */
.xco-2col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.xco-bcard{border:1px solid var(--rule);border-radius:16px;padding:20px;background:#fff}
.xco-bcard .t{font-weight:800;font-size:16.5px;margin-top:12px}
.xco-bcard .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xco-bcard .xsp-cta{margin-top:14px;font-size:14px;padding:12px 18px}
.xco-bcard .plink{display:inline-block;font-weight:800;font-size:14px;color:var(--purple);
text-decoration:none;margin-top:16px;min-height:44px;display:inline-flex;align-items:center}
.xco-bcard .plink:hover{color:var(--green-dark)}
.xco-phone{font-style:italic;font-weight:900;font-size:27px;letter-spacing:-.5px;margin-top:8px}
.xco-phone a{color:var(--ink);text-decoration:none}
.xco-loc{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}
.xco-loc-img{height:160px;background:#F4F6F8;border-bottom:1px solid var(--rule);display:flex;
align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:1px}
.xco-loc-img img{width:100%;height:100%;object-fit:cover;display:block}
.xco-loc-body{padding:18px}
.xco-loc-body .t{font-weight:800;font-size:16.5px}
.xco-loc-body .meta{font-size:12px;font-weight:700;color:var(--body);margin-top:2px}
.xco-loc-body .addr{font-size:13px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xco-loc-body .addr.hrs{font-size:12.5px;margin-top:6px}
.xco-loc-body a{display:inline-block;font-weight:800;font-size:13px;color:var(--purple);
text-decoration:none;margin-top:10px}
/* The two links stack rather than sit side by side: at 4-up the card is ~300px and a
   "Get directions" / "service area" pair wraps mid-phrase on the narrower ones. */
.xco-loc-body a.alt{display:block;margin-top:6px}
.xco-loc-body a:hover{color:var(--green-dark)}
/* A card with no exterior photograph (Troy, Waynesville) has no image box at all. It
   still has to line up with the two that do, so the body carries the shortfall. */
.xco-loc:not(:has(.xco-loc-img)) .xco-loc-body{padding-top:22px}
.xco-hours{border:1px solid var(--rule);border-radius:16px;margin-top:20px;overflow:hidden}
.xco-hours .row{display:flex;justify-content:space-between;gap:16px;padding:14px 20px;
border-bottom:1px solid var(--rule)}
.xco-hours .row:last-child{border-bottom:0}
.xco-hours .row span:first-child{font-weight:700;font-size:14px}
.xco-hours .row span:last-child{font-weight:600;font-size:14px;color:var(--body);text-align:right}
.xco-hours .row.em{background:var(--green-tint)}
.xco-hours .row.em span{font-weight:800;color:var(--promo-green)}
.xco-body{max-width:1280px;margin:0 auto;padding:56px 40px;display:flex;flex-direction:column;gap:48px}
/* Clearance for the hero booking card, which hangs into this section — only on the
   pages that actually render one (see .xsp-bookcol in template.py). */
.xhac-svc:has(.xsp-bookcol) .xco-body{padding-top:104px}
.xco-split{display:grid;grid-template-columns:1fr 360px;gap:48px}
.xco-heroslot{width:100%;height:250px;border-radius:16px;background:rgba(255,255,255,.08);
border:1px solid rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;
font-size:12px;font-weight:700;color:rgba(255,255,255,.55);letter-spacing:1px;overflow:hidden}
.xco-heroslot img{width:100%;height:100%;object-fit:cover;display:block}
.xco-hero-grid-400{grid-template-columns:1fr 400px;align-items:center}
.xco-ccard{border:1px solid var(--rule);border-radius:16px;padding:18px;background:#fff}
.xco-ccard .c{width:18px;height:18px;border-radius:50%;background:var(--green);color:#fff;
font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center}
.xco-ccard .t{font-weight:800;font-size:15px;margin-top:10px}
.xco-ccard .d{font-size:13px;line-height:1.5;font-weight:500;color:var(--body);margin-top:4px}
.xco-lchips{display:flex;align-items:center;gap:10px;margin-top:22px;flex-wrap:wrap}
.xco-lchips .lab{font-size:10.5px;font-weight:800;letter-spacing:1.5px;color:rgba(255,255,255,.5)}
.xco-lchips .chip{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);
border-radius:999px;padding:7px 14px;font-size:12px;font-weight:700;color:#fff}
.xco-fine{font-size:11px;font-weight:600;color:rgba(255,255,255,.45);margin-top:14px}
.xco-coupons{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px}
.xco-coupon{border:1.5px dashed #C4B5D4;border-radius:16px;padding:20px;display:flex;flex-direction:column}
.xco-coupon .pill{align-self:flex-start;background:var(--tint);color:var(--purple);font-size:10px;
font-weight:800;letter-spacing:1.5px;border-radius:999px;padding:5px 10px}
.xco-coupon .val{font-style:italic;font-weight:900;font-size:34px;letter-spacing:-1px;margin-top:12px}
.xco-coupon .val .per{font-size:16px;letter-spacing:0}
.xco-coupon .t{font-weight:800;font-size:15.5px;margin-top:2px}
.xco-coupon .d{font-size:13px;line-height:1.5;font-weight:500;color:var(--body);margin-top:4px;flex:1}
.xco-coupon .foot{display:flex;align-items:center;justify-content:space-between;gap:12px;
margin-top:16px;padding-top:14px;border-top:1px solid #EDEAF2}
.xco-coupon .lbl{font-size:11.5px;font-weight:700;color:var(--muted)}
.xco-claim{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:13px;padding:10px 16px;border-radius:10px;min-height:40px;
text-decoration:none;cursor:pointer;white-space:nowrap;transition:background .15s ease}
.xco-claim:hover{background:var(--green-hover)}
.xco-finenote{font-size:11.5px;line-height:1.6;font-weight:600;color:var(--muted);margin-top:24px}
.xco-mail{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:16px;
padding:22px;position:relative;overflow:hidden;color:#fff}
.xco-mail .t{font-weight:800;font-size:16px}
.xco-mail .d{font-size:12.5px;line-height:1.55;font-weight:500;color:rgba(255,255,255,.75);margin-top:6px}
.xco-mail form{display:flex;gap:8px;margin-top:14px}
.xco-mail input{flex:1;min-width:0;background:#fff;border:0;border-radius:10px;padding:12px 14px;
font-size:13px;font-weight:600;color:var(--ink);font-family:inherit}
.xco-mail button{background:var(--green);color:var(--ink);font-weight:800;font-size:13px;
padding:12px 16px;border-radius:10px;border:0;cursor:pointer;font-family:inherit}
.xco-story{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.xco-story p{margin-top:16px;font-size:14.5px;line-height:1.65;font-weight:500;color:var(--body)}
.xco-story p + p{margin-top:12px}
.xco-slot{width:100%;border-radius:16px;background:#F4F6F8;border:1px solid var(--rule);
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;
color:var(--muted);letter-spacing:1px;overflow:hidden}
.xco-slot img{width:100%;height:100%;object-fit:cover;display:block}
.xco-vals{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.xco-vals .xco-ccard .xsp-glyph{width:26px;height:26px}
.xco-vals .xco-ccard .t{margin-top:12px}
.xco-stats{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;
padding:32px 36px;position:relative;overflow:hidden}
.xco-stats .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;position:relative}
.xco-stats .n{font-style:italic;font-weight:900;font-size:30px;color:#fff}
.xco-stats .n .st{color:var(--stars)}
.xco-stats .cap{font-size:12.5px;line-height:1.5;font-weight:600;color:rgba(255,255,255,.75);margin-top:4px}
.xco-team{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.xco-team .slot{height:230px;border-radius:14px}
.xco-team .name{font-weight:800;font-size:14px;margin-top:10px}
.xco-team .role{font-size:12.5px;font-weight:600;color:var(--body)}
@media (max-width:809px){
.xco-2col{grid-template-columns:1fr;gap:12px;margin-top:16px}
.xco-hours .row{padding:13px 16px}
.xco-body{padding:40px 20px 48px;gap:40px}
.xhac-svc:has(.xsp-bookcol) .xco-body{padding-top:40px}
.xco-split{grid-template-columns:1fr;gap:40px}
.xco-hero-grid-400{grid-template-columns:1fr}
.xco-heroslot{height:200px;margin-top:24px}
.xco-coupons{grid-template-columns:1fr;gap:12px}
.xco-story{grid-template-columns:1fr;gap:20px}
.xco-story .xco-slot{height:200px}
.xco-vals{grid-template-columns:1fr;gap:12px}
.xco-stats{padding:26px 22px;border-radius:20px}
.xco-stats .grid{grid-template-columns:1fr 1fr;gap:18px}
.xco-team{grid-template-columns:1fr 1fr;gap:12px}
.xco-team .slot{height:180px}
}
"""

def shell(root_class, body, extra_css=""):
    """extra_css is for rules only one page needs. Keeping them out of COMPANY_CSS
    means editing one page's styles doesn't change the other three files, so a
    single-page revision stays a single Framer paste."""
    return f'''<section class="xhac-svc {root_class}">
  <style>{T.CSS}{COMPANY_CSS}{extra_css}</style>
{body}
{T.script("xhac-svc")}
</section>
'''

# ------------------------------------------------------- shared renderers
# Per client decision the page-specific ink CTA bands from mockups 4a-4d are
# omitted on all four company pages (the Footer component's CTA band covers it).
def section(eyebrow, h2, inner, lead=None, sid=None):
    """One page section. `lead` is the direct answer to the H2 question and goes
    between the heading and whatever the section renders — a question heading with
    a card grid under it and no sentence in between answers nothing."""
    anchor = f' id="{sid}"' if sid else ""
    return f'''<div{anchor}>
  <div class="xsp-eyebrow">{eyebrow}</div>
  <h2 class="xsp-h2">{h2}</h2>
  {T.paragraphs(lead)}
{inner}
</div>'''

def prose_section(eyebrow, h2, body, sid=None):
    """A section that is only a question and its answer."""
    return section(eyebrow, h2, "", lead=body, sid=sid)

# ================================================================
# /contact — mockup 4b (rail tier), copy verbatim
# ================================================================
# "same-day in most cases" was a response-time promise, and it is not one of the
# approved proof tokens. The approved wording is "90% same-day service"; anything
# looser reads as a guarantee the dispatcher cannot keep.
T.PROMOS["contactCall"] = dict(cls="lav", t="Need help right now?",
    d="Skip the form and call. A real person answers, day or night.",
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
  <div class="s">Office staffed Mon–Fri, 8–5 · emergencies 24/7.</div>
  <div class="btns">
    {T.schedule_btn("Schedule Service")}
    {T.call_btn(f"Call {T.PHONE_DISPLAY}")}
  </div>
  <div class="trust"><span><span class="st">★</span> {D.GOOGLE_RATING} from {D.REVIEW_COUNT} reviews</span><span class="bar">|</span><span>{D.YEARS_LOCAL} years local</span></div>
</div>'''

def contact_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
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

def slot_img(cls, photo, label, style=""):
    """A fixed-height photo box that renders either a placeholder or a real image.
    photo is a dict: {src, alt, pos?}. pos is object-position — the boxes here are
    wide and short, so a photo whose subject isn't dead centre needs it."""
    st = f' style="{style}"' if style else ""
    if not photo:
        return f'<div class="{cls}"{st} data-photo-slot>{label}</div>'
    p = f' style="object-position:{photo["pos"]}"' if photo.get("pos") else ""
    return (f'<div class="{cls}"{st}><img src="{photo["src"]}" alt="{photo.get("alt","")}"{p} '
            f'loading="lazy" decoding="async"></div>')

# Per-office presentation only. The addresses themselves live in site_data.OFFICES
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
    # metro is None for Waynesville on purpose — the client has not said whether it is
    # presented as Dayton, Cincinnati or Warren County, so nothing is guessed.
    metro = f'<div class="meta">Our {o["metro"]}-area shop</div>' if o.get("metro") else ""
    page = (f'<a href="{o["page"]}" class="alt">{o["locality"]} service area →</a>'
            if o.get("page") else "")
    return f'''<div class="xco-loc">
  {img}
  <div class="xco-loc-body">
    <div class="t">{o["locality"]}</div>
    {metro}
    <div class="addr">{o["street"]}<br>{o["citystate"]}</div>
    <div class="addr hrs">{o["hours"]}</div>
    <a href="{o["directions"]}">Get directions →</a>
    {page}
  </div>
</div>'''

def location_cards(d):
    cards = f'<div class="xco-2col">{"".join(location_card(o) for o in D.OFFICES)}</div>'
    lead = [
        'We work out of four Ohio shops. Beavercreek covers the Dayton side, Mason covers '
        'Cincinnati, and Troy and Waynesville fill in Miami and Warren counties between them.',
        f'One number reaches all four: <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>. There are '
        'no separate local lines.',
    ]
    return section("VISIT US", "Where are your offices?", cards,
                   lead=lead, sid="offices")

def offices_table():
    """The parseable copy of the office list. The cards carry the photos and the
    directions links; this carries the same four addresses in a shape an engine can
    lift whole. County comes from site_data, not from a coverage guess — dispatch
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
    # Addresses are NOT stored here. All four offices come from site_data.OFFICES, which
    # is client-confirmed 2026-08-02 and is also what the footer, the location pages and
    # the JSON-LD read. One written form, byte for byte, everywhere — a NAP audit compares
    # the visible block against the schema on the same page and a mismatch is
    # machine-detectable. See OFFICE_PHOTOS above for the per-card presentation.
    #
    # Hours confirmed by the client 2026-08-01, and now read from site_data. 8-5 weekdays
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
              "and plumbing, and it reaches all four Ohio offices."},
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

# ================================================================
# /financing-options — mockup 4c (rail tier), copy verbatim
# ================================================================
# Scoped to this page only (see shell(extra_css=...)) so the lender application
# styling doesn't churn /about, /contact and /specials.
FINANCING_CSS = """
/* --------------------- financing: lender application --------------------- */
/* Screen-reader-only. The apply controls read as "Apply Online" / "Start
   Application" visually; the extra span carries the new-tab warning and, on the
   chip, what the link actually does, since a lender name alone isn't a purpose. */
.xsp-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
clip:rect(0,0,0,0);white-space:nowrap;border:0}
/* A lender chip that is also the application link. Reads as a chip, behaves as a
   button: 44px target, arrow affordance, green border on hover. */
.xco-lchips a.chip{display:inline-flex;align-items:center;gap:7px;min-height:44px;
text-decoration:none;transition:background .15s ease,border-color .15s ease}
.xco-lchips a.chip:hover{background:rgba(255,255,255,.2);border-color:var(--green)}
.xco-lchips a.chip .arw{font-size:13px;line-height:1;color:var(--green-hover)}
.xco-apply{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:22px;
padding:18px 20px;border-radius:16px;background:rgba(255,255,255,.08);
border:1px solid rgba(255,255,255,.2)}
.xco-apply .k{font-weight:800;font-size:15.5px;color:#fff}
.xco-apply .s{font-size:12.5px;line-height:1.5;font-weight:500;color:rgba(255,255,255,.75);
margin-top:4px;max-width:52ch}
.xco-apply-btn{flex:none;display:inline-flex;align-items:center;justify-content:center;gap:8px;
background:var(--green);color:var(--ink);font-weight:800;font-size:14px;padding:12px 20px;
border-radius:10px;min-height:44px;text-decoration:none;white-space:nowrap;
box-shadow:0 6px 18px rgba(107,184,92,.28);transition:background .15s ease}
.xco-apply-btn:hover{background:var(--green-hover)}
.xco-apply-btn .arw{font-size:14px;line-height:1}
.xco-apply-btn:focus-visible,.xco-lchips a.chip:focus-visible{outline:3px solid #61BC47;
outline-offset:2px}
/* The fine print under the Apply button now carries a legal disclosure rather than
   a single throwaway line, so it gets readable weight and a real line height. The
   shared .xco-fine is 11px at 45% white, which is fine for a one-liner and not for
   this. Scoped here so nothing else on the site moves. */
.xco-fine{font-size:11.5px;line-height:1.6;color:rgba(255,255,255,.62);max-width:66ch}
.xco-fine a{color:rgba(255,255,255,.88);font-weight:700;text-decoration:underline;
text-underline-offset:2px}
.xco-fine a:hover{color:var(--green-hover)}
.xsp-book .trust{flex-wrap:wrap;row-gap:4px}
.xsp-book .trust a{color:var(--purple);font-weight:700;text-decoration:none}
.xsp-book .trust a:hover{color:var(--green-dark);text-decoration:underline}
@media (max-width:809px){
.xco-apply{flex-direction:column;align-items:stretch;gap:16px;padding:18px}
.xco-apply-btn{width:100%;padding:14px}
}
"""
T.PROMOS["finSpecials"] = dict(cls="lav", t="Stack a seasonal special",
    d="Current offers can be combined with financing for the best total price.",
    lm="See Specials →", href="/specials")
T.PROMOS["finXplan"] = dict(cls="mint", t="Protect the new system",
    d="X-Plan keeps your warranty valid with two documented tune-ups a year.",
    lm="Explore X-Plan →", href="/maintenance")
T.PROMOS["spFinance"] = dict(cls="lav", t="Big job? Finance it.",
    d="Specials stack with monthly payment plans through our lenders.",
    lm="Financing Options →", href="/financing-options")

# Apply Online CTA target — the live merchant application link, client-supplied
# 2026-07-31. It is Wright-Patt Credit Union's MerchantLinq portal, so it is one
# lender's application, not an aggregator across all three. Every apply CTA on
# this page names Wright-Patt for that reason; do not relabel them to a generic
# "our lenders" without a link that actually covers GoodLeap and Synchrony.
#
# TODO (marketing): confirm whether GoodLeap and Synchrony have their own customer
# application links. If they do, this becomes a three-way chooser rather than one
# button. Every apply control is marked data-apply-cta for a one-pass swap.
APPLY_HREF = ("https://wpcu.merchantlinq.com/customer?t=Sk0wSVBrdjV0VUxsUnJwbXNwWWtpaFhRdmNxN0o1S1"
              "V2V2E3NlVnM0xyKjFrODNIKlN1eDlQbElZNEpRT25lOWNBQnJvajUyYTVBNGduaDdwNWJqNDJzZFNLSGQq"
              "U3dkVUlKWmxSRUNlTmZIblZtUkowY1ZUWm8qU2RHSW1WM0JFUnFONXZINlN4cGxSQk1QcTdHeEpXZlB5RH"
              "laS3drYjVJZXdBREJFVGNwemkzeUtaVFRpTGR2QWxRc1FBMHZ1RTNPdzhydW9iWHdhTHJqTExGNWVzQWFl"
              "bWc9PQ==")
APPLY_LENDER = "Wright-Patt Credit Union"
# The page renders inside a Framer embed iframe. Left to itself, template.py's link
# handler retargets every off-site link to _top, which would replace the whole site
# with the lender's portal. An application the customer may abandon belongs in its
# own tab, so these carry an explicit target the handler now leaves alone.
APPLY_ATTRS = f'href="{APPLY_HREF}" target="_blank" rel="noopener noreferrer" data-apply-cta'

def apply_card():
    return f'''<div class="xsp-book">
  <div class="eyebrow">FINANCING</div>
  <div class="t">Apply in minutes.</div>
  <div class="s">A quick, secure application through {APPLY_LENDER} — most decisions come back right away.</div>
  <div class="btns">
    <a class="xsp-btn-green" {APPLY_ATTRS}>Apply Online</a>
    {T.call_btn(f"Call {T.PHONE_DISPLAY}")}
  </div>
  <!-- The mockup's trust row read "Secure application | No obligation". The first
       item now duplicates the sub-copy above it ("A quick, secure application…"),
       so it gives up its slot to the terms link rather than wrapping to a second
       line in a 360px card. -->
  <div class="trust"><span>No obligation</span><span class="bar">|</span><a href="/terms#financing">Financing terms</a></div>
</div>'''

def financing_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas xsp-mb">
        <a class="xsp-cta" {APPLY_ATTRS}>Apply Online</a>
        <a class="xsp-cta-outline" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
      </div>
      {T.chips(d["heroChips"])}
    </div>
    <div class="xsp-bookcol">{apply_card()}</div>
  </div>
</div>'''

def check_cards(eyebrow, h2, cards, lead=None, sid=None):
    inner = "".join(
        f'''<div class="xco-ccard"><span class="c">✓</span>
  <div class="t">{c["t"]}</div><div class="d">{c["d"]}</div></div>''' for c in cards)
    return section(eyebrow, h2, f'<div class="xco-2col">{inner}</div>', lead=lead, sid=sid)

def checks_only(eyebrow, h2, items, lead=None, sid=None):
    inner = "".join(f'<div class="xsp-check"><span class="c">✓</span>{i}</div>' for i in items)
    return section(eyebrow, h2, f'<div class="xsp-checks">{inner}</div>', lead=lead, sid=sid)

def lender_chip(name):
    """The lender that has a live application link gets a clickable chip; the
    others stay plain. Same visual weight either way, so the row still reads as
    three equal lenders rather than one endorsed one."""
    if name != APPLY_LENDER:
        return f'<div class="chip">{name}</div>'
    return (f'<a class="chip" {APPLY_ATTRS}>{name}'
            f'<span class="arw" aria-hidden="true">→</span>'
            f'<span class="xsp-sr">— apply online, opens in a new tab</span></a>')

def apply_panel():
    return f'''<div class="xco-apply">
    <div>
      <div class="k">Apply with {APPLY_LENDER}</div>
      <div class="s">A short, secure application on {APPLY_LENDER}'s site. Most decisions come back right away, and there's no obligation to move forward.</div>
    </div>
    <a class="xco-apply-btn" {APPLY_ATTRS}>Start Application
      <span class="arw" aria-hidden="true">→</span>
      <span class="xsp-sr">(opens in a new tab)</span>
    </a>
  </div>'''

def lenders_panel(v):
    stats = "".join(
        f'<div><div class="n">{s["n"]}</div><div class="cap">{s["cap"]}</div></div>' for s in v["stats"])
    chips = "".join(lender_chip(l) for l in v["lenders"])
    # No rates, APRs, or program terms here — by client instruction 2026-08-01,
    # Extreme is not permitted to advertise them. This is a standing constraint, not
    # a gap waiting to be filled: do not add a rate later thinking it was an
    # oversight. The lender states its own terms on its own application.
    return f'''<div class="xsp-value" id="xco-lenders">
  <div class="eyebrow">GOOD TO KNOW</div>
  <h3>{v["h2"]}</h3>
  <div class="stats">{stats}</div>
  <div class="xco-lchips"><span class="lab">OUR LENDERS</span>{chips}</div>
  {apply_panel()}
  <div class="xco-fine">{v["fine"]}</div>
</div>'''

FINANCING = {
    "breadcrumb": [("Home", "/"), ("Financing", "")],
    "h1": "HVAC and plumbing {X} in Dayton and Cincinnati",
    "h1Highlight": "financing",
    "answer": ("You can finance heating, cooling and plumbing work, and three lenders look at "
               "your application instead of one. Applying only asks for pre-approval, so it "
               "doesn't commit you to buying, and the lender sets the rate and the term."),
    # The old H1, demoted to the deck line.
    "intro": "A new system now. Payments that fit.",
    # REG Z. "$0 Down Options" and the "$0 down" stat below state an amount of down
    # payment. Under 12 CFR 1026.24(d)(1) that is a triggering term for closed-end
    # credit: an ad that states it must ALSO disclose the terms of repayment and the
    # APR, and Extreme is not permitted to publish either. Both were replaced with
    # non-triggering wording on 2026-08-02 per scratchpad/seo/copy-company.md §0a.5.
    #
    # MARKETING + LENDER SIGN-OFF STILL REQUIRED. This is a change to approved
    # marketing copy made on a legal-risk basis, not a copy preference. If the lender
    # confirms the claim can carry its required disclosures, it can come back.
    "heroChips": ["Apply in Minutes", "No Prepayment Penalty", "Options for Most Credit"],
    "why": [
        {"t": "One bill becomes a monthly payment",
         "d": "Spread the cost of a new system over time instead of paying it all at once."},
        {"t": "Don't downgrade the fix",
         "d": "Choose the system that's right for your home — not just the one that fits this month's budget."},
        {"t": "Keep your emergency fund intact",
         "d": "Breakdowns never pick a convenient month. Financing keeps your cushion where it belongs."},
        {"t": "Stacks with seasonal specials",
         "d": "Take whatever offer is running off the price, then put the rest on a monthly plan."},
    ],
    "qualifies": [
        "New AC or furnace installation",
        "Heat pumps &amp; ductless systems",
        "Water heaters — tank &amp; tankless",
        "Major HVAC &amp; plumbing repairs",
        "Indoor air quality equipment",
        "Sewer line &amp; repiping projects",
    ],
    "process": {
        "h2": "How do I apply for financing?",
        "steps": [
            {"title": "Get your upfront quote",
             "desc": "Your tech or comfort advisor prices the work first — so you know exactly what you're financing."},
            {"title": "Apply online in minutes",
             "desc": "A short, secure application through one of our lenders — most decisions come back right away."},
            {"title": "Approved &amp; installed",
             "desc": "We schedule the work — often the same week — and your monthly plan starts after the job is done right."},
        ],
    },
    "lenders": {
        "h2": "Financing that works like you'd hope.",
        "stats": [
            {"n": "Minutes", "cap": "to apply and get a decision — right from your kitchen table."},
            # Was "$0 down" — see the REG Z note on heroChips above. "Three lenders" is a
            # count of who reviews the application, not a term of credit, so it triggers
            # no disclosure obligation.
            {"n": "Three", "cap": "lenders reviewing your application, not one."},
            {"n": "No penalty", "cap": "for paying your plan off early."},
        ],
        "lenders": D.LENDERS,
        # Sits directly under the Apply button, which is where a customer decides.
        # Says the one thing that most often gets misunderstood — that applying is
        # a pre-approval, not a commitment — and links the full financing terms.
        "fine": ('Financing subject to credit approval. Applying is a request for pre-approval, '
                 'not an agreement to buy or to lend, and rates and terms are set by the lender. '
                 'See <a href="/terms#financing">full financing terms</a>.'),
    },
    "faqEyebrow": "FINANCING QUESTIONS",
    "faqH2": "What do people ask before applying?",
    # First Q&A is verbatim from mockup 4c; the others are authored from approved
    # claims (soft pull, no early-payoff penalty, stacks with specials, plural
    # lenders, lender sets the rate).
    #
    # [VERIFY] The soft-inquiry and no-early-payoff-penalty answers are asserted for
    # all three lenders. Confirm each one individually — if one runs a hard pull at
    # the options stage, the first answer has to be narrowed to the lenders it is
    # true for.
    "faq": [
        {"q": "Does applying affect my credit score?",
         "a": "Checking your options starts with a soft inquiry that doesn't affect your score. A full application follows only if you decide to move forward."},
        {"q": "What if my credit isn't perfect?",
         "a": "That's why we work with more than one lender. GoodLeap, Synchrony, and Wright-Patt Credit Union each cover a range of credit situations, and checking your options costs nothing."},
        {"q": "Can I pay it off early?",
         "a": "Yes. There's no penalty for paying your plan off early."},
        {"q": "Who sets the interest rate?",
         "a": "The lender does, not us. The rate and the term are both spelled out in their application, before you sign anything."},
        {"q": "Can I combine financing with specials?",
         "a": 'Yes. Whatever <a href="/specials">offer is running</a> comes off the price first, and the rest goes on the monthly plan.'},
    ],
    # The kitchen-table framing, with no dollar figure, no APR and no monthly amount,
    # so nothing in it triggers a Reg Z disclosure obligation.
    "table": {
        "eyebrow": "FINANCE OR PAY UPFRONT",
        "h2": "Is financing worth it compared with paying upfront?",
        "id": "compare",
        "takeaway": "Financing exists so a system that failed without warning doesn't push you "
                    "into a smaller unit or an empty savings account.",
        "caption": "Financing versus paying in full for a system replacement",
        "columns": ["What we look at", "Finance when", "Pay in full when"],
        "rows": [
            ["Timing", "The system already failed and replacement cannot wait",
             "The replacement is planned months ahead"],
            ["Cash on hand", "Paying in full would empty the emergency fund",
             "Cash is available without touching reserves"],
            ["System choice", "Budget alone would force a smaller or lower-efficiency system",
             "The preferred system is affordable outright"],
            ["Total cost", "A monthly payment is worth the finance charge",
             "Avoiding any finance charge is the priority"],
            ["Credit", "Credit is in reasonable shape and pre-approval is likely",
             "Credit is being repaired and a new account would set it back"],
        ],
    },
    "rail": {
        # The cropped file — the uncropped original frames a competitor's service
        # sticker, phone number and all. Do not swap this back.
        "photo": T.PHOTOS["ruudInstall"],
        # Was "in a Dayton-area home", which nothing in the repo establishes about this
        # frame. The alt describes what is in the photograph.
        "photoAlt": f"A Ruud air handler installed by {D.COMPANY}",
        # 625x1600 portrait in a 360x220 landscape slot: object-fit:cover fits the
        # width exactly and crops the height, so only the vertical axis does anything
        # here. 55% lands the visible band on the Ruud badge and spec plate — measured
        # against the crop, not the original.
        "photoPos": "50% 55%",
        "promos": ["finSpecials", "finXplan"],
    },
}

def financing_page(d, root_class):
    left = [
        T.mobile_photo(d["rail"]),
        check_cards("WHY FINANCE", "Can I finance a new furnace or AC?", d["why"],
                    sid="why",
                    lead=["Yes. New furnaces, air conditioners, heat pumps, water heaters and "
                          "the bigger repairs all qualify. The money comes from the lender "
                          "rather than from us, so approval, rate and term are theirs to set."]),
        checks_only("WHAT QUALIFIES", "What kind of work qualifies for financing?",
                    d["qualifies"], sid="qualifies",
                    lead=["Anything big enough that writing one check would sting: "
                          '<a href="/ac-installation">AC installation</a>, '
                          '<a href="/furnace-installation">furnace installation</a>, heat pumps '
                          'and ductless systems, tank and tankless '
                          '<a href="/plumbing/water-heater/installation">water heaters</a>, '
                          'major repairs, air quality equipment, sewer lines and repiping.']),
        T.process(d["process"], eyebrow="HOW IT WORKS"),
        section("OUR LENDERS", "Which lenders do you work with?",
                lenders_panel(d["lenders"]), sid="lenders",
                lead=[f'Three, not one: {", ".join(D.LENDERS[:-1])} and {D.LENDERS[-1]}. Working '
                      "with more than one lender is what gets an approval across a wider range "
                      "of credit situations, and finding out what you qualify for costs "
                      "nothing."]),
        T.table_section(d["table"]),
        T.mobile_inline_rail(d),
        T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"]),
        T.updated_line(UPDATED, UPDATED_ISO),
    ]
    body = f'''{financing_hero(d)}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {T.rail(d["rail"])}
</div>'''
    return shell(root_class, body, extra_css=FINANCING_CSS)

# ================================================================
# /specials — mockup 4d (full-width tier), copy verbatim
# ================================================================
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
     "desc": f'New customers save {D.REWARDS["newSystem"]} on a new heating, cooling or plumbing system, or {D.REWARDS["everythingElse"]} on everything else. Name whoever sent you when you book.',
     "foot": "Always available", "cta": "/referral", "ctaLabel": "See Extreme Rewards"},
    {"pill": "PLUMBING", "value": "$99", "title": "Drain Clearing Special",
     "desc": "Single accessible drain cleared, with a camera check if the clog keeps coming back.",
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
             f'{D.REWARDS["everythingElse"]} on everything else',
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
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
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

# ================================================================
# /about — mockup 4a (full-width tier), copy verbatim
# ================================================================
ABOUT = {
    "breadcrumb": [("Home", "/"), ("About Us", "")],
    "h1": "About {X} Heating, Air, Plumbing",
    "h1Highlight": "Extreme",
    # The two Ohio licence numbers are the single cheapest trust win on the site:
    # externally verifiable, and no competitor in the Dayton SERP publishes theirs.
    # Until the team section comes back after the photo shoot, the licences and the
    # founding year are what this page's expertise signal actually rests on.
    "answer": ("We're a locally owned heating, cooling and plumbing company, working the Dayton "
               f"and Cincinnati metros out of four Ohio shops since {D.FOUNDED}. We hold Ohio "
               f"licenses in both trades, and we've done more than "
               f"{D.JOBS_COMPLETED_LONG.rstrip('+')} jobs."),
    # The old H1, demoted to the deck line.
    "intro": "Locally owned. Extremely committed.",
    # "4.9 on Google" was wrong: the aggregate is Birdeye across platforms. The licence
    # chip is the only item on this row a customer can independently verify.
    "heroChips": ["Family Owned &amp; Operated", f"{D.YEARS_LOCAL} Years Local",
                  f"{D.GOOGLE_RATING} from {D.REVIEW_COUNT} reviews",
                  f"{D.LICENSE_HVAC} &middot; {D.LICENSE_PLUMBING}"],
    # PLACEHOLDERS until Block B of the shot list is shot. Both are real Extreme
    # photography, but neither is what its slot ultimately wants:
    #  - hero wants a team lineup; this is the branded vehicle at a community event
    #  - the story slot wants founders / the first van; this is a current van
    # The story copy says "From one van to the whole Miami Valley" — do NOT let the
    # alt text or any caption imply this photo is that first van.
    "heroPhoto": {"src": PHOTOS["troy"], "pos": "50% 45%",
                  "alt": f"The {D.COMPANY} team at a community event in Troy, Ohio"},
    "storyPhoto": {"src": PHOTOS["skyline"],
                   "alt": f"An {D.COMPANY} service van with the Dayton skyline behind it"},
    "story": {
        "h2": "How long have you been doing this?",
        # Founding year and the Mason opening are client-confirmed (2026-08-02). Dates
        # are worth stating plainly rather than as "two decades" — they are the kind of
        # specific, checkable fact both readers and AI answers cite.
        # [NEEDS: opening years for the Troy and Waynesville offices. Two more dates
        # would turn this paragraph into a timeline, which is a far stronger citation
        # target than a single founding year.]
        "p1": f"We started in {D.FOUNDED} the way most good service companies do: one van, one toolbox, and a promise to show up when we said we would. Mason opened in {D.MASON_OPENED}. Today it's four Ohio shops and a full crew of licensed HVAC and plumbing techs covering the same two metros.",
        "p2": "The work got bigger. The way it's priced didn't. You get a flat quote and you approve it before we open anything up, and a real person still answers the phone, day or night.",
    },
    "values": [
        {"t": "Honest pricing, upfront",
         "d": "Flat quotes you approve before we start. No surprise line items, ever."},
        {"t": "Your home, respected",
         "d": "Shoe covers, drop cloths, and a workspace left cleaner than we found it."},
        {"t": "Fast when it matters",
         "d": "90% of calls handled same-day, with a 24/7 line for real emergencies."},
        {"t": "Built on referrals",
         "d": "Most new customers come from old ones. We earn that, one visit at a time."},
    ],
    "stats": [
        {"n": D.YEARS_LOCAL, "cap": "years serving Ohio homes"},
        # The 4.9 is a Birdeye aggregate across platforms, not a Google-only rating.
        # The caption carries the denominator, because a rating with no review count
        # is the shape of a claim rather than a claim.
        {"n": f'<span class="st">★</span> {D.GOOGLE_RATING}',
         "cap": f"average across {D.REVIEW_COUNT} {D.REVIEW_SOURCE}"},
        {"n": D.SAME_DAY, "cap": "of calls handled same-day"},
        {"n": "24/7", "cap": "emergency service line"},
    ],
    # TODO: replace placeholder team names/roles with real staff + headshots (handoff 4a)
    # Real team, photos client-supplied 2026-08-01. Each was cropped to a
    # head-and-shoulders portrait at matching framing — the row runs four across and
    # mismatched crops are the first thing you notice.
    # TODO (client): confirm roles and years with the team for each person.
    #
    # NOT RENDERED. See the note in about_page() — the section is off the page until
    # the company photo shoot lands. Do not re-add it here or in the assembler.
    "team": [
        {"name": "Anthony Griffin", "role": "Installer", "photo": PHOTOS["team"]["anthony-griffin"]},
        {"name": "Jayvon Kilgore",  "role": "Installer", "photo": PHOTOS["team"]["jayvon-kilgore"]},
        {"name": "Joe Richardson",  "role": "Comfort Advisor", "photo": PHOTOS["team"]["joe-richardson"]},
        {"name": "Tyler Hardy",     "role": "Installer", "photo": PHOTOS["team"]["tyler-hardy"]},
    ],
    # Both cards used to point at /locations, so two differently-labelled links went
    # to the same place. The per-city pages exist; these are them.
    #
    # Loveland was removed from the Cincinnati card: it is not in builder/locations.py
    # and has no page, so it was a coverage claim with nothing behind it.
    "areas": [
        {"t": "Dayton metro",
         "d": "Dayton, Kettering, Beavercreek, Centerville, Springboro, Huber Heights and the surrounding Miami Valley.",
         "lm": "our Dayton service area →", "href": "/locations/dayton"},
        {"t": "Cincinnati metro",
         "d": "Cincinnati, Mason, West Chester, Fairfield, Middletown, Lebanon and communities across the metro.",
         "lm": "our Cincinnati service area →", "href": "/locations/cincinnati"},
    ],
    "table": {
        "eyebrow": "AT A GLANCE",
        "h2": "Who am I actually hiring?",
        "id": "at-a-glance",
        "takeaway": f"We've served the Dayton and Cincinnati metros since {D.FOUNDED}, under "
                    "Ohio HVAC license #37179.",
        "caption": "Company details at a glance",
        # A key/value fact sheet, so the second column has no name of its own —
        # "Detail | Extreme" read as though Extreme were one of several things being
        # compared. The row header carries the meaning; this just labels the pair.
        "columns": ["What you're asking", "The answer"],
        "rows": [
            ["Founded", f"{D.FOUNDED}, locally owned ever since"],
            ["Trades", "Heating, cooling, indoor air quality, residential plumbing"],
            ["Service area", "Dayton and Cincinnati metros, nine Ohio counties"],
            ["Offices", " · ".join(o["locality"] for o in D.OFFICES)],
            ["Ohio licenses", f'HVAC {D.LICENSE_HVAC} &middot; Plumbing {D.LICENSE_PLUMBING}'],
            ["Legal entities", f"{D.ENTITY_HVAC} (HVAC) · {D.ENTITY_PLUMBING} (plumbing)"],
            ["Jobs completed", D.JOBS_COMPLETED_LONG],
            ["Customer reviews", f"{D.GOOGLE_RATING}-star average across {D.REVIEW_COUNT} reviews"],
            ["Emergency service", "24/7, every day of the year"],
            ["Same-day service", f"{D.SAME_DAY} same-day service"],
            ["Membership", f'X-Plan, {D.XPLAN["annual"]} per year or {D.XPLAN["monthly"]} per month per system'],
        ],
    },
    "faqEyebrow": "ABOUT THE COMPANY",
    "faqH2": "What else do people ask?",
    # [NEEDS: is commercial work in scope? Third-party directory listings describe
    # Extreme as residential and commercial, and there is no commercial route on the
    # site. Either answer is fine; the mismatch between the two is not. The question is
    # deliberately absent until the client answers it.]
    "faq": [
        {"q": "When did you start?",
         "a": f"{D.FOUNDED}, and we've been locally owned ever since. The Mason office opened "
              f"in {D.MASON_OPENED}."},
        {"q": "Are you a franchise?",
         "a": "No. Locally owned, run out of four Ohio offices, and not part of a national "
              "chain."},
        {"q": "What are your Ohio license numbers?",
         "a": "Ohio HVAC #37179 and Ohio plumbing #13557. Both are on our estimates, invoices "
              'and trucks, as Ohio requires, and the <a href="/terms">license numbers and '
              'program terms</a> are on the terms page.'},
        {"q": "Do you do both HVAC and plumbing?",
         "a": 'Yes. Heating, cooling, indoor air quality and residential plumbing. One phone '
              'number and one <a href="/maintenance">X-Plan membership</a> cover both trades.'},
        {"q": "How many jobs have you done?",
         "a": f"More than {D.JOBS_COMPLETED_LONG.rstrip('+')} across the two metros since "
              f"{D.FOUNDED}."},
        {"q": "How do I get in touch?",
         "a": f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a> reaches all four offices. '
              '<a href="/contact">Addresses and directions</a> are on the contact page, and '
              '<a href="/referral">Extreme Rewards</a> pays you for sending someone new.'},
    ],
}

def about_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid xco-hero-grid-400">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      {T.chips(d["heroChips"])}
    </div>
    {slot_img("xco-heroslot", d.get("heroPhoto"), "DROP A TEAM PHOTO HERE")}
  </div>
</div>'''

def about_page(d, root_class):
    story = f'''<div>
  <div class="xco-story">
    <div>
      <div class="xsp-eyebrow">OUR STORY</div>
      <h2 class="xsp-h2">{d["story"]["h2"]}</h2>
      <p>{d["story"]["p1"]}</p>
      <p>{d["story"]["p2"]}</p>
    </div>
    {slot_img("xco-slot", d.get("storyPhoto"), "DROP A FOUNDERS / FIRST-VAN PHOTO",
              style="height:280px")}
  </div>
</div>'''
    licensed = prose_section(
        "LICENSED IN OHIO", "Are you licensed and insured?",
        ["Yes, on both counts: Ohio HVAC license #37179 and Ohio plumbing license #13557. Every "
         "tech is licensed and insured, and drug-tested and background-checked before they set "
         "foot in your house.",
         f'Heating and cooling runs through {D.ENTITY_HVAC}, plumbing through '
         f'{D.ENTITY_PLUMBING}. Both sets of '
         '<a href="/terms">license numbers and program terms</a> are on the terms page.'],
        sid="licensed")
    # [NEEDS: does the scheduler send a technician name and photo before arrival? It is
    # one of the strongest trust signals in the trade and it costs nothing to state.
    # Not written until the client confirms it happens.]
    who = prose_section(
        "AT YOUR DOOR", "Who will come to my house?",
        ["A licensed, insured technician in a marked company van. Shoe covers and drop cloths "
         "go down before anything starts, and we leave the space cleaner than we found it."],
        sid="who")
    values = "".join(
        f'''<div class="xco-ccard"><span class="xsp-glyph"><i></i><i></i></span>
  <div class="t">{v["t"]}</div><div class="d">{v["d"]}</div></div>''' for v in d["values"])
    values = section("WHAT WE STAND FOR", "How do you price a job?",
                     f'<div class="xco-vals">{values}</div>', sid="pricing",
                     lead=["Flat price, quoted before we start, and you approve it before "
                           "anything gets opened up. Estimates on replacements and new installs "
                           "are free, X-Plan members take 15% off repairs, and "
                           '<a href="/financing-options">financing covers the bigger '
                           "jobs</a>."])
    stats = "".join(
        f'<div><div class="n">{s["n"]}</div><div class="cap">{s["cap"]}</div></div>' for s in d["stats"])
    stats = f'''<div class="xco-stats">
  <img class="mark" src="{T.X_MARK}" alt="" style="position:absolute;right:-70px;bottom:-60px;width:300px;opacity:.06;transform:rotate(-8deg);filter:brightness(0) invert(1)">
  <div class="grid">{stats}</div>
</div>'''
    # The team section is off the page until the company photo shoot (client, 2026-08-02
    # — headshots for the whole company, then this page gets rebuilt around them). The
    # four names that were here carried roles guessed from filenames, so publishing
    # them was misattributing real people. Renderer and CSS stay; only the call is
    # removed, so restoring it is one line once the photos land.
    team = ""
    areas = "".join(
        f'''<a class="xsp-card" href="{a["href"]}">
  <span class="txt"><span class="t">{a["t"]}</span><br><span class="d">{a["d"]}</span></span>
  <span class="lm">{a["lm"]}</span><span class="mrow">→</span>
</a>''' for a in d["areas"])
    areas = section("WHERE WE WORK", "Do you come out to my town?",
                    f'<div class="xco-2col">{areas}</div>', sid="service-area",
                    lead=["Probably. We work across nine Ohio counties between the two metros: "
                          "Montgomery, Greene, Miami, Warren, Butler, Clark, Hamilton, Preble "
                          "and Darke."])
    # The full four-row address table lives on /contact only. Duplicating it here is a
    # near-duplicate-content signal on the two pages most likely to be compared.
    offices = prose_section(
        "OUR OFFICES", "Where are your offices?",
        ['Four of them, all in Ohio: '
         + ", ".join(o["locality"] for o in D.OFFICES[:-1]) + f' and {D.OFFICES[-1]["locality"]}. '
         f'They all route to the same number, '
         f'<a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>, and the '
         '<a href="/contact">addresses and directions</a> are on the contact page.'],
        sid="offices")
    reviews = prose_section(
        "WHAT CUSTOMERS SAY", "What do customers say?",
        [f"{D.GOOGLE_RATING} stars across {D.REVIEW_COUNT} {D.REVIEW_SOURCE} from homeowners "
         "around Dayton and Cincinnati. That number is a Birdeye aggregate, so it pulls from "
         "every platform people leave reviews on rather than from a single site."],
        sid="reviews")
    body = f'''{about_hero(d)}
<div class="xco-body">
  {story}
  {licensed}
  {who}
  {values}
  {stats}
  {team}
  {offices}
  {areas}
  {reviews}
  {T.table_section(d["table"])}
  {T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"])}
  {T.updated_line(UPDATED, UPDATED_ISO)}
</div>'''
    return shell(root_class, body)

# ------------------------------------------------------------ registry
def pages(root):
    other = os.path.join(root, "pages", "company")
    return [
        (os.path.join(other, "contact.html"), contact_page, CONTACT, "xsp-contact"),
        (os.path.join(other, "financing-options.html"), financing_page, FINANCING, "xsp-financing-options"),
        (os.path.join(other, "specials.html"), specials_page, SPECIALS, "xsp-specials"),
        (os.path.join(other, "about.html"), about_page, ABOUT, "xsp-about"),
    ]
