"""Service-page template system — design_handoff_services_pages.

Three tiers (detail / hub / subpage) assembled from shared section
renderers. Pages are emitted as self-contained <section> HTML embeds
matching the conventions of the existing service-page files.

Single source of truth for phone + asset URLs lives here.
"""

PHONE_TEL = "tel:18445847399"
PHONE_DISPLAY = "(844) 584-7399"
# ---------------------------------------------------------------- assets
# Everything the live site loads comes from this repo's own assets/ folder, served
# by jsDelivr. One repo, one place to look.
#
# ASSET_COMMIT pins what the site serves. jsDelivr caches the branch-to-commit
# resolution for 12 hours on top of a 7-day browser cache, so replacing a file in
# place does NOT change what visitors get — measured 2026-07-31: `@main` kept
# returning old bytes, a `?v=` query string did nothing, and the purge API reported
# "finished" while still serving the old commit. Pinning to a commit is the only
# thing that takes effect immediately.
#
# AFTER PUSHING new or changed assets: set ASSET_COMMIT to the new commit SHA and
# rebuild. `git rev-parse HEAD` gives it. "main" works but can serve stale files
# for up to 12 hours.
ASSET_REPO   = "https://cdn.jsdelivr.net/gh/extremheating-cloud/company-website"
ASSET_COMMIT = "c83bf3b6254c9bd3dbc1bd101024085c183abd20"

def cdn_asset(relpath, commit=None):
    """URL for anything under assets/. relpath is repo-relative below assets/,
    e.g. "team/tyler-hardy.jpg". Filenames are lowercase-hyphen with no spaces, so
    nothing needs percent-encoding — keep it that way."""
    return f"{ASSET_REPO}@{commit or ASSET_COMMIT}/assets/{relpath}"

CDN = f"{ASSET_REPO}@{ASSET_COMMIT}/assets/brand"
X_MARK = f"{CDN}/x-mark.png"

# ---------------------------------------------------------------- photography
# Named handles for the real Extreme photography, so pages refer to a subject
# rather than a filename. Add here rather than inlining a URL at a call site.
PHOTOS = {
    "beavercreek":  cdn_asset("locations/beavercreek-office.jpg"),
    "mason":        cdn_asset("locations/mason-office.jpg"),
    "vans":         cdn_asset("locations/vans-leaving.jpg"),
    "troy":         cdn_asset("locations/troy-community-event.jpg"),
    "skyline":      cdn_asset("locations/dayton-skyline-van.jpg"),
    "ruudHeatPump": cdn_asset("equipment/ruud-heat-pump.jpg"),
    "ruudInstall":  cdn_asset("equipment/ruud-install.jpg"),
    "traneInstall": cdn_asset("equipment/trane-install.jpg"),
    "geWaterHeater": cdn_asset("equipment/ge-water-heater-install.jpg"),
    "team": {
        "anthony-griffin": cdn_asset("team/anthony-griffin.jpg"),
        "jayvon-kilgore":  cdn_asset("team/jayvon-kilgore.jpg"),
        "joe-richardson":  cdn_asset("team/joe-richardson.jpg"),
        "tyler-hardy":     cdn_asset("team/tyler-hardy.jpg"),
    },
}

GRADIENT_HERO = "linear-gradient(180deg,#5E2C7E 0%,#542770 45%,#3A1A4E 100%)"

# ---------------------------------------------------------------- CSS
CSS = """
.xhac-svc{--purple:#542770;--purple-light:#5E2C7E;--purple-dark:#3A1A4E;--green:#6BB85C;
--green-hover:#8FD481;--green-dark:#4E9B41;--green-tint:#EEF7EC;--promo-green:#3D7A33;
--ink:#0F172A;--body:#475569;--muted:#94A3B8;--rule:#E7E7EA;--soft:#F7F6FA;--tint:#F4F1F8;
--stars:#F6A723;
font-family:"Montserrat",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial;
color:var(--ink);width:100%;overflow-x:hidden;
/* The embed is a bare <section>. Framer's page supplies the white behind it, but
   standalone — a local preview, or anyone opening the file — whatever is behind
   shows through, and on a dark-mode browser that is black under dark text.
   Own the background so the embed renders correctly anywhere. color-scheme keeps
   form controls light too, or the ZIP input renders dark-on-dark. */
background:#fff;color-scheme:light}
.xhac-svc *{box-sizing:border-box;margin:0}
.xsp-wrap{max-width:1280px;margin:0 auto;padding:0 40px}
.xsp-dt{}
.xsp-mb{display:none !important}

/* Where in-page anchor links land. The site header is position:sticky;top:0, so a
   section scrolled flush to the viewport top slides underneath it. scroll-margin-top
   is honoured by scrollIntoView — including across the embed iframe boundary — and
   pushes the landing point down by this much. TUNE THIS ONE VALUE if the header
   height changes: it should be header height + ~20px of breathing room. */
.xhac-svc{--xsp-anchor-offset:112px}
.xhac-svc [id]{scroll-margin-top:var(--xsp-anchor-offset)}

/* buttons */
.xsp-btn-green{display:flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:15px;padding:14px;border-radius:10px;min-height:44px;
text-decoration:none;cursor:pointer;border:0;font-family:inherit;width:100%;
box-shadow:0 6px 18px rgba(107,184,92,.35);transition:background .15s ease,color .15s ease}
.xsp-btn-green:hover{background:var(--green-dark);color:#fff}
.xsp-btn-purple{display:flex;align-items:center;justify-content:center;background:var(--purple);
color:#fff;font-weight:800;font-size:15px;padding:14px;border-radius:10px;min-height:44px;
text-decoration:none;cursor:pointer;border:0;font-family:inherit;width:100%;margin-top:10px;
transition:background .15s ease}
.xsp-btn-purple:hover{background:#3E1C54}
.xsp-cta{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:14px;padding:12px 20px;border-radius:10px;min-height:44px;
text-decoration:none;cursor:pointer;border:0;font-family:inherit;white-space:nowrap;
transition:background .15s ease}
.xsp-cta:hover{background:var(--green-hover)}
.xsp-cta-outline{display:inline-flex;align-items:center;justify-content:center;border:1.5px solid rgba(255,255,255,.45);
color:#fff;font-weight:800;font-size:14px;padding:12px 20px;border-radius:10px;min-height:44px;
text-decoration:none;background:transparent;white-space:nowrap;transition:border-color .15s,color .15s}
.xsp-cta-outline:hover{border-color:var(--green);color:var(--green)}

/* hero */
.xsp-hero{background:linear-gradient(180deg,#5E2C7E 0%,#542770 45%,#3A1A4E 100%);position:relative;color:#fff}
.xsp-hero-mark{position:absolute;inset:0;overflow:hidden;pointer-events:none}
.xsp-hero-mark img{position:absolute;right:-90px;top:-40px;width:620px;opacity:.06;
transform:rotate(-8deg);filter:brightness(0) invert(1)}
.xsp-hero-grid{position:relative;display:grid;grid-template-columns:1fr 360px;gap:48px;
max-width:1280px;margin:0 auto;padding:48px 40px 64px}
.xsp-hero-grid.nocard{grid-template-columns:1fr;padding-bottom:48px}
.xsp-crumbs{font-size:12px;font-weight:700;color:rgba(255,255,255,.7)}
.xsp-crumbs a{color:rgba(255,255,255,.7);text-decoration:none}
.xsp-crumbs a:hover{color:var(--green-hover)}
.xsp-crumbs .cur{color:var(--green)}
.xsp-crumbs .sep{margin:0 7px;opacity:.6}
.xsp-h1{margin-top:14px;font-style:italic;font-weight:900;font-size:46px;line-height:1.08;letter-spacing:-1px;color:#fff}
.xsp-h1 em{font-style:italic;color:var(--green)}
.xsp-hero.sub .xsp-h1{font-size:42px}
.xsp-intro{margin-top:16px;max-width:520px;font-size:15.5px;line-height:1.6;font-weight:500;color:rgba(255,255,255,.82)}
.xsp-chiprow{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap}
.xsp-chip{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);border-radius:12px;
padding:10px 14px;font-size:12.5px;font-weight:700;color:#fff}
.xsp-chip .st{color:var(--stars)}
.xsp-hero-ctas{display:flex;gap:12px;margin-top:24px;flex-wrap:wrap}
.xsp-trustline{display:flex;gap:18px;margin-top:22px;font-size:12.5px;font-weight:700;color:rgba(255,255,255,.85);flex-wrap:wrap}
.xsp-trustline .st{color:var(--stars)}
.xsp-trustline .di{color:var(--green)}

/* booking card (hero overlap) */
.xsp-bookcol{position:relative;margin-bottom:-84px;align-self:start}
.xsp-book{background:#fff;border-radius:16px;box-shadow:0 20px 50px rgba(15,23,42,.25);padding:24px;color:var(--ink)}
.xsp-book.inflow{box-shadow:0 12px 30px rgba(84,39,112,.12);border:1px solid var(--rule)}
.xsp-book .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--green-dark)}
.xsp-book .t{font-weight:800;font-size:18px;margin-top:8px}
.xsp-book .s{font-size:13px;font-weight:500;color:var(--body);margin-top:6px;line-height:1.5}
.xsp-book .btns{margin-top:16px}
.xsp-book .trust{display:flex;align-items:center;justify-content:center;gap:14px;border-top:1px solid var(--rule);
margin-top:16px;padding-top:14px;font-size:12px;font-weight:700;color:var(--body)}
.xsp-book .trust .st{color:var(--stars)}
.xsp-book .trust .bar{color:#D8D5DE}

/* pill sub-nav */
.xsp-pillbar{background:#fff;border-bottom:1px solid var(--rule)}
.xsp-pillbar-in{max-width:1280px;margin:0 auto;padding:14px 40px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.xsp-pill-label{font-size:10.5px;font-weight:800;letter-spacing:1.8px;color:var(--muted)}
.xsp-pills{display:flex;gap:8px;flex-wrap:wrap}
.xsp-pill{border-radius:999px;padding:8px 16px;font-size:12.5px;font-weight:700;text-decoration:none;
color:var(--purple);background:var(--tint);min-height:32px;display:inline-flex;align-items:center;
transition:background .15s,color .15s}
.xsp-pill:hover{background:#E9E2F1}
.xsp-pill.active{background:var(--purple);color:#fff;font-weight:800}

/* body grid */
.xsp-bodygrid{display:grid;grid-template-columns:1fr 360px;gap:48px;max-width:1280px;margin:0 auto;padding:56px 40px}
.xsp-main{display:flex;flex-direction:column;gap:48px;min-width:0}
.xsp-rail{padding-top:64px;display:flex;flex-direction:column;gap:16px;align-self:start}
.xsp-rail.flush{padding-top:0}
.xsp-eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--green-dark)}
.xsp-eyebrow.purple{color:var(--purple)}
.xsp-h2{margin-top:10px;font-style:italic;font-weight:900;font-size:33px;letter-spacing:-.5px;color:var(--ink)}

/* checklist */
.xsp-checks{display:grid;grid-template-columns:1fr 1fr;gap:12px 24px;margin-top:20px}
.xsp-check{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:700;color:var(--body)}
.xsp-check .c{width:18px;height:18px;flex:none;border-radius:50%;background:var(--green);color:#fff;
font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center}
.xsp-callout{margin-top:20px;background:var(--green-tint);border-radius:12px;padding:14px 18px;
font-size:13px;font-weight:600;color:var(--promo-green);line-height:1.55}
.xsp-callout a{color:var(--promo-green);font-weight:800;text-decoration:none}
.xsp-callout.safety{background:var(--ink);color:rgba(255,255,255,.85)}
.xsp-callout.safety b{color:var(--green-hover)}
.xsp-callout.safety a{color:#fff;font-weight:800}

/* what-we-do cards */
.xsp-cards3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px}
.xsp-card{border:1px solid var(--rule);border-radius:16px;padding:20px;background:#fff;display:flex;
flex-direction:column;gap:8px;text-decoration:none;transition:box-shadow .18s,border-color .18s,transform .18s}
.xsp-card:hover{box-shadow:0 12px 30px rgba(84,39,112,.12);border-color:#D8CCE4;transform:translateY(-2px)}
.xsp-card .t{font-weight:800;font-size:16.5px;color:var(--ink)}
.xsp-card .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body)}
.xsp-card .lm{font-weight:800;font-size:13px;color:var(--purple);margin-top:2px}
.xsp-card:hover .lm{color:var(--green-dark)}
.xsp-glyph{position:relative;display:block;width:30px;height:30px;flex:none}
.xsp-glyph i{position:absolute;inset:11px 2px;border-radius:2px;display:block}
.xsp-glyph i:first-child{background:var(--purple);transform:rotate(45deg)}
.xsp-glyph i:last-child{background:var(--green);transform:rotate(-45deg)}

/* process */
.xsp-steps{display:flex;flex-direction:column;gap:22px;margin-top:20px}
.xsp-step{display:flex;gap:0}
.xsp-step .n{flex:0 0 44px;font-style:italic;font-weight:900;font-size:25px;color:var(--purple)}
.xsp-step .t{font-weight:800;font-size:15px}
.xsp-step .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px;max-width:560px}

/* decision card */
.xsp-decision{border:1px solid var(--rule);border-radius:16px;padding:20px 22px;background:#fff}
.xsp-decision .t{font-weight:800;font-size:16.5px}
.xsp-decision .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:6px;max-width:620px}
.xsp-decision a{display:inline-flex;align-items:center;margin-top:12px;border:2px solid var(--purple);
color:var(--purple);font-weight:800;font-size:13.5px;padding:10px 18px;border-radius:10px;min-height:40px;
text-decoration:none;transition:background .15s,color .15s}
.xsp-decision a:hover{background:var(--purple);color:#fff}

/* faq */
.xsp-faq{display:flex;flex-direction:column;gap:12px;margin-top:20px}
.xsp-qa{border:1px solid var(--rule);border-radius:14px;background:#fff;overflow:hidden}
.xsp-qa button{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;
padding:16px 18px;background:none;border:0;cursor:pointer;font-family:inherit;text-align:left;
font-weight:700;font-size:15px;color:var(--ink);min-height:44px}
.xsp-qa .tog{width:26px;height:26px;flex:none;border-radius:50%;background:var(--tint);color:var(--purple);
display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;transition:background .15s,color .15s}
.xsp-qa.open .tog{background:var(--purple);color:#fff}
.xsp-qa .a{display:none;font-size:13.5px;line-height:1.6;font-weight:500;color:var(--body);
padding:0 18px 16px;max-width:620px}
.xsp-qa.open .a{display:block}

/* rail photo + promos */
.xsp-photo{height:220px;border-radius:14px;background:#F4F6F8;border:1px solid var(--rule);
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--muted);
letter-spacing:1px;overflow:hidden}
.xsp-photo img{width:100%;height:100%;object-fit:cover;display:block}
.xsp-promo{border-radius:14px;padding:18px 20px;display:block;text-decoration:none}
.xsp-promo.lav{background:var(--tint)}
.xsp-promo.mint{background:var(--green-tint)}
.xsp-promo .t{font-weight:800;font-size:15px;color:var(--purple)}
.xsp-promo.mint .t{color:var(--promo-green)}
.xsp-promo .d{font-size:12.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:6px}
.xsp-promo .lm{font-weight:800;font-size:13px;color:var(--purple);margin-top:10px}
.xsp-promo.mint .lm{color:var(--promo-green)}
.xsp-promo:hover .lm{text-decoration:underline}
.xsp-sibs{border:1px solid var(--rule);border-radius:14px;padding:18px 20px;background:#fff}
.xsp-sibs .h{font-size:10.5px;font-weight:800;letter-spacing:1.8px;color:var(--muted)}
.xsp-sibs a{display:flex;align-items:center;justify-content:space-between;padding:10px 0;
font-size:13.5px;font-weight:700;color:var(--ink);text-decoration:none;border-bottom:1px solid #F1F0F4;min-height:40px}
.xsp-sibs a:last-child{border-bottom:0;padding-bottom:0}
.xsp-sibs a:hover{color:var(--purple)}
.xsp-sibs .ar{color:var(--purple);font-weight:800}

/* emergency band */

/* related strip */
.xsp-rel{background:var(--soft)}
.xsp-rel-in{max-width:1280px;margin:0 auto;padding:44px 40px}
.xsp-rel-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:16px}
.xsp-rel-card{background:#fff;border-radius:14px;padding:18px;box-shadow:0 1px 2px rgba(15,23,42,.05);
text-decoration:none;display:flex;flex-direction:column;gap:6px;transition:box-shadow .18s,transform .18s}
.xsp-rel-card:hover{box-shadow:0 12px 30px rgba(84,39,112,.12);transform:translateY(-2px)}
.xsp-rel-card .t{font-weight:800;font-size:15px;color:var(--ink)}
.xsp-rel-card .lm{font-weight:800;font-size:13px;color:var(--purple)}
.xsp-rel-card:hover .lm{color:var(--green-dark)}

/* ------------------------- mobile (2b stacking) ------------------------- */
@media (max-width:809px){
.xhac-svc{--xsp-anchor-offset:96px}
.xsp-dt{display:none !important}
.xsp-mb{display:revert !important}
.xsp-wrap,.xsp-pillbar-in,.xsp-rel-in{padding-left:20px;padding-right:20px}
.xsp-hero-grid{grid-template-columns:1fr;gap:0;padding:32px 20px 44px}
.xsp-h1{font-size:34px;letter-spacing:-.5px}
.xsp-hero.sub .xsp-h1{font-size:32px}
.xsp-intro{font-size:14px}
.xsp-hero-ctas{flex-direction:column;gap:14px}
.xsp-hero-ctas.xsp-mb{display:flex !important;flex-direction:column;gap:14px}
.xsp-hero-ctas .xsp-cta,.xsp-hero-ctas .xsp-cta-outline{width:100%}
.xsp-chiprow{gap:8px}
.xsp-chip{padding:7px 10px;font-size:11px;border-radius:10px}
.xsp-bookcol{display:none}
.xsp-bodygrid{grid-template-columns:1fr;gap:40px;padding:40px 20px 48px}
.xsp-rail{display:none}
.xsp-h2{font-size:24px;letter-spacing:-.4px}
.xsp-checks{grid-template-columns:1fr;gap:10px}
.xsp-cards3{grid-template-columns:1fr;gap:0;margin-top:12px}
.xsp-card{flex-direction:row;align-items:center;gap:12px;border:0;border-radius:0;
border-bottom:1px solid #F1F0F4;padding:13px 0;background:transparent}
.xsp-card:hover{box-shadow:none;transform:none}
.xsp-card .xsp-glyph{width:26px;height:26px}
.xsp-card .glyphwrap{flex:none}
.xsp-card .txt{flex:1}
.xsp-card .t{font-size:14.5px}
.xsp-card .d{font-size:11.5px;line-height:1.45}
.xsp-card .lm{display:none}
.xsp-card .mrow{display:block;color:var(--purple);font-weight:800}
.xsp-step .d{font-size:13px}
.xsp-rel-grid{grid-template-columns:1fr;gap:0;margin-top:10px}
.xsp-rel-card{flex-direction:row;align-items:center;justify-content:space-between;border-radius:0;
box-shadow:none;background:transparent;padding:13px 0;border-bottom:1px solid #F1F0F4}
.xsp-rel-card:hover{box-shadow:none;transform:none}
.xsp-mbrail.xsp-mb{display:flex !important;flex-direction:column;gap:14px}
}
@media (min-width:810px){
.xsp-card .mrow{display:none}
}
"""

# ---------------------------------------------------------------- JS
def script(root_class):
    return f"""
  <script>
    (() => {{
      const root = document.currentScript.closest(".{root_class}");
      if (!root) return;
      root.querySelectorAll("a[href]").forEach((a) => {{
        const h = a.getAttribute("href") || "";
        if (h && !h.startsWith("#") && !h.startsWith("tel:")) {{
          // Default off-site links to _top so they escape the embed iframe instead
          // of loading a full site inside a content-sized frame. A link that already
          // declares a target (the lender application uses _blank) keeps its own.
          if (!a.getAttribute("target")) a.setAttribute("target", "_top");
          if (!a.getAttribute("rel")) a.setAttribute("rel", "noopener");
        }}
      }});
      // In Framer the embed iframe is sized to its content, so this document has
      // nothing to scroll — scrollIntoView has to cross the frame boundary to move
      // the parent page. A plain hash jump never does that (the anchor just sets the
      // hash and nothing moves), and "smooth" does not cross the boundary either —
      // it silently no-ops. Instant is the behaviour that works in an embed, in a
      // scrollable iframe, and standalone.
      //
      // The site header is position:sticky;top:0, so landing flush with the top hides
      // the section heading underneath it. Measure the real header at jump time and
      // clear it; --xsp-anchor-offset in the CSS is the fallback for when the parent
      // can't be read.
      // How far below the viewport top an anchored section should land: enough to
      // clear the site's sticky header. Measured off the real header when the parent
      // is readable; --xsp-anchor-offset in the CSS is the fallback.
      const landingOffset = () => {{
        try {{
          const pw = window.parent;
          if (pw && pw !== window && pw.document) {{
            let node = pw.document.elementFromPoint(Math.round(pw.innerWidth / 2), 4);
            let headerH = 0, hops = 0;
            while (node && hops++ < 12) {{
              const cs = pw.getComputedStyle(node);
              if (cs.position === "sticky" || cs.position === "fixed") {{
                const r = node.getBoundingClientRect();
                if (r.top <= 1 && r.height > 0 && r.height < pw.innerHeight * 0.5) {{
                  headerH = Math.max(headerH, r.height);
                }}
              }}
              node = node.parentElement;
            }}
            if (headerH) return Math.round(headerH + 20);
          }}
        }} catch (err) {{}}
        const v = parseInt(getComputedStyle(document.documentElement)
          .getPropertyValue("--xsp-anchor-offset"), 10);
        return isNaN(v) ? 112 : v;
      }};

      const jumpTo = (target) => {{
        if (!target) return;
        const offset = landingOffset();
        // scrollIntoView cannot be trusted to cross the embed boundary correctly.
        // Measured in a content-sized iframe under a sticky header: the browser
        // scrolls the parent to (target's Y *within this document*) - offset and
        // never adds the iframe's own offsetTop in the parent, so every anchor
        // lands short by exactly however far down the page the embed sits. Compute
        // the absolute position and drive the parent's scroll directly instead.
        try {{
          const pw = window.parent;
          const fe = window.frameElement;
          if (pw && pw !== window && fe) {{
            const frameTop = fe.getBoundingClientRect().top + (pw.scrollY || pw.pageYOffset || 0);
            const targetTop = target.getBoundingClientRect().top + (window.scrollY || 0);
            pw.scrollTo(0, Math.max(0, Math.round(frameTop + targetTop - offset)));
            if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
            try {{ target.focus({{ preventScroll: true }}); }} catch (err) {{}}
            return;
          }}
        }} catch (err) {{}}
        // Standalone, or a parent we're not allowed to read: scrollIntoView is
        // correct here because there is only one scrolling box involved.
        target.style.scrollMarginTop = offset + "px";
        target.scrollIntoView({{ behavior: "auto", block: "start" }});
        if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
        try {{ target.focus({{ preventScroll: true }}); }} catch (err) {{}}
      }};

      root.querySelectorAll('a[href^="#"]').forEach((a) => {{
        const id = (a.getAttribute("href") || "").slice(1);
        if (!id) return;
        a.addEventListener("click", (e) => {{
          const target = document.getElementById(id);
          if (!target) return;
          e.preventDefault();
          jumpTo(target);
        }});
      }});

      // Deep links from another page (/terms#financing) land the hash on the PARENT
      // url — this document never sees it, and the parent has no element with that
      // id because the section lives in here. Read the parent's hash on load and, if
      // it names something inside this embed, run the same jump an in-page anchor
      // would. Without this a cross-page anchor silently lands at the top of the page.
      try {{
        let hash = window.location.hash;
        if (!hash && window.parent !== window) hash = window.parent.location.hash || "";
        const id = decodeURIComponent(hash.replace(/^#/, ""));
        const target = id ? document.getElementById(id) : null;
        if (target) {{
          // Framer is still laying out (and loading images) when this runs, so the
          // first jump can land short. Repeat once the layout settles, then stop —
          // and abandon it the moment the reader scrolls, so we never yank the page
          // out from under someone who has started reading.
          let userMoved = false;
          const release = () => {{ userMoved = true; }};
          ["wheel", "touchstart", "keydown"].forEach((evt) => {{
            window.addEventListener(evt, release, {{ once: true, passive: true }});
            try {{ window.parent.addEventListener(evt, release, {{ once: true, passive: true }}); }} catch (err) {{}}
          }});
          const settle = (delay) => setTimeout(() => {{ if (!userMoved) jumpTo(target); }}, delay);
          requestAnimationFrame(() => requestAnimationFrame(() => jumpTo(target)));
          settle(250);
          settle(800);
        }}
      }} catch (err) {{}}

      root.querySelectorAll(".js-schedule").forEach((el) => {{
        el.addEventListener("click", (e) => {{
          e.preventDefault();
          try {{
            if (window.parent && window.parent !== window) {{
              window.parent.dispatchEvent(new window.parent.CustomEvent("open-contact-dialog"));
              return;
            }}
          }} catch (err) {{}}
          window.dispatchEvent(new CustomEvent("open-contact-dialog"));
        }});
      }});
      root.querySelectorAll(".xsp-faq").forEach((faq) => {{
        faq.querySelectorAll(".xsp-qa > button").forEach((btn) => {{
          btn.addEventListener("click", () => {{
            const row = btn.parentElement;
            const wasOpen = row.classList.contains("open");
            faq.querySelectorAll(".xsp-qa").forEach((r) => {{
              r.classList.remove("open");
              r.querySelector("button").setAttribute("aria-expanded", "false");
              r.querySelector(".tog").textContent = "+";
            }});
            if (!wasOpen) {{
              row.classList.add("open");
              btn.setAttribute("aria-expanded", "true");
              row.querySelector(".tog").textContent = "−";
            }}
          }});
        }});
      }});
      const inIframe = window.parent && window.parent !== window;
      const sendSize = () => {{
        try {{
          if (inIframe) window.parent.postMessage(
            {{ type: "embed-resize", height: Math.ceil(root.getBoundingClientRect().height), source: "{root_class}" }}, "*");
        }} catch (e) {{}}
      }};
      if ("ResizeObserver" in window) new ResizeObserver(sendSize).observe(root);
      window.addEventListener("load", sendSize);
      sendSize();
    }})();
  </script>"""

# ------------------------------------------------------- section renderers
def esc(s):
    return s  # copy strings are authored with entities where needed

def crumbs(items):
    out = []
    for i, (label, href) in enumerate(items):
        last = i == len(items) - 1
        if last:
            out.append(f'<span class="cur">{label}</span>')
        else:
            out.append(f'<a href="{href}">{label}</a><span class="sep">›</span>')
    return f'<div class="xsp-crumbs">{"".join(out)}</div>'

def h1(text, highlight):
    return f'<h1 class="xsp-h1">{text.replace("{X}", f"<em>{highlight}</em>")}</h1>'

def chips(items):
    spans = []
    for c in items:
        star = '<span class="st">★</span> ' if c.startswith("4.9") else ""
        label = c
        spans.append(f'<div class="xsp-chip">{star}{label}</div>')
    return f'<div class="xsp-chiprow">{"".join(spans)}</div>'

def schedule_btn(label, cls="xsp-btn-green"):
    return f'<a class="{cls} js-schedule" href="#" role="button">{label}</a>'

def call_btn(label, cls="xsp-btn-purple"):
    return f'<a class="{cls}" href="{PHONE_TEL}">{label}</a>'

def booking_card(bc, inflow=False, schedule_label="Schedule Service"):
    flow = " inflow" if inflow else ""
    return f'''<div class="xsp-book{flow}">
  <div class="eyebrow">{bc["eyebrow"]}</div>
  <div class="t">{bc["title"]}</div>
  <div class="s">{bc["sub"]}</div>
  <div class="btns">
    {schedule_btn(schedule_label)}
    {call_btn(f"Call {PHONE_DISPLAY}")}
  </div>
  <div class="trust"><span><span class="st">★</span> 4.9 on Google</span><span class="bar">|</span><span>{bc.get("trust2", "20+ years local")}</span></div>
</div>'''

def hero_detail(d):
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{X_MARK}" alt=""></div>
  <div class="xsp-hero-grid">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas xsp-mb">
        {schedule_btn("Schedule Service", "xsp-cta js-schedule")}
        <a class="xsp-cta-outline" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      </div>
      {chips(d["heroChips"])}
    </div>
    <div class="xsp-bookcol">{booking_card(d["bookingCard"])}</div>
  </div>
</div>'''

def hero_sub(d):
    return f'''<div class="xsp-hero sub">
  <div class="xsp-hero-mark"><img src="{X_MARK}" alt=""></div>
  <div class="xsp-hero-grid nocard">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas">
        {schedule_btn(d.get("scheduleLabel", "Schedule Service"), "xsp-cta js-schedule")}
        <a class="xsp-cta-outline" href="{PHONE_TEL}">Call Now</a>
      </div>
      <div class="xsp-trustline"><span><span class="st">★</span> 4.9 on Google</span><span>◆ 20+ years locally owned</span><span>◆ 24/7 emergency service</span></div>
    </div>
  </div>
</div>'''

def pill_nav(p):
    pills = "".join(
        f'<a class="xsp-pill{" active" if it["active"] else ""}" href="{it["href"]}"'
        + (' aria-current="page"' if it["active"] else "")
        + f'>{it["label"]}</a>'
        for it in p["items"]
    )
    return f'''<div class="xsp-pillbar"><div class="xsp-pillbar-in">
  <span class="xsp-pill-label">{p["label"]}</span>
  <div class="xsp-pills">{pills}</div>
</div></div>'''

def checklist(s, trade_eyebrow="green"):
    items = "".join(
        f'<div class="xsp-check"><span class="c">✓</span>{i}</div>' for i in s["items"]
    )
    variant = " safety" if s.get("safety") else ""
    return f'''<div>
  <div class="xsp-eyebrow{"" if trade_eyebrow == "green" else " purple"}">{s["eyebrow"]}</div>
  <h2 class="xsp-h2">{s["h2"]}</h2>
  <div class="xsp-checks">{items}</div>
  <div class="xsp-callout{variant}">{s["callout"]}</div>
</div>'''

def what_we_do(w):
    cards = "".join(
        f'''<a class="xsp-card" href="{c["href"]}">
      <span class="glyphwrap"><span class="xsp-glyph"><i></i><i></i></span></span>
      <span class="txt"><span class="t">{c["title"]}</span><br><span class="d">{c["desc"]}</span></span>
      <span class="lm">Learn more →</span><span class="mrow">→</span>
    </a>''' for c in w["cards"]
    )
    return f'''<div>
  <div class="xsp-eyebrow">WHAT WE DO</div>
  <h2 class="xsp-h2">{w["h2"]}</h2>
  <div class="xsp-cards3">{cards}</div>
</div>'''

def process(p, eyebrow="WHAT TO EXPECT", h2="A visit without surprises."):
    steps = "".join(
        f'''<div class="xsp-step"><div class="n">0{i + 1}</div>
    <div><div class="t">{s["title"]}</div><div class="d">{s["desc"]}</div></div></div>'''
        for i, s in enumerate(p["steps"])
    )
    return f'''<div>
  <div class="xsp-eyebrow">{eyebrow}</div>
  <h2 class="xsp-h2">{p.get("h2", h2)}</h2>
  <div class="xsp-steps">{steps}</div>
</div>'''

def decision_card(dc):
    return f'''<div class="xsp-decision">
  <div class="t">{dc["title"]}</div>
  <div class="d">{dc["desc"]}</div>
  <a href="{dc["href"]}">{dc["linkLabel"]}</a>
</div>'''

def faq(f, eyebrow, h2="Your questions, answered."):
    rows = []
    for i, qa in enumerate(f):
        open_cls = " open" if i == 0 else ""
        tog = "−" if i == 0 else "+"
        exp = "true" if i == 0 else "false"
        rows.append(f'''<div class="xsp-qa{open_cls}">
    <button type="button" aria-expanded="{exp}"><span>{qa["q"]}</span><span class="tog" aria-hidden="true">{tog}</span></button>
    <div class="a">{qa["a"]}</div>
  </div>''')
    return f'''<div>
  <div class="xsp-eyebrow">{eyebrow}</div>
  {f'<h2 class="xsp-h2">{h2}</h2>' if h2 else ""}
  <div class="xsp-faq">{"".join(rows)}</div>
</div>'''

PROMOS = {
    "financing": dict(cls="lav", t="Interested in financing?",
        d="Spread out the cost of a new comfort system with flexible payment options that fit your budget.",
        lm="Learn More →", href="/financing-options"),
    "xplan": dict(cls="mint", t="X-Plan members save 15% on repairs",
        d="Two tune-ups a year, priority scheduling, and a 5-year warranty on repairs.",
        lm="Explore X-Plan →", href="/maintenance"),
    "xplanSub": dict(cls="mint", t="X-Plan members save 15% on repairs",
        d="Plus a 5-year warranty on repairs and priority scheduling.",
        lm="Explore X-Plan →", href="/maintenance"),
    "scheduleFast": dict(cls="lav", t="Need plumbing help fast?",
        d="Book service online and we'll get a plumber out as soon as possible.",
        lm="Schedule Service →", href="#", schedule=True),
    "specials": dict(cls="mint", t="Plumbing specials",
        d="Check out current offers on repairs, installs, and more.",
        lm="View Specials →", href="/specials"),
}

def promo(key):
    p = PROMOS[key]
    sched = " js-schedule" if p.get("schedule") else ""
    return f'''<a class="xsp-promo {p["cls"]}{sched}" href="{p["href"]}">
  <div class="t">{p["t"]}</div><div class="d">{p["d"]}</div><div class="lm">{p["lm"]}</div>
</a>'''

def photo_slot(label="PHOTO — TECH AT UNIT", src=None, alt="", pos=None):
    """pos sets object-position for sources whose subject isn't centred. The slot is
    360x220 landscape and the image is object-fit:cover, so a portrait photo shows
    only a horizontal band of itself — pos is how you choose which band."""
    if src:
        style = f' style="object-position:{pos}"' if pos else ""
        return (f'<div class="xsp-photo"><img src="{src}" alt="{alt}"{style} '
                f'loading="lazy" decoding="async"></div>')
    return f'<div class="xsp-photo" data-photo-slot>{label}</div>'

def rail(r, flush=False, extra=""):
    parts = []
    if r.get("photo") or r.get("photoSlot"):
        parts.append(photo_slot(r.get("photoLabel", "PHOTO — TECH AT UNIT"),
                                r.get("photo"), r.get("photoAlt", ""), r.get("photoPos")))
    parts += [promo(k) for k in r["promos"]]
    return f'<aside class="xsp-rail{" flush" if flush else ""}">{extra}{"".join(parts)}</aside>'

def sibling_links(s):
    links = "".join(
        f'<a href="{it["href"]}">{it["title"]}<span class="ar">→</span></a>' for it in s["items"]
    )
    return f'<div class="xsp-sibs"><div class="h">{s["label"]}</div>{links}</div>'

def related(rel):
    cards = "".join(
        f'''<a class="xsp-rel-card" href="{r["href"]}"><span class="t">{r["title"]}</span><span class="lm xsp-dt">Learn more →</span><span class="lm xsp-mb">→</span></a>'''
        for r in rel
    )
    return f'''<div class="xsp-rel"><div class="xsp-rel-in">
  <div class="xsp-eyebrow purple">KEEP EXPLORING</div>
  <div class="xsp-rel-grid">{cards}</div>
</div></div>'''

def mobile_inline_rail(d, with_photo=False):
    """2b: photo + financing/x-plan promos flow inline after Process on mobile.

    The rail is display:none under 810px, so a rail photo is desktop-only unless it
    is repeated here. with_photo defaults off: turning it on for every page that has
    a rail photo would change ~30 already-pasted service pages, so callers opt in.
    """
    parts = []
    if with_photo and d["rail"].get("photo"):
        parts.append(photo_slot("", d["rail"]["photo"], d["rail"].get("photoAlt", ""),
                                d["rail"].get("photoPos")))
    parts += [promo(k) for k in d["rail"]["promos"]]
    return f'<div class="xsp-mbrail xsp-mb">{"".join(parts)}</div>'

# ------------------------------------------------------------ assemblers
def page_shell(root_class, body):
    return f'''<section class="xhac-svc {root_class}">
  <style>{CSS}</style>
{body}
{script("xhac-svc")}
</section>
'''

def detail_page(d, root_class):
    """Tier 2 — detail template (2a/2b). Optional pillNav → 2e combo."""
    left = [checklist(d["symptoms"])]
    if d.get("whatWeDo"):
        left.append(what_we_do(d["whatWeDo"]))
    left.append(process(d["process"]))
    left.append(mobile_inline_rail(d))
    left.append(faq(d["faq"], d["faqEyebrow"]))
    body = f'''{hero_detail(d)}
{pill_nav(d["pillNav"]) if d.get("pillNav") else ""}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {rail(d["rail"])}
</div>
{xplan_panel()}
{related(d["related"])}'''
    return page_shell(root_class, body)

def sub_page(d, root_class):
    """Tier 3 — sub-page template (2d)."""
    left = [checklist(d["symptoms"])]
    left.append(process(d["process"]))
    if d.get("decision"):
        left.append(decision_card(d["decision"]))
    left.append(mobile_inline_rail(d))
    left.append(faq(d["faq"], d["faqEyebrow"]))
    rail_extra = booking_card(d["bookingCard"], inflow=True,
                              schedule_label=d.get("scheduleLabel", "Schedule Service"))
    tail = ""
    if d["rail"].get("photo"):
        tail = photo_slot("", d["rail"]["photo"], d["rail"].get("photoAlt", ""),
                          d["rail"].get("photoPos"))
    rail_html = f'''<aside class="xsp-rail flush">{rail_extra}{promo(d["rail"]["promos"][0])}{sibling_links(d["siblings"])}{tail}</aside>'''
    body = f'''{hero_sub(d)}
{pill_nav(d["pillNav"])}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {rail_html}
</div>
{xplan_panel()}'''
    return page_shell(root_class, body)

# ------------------------------------------------------------ hub sections
HUB_CSS = """
.xsp-hubhero-grid{position:relative;display:grid;grid-template-columns:1fr .9fr;gap:48px;align-items:center;
max-width:1280px;margin:0 auto;padding:48px 40px 72px}
.xsp-hub-pill{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.3);
background:rgba(255,255,255,.1);border-radius:999px;padding:7px 14px;font-size:11.5px;font-weight:800;
letter-spacing:2px;color:#fff}
.xsp-hub-pill .dot{width:7px;height:7px;border-radius:50%;background:var(--green)}
.xsp-hubhero-grid .xsp-h1{font-size:44px}
.xsp-hub-photo{position:relative;min-height:280px}
.xsp-hub-photo .slashw{position:absolute;left:2%;right:-6%;bottom:26px;height:14px;background:#fff;opacity:.25;
transform:rotate(-9deg) skewX(-16deg)}
.xsp-hub-photo .slash{position:absolute;left:-6%;right:-2%;bottom:34px;height:44px;background:var(--green);
transform:rotate(-9deg) skewX(-16deg);box-shadow:0 20px 60px rgba(0,0,0,.3)}
.xsp-hub-photo .ph{position:relative;height:280px;border-radius:20px;overflow:hidden;background:#F4F6F8;
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:1px}
.xsp-hub-photo .ph img{width:100%;height:100%;object-fit:cover;display:block}
.xsp-xplan-detail{list-style:none;margin:16px 0 0;padding:0;display:grid;
grid-template-columns:1fr 1fr;gap:8px 22px}
.xsp-xplan-detail li{display:flex;gap:9px;font-size:13.5px;font-weight:600;color:rgba(255,255,255,.9)}
.xsp-xplan-detail li .c{width:17px;height:17px;flex:none;border-radius:50%;background:var(--green);
color:var(--ink);font-size:10px;font-weight:800;display:grid;place-items:center}
@media (max-width:809px){.xsp-xplan-detail{grid-template-columns:1fr}}
.xsp-cut{position:relative;height:84px;background:#fff;clip-path:polygon(0 62%,100% 0,100% 100%,0 100%)}
.xsp-promise{background:#fff;padding:6px 0 26px}
.xsp-promise-in{max-width:1280px;margin:0 auto;padding:0 40px;display:flex;justify-content:space-between;
align-items:center;gap:20px;flex-wrap:wrap}
.xsp-promise-label{font-size:12px;font-weight:800;letter-spacing:1.8px;color:var(--muted)}
.xsp-promise-items{display:flex;gap:26px;flex-wrap:wrap}
.xsp-promise-items span{font-size:12.5px;font-weight:700;color:var(--body)}
.xsp-promise-items .di{color:var(--green)}
.xsp-hubsec{background:#fff;padding:44px 0 56px}
.xsp-hubsec.soft{background:var(--soft)}
.xsp-hubsec-in{max-width:1280px;margin:0 auto;padding:0 40px}
.xsp-grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px}
.xsp-grid4{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;margin-top:20px}
.xsp-notsure{background:var(--tint);border:0;border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:8px;
text-decoration:none;transition:box-shadow .18s,transform .18s}
.xsp-notsure:hover{box-shadow:0 12px 30px rgba(84,39,112,.12);transform:translateY(-2px)}
.xsp-notsure .t{font-weight:800;font-size:16.5px;color:var(--purple)}
.xsp-notsure .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body)}
.xsp-notsure .lm{font-weight:800;font-size:13px;color:var(--purple);margin-top:2px}
.xsp-badge{display:inline-block;background:var(--green-tint);color:var(--green-dark);font-weight:800;
font-size:9.5px;letter-spacing:.6px;border-radius:5px;padding:3px 7px;margin-left:8px;vertical-align:middle}
a.xsp-xplan{text-decoration:none;cursor:pointer;transition:box-shadow .18s,transform .18s}
a.xsp-xplan:hover{box-shadow:0 18px 44px rgba(84,39,112,.35);transform:translateY(-2px)}
.xsp-xplan{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;padding:40px 44px;
color:#fff;position:relative;overflow:hidden;display:grid;grid-template-columns:1.1fr auto;gap:32px;align-items:center}
.xsp-xplan .mark{position:absolute;right:-40px;bottom:-46px;width:300px;opacity:.06;pointer-events:none;
filter:brightness(0) invert(1)}
.xsp-xplan .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--green-hover)}
.xsp-xplan h2{margin-top:10px;font-style:italic;font-weight:900;font-size:30px;letter-spacing:-.5px;color:#fff}
.xsp-xplan .chips{display:flex;gap:9px;margin-top:16px;flex-wrap:wrap}
.xsp-xplan .chip{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);border-radius:999px;
padding:8px 14px;font-size:12.5px;font-weight:700}
.xsp-xplan .price{position:relative;text-align:right}
.xsp-xplan .amt{font-style:italic;font-weight:900;font-size:34px}
.xsp-xplan .per{font-size:15px;font-weight:700;opacity:.85;font-style:normal}
.xsp-xplan .alt{font-size:13px;font-weight:700;color:rgba(255,255,255,.75);margin-top:4px}
.xsp-xplan .xsp-cta{margin-top:14px}
.xsp-cross{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.xsp-cross .xsp-promo .t{font-size:16.5px}
@media (max-width:809px){
.xsp-hubhero-grid{grid-template-columns:1fr;gap:28px;padding:32px 20px 52px}
.xsp-hubhero-grid .xsp-h1{font-size:34px}
.xsp-hub-photo{min-height:0}
.xsp-hub-photo .ph{height:200px}
.xsp-cut{height:44px;clip-path:polygon(0 55%,100% 0,100% 100%,0 100%)}
.xsp-promise-in{padding:0 20px}
.xsp-promise-items{display:grid;grid-template-columns:1fr 1fr;gap:8px 16px}
.xsp-hubsec-in{padding:0 20px}
.xsp-grid3,.xsp-grid4{grid-template-columns:1fr;gap:10px;margin-top:14px}
.xsp-xplan{grid-template-columns:1fr;padding:28px 22px;border-radius:20px}
.xsp-xplan .price{text-align:left}
.xsp-cross{grid-template-columns:1fr}
}
"""

def hub_hero(d):
    # The hub's photo box is .ph, not .xsp-photo, so photo_slot's wrapper doesn't fit
    # here — but the img itself must still honour photoPos, or a portrait source
    # silently centre-crops in a wide box.
    if d.get("photo"):
        pos = f' style="object-position:{d["photoPos"]}"' if d.get("photoPos") else ""
        hub_photo = (f'<img src="{d["photo"]}" alt="{d.get("photoAlt", "")}"{pos} '
                     f'loading="lazy" decoding="async">')
    else:
        hub_photo = d.get("photoLabel", "PHOTO — TEAM / INSTALL")
    return f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{X_MARK}" alt=""></div>
  <div class="xsp-hubhero-grid">
    <div>
      <span class="xsp-hub-pill"><span class="dot"></span>{d["eyebrow"]}</span>
      {h1(d["h1"], d["h1Highlight"])}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas">
        {schedule_btn("Schedule Service", "xsp-cta js-schedule")}
        <a class="xsp-cta-outline" href="{PHONE_TEL}">Call Now</a>
      </div>
    </div>
    <div class="xsp-hub-photo">
      <div class="slashw"></div><div class="slash"></div>
      <div class="ph">{hub_photo}</div>
    </div>
  </div>
</div>
<div class="xsp-cut"></div>'''

def promise_strip():
    items = ["Same-day in most cases", "Upfront pricing", "Licensed & insured", "Satisfaction guaranteed"]
    spans = "".join(f'<span><span class="di">◆</span> {i}</span>' for i in items)
    return f'''<div class="xsp-promise"><div class="xsp-promise-in">
  <div class="xsp-promise-label">THE EXTREME PROMISE</div>
  <div class="xsp-promise-items">{spans}</div>
</div></div>'''

def hub_core(d):
    cards = "".join(
        f'''<a class="xsp-card" href="{c["href"]}">
      <span class="glyphwrap"><span class="xsp-glyph"><i></i><i></i></span></span>
      <span class="txt"><span class="t">{c["title"]}</span><br><span class="d">{c["desc"]}</span></span>
      <span class="lm">Learn more →</span><span class="mrow">→</span>
    </a>''' for c in d["core"]
    )
    notsure = f'''<a class="xsp-notsure" href="{PHONE_TEL}">
      <span class="t">Not sure what you need?</span>
      <span class="d">Describe the problem — we'll point you the right way and get the right tech out.</span>
      <span class="lm">Call {PHONE_DISPLAY} →</span>
    </a>'''
    return f'''<div class="xsp-hubsec"><div class="xsp-hubsec-in">
  <div class="xsp-eyebrow">CORE SERVICES</div>
  <h2 class="xsp-h2">{d["coreH2"]}</h2>
  <div class="xsp-grid3">{cards}{notsure}</div>
</div></div>'''

def hub_additional(d):
    cards = "".join(
        f'''<a class="xsp-card" href="{c["href"]}">
      <span class="txt"><span class="t">{c["title"]}{f'<span class="xsp-badge">{c["badge"]}</span>' if c.get("badge") else ""}</span><br><span class="d">{c["desc"]}</span></span>
      <span class="lm">Learn more →</span><span class="mrow">→</span>
    </a>''' for c in d["additional"]
    )
    return f'''<div class="xsp-hubsec soft"><div class="xsp-hubsec-in">
  <div class="xsp-eyebrow purple">{d["additionalLabel"]}</div>
  <div class="xsp-grid4">{cards}</div>
</div></div>'''

# Every X-Plan fact the site states, in one place. Change a price here and it changes
# on the hub, the maintenance page, and all 38 location maintenance pages at once.
# Client-confirmed figures — see the extreme-brand skill before editing any of them.
# Members pay DISCOUNTED service call rates, never free: writing "$0" or "free" here
# would be wrong and is the mistake the handoff calls out by name.
XPLAN = {
    "annual": "$249",
    "monthly": "$20.75",
    "chips": ["Priority scheduling", "15% off repairs", "5-year repair warranty"],
    "detail": [
        "Both seasonal tune-ups included",
        "15% off repairs",
        "Priority scheduling",
        "Member service calls: $77 vs $97 · $177 vs $197 after hours",
    ],
}

def xplan_panel(detail=False):
    """The X-Plan band. `detail` adds the member benefit list the location maintenance
    pages carry; the pricing is the same object either way."""
    rows = ""
    if detail:
        rows = ('<ul class="xsp-xplan-detail">' +
                "".join(f'<li><span class="c">✓</span><span>{d}</span></li>'
                        for d in XPLAN["detail"]) + "</ul>")
    chips = "".join(f'<span class="chip">{c}</span>' for c in XPLAN["chips"])
    return f'''<div class="xsp-hubsec"><div class="xsp-hubsec-in">
  <a class="xsp-xplan js-schedule" href="#" role="button" aria-label="Join X-Plan — schedule service">
    <img class="mark" src="{CDN}/logo-white.png" alt="">
    <div>
      <div class="eyebrow">X-PLAN MAINTENANCE</div>
      <h2>Never think about tune-ups again.</h2>
      <div class="chips">{chips}</div>
      {rows}
    </div>
    <div class="price">
      <div class="amt">{XPLAN["annual"]}<span class="per"> / year</span></div>
      <div class="alt">or {XPLAN["monthly"]} / month per system</div>
      <span class="xsp-cta">Join X-Plan</span>
    </div>
  </a>
</div></div>'''

def specials_panel():
    return f'''<div class="xsp-hubsec"><div class="xsp-hubsec-in">
  <div class="xsp-xplan">
    <img class="mark" src="{CDN}/logo-white.png" alt="">
    <div>
      <div class="eyebrow">PLUMBING SPECIALS</div>
      <h2>Current offers on repairs and installs.</h2>
      <div class="chips"><span class="chip">Upfront pricing</span><span class="chip">Licensed plumbers</span><span class="chip">Same-day in most cases</span></div>
    </div>
    <div class="price"><a class="xsp-cta" href="/specials">View Specials</a></div>
  </div>
</div></div>'''

def hub_crosslinks(d):
    cards = "".join(
        f'''<a class="xsp-promo {c["cls"]}" href="{c["href"]}">
      <div class="t">{c["t"]}</div><div class="d">{c["d"]}</div><div class="lm">{c["lm"]}</div>
    </a>''' for c in d["cross"]
    )
    return f'''<div class="xsp-hubsec" style="padding-top:0"><div class="xsp-hubsec-in">
  <div class="xsp-cross">{cards}</div>
</div></div>'''

def hub_page(d, root_class):
    """Tier 1 — hub template (2c)."""
    panel = xplan_panel() if d.get("panel") == "xplan" else specials_panel()
    body = f'''{hub_hero(d)}
{promise_strip()}
{hub_core(d)}
{hub_additional(d)}
{panel}
{hub_crosslinks(d)}'''
    return page_shell(root_class, body)

CSS = CSS + HUB_CSS

# ------------------------------------------------ X-Plan membership page (3a)
XPLAN_CSS = """
.xsp-bookcol.pricing .price-row{display:flex;align-items:baseline;gap:8px;margin-top:10px}
.xsp-bookcol.pricing .amt{font-style:italic;font-weight:900;font-size:38px;color:var(--ink)}
.xsp-bookcol.pricing .per{font-weight:700;font-size:14px;color:var(--body)}
.xsp-bookcol.pricing .alt{font-size:13px;font-weight:600;color:var(--body);margin-top:4px}
.xsp-benefits{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.xsp-benefit{border:1px solid var(--rule);border-radius:16px;padding:18px;background:#fff;display:flex;gap:12px}
.xsp-benefit .c{width:18px;height:18px;flex:none;border-radius:50%;background:var(--green);color:#fff;
font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-top:2px}
.xsp-benefit .t{font-weight:800;font-size:15px;color:var(--ink)}
.xsp-benefit .d{font-size:13px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xsp-usecases{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px}
.xsp-usecase{border:1px solid var(--rule);border-radius:16px;padding:20px;background:#fff;display:flex;
flex-direction:column;gap:8px}
.xsp-usecase .t{font-weight:800;font-size:16.5px;color:var(--ink)}
.xsp-usecase .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body)}
.xsp-value{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;
padding:36px 40px;color:#fff;margin-top:20px}
.xsp-value .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:2px;color:var(--green-hover)}
.xsp-value h3{margin-top:10px;font-style:italic;font-weight:900;font-size:26px;letter-spacing:-.5px;color:#fff}
.xsp-value .stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;margin-top:22px}
.xsp-value .n{font-style:italic;font-weight:900;font-size:26px;color:#fff}
.xsp-value .cap{font-size:12.5px;line-height:1.5;font-weight:500;color:rgba(255,255,255,.75);margin-top:6px}
.xsp-joinband{background:var(--ink)}
.xsp-joinband-in{max-width:1280px;margin:0 auto;padding:20px 40px;display:flex;align-items:center;
justify-content:space-between;gap:24px;flex-wrap:wrap}
.xsp-joinband b{font-weight:800;font-size:15px;color:#fff}
.xsp-joinband span{font-size:13px;font-weight:500;color:rgba(255,255,255,.6)}
@media (max-width:809px){
.xsp-bookcol.pricing{display:block !important;margin:28px 0 0}
.xsp-benefits,.xsp-usecases{grid-template-columns:1fr;gap:12px}
.xsp-value{padding:26px 22px;border-radius:20px}
.xsp-value .stats{grid-template-columns:1fr;gap:18px}
.xsp-joinband-in{padding:20px;flex-direction:column;align-items:flex-start;gap:12px}
}
"""
CSS = CSS + XPLAN_CSS

# Join X-Plan CTA target — TODO: pending confirmation (ScheduleEngine vs signup form).
# Interim: anchors to the pricing card; marked with data-join-cta for one-pass wiring.
JOIN_HREF = "#xsp-pricing"

def pricing_card(pc):
    return f'''<div class="xsp-book" id="xsp-pricing">
  <div class="eyebrow">X-PLAN MEMBERSHIP</div>
  <div class="price-row"><span class="amt">$249</span><span class="per">/ year</span></div>
  <div class="alt">or $20.75 / month</div>
  <div class="btns">
    <a class="xsp-btn-green" href="{JOIN_HREF}" data-join-cta>Join X-Plan</a>
    {call_btn(f"Call {PHONE_DISPLAY}")}
  </div>
  <div class="trust"><span>Two visits a year</span><span class="bar">|</span><span>15% off all repairs</span></div>
</div>'''

def benefits_grid(b):
    cards = "".join(
        f'''<div class="xsp-benefit"><span class="c">✓</span>
        <div><div class="t">{c["t"]}</div><div class="d">{c["d"]}</div></div></div>''' for c in b["cards"])
    return f'''<div>
  <div class="xsp-eyebrow">WHAT'S INCLUDED</div>
  <h2 class="xsp-h2">{b["h2"]}</h2>
  <div class="xsp-benefits">{cards}</div>
</div>'''

def usecase_cards(u):
    cards = "".join(
        f'''<div class="xsp-usecase">
        <span class="xsp-glyph"><i></i><i></i></span>
        <span class="t">{c["t"]}</span><span class="d">{c["d"]}</span></div>''' for c in u["cards"])
    return f'''<div>
  <div class="xsp-eyebrow">IS X-PLAN FOR YOU?</div>
  <h2 class="xsp-h2">{u["h2"]}</h2>
  <div class="xsp-usecases">{cards}</div>
</div>'''

def value_panel(v):
    stats = "".join(
        f'<div><div class="n">{s["n"]}</div><div class="cap">{s["cap"]}</div></div>' for s in v["stats"])
    return f'''<div>
  <div class="xsp-value">
    <div class="eyebrow">DOES IT PAY FOR ITSELF?</div>
    <h3>{v["h2"]}</h3>
    <div class="stats">{stats}</div>
  </div>
</div>'''

def join_band(j):
    return f'''<div class="xsp-joinband"><div class="xsp-joinband-in">
  <div><b>{j["bold"]}</b> <span>{j["rest"]}</span></div>
  <a class="xsp-cta" href="{JOIN_HREF}" data-join-cta>Join X-Plan</a>
</div></div>'''

def xplan_page(d, root_class):
    """3a — detail anatomy, membership-flavored. No pill nav, no related strip,
    no site-wide X-Plan panel (the whole page is the X-Plan CTA)."""
    hero = f'''<div class="xsp-hero">
  <div class="xsp-hero-mark"><img src="{X_MARK}" alt=""></div>
  <div class="xsp-hero-grid">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      <p class="xsp-intro">{d["intro"]}</p>
      {chips(d["heroChips"])}
    </div>
    <div class="xsp-bookcol pricing">{pricing_card(d)}</div>
  </div>
</div>'''
    left = [
        benefits_grid(d["benefits"]),
        usecase_cards(d["useCases"]),
        value_panel(d["value"]),
        process(d["process"], eyebrow="HOW IT WORKS"),
        faq(d["faq"], d["faqEyebrow"], h2=None),
    ]
    rail_html = f'<aside class="xsp-rail">{promo("askJoin")}{promo("tuneUpNow")}</aside>'
    body = f'''{hero}
<div class="xsp-bodygrid">
  <div class="xsp-main">{"".join(left)}</div>
  {rail_html}
</div>
{join_band(d["joinBand"])}'''
    return page_shell(root_class, body)

PROMOS["askJoin"] = dict(cls="lav", t="Questions before joining?",
    d="Call us and we'll walk through whether X-Plan makes sense for your home.",
    lm=f"Call {PHONE_DISPLAY} →", href=PHONE_TEL)
PROMOS["tuneUpNow"] = dict(cls="mint", t="Due for a tune-up now?",
    d="Book a one-time visit and we'll get someone out. You can join X-Plan whenever you're ready.",
    lm="Schedule a Tune-Up →", href="#", schedule=True)
