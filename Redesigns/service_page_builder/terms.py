"""Terms of Service & Limited Warranty — /terms.

Two jobs:

1. Carry forward the EXISTING published terms verbatim. The body text below was
   extracted from the live https://www.extremeheating.com/terms on 2026-07-31 and
   is reproduced word for word — payment, scope, limited warranty, water-related
   exclusions, concealed conditions, customer-supplied parts, performance, access,
   permits, disclaimer, liability, delays, lien rights, indemnification, acceptance.

2. Add the two program sections the site was missing. The Extreme Rewards terms
   line printed on the brochure points here, and until now this page carried no
   referral terms at all.

Sourcing: program facts come from ~/.claude/skills/extreme-brand/references/programs.md.
A terms page is where eligibility and payout rules belong, so the rules from that
file's internal section that BIND a customer are published here (naming at booking,
24-month lookback, validity, one reward per job, exclusions, greater-of stacking).
Deliberately NOT published, because they are commercial rather than binding:
the spend backstop thresholds, the internal job-type table, gift-card activation
cost, batching cadence, and cost per acquisition.

Nothing here is invented. Clauses a terms page would normally carry that are not in
the source file are listed in TERMS_GAPS for the client and their attorney.
"""
import os
import template as T
import company_pages as CP

TERMS_CSS = """
/* ------------------------------- /terms ------------------------------- */
.xsp-terms .xsp-h1,.xsp-terms .xsp-h2,.xsp-terms .xtm-h3{font-weight:800}
.xsp-terms .xsp-eyebrow{color:#3F852B}
.xsp-terms .xsp-crumbs .cur{color:var(--green-hover)}
.xsp-terms .xsp-crumbs a{display:inline-block;padding:15px 6px;margin:-15px -6px}
.xsp-terms :focus-visible{outline:3px solid #61BC47;outline-offset:2px}

.xtm-updated{margin-top:16px;font-size:12.5px;font-weight:700;color:rgba(255,255,255,.75)}
.xtm-lead{max-width:820px}
.xtm-lead p{font-size:15px;line-height:1.7;font-weight:500;color:var(--body);margin-top:14px}

/* summary card */
.xtm-summary{background:var(--tint);border-radius:16px;padding:26px 30px;margin-top:24px}
.xtm-summary .k{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--purple)}
.xtm-summary h2{margin-top:8px;font-style:italic;font-weight:800;font-size:26px;
letter-spacing:-.4px;color:var(--purple)}
.xtm-summary p{margin-top:12px;font-size:14.5px;line-height:1.65;font-weight:500;color:var(--ink);
max-width:760px}
.xtm-summary ul{list-style:none;padding:0;margin:16px 0 0;display:flex;flex-direction:column;gap:9px}
.xtm-summary li{display:flex;gap:10px;font-size:14px;line-height:1.6;font-weight:500;color:var(--ink)}
.xtm-summary li .b{width:7px;height:7px;border-radius:50%;background:var(--green);flex:none;margin-top:8px}
.xtm-note{margin-top:16px;background:#fff;border-radius:12px;padding:14px 16px;font-size:13px;
line-height:1.65;font-weight:500;color:var(--body)}
.xtm-note b{color:var(--ink);font-weight:800}

/* contact strip */
.xtm-contact{border:1px solid var(--rule);border-radius:16px;padding:20px 24px;margin-top:20px;
display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;background:#fff}
.xtm-contact .t{font-weight:800;font-size:16.5px}
.xtm-contact .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}

/* legal sections */
.xtm-sec{margin-top:34px;scroll-margin-top:var(--xsp-anchor-offset)}
.xtm-h3{font-size:19px;letter-spacing:-.2px;color:var(--ink);
padding-bottom:10px;border-bottom:2px solid var(--green)}
.xtm-sec p{margin-top:12px;font-size:14.5px;line-height:1.75;font-weight:500;color:var(--body);
max-width:78ch}
.xtm-sec p b{color:var(--ink);font-weight:800}
.xtm-sec ul{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-direction:column;gap:8px}
.xtm-sec li{display:flex;gap:10px;font-size:14.5px;line-height:1.7;font-weight:500;color:var(--body);
max-width:78ch}
.xtm-sec li .b{width:6px;height:6px;border-radius:50%;background:var(--green);flex:none;margin-top:9px}
.xtm-sec li b{color:var(--ink);font-weight:800}

/* the two program blocks get a tinted rail so they read as additions */
.xtm-prog{border-left:4px solid var(--green);padding-left:22px}

/* jump nav */
.xtm-toc{border:1px solid var(--rule);border-radius:16px;padding:20px 24px;margin-top:24px;background:#fff}
/* --muted (#94A3B8) is only 2.56:1 on white and fails AA as a label; --body clears it. */
.xtm-toc .k{font-size:10.5px;font-weight:800;letter-spacing:1.8px;color:var(--body)}
.xtm-toc ol{margin:12px 0 0;padding-left:20px;columns:2;column-gap:32px}
.xtm-toc li{font-size:13.5px;line-height:1.9;font-weight:600}
.xtm-toc a{color:var(--purple);text-decoration:none}
.xtm-toc a:hover{color:var(--green-dark);text-decoration:underline}

@media (max-width:809px){
.xtm-summary{padding:22px 20px}
.xtm-summary h2{font-size:21px}
.xtm-sec{margin-top:28px}
.xtm-h3{font-size:17.5px}
.xtm-prog{padding-left:16px;border-left-width:4px}
.xtm-toc ol{columns:1}
.xtm-contact{padding:18px 20px}
}
"""


def shell(root_class, body):
    return f'''<section class="xhac-svc {root_class}">
  <style>{T.CSS}{CP.COMPANY_CSS}{TERMS_CSS}</style>
{body}
{T.script("xhac-svc")}
</section>
'''


# ---------------------------------------------------------------------------
# EXISTING published terms — reproduced verbatim from the live /terms page.
# Do not reword. Legal entity is "Extreme Heating & Cooling LLC" as published.
# ---------------------------------------------------------------------------
# Two separate legal entities under common ownership (client-confirmed 2026-07-31):
#   Extreme Heating & Cooling LLC  — the HVAC company
#   Extreme Home Services LLC      — the plumbing company
# Registered form of the HVAC entity confirmed by the client 2026-07-31 as LLC, matching
# the previously published page. "LTD" appeared in earlier drafts and is not correct.
# Every mention on this page derives from this constant — change it here, not inline.
ENTITY = "Extreme Heating &amp; Cooling LLC"
ENTITY_PLUMBING = "Extreme Home Services LLC"
ENTITY_SCOPE = f"{ENTITY} and {ENTITY_PLUMBING}"

# Effective date of this version of the Terms.
EFFECTIVE = "August 1, 2026"

EXISTING_SECTIONS = [
    ("payment-terms", "Payment Terms", [
        "Payment for the work described is due immediately upon completion unless otherwise specified in writing. A deposit may be required to schedule work. Any unpaid balance will be subject to a late charge of 10% per month, or the maximum amount permitted by law, plus all costs of collection, including reasonable attorney fees and court costs, as permitted by law.",
    ]),
    ("scope-of-work", "Scope of Work / Change Orders", [
        "Only the work specifically listed on the estimate or invoice is included. Additional work requested by Customer or required due to unforeseen or concealed conditions must be approved in writing and may result in additional charges.",
    ]),
    ("limited-warranty", "Limited Warranty", [
        "Extreme warrants its materials and workmanship to be free from defects for one (1) year after performance, unless otherwise specified in writing. This warranty does not cover faults caused by misuse, negligence, improper maintenance, unauthorized alterations or repairs, abnormal operating conditions, power surges, or acts of God. Manufacturer warranties, if any, apply to equipment and parts and supersede Extreme's warranty where applicable.",
    ]),
    ("no-warranty-items", "No Warranty Items / Water-Related HVAC Issues", [
        "Unless otherwise stated in writing, Extreme does not warranty drain cleaning, snake, or roto services. Extreme is not responsible for HVAC drain clogs, condensate line backups, water leaks, or any water-related damage or conditions arising from HVAC equipment, drainage, or condensate issues, including damage to drywall, flooring, ceilings, fixtures, furniture, or personal property. Extreme does not warrant cracked, separated, collapsed, or otherwise damaged and unusable piping or drains.",
    ]),
    ("concealed-conditions", "Existing / Concealed Conditions", [
        "Customer acknowledges that existing or concealed conditions may be discovered during service or installation, including but not limited to damaged ductwork, corrosion, mold, asbestos, code violations, unsafe venting, drainage issues, or prior improper installation. Extreme is not responsible for pre-existing or concealed conditions and is not liable for resulting damage or additional costs.",
    ]),
    ("customer-supplied", "Customer-Supplied Parts / Equipment", [
        "Extreme provides no warranty and assumes no liability for customer-supplied parts, equipment, thermostats, filters, or accessories, including compatibility, performance, or damage arising from their use.",
    ]),
    ("no-performance-guarantee", "No Performance Guarantee", [
        "Extreme does not guarantee temperatures, utility savings, air quality results, or overall system performance where conditions outside Extreme's control exist, including duct design or condition, insulation, building envelope issues, equipment sizing selected by others, customer settings, or customer maintenance.",
    ]),
    ("property-access", "Property Access / Cosmetic Items", [
        "Customer grants permission to access the property, including attics, crawl spaces, and mechanical areas, and acknowledges that minor cosmetic impacts may occur when accessing equipment or routing lines, including drywall, paint, trim, landscaping, and surfaces. Unless specifically included in writing, patching, painting, and finish work are not included.",
    ]),
    ("permits", "Permits / Inspections", [
        "Where permits or inspections are required, Customer is responsible for associated fees unless otherwise stated in writing. Extreme is not responsible for delays or additional costs caused by inspection scheduling or corrections required due to pre-existing conditions or work performed by others.",
    ]),
    ("exclusive-warranty", "Exclusive Warranty / Disclaimer of Other Warranties", [
        "This Limited Warranty is the only warranty provided by Extreme and is in lieu of all other warranties, express or implied, including implied warranties of merchantability or fitness for a particular purpose.",
    ]),
    ("limitation-of-liability", "Limitation of Liability", [
        "Extreme is not responsible for reimbursement for work performed by others. Extreme is not liable for lost profits or any incidental, special, exemplary, indirect, or consequential damages arising from any work performed or any problem, whether or not covered by warranty. Extreme's total liability is limited to and shall not exceed the amount paid under the applicable estimate or invoice.",
    ]),
    ("delays", "Delays / Third Parties", [
        "Extreme is not responsible for delays caused by unforeseen issues, including weather-related events, pandemic, supply delays, or third-party delays, and is not liable for expenses incurred due to scheduling or completing inspections with municipalities and/or county building or utility departments.",
    ]),
    # The only clause where the published text was altered rather than reproduced. It named
    # the HVAC entity alone, which left plumbing work sold by Extreme Home Services LLC
    # outside it. Changed at the client's instruction 2026-07-31: names both companies, and
    # ties each one's lien to the work it furnished rather than letting either lien for the
    # other's. Everything else in the clause is the original wording.
    ("lien-rights", "Lien Rights", [
        f"Customer acknowledges that each of {ENTITY} and {ENTITY_PLUMBING} may have the right to file a mechanic's lien or other lien claim against the property for unpaid labor, services, and materials it furnished, as permitted by Ohio law. Customer agrees to pay all amounts due in accordance with these Terms to avoid lien filing, and to pay reasonable costs of collection, including attorney fees and court costs, as permitted by law.",
    ]),
    ("indemnification", "Indemnification", [
        "Customer agrees to indemnify Extreme from any claims, judgments, damages, fees, costs, expenses, losses, or liabilities arising from or directly related to Customer's violation of these Terms, including collection costs and reasonable attorney fees.",
    ]),
]

# ---------------------------------------------------------------------------
# NEW — Extreme Rewards. Facts from programs.md. Amounts and the customer-facing
# job wording ("a new heating, cooling, or plumbing system" / "any repair or
# installation") are the approved language; the internal job-type table and the
# spend backstop are deliberately absent.
# ---------------------------------------------------------------------------
REWARDS_SECTION = ("extreme-rewards", "Extreme Rewards Referral Program", [
    f"<b>Who offers the program.</b> Extreme Rewards is offered and administered by {ENTITY}, including where the referred customer's job is performed by {ENTITY_PLUMBING}.",
    "<b>What the program pays.</b> Extreme Rewards pays an existing customer when a new customer they referred completes a qualifying job. The referred customer saves $250 on a new heating, cooling, or plumbing system, or $100 on everything else. The referring customer earns the same amount their referred customer saved, and Extreme issues it on a Visa gift card.",
    "<b>How a referral is credited.</b> The referred customer must name the referring customer at the time they book the job. Extreme cannot apply a referral to a job after it is booked and does not accept retroactive claims.",
    "<b>Who qualifies as a referred customer.</b> The referred customer must be new to Extreme, meaning Extreme has not performed service at that address within the previous 24 months.",
    "<b>How long a referral stays valid.</b> A referral name remains valid for 90 days from the date it is given.",
    "<b>When rewards are issued.</b> Extreme issues rewards on a Visa gift card after the referred customer's job is complete and paid in full, and within 90 days of that completion. Extreme does not pay on a lead, on a booking, or on an incomplete or unpaid job.",
    "<b>How many rewards can be earned.</b> Extreme issues one reward per completed job. Where a single visit includes more than one type of qualifying work, Extreme issues one reward at the higher applicable amount. There is no limit on the number of separate referrals a customer may make.",
    "<b>Exclusions.</b> Self-referrals and Extreme employees are not eligible. A property owner may not refer their own property.",
    "<b>Combining with other offers.</b> The referral discount does not combine with other active promotions; the referred customer receives the greater of the two. Accrued X-Plan credit is not a promotion and applies in addition to the referral discount.",
    "<b>Taxes.</b> Referral rewards may constitute taxable income to the recipient. Extreme may be required to collect tax information and to issue tax forms where reward totals meet applicable reporting thresholds. Recipients are responsible for any taxes owed.",
])

# ---------------------------------------------------------------------------
# NEW — X-Plan. Zero Risk Investment carries BOTH conditions (consecutive years,
# $2,500 or 10 years cap). Transferability is NOT claimed — the accrual follows
# the member, not the property.
# ---------------------------------------------------------------------------
XPLAN_SECTION = ("x-plan", "X-Plan Membership", [
    f"<b>Who offers the membership.</b> X-Plan is offered and administered by {ENTITY}, including member benefits that apply to work performed by {ENTITY_PLUMBING}.",
    "<b>Pricing.</b> X-Plan costs $249 per year or $20.75 per month.",
    "<b>Zero Risk Investment.</b> 100% of the investment of an X-Plan membership in consecutive years is applied toward end-of-life equipment replacement, up to a maximum of $2,500 or 10 years, whichever comes first. A lapse in membership interrupts the accrual. <b>The accrual follows the member, not the property, and does not transfer with the sale of a home.</b>",
    "<b>Included services.</b> Membership includes two Safety &amp; Performance Visits a year, a multi-point air conditioner tune-up and service, refrigerant charge calibration up to 1 lb, a heating system safety checkup and service, detailed evaluation and efficiency measurements, airflow adjustments as needed, thermostat calibration and configuration, and professional recommendations to prolong equipment life.",
    "<b>Member benefits.</b> Members also receive Extreme Priority Scheduling, 15% off all repairs, a reduced service fee including after-hours and holidays, a discount on the complete line of indoor air quality components including air duct cleaning, and access to exclusive member offers and discounts.",
    "<b>Repair warranty.</b> Qualified repairs performed by Extreme technicians carry a Worry-Free 5-Year Warranty. It applies only to those repairs and remains subject to the exclusions set out in the Limited Warranty and No Warranty Items sections above.",
])

# ---------------------------------------------------------------------------
# NEW — Financing (client instruction 2026-07-31). The load-bearing point the
# client asked for: submitting an application is a request for PRE-APPROVAL. It
# creates no agreement with Extreme and no credit agreement with the lender.
#
# Everything here is either (a) already published on /financing-options
# ("Financing subject to credit approval", the three named lenders), (b) the
# client's own instruction, or (c) a direct consequence of Extreme not being the
# lender. Nothing states a rate, a term length, an approval standard, or a
# lender's internal process — Extreme does not control any of those and must not
# appear to promise them. See TERMS_GAPS for what an attorney still has to add.
# ---------------------------------------------------------------------------
FINANCING_SECTION = ("financing", "Financing", [
    "<b>Extreme is not the lender.</b> Financing is offered by third-party lenders, including GoodLeap, Synchrony, and Wright-Patt Credit Union. Extreme does not extend credit, is not a party to any credit agreement between Customer and a lender, and does not act as the lender's agent.",
    "<b>Applying is a request for pre-approval.</b> Submitting a financing application through a link provided by Extreme is a request for pre-approval from that lender. It is not an agreement between Customer and Extreme, it is not an agreement by Extreme to perform any work or to hold any price, and it is not a credit agreement between Customer and Wright-Patt Credit Union or any other lender. Pre-approval does not obligate Customer to proceed with any work or to accept any offer of credit.",
    "<b>When financing actually exists.</b> Financing exists only if the lender approves Customer's application and Customer enters into the lender's own loan or credit agreement. All financing is subject to credit approval.",
    "<b>The lender sets the terms.</b> Credit decisions, amounts, rates, fees, payment schedules, and account terms are determined by the lender and are governed by the agreement between Customer and that lender. Extreme does not set, control, or guarantee approval or any particular terms, and any figures Extreme provides for illustration are estimates only.",
    "<b>Applications are submitted to the lender.</b> A financing application link provided by Extreme opens the lender's own website. Information Customer submits there is collected and used by the lender under the lender's terms and privacy policy, not Extreme's.",
    "<b>Extreme's Terms still govern the work.</b> These Terms, together with the applicable estimate or invoice, govern the work Extreme performs regardless of how Customer chooses to pay for it. Disputes about a credit application, a credit decision, or the servicing of a financed account are between Customer and the lender.",
])

ACCEPTANCE_SECTION = ("acceptance", "Acceptance of Terms", [
    "By signing an estimate or invoice, authorizing work, scheduling service, or making payment, Customer confirms acceptance of these Terms of Service and Limited Warranty.",
])

# Clauses a terms page would normally carry that are NOT in programs.md or on the
# existing published page. Not written, because inventing a term is worse than a
# gap. Surfaced to the client in the build report.
TERMS_GAPS = [
    "Right to modify, suspend, or end Extreme Rewards or X-Plan, and what happens to referrals or memberships already in flight.",
    "X-Plan cancellation, refund, auto-renewal and what happens to accrued Zero Risk Investment credit on cancellation or lapse.",
    "Whether X-Plan pricing is per system or per household, and how additional systems are priced.",
    "Visa gift card issuer terms, expiry, and replacement of lost cards.",
    "Governing law and dispute resolution for the programs (the existing page references Ohio law only for lien rights).",
    # Raised by the Financing section added 2026-07-31.
    "Financing: whether a quote or price is held while a financing application is pending, and for how long. The section says applying does not hold a price, which is the safe default — confirm it matches how sales actually operates.",
    "Financing: what happens to Extreme's payment terms if a customer is declined after work is scheduled or started. Payment Terms currently says payment is due on completion with no financing contingency.",
    "Financing: whether Extreme receives compensation from any lender, which may carry disclosure obligations.",
    "Financing: confirm Extreme's agreements with GoodLeap, Synchrony, and Wright-Patt Credit Union permit naming them on the website and in these Terms, and require no specific lender-mandated disclosure language.",
    # Raised by the two-entity structure confirmed 2026-07-31. The registered form of
    # the HVAC entity was the blocking item here and is now closed: the client
    # confirmed LLC on 2026-07-31, matching the previously published page.
    "Whether the umbrella corporation should be named in these Terms at all.",
    "Lien Rights was amended 2026-07-31 to name both LLCs, each for the work it furnished. This is the one place the previously published legal text was changed, so it should get an attorney read before the effective date.",
]


def sec(anchor, title, paras, prog=False):
    body = "".join(f"<p>{p}</p>" for p in paras)
    cls = "xtm-sec xtm-prog" if prog else "xtm-sec"
    return f'''<div class="{cls}" id="{anchor}">
  <h3 class="xtm-h3">{title}</h3>
  {body}
</div>'''


def hero():
    return f'''<div class="xsp-hero sub">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs([("Home", "/"), ("Terms", "")])}
      <div class="xsp-eyebrow" style="color:#8FD481;margin-top:14px">POLICIES &amp; COVERAGE</div>
      <h1 class="xsp-h1">Terms of Service &amp; Limited Warranty</h1>
      <p class="xsp-intro">These Terms apply to all estimates, invoices, and work performed by
      {ENTITY_SCOPE}. In these Terms, "Extreme" refers to both. By signing an estimate or
      invoice, authorizing work, scheduling service, or making payment, Customer acknowledges
      and agrees to these Terms.</p>
      <div class="xtm-updated">Effective {EFFECTIVE}</div>
    </div>
  </div>
</div>'''


def summary():
    bullets = [
        "Payment is due upon completion unless otherwise stated in writing.",
        "Additional work outside the listed scope requires written approval.",
        "Standard workmanship and material warranty is one year unless otherwise stated in writing.",
        "Manufacturer warranties may apply separately to parts and equipment.",
        "Extreme's liability is limited to the amount paid under the applicable estimate or invoice.",
        "Referral rewards require the referring customer to be named when the job is booked.",
        "Applying for financing is a request for pre-approval and does not create an agreement with Extreme or a lender.",
    ]
    lis = "".join(f'<li><span class="b"></span><span>{b}</span></li>' for b in bullets)
    return f'''<div class="xtm-summary">
  <div class="k">IMPORTANT INFORMATION</div>
  <h2>Please review these Terms carefully.</h2>
  <p>This page outlines payment expectations, warranty limits, property access, liability limits,
  and other conditions that apply to work performed by {ENTITY_SCOPE}. Heating and cooling work is
  performed by {ENTITY}; plumbing work is performed by {ENTITY_PLUMBING}. These Terms also set out
  the terms that govern the Extreme Rewards referral program and X-Plan membership.</p>
  <ul>{lis}</ul>
  <div class="xtm-note"><b>Note:</b> Drain cleaning, snake, and roto services are not warranted
  unless specifically stated in writing. Water-related HVAC issues and resulting property damage
  are also excluded as outlined below.</div>
</div>'''


def contact():
    return f'''<div class="xtm-contact">
  <div>
    <div class="t">Contact Our Team</div>
    <div class="d">Questions about these terms can be directed to our team before service is authorized.</div>
  </div>
  <a class="xsp-cta" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
</div>'''


def toc(sections):
    items = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _ in sections)
    return f'''<div class="xtm-toc">
  <div class="k">ON THIS PAGE</div>
  <ol>{items}</ol>
</div>'''


def terms_page(d, root_class):
    # The green left rule marks the sections added on top of the original published
    # terms — the two Extreme programs plus financing. Financing is not an Extreme
    # program; it shares the treatment because it is offering-specific rather than
    # part of the base work terms.
    programs = [REWARDS_SECTION, XPLAN_SECTION, FINANCING_SECTION]
    all_sections = EXISTING_SECTIONS + programs + [ACCEPTANCE_SECTION]
    prog_anchors = {a for a, _, _ in programs}
    body_secs = "".join(
        sec(a, t, p, prog=(a in prog_anchors)) for a, t, p in all_sections)
    body = f'''{hero()}
<div class="xco-body">
  <div class="xtm-lead">
    {summary()}
    {contact()}
    {toc(all_sections)}
  </div>
  <div>{body_secs}</div>
</div>'''
    return shell(root_class, body)


def pages(root):
    return [(os.path.join(root, "Other pages", "terms.html"),
             terms_page, {}, "xsp-terms")]
