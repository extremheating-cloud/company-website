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
/* Color inheritance is scoped to the purple bar and the mobile panel. Applying it to
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
/* NEW rides above the label, centred on it. The button is 44px tall for the tap
   target while the text is ~17px, so the chip sits in space the row already had. */
.xh-navbtn.has-new{position:relative}
.xh-navbtn .xh-new{position:absolute;left:50%;top:2px;transform:translateX(-50%);
background:#6BB85C;color:#0F172A;font-size:8.5px;font-weight:800;letter-spacing:1px;
line-height:1;border-radius:4px;padding:3px 5px;white-space:nowrap}
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

/* ---- mobile: bar trigger + full-screen panel, matching the Framer mobile header ---- */
.xh-burger{display:none;width:44px;height:44px;border:1.5px solid rgba(255,255,255,.4);
border-radius:12px;background:transparent;cursor:pointer;align-items:center;justify-content:center}
.xh-burger span{display:block;width:18px;height:2px;background:#fff;
box-shadow:0 5px 0 #fff,0 -5px 0 #fff}
.xh-burger:active{transform:scale(.96)}

.xh-panel{display:none;position:fixed;inset:0;z-index:950;flex-direction:column;
background:linear-gradient(160deg,#5E2C7E 0%,#542770 45%,#3A1A4E 100%);color:#fff}
.xh-panel[data-open="true"]{display:flex}
.xh-panel-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;
border-bottom:1px solid rgba(255,255,255,.12);flex:none}
.xh-panel-bar .xh-logo img{width:min(52vw,200px);height:auto;margin:3px 0 0 -6px}
.xh-close{width:44px;height:44px;border:1.5px solid rgba(255,255,255,.45);border-radius:11px;
background:transparent;color:#fff;font-size:16px;cursor:pointer;display:grid;place-items:center}
.xh-close:active{transform:scale(.96)}
.xh-scroll{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:4px 20px 16px}

/* Rows are large italic display type, one per line with a rule beneath. */
.xh-acc>button,.xh-simple a{width:100%;display:flex;align-items:center;
justify-content:space-between;gap:10px;padding:16px 2px;min-height:44px;background:none;
border:0;border-bottom:1px solid rgba(255,255,255,.12);cursor:pointer;text-align:left;
font-style:italic;font-weight:900;font-size:19px;color:#fff;font-family:inherit;
text-decoration:none}
.xh-acc>button:focus-visible,.xh-simple a:focus-visible{outline:2px solid #fff;outline-offset:-2px}
.xh-caret{font-style:normal;font-size:13px;color:rgba(255,255,255,.55)}
.xh-acc[data-open="true"] .xh-caret{color:#6BB85C}
.xh-save{display:inline-block;margin-left:10px;vertical-align:middle;background:#6BB85C;
color:#0F172A;font-style:normal;font-weight:800;font-size:9.5px;letter-spacing:1px;
border-radius:5px;padding:3px 7px}

/* Expanded content sits in an inset card, two columns, green section labels. */
.xh-acc>div{display:none}
.xh-acc[data-open="true"]>div{display:block;margin:12px 0 16px;
background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);
border-radius:14px;padding:16px 16px 14px}
.xh-mini{font-weight:800;font-size:9.5px;letter-spacing:1.6px;color:#8FD481;margin:0 0 8px}
.xh-mini + .xh-grid + .xh-mini{margin-top:14px}
.xh-grid{display:grid;grid-template-columns:1fr 1fr;gap:2px 12px;margin-bottom:12px}
.xh-grid a{display:flex;align-items:center;min-height:40px;padding:4px 2px;
font-weight:600;font-size:13px;color:rgba(255,255,255,.92);text-decoration:none;
border-bottom:0}
.xh-grid a:active{color:#8FD481}
.xh-all{display:inline-block;font-weight:800;font-size:13px;color:#8FD481;
text-decoration:none;padding:6px 2px;min-height:32px}

/* Pinned actions at the foot of the panel. */
.xh-pinned{flex:none;background:rgba(15,23,42,.25);border-top:1px solid rgba(255,255,255,.12);
padding:14px 20px calc(14px + env(safe-area-inset-bottom));display:grid;gap:10px}
.xh-pinned .cta{width:100%;min-height:48px;border:0;border-radius:12px;cursor:pointer;
background:#6BB85C;color:#0F172A;font-weight:800;font-size:15.5px;font-family:inherit}
.xh-pinned .call{width:100%;min-height:48px;display:flex;align-items:center;
justify-content:center;border:1.5px solid rgba(255,255,255,.45);border-radius:12px;
color:#fff;font-weight:800;font-size:15px;text-decoration:none}
.xh-pinned .trust{display:flex;align-items:center;justify-content:center;gap:8px;
font-weight:700;font-size:12px;color:rgba(255,255,255,.82)}
.xh-pinned .trust .s{color:#F6A723;letter-spacing:1px}

.xh-callbar{position:fixed;left:0;right:0;bottom:0;z-index:940;display:none;gap:10px;
padding:10px 16px calc(10px + env(safe-area-inset-bottom));
background:rgba(58,26,78,.97);backdrop-filter:blur(8px);border-top:1px solid rgba(255,255,255,.14)}
/* nowrap is load-bearing, not cosmetic. flex:1 was splitting the bar down the middle,
   which on a 320px screen is 139px a side — enough for "Schedule Online" (needs 102)
   but not for "Call (844) 584-7399" (needs 154), so the phone number wrapped onto a
   second line. With nowrap the flex items' default min-width:auto floors each button
   at its content width, so Call takes its 154 and Schedule gives up the slack it was
   never using. Measured, not guessed. */
.xh-callbar a,.xh-callbar button{flex:1;display:inline-flex;align-items:center;
justify-content:center;min-height:48px;border-radius:12px;font-weight:800;font-size:15px;
border:0;cursor:pointer;font-family:inherit;text-decoration:none;white-space:nowrap}
.xh-callbar .call{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.28)}
.xh-callbar .sched{background:#6BB85C;color:#0F172A}
/* Set by the header script while the mobile menu is open; the panel has its own
   pinned Schedule/Call pair and the bar was landing on top of it. */
.xh-menu-open .xh-callbar{display:none}

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
/* Narrowest phones still in use (iPhone SE, 320px). Measured there: the two labels
   need 154 + 114 = 268px of content, and the default 32px of bar padding plus a 10px
   gap leaves 278 — it fits, but by ten pixels, which is not a margin. Tightening the
   chrome rather than shrinking the type keeps both buttons at their 48px tap target
   and the number at full size, which is the one thing on screen someone is trying to
   read when the heat is out. */
@media (max-width:359px){
  .xh-callbar{padding-left:12px;padding-right:12px;gap:8px}
  .xh-callbar a,.xh-callbar button{font-size:14.5px}
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
.xf-grid{display:grid;grid-template-columns:1.7fr 1fr 1fr 1fr 1fr;gap:32px;padding:34px 0 30px}
/* The tight file, not logo-white.png: that one is 55% transparent padding, so a
   76px box only ever drew a 34px logo. Same box, nearly twice the mark. */
.xf-logo{height:64px;width:auto;display:block}
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
/* The sitewide NAP. `address` because that is what it is; font-style reset because
   the element italicises by default and the rest of the column does not. */
.xf-nap{font-style:normal;font-size:13.5px;font-weight:600;line-height:1.6;
color:rgba(255,255,255,.78);margin:0 0 8px}
.xf-nap b{display:block;color:#fff;font-weight:800;margin-bottom:2px}
.xf-meta{font-size:12.5px;color:rgba(255,255,255,.55);margin-top:8px;line-height:1.6}
.xf-areas{padding:22px 0;border-top:1px solid rgba(255,255,255,.12);
font-size:12px;line-height:1.7;color:rgba(255,255,255,.55);display:grid;gap:8px}
.xf-areas b{color:rgba(255,255,255,.8);font-weight:800;letter-spacing:.4px;margin-right:6px}
.xf-areas a{color:rgba(255,255,255,.62);text-decoration:none}
.xf-areas a:hover{color:#8FD481;text-decoration:underline}
/* The office row is the one line in this band that points at premises rather than at
   service areas, so it reads a step brighter than the towns beneath it. */
.xf-offices a{color:rgba(255,255,255,.85);font-weight:700}
.xf-bottom{display:flex;align-items:center;justify-content:space-between;gap:12px;
padding:18px 0 30px;border-top:1px solid rgba(255,255,255,.12);
font-size:12px;color:rgba(255,255,255,.55)}
.xf-bottom .links{display:flex;gap:18px}
.xf-bottom a{min-height:32px;display:inline-flex;align-items:center}
.xf-bottom a:hover{color:#8FD481}

@media (max-width:1023px){
  .xf-wrap{padding:0 24px}
  .xf-grid{grid-template-columns:1.4fr 1fr 1fr;gap:28px}
  .xf-logo{height:56px}
  .xf-mark{width:240px}
}
@media (max-width:809px){
  .xf-wrap{padding:0 20px}
  .xf-cta{flex-direction:column;align-items:stretch;text-align:left;padding:32px 0 28px}
  .xf-cta h2{font-size:21px}
  .xf-cta-btns{flex-direction:column}
  .xf-btn-green,.xf-btn-outline{width:100%;min-height:48px}
  .xf-grid{grid-template-columns:1fr 1fr;gap:24px 20px;padding:30px 0 26px}
  .xf-logo{height:50px}
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
        ("lav", "Want to spread out the cost?",
         "You can pay for a new system monthly instead of all at once. See what you qualify "
         "for before you decide anything.", "See payment options →", "/financing-options"),
        ("mint", "X-Plan Maintenance Plan",
         "Your tune-ups get scheduled for you, and when something breaks you jump the line. "
         "Members pay less on the work too. $20.75 a month.",
         "See what's included →", "/maintenance"),
    ],
    "plumbing": [
        ("lav", "Need a plumber today?",
         "Burst pipe or a drain backing up? We come out same day across Dayton and "
         "Cincinnati, and we answer the emergency line at night.",
         "Schedule Service →", None),          # None = opens the schedule dialog
        ("mint", "Plumbing Specials",
         "What we have running on plumbing work right now. Worth a look before you book.",
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

def _nav_item(label, key, badge=""):
    """badge rides above the label rather than beside it — the nav bar has room in
    the button's top padding, and a chip on the baseline would push the row's
    spacing around."""
    tag = f'<span class="xh-new">{badge}</span>' if badge else ""
    return f'''<button class="xh-navbtn{" has-new" if badge else ""}" type="button" data-menu="{key}"
        aria-expanded="false" aria-haspopup="true">
      {tag}{label} <span class="car" aria-hidden="true">▼</span><span class="bar" aria-hidden="true"></span>
    </button>'''

def _panel_acc(label, core, additional, all_label, all_href, badge=""):
    core_links = "".join(f'<a href="{h}">{t}</a>' for t, d, h, c in core)
    add_links = "".join(f'<a href="{h}">{t}</a>' for t, h, b in additional)
    # Inline here, not stacked as on desktop: these rows are full-width and the chip
    # sits naturally after the label, the same way SAVE does on Specials.
    tag = f'<span class="xh-save">{badge}</span>' if badge else ""
    return f'''<div class="xh-acc">
      <button type="button" aria-expanded="false">
        <span>{label}{tag}</span><span class="xh-caret" aria-hidden="true">▼</span>
      </button>
      <div>
        <p class="xh-mini">CORE SERVICES</p>
        <div class="xh-grid">{core_links}</div>
        <p class="xh-mini">ADDITIONAL</p>
        <div class="xh-grid">{add_links}</div>
        <a class="xh-all" href="{all_href}">{all_label} →</a>
      </div>
    </div>'''

def header(current=""):
    """current is a top-level route ('/locations') so the active item can be marked."""
    def cls(href):
        return ' is-current' if current and current.startswith(href) else ''
    simple = "".join(
        f'<a class="xh-link{cls(h)}" href="{h}">{l}</a>' for l, h in D.NAV_SIMPLE)
    # Specials carries a SAVE badge in the mobile panel.
    panel_simple = "".join(
        f'<a href="{h}"><span>{l}'
        f'{"<span class=\'xh-save\'>SAVE</span>" if l == "Specials" else ""}</span></a>'
        for l, h in D.NAV_SIMPLE)
    return f'''<header class="xh-hd">
  <div class="xh-bar">
    <a class="xh-logo" href="/" aria-label="{D.COMPANY} — home">
      <img src="{LOGO_TIGHT}" alt="{D.COMPANY}"{T.dim_attrs(LOGO_TIGHT)}>
    </a>
    <nav class="xh-nav" aria-label="Primary">
      {_nav_item("Heating &amp; Air", "hvac")}
      {_nav_item("Plumbing", "plumbing", badge="NEW")}
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
    {_panel("hvac", D.HVAC_CORE, D.HVAC_ADDITIONAL, "X-PLAN &amp; ADDITIONAL SERVICES",
            "View All HVAC Services →", "/services")}
    {_panel("plumbing", D.PLUMB_CORE, D.PLUMB_ADDITIONAL, "ADDITIONAL SERVICES",
            "View All Plumbing Services →", "/plumbing/services")}
  </div>

  <div class="xh-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="xh-panel-bar">
      <a class="xh-logo" href="/"><img src="{LOGO_TIGHT}" alt="{D.COMPANY}"{T.dim_attrs(LOGO_TIGHT)}></a>
      <button class="xh-close" type="button" aria-label="Close menu">×</button>
    </div>
    <div class="xh-scroll">
      {_panel_acc("Heating &amp; Air", D.HVAC_CORE, D.HVAC_ADDITIONAL,
                  "All HVAC Services", "/services")}
      {_panel_acc("Plumbing", D.PLUMB_CORE, D.PLUMB_ADDITIONAL,
                  "All Plumbing Services", "/plumbing/services", badge="NEW")}
      <div class="xh-simple">{panel_simple}</div>
    </div>
    <div class="xh-pinned">
      <button class="cta js-schedule" type="button">Schedule Service</button>
      <a class="call" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
      <div class="trust"><span class="s">★★★★★</span> {D.GOOGLE_RATING} on Google · 24/7 emergency</div>
    </div>
  </div>
</header>

<div class="xh-callbar">
  <a class="call" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
  <button class="sched js-schedule" type="button">Schedule Online</button>
</div>'''

# ---------------------------------------------------------------- footer
def _area_links(items):
    """Service-area towns in the footer link to their own location pages. They are the
    deepest crawlable path into the /locations tree, so leaving them as plain text
    wastes the one place every page links from.

    Anchor text is always the plain place name. A boilerplate link repeated on ~311
    pages is discounted anyway, and dressing it as "Dayton Furnace Repair" is the
    clearest manipulated-linking tell available for no gain."""
    return " · ".join(f'<a href="/locations/{slug}">{name}</a>' for slug, name in items)

def _core_only(items):
    """The footer carries the core metros, not all 38 towns.

    38 towns x ~311 pages was ~11,800 identical boilerplate links spread evenly over
    every town the company has a page for, which is the same as spreading them over
    none. The other towns stay one click away on /locations and keep their links from
    every town in their own metro, so nothing is orphaned — the footer just stops
    spending its ~311 links on pages nobody is trying to rank.

    The set of towns this keeps is the same set `shell.py` leaves indexed, read from
    `locations.py` rather than restated here — a footer that promoted a town whose
    service pages are noindexed would be spending ~311 links on a dead end. It answers
    to whichever name that module settles on (`is_core`, `CORE`, or the `FEATURED` set
    shell.py already reads), and until one of them lands it returns the full list,
    which is the behavior that shipped before. A footer that is too generous is a
    missed opportunity; a footer that silently empties itself is a broken site.
    """
    is_core = getattr(L, "is_core", None)
    if callable(is_core):
        keep = [(s, n) for s, n in items if is_core(s)]
    else:
        core = getattr(L, "CORE_SET", None) or getattr(L, "CORE", None) \
            or getattr(L, "FEATURED", None)
        if not core:
            return items
        core = set(core)
        keep = [(s, n) for s, n in items if s in core]
    return keep or items

def _office_links():
    """The four office cities, linked from every page.

    These are premises, not service areas, and they are the only location pages
    carrying a postal address. Sitewide links are what keeps them the first thing
    reachable from anywhere on the site. An office with no location page yet is still
    named here — it is a real premises and the rest of the site counts it — it just
    renders as text rather than being linked into a 404."""
    return " · ".join(
        f'<a href="{href}">{name}</a>' if href else f'<span>{name}</span>'
        for name, href in D.FOOTER_NAP["offices"])

def footer():
    """Rendered on every page, so every link here costs ~311 links of boilerplate.

    Budget: ~18 column links + 4 contact + 4 social + 4 offices + 10 core metros +
    /locations + terms ≈ 42. Add to it only after subtracting something."""
    nap = D.FOOTER_NAP
    cols = ""
    for heading, links in D.FOOTER_COLUMNS:
        cols += (f'<div class="xf-col"><div class="xf-h">{heading}</div>' +
                 "".join(f'<a href="{h}">{l}</a>' for l, h in links) + "</div>")
    social = "".join(
        f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in D.SOCIAL)
    return f'''<footer class="xf">
  <div class="xf-accent"></div>
  <img class="xf-mark" src="{X_MARK}" alt="" aria-hidden="true"{T.dim_attrs(X_MARK)} loading="lazy" decoding="async">
  <div class="xf-wrap">
    <div class="xf-cta">
      <div>
        <h2>Need someone out today? Let's get you on the schedule.</h2>
        <p>Someone answers the phone 24/7, across Dayton &amp; Cincinnati.</p>
      </div>
      <div class="xf-cta-btns">
        <button class="xf-btn-green js-schedule" type="button">Schedule Service&nbsp;&nbsp;→</button>
        <a class="xf-btn-outline" href="{D.PHONE_TEL}">Call {D.PHONE_DISPLAY}</a>
      </div>
    </div>

    <div class="xf-grid">
      <div class="xf-col xf-brand">
        <img class="xf-logo" src="{LOGO_TIGHT}" alt="{D.COMPANY}"{T.dim_attrs(LOGO_TIGHT)} loading="lazy" decoding="async">
        <p class="xf-blurb">Locally owned, and we have been working on homes across the Miami
        Valley and Greater Cincinnati for over 20 years.</p>
        <div class="xf-247"><span class="dot"></span>We answer 24/7 · 7 days a week</div>
        <div class="xf-social">{social}</div>
      </div>
      {cols}
      <div class="xf-col">
        <div class="xf-h">CONTACT</div>
        <address class="xf-nap">
          <b>{nap["name"]}</b>{nap["street"]}<br>{nap["citystate"]}
        </address>
        <a class="xf-phone" href="{nap["phoneHref"]}">{nap["phoneDisplay"]}</a>
        <a href="{nap["emailHref"]}">{nap["email"]}</a>
        <a class="js-schedule" href="#">Schedule online</a>
        <a href="/contact">Contact us</a>
        <div class="xf-meta">{nap["hoursStaffed"]}<br>{nap["hoursEmergency"]}</div>
      </div>
    </div>

    <div class="xf-areas">
      <div class="xf-offices"><b>{nap["officesLabel"].upper()}</b>{_office_links()}</div>
      <div><b>DAYTON AREA</b>{_area_links(_core_only(L.DAYTON))}</div>
      <div><b>CINCINNATI AREA</b>{_area_links(_core_only(L.CINCINNATI))}</div>
      <div><b>SERVICE AREA</b><a href="/locations">All {len(L.ALL)} communities we serve →</a></div>
    </div>

    <div class="xf-bottom">
      <div>{D.FOOTER_LEGAL}</div>
      <div class="links">
        <!-- The route exists now (builder/privacy.py) and the client asked for it to be
             published, so the link is restored. The page carries a visible draft notice
             until counsel signs off — see privacy.PRIVACY_GAPS. -->
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
      </div>
    </div>
  </div>
</footer>'''

# ---------------------------------------------------------------- behaviour
# Where build_site.py publishes the schedule wizard bundle (built from
# src/schedule/mount.tsx by `npm run build:schedule`).
SCHEDULE_SRC = "/js/schedule.js"

JS = """
<script>
(function(){
  var SCHEDULE_SRC = '/js/schedule.js';
  var hd = document.querySelector('.xh-hd');
  if (!hd) return;

  /* --- mega menus. State lives on the header root, not the nav item, because the
         panels sit in .xm-shell outside the bar. Nesting them inside the bar meant the
         bar's color reset reached in and rendered the dropdown's links white on
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
  /* The menu-open flag also hides the sticky call bar — the panel pins its own
     Schedule and Call buttons to the bottom and the two were stacking on top of
     each other. */
  function openPanel(){ panel.dataset.open='true'; burger.setAttribute('aria-expanded','true');
                        document.documentElement.classList.add('xh-menu-open');
                        document.body.style.overflow='hidden'; }
  function closePanel(){ if(!panel) return; panel.dataset.open='false';
                         burger.setAttribute('aria-expanded','false');
                         document.documentElement.classList.remove('xh-menu-open');
                         document.body.style.overflow=''; }
  if (burger) burger.addEventListener('click', openPanel);
  if (closeBtn) closeBtn.addEventListener('click', closePanel);
  hd.querySelectorAll('.xh-panel a').forEach(function(a){ a.addEventListener('click', closePanel); });

  hd.querySelectorAll('.xh-acc > button').forEach(function(b){
    b.addEventListener('click', function(){
      var acc = b.parentElement, open = acc.dataset.open === 'true';
      acc.dataset.open = open ? 'false' : 'true';
      b.setAttribute('aria-expanded', open ? 'false' : 'true');
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

  /* --- schedule wizard: load on demand ------------------------------------
     The wizard is React and weighs ~59KB gzipped, so it is not on the critical
     path of a page whose whole job is to be read. Instead this listens for the
     same 'open-contact-dialog' event every Schedule button already fires — the
     header, the footer, the hero, the booking cards, the promo tiles — and pulls
     the bundle in the first time one of them is used. Once the dialog is mounted
     it answers the event itself and this listener steps aside.
     Warming on the first hover/touch means the click usually finds it cached. */
  var loading = false;
  function loadWizard(replay){
    if (window.XHSchedule) { if (replay) window.XHSchedule.open(); return; }
    if (replay) window.__xhScheduleWanted = true;
    if (loading) return;
    loading = true;
    var s = document.createElement('script');
    s.src = SCHEDULE_SRC;
    s.defer = true;
    s.onerror = function(){
      loading = false;
      /* No wizard, no dead end: the contact page has the form and the phone number. */
      if (window.__xhScheduleWanted) { window.__xhScheduleWanted = false; location.href = '/contact'; }
    };
    document.head.appendChild(s);
  }
  window.addEventListener('open-contact-dialog', function(){ loadWizard(true); });
  ['pointerover','touchstart','focusin'].forEach(function(evt){
    document.addEventListener(evt, function(e){
      if (e.target && e.target.closest && e.target.closest('.js-schedule')) loadWizard(false);
    }, {passive:true});
  });
})();

/* --- FAQ accordions ------------------------------------------------------
   The generated pages carry this behavior inside their embed script, and the
   self-hosted shell strips that script because the rest of it is iframe
   plumbing (see shell._strip_embed). Without a handler here every answer but
   the first stays shut on every page. Delegated from the document so it covers
   any FAQ block on any page, in its own IIFE so a page without the header
   still gets it. */
(function(){
  document.addEventListener('click', function(e){
    var btn = e.target && e.target.closest ? e.target.closest('.xsp-qa > button') : null;
    if (!btn) return;
    var row = btn.parentElement;
    var group = row.closest('.xsp-faq') || document;
    var wasOpen = row.classList.contains('open');
    group.querySelectorAll('.xsp-qa').forEach(function(r){
      r.classList.remove('open');
      var b = r.querySelector('button'), t = r.querySelector('.tog');
      if (b) b.setAttribute('aria-expanded', 'false');
      if (t) t.textContent = '+';
    });
    if (!wasOpen) {
      row.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      var tog = row.querySelector('.tog');
      if (tog) tog.textContent = '−';
    }
  });
})();
</script>
"""
