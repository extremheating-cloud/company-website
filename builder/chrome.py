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
.xh-hd a{color:inherit;text-decoration:none}
.xh-bar{max-width:1280px;margin:0 auto;padding:14px 40px;display:flex;align-items:center;
justify-content:space-between;gap:24px}
.xh-logo{display:flex;align-items:center;flex:none}
.xh-logo img{height:44px;width:auto;display:block}

.xh-nav{display:flex;align-items:center;gap:26px;font-weight:600;font-size:14px}
.xh-navitem{position:relative}
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

/* ---- mega menu ---- */
.xh-mega{position:absolute;top:100%;left:-24px;width:min(760px,calc(100vw - 48px));
background:#fff;color:#0F172A;border-radius:16px;box-shadow:0 24px 60px rgba(15,23,42,.28);
padding:24px;display:none;grid-template-columns:1.4fr 1fr;gap:24px}
.xh-navitem[data-open="true"] .xh-mega{display:grid}
.xh-mega h3{margin:0 0 12px;font-size:10.5px;font-weight:800;letter-spacing:1.6px;color:#5F2980}
.xh-row{display:block;padding:10px 12px;border-radius:10px}
.xh-row:hover{background:#F4F1F8}
.xh-row .t{font-weight:800;font-size:14.5px;color:#0F172A}
.xh-row .d{font-size:12.5px;color:#475569;margin-top:2px}
.xh-chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 0 12px}
.xh-chip{font-size:11.5px;font-weight:700;color:#5F2980;background:#F4F1F8;border-radius:999px;
padding:4px 10px;min-height:28px;display:inline-flex;align-items:center}
.xh-chip:hover{background:#E8DFF0}
.xh-alt{border-left:1px solid #E7E7EA;padding-left:24px}
.xh-alt a{display:flex;align-items:center;justify-content:space-between;gap:8px;
padding:9px 0;font-size:13.5px;font-weight:600;color:#475569}
.xh-alt a:hover{color:#5F2980}
.xh-badge{font-size:9.5px;font-weight:800;letter-spacing:1px;color:#3F852B;background:#ECF5E9;
border-radius:999px;padding:3px 8px}

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
  .xh-mega{left:-12px;width:min(620px,calc(100vw - 32px));grid-template-columns:1fr}
  .xh-alt{border-left:0;border-top:1px solid #E7E7EA;padding:16px 0 0}
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
def _mega(label, core, additional, alt_label):
    rows = ""
    for title, desc, href, chips in core:
        chip_html = ""
        if chips:
            chip_html = ('<div class="xh-chips">' +
                         "".join(f'<a class="xh-chip" href="{h}">{l}</a>' for l, h in chips) +
                         "</div>")
        rows += (f'<a class="xh-row" href="{href}"><span class="t">{title}</span>'
                 f'<span class="d">{desc}</span></a>{chip_html}')
    alts = "".join(
        f'<a href="{href}">{title}'
        f'{f"<span class=\"xh-badge\">{badge}</span>" if badge else ""}</a>'
        for title, href, badge in additional)
    return f'''<div class="xh-mega" role="menu">
      <div><h3>{label}</h3>{rows}</div>
      <div class="xh-alt"><h3>{alt_label}</h3>{alts}</div>
    </div>'''

def _nav_item(label, core, additional, alt_label, idx):
    return f'''<div class="xh-navitem" data-mega="{idx}">
      <button class="xh-navbtn" type="button" aria-expanded="false" aria-haspopup="true">
        {label} <span class="car" aria-hidden="true">▼</span>
      </button>
      {_mega(label.upper(), core, additional, alt_label)}
    </div>'''

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
      {_nav_item("Plumbing", D.PLUMB_CORE, D.PLUMB_ADDITIONAL, "ADDITIONAL SERVICES", 0)}
      {_nav_item("Heating &amp; Air", D.HVAC_CORE, D.HVAC_ADDITIONAL, "ADDITIONAL SERVICES", 1)}
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

  /* --- mega menus: open on hover for pointers, on click for everyone --- */
  var items = hd.querySelectorAll('.xh-navitem');
  function closeAll(except){
    items.forEach(function(it){
      if (it === except) return;
      it.dataset.open = 'false';
      it.querySelector('.xh-navbtn').setAttribute('aria-expanded','false');
    });
  }
  items.forEach(function(it){
    var btn = it.querySelector('.xh-navbtn');
    btn.addEventListener('click', function(e){
      e.preventDefault();
      var open = it.dataset.open === 'true';
      closeAll(it);
      it.dataset.open = open ? 'false' : 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
    });
    it.addEventListener('mouseenter', function(){
      if (matchMedia('(hover:hover) and (pointer:fine)').matches){ closeAll(it); it.dataset.open='true';
        btn.setAttribute('aria-expanded','true'); }
    });
    it.addEventListener('mouseleave', function(){
      if (matchMedia('(hover:hover) and (pointer:fine)').matches){ it.dataset.open='false';
        btn.setAttribute('aria-expanded','false'); }
    });
  });
  document.addEventListener('click', function(e){ if (!hd.contains(e.target)) closeAll(null); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape'){ closeAll(null); closePanel(); } });

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
