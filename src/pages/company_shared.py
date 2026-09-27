from layout import components as T

PHOTOS = T.PHOTOS

# must match the schema dateModified for these routes; never stamp from the build clock
UPDATED = "August 2, 2026"
UPDATED_ISO = "2026-08-02"

COMPANY_CSS = """
.xco-2col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.xco-bcard{border:1px solid var(--rule);border-radius:16px;padding:20px;background:#fff}
.xco-bcard .t{font-weight:800;font-size:16.5px;margin-top:12px}
.xco-bcard .d{font-size:13.5px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xco-bcard .xsp-cta{margin-top:14px;font-size:14px;padding:12px 18px}
.xco-bcard .plink{display:inline-block;font-weight:800;font-size:14px;color:var(--purple);
text-decoration:none;margin-top:16px;min-height:44px;display:inline-flex;align-items:center}
.xco-bcard .plink:hover{color:var(--green-dark)}
.xco-phone{font-style:italic;font-weight:900;font-size:27px;letter-spacing:-.5px;margin-top:8px}
.xco-phone a{color:var(--ink);text-decoration:none}
.xco-loc{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}
.xco-loc-img{height:160px;background:#F4F6F8;border-bottom:1px solid var(--rule);display:flex;
align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:1px}
.xco-loc-img img{width:100%;height:100%;object-fit:cover;display:block}
.xco-loc-body{padding:18px}
.xco-loc-body .t{font-weight:800;font-size:16.5px}
.xco-loc-body .meta{font-size:12px;font-weight:700;color:var(--body);margin-top:2px}
.xco-loc-body .addr{font-size:13px;line-height:1.55;font-weight:500;color:var(--body);margin-top:4px}
.xco-loc-body .addr.hrs{font-size:12.5px;margin-top:6px}
.xco-loc-body a{display:inline-block;font-weight:800;font-size:13px;color:var(--purple);
text-decoration:none;margin-top:10px}
.xco-loc-body a.tel{display:block;margin-top:6px;font-size:13.5px;color:var(--ink)}
.xco-sms{margin-top:8px;font-size:14px;font-weight:600;color:var(--ink)}
.xco-sms a{color:var(--purple);text-decoration:none}
.xco-sms a:hover{text-decoration:underline}
.xco-loc-body a.tel:hover{color:var(--purple)}
.xco-loc-body a.alt{display:block;margin-top:6px}
.xco-loc-body a:hover{color:var(--green-dark)}
.xco-loc:not(:has(.xco-loc-img)) .xco-loc-body{padding-top:22px}
.xco-hours{border:1px solid var(--rule);border-radius:16px;margin-top:20px;overflow:hidden}
.xco-hours .row{display:flex;justify-content:space-between;gap:16px;padding:14px 20px;
border-bottom:1px solid var(--rule)}
.xco-hours .row:last-child{border-bottom:0}
.xco-hours .row span:first-child{font-weight:700;font-size:14px}
.xco-hours .row span:last-child{font-weight:600;font-size:14px;color:var(--body);text-align:right}
.xco-hours .row.em{background:var(--green-tint)}
.xco-hours .row.em span{font-weight:800;color:var(--promo-green)}
.xco-body{max-width:1280px;margin:0 auto;padding:56px 40px;display:flex;flex-direction:column;gap:48px}
.xhac-svc:has(.xsp-bookcol) .xco-body{padding-top:104px}
.xco-split{display:grid;grid-template-columns:1fr 360px;gap:48px}
.xco-heroslot{width:100%;height:auto;aspect-ratio:1600/470;border-radius:16px;
background:rgba(255,255,255,.08);
border:1px solid rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;
font-size:12px;font-weight:700;color:rgba(255,255,255,.55);letter-spacing:1px;overflow:hidden}
.xco-heroslot img{width:100%;height:100%;object-fit:cover;display:block}
.xco-hero-grid-400{grid-template-columns:1fr;gap:30px}
.xco-hero-grid-400 > div:first-child{max-width:70ch}
.xco-ccard{border:1px solid var(--rule);border-radius:16px;padding:18px;background:#fff}
.xco-ccard .c{width:18px;height:18px;border-radius:50%;background:var(--green);color:#fff;
font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center}
.xco-ccard .t{font-weight:800;font-size:15px;margin-top:10px}
.xco-ccard .d{font-size:13px;line-height:1.5;font-weight:500;color:var(--body);margin-top:4px}
.xco-lchips{display:flex;align-items:center;gap:10px;margin-top:22px;flex-wrap:wrap}
.xco-lchips .lab{font-size:10.5px;font-weight:800;letter-spacing:1.5px;color:rgba(255,255,255,.5)}
.xco-lchips .chip{border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);
border-radius:999px;padding:7px 14px;font-size:12px;font-weight:700;color:#fff}
.xco-fine{font-size:11px;font-weight:600;color:rgba(255,255,255,.45);margin-top:14px}
.xco-coupons{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px}
.xco-coupon{border:1.5px dashed #C4B5D4;border-radius:16px;padding:20px;display:flex;flex-direction:column}
.xco-coupon .pill{align-self:flex-start;background:var(--tint);color:var(--purple);font-size:10px;
font-weight:800;letter-spacing:1.5px;border-radius:999px;padding:5px 10px}
.xco-coupon .val{font-style:italic;font-weight:900;font-size:34px;letter-spacing:-1px;margin-top:12px}
.xco-coupon .val .per{font-size:16px;letter-spacing:0}
.xco-coupon .t{font-weight:800;font-size:15.5px;margin-top:2px}
.xco-coupon .d{font-size:13px;line-height:1.5;font-weight:500;color:var(--body);margin-top:4px;flex:1}
.xco-coupon .foot{display:flex;align-items:center;justify-content:space-between;gap:12px;
margin-top:16px;padding-top:14px;border-top:1px solid #EDEAF2}
.xco-coupon .lbl{font-size:11.5px;font-weight:700;color:var(--muted)}
.xco-claim{display:inline-flex;align-items:center;justify-content:center;background:var(--green);
color:var(--ink);font-weight:800;font-size:13px;padding:10px 16px;border-radius:10px;min-height:40px;
text-decoration:none;cursor:pointer;white-space:nowrap;transition:background .15s ease}
.xco-claim:hover{background:var(--green-hover)}
.xco-finenote{font-size:11.5px;line-height:1.6;font-weight:600;color:var(--muted);margin-top:24px}
.xco-mail{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:16px;
padding:22px;position:relative;overflow:hidden;color:#fff}
.xco-mail .t{font-weight:800;font-size:16px}
.xco-mail .d{font-size:12.5px;line-height:1.55;font-weight:500;color:rgba(255,255,255,.75);margin-top:6px}
.xco-mail form{display:flex;gap:8px;margin-top:14px}
.xco-mail input{flex:1;min-width:0;background:#fff;border:0;border-radius:10px;padding:12px 14px;
font-size:13px;font-weight:600;color:var(--ink);font-family:inherit}
.xco-mail button{background:var(--green);color:var(--ink);font-weight:800;font-size:13px;
padding:12px 16px;border-radius:10px;border:0;cursor:pointer;font-family:inherit}
.xco-story{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.xco-story p{margin-top:16px;font-size:14.5px;line-height:1.65;font-weight:500;color:var(--body)}
.xco-story p + p{margin-top:12px}
.xco-slot{width:100%;border-radius:16px;background:#F4F6F8;border:1px solid var(--rule);
display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;
color:var(--muted);letter-spacing:1px;overflow:hidden}
.xco-slot img{width:100%;height:100%;object-fit:cover;display:block}
.xco-vals{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
.xco-vals .xco-ccard .xsp-glyph{width:26px;height:26px}
.xco-vals .xco-ccard .t{margin-top:12px}
.xco-stats{background:linear-gradient(135deg,#5E2C7E,#542770 45%,#3E1C54);border-radius:24px;
padding:32px 36px;position:relative;overflow:hidden}
.xco-stats .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;position:relative}
.xco-stats .n{font-style:italic;font-weight:900;font-size:30px;color:#fff}
.xco-stats .n .st{color:var(--stars)}
.xco-stats .cap{font-size:12.5px;line-height:1.5;font-weight:600;color:rgba(255,255,255,.75);margin-top:4px}
.xco-crew + .xco-crew{margin-top:30px}
.xco-crew-hd{display:flex;align-items:center;gap:10px;padding-bottom:9px;
border-bottom:2px solid var(--rule);margin-bottom:16px}
.xco-crew-hd h3{margin:0;font-size:15px;font-weight:800;letter-spacing:-.01em;color:var(--ink)}
.xco-crew-hd .n{font-size:12px;font-weight:700;color:var(--muted);font-variant-numeric:tabular-nums}
.xco-team{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:20px 14px}
.xco-mem{margin:0}
/* height:auto — aspect-ratio is ignored once the height attr is set */
.xco-mem img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:12px;
display:block;background:var(--tint)}
.xco-mem figcaption{margin-top:9px}
.xco-mem .nm{display:block;font-weight:800;font-size:13.5px;color:var(--ink);line-height:1.25}
.xco-mem .rl{display:block;font-size:11.5px;font-weight:600;color:var(--body);line-height:1.3;
margin-top:2px}
.xco-team-lead{grid-template-columns:repeat(2,minmax(0,1fr));max-width:460px;gap:20px}
.xco-team-lead .nm{font-size:15px}
.xco-team-lead .rl{font-size:12.5px}
@media (max-width:809px){
.xco-2col{grid-template-columns:1fr;gap:12px;margin-top:16px}
.xco-hours .row{padding:13px 16px}
.xco-body{padding:40px 20px 48px;gap:40px}
.xhac-svc:has(.xsp-bookcol) .xco-body{padding-top:40px}
.xco-split{grid-template-columns:1fr;gap:40px}
.xco-heroslot{margin-top:22px}
.xco-coupons{grid-template-columns:1fr;gap:12px}
.xco-story{grid-template-columns:1fr;gap:20px}
.xco-story .xco-slot{height:200px}
.xco-vals{grid-template-columns:1fr;gap:12px}
.xco-stats{padding:26px 22px;border-radius:20px}
.xco-stats .grid{grid-template-columns:1fr 1fr;gap:18px}
}
@media (max-width:359px){
.xco-team{grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:16px 10px}
.xco-mem .nm{font-size:12.5px}
.xco-mem .rl{font-size:10px}
}
"""

def shell(root_class, body, extra_css=""):
    return f'''<section class="xhac-svc {root_class}">
  <style>{T.CSS}{COMPANY_CSS}{extra_css}</style>
{body}
{T.script("xhac-svc")}
</section>
'''

def section(eyebrow, h2, inner, lead=None, sid=None):
    anchor = f' id="{sid}"' if sid else ""
    return f'''<div{anchor}>
  <div class="xsp-eyebrow">{eyebrow}</div>
  <h2 class="xsp-h2">{h2}</h2>
  {T.paragraphs(lead)}
{inner}
</div>'''

def prose_section(eyebrow, h2, body, sid=None):
    return section(eyebrow, h2, "", lead=body, sid=sid)

def slot_img(cls, photo, label, style=""):
    st = f' style="{style}"' if style else ""
    if not photo:
        return f'<div class="{cls}"{st} data-photo-slot>{label}</div>'
    p = f' style="object-position:{photo["pos"]}"' if photo.get("pos") else ""
    return (f'<div class="{cls}"{st}><img src="{photo["src"]}" alt="{photo.get("alt","")}"{p} '
            f'loading="lazy" decoding="async"></div>')
