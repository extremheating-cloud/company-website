from layout import components as T
from data import business as D

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


# Copy rules: no radon/rebate/trade-ally claims, no fees in h1/h2/hero, X-Plan accrual states both conditions.

UPDATED, UPDATED_ISO = "August 2, 2026", "2026-08-02"

# Birdeye aggregate across platforms, not Google-only: don't name Google.
REVIEW_CHIP = f"{D.GOOGLE_RATING} from {D.REVIEW_COUNT} reviews"


def sec(h2, body, h3s=None, table=None, sid=None, eyebrow=None):
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


COST_ROW = ("Repair cost", "The quote is well under a third of replacement cost",
            "The quote is at or above roughly a third of replacement cost")
