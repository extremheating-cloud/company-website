import os
from layout import components as T
from data import business as D
from pages.company_shared import UPDATED, UPDATED_ISO, shell, section

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
# The page renders inside a Framer embed iframe. Left to itself, components.py's link
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
  {T.hero_mark()}
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
                    # The three advertised payments belong here, on the page someone
                    # opens specifically to find out whether they can afford this. The
                    # page previously said "the lender sets the rate" four times and
                    # never named a single figure, which is what the blind reader
                    # review's price shopper walked away from. No rate and no term
                    # appear, here or anywhere — see business.FINANCE_* on why.
                    lead=[f"Yes. An air conditioner starts "
                          f"{D.finance_line(D.FINANCE_AC, 'an AC')}, a heat pump "
                          f"{D.finance_line(D.FINANCE_HEAT_PUMP, 'a heat pump')}, and a "
                          f"furnace and air conditioner replaced together "
                          f"{D.finance_line(D.FINANCE_FULL_SYSTEM, 'a full system')}.",
                          "Those are the best-case advertised payments rather than a quote "
                          "for your house. Water heaters and the bigger repairs qualify too. "
                          "The money comes from the lender rather than from us, so approval, "
                          "rate and term are theirs to set."]),
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

def pages(root):
    return [(os.path.join(root, "pages", "company", "financing-options.html"), financing_page, FINANCING,
             "xsp-financing-options")]
