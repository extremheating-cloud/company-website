from layout import components as T

TEL, PH = T.PHONE_TEL, T.PHONE_DISPLAY

def call(text):
    return text.replace("{tel}", f'<a href="{TEL}">{PH}</a>')

STEP1 = {"title": "Book in minutes", "desc": "Call or schedule online — we confirm your arrival window fast, with same-day service in most cases."}
STEP2 = {"title": "Diagnose & quote upfront", "desc": "We walk you through what's wrong and your options — flat, upfront pricing you approve first."}

def steps(last_title, last_desc, step1=None, step2=None):
    return {"steps": [step1 or STEP1, step2 or STEP2, {"title": last_title, "desc": last_desc}]}

def detail(slug, crumb_parent, name, h1, hl, intro, chips, book_eyebrow, book_title,
           sym_eyebrow, sym_h2, symptoms, callout, wwd_h2, cards, process_,
           faq_eyebrow, faqs, related, img=None, pills=None, promos=None, safety=False):
    d = {
        "breadcrumb": [crumb_parent, (name, "")],
        "h1": h1, "h1Highlight": hl, "intro": intro, "heroChips": chips,
        "bookingCard": {"eyebrow": book_eyebrow, "title": book_title,
                        "sub": "Upfront pricing before any work begins."},
        "symptoms": {"eyebrow": sym_eyebrow, "h2": sym_h2, "items": symptoms,
                     "callout": call(callout), "safety": safety},
        "whatWeDo": {"h2": wwd_h2, "cards": cards} if cards else None,
        "process": process_, "faqEyebrow": faq_eyebrow, "faq": faqs,
        "rail": {"photo": img, "photoSlot": True, "photoLabel": "PHOTO — TECH ON THE JOB",
                 "promos": promos or ["financing", "xplan"]},
        "related": related,
    }
    if pills:
        d["pillNav"] = pills
    if not cards:
        d.pop("whatWeDo")
    return d

def sub(crumbs, h1, hl, intro, pills, sym_eyebrow, sym_h2, symptoms, callout,
        process_, decision, faq_eyebrow, faqs, book_eyebrow, book_title, book_sub,
        sib_label, sibs, img=None, alt=None, imgPos=None, safety=False,
        schedule_label="Schedule Service", promo="xplanSub", trust2="20+ years local"):
    return {
        "breadcrumb": crumbs, "h1": h1, "h1Highlight": hl, "intro": intro,
        "scheduleLabel": schedule_label,
        "pillNav": pills,
        "symptoms": {"eyebrow": sym_eyebrow, "h2": sym_h2, "items": symptoms,
                     "callout": call(callout), "safety": safety},
        "process": process_, "decision": decision,
        "faqEyebrow": faq_eyebrow, "faq": faqs,
        "bookingCard": {"eyebrow": book_eyebrow, "title": book_title, "sub": book_sub, "trust2": trust2},
        "rail": {"promos": [promo], "photo": img, "photoAlt": alt, "photoPos": imgPos},
        "siblings": {"label": sib_label, "items": sibs},
    }

def pillset(label, items, active):
    return {"label": label, "items": [
        {"label": l, "href": h, "active": l == active} for l, h in items]}

SPEED_FAQ = {"q": "How fast can you get here?",
    "a": "In most cases, same day — about 90% of our calls are handled the day you reach out, with 24/7 emergency service when it can't wait."}


# ======================================================================
# GEO content layer
# ----------------------------------------------------------------------
# Everything below rewrites the page data built above: answer-first blocks,
# real H2/H3 body sections, decision tables, per-page FAQ headings and the
# visible last-updated line. It is applied as a second pass rather than
# threaded through detail()/sub()/plumb_sub() so the constructors above keep
# their positional signatures and a copy change stays a one-key edit.
#
# Rules held throughout, from the client decisions of 2026-08-02:
#   · No radon claims anywhere. The company does not do radon mitigation, so
#     the radon H2, the radon table row and the radon FAQ from the research
#     deliverables are dropped rather than softened.
#   · No rebate or utility trade-ally claims.
#   · Service-call and dispatch fees never appear in an h1, h2 or hero. They
#     are not used below at all.
#   · The repair-quote-approaching-a-third-of-replacement rule of thumb is
#     approved and is used in the decision tables.
#   · No team copy, no technician names, no author attribution. E-E-A-T leans
#     on the company, its two Ohio licences and its history.
#   · X-Plan accrual always carries BOTH conditions in one sentence:
#     consecutive years AND capped at $2,500 or 10 years.
# ======================================================================

UPDATED, UPDATED_ISO = "August 2, 2026", "2026-08-02"

# The hero chip used to read "4.9 on Google". The 1,595-review figure is a
# Birdeye aggregate pooling several platforms, so naming Google is a claim a
# competitor can disprove in a minute. The rating source comes off the chip
# and the count goes on.
REVIEW_CHIP = "4.9 from 1,595 reviews"


def sec(h2, body, h3s=None, table=None, sid=None, eyebrow=None):
    """One body section: an H2 question, its direct answer, optional H3
    sub-questions, optional table rendered inside the section."""
    s = {"h2": h2, "body": body}
    if h3s:
        s["h3s"] = [{"h3": h, "body": b} for h, b in h3s]
    if table:
        s["table"] = table
    if sid:
        s["id"] = sid
    if eyebrow:
        s["eyebrow"] = eyebrow
    return s


def tbl(caption, takeaway, columns, rows, h2=None, sid=None, eyebrow=None):
    t = {"caption": caption, "takeaway": takeaway, "columns": columns, "rows": rows}
    if h2:
        t["h2"] = h2
    if sid:
        t["id"] = sid
    if eyebrow:
        t["eyebrow"] = eyebrow
    return t


def qa(*pairs):
    return [{"q": q, "a": a} for q, a in pairs]


def geo(store, key, callout=None, **fields):
    """Apply the rewrite to one page. `callout` reaches into symptoms so a
    page can hand off to a sibling from its callout without restating it."""
    d = store[key]
    d.update(fields)
    if callout is not None:
        d["symptoms"]["callout"] = call(callout)
    if d.get("heroChips"):
        d["heroChips"] = [REVIEW_CHIP if c == "4.9 on Google" else c
                          for c in d["heroChips"]]
    d.setdefault("updated", UPDATED)
    d.setdefault("updatedISO", UPDATED_ISO)
    return d


# ---------------------------------------------------------------- shared rows
# The third-of-replacement-cost row is the same judgement on every
# repair-or-replace table, so it is written once. The age row never is: the
# threshold differs by equipment type and that difference is the point.
COST_ROW = ("Repair cost", "The quote is well under a third of replacement cost",
            "The quote is at or above roughly a third of replacement cost")
