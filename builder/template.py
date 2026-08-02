"""Service-page template system — design_handoff_services_pages.

Three tiers (detail / hub / subpage) assembled from shared section
renderers. Pages are emitted as self-contained <section> HTML embeds
matching the conventions of the existing service-page files.

Single source of truth for phone + asset URLs lives here.
"""
import re

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
ASSET_COMMIT = "033972506c03489eec477421491916a718bcfabc"

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
    "ruudCondenser": cdn_asset("equipment/ruud-condenser.jpg"),
    "ruudInstall":  cdn_asset("equipment/ruud-install.jpg"),
    # Real job photography, August 2026 — these replaced carried-over stock
    "acRepairGauges":   cdn_asset("service/ac-repair-gauges.jpg"),
    "acContactor":      cdn_asset("service/ac-contactor.jpg"),
    "furnaceService":   cdn_asset("service/furnace-service.jpg"),
    "furnaceRepairOpen": cdn_asset("service/furnace-repair-open.jpg"),
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

# ------------------------------------------------------- intrinsic image sizes
# Every <img> the builder emits carries width/height so the browser reserves the
# box before the bytes arrive. The numbers below are the REAL pixel dimensions of
# the files in assets/, read with PIL — not the rendered CSS size, and not a guess.
# They are a literal table because the builder is stdlib-only and stdlib has no
# image decoder.
#
# REGENERATE after adding, replacing or re-exporting anything under assets/:
#
#   python3 - <<'PY'
#   from PIL import Image; import os
#   for root, _, files in os.walk("assets"):
#       if os.path.basename(root) == "print": continue
#       for f in sorted(files):
#           if not f.lower().endswith((".jpg",".jpeg",".png",".webp",".avif",".gif")): continue
#           p = os.path.join(root, f)
#           with Image.open(p) as im: w, h = im.size
#           print(f'    "{os.path.relpath(p, "assets")}": ({w}, {h}),')
#   PY
#
# A file missing from this table emits no width/height rather than a wrong one —
# a wrong aspect ratio is a worse bug than an unsized image.
ASSET_DIMS = {
    "brand/apple-touch-icon.png": (180, 180),
    "brand/logo-white-tight.png": (410, 101),
    "brand/logo-white.avif": (502, 207),
    "brand/logo-white.png": (502, 207),
    "brand/logo.png": (504, 202),
    "brand/van-mock-up.jpg": (1400, 840),
    "brand/van.png": (1024, 576),
    "brand/x-mark.png": (420, 446),
    "brands/daikin.png": (900, 188),
    "brands/ruud.png": (648, 398),
    "brands/trane.png": (288, 96),
    "cities/beavercreek.jpg": (492, 327),
    "cities/bellbrook.jpg": (1024, 680),
    "cities/blue-ash.jpg": (600, 398),
    "cities/butler-county.jpg": (500, 534),
    "cities/centerville.jpg": (680, 452),
    "cities/cincinnati.jpg": (612, 408),
    "cities/clark-county.jpg": (500, 534),
    "cities/darke-county.jpg": (500, 534),
    "cities/dayton.jpg": (557, 370),
    "cities/englewood.jpg": (800, 531),
    "cities/fairborn.jpg": (928, 290),
    "cities/fairfield.jpg": (790, 440),
    "cities/franklin.jpg": (1024, 683),
    "cities/greene-county.jpg": (500, 534),
    "cities/huber.jpg": (689, 459),
    "cities/kettering.jpg": (469, 310),
    "cities/lebanon.jpg": (1400, 909),
    "cities/mason.jpg": (640, 311),
    "cities/miami-county.jpg": (500, 534),
    "cities/miamisburg.jpg": (814, 540),
    "cities/middletown.jpg": (1024, 1011),
    "cities/montgomery-county.jpg": (500, 534),
    "cities/moraine.jpg": (600, 400),
    "cities/northgate.jpg": (831, 711),
    "cities/oakwood.jpg": (498, 331),
    "cities/preble-county.jpg": (500, 534),
    "cities/riverside.jpg": (519, 345),
    "cities/sharonville.jpg": (319, 147),
    "cities/springboro.jpg": (1922, 1276),
    "cities/springfield.jpg": (2558, 1698),
    "cities/tipp.jpg": (1024, 683),
    "cities/troy.jpg": (1570, 883),
    "cities/vandalia.jpg": (510, 339),
    "cities/warren-county.jpg": (500, 534),
    "cities/wc.jpg": (708, 400),
    "cities/west-chester.jpg": (1280, 718),
    "cities/xenia.jpg": (1087, 801),
    "equipment/envirocon.jpg": (242, 230),
    "equipment/eruv1424v.jpg": (480, 450),
    "equipment/ge-water-heater-install.jpg": (1542, 2048),
    "equipment/muv-401h.jpg": (480, 450),
    "equipment/muv-403h.jpg": (480, 450),
    "equipment/ruud-condenser.jpg": (825, 1100),
    "equipment/ruud-heat-pump.jpg": (1050, 1400),
    "equipment/ruud-install.jpg": (625, 1600),
    "equipment/trane-install-2.jpg": (1512, 2016),
    "equipment/trane-install.jpg": (1512, 2016),
    "locations/apple-plumbing-van.jpg": (3537, 2267),
    "locations/beavercreek-office.jpg": (1400, 934),
    "locations/cinci.jpg": (680, 453),
    "locations/dayton-skyline-van.jpg": (1800, 1200),
    "locations/locations.jpg": (665, 663),
    "locations/mason-office.jpg": (1800, 1013),
    "locations/troy-community-event.jpg": (1050, 1400),
    "locations/vans-leaving.jpg": (1642, 1341),
    "service/ac-contactor.jpg": (1080, 810),
    "service/ac-dual.jpg": (1152, 806),
    "service/ac-install.jpg": (654, 661),
    "service/ac-maintenance.jpg": (500, 350),
    "service/ac-repair-gauges.jpg": (825, 1100),
    "service/ac-repair.jpg": (881, 661),
    "service/ac-replacement.jpg": (500, 350),
    "service/ac.jpg": (1152, 806),
    "service/air-quality.jpg": (600, 531),
    "service/beavercreek-img1.jpg": (1000, 667),
    "service/beavercreek-img2.jpg": (1000, 560),
    "service/beavercreek-img3.jpg": (1000, 560),
    "service/before-after-ducts.jpg": (600, 533),
    "service/chemical-air-quality.jpg": (600, 533),
    "service/common-signs-duct-system.jpg": (900, 675),
    "service/dirty-duct.jpg": (239, 210),
    "service/dirty-ducts2.jpg": (249, 152),
    "service/duct-air-quality.jpg": (600, 533),
    "service/duct-cleaning-tools.jpg": (940, 627),
    "service/duct-cleaning-truck.jpg": (600, 533),
    "service/duct-cleaning.jpg": (900, 724),
    "service/duct-technicians.jpg": (625, 438),
    "service/faq.jpg": (600, 531),
    "service/financing-options.jpg": (900, 724),
    "service/furnace-install.jpg": (379, 349),
    "service/furnace-repair-open.jpg": (825, 1100),
    "service/furnace-repair.jpg": (1100, 917),
    "service/furnace-replace.jpg": (500, 350),
    "service/furnace-service.jpg": (825, 1100),
    "service/furnace.jpg": (500, 350),
    "service/furnace2.jpg": (500, 350),
    "service/heatpump.jpg": (890, 623),
    "service/humidifier.jpg": (618, 432),
    "service/indoor-air-quality-services.jpg": (898, 629),
    "service/maintenance.jpg": (364, 255),
    "service/moisture-air-quality.jpg": (600, 533),
    "service/professional-duct-cleaning.jpg": (940, 513),
    "service/sale.jpg": (943, 840),
    "service/smart-thermostat.jpg": (730, 588),
    "service/thermostat.jpg": (898, 629),
    "team/anthony-griffin.jpg": (574, 766),
    "team/jayvon-kilgore.jpg": (574, 766),
    "team/joe-richardson.jpg": (496, 662),
    "team/tyler-hardy.jpg": (574, 766),
}

def asset_dims(src):
    """(width, height) of the file behind an assets/ URL, or None if it isn't in
    ASSET_DIMS. Works on the jsDelivr URLs the site serves today and on the plain
    /assets/... paths it will serve after cutover — both contain "/assets/"."""
    if not src:
        return None
    rel = src.split("?", 1)[0].split("#", 1)[0]
    marker = "/assets/"
    i = rel.find(marker)
    rel = rel[i + len(marker):] if i != -1 else rel.lstrip("/")
    d = ASSET_DIMS.get(rel)
    return d if d else None

def dim_attrs(src):
    """` width="W" height="H"` for an <img>, or "" when the file is unknown."""
    d = asset_dims(src)
    return f' width="{d[0]}" height="{d[1]}"' if d else ""

# ---------------------------------------------------------------- CSS
CSS = """
.xhac-svc{--purple:#542770;--purple-light:#5E2C7E;--purple-dark:#3A1A4E;--green:#6BB85C;
--green-hover:#8FD481;--green-dark:#4E9B41;--green-tint:#EEF7EC;--promo-green:#3D7A33;
--ink:#0F172A;--body:#475569;--muted:#94A3B8;--rule:#E7E7EA;--soft:#F7F6FA;--tint:#F4F1F8;
--stars:#F6A723;
/* "Montserrat Fallback" is the metric-overridden local face shell.py defines alongside
   the self-hosted woff2. It is what stops the swap from shifting layout — the measured
   CLS on this site is fonts, not images. An unknown family name is skipped by the
   browser, so this is inert until shell.py declares it. */
font-family:"Montserrat","Montserrat Fallback",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial;
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

/* booking card (hero overlap)
   align-self:end pins the card to the bottom of the hero grid so the -84px margin
   actually pulls it past the edge and it hangs over the section below. With
   align-self:start the card floated at the top of a taller row and the negative
   margin did nothing — which is why the service pages never overhung. Every page
   that renders a .xsp-bookcol also renders a body section below it, so the
   clearance on .xsp-bodygrid / .xco-body is unconditional. */
.xsp-bookcol{position:relative;margin-bottom:-84px;align-self:end}
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
/* Only the pages whose hero carries a booking card need clearance for it — the sub
   pages put that card in the rail instead, and padding them too would just open a
   48px hole. Scoped with :has() so no generator has to remember to flag it; a browser
   without :has() falls back to the plain 56px, which is what shipped before. */
.xhac-svc:has(.xsp-bookcol) .xsp-bodygrid{padding-top:104px}
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

/* media block — one photo or one video, full width of the main column */
.xsp-shot{position:relative;margin-top:20px;aspect-ratio:16 / 9;border-radius:14px;overflow:hidden;
background:#0F172A;border:1px solid var(--rule)}
.xsp-shot img,.xsp-shot iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.xsp-shot img{object-fit:cover}
.xsp-mediasub{margin-top:10px;font-size:14px;line-height:1.6;font-weight:500;color:var(--body);max-width:64ch}
.xsp-mediacap{margin-top:10px;font-size:12.5px;font-weight:600;color:var(--muted)}

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

/* ---------------------- GEO content model ----------------------
   Four pieces the copy needs and the old template had nowhere to put: the
   answer-first block, real H2/H3 body sections, decision tables, and a visible
   last-updated line. */

/* The answer-first block sits in the hero copy column, directly under the H1.
   It is the page's lead paragraph, not a callout: no box, no border, no tint, no
   rule. Size and weight carry it, and the deck below steps down so the order of
   importance reads correctly. Anything boxed here would look like an aside and get
   read as one. */
.xsp-answer{margin-top:18px;max-width:640px}
.xsp-answer p{font-size:18px;line-height:1.55;font-weight:600;color:#fff;letter-spacing:-.1px}
.xsp-answer p + p{margin-top:10px}
.xsp-answer + .xsp-intro{margin-top:12px;font-size:14.5px;color:rgba(255,255,255,.72)}

/* body sections: an H2 question, its direct answer, optional H3 sub-questions.
   .xsp-main already puts 48px between blocks, so a section owns only its internals. */
.xsp-h3{margin-top:24px;font-weight:800;font-size:18px;line-height:1.35;letter-spacing:-.2px;color:var(--ink)}
.xsp-prose{margin-top:12px;font-size:15px;line-height:1.65;font-weight:500;color:var(--body);max-width:68ch}
/* Contextual links in body copy. These are the site's internal-linking backbone — 139
   of them across the service pages — so they stay inline in the sentence where their
   anchor text means something, rather than becoming buttons. A 1px underline set off
   the baseline reads as a link without the heavy default rule cutting through the
   descenders. */
.xsp-prose a{color:var(--purple);font-weight:700;text-decoration:underline;
text-decoration-thickness:1px;text-underline-offset:3px;text-decoration-color:#C9B8D8}
.xsp-prose a:hover{color:var(--green-dark);text-decoration-color:currentColor}
/* A phone number in prose is a fact first and a link second. It keeps tel: so it is
   still tappable, but it is not competing with the contextual links around it — the
   button under the section is the thing meant to be pressed. */
.xsp-prose a[href^="tel:"]{color:var(--ink);text-decoration-color:#D9D4E0}
.xsp-prose a[href^="tel:"]:hover{color:var(--purple)}
/* The action row that closes a section whose answer is "call or book". */
.xsp-inlinecta{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}

/* The one-sentence takeaway that has to sit immediately above a table — engines lift
   it when they can't lift the table. Heavier than body copy, lighter than a heading. */
.xsp-takeaway{margin-top:18px;font-size:15.5px;line-height:1.6;font-weight:700;color:var(--ink);max-width:68ch}

/* Decision tables.
   Desktop: a purple header band, a tinted row-header column, hairline rules and a
   soft lift. The caption sits ABOVE the card rather than inside it — inside, it read
   as a stray label floating over the header row.
   Mobile (<=700px): the table becomes stacked cards. A four-column comparison in a
   390px scroller means reading one column at a time and losing the row you were on;
   as cards, each row is a self-contained "Factor: value, value, value" block. The
   markup stays a real <table> — only `display` changes — and table_block() adds the
   ARIA roles back, because display:block strips a table's implicit roles from the
   accessibility tree in Chrome and Firefox. */
.xsp-tablewrap{margin-top:14px;border:1px solid var(--rule);border-radius:14px;background:#fff;
overflow:hidden;overflow-x:auto;-webkit-overflow-scrolling:touch;
box-shadow:0 1px 2px rgba(15,23,42,.04),0 8px 24px -12px rgba(84,39,112,.18)}
.xsp-tablewrap:focus-visible{outline:2px solid var(--purple);outline-offset:2px}
.xsp-table{border-collapse:collapse;width:100%;min-width:560px;font-size:13.5px;line-height:1.55}
/* The table's title, sitting above the box as a sub-headline. Sentence case at
   reading size — as a tiny uppercase tracked-out label it read as chrome, and long
   ones are a wall of capitals. */
.xsp-tablelabel{margin:20px 0 10px;font-size:16.5px;line-height:1.45;font-weight:800;
color:var(--ink);max-width:68ch}
.xsp-tablelabel + .xsp-tablewrap{margin-top:0}
.xsp-table th,.xsp-table td{padding:13px 16px;text-align:left;vertical-align:top;
border-bottom:1px solid #EFECF3}
.xsp-table thead th{font-weight:800;font-size:11.5px;letter-spacing:.6px;text-transform:uppercase;
color:#fff;background:var(--purple);border-bottom:0;white-space:nowrap}
.xsp-table thead th:first-child{border-top-left-radius:13px}
.xsp-table thead th:last-child{border-top-right-radius:13px}
.xsp-table tbody th{font-weight:800;color:var(--ink);width:24%;background:#FAF8FC}
.xsp-table tbody td{font-weight:500;color:var(--body)}
.xsp-table tbody tr:last-child th,.xsp-table tbody tr:last-child td{border-bottom:0}
@media (hover:hover){.xsp-table tbody tr:hover td{background:#FBFAFC}}

/* Stacked cards under 700px. 700, not the site's 810 breakpoint: a three-column
   comparison is still readable on a tablet and only breaks down on a phone.
   The wrapper drops its border and shadow so the CARDS carry the styling — a card
   inside a card reads as a mistake. Column headers move into each cell via
   data-label, which table_block() writes. */
/* Two ranges, one treatment. Under 700px the viewport is the constraint. But from 810
   to ~1090 the RAIL is: .xsp-bodygrid is `1fr 360px` with a 48px gap and 40px padding,
   so the main column is viewport-488 — 322px at 810 and 536px at 1024, both under the
   table's 560px minimum. Left alone that band side-scrolls a four-column table inside
   a half-width column, which is worse than a phone. Between 700 and 809 the rail is
   hidden and the column is full width, so the table fits and stays a table. */
@media (max-width:699px), (min-width:810px) and (max-width:1090px){
  .xsp-tablewrap{border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}
  .xsp-table{min-width:0;display:block;font-size:14px}
  .xsp-tablelabel{font-size:15.5px;margin-top:18px}
  .xsp-table thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);
  clip-path:inset(50%);white-space:nowrap}
  .xsp-table tbody{display:block}
  .xsp-table tbody tr{display:block;background:#fff;border:1px solid var(--rule);border-radius:14px;
  padding:4px 0;margin-bottom:12px;box-shadow:0 1px 2px rgba(15,23,42,.04)}
  .xsp-table tbody tr:last-child{margin-bottom:0}
  /* The row header becomes the card title. */
  .xsp-table tbody th{display:block;width:auto;background:transparent;border-bottom:1px solid #EFECF3;
  font-size:15px;color:var(--ink);padding:12px 16px}
  /* Label above value, not beside it. Side by side looks tidy while column names are
     short ("Single-stage") and falls apart when they are not — "Replacement usually
     makes sense when" wraps to three lines against a one-line value and the pair
     stops reading as a pair. Stacked handles any length. */
  .xsp-table tbody td{display:block;border-bottom:1px solid #F5F3F8;padding:11px 16px 12px}
  .xsp-table tbody tr td:last-child{border-bottom:0}
  .xsp-table tbody td::before{content:attr(data-label);display:block;margin-bottom:3px;
  font-weight:800;font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:var(--purple)}
  .xsp-table tbody td>span{display:block}
}

/* Last updated. Quiet, but present — it has to match schema dateModified exactly. */
.xsp-updated{font-size:12.5px;font-weight:700;color:var(--muted)}

/* Click-to-load video facade. The YouTube iframe pulls ~835 KiB before anyone presses
   play; this is the poster, and the player replaces it on click. */
.xsp-shot .xsp-vplay{position:absolute;inset:0;width:100%;height:100%;border:0;cursor:pointer;
display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:24px;
background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);color:#fff;font-family:inherit;
text-align:center}
.xsp-vplay .pl{width:62px;height:62px;border-radius:50%;background:var(--green);color:var(--ink);
display:flex;align-items:center;justify-content:center;font-size:22px;padding-left:5px;
box-shadow:0 10px 28px rgba(0,0,0,.35);transition:background .15s,transform .15s}
.xsp-vplay:hover .pl{background:var(--green-hover);transform:scale(1.06)}
.xsp-vplay .vt{font-size:14.5px;font-weight:800;max-width:34ch;line-height:1.4}
.xsp-vplay .vh{font-size:11.5px;font-weight:700;letter-spacing:1.6px;color:rgba(255,255,255,.6)}

/* ------------------------- mobile (2b stacking) ------------------------- */
@media (max-width:809px){
.xsp-answer{max-width:none}
.xsp-answer p{font-size:16px;line-height:1.5}
.xsp-answer + .xsp-intro{font-size:13.5px}
.xsp-h3{font-size:16.5px;margin-top:20px}
.xsp-prose{font-size:14.5px}
.xsp-takeaway{font-size:14.5px}
.xsp-vplay .pl{width:52px;height:52px;font-size:19px}
.xsp-vplay .vt{font-size:13.5px}
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
.xsp-chiprow{gap:8px;justify-content:center}
.xsp-chip{padding:7px 10px;font-size:11px;border-radius:10px}
.xsp-bookcol{display:none}
.xsp-bodygrid{grid-template-columns:1fr;gap:40px;padding:40px 20px 48px}
/* the hero card is display:none here, so there is nothing to clear */
.xhac-svc:has(.xsp-bookcol) .xsp-bodygrid{padding-top:40px}
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
      // Video facade: swap the poster button for the real player on click, with
      // autoplay=1 so the press that loaded it also starts it. Nothing reaches
      // youtube.com until this runs.
      root.querySelectorAll(".js-video").forEach((btn) => {{
        btn.addEventListener("click", () => {{
          const id = btn.getAttribute("data-video");
          const title = btn.getAttribute("data-title") || "";
          if (!id) return;
          const f = document.createElement("iframe");
          f.setAttribute("src",
            "https://www.youtube.com/embed/" + id + "?rel=0&modestbranding=1&autoplay=1");
          f.setAttribute("title", title);
          f.setAttribute("allow",
            "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture");
          f.setAttribute("allowfullscreen", "");
          btn.replaceWith(f);
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
    # Every trail starts at Home. The service and plumbing pages used to start at
    # their own category, so 31 pages offered no way back to the homepage from the
    # breadcrumb while all 267 location pages did. Prepending here rather than in 31
    # data definitions keeps the two from drifting apart again; pages that already
    # start at Home are left alone.
    items = list(items)
    if not items or items[0][1] != "/":
        items = [("Home", "/")] + items
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

# --------------------------------------------------- GEO content model pieces
# Four optional page-data fields, all rendered by detail_page() and sub_page():
#
#   answer    str (or list of str) — the answer-first block. Renders as the FIRST
#             element after the <h1>, inside the hero copy column. id="answer" is
#             stable on purpose: speakable schema targets it by selector.
#   sections  [{h2, body, h3s?, table?, eyebrow?, id?}] — real <h2>/<h3> headings
#             with paragraphs, so a page can carry 5-7 H2s instead of three.
#             `sectionsTail` is the same shape, rendered after Process instead of
#             before it, for the sections that belong at the end of the page.
#   table     {caption, takeaway, columns, rows, h2?, eyebrow?} — a real <table>.
#   updated   human date string; `updatedISO` is the machine form. The visible line
#             and schema dateModified must be the same date.
#
# `body` is a string or a list of strings; each becomes one <p>. Copy is authored
# with HTML entities already in place (see esc), so nothing here escapes.

_PHONE_RX = re.compile(re.escape(PHONE_DISPLAY))

def autolink_phone(html):
    """Make every phone number in page text tappable.

    108 of them across 101 pages were plain text — readable on a desktop, useless on
    the phone someone is holding when their heat is out. Chasing the strings would
    only work until the next copy edit, so this runs over the assembled body instead.

    It walks tokens rather than regexing the whole document, because the number also
    appears inside href/aria-label/title attributes, inside anchors that are already
    links, and inside the <script> on /locations. Substituting there would produce a
    nested anchor or broken JavaScript. Only bare text nodes, outside <a>, <script>
    and <style>, are touched.
    """
    out, in_a, in_raw = [], 0, 0
    for tok in re.split(r"(<[^>]+>)", html):
        if tok.startswith("<"):
            low = tok.lower()
            if re.match(r"<a\b", low):
                in_a += 1
            elif low.startswith("</a"):
                in_a = max(0, in_a - 1)
            elif re.match(r"<(script|style)\b", low):
                in_raw += 1
            elif re.match(r"</(script|style)", low):
                in_raw = max(0, in_raw - 1)
            out.append(tok)
        elif in_a or in_raw:
            out.append(tok)
        else:
            out.append(_PHONE_RX.sub(
                f'<a href="{PHONE_TEL}">{PHONE_DISPLAY}</a>', tok))
    return "".join(out)

def paragraphs(body, cls="xsp-prose"):
    if not body:
        return ""
    items = body if isinstance(body, (list, tuple)) else [body]
    return "".join(f'<p class="{cls}">{p}</p>' for p in items)

def answer_block(d):
    """The answer-first block. Deliberately unstyled as a box: it is the page's lead
    paragraph, and a bordered callout reads as an aside instead of as the answer."""
    a = d.get("answer")
    if not a:
        return ""
    items = a if isinstance(a, (list, tuple)) else [a]
    return ('<div class="xsp-answer" id="answer">'
            + "".join(f"<p>{p}</p>" for p in items) + "</div>")

def table_block(t):
    """A real <table> — <caption>, <thead>, th scope=col, th scope=row — because an
    engine that cannot parse the table cannot cite it. The takeaway sentence goes
    immediately BEFORE the table; that is the sentence that gets lifted when the
    table itself doesn't. The wrapper carries overflow-x inline as well as in CSS so
    a wide table can never make the page scroll sideways, and it is focusable with a
    label so it can be scrolled from the keyboard."""
    # role="table"/"row"/"cell" are redundant on a real table and normally worth
    # leaving off — but under 700px the CSS sets display:block on these elements,
    # and Chrome and Firefox drop a table's implicit roles the moment it stops being
    # display:table. Without these the cards are read as a pile of unrelated text.
    cols = list(t["columns"])
    head = "".join(f'<th scope="col">{c}</th>' for c in cols)
    rows = []
    for r in t["rows"]:
        cells = list(r)
        first = f'<th scope="row" role="rowheader">{cells[0]}</th>'
        # data-label supplies the column name as a prefix inside each stacked card;
        # the value is wrapped so it can be right-aligned against that label.
        rest = "".join(
            f'<td role="cell" data-label="{cols[i + 1]}"><span>{c}</span></td>'
            for i, c in enumerate(cells[1:]))
        rows.append(f'<tr role="row">{first}{rest}</tr>')
    # The title is a sub-headline ABOVE the box, not a <caption> inside it. As a
    # caption it broke twice: in card mode the table is display:block, which took the
    # caption's width with it and stacked the words one per line; and on desktop the
    # wrapper's overflow clipped the left edge of any caption wider than the table.
    # Out here it is just a line of text, so it can neither be squeezed nor clipped.
    # It still names the table for assistive tech, via aria-labelledby rather than the
    # caption element.
    caption = t.get("caption")
    label = ""
    labelled = ""
    if caption:
        tid = "tbl-" + re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", caption).lower()).strip("-")[:48]
        label = f'<p class="xsp-tablelabel" id="{tid}">{caption}</p>'
        labelled = f' aria-labelledby="{tid}"'
    # tabindex makes the scroll box reachable from the keyboard, which is the whole
    # point of a scrolling container. role="region" only goes on when there is a name
    # to give it — an unnamed region is worse than no region.
    region = f' role="region"{labelled}' if caption else ""
    takeaway = f'<p class="xsp-takeaway">{t["takeaway"]}</p>' if t.get("takeaway") else ""
    # No inline overflow-x here any more: under 700px the CSS sets overflow:visible so
    # the cards flow, and an inline style would win over it and reinstate the scroller.
    return (f'{takeaway}{label}<div class="xsp-tablewrap" '
            f'tabindex="0"{region}>'
            f'<table class="xsp-table" role="table"{labelled}>'
            f"<thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody>"
            f"</table></div>")

def table_section(t):
    """A table standing on its own as a page section, with its own heading."""
    eyebrow = f'<div class="xsp-eyebrow purple">{t["eyebrow"]}</div>' if t.get("eyebrow") else ""
    heading = f'<h2 class="xsp-h2">{t["h2"]}</h2>' if t.get("h2") else ""
    sid = f' id="{t["id"]}"' if t.get("id") else ""
    return f'<div class="xsp-section"{sid}>{eyebrow}{heading}{table_block(t)}</div>'

def content_section(s):
    """One body section: an <h2> question, the direct answer under it, then any <h3>
    sub-questions with their own answers, then an optional table."""
    parts = []
    if s.get("eyebrow"):
        cls = "" if s.get("eyebrowColor", "green") == "green" else " purple"
        parts.append(f'<div class="xsp-eyebrow{cls}">{s["eyebrow"]}</div>')
    parts.append(f'<h2 class="xsp-h2">{s["h2"]}</h2>')
    parts.append(paragraphs(s.get("body")))
    for sub in s.get("h3s", []):
        parts.append(f'<h3 class="xsp-h3">{sub["h3"]}</h3>')
        parts.append(paragraphs(sub.get("body")))
    if s.get("table"):
        parts.append(table_block(s["table"]))
    # An optional action row. A section whose answer IS "call or book" should end in a
    # button, not in an underlined phone number buried mid-paragraph — the number stays
    # in the prose because that is the sentence an AI answer lifts, but the tap target
    # is a real button. cta: True gives the standard Schedule + Call pair; a dict gives
    # a single custom link, e.g. {"label": "Explore X-Plan", "href": "/maintenance"}.
    cta = s.get("cta")
    if cta is True:
        parts.append(f'<div class="xsp-inlinecta">{schedule_btn("Schedule Service", "xsp-cta")}'
                     f'<a class="xsp-cta-outline" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div>')
    elif isinstance(cta, dict):
        parts.append(f'<div class="xsp-inlinecta">'
                     f'<a class="xsp-cta" href="{cta["href"]}">{cta["label"]}</a></div>')
    sid = f' id="{s["id"]}"' if s.get("id") else ""
    return f'<div class="xsp-section"{sid}>{"".join(parts)}</div>'

def content_sections(items):
    """List form, so an assembler can splice it straight into its column."""
    return [content_section(s) for s in (items or [])]

def updated_line(text, iso=None):
    """Visible "Last updated" line. This date and schema dateModified have to match
    exactly — engines read the rendered text and compare. Pass `updatedISO` through
    to shell.py for the schema side; never stamp either from the build clock."""
    if not text:
        return ""
    dt = f' datetime="{iso}"' if iso else ""
    return f'<p class="xsp-updated">Last updated <time{dt}>{text}</time></p>'

def hero_mark():
    """The decorative X watermark behind every hero.

    Carries its intrinsic size so it can never shift layout. It is also, today, the
    measured LCP element on every page type — a 33 KB PNG drawn at 6% opacity that
    says nothing. Replacing it with an inline SVG moves LCP to real content and drops
    662 requests sitewide (performance.md §6.2); that swap is blocked only on
    [NEEDS: an SVG of the X mark], and when it arrives it happens in this function."""
    return (f'<div class="xsp-hero-mark">'
            f'<img src="{X_MARK}" alt="" aria-hidden="true"{dim_attrs(X_MARK)}></div>')

# Sub pages carry the same three proof points on every page, so they are a default
# here rather than repeated in every page's data. A page can still override them by
# setting heroChips, the same key the detail pages use.
# Kept short on purpose: the row is 344px wide, which is inside the narrowest overview
# page's chip row, so a sub page never wraps to two lines where its own overview sits
# on one. "20+ Years Locally Owned" and "24/7 Emergency Service" pushed it to 459px
# and wrapped on every phone.
SUB_CHIPS = ["4.9 on Google", "Locally Owned", "24/7 Emergency"]

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
  {hero_mark()}
  <div class="xsp-hero-grid">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      {answer_block(d)}
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
    """Same anatomy as hero_detail: booking card in the hero, overhanging the section
    below, and the CTA pair in the copy column reduced to a mobile fallback for when
    the card is hidden. The sub pages used to be the one page type without the card
    in the hero — it lived inline in the rail, so it never overhung anything."""
    label = d.get("scheduleLabel", "Schedule Service")
    return f'''<div class="xsp-hero sub">
  {hero_mark()}
  <div class="xsp-hero-grid">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      {answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      <div class="xsp-hero-ctas xsp-mb">
        {schedule_btn(label, "xsp-cta js-schedule")}
        <a class="xsp-cta-outline" href="{PHONE_TEL}">Call Now</a>
      </div>
      {chips(d.get("heroChips", SUB_CHIPS))}
    </div>
    <div class="xsp-bookcol">{booking_card(d["bookingCard"], schedule_label=label)}</div>
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

# The FAQ heading every page used to carry, verbatim. It is a slogan, it is identical
# on 311 pages, and it wastes the strongest H2 slot on the page — so pages can now set
# `faqH2` to a question and get a heading that earns its place. Kept as the default so
# nothing that has not been rewritten changes. `faqH2: None` drops the heading entirely.
DEFAULT_FAQ_H2 = "Your questions, answered."

def faq(f, eyebrow, h2=DEFAULT_FAQ_H2):
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

def photo_slot(label="PHOTO — TECH AT UNIT", src=None, alt="", pos=None, eager=False):
    """pos sets object-position for sources whose subject isn't centred. The slot is
    360x220 landscape and the image is object-fit:cover, so a portrait photo shows
    only a horizontal band of itself — pos is how you choose which band.

    `eager` is for the copy of this slot that is actually the LCP element. On mobile
    that is the photo at the top of the body (mobile_photo); lazy-loading the LCP
    image delays it by a whole round trip. Both copies of the rail photo share one
    URL, so marking both eager is still one request."""
    if src:
        style = f' style="object-position:{pos}"' if pos else ""
        load = (' fetchpriority="high" decoding="async"' if eager
                else ' loading="lazy" decoding="async"')
        return (f'<div class="xsp-photo"><img src="{src}" alt="{alt}"{style}'
                f'{dim_attrs(src)}{load}></div>')
    return f'<div class="xsp-photo" data-photo-slot>{label}</div>'

def rail(r, flush=False, extra=""):
    parts = []
    if r.get("photo") or r.get("photoSlot"):
        parts.append(photo_slot(r.get("photoLabel", "PHOTO — TECH AT UNIT"),
                                r.get("photo"), r.get("photoAlt", ""), r.get("photoPos"),
                                eager=True))
    parts += [promo(k) for k in r["promos"]]
    return f'<aside class="xsp-rail{" flush" if flush else ""}">{extra}{"".join(parts)}</aside>'

def sibling_links(s):
    links = "".join(
        f'<a href="{it["href"]}">{it["title"]}<span class="ar">→</span></a>' for it in s["items"]
    )
    return f'<div class="xsp-sibs"><div class="h">{s["label"]}</div>{links}</div>'

def media_block(m):
    """One piece of evidence in the main column — a photo or a video, full width of
    the column at 16:9. Deliberately one per block: a photo and a video side by side
    never share a height (a 4:3 frame next to a 16:9 player leaves a hole under the
    shorter one), so each gets its own section and its own heading."""
    if m.get("photo"):
        pos = m.get("photoPos", "50% 50%")
        shot = (f'<div class="xsp-shot"><img src="{m["photo"]}" alt="{m.get("photoAlt", "")}" '
                f'style="object-position:{pos}"{dim_attrs(m["photo"])} '
                f'loading="lazy" decoding="async"></div>')
    else:
        # Click-to-load facade. loading="lazy" does nothing for a YouTube iframe —
        # measured, it still pulls ~835 KiB of player JavaScript on load. Nothing
        # third-party is requested until someone presses play, and the button is a
        # real <button> so it works from the keyboard.
        shot = (f'<div class="xsp-shot">'
                f'<button type="button" class="xsp-vplay js-video" '
                f'data-video="{m["video"]}" data-title="{m["videoTitle"]}" '
                f'aria-label="Play video: {m["videoTitle"]}">'
                f'<span class="pl" aria-hidden="true">&#9654;</span>'
                f'<span class="vt">{m["videoTitle"]}</span>'
                f'<span class="vh">WATCH ON YOUTUBE</span>'
                f'</button></div>')
    sub = f'<p class="xsp-mediasub">{m["sub"]}</p>' if m.get("sub") else ""
    cap = f'<p class="xsp-mediacap">{m["caption"]}</p>' if m.get("caption") else ""
    return f'''<div>
  <div class="xsp-eyebrow">{m["eyebrow"]}</div>
  <h2 class="xsp-h2">{m["h2"]}</h2>
  {sub}
  {shot}
  {cap}
</div>'''

def related(rel):
    cards = "".join(
        f'''<a class="xsp-rel-card" href="{r["href"]}"><span class="t">{r["title"]}</span><span class="lm xsp-dt">Learn more →</span><span class="lm xsp-mb">→</span></a>'''
        for r in rel
    )
    return f'''<div class="xsp-rel"><div class="xsp-rel-in">
  <div class="xsp-eyebrow purple">KEEP EXPLORING</div>
  <div class="xsp-rel-grid">{cards}</div>
</div></div>'''

def mobile_inline_rail(d):
    """2b: the financing/x-plan promos flow inline after Process on mobile, where the
    rail itself is display:none."""
    parts = [promo(k) for k in d["rail"]["promos"]]
    return f'<div class="xsp-mbrail xsp-mb">{"".join(parts)}</div>'

def mobile_photo(r):
    """The rail photo's mobile home: the top of the body, directly under the pill nav.
    It rode along with the promos for a while, which dropped it halfway down the page
    between two text sections — it read as an interruption rather than as the page's
    image."""
    if not r.get("photo"):
        return ""
    return ('<div class="xsp-mbphoto xsp-mb">'
            + photo_slot("", r["photo"], r.get("photoAlt", ""), r.get("photoPos"),
                         eager=True)
            + "</div>")

# ------------------------------------------------------------ assemblers
def page_shell(root_class, body):
    return f'''<section class="xhac-svc {root_class}">
  <style>{CSS}</style>
{body}
{script("xhac-svc")}
</section>
'''

def detail_page(d, root_class):
    """Tier 2 — detail template (2a/2b). Optional pillNav → 2e combo.

    Optional GEO fields: `answer`, `sections`, `table`, `sectionsTail`, `faqH2`,
    `updated` / `updatedISO`. Section order in the main column is

      symptoms → whatWeDo → sections → media → process → table → sectionsTail
      → FAQ → last updated

    so `sections` carries the questions that set up the page and `sectionsTail`
    the ones that follow from the process. Everything is optional; a page that
    supplies none of it renders exactly as it did before."""
    left = [mobile_photo(d["rail"]), checklist(d["symptoms"])]
    if d.get("whatWeDo"):
        left.append(what_we_do(d["whatWeDo"]))
    left += content_sections(d.get("sections"))
    for m in d.get("media", []):
        left.append(media_block(m))
    left.append(process(d["process"]))
    if d.get("table"):
        left.append(table_section(d["table"]))
    left += content_sections(d.get("sectionsTail"))
    left.append(mobile_inline_rail(d))
    left.append(faq(d["faq"], d["faqEyebrow"], h2=d.get("faqH2", DEFAULT_FAQ_H2)))
    left.append(updated_line(d.get("updated"), d.get("updatedISO")))
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
    """Tier 3 — sub-page template (2d).

    Same optional GEO fields as detail_page(). Order in the main column is

      symptoms → sections → process → decision → table → sectionsTail
      → FAQ → last updated

    The table sits after the decision card on purpose: on the repair pages the card
    asks the repair-or-replace question and the table answers it."""
    left = [mobile_photo(d["rail"]), checklist(d["symptoms"])]
    left += content_sections(d.get("sections"))
    left.append(process(d["process"]))
    if d.get("decision"):
        left.append(decision_card(d["decision"]))
    if d.get("table"):
        left.append(table_section(d["table"]))
    left += content_sections(d.get("sectionsTail"))
    left.append(mobile_inline_rail(d))
    left.append(faq(d["faq"], d["faqEyebrow"], h2=d.get("faqH2", DEFAULT_FAQ_H2)))
    left.append(updated_line(d.get("updated"), d.get("updatedISO")))
    # The booking card moved into the hero (see hero_sub), so the rail is photo first
    # then the promo and sibling links — the same rail the detail pages carry.
    photo = ""
    if d["rail"].get("photo"):
        photo = photo_slot("", d["rail"]["photo"], d["rail"].get("photoAlt", ""),
                           d["rail"].get("photoPos"), eager=True)
    rail_html = f'''<aside class="xsp-rail flush">{photo}{promo(d["rail"]["promos"][0])}{sibling_links(d["siblings"])}</aside>'''
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
        hub_photo = (f'<img src="{d["photo"]}" alt="{d.get("photoAlt", "")}"{pos}'
                     f'{dim_attrs(d["photo"])} loading="lazy" decoding="async">')
    else:
        hub_photo = d.get("photoLabel", "PHOTO — TEAM / INSTALL")
    return f'''<div class="xsp-hero">
  {hero_mark()}
  <div class="xsp-hubhero-grid">
    <div>
      <span class="xsp-hub-pill"><span class="dot"></span>{d["eyebrow"]}</span>
      {h1(d["h1"], d["h1Highlight"])}
      {answer_block(d)}
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
    <img class="mark" src="{CDN}/logo-white.png" alt="" aria-hidden="true" width="502" height="207">
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
    <img class="mark" src="{CDN}/logo-white.png" alt="" aria-hidden="true" width="502" height="207">
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
  {hero_mark()}
  <div class="xsp-hero-grid">
    <div>
      {crumbs(d["breadcrumb"])}
      {h1(d["h1"], d["h1Highlight"])}
      {answer_block(d)}
      <p class="xsp-intro">{d["intro"]}</p>
      {chips(d["heroChips"])}
    </div>
    <div class="xsp-bookcol pricing">{pricing_card(d)}</div>
  </div>
</div>'''
    left = [
        benefits_grid(d["benefits"]),
        usecase_cards(d["useCases"]),
    ]
    left += content_sections(d.get("sections"))
    left += [
        value_panel(d["value"]),
        process(d["process"], eyebrow="HOW IT WORKS"),
    ]
    if d.get("table"):
        left.append(table_section(d["table"]))
    left += content_sections(d.get("sectionsTail"))
    # This page has always suppressed the FAQ heading — the eyebrow carries it — so
    # its default stays None rather than DEFAULT_FAQ_H2.
    left.append(faq(d["faq"], d["faqEyebrow"], h2=d.get("faqH2")))
    left.append(updated_line(d.get("updated"), d.get("updatedISO")))
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
