"""Company pages — design_handoff_company_pages (screens 4a-4d).

/about · /contact · /financing-options · /specials, emitted to "pages/company/"
with the same embed conventions as the service pages. Copy is verbatim from
the mockups; placeholders carry TODO markers per the handoff README.
"""
import os
import template as T

PHOTOS = T.PHOTOS  # real Extreme photography, commit-pinned — defined in template.py

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
.xco-loc-body .addr{font-size:13px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xco-loc-body a{display:inline-block;font-weight:800;font-size:13px;color:var(--purple);
text-decoration:none;margin-top:10px}
.xco-loc-body a:hover{color:var(--green-dark)}
.xco-hours{border:1px solid var(--rule);border-radius:16px;margin-top:20px;overflow:hidden}
.xco-hours .row{display:flex;justify-content:space-between;gap:16px;padding:14px 20px;
border-bottom:1px solid var(--rule)}
.xco-hours .row:last-child{border-bottom:0}
.xco-hours .row span:first-child{font-weight:700;font-size:14px}
.xco-hours .row span:last-child{font-weight:600;font-size:14px;color:var(--body);text-align:right}
.xco-hours .row.em{background:var(--green-tint)}
.xco-hours .row.em span{font-weight:800;color:var(--promo-green)}
.xco-body{max-width:1280px;margin:0 auto;padding:56px 40px;display:flex;flex-direction:column;gap:48px}
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
def section(eyebrow, h2, inner):
    return f'''<div>
  <div class="xsp-eyebrow">{eyebrow}</div>
  <h2 class="xsp-h2">{h2}</h2>
{inner}
</div>'''

# ================================================================
# /contact — mockup 4b (rail tier), copy verbatim
# ================================================================
T.PROMOS["contactCall"] = dict(cls="lav", t="Need help right now?",
    d="Skip the form — call and we'll dispatch a tech, same-day in most cases.",
    lm=f"Call {T.PHONE_DISPLAY} →", href=T.PHONE_TEL)
T.PROMOS["contactXplan"] = dict(cls="mint", t="X-Plan members skip the line",
    d="Priority scheduling, two tune-ups a year, and 15% off repairs.",
    lm="Explore X-Plan →", href="/maintenance")

def contact_card():
    # TODO: confirm real office hours (handoff: "Office hours Mon-Fri · emergencies 24/7." is placeholder wording)
    return f'''<div class="xsp-book">
  <div class="eyebrow">CONTACT US</div>
  <div class="xco-phone"><a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a></div>
  <div class="s">Office staffed Mon–Fri, 8–5 · emergencies 24/7.</div>
  <div class="btns">
    {T.schedule_btn("Schedule Service")}
    {T.call_btn(f"Call {T.PHONE_DISPLAY}")}
  </div>
  <div class="trust"><span><span class="st">★</span> 4.9 on Google</span><span class="bar">|</span><span>20+ years local</span></div>
</div>'''

def contact_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
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
    <div class="d">Hit Schedule Service and pick a time that works — it takes about a minute, day or night.</div>
    <a class="xsp-cta js-schedule" href="#" role="button">Schedule Service</a>
  </div>
  <div class="xco-bcard">
    <span class="xsp-glyph"><i></i><i></i></span>
    <div class="t">Call the office</div>
    <div class="d">Talk to a real person — same-day dispatch in most cases, and 24/7 help in emergencies.</div>
    <a class="plink" href="{T.PHONE_TEL}">{T.PHONE_DISPLAY} →</a>
  </div>
</div>'''
    return section("BOOK A VISIT", "Two ways to get on the schedule.", cards)

def maps_dir(address):
    """A Google Maps directions link for a street address. The link text says "Get
    directions", so this uses the dir endpoint rather than a name search — a search
    for the company name can land on the wrong pin or a disambiguation list."""
    from urllib.parse import quote
    # & is escaped because this goes straight into an href in the HTML.
    return f"https://www.google.com/maps/dir/?api=1&amp;destination={quote(address)}"

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

def location_card(loc):
    img = slot_img("xco-loc-img", loc.get("photo"), loc.get("photoLabel", ""))
    return f'''<div class="xco-loc">
  {img}
  <div class="xco-loc-body">
    <div class="t">{loc["city"]}</div>
    <div class="addr">{loc["address"]}</div>
    <a href="{loc["directions"]}">Get directions →</a>
  </div>
</div>'''

def location_cards(d):
    cards = f'<div class="xco-2col">{"".join(location_card(l) for l in d["locations"])}</div>'
    return section("VISIT US", "Two locations, one phone number.", cards)

def hours_table(d):
    rows = []
    for row in d["hours"]:
        em = ' em' if row.get("em") else ""
        rows.append(f'<div class="row{em}"><span>{row["label"]}</span><span>{row["value"]}</span></div>')
    return section("HOURS", "When to reach us.", f'<div class="xco-hours">{"".join(rows)}</div>')

CONTACT = {
    "breadcrumb": [("Home", "/"), ("Contact", "")],
    "h1": "Get in touch with the {X}.",
    "h1Highlight": "Extreme Team",
    "intro": "Call or book online in a couple of clicks — a real person answers, and most visits happen the same day you reach out.",
    "heroChips": ["Same-Day in Most Cases", "24/7 Emergency Line", "Dayton &amp; Cincinnati"],
    # Addresses confirmed by the client 2026-08-01. The cards are headed by metro
    # ("Dayton" / "Cincinnati") because that is how people search, with the actual
    # suburb in the address line beneath. Directions links point at the address
    # itself rather than a name search, so they resolve to one pin every time.
    "locations": [
        {"city": "Dayton",
         # 65% pushes the crop down onto the sign so the 712 street number stays in
         # frame — it is the thing that makes this read as a location card.
         "photo": {"src": PHOTOS["beavercreek"], "pos": "50% 65%",
                   "alt": "Extreme service van at the Beavercreek office sign on North Fairfield Road"},
         "address": "712 N Fairfield Rd<br>Beavercreek, OH 45434",
         "directions": maps_dir("712 N Fairfield Rd, Beavercreek, OH 45434")},
        {"city": "Cincinnati",
         "photo": {"src": PHOTOS["mason"],
                   "alt": "The Extreme office building in the Cincinnati metro"},
         "address": "5633 Tylersville Rd<br>Mason, OH 45040",
         "directions": maps_dir("5633 Tylersville Rd, Mason, OH 45040")},
    ],
    # Hours confirmed by the client 2026-08-01. The earlier 24/7-vs-hours conflict is
    # resolved: 8-5 weekdays is when the OFFICE is staffed, and emergency service
    # really does run around the clock. The two rows are labelled so they can't be
    # read as competing — the site's 24/7 claims on 34 other pages all stand.
    #
    # Keep these two facts distinct if this table is ever edited. Collapsing them
    # into one "hours" figure is what produced the contradiction in the first place.
    "hours": [
        {"label": "Staffed office", "value": "Monday – Friday, 8:00 AM – 5:00 PM"},
        {"label": "Emergency service", "value": "24/7 — every day of the year", "em": True},
    ],
    "rail": {
        # PLACEHOLDER at the client's direction until dispatcher photos are shot —
        # this is a van shot standing in for an office/dispatch image. Swap it for
        # shot B3 (dispatcher at the desk) when the session delivers.
        "photo": PHOTOS["vans"],
        "photoAlt": "Extreme service vans heading out on calls",
        "promos": ["contactCall", "contactXplan"],
    },
}

def contact_page(d, root_class):
    left = [
        book_cards(d),
        location_cards(d),
        hours_table(d),
        T.mobile_inline_rail(d),
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

def check_cards(eyebrow, h2, cards):
    inner = "".join(
        f'''<div class="xco-ccard"><span class="c">✓</span>
  <div class="t">{c["t"]}</div><div class="d">{c["d"]}</div></div>''' for c in cards)
    return section(eyebrow, h2, f'<div class="xco-2col">{inner}</div>')

def checks_only(eyebrow, h2, items):
    inner = "".join(f'<div class="xsp-check"><span class="c">✓</span>{i}</div>' for i in items)
    return section(eyebrow, h2, f'<div class="xsp-checks">{inner}</div>')

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
    "h1": "A new system now. {X} that fit.",
    "h1Highlight": "Payments",
    "intro": "Don't put off a failing furnace or AC because of one big bill. Flexible monthly payment plans through our lenders — GoodLeap, Synchrony, and Wright-Patt Credit Union — make the right fix affordable.",
    # "$0 Down Options" and the "$0 down" stat below state a downpayment amount.
    # Under Reg Z (12 CFR 1026.24(d)) that is a "triggering term" for closed-end
    # credit — an ad that states it must also disclose the terms of repayment and
    # the APR. Since Extreme is not permitted to advertise rates, those two claims
    # may need rewording to something non-triggering ("financing available",
    # "low monthly payments"). Flagged for the client and their lender 2026-08-01;
    # NOT changed unilaterally, because it is approved marketing copy.
    "heroChips": ["Apply in Minutes", "$0 Down Options", "Options for Most Credit"],
    "why": [
        {"t": "One bill becomes a monthly payment",
         "d": "Spread the cost of a new system over time instead of paying it all at once."},
        {"t": "Don't downgrade the fix",
         "d": "Choose the system that's right for your home — not just the one that fits this month's budget."},
        {"t": "Keep your emergency fund intact",
         "d": "Breakdowns never pick a convenient month. Financing keeps your cushion where it belongs."},
        {"t": "Stacks with specials &amp; rebates",
         "d": "Combine financing with seasonal offers and utility rebates for the best total price."},
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
        "h2": "Three steps to yes.",
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
            {"n": "$0 down", "cap": "options available on qualifying plans."},
            {"n": "No penalty", "cap": "for paying your plan off early."},
        ],
        "lenders": ["GoodLeap", "Synchrony", "Wright-Patt Credit Union"],
        # Sits directly under the Apply button, which is where a customer decides.
        # Says the one thing that most often gets misunderstood — that applying is
        # a pre-approval, not a commitment — and links the full financing terms.
        "fine": ('Financing subject to credit approval. Applying is a request for pre-approval, '
                 'not an agreement to buy or to lend — rates and terms are set by the lender. '
                 'See <a href="/terms#financing">financing terms</a>.'),
    },
    "faqEyebrow": "FINANCING QUESTIONS",
    # First Q&A is verbatim from mockup 4c; the other three answers are authored
    # from approved claims (soft pull, no early-payoff penalty, stacks with
    # specials, plural lenders) — marketing to review in staging.
    "faq": [
        {"q": "Does applying affect my credit score?",
         "a": "Checking your options starts with a soft inquiry that doesn't affect your score. A full application follows only if you decide to move forward."},
        {"q": "What if my credit isn't perfect?",
         "a": "That's why we work with more than one lender. GoodLeap, Synchrony, and Wright-Patt Credit Union each cover a range of credit situations — and checking your options costs nothing."},
        {"q": "Can I pay it off early?",
         "a": "Yes — there's no penalty for paying your plan off early."},
        {"q": "Can I combine financing with specials?",
         "a": "Yes — financing stacks with seasonal specials and utility rebates for the best total price on the work."},
    ],
    "rail": {
        # The cropped file — the uncropped original frames a competitor's service
        # sticker, phone number and all. Do not swap this back.
        "photo": T.PHOTOS["ruudInstall"],
        "photoAlt": "Ruud air handler installed in a Dayton-area home",
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
        check_cards("WHY FINANCE", "The right fix, without draining savings.", d["why"]),
        checks_only("WHAT QUALIFIES", "Finance more than just new systems.", d["qualifies"]),
        T.process(d["process"], eyebrow="HOW IT WORKS"),
        lenders_panel(d["lenders"]),
        # with_photo: the rail is hidden under 810px, so this is the only place the
        # install photo appears on mobile.
        T.mobile_inline_rail(d, with_photo=True),
        T.faq(d["faq"], d["faqEyebrow"], h2=None),
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
    {"pill": "REFERRALS", "value": "$250 off", "title": "When a Friend Refers You",
     "desc": "New customers save $250 on a new heating, cooling, or plumbing system, or $100 on everything else. Just name whoever sent you when you book.",
     "foot": "Always available", "cta": "/referral", "ctaLabel": "See Extreme Rewards"},
    {"pill": "PLUMBING", "value": "$99", "title": "Drain Clearing Special",
     "desc": "Single accessible drain cleared, with a camera check if the clog keeps coming back.",
     "foot": "Limited time", "cta": "schedule"},
    {"pill": "NEW SYSTEMS", "value": "Free", "title": "Second Opinion on Replacement",
     "desc": "Told you need a whole new system? Get a no-pressure second look before you commit.",
     "foot": "Limited time", "cta": "schedule"},
    {"pill": "MEMBERSHIP", "value": "$249", "valueSuffix": "/yr", "title": "Join X-Plan Maintenance",
     "desc": "Two tune-ups a year, 15% off repairs, priority scheduling, and discounted service calls.",
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
    "h1": "Seasonal specials, {X}.",
    "h1Highlight": "extreme savings",
    "intro": "Real offers on the work you actually need — no gimmicks, no fine-print traps. Mention the offer when you book and we apply it to your invoice.",
    "heroChips": ["Updated Seasonally", "Mention at Booking", "Combine with Financing"],
    "redeem": {
        "h2": "Three steps, zero coupons to print.",
        "steps": [
            {"title": "Pick your offer",
             "desc": "One offer per visit — choose the one that saves you the most."},
            {"title": "Mention it when you book",
             "desc": "Tell us on the phone or note it in the online scheduler — we attach it to your appointment."},
            {"title": "Savings applied on your invoice",
             "desc": "The discount shows up in your upfront quote — before any work begins."},
        ],
    },
    "fineNote": "Offers can't be combined with other discounts unless noted. One offer per household per visit. Must be mentioned at time of booking. Expiration dates and full terms set per promotion.",
}

def specials_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
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
    body = f'''{specials_hero(d)}
<div class="xco-body">
  {section("CURRENT OFFERS", "This season's deals.", coupons)}
  <div class="xco-split">
    <div>{redeem}</div>
    <div style="display:flex;flex-direction:column;gap:16px">{right}</div>
  </div>
</div>'''
    return shell(root_class, body)

# ================================================================
# /about — mockup 4a (full-width tier), copy verbatim
# ================================================================
ABOUT = {
    "breadcrumb": [("Home", "/"), ("About Us", "")],
    "h1": "Locally owned. {X} committed.",
    "h1Highlight": "Extremely",
    "intro": "The Extreme Team is a family-owned heating, cooling, and plumbing company serving Dayton and Cincinnati — built on honest pricing, clean workmanship, and neighbors referring neighbors.",
    "heroChips": ["Family Owned &amp; Operated", "20+ Years Local", "4.9 on Google"],
    # PLACEHOLDERS until Block B of the shot list is shot. Both are real Extreme
    # photography, but neither is what its slot ultimately wants:
    #  - hero wants a team lineup; this is the branded vehicle at a community event
    #  - the story slot wants founders / the first van; this is a current van
    # The story copy says "From one van to the whole Miami Valley" — do NOT let the
    # alt text or any caption imply this photo is that first van.
    "heroPhoto": {"src": PHOTOS["troy"], "pos": "50% 45%",
                  "alt": "The Extreme Team at a community event in Troy, Ohio"},
    "storyPhoto": {"src": PHOTOS["skyline"],
                   "alt": "An Extreme service van with the Dayton skyline behind it"},
    "story": {
        "h2": "From one van to the whole Miami Valley.",
        # TODO: founding-story specifics — "20+ years" is approved; add the real
        # founding year only if the client confirms it (handoff 4a).
        "p1": "Extreme Heating, Air, Plumbing started the way most good service companies do — one van, one toolbox, and a promise to show up when we said we would. Two decades later we cover Dayton and Cincinnati with a full team of licensed HVAC and plumbing pros.",
        "p2": "The size changed. The promise didn't: upfront pricing before any work begins, techs who treat your home like their own, and a real person answering the phone — day or night.",
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
        {"n": "20+", "cap": "years serving Ohio homes"},
        {"n": '<span class="st">★</span> 4.9', "cap": "average Google rating"},
        {"n": "90%", "cap": "of calls handled same-day"},
        {"n": "24/7", "cap": "emergency service line"},
    ],
    # TODO: replace placeholder team names/roles with real staff + headshots (handoff 4a)
    # Real team, photos client-supplied 2026-08-01. Each was cropped to a
    # head-and-shoulders portrait at matching framing — the row runs four across and
    # mismatched crops are the first thing you notice.
    # TODO (client): confirm roles and years with the team for each person.
    "team": [
        {"name": "Anthony Griffin", "role": "Installer", "photo": PHOTOS["team"]["anthony-griffin"]},
        {"name": "Jayvon Kilgore",  "role": "Installer", "photo": PHOTOS["team"]["jayvon-kilgore"]},
        {"name": "Joe Richardson",  "role": "Comfort Advisor", "photo": PHOTOS["team"]["joe-richardson"]},
        {"name": "Tyler Hardy",     "role": "Installer", "photo": PHOTOS["team"]["tyler-hardy"]},
    ],
    # TODO: confirm /locations vs per-city location page URLs (handoff URL map)
    "areas": [
        {"t": "Dayton",
         "d": "Serving Dayton, Kettering, Beavercreek, Centerville, Springboro, and surrounding Miami Valley communities.",
         "lm": "Dayton location &amp; service area →", "href": "/locations"},
        {"t": "Cincinnati",
         "d": "Serving Cincinnati, Mason, West Chester, Loveland, Fairfield, and communities across the metro.",
         "lm": "Cincinnati location &amp; service area →", "href": "/locations"},
    ],
}

def about_hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid xco-hero-grid-400">
    <div>
      {T.crumbs(d["breadcrumb"])}
      {T.h1(d["h1"], d["h1Highlight"])}
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
    values = "".join(
        f'''<div class="xco-ccard"><span class="xsp-glyph"><i></i><i></i></span>
  <div class="t">{v["t"]}</div><div class="d">{v["d"]}</div></div>''' for v in d["values"])
    values = section("WHAT WE STAND FOR", "Four things we never compromise on.",
                     f'<div class="xco-vals">{values}</div>')
    stats = "".join(
        f'<div><div class="n">{s["n"]}</div><div class="cap">{s["cap"]}</div></div>' for s in d["stats"])
    stats = f'''<div class="xco-stats">
  <img class="mark" src="{T.X_MARK}" alt="" style="position:absolute;right:-70px;bottom:-60px;width:300px;opacity:.06;transform:rotate(-8deg);filter:brightness(0) invert(1)">
  <div class="grid">{stats}</div>
</div>'''
    team = "".join(
        f'''<div>{slot_img("xco-slot slot", {"src": m["photo"], "alt": m["name"]} if m.get("photo") else None, "TECH HEADSHOT")}
  <div class="name">{m["name"]}</div><div class="role">{m["role"]}</div></div>''' for m in d["team"])
    team = section("MEET THE TEAM", "The faces at your door.", f'<div class="xco-team">{team}</div>')
    areas = "".join(
        f'''<a class="xsp-card" href="{a["href"]}">
  <span class="txt"><span class="t">{a["t"]}</span><br><span class="d">{a["d"]}</span></span>
  <span class="lm">{a["lm"]}</span><span class="mrow">→</span>
</a>''' for a in d["areas"])
    areas = section("WHERE WE WORK", "Two home bases, one Extreme Team.",
                    f'<div class="xco-2col">{areas}</div>')
    body = f'''{about_hero(d)}
<div class="xco-body">
  {story}
  {values}
  {stats}
  {team}
  {areas}
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
