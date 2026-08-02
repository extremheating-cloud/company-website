"""Header and footer — rewritten from scratch as single responsive components.

Framer carried three headers and three footers and swapped them per breakpoint, which
is why none of them had a media query. Off Framer that approach breaks: all three
footers use the same `.xf-footer` root class, so loading them together would collide.
These are one of each, with real breakpoints.

Breakpoints match the rest of the site: 1024 and 810.
  >= 1024   full nav with mega-menus
  810-1023  condensed nav, mega-menus still open on hover/focus
  < 810     hamburger, full-screen panel, sticky call bar

Everything comes from site_data.py. No copy or URLs are authored here.
"""
import site_data as D
import template as T
import locations as L

LOGO = f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/assets/brand/logo-white.png"
LOGO_TIGHT = f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/assets/brand/logo-white-tight.png"
X_MARK = f"{T.ASSET_REPO}@{T.ASSET_COMMIT}/assets/brand/x-mark.png"

CSS = """
/* ============================== header ============================== */
.xh-hd{position:sticky;top:0;z-index:900;background:#5E2C7E;color:#fff;
font-family:"Montserrat",ui-sans-serif,system-ui,sans-serif}
.xh-hd *{box-sizing:border-box}
.xh-hd a{text-decoration:none}
/* Colour inheritance is scoped to the purple bar and the mobile panel. Applying it to
   every descendant forced the white dropdown's links to render white-on-lavender. */
.xh-bar a,.xh-panel a,.xh-callbar a{color:inherit}
.xh-bar{max-width:1280px;margin:0 auto;padding:14px 40px;display:flex;align-items:center;
justify-content:space-between;gap:24px}
.xh-logo{display:flex;align-items:center;flex:none}
.xh-logo img{height:44px;width:auto;display:block}

.xh-nav{display:flex;align-items:center;gap:26px;font-weight:600;font-size:14px}
.xh-navitem{position:static}
.xh-hd{position:sticky}
.xh-navbtn{display:inline-flex;align-items:center;gap:6px;background:none;border:0;padding:10px 0;
color:#fff;font:inherit;font-weight:600;cursor:pointer;min-height:44px}
.xh-navbtn .car{font-size:9px;opacity:.6;transition:transform .18s ease}
.xh-navitem[data-open="true"] .xh-navbtn .car{transform:rotate(180deg)}
.xh-nav a.xh-link{display:inline-flex;align-items:center;min-height:44px}
.xh-nav a.xh-link:hover,.xh-navbtn:hover{color:#8FD481}
.xh-nav .is-current{color:#8FD481}

.xh-actions{display:flex;align-items:center;gap:18px;flex:none}
.xh-phone{font-weight:800;font-size:15px;white-space:nowrap}
.xh-phone:hover{color:#8FD481}
.xh-cta{background:#6BB85C;color:#0F172A;font-weight:800;font-size:14px;padding:12px 20px;
border-radius:10px;border:0;cursor:pointer;font-family:inherit;min-height:44px;white-space:nowrap}
.xh-cta:hover{background:#8FD481}

/* ---- mega menu: full-width panel, matching the Framer desktop header ---- */
.xh-navbtn{position:relative}
.xh-navbtn .bar{position:absolute;left:0;right:0;bottom:-14px;height:3px;background:#6BB85C;
transform:scaleX(0);transform-origin:center;transition:transform .15s ease;border-radius:2px}
.xh-navbtn[aria-expanded="true"]{color:#6BB85C;font-weight:800}
.xh-navbtn[aria-expanded="true"] .bar{transform:scaleX(1)}

.xm-scrim{position:fixed;left:0;right:0;bottom:0;background:rgba(15,23,42,.45);z-index:890;display:none}
.xh-hd[data-menu] .xm-scrim{display:block}
.xm-shell{position:absolute;left:0;right:0;top:100%;z-index:900}
.xm-panel{background:#fff;border-top:1px solid #E7E7EA;
box-shadow:0 24px 60px rgba(15,23,42,.22);display:none}
.xh-hd[data-menu="hvac"] .xm-panel[data-menu="hvac"],
.xh-hd[data-menu="plumbing"] .xm-panel[data-menu="plumbing"]{display:block;animation:xmIn .15s ease-out both}
@keyframes xmIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
@media (prefers-reduced-motion:reduce){.xm-panel{animation:none!important}}

.xm-grid{max-width:1280px;margin:0 auto;padding:30px 40px 34px;
display:grid;grid-template-columns:1.1fr 1fr 340px;gap:40px}
.xm-label{font-weight:800;font-size:10.5px;letter-spacing:1.8px;color:#94A3B8;
padding-bottom:12px;border-bottom:1px solid #E7E7EA;margin-bottom:10px}
.xm-row{display:flex;align-items:flex-start;gap:12px;padding:11px 10px;border-radius:10px;
text-decoration:none;transition:background .13s ease}
.xm-row .txt{flex:1;display:flex;flex-direction:column;gap:2px}
.xm-row .t{font-weight:800;font-size:14px;color:#0F172A;display:flex;align-items:center;gap:8px}
.xm-row .d{font-weight:500;font-size:11.5px;color:#475569}
.xm-row .go{opacity:0;color:#6BB85C;font-weight:800;transition:opacity .13s ease}
.xm-row:hover{background:#F4F1F8}
.xm-row:hover .t{color:#5F2980}
.xm-row:hover .go{opacity:1}
.xm-row:focus-visible{outline:2px solid #5F2980;outline-offset:-2px}
.xm-row.slim{padding:10px}
.xm-glyph{position:relative;display:block;width:26px;height:26px;flex:none}
.xm-glyph i{position:absolute;inset:9.5px 2px;border-radius:2px}
.xm-glyph i:first-child{background:#5F2980;transform:rotate(45deg)}
.xm-glyph i:last-child{background:#6BB85C;transform:rotate(-45deg)}
.xm-badge{background:#EEF7EC;color:#4E9B41;font-weight:800;font-size:9.5px;letter-spacing:.6px;
border-radius:5px;padding:3px 7px}
.xm-chips{display:flex;flex-wrap:wrap;gap:6px;padding:2px 10px 8px 46px}
.xm-chip{background:#F4F1F8;color:#5F2980;font-weight:700;font-size:10.5px;border-radius:6px;
padding:5px 9px;text-decoration:none;transition:background .13s ease,color .13s ease}
.xm-chip:hover{background:#5F2980;color:#fff}
.xm-divider{height:1px;background:#E7E7EA;margin:12px 0}
.xm-viewall{display:inline-block;font-weight:800;font-size:13px;color:#5F2980;
text-decoration:none;padding:6px 10px}
.xm-viewall:hover{color:#3F852B}
.xm-aside{display:flex;flex-direction:column;gap:14px}
.xm-promo{border-radius:14px;padding:18px 20px}
.xm-promo.lav{background:#F4F1F8}
.xm-promo.mint{background:#EEF7EC}
.xm-promo .h{font-weight:800;font-size:15px;margin-bottom:6px}
.xm-promo.lav .h{color:#5F2980}
.xm-promo.mint .h{color:#3D7A33}
.xm-promo p{font-weight:500;font-size:12.5px;line-height:1.55;color:#475569;margin:0 0 10px}
.xm-promo a,.xm-promo button{font-weight:800;font-size:13px;color:#5F2980;text-decoration:none;
background:none;border:0;padding:0;cursor:pointer;font-family:inherit}
.xm-promo.mint a,.xm-promo.mint button{color:#3D7A33}
.xm-promo a:hover,.xm-promo button:hover{text-decoration:underline}

/* ---- mobile ---- */
.xh-burger{display:none;background:none;border:0;cursor:pointer;padding:10px;
width:44px;height:44px;align-items:center;justify-content:center}
.xh-burger span{display:block;width:22px;height:2px;background:#fff;position:relative}
.xh-burger span::before,.xh-burger span::after{content:"";position:absolute;left:0;width:22px;
height:2px;background:#fff}
.xh-burger span::before{top:-7px} .xh-burger span::after{top:7px}
.xh-panel{display:none;position:fixed;inset:0;top:0;background:#3A1A4E;z-index:950;
overflow-y:auto;-webkit-overflow-scrolling:touch;padding:0 0 96px}
.xh-panel[data-open="true"]{display:block}
.xh-panel-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;
position:sticky;top:0;background:#3A1A4E}
.xh-close{background:none;border:0;color:#fff;font-size:26px;line-height:1;cursor:pointer;
width:44px;height:44px}
.xh-acc{border-top:1px solid rgba(255,255,255,.12)}
.xh-acc>button{width:100%;display:flex;align-items:center;justify-content:space-between;
background:none;border:0;color:#fff;font:inherit;font-weight:700;font-size:16px;
padding:16px 20px;min-height:56px;cursor:pointer}
.xh-acc>div{display:none;padding:0 20px 12px}
.xh-acc[data-open="true"]>div{display:block}
.xh-acc a{display:block;padding:11px 0;font-size:14.5px;font-weight:600;
color:rgba(255,255,255,.82);border-bottom:1px solid rgba(255,255,255,.08)}
.xh-acc a:last-child{border-bottom:0}
.xh-panel .xh-simple a{display:block;padding:16px 20px;font-weight:700;font-size:16px;color:#fff;
border-top:1px solid rgba(255,255,255,.12)}
.xh-callbar{position:fixed;left:0;right:0;bottom:0;z-index:960;display:none;gap:10px;padding:10px 16px;
background:rgba(58,26,78,.97);backdrop-filter:blur(8px);border-top:1px solid rgba(255,255,255,.14)}
.xh-callbar a,.xh-callbar button{flex:1;display:inline-flex;align-items:center;justify-content:center;
min-height:48px;border-radius:12px;font-weight:800;font-size:15px;border:0;cursor:pointer;
font-family:inherit;text-decoration:none}
.xh-callbar .call{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.28)}
.xh-callbar .sched{background:#6BB85C;color:#0F172A}

@media (max-width:1023px){
  .xh-bar{padding:12px 24px;gap:14px}
  .xh-nav{gap:16px;font-size:13.5px}
  .xh-phone{display:none}
  .xm-grid{grid-template-columns:1fr 1fr;gap:28px;padding:24px 24px 28px}
  .xm-aside{grid-column:1 / -1;flex-direction:row}
  .xm-promo{flex:1}
}
@media (max-width:809px){
  .xh-bar{padding:10px 16px}
  .xh-nav,.xh-actions{display:none}
  .xh-burger{display:flex}
  .xh-logo img{height:38px}
  .xh-callbar{display:flex}
  body{padding-bottom:68px}
}
@media (prefers-reduced-motion:reduce){.xh-hd *{transition:none!important}}

/* ============================== footer ============================== */
.xf{position:relative;background:#3A1A4E;color:#fff;overflow:hidden;
font-family:"Montserrat",ui-sans-serif,system-ui,sans-serif}
.xf *{box-sizing:border-box}
.xf a{color:inherit;text-decoration:none}
.xf-accent{height:4px;background:linear-gradient(90deg,#6BB85C,#5F2980)}
.xf-mark{position:absolute;right:-60px;top:20px;width:340px;opacity:.05;
transform:rotate(-8deg);filter:brightness(0) invert(1);pointer-events:none}
.xf-wrap{position:relative;max-width:1280px;margin:0 auto;padding:0 40px}
.xf-cta{display:flex;align-items:center;justify-content:space-between;gap:24px;
padding:40px 0 34px;border-bottom:1px solid rgba(255,255,255,.14)}
.xf-cta h2{margin:0;font-style:italic;font-weight:900;font-size:26px;letter-spacing:-.5px}
.xf-cta p{margin:8px 0 0;font-size:14px;font-weight:500;color:rgba(255,255,255,.72)}
.xf-cta-btns{display:flex;gap:10px;flex:none}
.xf-btn-green,.xf-btn-outline{display:inline-flex;align-items:center;justify-content:center;
min-height:46px;padding:12px 22px;border-radius:12px;font-weight:800;font-size:14.5px;
border:0;cursor:pointer;font-family:inherit;white-space:nowrap}
.xf-btn-green{background:#6BB85C;color:#0F172A}
.xf-btn-green:hover{background:#8FD481}
.xf-btn-outline{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.4)}
.xf-btn-outline:hover{border-color:#6BB85C;color:#8FD481}
.xf-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:32px;padding:34px 0 30px}
.xf-logo{height:40px;width:auto;display:block}
.xf-blurb{margin:14px 0 0;font-size:13px;line-height:1.6;font-weight:500;color:rgba(255,255,255,.72)}
.xf-247{display:flex;align-items:center;gap:8px;margin-top:14px;font-size:12.5px;font-weight:700}
.xf-247 .dot{width:8px;height:8px;border-radius:50%;background:#6BB85C}
.xf-social{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px}
.xf-social a{font-size:12.5px;font-weight:600;color:rgba(255,255,255,.72);min-height:32px;
display:inline-flex;align-items:center}
.xf-social a:hover{color:#8FD481}
.xf-h{font-size:10.5px;font-weight:800;letter-spacing:1.6px;color:#8FD481;margin-bottom:12px}
.xf-col a{display:block;padding:6px 0;font-size:13.5px;font-weight:600;
color:rgba(255,255,255,.78);min-height:32px}
.xf-col a:hover{color:#fff}
.xf-phone{font-weight:800!important;font-size:16px!important;color:#fff!important}
.xf-meta{font-size:12.5px;color:rgba(255,255,255,.55);margin-top:8px;line-height:1.6}
.xf-areas{padding:22px 0;border-top:1px solid rgba(255,255,255,.12);
font-size:12px;line-height:1.7;color:rgba(255,255,255,.55);display:grid;gap:8px}
.xf-areas b{color:rgba(255,255,255,.8);font-weight:800;letter-spacing:.4px;margin-right:6px}
.xf-areas a{color:rgba(255,255,255,.62);text-decoration:none}
.xf-areas a:hover{color:#8FD481;text-decoration:underline}
.xf-bottom{display:flex;align-items:center;justify-content:space-between;gap:12px;
padding:18px 0 30px;border-top:1px solid rgba(255,255,255,.12);
font-size:12px;color:rgba(255,255,255,.55)}
.xf-bottom .links{display:flex;gap:18px}
.xf-bottom a{min-height:32px;display:inline-flex;align-items:center}
.xf-bottom a:hover{color:#8FD481}

@media (max-width:1023px){
  .xf-wrap{padding:0 24px}
  .xf-grid{grid-template-columns:1.4fr 1fr 1fr;gap:28px}
  .xf-mark{width:240px}
}
@media (max-width:809px){
  .xf-wrap{padding:0 20px}
  .xf-cta{flex-direction:column;align-items:stretch;text-align:left;padding:32px 0 28px}
  .xf-cta h2{font-size:21px}
  .xf-cta-btns{flex-direction:column}
  .xf-btn-green,.xf-btn-outline{width:100%;min-height:48px}
  .xf-grid{grid-template-columns:1fr 1fr;gap:24px 20px;padding:30px 0 26px}
  .xf-brand{grid-column:1 / -1}
  .xf-bottom{flex-direction:column;align-items:flex-start;gap:10px}
  .xf-mark{width:150px;top:12px;right:-24px}
}
@media (max-width:479px){ .xf-grid{grid-template-columns:1fr} }
"""

# ---------------------------------------------------------------- header
# Promo asides, verbatim from the Framer desktop header.
PROMOS = {
    "hvac": [
        ("lav", "Interested in Financing?",
         "Spread out the cost of a new comfort system with flexible payment options that fit "
         "your budget.", "Learn More →", "/financing-options"),
        ("mint", "X-Plan Maintenance Plan",
         "Scheduled tune-ups, priority service, and exclusive member discounts — from "
         "$20.75/mo.", "Explore X-Plan →", "/maintenance"),
    ],
    "plumbing": [
        ("lav", "Need Plumbing Help Fast?",
         "Same-day and emergency plumbing service across Dayton &amp; Cincinnati.",
         "Schedule Service →", None),          # None = opens the schedule dialog
        ("mint", "Plumbing Specials",
         "Current offers and seasonal savings on plumbing services.",
         "View Specials →", "/specials"),
    ],
}

def _core_row(title, desc, href, chips):
    chip_html = ""
    if chips:
        chip_html = ('<div class="xm-chips">' +
                     "".join(f'<a class="xm-chip" href="{h}">{l}</a>' for l, h in chips) +
                     "</div>")
    return f'''<div><a class="xm-row" href="{href}">
        <span class="xm-glyph" aria-hidden="true"><i></i><i></i></span>
        <span class="txt"><span class="t">{title}</span><span class="d">{desc}</span></span>
        <span class="go" aria-hidden="true">→</span>
      </a>{chip_html}</div>'''

def _add_row(title, href, badge):
    b = f'<span class="xm-badge">{badge}</span>' if badge else ""
    return (f'<a class="xm-row slim" href="{href}"><span class="txt">'
            f'<span class="t">{title}{b}</span></span>'
            f'<span class="go" aria-hidden="true">→</span></a>')

def _aside(key):
    out = ""
    for cls, head, body, cta, href in PROMOS[key]:
        action = (f'<a href="{href}">{cta}</a>' if href
                  else f'<button class="js-schedule" type="button">{cta}</button>')
        out += (f'<div class="xm-promo {cls}"><div class="h">{head}</div>'
                f'<p>{body}</p>{action}</div>')
    return f'<div class="xm-aside">{out}</div>'

def _panel(key, core, additional, alt_label, viewall_label, viewall_href):
    return f'''<div class="xm-panel" data-menu="{key}">
      <div class="xm-grid">
        <div>
          <div class="xm-label">CORE SERVICES</div>
          {"".join(_core_row(*r) for r in core)}
        </div>
        <div>
          <div class="xm-label">{alt_label}</div>
          {"".join(_add_row(*r) for r in additional)}
          <div class="xm-divider"></div>
          <a class="xm-viewall" href="{viewall_href}">{viewall_label}</a>
        </div>
        {_aside(key)}
      </div>
    </div>'''

def _nav_item(label, key):
    return f'''<button class="xh-navbtn" type="button" data-menu="{key}"
        aria-expanded="false" aria-haspopup="true">
      {label} <span class="car" aria-hidden="true">▼</span><span class="bar" aria-hidden="true"></span>
    </button>'''

def _panel_acc(label, core, additional):
    links = "".join(f'<a href="{h}">{t}</a>' for t, d, h, c in core)
    links += "".join(f'<a href="{h}">{t}</a>' for t, h, b in additional)
    return f'''<div class="xh-acc">
      <button type="button" aria-expanded="false">{label}<span aria-hidden="true">＋</span></button>
      <div>{links}</div>
    </div>'''

def header(current=""):
    """current is a top-level route ('/locations') so the active item can be marked."""
    def cls(href):
        return ' is-current' if current and current.startswith(href) else ''
    simple = "".join(
        f'<a class="xh-link{cls(h)}" href="{h}">{l}</a>' for l, h in D.NAV_SIMPLE)
    panel_simple = "".join(f'<a href="{h}">{l}</a>' for l, h in D.NAV_SIMPLE)
    return f'''<header class="xh-hd">
  <div class="xh-bar">
    <a class="xh-logo" href="/" aria-label="{D.COMPANY} — home">
      <img src="{LOGO_TIGHT}" alt="{D.COMPANY}">
    </a>
    <nav class="xh-nav" aria-label="Primary">
      {_nav_item("Plumbing", "plumbing")}
      {_nav_item("Heating &amp; Air", "hvac")}
      {simple}
    </nav>
    <div class="xh-actions">
      <a class="xh-phone" href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>
      <button class="xh-cta js-schedule" type="button">Schedule Service</button>
    </div>
    <button class="xh-burger" type="button" aria-label="Open menu" aria-expanded="false">
      <span></span>
    </button>
  </div>
  <div class="xm-scrim" aria-hidden="true"></div>
  <div class="xm-shell">
    {_panel("plumbing", D.PLUMB_CORE, D.PLUMB_ADDITIONAL, "ADDITIONAL SERVICES",
            "View All Plumbing Services →", "/plumbing/services")}
    {_panel("hvac", D.HVAC_CORE, D.HVAC_ADDITIONAL, "X-PLAN &amp; ADDITIONAL SERVICES",
            "View All HVAC Services →", "/services")}
  </div>

  <div class="xh-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="xh-panel-bar">
      <a class="xh-logo" href="/"><img src="{LOGO_TIGHT}" alt="{D.COMPANY}"></a>
      <button class="xh-close" type="button" aria-label="Close menu">×</button>
    </div>
    {_panel_acc("Plumbing", D.PLUMB_CORE, D.PLUMB_ADDITIONAL)}
    {_panel_acc("Heating &amp; Air", D.HVAC_CORE, D.HVAC_ADDITIONAL)}
    <div class="xh-simple">{panel_simple}</div>
  </div>
</header>

<div class="xh-callbar">
  <a class="call" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
  <button class="sched js-schedule" type="button">Schedule</button>
</div>'''

# ---------------------------------------------------------------- footer
def _area_links(items):
    """Service-area towns in the footer link to their own location pages. They are the
    deepest crawlable path into the /locations tree, so leaving them as plain text
    wastes the one place every page links from."""
    return " · ".join(f'<a href="/locations/{slug}">{name}</a>' for slug, name in items)

def footer():
    cols = ""
    for heading, links in D.FOOTER_COLUMNS:
        cols += (f'<div class="xf-col"><div class="xf-h">{heading}</div>' +
                 "".join(f'<a href="{h}">{l}</a>' for l, h in links) + "</div>")
    social = "".join(
        f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in D.SOCIAL)
    return f'''<footer class="xf">
  <div class="xf-accent"></div>
  <img class="xf-mark" src="{X_MARK}" alt="" aria-hidden="true">
  <div class="xf-wrap">
    <div class="xf-cta">
      <div>
        <h2>Need help today? The Extreme Team is ready.</h2>
        <p>24/7 emergency service across Dayton &amp; Cincinnati.</p>
      </div>
      <div class="xf-cta-btns">
        <button class="xf-btn-green js-schedule" type="button">Schedule Service&nbsp;&nbsp;→</button>
        <a class="xf-btn-outline" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
      </div>
    </div>

    <div class="xf-grid">
      <div class="xf-col xf-brand">
        <img class="xf-logo" src="{LOGO}" alt="{D.COMPANY}">
        <p class="xf-blurb">Locally owned &amp; operated, serving the Miami Valley and Greater
        Cincinnati for over 20 years.</p>
        <div class="xf-247"><span class="dot"></span>Available 24/7 · 7 days a week</div>
        <div class="xf-social">{social}</div>
      </div>
      {cols}
      <div class="xf-col">
        <div class="xf-h">CONTACT</div>
        <a class="xf-phone" href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>
        <a class="js-schedule" href="#">Schedule online</a>
        <a href="/contact">Contact us</a>
        <div class="xf-meta">Office staffed Mon–Fri, 8–5<br>Emergencies 24/7</div>
      </div>
    </div>

    <div class="xf-areas">
      <div><b>DAYTON AREA</b>{_area_links(L.DAYTON)}</div>
      <div><b>CINCINNATI AREA</b>{_area_links(L.CINCINNATI)}</div>
      <div><b>COUNTIES</b>{_area_links(L.COUNTIES)}</div>
    </div>

    <div class="xf-bottom">
      <div>&copy; 2026 {D.COMPANY}. All rights reserved. · Licensed &amp; insured in Ohio</div>
      <div class="links">
        <!-- TODO (legal): no privacy policy exists yet, so the link is omitted rather
             than shipped as a 404. This needs writing: the schedule form collects name,
             email, phone and address, and uploads customer photos to Cloudinary, so
             there is real personal data being handled. Add the route, then restore
             <a href="/privacy">Privacy</a> here. -->
        <a href="/terms">Terms</a>
      </div>
    </div>
  </div>
</footer>'''

# ---------------------------------------------------------------- behaviour
JS = """
<script>
(function(){
  var hd = document.querySelector('.xh-hd');
  if (!hd) return;

  /* --- mega menus. State lives on the header root, not the nav item, because the
         panels sit in .xm-shell outside the bar. Nesting them inside the bar meant the
         bar's colour reset reached in and rendered the dropdown's links white on
         white. --- */
  var btns = hd.querySelectorAll('.xh-navbtn');
  function setMenu(key){
    if (key) hd.setAttribute('data-menu', key); else hd.removeAttribute('data-menu');
    btns.forEach(function(b){
      b.setAttribute('aria-expanded', b.dataset.menu === key ? 'true' : 'false');
    });
  }
  function closeAll(){ setMenu(null); }
  btns.forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      setMenu(hd.getAttribute('data-menu') === btn.dataset.menu ? null : btn.dataset.menu);
    });
    btn.addEventListener('mouseenter', function(){
      if (matchMedia('(hover:hover) and (pointer:fine)').matches) setMenu(btn.dataset.menu);
    });
  });
  var shell = hd.querySelector('.xm-shell');
  /* Close on leaving the bar+panel together, so moving the pointer from the button
     down into the panel does not dismiss it. */
  [hd.querySelector('.xh-bar'), shell].forEach(function(el){
    if (!el) return;
    el.addEventListener('mouseleave', function(e){
      if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
      var to = e.relatedTarget;
      if (to && (hd.querySelector('.xh-bar').contains(to) || (shell && shell.contains(to)))) return;
      closeAll();
    });
  });
  document.addEventListener('click', function(e){ if (!hd.contains(e.target)) closeAll(); });
  var scrim = hd.querySelector('.xm-scrim');
  if (scrim) scrim.addEventListener('click', closeAll);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape'){ closeAll(); closePanel(); } });

  /* --- mobile panel --- */
  var panel = hd.querySelector('.xh-panel'),
      burger = hd.querySelector('.xh-burger'),
      closeBtn = hd.querySelector('.xh-close');
  function openPanel(){ panel.dataset.open='true'; burger.setAttribute('aria-expanded','true');
                        document.body.style.overflow='hidden'; }
  function closePanel(){ if(!panel) return; panel.dataset.open='false';
                         burger.setAttribute('aria-expanded','false'); document.body.style.overflow=''; }
  if (burger) burger.addEventListener('click', openPanel);
  if (closeBtn) closeBtn.addEventListener('click', closePanel);
  hd.querySelectorAll('.xh-panel a').forEach(function(a){ a.addEventListener('click', closePanel); });

  hd.querySelectorAll('.xh-acc > button').forEach(function(b){
    b.addEventListener('click', function(){
      var acc = b.parentElement, open = acc.dataset.open === 'true';
      acc.dataset.open = open ? 'false' : 'true';
      b.setAttribute('aria-expanded', open ? 'false' : 'true');
      b.querySelector('span').textContent = open ? '＋' : '−';
    });
  });

  /* --- schedule triggers, header + footer + anywhere on the page --- */
  document.querySelectorAll('.js-schedule').forEach(function(el){
    el.addEventListener('click', function(e){
      e.preventDefault();
      closePanel();
      window.dispatchEvent(new CustomEvent('open-contact-dialog'));
    });
  });
})();
</script>
"""
