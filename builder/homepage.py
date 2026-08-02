"""Homepage — the four Framer components combined into one HTML page.

Ported from framer/homepage/{Hero,AboutFaqReviews,XPlan,Brands}.tsx. Copy is verbatim;
what changed is that the four separate React islands, each with its own <style> block
and its own copy of the theme tokens, are now one document with one stylesheet.

Prices, phone numbers and the review list come from site_data.py and reviews.py, so
the homepage no longer carries its own copies of facts that appear elsewhere.
"""
import site_data as D
import template as T
from reviews import REVIEWS

X_MARK = f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/assets/brand/x-mark.png"
LOGO_WHITE = f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/assets/brand/logo-white.png"
VAN = T.cdn_asset("brand/van.png")

ROTATING = ["Repairs", "Installs", "Tune-Ups", "Plumbing"]

HVAC_SERVICES = [
    ("Cooling", "AC repair, replacement, and tune-ups.", "/air-conditioning"),
    ("Heating", "Furnace repairs, installs, and safety checks.", "/furnace-heating"),
    ("Maintenance Plans", "Bi-annual tune-ups and priority service.", "/maintenance"),
    ("Airflow &amp; Ducts", "Duct cleaning and air balancing.", "/duct-cleaning"),
    ("Heat Pumps", "Year-round efficiency with heat pump systems.", "/heat-pump"),
    ("Indoor Air Quality", "Filtration, UV, and humidity control.", "/indoor-air-quality"),
]
PLUMBING_SERVICES = [
    ("Drain Cleaning", "Fast help for clogged and slow drains.", "/plumbing/clogged-drain"),
    ("Sump Pump", "Protection against basement water issues.", "/plumbing/sump-pump/overview"),
    ("Water Heaters", "Repair and replacement for hot water systems.", "/plumbing/water-heater/overview"),
    ("Leak Detection", "Find and repair hidden plumbing leaks quickly.", "/plumbing/leak-detection"),
    ("Gas Line", "Safe installation and repair for gas piping.", "/plumbing/gas-line/overview"),
    ("Water Treatment", "Filtration and conditioning for cleaner water.", "/plumbing/water-treatment"),
]
FAQS = [
    ("Are your technicians licensed and insured?",
     "Yes. Our HVAC technicians are fully licensed and insured, and receive ongoing training to "
     "deliver safe, high-quality service in every home."),
    ("Do you offer free estimates?",
     "Yes — we provide free estimates for system replacements, new installations, and major repair projects."),
    ("Do you offer financing options?",
     "We partner with trusted lenders to offer convenient monthly payment options on qualifying "
     "equipment and repair work."),
    ("Which areas do you serve?",
     "Extreme Heating, Air, Plumbing serves homeowners across Dayton, Cincinnati, Troy, Tipp City, "
     "and surrounding Miami Valley communities."),
]
BRANDS = [("Trane", "trane.png"), ("Ruud", "ruud.png"), ("Daikin", "daikin.png")]

CSS = """
/* ================================ hero ================================ */
.hp-hero{position:relative;padding-bottom:0;background:linear-gradient(150deg,#5E2C7E 0%,#542770 45%,#3A1A4E 100%);
color:#fff;overflow:hidden}
.hp-hero-mark{position:absolute;right:-90px;top:-40px;width:620px;opacity:.06;
transform:rotate(-8deg);filter:brightness(0) invert(1);pointer-events:none}
.hp-wrap{position:relative;max-width:1280px;margin:0 auto;padding:0 40px}
.hp-hero-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:24px;align-items:end;
padding:56px 0 0}
/* The slash is decorative and bleeds left out of the van column. Copy sits above
   it unconditionally so a wider van can never cut into the text. */
.hp-hero-in{padding:0 0 64px;max-width:640px;position:relative;z-index:2}

/* Van column. The slash is a rotated + skewed bar behind the van — the same geometry
   the Framer hero used, expressed as percentages so it tracks the column at any width. */
.hp-van-col{position:relative;width:100%;align-self:end;min-height:0;
aspect-ratio:569 / 430;max-height:560px}
.hp-slash{position:absolute;left:-4%;right:-16%;bottom:20%;height:13.3%;
background:#6BB85C;transform:rotate(-9deg) skewX(-16deg);box-shadow:0 20px 60px rgba(0,0,0,.3)}
.hp-slash-w{position:absolute;left:1%;right:-23%;bottom:17.5%;height:3.75%;
background:#fff;opacity:.25;transform:rotate(-9deg) skewX(-16deg)}
/* Bleeds past the column edge on purpose — the hero is overflow:hidden, so the
   van reads as driving out of frame rather than sitting in a box. */
.hp-van{position:absolute;left:50%;bottom:20%;transform:translateX(-50%);
width:126%;max-width:none;filter:drop-shadow(0 26px 34px rgba(0,0,0,.38))}
/* Mobile stage: van sits under the copy instead of beside it. */
.hp-van-stage{display:none;position:relative;aspect-ratio:350 / 210;margin-top:22px}
.hp-van-stage .hp-slash{left:-11.4%;right:-11.4%;bottom:25.7%;height:19%}
.hp-van-stage .hp-van{bottom:26.7%;transform:translateX(-50%);width:100%;max-width:none;
filter:drop-shadow(0 16px 20px rgba(0,0,0,.35))}
.hp-badge{display:inline-flex;align-items:center;gap:9px;border:1px solid rgba(255,255,255,.3);
background:rgba(255,255,255,.1);border-radius:999px;padding:8px 15px;font-size:11.5px;
font-weight:800;letter-spacing:1.4px}
.hp-badge .dot{width:7px;height:7px;border-radius:50%;background:#6BB85C}
.hp-h1{margin:20px 0 0;font-style:italic;font-weight:900;font-size:clamp(34px,5.4vw,54px);
line-height:1.06;letter-spacing:-1.2px}
.hp-roll{display:inline-block;height:1.06em;overflow:hidden;vertical-align:bottom}
.hp-roll ul{list-style:none;margin:0;padding:0;animation:hp-roll 9s infinite}
.hp-roll li{height:1.06em;color:#6BB85C}
@keyframes hp-roll{0%,18%{transform:translateY(0)}25%,43%{transform:translateY(-1.06em)}
50%,68%{transform:translateY(-2.12em)}75%,93%{transform:translateY(-3.18em)}100%{transform:translateY(-4.24em)}}
@media (prefers-reduced-motion:reduce){.hp-roll ul{animation:none}}
.hp-lede{margin:18px 0 0;max-width:560px;font-size:16px;line-height:1.65;font-weight:500;
color:rgba(255,255,255,.84)}
.hp-cta-row{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.hp-btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;
padding:13px 24px;border-radius:12px;font-weight:800;font-size:15px;border:0;cursor:pointer;
font-family:inherit;text-decoration:none;white-space:nowrap}
.hp-btn-green{background:#6BB85C;color:#0F172A;box-shadow:0 8px 24px rgba(107,184,92,.32)}
.hp-btn-green:hover{background:#8FD481}
.hp-btn-ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.45)}
.hp-btn-ghost:hover{border-color:#6BB85C;color:#8FD481}
.hp-trust{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:26px;font-size:13px;font-weight:700;
color:rgba(255,255,255,.8)}
.hp-trust .st{color:#F6A723;letter-spacing:1px}
.hp-promise{background:#0F172A;color:#fff}
.hp-promise-in{max-width:1280px;margin:0 auto;padding:16px 40px;display:flex;align-items:center;
gap:12px 30px;flex-wrap:wrap}
.hp-promise .lab{font-size:11px;font-weight:800;letter-spacing:1.8px;color:rgba(255,255,255,.45)}
.hp-promise .item{font-size:13.5px;font-weight:600;color:rgba(255,255,255,.85)}

/* ============================== sections ============================== */
.hp-sec{padding:64px 0}
.hp-sec.alt{background:#F7F6FA}
.hp-eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:#5F2980}
.hp-h2{margin:10px 0 0;font-style:italic;font-weight:900;font-size:clamp(24px,3.4vw,32px);
letter-spacing:-.7px;color:#0F172A}
.hp-sub{margin:12px 0 0;max-width:62ch;font-size:15px;line-height:1.65;font-weight:500;color:#475569}
.hp-head-row{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.hp-more{font-weight:800;font-size:14px;color:#5F2980;text-decoration:none;white-space:nowrap;
min-height:44px;display:inline-flex;align-items:center}
.hp-more:hover{color:#3F852B}
.hp-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.hp-card{display:block;border:1px solid #E7E7EA;border-radius:16px;padding:20px;background:#fff;
text-decoration:none;transition:box-shadow .15s ease,transform .15s ease}
.hp-card:hover{box-shadow:0 12px 30px rgba(84,39,112,.12);transform:translateY(-2px)}
.hp-card .t{font-weight:800;font-size:16.5px;color:#0F172A}
.hp-card .d{font-size:13.5px;line-height:1.55;font-weight:500;color:#475569;margin-top:6px}
.hp-card .lm{display:inline-block;margin-top:14px;font-weight:800;font-size:13.5px;color:#5F2980}
.hp-x{display:inline-block;position:relative;width:26px;height:26px}
.hp-x i{position:absolute;inset:9.5px 2px;border-radius:2px}
.hp-x i:first-child{background:#5F2980;transform:rotate(45deg)}
.hp-x i:last-child{background:#6BB85C;transform:rotate(-45deg)}

/* ================================ about ================================ */
.hp-about{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:center}
.hp-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:26px}
.hp-stats .n{font-style:italic;font-weight:900;font-size:28px;color:#5F2980}
.hp-stats .l{font-size:12.5px;font-weight:600;color:#475569;margin-top:2px}
.hp-video{position:relative;border-radius:18px;overflow:hidden;background:#0F172A;aspect-ratio:16/10}
.hp-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}

/* ================================= faq ================================= */
.hp-faq{border-top:1px solid #E7E7EA;margin-top:26px}
.hp-faq details{border-bottom:1px solid #E7E7EA}
.hp-faq summary{list-style:none;cursor:pointer;padding:18px 0;font-weight:700;font-size:15.5px;
color:#0F172A;display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px}
.hp-faq summary::-webkit-details-marker{display:none}
.hp-faq summary::after{content:"＋";color:#5F2980;font-weight:800;flex:none}
.hp-faq details[open] summary::after{content:"−"}
.hp-faq p{margin:0 0 18px;font-size:14.5px;line-height:1.7;font-weight:500;color:#475569;max-width:70ch}

/* =============================== reviews =============================== */
.hp-revs{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}
.hp-rev{border:1px solid #E7E7EA;border-radius:16px;padding:20px;background:#fff}
.hp-rev .stars{color:#F6A723;font-size:14px;letter-spacing:2px}
.hp-rev .q{font-size:14px;line-height:1.6;font-weight:500;color:#475569;margin-top:10px}
.hp-rev .who{font-size:12.5px;font-weight:700;color:#0F172A;margin-top:14px}
.hp-rev .who span{color:#94A3B8;font-weight:600}

/* =============================== x-plan =============================== */
.hp-xp{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;
padding:38px 40px;color:#fff;position:relative;overflow:hidden}
.hp-xp-mark{position:absolute;right:-40px;bottom:-40px;width:260px;opacity:.06;
transform:rotate(-8deg);filter:brightness(0) invert(1)}
.hp-xp-grid{position:relative;display:grid;grid-template-columns:1.15fr .85fr;gap:36px;align-items:center}
.hp-xp .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:#8FD481}
.hp-xp h2{margin:10px 0 0;font-style:italic;font-weight:900;font-size:28px;letter-spacing:-.6px}
.hp-zri{border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.08);
border-radius:14px;padding:16px 18px;margin-top:18px}
.hp-zri .lab{font-size:10.5px;font-weight:800;letter-spacing:1.6px;color:#8FD481}
.hp-zri p{margin:6px 0 0;font-size:13.5px;line-height:1.6;font-weight:500;color:rgba(255,255,255,.88)}
.hp-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.hp-chip{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);border-radius:999px;
padding:8px 14px;font-size:12.5px;font-weight:700}
.hp-price{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-top:22px}
.hp-price .amt{font-style:italic;font-weight:900;font-size:34px;letter-spacing:-.6px}
.hp-price .per{font-size:15px;font-weight:700}
.hp-price .alt{font-size:13.5px;font-weight:700;color:rgba(255,255,255,.75)}
.hp-inc{background:#fff;border-radius:16px;padding:24px;color:#0F172A}
.hp-inc .lab{font-size:11.5px;font-weight:800;letter-spacing:2px;color:#5F2980;margin-bottom:14px}
.hp-inc ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.hp-inc li{display:flex;gap:9px;font-size:13.5px;font-weight:600;color:#475569;line-height:1.45}
.hp-inc .c{width:18px;height:18px;flex:none;border-radius:50%;background:#3F852B;color:#fff;
font-size:10px;font-weight:800;display:grid;place-items:center}

/* =============================== brands =============================== */
.hp-brands{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;max-width:880px;
margin:30px auto 0;align-items:center}
.hp-brand{display:flex;align-items:center;justify-content:center;min-height:88px}
.hp-brand img{max-width:200px;width:100%;height:52px;object-fit:contain;display:block;
filter:grayscale(1) opacity(.55);transition:filter .22s ease,transform .22s ease}
@media (hover:hover) and (pointer:fine){.hp-brand img:hover{filter:none;transform:scale(1.03)}}
@media (hover:none){.hp-brand img{filter:none}}

/* ============================= responsive ============================= */
@media (max-width:1023px){
  .hp-wrap{padding:0 24px}
  .hp-cards,.hp-revs{grid-template-columns:1fr 1fr}
  .hp-hero-grid{grid-template-columns:1fr .95fr;gap:18px}
  .hp-van{width:112%}
  .hp-about{grid-template-columns:1fr;gap:28px}
  .hp-xp-grid{grid-template-columns:1fr;gap:26px}
  .hp-promise-in{padding:14px 24px}
}
@media (max-width:809px){
  .hp-wrap{padding:0 20px}
  .hp-hero-grid{grid-template-columns:1fr;gap:0;padding:38px 0 0}
  .hp-hero-in{padding:0 0 8px;max-width:none}
  .hp-van-col{display:none}
  .hp-van-stage{display:block}
  .hp-sec{padding:44px 0}
  .hp-cards,.hp-revs,.hp-brands{grid-template-columns:1fr;gap:12px}
  .hp-stats{grid-template-columns:1fr 1fr;gap:16px}
  .hp-cta-row{flex-direction:column;align-items:stretch}
  .hp-btn{width:100%}
  .hp-xp{padding:26px 22px;border-radius:20px}
  .hp-head-row{flex-direction:column;align-items:flex-start;gap:10px}
  .hp-brand img{height:38px;max-width:150px}
  .hp-promise-in{padding:14px 20px;gap:8px 18px}
}
"""

def _cards(items):
    return "".join(
        f'''<a class="hp-card" href="{href}">
      <span class="hp-x" aria-hidden="true"><i></i><i></i></span>
      <div class="t">{t}</div><div class="d">{d}</div>
      <span class="lm">Learn more →</span></a>''' for t, d, href in items)

def homepage():
    roll = "".join(f"<li>{w}</li>" for w in ROTATING + [ROTATING[0]])
    stats = "".join(f'<div><div class="n">{n}</div><div class="l">{l}</div></div>'
                    for n, l in D.STATS)
    faqs = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
    revs = "".join(
        f'<div class="hp-rev"><div class="stars">★★★★★</div><div class="q">“{q}”</div>'
        f'<div class="who">{who}{f" <span>· {c}</span>" if c else ""}</div></div>'
        for q, who, c in REVIEWS[:3])
    perks = "".join(f'<span class="hp-chip">{p}</span>' for p in D.XPLAN["perks"])
    inc = "".join(f'<li><span class="c">✓</span><span>{i}</span></li>'
                  for i in D.XPLAN["includes"])
    brands = "".join(
        f'<div class="hp-brand"><img src="{T.cdn_asset("brands/"+f)}" alt="{n}" '
        f'loading="lazy" decoding="async"></div>' for n, f in BRANDS)

    return f'''<style>{CSS}</style>

<section class="hp-hero">
  <img class="hp-hero-mark" src="{X_MARK}" alt="" aria-hidden="true">
  <div class="hp-wrap"><div class="hp-hero-grid"><div class="hp-hero-in">
    <span class="hp-badge"><span class="dot"></span>LOCALLY OWNED · DAYTON + CINCINNATI</span>
    <h1 class="hp-h1">Trusted Team<br>for
      <span class="hp-roll"><ul>{roll}</ul></span>
    </h1>
    <p class="hp-lede">Fast repairs, full system replacements, routine maintenance, and dependable
    plumbing help — delivered by a team your neighbors already trust.</p>
    <div class="hp-cta-row">
      <button class="hp-btn hp-btn-green js-schedule" type="button">Schedule Service&nbsp;&nbsp;→</button>
      <a class="hp-btn hp-btn-ghost" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
    </div>
    <div class="hp-trust">
      <span><span class="st">★★★★★</span> {D.GOOGLE_RATING} on Google</span>
      <span>◆ {D.YEARS_LOCAL} Years Locally Owned</span>
      <span>◆ 24/7 Emergency</span>
    </div>

    <div class="hp-van-stage" aria-hidden="true">
      <div class="hp-slash"></div>
      <img class="hp-van" src="{VAN}" alt="">
    </div>
  </div>

  <div class="hp-van-col">
    <div class="hp-slash" aria-hidden="true"></div>
    <div class="hp-slash-w" aria-hidden="true"></div>
    <img class="hp-van" src="{VAN}" alt="Extreme service van">
  </div>
  </div></div>
</section>

<div class="hp-promise"><div class="hp-promise-in">
  <span class="lab">THE EXTREME PROMISE</span>
  <span class="item">◆ Licensed &amp; Insured</span>
  <span class="item">◆ Free Replacement Estimates</span>
  <span class="item">◆ Financing Available</span>
  <span class="item">◆ X-Plan from {D.XPLAN["monthly"]}/mo</span>
</div></div>

<section class="hp-sec"><div class="hp-wrap">
  <div class="hp-head-row">
    <div>
      <div class="hp-eyebrow">OUR HVAC SERVICES</div>
      <h2 class="hp-h2">Comfort solutions for every season of the year.</h2>
      <p class="hp-sub">Explore our major heating, cooling, air quality, and maintenance services
      designed to keep your home comfortable year-round.</p>
    </div>
    <a class="hp-more" href="/services">View All HVAC Services →</a>
  </div>
  <div class="hp-cards">{_cards(HVAC_SERVICES)}</div>
</div></section>

<section class="hp-sec alt"><div class="hp-wrap">
  <div class="hp-head-row">
    <div>
      <div class="hp-eyebrow">OUR PLUMBING SERVICES</div>
      <h2 class="hp-h2">Reliable help for your home plumbing systems.</h2>
      <p class="hp-sub">Explore our major drain, water heater, and leak detection services designed
      to keep your home's plumbing running reliably.</p>
    </div>
    <a class="hp-more" href="/plumbing/services">View All Plumbing Services →</a>
  </div>
  <div class="hp-cards">{_cards(PLUMBING_SERVICES)}</div>
</div></section>

<section class="hp-sec"><div class="hp-wrap">
  <div class="hp-about">
    <div>
      <div class="hp-eyebrow">ABOUT EXTREME</div>
      <h2 class="hp-h2">{D.TAGLINE}</h2>
      <p class="hp-sub">For over two decades, the Extreme Team has helped homeowners across Dayton,
      Cincinnati, and the Miami Valley stay comfortable in every season. From emergency repairs to
      full system replacements, we're known for honest recommendations, precise workmanship, and
      friendly, no-pressure service.</p>
      <div class="hp-stats">{stats}</div>
      <div class="hp-cta-row"><a class="hp-btn hp-btn-green" href="/about">About Us&nbsp;&nbsp;→</a></div>
    </div>
    <div class="hp-video">
      <iframe src="https://www.youtube.com/embed/lUjB1pt9yBw?rel=0&amp;modestbranding=1"
        title="Meet the Extreme Team" loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>
    </div>
  </div>
</div></section>

<section class="hp-sec alt"><div class="hp-wrap">
  <div class="hp-eyebrow">EQUIPMENT WE INSTALL</div>
  <h2 class="hp-h2">The brands we stand behind.</h2>
  <p class="hp-sub">We install and service Trane, Ruud, and Daikin systems — and we repair every
  major brand, whoever put it in.</p>
  <div class="hp-brands">{brands}</div>
</div></section>

<section class="hp-sec"><div class="hp-wrap">
  <div class="hp-xp">
    <img class="hp-xp-mark" src="{LOGO_WHITE}" alt="" aria-hidden="true">
    <div class="hp-xp-grid">
      <div>
        <div class="eyebrow">X-PLAN MEMBERSHIP</div>
        <h2>The smart way to protect your home's comfort &amp; savings.</h2>
        <div class="hp-zri">
          <div class="lab">ZERO RISK INVESTMENT</div>
          <p>{D.XPLAN["zeroRisk"]}</p>
        </div>
        <div class="hp-chips">{perks}</div>
        <div class="hp-price">
          <span class="amt">{D.XPLAN["annual"]}<span class="per">/year</span></span>
          <span class="alt">or {D.XPLAN["monthly"]}/month {D.XPLAN["monthlyNote"]}</span>
        </div>
        <div class="hp-cta-row">
          <button class="hp-btn hp-btn-green js-schedule" type="button">Join X-Plan&nbsp;&nbsp;→</button>
        </div>
      </div>
      <div class="hp-inc">
        <div class="lab">WHAT'S INCLUDED</div>
        <ul>{inc}</ul>
      </div>
    </div>
  </div>
</div></section>

<section class="hp-sec alt"><div class="hp-wrap">
  <div class="hp-eyebrow">CUSTOMER REVIEWS</div>
  <h2 class="hp-h2">See what homeowners say about the Extreme Team.</h2>
  <p class="hp-sub">Real feedback from families across Dayton, Cincinnati, and the Miami Valley —
  pulled directly from our Google Reviews.</p>
  <div class="hp-revs">{revs}</div>
</div></section>

<section class="hp-sec"><div class="hp-wrap">
  <div class="hp-faq">
    <div class="hp-eyebrow">FAQ</div>
    <h2 class="hp-h2">Your questions, answered.</h2>
    <p class="hp-sub">Answers to the most common questions our customers ask. If you don't see what
    you're looking for, our team is always happy to help.</p>
    {faqs}
  </div>
</div></section>
'''

META = {
    "url": "/",
    "title": f"HVAC &amp; Plumbing in Dayton &amp; Cincinnati | {D.COMPANY}",
    "description": ("Trusted heating, cooling and plumbing across Dayton and Cincinnati. "
                    "Same-day service in most cases, upfront pricing, 24/7 emergency line."),
    "nav": "",
}
