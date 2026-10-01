import os
import re
from layout import components as T
from pages import company_shared as CP
from data import business as D
from pages import terms as TM

PRIVACY_CSS = """
.xtm-h4{margin:26px 0 0;font-size:15.5px;font-weight:800;letter-spacing:-.1px;color:var(--ink)}
.xtm-eff{font-size:13px;font-weight:700;color:var(--muted)}
.xpv-draft{border:2px solid #B4342A;background:#FDF3F2;border-radius:16px;
padding:20px 24px;margin-top:24px}
.xpv-draft .k{font-size:11.5px;font-weight:800;letter-spacing:2px;color:#B4342A}
.xpv-draft p{margin-top:10px;font-size:14px;line-height:1.65;font-weight:600;color:var(--ink);
max-width:78ch}
.xpv-draft p + p{margin-top:8px}
@media (max-width:809px){.xpv-draft{padding:18px 20px}}
"""


def shell(root_class, body):
    return f'''<section class="xhac-svc {root_class}">
  <style>{T.CSS}{CP.COMPANY_CSS}{TM.TERMS_CSS}{PRIVACY_CSS}</style>
{body}
{T.script("xhac-svc")}
</section>
'''


ENTITY = TM.ENTITY
ENTITY_PLUMBING = TM.ENTITY_PLUMBING
ENTITY_SCOPE = TM.ENTITY_SCOPE

EFFECTIVE = "September 27, 2026"

PRIVACY_ADDRESS = D.OFFICE_PRIMARY["oneline"]

PRIVACY_EMAIL = D.EMAIL


_NEEDS_RE = re.compile(r"\[NEEDS:.*?\]", re.S)
_TAG_RE = re.compile(r"<[^>]+>")

_STRIPPED = []


def _clean(paras):
    # [NEEDS: ...] markers are stripped and HOLD:: paragraphs never render; both are logged to PRIVACY_GAPS.
    out = []
    for p in paras:
        if p.startswith("HOLD::"):
            _STRIPPED.append("HELD BACK, not rendered: " + _TAG_RE.sub("", p[6:]).strip())
            continue
        markers = _NEEDS_RE.findall(p)
        for m in markers:
            _STRIPPED.append(m.strip("[]").strip())
        cleaned = re.sub(r"\s+", " ", _NEEDS_RE.sub("", p)).strip()
        if markers and len(_TAG_RE.sub("", cleaned).strip()) < 80:
            if cleaned:
                _STRIPPED.append("Dropped (nothing left once the marker came out): "
                                 + _TAG_RE.sub("", cleaned).strip())
            continue
        out.append(cleaned)
    return out


DRAFT_NOTICE = f'''<div class="xpv-draft">
  <div class="k">DRAFT &mdash; PENDING ATTORNEY REVIEW</div>
  <p>This Privacy Policy is a <b>draft prepared for review by {ENTITY_SCOPE}'s attorney</b>.
  It has not been reviewed or approved by counsel, and it should not be relied on as a final
  statement of {ENTITY_SCOPE}'s privacy practices.</p>
  <p>It describes what this website does today, written by reading the site's own code. Several
  points are still being confirmed, including retention periods, the site's analytics and
  advertising tags, and how text-message preferences are handled. The effective date shown below
  is a placeholder until the reviewed version is published.</p>
  <p>Questions in the meantime go to <a href="mailto:{PRIVACY_EMAIL}">{PRIVACY_EMAIL}</a> or
  <a href="{T.PHONE_TEL}">{T.PHONE_DISPLAY}</a>.</p>
</div>'''


SECTIONS = [
    ("who-this-covers", "Who This Policy Covers", [
        f"<b>The companies.</b> This Privacy Policy applies to {D.DOMAIN} and to "
        f"the information collected by {ENTITY_SCOPE}. In this policy, \"Extreme\" means "
        f"both companies. Heating and cooling work is performed by {ENTITY}; plumbing work "
        f"is performed by {ENTITY_PLUMBING}. The two share this website, one phone number "
        f"and one scheduling system, so one policy covers both.",

        "<b>Where Extreme operates.</b> Extreme is an Ohio business serving homeowners in "
        "the Dayton and Cincinnati metro areas. Information collected through this site is "
        "stored and processed in the United States.",

        "<b>What this policy does not cover.</b> This policy covers this website and the "
        "requests you send through it. It also covers the Extreme employee app. See "
        "<a href=\"#employee-app\">The Extreme Employee App</a> below. "
        "It does not cover other companies' websites you "
        "reach from here, including lender sites, review sites and social media, each of "
        "which has its own privacy policy.",
    ]),

    ("information-we-collect", "Information Extreme Collects", [
        "<b>What you enter to schedule a visit.</b> Your first and last name, your mobile "
        "number, your email address if you choose to give one, and the service address "
        "where the work will happen. You also tell Extreme how you would like to be "
        "reached, whether you have used Extreme before, what service you need and the "
        "follow-up answers you select, the day and arrival window you would like, and your "
        "acknowledgement of the booking terms shown to you before you confirm.",

        "<b>Optional details about your home.</b> The details step is skippable. If you "
        "complete it, Extreme collects the property type, whether you own or rent, the "
        "approximate age of the system or the home, and where the outdoor unit sits. These "
        "help route the right technician with the right parts.",

        "<b>Anything you type in the notes field.</b> The notes box is free text and goes "
        "to Extreme exactly as you write it. Please don't put payment card numbers, bank "
        "details, Social Security numbers or health information there. Extreme does not "
        "need any of it to schedule a visit.",

        "<b>Photos you upload.</b> You may attach up to five photos of the problem. Photos "
        "are uploaded to Cloudinary, Extreme's image host, and Extreme receives a web link "
        "to each one. <b>Those links are public: anyone who has the link can open the "
        "photo.</b> Photos taken inside a home often show more than the equipment, so upload "
        "only what you are comfortable sharing. Photos are optional, and every request can "
        "be booked without them.",

        "<b>What you type in the address field.</b> To suggest matching Ohio addresses, "
        "what you type into the service-address field is sent to an address lookup service "
        "as you type it, once you have entered at least three characters. See "
        "<a href=\"#service-providers\">Service Providers</a> for who that is.",

        "<b>What your browser sends automatically.</b> Like most websites, this site and "
        "the services that deliver parts of it receive your IP address, your browser and "
        "device type, the pages you view, the page that referred you, and the date and time.",

        "<b>Advertising click identifiers.</b> If you arrive from a Google Ads click, the "
        "site saves that click's identifier in your browser's local storage so a booking can "
        "later be matched back to the ad that produced it. It stays in your browser until "
        "you clear your site data and is not linked to you by name unless you go on to book.",

        "<b>What this site does not collect.</b> This site does not take payment card "
        "numbers, bank account numbers or Social Security numbers, and it does not process "
        "payments or credit applications. Financing applications are submitted on the "
        "lender's own website, under the lender's privacy policy. See the Financing "
        "section of the <a href=\"/terms#financing\">Terms</a>.",

        "[NEEDS: whether inbound or outbound calls to " + D.PHONE_DISPLAY + " are recorded, and "
        "whether a call-tracking vendor such as CallRail is in use. If either is true it has "
        "to be disclosed here and the vendor named in Service Providers.]",
    ]),

    ("how-we-use", "How Extreme Uses It", [
        "<b>To do the work you asked for.</b> Scheduling the visit, routing the right "
        "technician, confirming the appointment, reaching you if something changes, "
        "performing the work, and following up afterward.",

        "<b>To prepare before arriving.</b> The issue you select, the details you give "
        "about your home, and any photos you upload are used to understand the problem "
        "before a technician arrives so the right parts are on the truck.",

        "<b>To keep your service record.</b> Estimates, invoices, work performed and "
        "warranty coverage, so Extreme can honor the Limited Warranty in the "
        "<a href=\"/terms#limited-warranty\">Terms</a> and answer questions about past work.",

        "<b>To administer the programs you join.</b> "
        "<a href=\"/maintenance\">X-Plan membership</a> and "
        "<a href=\"/referral\">Extreme Rewards</a> referral credit, under the terms published "
        "on the <a href=\"/terms\">Terms</a> page.",

        "<b>To understand the website.</b> Which pages and which ads lead to booked visits, "
        "so the site and the advertising spend can be improved. This is measured in "
        "aggregate, not to build a profile of you.",

        "<b>To meet legal obligations and protect people.</b> Tax and business records, "
        "responding to lawful requests, investigating fraud or misuse, and enforcing the "
        "<a href=\"/terms\">Terms</a>.",

        "[NEEDS: whether Extreme sends marketing email or marketing texts to people who "
        "submit the schedule form. If yes, this section has to say so plainly and the form "
        "needs its own consent line — a transactional confirmation is not consent to "
        "marketing.]",
    ]),

    ("service-providers", "Service Providers Extreme Uses", [
        "Extreme uses a small number of outside companies to run the website and the "
        "scheduling form. Each one receives only what it needs to do its job. They are "
        "named here rather than described generically, because you deserve to know exactly "
        "where what you type actually goes.",

        "<b>Formspree — form delivery.</b> When you submit the schedule form, everything "
        "you entered, together with the links to any photos, is sent through Formspree, "
        "which delivers it to Extreme's inbox and keeps a copy in Extreme's Formspree "
        "account.",

        "<b>Cloudinary — photo hosting.</b> Photos you attach are uploaded directly from "
        "your browser to Cloudinary and stored there. Extreme receives a link to each one. "
        "As noted above, those links are publicly accessible to anyone who has them.",

        "<b>Google — address suggestions, fonts and video.</b> Google's Maps and Places "
        "service returns the address suggestions in the service-address field, and receives "
        "what you type there. Google Fonts serves the site's typeface on every page, and "
        "embedded YouTube videos load from Google when a page containing one is opened. "
        "Google receives your IP address in each case, and may set cookies if you play a "
        "video. Google's use of that information is governed by Google's own privacy policy.",

        "<b>Komoot — backup address suggestions.</b> If Google's address service is "
        "unavailable, the site falls back to Photon, a free geocoder operated by Komoot and "
        "built on OpenStreetMap data. The same address text is sent there instead.",

        "<b>jsDelivr — images.</b> Photographs and graphics on the site are delivered by "
        "the jsDelivr content network, which receives your IP address.",

        # Written from tags/head.html and tags/body.html. New vendor there, add it here.
        "<b>Analytics and advertising measurement.</b> Every page loads Google Tag Manager, "
        "which in turn loads Google Analytics 4 and Google Ads conversion tracking. These "
        "record that pages were viewed, that a booking form was opened and that a booking was "
        "completed, along with general device and location information, and they set cookies "
        "in your browser. Google receives that information directly. It is used to measure "
        "which advertising produces calls and bookings, not to identify you by name. When you "
        "submit our online booking form, your email, phone number, name and address may be "
        "hashed and shared with Google to measure how our ads perform (Google Ads enhanced "
        "conversions).",

        "<b>Call measurement.</b> Google Ads may replace the phone number shown on the site "
        "with a forwarding number so that a call can be attributed to the advertising that "
        "produced it. The call still reaches the same office. The local numbers listed for "
        "each office are not replaced.",

        "<b>Booking and chat widgets.</b> Two further pieces of software load on every page: "
        f"{D.PRODUCT}, Extreme's own software, which powers the chat "
        "window in the corner of the page, and the ServiceTitan online scheduler, which "
        "opens in a window on this site when you book. "
        "Anything you type into the chat is received by Extreme. Anything you type into the "
        "scheduler is received by ServiceTitan as well as by Extreme, and ServiceTitan's own "
        "privacy terms apply to what it holds.",

        # 2026-10-01: the chat no longer collects texting consent; the Telnyx campaign is retired.
        f"<b>The chat window.</b> The chat window asks for your name. Your mobile number is "
        f"optional: {D.PRODUCT} uses it to find your account and so the office can call you "
        "back. The chat does not send you text messages. Texts you send to "
        f"{D.SMS_DISPLAY} are handled in ServiceTitan, our scheduling software; the Calls and "
        "Text Messages section below says how to stop them.",

        "[NEEDS: whether Extreme sends customer names, phone numbers or email addresses to "
        "Birdeye — or any other review platform — to request a review after a job. The site "
        "cites 2,000+ Birdeye reviews, so this flow probably exists. If it does, Birdeye "
        "belongs in this list and the review-request must be described in How Extreme Uses "
        "It. This is the most likely disclosure gap on the page.]",

        "[NEEDS: whether Extreme has signed a data processing agreement, or equivalent "
        "contractual restriction, with Formspree and Cloudinary. Attorney question — it "
        "determines whether this page can state that these providers may use the "
        "information only on Extreme's behalf.]",
    ]),

    ("other-sharing", "When Else Extreme Shares Information", [
        "<b>With the people doing the work.</b> Your name, address, phone number and the "
        "job details go to the technician assigned to your visit and to the office staff "
        "scheduling and invoicing it.",

        "<b>When you direct it.</b> If you ask Extreme to coordinate with a landlord, a "
        "property manager, a home warranty company or an insurer, Extreme shares what is "
        "needed for that purpose.",

        "<b>When the law requires it.</b> To comply with a subpoena, court order or other "
        "lawful request, to establish or defend a legal claim, or where Extreme believes in "
        "good faith that disclosure is necessary to prevent harm.",

        "<b>If the business changes hands.</b> If Extreme is sold, merged or reorganized, "
        "customer records may transfer as part of that transaction. This policy would "
        "continue to apply to the information transferred until it is replaced by a policy "
        "you are notified of.",

        "<b>What Extreme does not do.</b> Extreme does not sell your personal information, "
        "and does not give your name, phone number, email address or service address to "
        "other companies for their own marketing. "
        "[NEEDS: client confirmation that no customer or lead data is sold, traded or "
        "shared with lead-generation networks, partner contractors, home warranty companies "
        "or marketing partners. If any of that happens, this paragraph is wrong and has to "
        "be rewritten before publication.]",

        "[NEEDS: attorney review of whether the advertising tags described above constitute "
        "a \"sale\" or \"sharing\" under any state privacy statute that applies to Extreme, "
        "and whether an opt-out link is required as a result. Drafted as a plain no-sale "
        "statement, which is accurate for money changing hands but is not the whole of what "
        "some statutes define as selling.]",

        "<b>Subcontractors.</b> [NEEDS: whether Extreme uses subcontracted labor for any "
        "work sold under either entity. If so, say so here — a customer whose address goes "
        "to a third-party crew should learn that from this page, not at the door.]",
    ]),

    ("text-messages", "Calls and Text Messages", [
        "<b>Why Extreme needs your mobile number.</b> The number you give when you book is "
        "how Extreme confirms the appointment, tells you when the technician is on the way, "
        "and reaches you if the schedule changes. Choosing Call, Text or Email tells Extreme "
        "which you prefer.",

        "<b>Message rates.</b> Message and data rates may apply. Message frequency varies "
        "with your appointment.",

        # 2026-10-01: texts go to the main line and are answered in ServiceTitan (the Telnyx
        # campaign is retired). The sentence must still name the texting number.
        "<b>Stopping messages.</b> Reply STOP to any text message from "
        f"{D.SMS_DISPLAY} to opt out immediately, or call the office at "
        f"<a href=\"{T.PHONE_TEL}\">{T.PHONE_DISPLAY}</a> at any time and ask to be taken off "
        "text messages. Reply HELP to any text for assistance. Stopping texts does not "
        "cancel a scheduled visit: call the office to change or cancel an appointment.",

        "<b>Mobile numbers are never shared for marketing.</b> Extreme does not sell or "
        "share mobile numbers, or consent to receive text messages, with any third party for "
        "that party's marketing purposes.",

        "[NEEDS: attorney review of consent. The schedule form today has no separate "
        "opt-in for text messages — the only checkbox is the booking acknowledgement. That "
        "may be adequate for purely transactional appointment texts, but it is not consent "
        "to marketing texts. If Extreme sends anything promotional, the form needs an "
        "express consent line and this section needs to describe it.]",
    ]),

    ("cookies", "Cookies, Local Storage and Analytics", [
        "<b>What this site stores on your device.</b> The site saves advertising click "
        "identifiers in your browser's local storage, as described above, so that a booking "
        "can be attributed to the ad that produced it. Clearing your browsing data removes "
        "them.",

        "<b>Cookies set by others.</b> Services embedded in the site can set their own "
        "cookies, most commonly Google, when an embedded YouTube video is played, and any "
        "analytics or advertising tags installed on the page. Extreme does not control those "
        "cookies.",

        "<b>Your browser controls.</b> Every major browser lets you block or delete "
        "cookies and clear local storage, and most offer a private browsing mode. Blocking "
        "them will not stop you from booking a visit.",

        "<b>Do Not Track.</b> Browsers vary in how they send Do Not Track signals and there "
        "is no common standard for honoring them, so this site does not respond to them. "
        "[NEEDS: attorney direction on whether Extreme should honor Global Privacy Control "
        "signals, which several state statutes treat differently from Do Not Track.]",
    ]),

    ("retention", "How Long Extreme Keeps It", [
        "<b>Service records.</b> Records of work performed — estimates, invoices, equipment "
        "installed and warranty coverage — are kept for as long as needed to honor "
        "warranties, meet tax and accounting obligations, and answer questions about past "
        "work at your address.",

        "<b>Requests that never became a job.</b> [NEEDS: how long Extreme keeps schedule "
        "requests that were canceled or never completed. State a period here — an indefinite "
        "retention answer is a liability, and \"as long as necessary\" is not an answer a "
        "customer can act on.]",

        "<b>Form submissions held by Formspree.</b> [NEEDS: the submission-archive retention "
        "setting on Extreme's Formspree account. It varies by plan, and it is the copy "
        "nobody thinks about deleting.]",

        "<b>Photos.</b> [NEEDS: a retention answer for Cloudinary. Nothing in the current "
        "setup deletes uploaded photos automatically, which means today's honest answer is "
        "\"indefinitely\" — that should be fixed with an automatic deletion rule rather than "
        "disclosed as a permanent state.]",

        "<b>Deletion on request.</b> Whatever the periods above, you can ask Extreme to "
        "delete your information sooner, and Extreme will do so except where a record must "
        "be kept for warranty, tax, accounting or legal reasons. See "
        "<a href=\"#your-choices\">Your Choices</a>.",
    ]),

    ("your-choices", "Your Choices, and How to Request Deletion", [
        "<b>What you can ask for.</b> You can ask Extreme for a copy of the information it "
        "holds about you, ask for it to be corrected, ask for photos you uploaded to be "
        "deleted, ask to stop receiving marketing email or text messages, or ask for your "
        "information to be deleted altogether. Extreme honors these requests from any "
        "customer, wherever you live.",

        f"<b>How to ask.</b> Email <a href=\"mailto:{PRIVACY_EMAIL}\">{PRIVACY_EMAIL}</a> with "
        f"\"Privacy Request\" in the subject line, call "
        f"<a href=\"{T.PHONE_TEL}\">{T.PHONE_DISPLAY}</a>, or write to {ENTITY}, "
        f"{PRIVACY_ADDRESS}. Please include the name, phone number and service address used "
        f"when you booked, so the right record can be found. That is the only reason Extreme "
        f"asks for it, and it is not used for anything else.",

        "<b>How long it takes.</b> [NEEDS: a response commitment. Forty-five days is the "
        "window most state statutes use and is the safe default; confirm the office can "
        "actually meet whatever number is published.]",

        "<b>What Extreme may have to keep.</b> Some records cannot be deleted on request: "
        "invoices and tax records, records supporting an active warranty, and anything "
        "Extreme is required to retain by law or needs to establish or defend a legal claim. "
        "Extreme will tell you if that applies to your request.",

        "<b>No penalty for asking.</b> Extreme will not refuse service, charge a different "
        "amount, or provide a different level of service because you exercised any of these "
        "choices.",

        "<b>A note on the third parties above.</b> Deleting your information from Extreme's "
        "records does not by itself delete copies held by Google or other advertising "
        "services from their own tracking. Those are controlled through your browser and "
        "through your account settings with those companies.",
    ]),

    ("security", "How Extreme Protects It", [
        "<b>Reasonable safeguards.</b> The website is served over an encrypted connection, "
        "and form submissions and photo uploads travel over encrypted connections to the "
        "providers named above. Access to customer records inside Extreme is limited to "
        "staff who need it to do their jobs.",

        "<b>No guarantee.</b> No website or method of transmitting information over the "
        "internet is completely secure. Extreme cannot guarantee absolute security, and any "
        "information you send is sent at your own risk.",

        "<b>What not to send.</b> Please do not email or type payment card numbers, bank "
        "account numbers or Social Security numbers into the notes field or any other part "
        "of this site. Extreme will never ask for them there.",

        "[NEEDS: attorney direction on breach notification. Ohio has a data breach "
        "notification statute; whether this page should describe a notification commitment, "
        "and in what terms, is a legal decision.]",
    ]),

    ("children", "Children's Privacy", [
        "<b>This site is for adults.</b> Extreme's services are sold to homeowners and "
        "property owners. This website is not directed to children, and Extreme does not "
        "knowingly collect personal information from anyone under 13.",

        "<b>If it happens anyway.</b> If you believe a child under 13 has given Extreme "
        f"personal information, contact <a href=\"mailto:{PRIVACY_EMAIL}\">{PRIVACY_EMAIL}</a> "
        f"or call <a href=\"{T.PHONE_TEL}\">{T.PHONE_DISPLAY}</a> and it will be deleted.",

        "<b>Photos of a home.</b> A photo a customer uploads of a leak or a furnace may "
        "incidentally show other members of the household. Extreme uses those photos only to "
        "diagnose and prepare for the work requested, and deletes them on request like any "
        "other information.",
    ]),

    ("other-sites", "Other Companies' Websites", [
        "This site links to websites Extreme does not control, including "
        "<a href=\"/financing-options\">financing lenders</a>, review platforms, manufacturer "
        "sites and social media pages. Following one of those links takes you out of this "
        "policy's scope. Anything you enter there is collected by that company, under its own "
        "privacy policy, not this one. That is especially true of financing: a credit "
        "application is submitted on the lender's site and Extreme never sees what you enter "
        "there.",
    ]),

    ("changes", "Changes to This Policy", [
        "Extreme may update this policy as the website, the services it uses, or the law "
        "change. The current version is always posted here with its effective date at the "
        "top of the page. Continuing to use the site after an update means the updated "
        "policy applies. "
        "[NEEDS: whether Extreme wants to commit to notifying customers directly of material "
        "changes, and by what channel.]",
    ]),

    # Verbatim from ExtremeAppStore/privacy-policy-employee-app.md; 365 days must match followup-pro RETENTION_DAYS.
    ("employee-app", 'The Extreme Employee App', [
        '<span class="xtm-eff">Effective September 24, 2026</span>',
        'This section is for the technicians and office staff of Extreme Heating and Cooling Ltd ("Extreme") who use the Extreme app on an iPhone or iPad. The rest of this policy is about customers and this website.',
        '<h4 class="xtm-h4">What the app collects, and why</h4>',
        "<b>Your account.</b> When you sign in with your company Google account, the app sends your email address and your account's user ID to FollowUp Pro, Extreme's own business system. FollowUp Pro uses them to match you to your ServiceTitan technician record, to decide which parts of the app you can use, and to put your name on what you log.",
        '<b>What you log.</b> Follow-up outcomes, notes and next follow-up dates. Parts you use on a job, parts you take from the shop, and transfer and stock requests with any notes. For office staff, counts, stock moves, approvals and other inventory changes. Each is saved with your name, so the office knows who did what.',
        '<b>Call recordings you play.</b> Recordings of your calls come from ServiceTitan. The first time one is played, FollowUp Pro keeps a copy in Google Cloud Storage and plays it through a private link that stops working after 10 minutes. A recording plays only for the technician on the call and for the people Extreme allows to listen.',
        '<b>How you use the app.</b> FollowUp Pro records when you last signed in to the app. Each time a call recording is played, it also records which call it was, who played it and when. Extreme keeps this usage data for security and support, and deletes it after 365 days.',
        '<b>The camera.</b> The app uses the camera only to read part barcodes. The barcode is read on the phone and matched against the parts list the app keeps on the phone. A code is sent to FollowUp Pro only when you link it to a part. No photo or video leaves the phone.',
        "The app also shows you things it doesn't collect from you: your pay statements and hours, your coaching numbers, and customer and job details. Those come from Extreme's records in ServiceTitan and FollowUp Pro.",
        "The app doesn't collect your location, contacts, photos or device identifiers. It has no advertising, analytics or crash-reporting software in it.",
        '<h4 class="xtm-h4">What stays on your phone</h4>',
        "Your sign-in is kept in the Keychain on your iPhone or iPad, for that device only. The app keeps copies of your follow-ups, your numbers and the calculators' settings so it opens quickly and works without signal. Pay isn't kept on the device: a pay statement you open as a PDF is deleted when you close it. The files the app saves are left out of iCloud backups.",
        "Signing out deletes your sign-in and those copies. The parts catalog, the list of technicians and any material logs still waiting to send stay on the device. An unsent log still has to reach the shop's stock count.",
        '<h4 class="xtm-h4">Where it\'s stored</h4>',
        "FollowUp Pro runs on Google Firebase and Google Cloud, in the United States. Google also handles sign-in, because Extreme's company accounts are Google Workspace accounts.",
        '<h4 class="xtm-h4">Who receives it</h4>',
        "<b>Extreme.</b> The office and managers see what you log in FollowUp Pro. Follow-up entries go into the customer's shared follow-up history, which the office and other staff working with that customer can see.",
        "<b>ServiceTitan.</b> When you log a follow-up, a note is added to the customer's record in ServiceTitan, Extreme's field-service software. It carries your name, the outcome, what you wrote, the next follow-up date, and the estimate and job it's about.",
        '<b>Google.</b> Google hosts FollowUp Pro and runs the sign-in.',
        "Extreme doesn't sell this information. The app shows no ads and doesn't track you across other companies' apps or websites.",
        '<h4 class="xtm-h4">How long it\'s kept</h4>',
        "FollowUp Pro deletes these once they're more than 365 days old. A cleanup runs every night.",
        '<ul><li><span class="b"></span><span>Follow-up entries: the outcomes, notes and next follow-up dates you log, and the ServiceTitan calls filed in a customer\'s follow-up history. Each customer\'s follow-up summary is worked out again from the entries that are left.</span></li><li><span class="b"></span><span>The time you last signed in to the app.</span></li><li><span class="b"></span><span>The record of each recording play: which call, who played it and when.</span></li><li><span class="b"></span><span>The saved copy of a call recording, 365 days after the copy was made.</span></li><li><span class="b"></span><span>FollowUp Pro\'s copy of each ServiceTitan call record: who was on the call, the customer, the direction and how long it lasted.</span></li><li><span class="b"></span><span>The copy of clocked hours the Pay tab keeps so it opens quickly.</span></li></ul>',
        'One-time sign-in codes expire after two minutes and are deleted within two days.',
        "These stay, because they're Extreme's business records:",
        '<ul><li><span class="b"></span><span>Parts and stock records: parts used on jobs, parts taken from the shop, transfer and stock requests, counts, stock moves and approvals. The shop\'s stock count depends on them.</span></li><li><span class="b"></span><span>Notes sent to ServiceTitan. A follow-up note on a customer\'s record in ServiceTitan follows ServiceTitan\'s records. Deleting the entry in FollowUp Pro doesn\'t remove the note from ServiceTitan.</span></li><li><span class="b"></span><span>The office\'s own call records. When the office logs a follow-up outcome from its queue, it\'s also saved in the office\'s call records, which the office\'s reports count.</span></li><li><span class="b"></span><span>Pay and coaching records. Your pay statements, hours and coaching numbers come from Extreme\'s payroll and job records and are kept with them. That includes the PDF copy of a pay statement that FollowUp Pro saves the first time the statement is opened.</span></li><li><span class="b"></span><span>Your FollowUp Pro account (your email address, name and role), for as long as you have the account. Google\'s sign-in service also keeps when your account last signed in, as part of the account.</span></li></ul>',
        "Google Cloud keeps FollowUp Pro's server logs, which record the IP address each request came from, for 30 days.",
        '<h4 class="xtm-h4">Seeing, correcting or deleting your information</h4>',
        'To get a copy of your information, or to have it corrected or deleted, email <a href="mailto:onboarding@extremeheating.com">onboarding@extremeheating.com</a>.',
        "You can't create or delete an account in the app. Extreme's Google Workspace administrator creates and removes company accounts, and an administrator can turn off your app access in FollowUp Pro. A note already added to a customer's record in ServiceTitan stays there until someone removes it in ServiceTitan.",
        '<h4 class="xtm-h4">Security</h4>',
        "The app talks to Extreme's servers only over encrypted (HTTPS) connections, and it keeps your sign-in in the device's Keychain.",
    ]),
]

CONTACT_SECTION = ("contact-us", "How to Contact Extreme", [
    f"<b>By phone.</b> <a href=\"{T.PHONE_TEL}\">{T.PHONE_DISPLAY}</a>. The office is staffed "
    f"{D.HOURS_STAFFED}, and the emergency line is answered 24/7.",

    f"<b>By email.</b> <a href=\"mailto:{PRIVACY_EMAIL}\">{PRIVACY_EMAIL}</a>, with \"Privacy "
    f"Request\" in the subject line.",

    f"<b>By mail.</b> {ENTITY} / {ENTITY_PLUMBING}, {PRIVACY_ADDRESS}. "
    "[NEEDS: create a dedicated privacy@extremeheating.com alias and point it at whoever "
    "actually owns these requests. A privacy contact that lands in the general sales inbox "
    "is how a deletion request gets missed.]",

    f"<b>Office addresses.</b> All four {D.COMPANY} offices, and directions to each, are on "
    f"the <a href=\"/contact\">contact page</a>.",
])


PRIVACY_GAPS = [
    "ATTORNEY REVIEW — this entire page is an unreviewed draft and renders a visible draft "
    "notice saying so. It must not be linked from the sitewide footer, and the notice must "
    "not be removed, until counsel has read it and the items below are resolved.",
    "RESOLVED 2026-08-03: counsel approved the page as it stood and it is published with a\n"
    "real effective date. The items below are NOT blockers on that approval — they are the\n"
    "open questions a future revision should close, and several of them are answers only the\n"
    "business can give.",
    "RESOLVED 2026-08-03: the tag inventory is confirmed and disclosed — GTM, GA4, "
    "Google Ads with call measurement, FollowUp Pro and the "
    "ServiceTitan scheduler. Counsel should still review whether the advertising "
    "tags require a consent mechanism for Ohio visitors, which is a separate "
    "question from disclosure and is still open below.",
    "STOP/HELP keywords are NOT published, because nobody has confirmed the texting platform "
    "honors them. The clause tells customers to call the office instead. Restore the keyword "
    "sentence once the platform is confirmed.",
    "Birdeye: whether customer contact details are sent to a review platform after a job. "
    "The site cites 2,000+ Birdeye reviews, so this flow probably exists and is undisclosed.",
    "Call recording and call tracking on " + D.PHONE_DISPLAY + ".",
    "Retention periods: canceled/unbooked requests, the Formspree submission archive, and "
    "uploaded photos on Cloudinary.",
    "Response-time commitment for access and deletion requests (45 days is the common "
    "statutory window).",
    "Confirmation that no customer or lead data is sold or shared with lead-generation "
    "networks, partner contractors or marketing partners.",
    "Whether marketing email or marketing text messages are sent to form submitters, and if "
    "so, adding an express consent line to the schedule form.",
    "Whether subcontracted labor is used, since that sends a customer's address to a third "
    "party.",
    "Data processing agreements with Formspree and Cloudinary — required before this page "
    "can state that these providers use the information only on Extreme's behalf.",
    "Whether any state privacy statute applies to Extreme, and whether an opt-out link, a "
    "Global Privacy Control response, or state-specific rights language is therefore needed.",
    "Breach notification: whether to describe a notification commitment on this page.",
    "A dedicated privacy@extremeheating.com alias, and an owner for the requests it receives.",
    "ENGINEERING: Cloudinary photos are uploaded through an unsigned preset and returned as "
    "permanent public URLs with no expiry. The draft discloses this honestly, but the right "
    "answer is signed or expiring delivery URLs plus an automatic deletion rule. Fixing it "
    "would let two paragraphs of this page get considerably shorter.",
]


def hero():
    return f'''<div class="xsp-hero sub">
  {T.hero_mark()}
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs([("Home", "/"), ("Privacy", "")])}
      <div class="xsp-eyebrow" style="color:#8FD481;margin-top:14px">PRIVACY &amp; YOUR DATA</div>
      <h1 class="xsp-h1">Privacy Policy</h1>
      <p class="xsp-intro">This policy explains what {ENTITY_SCOPE} collect when you use this
      site or schedule a visit, who it goes to, how long it is kept, and how to ask for a copy
      of it or have it deleted.</p>
      <div class="xtm-updated">Effective {EFFECTIVE}</div>
    </div>
  </div>
</div>'''


def summary():
    bullets = [
        "Booking a visit means giving Extreme your name, mobile number, service address "
        "and the details of the job. Email is optional.",
        "Photos you upload are stored by Cloudinary, and anyone who has the link can open "
        "them, so upload only what you are comfortable sharing.",
        "What you type into the address field is sent to Google, or to Komoot when Google "
        "is unavailable, to suggest matching addresses.",
        "Extreme does not sell your personal information, and never shares mobile numbers "
        "for anyone else's marketing.",
        "You can ask for a copy of your information, ask for it to be corrected, or ask "
        "for it to be deleted.",
        "Financing applications are submitted on the lender's website and are covered by "
        "the lender's privacy policy, not this one.",
    ]
    lis = "".join(f'<li><span class="b"></span><span>{b}</span></li>' for b in bullets)
    return f'''<div class="xtm-summary">
  <div class="k">THE SHORT VERSION</div>
  <h2>What Extreme collects, and what happens to it.</h2>
  <p>Extreme asks for what it needs to get a technician to the right address with the right
  parts, and nothing more. This page names every outside company involved rather than
  describing them generically, so you can see exactly where what you type ends up.</p>
  <ul>{lis}</ul>
  <div class="xtm-note"><b>Note:</b> This site does not take payment card numbers, bank
  account numbers or Social Security numbers, and it does not process payments. Please don't
  enter any of them in the notes field.</div>
</div>'''


def contact():
    return f'''<div class="xtm-contact">
  <div>
    <div class="t">Questions About Your Information</div>
    <div class="d">Ask for a copy, a correction, or a deletion, by phone or by email.</div>
  </div>
  <a class="xsp-cta" href="{T.PHONE_TEL}">Call {T.PHONE_DISPLAY}</a>
</div>'''


def privacy_page(d, root_class):
    _STRIPPED.clear()
    all_sections = [(a, t, _clean(p)) for a, t, p in SECTIONS + [CONTACT_SECTION]]
    body_secs = "".join(TM.sec(a, t, p) for a, t, p in all_sections)
    for note in _STRIPPED:
        if note not in PRIVACY_GAPS:
            PRIVACY_GAPS.append(note)
    body = f'''{hero()}
<div class="xco-body">
  <div class="xtm-lead">
    {summary()}
    {contact()}
    {TM.toc(all_sections)}
  </div>
  <div>{body_secs}</div>
</div>'''
    return shell(root_class, body)


def pages(root):
    return [(os.path.join(root, "pages", "company", "privacy.html"),
             privacy_page, {}, "xsp-privacy")]
