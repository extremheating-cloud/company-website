"""Extreme Rewards referral page — /referral.

Every amount, condition and term comes from the CUSTOMER-FACING sections of
~/.claude/skills/extreme-brand/references/programs.md. Nothing from that file's
internal-rules section appears here — no job-type table, no spend backstop, no
payout mechanics, no tax handling, no cost per acquisition, and no stacking rule
(stacking moved into the internal section in the 2026-07-31 revision).

The program is deliberately two numbers: $250 on a new heating, cooling, or
plumbing system, $100 on everything else, and the referrer earns
whatever their friend saved. programs.md bans tiers, spend thresholds and job-type
lists from customer copy — so this page carries no payout calculator, and no
X-Plan referral bonuses (the +$30 / +$20 were removed from the program).

Mechanism note: this program pays because the referred customer NAMES the
referrer at booking. There is deliberately no "enter your friend's email" capture
form — a form implies submitting it is what earns the reward, which is exactly
what creates payout disputes. The share block is a copy-a-message convenience
that repeats the naming instruction instead.
"""
import os
import template as T
import company_pages as CP

# Accessible green for type on light backgrounds (4.56:1). #6BB85C/#61BC47 are
# fills only — they fail AA as text on white (2.43:1 / 2.39:1).
GREEN_TEXT = "#3F852B"

REFERRAL_CSS = """
/* ------------------------- Extreme Rewards (/referral) ------------------------- */
/* Montserrat 400-800 only on this page — the shared template's 900 is capped. */
.xsp-referral .xsp-h1,.xsp-referral .xsp-h2,.xsp-referral .xsp-step .n{font-weight:800}
/* Every green glyph/eyebrow on white steps down to the accessible green. */
.xsp-referral .xsp-eyebrow{color:#3F852B}
.xsp-referral .xsp-check .c{background:#3F852B;color:#fff}
/* breadcrumb sits on the lightest part of the hero gradient (#5E2C7E) where
   --green lands at 4.04:1; the lighter token clears AA at 5.57:1. */
.xsp-referral .xsp-crumbs .cur{color:var(--green-hover)}
/* 44px thumb target on the breadcrumb without shifting the hero layout */
.xsp-referral .xsp-crumbs a{display:inline-block;padding:15px 6px;margin:-15px -6px}
.xsp-referral :focus-visible{outline:3px solid #61BC47;outline-offset:2px}

/* the mirror line under the H1 — the sentence the whole program rests on */
.xrf-mirror-line{margin-top:14px;font-style:italic;font-weight:800;font-size:24px;
letter-spacing:-.3px;color:var(--green-hover)}

/* the mechanism — the single most important block on the page */
.xrf-mech{background:#fff}
.xrf-mech-in{max-width:1280px;margin:0 auto;padding:44px 40px 0}
.xrf-mech-card{background:var(--tint);border-left:6px solid var(--green);border-radius:16px;
padding:28px 32px}
/* purple (not green-text) on the tint fill: #3F852B drops to 4.08:1 on #F4F1F8.
   This is the brand's documented pairing — purple-tint callout + purple heading. */
.xrf-mech-card .k{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--purple)}
.xrf-mech-card h2{margin-top:10px;font-style:italic;font-weight:800;font-size:30px;
line-height:1.15;letter-spacing:-.5px;color:var(--purple)}
.xrf-mech-card p{margin-top:12px;font-size:15px;line-height:1.6;font-weight:500;color:var(--ink);
max-width:760px}
.xrf-mech-card p b{font-weight:800}

/* the two-number offer, shown as a mirror */
.xrf-pairs{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.xrf-pair{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}
.xrf-pair .head{background:var(--tint);padding:16px 20px;font-weight:800;font-size:16.5px;
color:var(--purple);line-height:1.35}
.xrf-pair .cells{display:grid;grid-template-columns:1fr 1fr}
.xrf-pair .cell{padding:22px 18px;text-align:center}
.xrf-pair .cell.you{background:var(--green-tint);border-left:1px solid var(--rule)}
/* Label stays --body on both sides: #3F852B on the green tint is only 4.16:1, which
   fails AA at this 11px size. The tinted cell and the green numeral carry the signal. */
.xrf-pair .lab{font-size:11px;font-weight:800;letter-spacing:1.6px;color:var(--body)}
.xrf-pair .amt{font-style:italic;font-weight:800;font-size:36px;letter-spacing:-1px;
color:var(--purple);margin-top:8px;line-height:1}
.xrf-pair .cell.you .amt{color:#3F852B}
.xrf-nolimit{margin-top:16px;font-size:14px;line-height:1.6;font-weight:600;color:var(--body)}
.xrf-nolimit b{color:var(--ink);font-weight:800}

/* share */
.xrf-share{border:1px solid var(--rule);border-radius:16px;background:#fff;padding:24px;margin-top:20px}
.xrf-msg{background:var(--soft);border:1px solid var(--rule);border-radius:12px;padding:16px 18px;
font-size:16px;line-height:1.65;font-weight:500;color:var(--ink);margin-top:14px}
.xrf-share-row{display:flex;align-items:center;gap:14px;margin-top:14px;flex-wrap:wrap}
.xrf-copy{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:14px;padding:12px 20px;border-radius:10px;min-height:44px;
border:0;cursor:pointer;font-family:inherit;transition:background .15s}
.xrf-copy:hover{background:var(--green-hover)}
.xrf-copied{font-size:13px;font-weight:700;color:#3F852B}

/* x-plan strip */
.xrf-xp{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;
background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:16px;padding:24px 28px;
color:#fff;margin-top:20px}
.xrf-xp .t{font-weight:800;font-size:18px}
.xrf-xp .d{font-size:13.5px;line-height:1.55;font-weight:500;color:rgba(255,255,255,.8);margin-top:6px;
max-width:60ch}
.xrf-xp .xsp-cta{white-space:nowrap}

/* terms */
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


# ---------------------------------------------------------------- content
# Page title / meta description for Framer page settings (embeds cannot set these):
PAGE_TITLE = "Extreme Rewards Referral Program | Give $250. Get $250."
PAGE_DESC = (
    "Refer a friend: they save $250 on a new system or $100 on any repair, and you "
    "earn the same on a Visa gift card. Have them name you when they book."
)

REFERRAL = {
    "breadcrumb": [("Home", "/"), ("Extreme Rewards", "")],
    "h1": "Give {X}. Get $250.",
    "h1Highlight": "$250",
    "mirror": "Whatever they save, you earn.",
    # "everything else" is a client-directed change from the MD's approved wording ("any
    # repair or installation"), applied site-wide on 2026-07-31 at the client's instruction:
    # /referral, /specials and /terms all now say it. programs.md keeps the narrower phrasing
    # on purpose as a commercial guard (a diagnostic that doesn't lead to work isn't a
    # repair); "everything else" reads as covering a standalone diagnostic too. The client
    # was told and chose to align. Update programs.md if this becomes the official wording.
    "intro": "Send someone our way and they'll get $250 off a new heating, cooling, or plumbing system, or $100 off everything else. When the job's finished, you earn the same amount on a Visa gift card.",
    "heroChips": [
        "No limit on how many friends you refer",
        "Paid on a Visa gift card",
        "New customers only",
    ],
    "pairs": [
        {"head": "They're getting a new heating, cooling, or plumbing system",
         "they": "$250", "you": "$250"},
        {"head": "Everything else",
         "they": "$100", "you": "$100"},
    ],
    "how": {
        "h2": "Three steps, and only one of them is yours.",
        "steps": [
            {"title": "Tell a friend about us",
             "desc": "Give them our name, and yours. They save $250 on a new heating, cooling, or plumbing system, or $100 on everything else."},
            {"title": "They mention your name when they book",
             "desc": "This is the step that counts. We ask every new customer who sent them, and your name in that answer is what earns your card."},
            {"title": "You earn a Visa gift card once the job is done and paid",
             "desc": "Whatever your friend saved, you earn. We don't pay on the booking. We pay once the work is finished and the invoice is settled, and cards go out within 90 days of that."},
        ],
    },
    # Written to sound like a text someone actually sends, not a brochure. Leads with what
    # the friend gets: programs.md is explicit that a referrer hesitates over an offer that
    # makes them look like they're collecting a commission on a friend.
    "shareMsg": "I use Extreme for heating, cooling, and plumbing. They're local, and they price the work up front before they start. If you call them, mention my name: new customers get $250 off a new system, or $100 off everything else. extremeheating.com",
    "termsLine": 'New customers only. Referral must be named when the job is booked. Reward issued within 90 days of job completion. See full terms at <a href="/terms">extremeheating.com/terms</a>.',
    "plain": [
        ("New customers only.", "We can't have serviced that address in the last 24 months."),
        ("Your name has to be given when the job is booked.", "We can't add it to a job after the fact, so tell your friend to have it ready."),
        ("Your name stays valid for 90 days after it's given.", "That covers you if the job gets scheduled or finished later. It is not extra time to get your name added."),
        ("We issue cards within 90 days of the job being completed and paid.", "The work has to be finished and the invoice settled before a card goes out."),
        ("No referring yourself, and Extreme employees aren't eligible.", "The program is for customers sending us someone new."),
    ],
}


def hero(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{T.X_MARK}" alt=""></div>
  <div class="xsp-hero-grid nocard">
    <div>
      {T.crumbs(d["breadcrumb"])}
      <div class="xsp-eyebrow" style="color:#8FD481;margin-top:14px">EXTREME REWARDS</div>
      {T.h1(d["h1"], d["h1Highlight"])}
      <div class="xrf-mirror-line">{d["mirror"]}</div>
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
    return f'''<div>
  <div class="xsp-eyebrow">THE WHOLE PROGRAM</div>
  <h2 class="xsp-h2">Two numbers, and they match.</h2>
  <div class="xrf-pairs">{cards}</div>
  <div class="xrf-nolimit">If your friend saved $100, you earn $100. There's no limit on how many
  friends you can refer.</div>
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
  <h2 class="xsp-h2">Something to send them.</h2>
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
  <h2 class="xsp-h2">What qualifies.</h2>
  <div class="xrf-terms">
    <div class="xrf-terms-line">{d["termsLine"]}</div>
    <ul class="xrf-plain">{items}</ul>
  </div>
</div>'''


def referral_page(d, root_class):
    body = f'''{hero(d)}
{mechanism()}
<div class="xco-body">
  {pairs(d)}
  <div id="xrf-how">{T.process(d["how"], eyebrow="HOW IT WORKS")}</div>
  {xplan_strip()}
  {share(d)}
  {terms(d)}
</div>'''
    return shell(root_class, body)


def pages(root):
    return [(os.path.join(root, "Other pages", "referral.html"),
             referral_page, REFERRAL, "xsp-referral")]
