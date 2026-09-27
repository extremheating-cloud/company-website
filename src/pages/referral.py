# Customer-facing programs.md terms only. No capture form: naming the referrer at booking earns the reward.
import os
from layout import components as T
from pages import company_shared as CP
from data import business as D

# AA-safe text green on white (4.56:1); #6BB85C/#61BC47 are fills only.
GREEN_TEXT = "#3F852B"

REFERRAL_CSS = """
.xsp-referral .xsp-h1,.xsp-referral .xsp-h2,.xsp-referral .xsp-step .n{font-weight:800}
.xsp-referral .xsp-eyebrow{color:#3F852B}
.xsp-referral .xsp-check .c{background:#3F852B;color:#fff}
/* --green is 4.04:1 on the hero gradient here; --green-hover clears AA */
.xsp-referral .xsp-crumbs .cur{color:var(--green-hover)}
/* 44px thumb target on the breadcrumb without shifting the hero layout */
.xsp-referral .xsp-crumbs a{display:inline-block;padding:15px 6px;margin:-15px -6px}
.xsp-referral :focus-visible{outline:3px solid #61BC47;outline-offset:2px}

.xrf-mirror-line{margin-top:14px;font-style:italic;font-weight:800;font-size:24px;
letter-spacing:-.3px;color:var(--green-hover)}

.xrf-mech{background:#fff}
.xrf-mech-in{max-width:1280px;margin:0 auto;padding:44px 40px 0}
.xrf-mech-card{background:var(--tint);border-left:6px solid var(--green);border-radius:16px;
padding:28px 32px}
/* purple, not #3F852B: green text drops to 4.08:1 on the tint */
.xrf-mech-card .k{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--purple)}
.xrf-mech-card h2{margin-top:10px;font-style:italic;font-weight:800;font-size:30px;
line-height:1.15;letter-spacing:-.5px;color:var(--purple)}
.xrf-mech-card p{margin-top:12px;font-size:15px;line-height:1.6;font-weight:500;color:var(--ink);
max-width:760px}
.xrf-mech-card p b{font-weight:800}

.xrf-pairs{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.xrf-pair{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}
.xrf-pair .head{background:var(--tint);padding:16px 20px;font-weight:800;font-size:16.5px;
color:var(--purple);line-height:1.35}
.xrf-pair .cells{display:grid;grid-template-columns:1fr 1fr}
.xrf-pair .cell{padding:22px 18px;text-align:center}
.xrf-pair .cell.you{background:var(--green-tint);border-left:1px solid var(--rule)}
/* --body, not #3F852B: green is 4.16:1 on the green tint and fails AA at 11px */
.xrf-pair .lab{font-size:11px;font-weight:800;letter-spacing:1.6px;color:var(--body)}
.xrf-pair .amt{font-style:italic;font-weight:800;font-size:36px;letter-spacing:-1px;
color:var(--purple);margin-top:8px;line-height:1}
.xrf-pair .cell.you .amt{color:#3F852B}
.xrf-nolimit{margin-top:16px;font-size:14px;line-height:1.6;font-weight:600;color:var(--body)}
.xrf-nolimit b{color:var(--ink);font-weight:800}

.xrf-share{border:1px solid var(--rule);border-radius:16px;background:#fff;padding:24px;margin-top:20px}
.xrf-msg{background:var(--soft);border:1px solid var(--rule);border-radius:12px;padding:16px 18px;
font-size:16px;line-height:1.65;font-weight:500;color:var(--ink);margin-top:14px}
.xrf-share-row{display:flex;align-items:center;gap:14px;margin-top:14px;flex-wrap:wrap}
.xrf-copy{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:14px;padding:12px 20px;border-radius:10px;min-height:44px;
border:0;cursor:pointer;font-family:inherit;transition:background .15s}
.xrf-copy:hover{background:var(--green-hover)}
.xrf-copied{font-size:13px;font-weight:700;color:#3F852B}

.xrf-xp{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;
background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:16px;padding:24px 28px;
color:#fff;margin-top:20px}
.xrf-xp .t{font-weight:800;font-size:18px}
.xrf-xp .d{font-size:13.5px;line-height:1.55;font-weight:500;color:rgba(255,255,255,.8);margin-top:6px;
max-width:60ch}
.xrf-xp .xsp-cta{white-space:nowrap}

.xrf-terms{border:1px solid var(--rule);border-radius:16px;background:#fff;padding:24px;margin-top:20px}
.xrf-terms-line{background:var(--tint);border-radius:12px;padding:16px 18px;font-size:14px;
line-height:1.65;font-weight:700;color:var(--ink)}
.xrf-terms-line a{color:var(--purple);font-weight:800}
.xrf-plain{list-style:none;padding:0;margin:18px 0 0;display:flex;flex-direction:column;gap:10px}
.xrf-plain li{display:flex;gap:10px;font-size:13.5px;line-height:1.6;font-weight:500;color:var(--body)}
.xrf-plain li .b{width:7px;height:7px;border-radius:50%;background:var(--green);flex:none;margin-top:7px}
.xrf-plain li b{color:var(--ink);font-weight:800}

@media (max-width:809px){
.xrf-mirror-line{font-size:19px;margin-top:12px}
.xrf-mech-in{padding:32px 20px 0}
.xrf-mech-card{padding:22px 20px;border-left-width:5px}
.xrf-mech-card h2{font-size:23px}
.xrf-mech-card p{font-size:14.5px}
.xrf-pairs{grid-template-columns:1fr;gap:14px}
.xrf-pair .head{padding:14px 16px;font-size:15.5px}
.xrf-pair .cell{padding:18px 12px}
.xrf-pair .amt{font-size:30px}
.xrf-share,.xrf-terms{padding:20px}
.xrf-copy{width:100%}
.xrf-xp{grid-template-columns:1fr;padding:22px 20px}
.xrf-xp .xsp-cta{width:100%}
}
"""

SHARE_JS = """
  <script>
    (() => {
      const root = document.currentScript.closest(".xhac-svc");
      if (!root) return;
      const share = root.querySelector("[data-xrf-share]");
      if (!share) return;
      const btn = share.querySelector("[data-xrf-copy]");
      const msg = share.querySelector("[data-xrf-msg]");
      const said = share.querySelector("[data-xrf-copied]");
      btn.addEventListener("click", async () => {
        const text = msg.textContent.trim();
        let ok = false;
        try {
          await navigator.clipboard.writeText(text);
          ok = true;
        } catch (e) {
          try {
            const ta = document.createElement("textarea");
            ta.value = text;
            ta.setAttribute("readonly", "");
            ta.style.position = "fixed";
            ta.style.opacity = "0";
            document.body.appendChild(ta);
            ta.select();
            ok = document.execCommand("copy");
            document.body.removeChild(ta);
          } catch (e2) {}
        }
        said.textContent = ok
          ? "Copied. Paste it into a text or email."
          : "Press and hold the message above to copy it.";
      });
    })();
  </script>"""


def shell(root_class, body):
    return f'''<section class="xhac-svc {root_class}">
  <style>{T.CSS}{CP.COMPANY_CSS}{REFERRAL_CSS}</style>
{body}
{T.script("xhac-svc")}
{SHARE_JS}
</section>
'''


# Framer page-settings copy; keep in sync with head.CORE["/referral"].
PAGE_TITLE = f"Refer a Friend & Earn $250 | {D.COMPANY}"
PAGE_DESC = (
    f'Extreme Rewards: a friend saves {D.REWARDS["newSystem"]} on a new system or '
    f'{D.REWARDS["everythingElse"]} on any other job of {D.REWARDS["everythingElseMin"]} or more, '
    "and you earn the same on a Visa gift card. Name them at booking."
)

UPDATED = CP.UPDATED
UPDATED_ISO = CP.UPDATED_ISO

REFERRAL = {
    "breadcrumb": [("Home", "/"), ("Extreme Rewards", "")],
    "h1": "Give {X}. Get $250.",
    "h1Highlight": "$250",
    "mirror": "Whatever they save, you earn.",
    "answer": ("A friend you send us saves "
               f'{D.REWARDS["newSystem"]} on a new heating, cooling or plumbing system, or '
               f'{D.REWARDS["everythingElse"]} on any other job of '
               f'{D.REWARDS["everythingElseMin"]} or more. You earn the same amount back '
               "on a Visa gift card once their job is done."),
    "intro": "There's no limit on how many people you send, and no form to fill in. They just have to give your name when they book.",
    "heroChips": [
        "No limit on how many friends you refer",
        "Paid on a Visa gift card",
        "New customers only",
    ],
    "pairs": [
        {"head": "They're getting a new heating, cooling, or plumbing system",
         "they": D.REWARDS["newSystem"], "you": D.REWARDS["newSystem"]},
        {"head": f'Everything else, on jobs of {D.REWARDS["everythingElseMin"]} or more',
         "they": D.REWARDS["everythingElse"], "you": D.REWARDS["everythingElse"]},
    ],
    "how": {
        "h2": "How do I earn a referral reward?",
        "steps": [
            {"title": "Tell a friend about us",
             "desc": f'Give them our name, and yours. They save {D.REWARDS["newSystem"]} on a new '
                      f'heating, cooling, or plumbing system, or {D.REWARDS["everythingElse"]} on any '
                      f'other job of {D.REWARDS["everythingElseMin"]} or more.'},
            {"title": "They mention your name when they book",
             "desc": "This is the step that counts. We ask every new customer who sent them, and your name in that answer is what earns your card."},
            {"title": "You earn a Visa gift card once the job is done and paid",
             "desc": "Whatever your friend saved, you earn. We don't pay on the booking. We pay once the work is finished and the invoice is settled, and cards go out within 90 days of that."},
        ],
    },
    "shareMsg": f"I use Extreme for heating, cooling, and plumbing. They're local, and they price "
                f"the work up front before they start. If you call them, mention my name: new "
                f'customers get {D.REWARDS["newSystem"]} off a new system, or '
                f'{D.REWARDS["everythingElse"]} off any other job of '
                f'{D.REWARDS["everythingElseMin"]} or more. extremeheating.com',
    "termsLine": f'New customers only. The {D.REWARDS["everythingElse"]} applies to jobs of {D.REWARDS["everythingElseMin"]} or more; the {D.REWARDS["newSystem"]} new-system reward has no minimum. Referral must be named when the job is booked. Reward issued within 90 days of job completion. See full terms at <a href="/terms">extremeheating.com/terms</a>.',
    "plain": [
        ("New customers only.", "We can't have serviced that address in the last 24 months."),
        ("Your name has to be given when the job is booked.", "We can't add it to a job after the fact, so tell your friend to have it ready."),
        ("Your name stays valid for 90 days after it's given.", "That covers you if the job gets scheduled or finished later. It is not extra time to get your name added."),
        ("We issue cards within 90 days of the job being completed and paid.", "The work has to be finished and the invoice settled before a card goes out."),
        ("No referring yourself, and Extreme employees aren't eligible.", "The program is for customers sending us someone new."),
    ],
    "table": {
        "eyebrow": "THE TWO AMOUNTS",
        "h2": "How much does a referral pay?",
        "id": "amounts",
        "takeaway": f'A referral on a new heating, cooling or plumbing system pays '
                    f'{D.REWARDS["newSystem"]} to the person who sent them.',
        "caption": "Extreme Rewards amounts",
        "columns": ["What the referred customer books", "What they save", "What the referrer earns"],
        "rows": [
            ["A new heating, cooling or plumbing system",
             f'{D.REWARDS["newSystem"]} off the job',
             f'{D.REWARDS["newSystem"]} on a Visa gift card'],
            [f'Everything else, on jobs of {D.REWARDS["everythingElseMin"]} or more',
             f'{D.REWARDS["everythingElse"]} off the job',
             f'{D.REWARDS["everythingElse"]} on a Visa gift card'],
        ],
    },
    "faqEyebrow": "REFERRAL QUESTIONS",
    "faqH2": "What do people ask about Extreme Rewards?",
    "faq": [
        {"q": "How does Extreme Rewards work?",
         "a": "Your friend books a job and gives your name. They save "
              f'{D.REWARDS["newSystem"]} on a new system or '
              f'{D.REWARDS["everythingElse"]} on any other job of '
              f'{D.REWARDS["everythingElseMin"]} or more, and you earn the same amount '
              "on a Visa gift card."},
        {"q": "Is there a limit on how many people I can refer?",
         "a": "No limit. Every completed job earns its own card."},
        {"q": "When do I get my card?",
         "a": "Within 90 days of the job being finished and paid. The invoice has to be settled "
              "before a card goes out."},
        {"q": "Can my name be added to a job after the visit?",
         "a": "No. It has to be given when the job is booked — we can't add it afterwards, so "
              'have your friend <a href="/contact">book with your name ready</a>.'},
        {"q": "How long does my name stay valid?",
         "a": "90 days from the day it's given, which covers a job that gets scheduled or "
              "finished later. It isn't extra time to get the name added."},
        {"q": "Do employees qualify?",
         "a": "No. This is for customers sending us someone new, so self-referrals and employee "
              "referrals aren't eligible."},
    ],
}


def hero(d):
    return f'''<div class="xsp-hero">
  {T.hero_mark()}
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs(d["breadcrumb"])}
      <div class="xsp-eyebrow" style="color:#8FD481;margin-top:14px">EXTREME REWARDS</div>
      {T.h1(d["h1"], d["h1Highlight"])}
      <div class="xrf-mirror-line">{d["mirror"]}</div>
      {T.answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas">
        <a class="xsp-cta" href="#xrf-share">Share With a Friend</a>
        <a class="xsp-cta-outline" href="#xrf-how">See How It Works</a>
      </div>
      {T.chips(d["heroChips"])}
    </div>
  </div>
</div>'''


def mechanism():
    return '''<div class="xrf-mech"><div class="xrf-mech-in">
  <div class="xrf-mech-card">
    <div class="k">WHAT EARNS YOUR GIFT CARD</div>
    <h2>Tell your friend to mention your name when they book.</h2>
    <p>When your friend calls or books online, we ask who we can thank for sending them. The name
    they give is the one we pay. There's no form on this page that does it for you, and we can't
    add your name to a job after it's booked, so make sure your friend has it ready.</p>
  </div>
</div></div>'''


def pairs(d):
    cards = "".join(f'''<div class="xrf-pair">
    <div class="head">{p["head"]}</div>
    <div class="cells">
      <div class="cell"><div class="lab">THEY SAVE</div><div class="amt">{p["they"]}</div></div>
      <div class="cell you"><div class="lab">YOU EARN</div><div class="amt">{p["you"]}</div></div>
    </div>
  </div>''' for p in d["pairs"])
    return f'''<div id="xrf-pairs">
  <div class="xsp-eyebrow">THE WHOLE PROGRAM</div>
  <h2 class="xsp-h2">What is the Extreme Rewards referral program?</h2>
  {T.paragraphs(['Two numbers, and they match. Whatever your friend saves on the job they book, '
                 'you earn back on a Visa gift card.'])}
  <div class="xrf-pairs">{cards}</div>
  <div class="xrf-nolimit">If your friend saved {D.REWARDS["everythingElse"]}, you earn
  {D.REWARDS["everythingElse"]}. There's no limit on how many friends you can refer.</div>
  <div class="xrf-nolimit">The {D.REWARDS["everythingElse"]} applies to jobs of
  {D.REWARDS["everythingElseMin"]} or more. The {D.REWARDS["newSystem"]} on a new system has no minimum.</div>
</div>'''


def xplan_strip():
    return '''<div class="xrf-xp">
  <div>
    <div class="t">While you're here, X-Plan covers your own system.</div>
    <div class="d">Two Safety &amp; Performance Visits a year, 15% off all repairs, and priority
    scheduling.</div>
  </div>
  <a class="xsp-cta" href="/maintenance">Explore X-Plan</a>
</div>'''


def share(d):
    return f'''<div id="xrf-share">
  <div class="xsp-eyebrow">SHARE IT</div>
  <h2 class="xsp-h2">How do I tell a friend about Extreme?</h2>
  {T.paragraphs(["Give them the company name and yours. A short message works better than a "
                 "pitch, and the one below is written to be sent as a text rather than read as "
                 "an ad."])}
  <div class="xrf-share" data-xrf-share>
    <p style="font-size:14px;line-height:1.6;font-weight:500;color:var(--body);max-width:70ch">
    Copy this and send it to whoever came to mind. It already tells them to name you when they
    book.</p>
    <div class="xrf-msg" data-xrf-msg>{d["shareMsg"]}</div>
    <div class="xrf-share-row">
      <button type="button" class="xrf-copy" data-xrf-copy>Copy Message</button>
      <span class="xrf-copied" data-xrf-copied role="status" aria-live="polite"></span>
    </div>
  </div>
</div>'''


def terms(d):
    items = "".join(
        f'<li><span class="b"></span><span><b>{b}</b> {rest}</span></li>' for b, rest in d["plain"])
    return f'''<div id="xrf-terms">
  <div class="xsp-eyebrow">THE FINE PRINT, IN PLAIN ENGLISH</div>
  <h2 class="xsp-h2">Who is eligible to refer someone?</h2>
  {T.paragraphs(['If we have worked on your home before, you can refer someone, as many times '
                 'as you like. The person you send has to be new to us, meaning no service at '
                 'that address in the last 24 months. You cannot refer yourself, and employees '
                 'are not eligible.'])}
  <div class="xrf-terms">
    <div class="xrf-terms-line">{d["termsLine"]}</div>
    <ul class="xrf-plain">{items}</ul>
  </div>
</div>'''


def crosslinks():
    return T.paragraphs(
        ['While you\'re here: <a href="/maintenance">X-Plan</a> covers your own system, '
         '<a href="/specials">this season\'s specials</a> apply to the job your friend books, '
         '<a href="/financing-options">financing on a new system</a> runs through three lenders, '
         'and every <a href="/services">heating, cooling and plumbing service</a> is booked on '
         'the same number. Full '
         '<a href="/terms#extreme-rewards">Extreme Rewards terms</a> are on the terms page.'])


def referral_page(d, root_class):
    body = f'''{hero(d)}
{mechanism()}
<div class="xco-body">
  {pairs(d)}
  {T.table_section(d["table"])}
  <div id="xrf-how">{T.process(d["how"], eyebrow="HOW IT WORKS")}</div>
  {xplan_strip()}
  {share(d)}
  {terms(d)}
  {T.faq(d["faq"], d["faqEyebrow"], h2=d["faqH2"])}
  {crosslinks()}
  {T.updated_line(UPDATED, UPDATED_ISO)}
</div>'''
    return shell(root_class, body)


def pages(root):
    return [(os.path.join(root, "pages", "company", "referral.html"),
             referral_page, REFERRAL, "xsp-referral")]
