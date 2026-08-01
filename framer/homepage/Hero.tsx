import * as React from "react"
import {
    COLORS,
    GRADIENTS,
    FONT_STACK,
    ensureMontserrat,
    PHONE_DISPLAY,
    PHONE_TEL,
    ASSETS,
    openScheduleDialog,
} from "https://framer.com/m/Theme-cgWgED.js@B2PNlINgwl1DTpD88aOo"

const ROTATING_WORDS = ["Repairs", "Installs", "Tune-Ups", "Plumbing"]
const GOOGLE_RATING = "4.9"

type Service = {
    label: string
    sub: string
    subShort: string
    href: string
}

const HVAC_SERVICES: Service[] = [
    { label: "Cooling", sub: "AC repair, replacement, and tune-ups.", subShort: "AC repair, replacement, and tune-ups.", href: "/air-conditioning" },
    { label: "Heating", sub: "Furnace repairs, installs, and safety checks.", subShort: "Furnace repairs, installs, and safety checks.", href: "/furnace-heating" },
    { label: "Maintenance Plans", sub: "Bi-annual tune-ups and priority service.", subShort: "Bi-annual tune-ups and priority service.", href: "/maintenance" },
    { label: "Airflow & Ducts", sub: "Duct cleaning and air balancing.", subShort: "Duct cleaning and air balancing.", href: "/duct-cleaning" },
    { label: "Heat Pumps", sub: "Year-round efficiency with heat pump systems.", subShort: "Year-round efficiency with heat pump systems.", href: "/heat-pump" },
    { label: "Indoor Air Quality", sub: "Filtration, UV, and humidity control.", subShort: "Filtration, UV, and humidity control.", href: "/indoor-air-quality" },
]

const PLUMBING_SERVICES: Service[] = [
    { label: "Drain Cleaning", sub: "Fast help for clogged and slow drains.", subShort: "Clogged & slow drains.", href: "/plumbing/clogged-drain" },
    { label: "Sump Pump", sub: "Protection against basement water issues.", subShort: "Basement water protection.", href: "/plumbing/sump-pump/overview" },
    { label: "Water Heaters", sub: "Repair and replacement for hot water systems.", subShort: "Repair & replacement.", href: "/plumbing/water-heater/overview" },
    { label: "Leak Detection", sub: "Find and repair hidden plumbing leaks quickly.", subShort: "Find hidden leaks fast.", href: "/plumbing/leak-detection" },
    { label: "Gas Line", sub: "Safe installation and repair for gas piping.", subShort: "Safe install & repair.", href: "/plumbing/gas-line/overview" },
    { label: "Water Treatment", sub: "Filtration and conditioning for cleaner water.", subShort: "Cleaner water at home.", href: "/plumbing/water-treatment" },
]

function XGlyph({ size = 30 }: { size?: number }) {
    const inset = `${Math.round(size * (9.5 / 26) * 10) / 10}px 2px`
    const bar: React.CSSProperties = {
        position: "absolute",
        inset,
        borderRadius: 2,
    }
    return (
        <span
            aria-hidden
            style={{
                position: "relative",
                display: "block",
                width: size,
                height: size,
                flexShrink: 0,
            }}
        >
            <span
                style={{
                    ...bar,
                    background: COLORS.purple,
                    transform: "rotate(45deg)",
                }}
            />
            <span
                style={{
                    ...bar,
                    background: COLORS.green,
                    transform: "rotate(-45deg)",
                }}
            />
        </span>
    )
}

function RollingWord() {
    return (
        <span className="xh-roll-window">
            <span className="xh-roll">
                {[...ROTATING_WORDS, ROTATING_WORDS[0]].map((w, i) => (
                    <span key={i} className="xh-word">
                        {w}
                    </span>
                ))}
            </span>
        </span>
    )
}

function Hero() {
    React.useEffect(ensureMontserrat, [])

    return (
        <div className="xh-root">
            <style>{CSS}</style>

            <section className="xh-hero">
                <img
                    className="xh-hero-mark"
                    src={ASSETS.xMark}
                    alt=""
                    aria-hidden
                />
                <div className="xh-hero-grid">
                    <div className="xh-hero-copy">
                        <span className="xh-badge">
                            <span className="dot" aria-hidden />
                            <span className="xh-dt">
                                LOCALLY OWNED · DAYTON + CINCINNATI
                            </span>
                            <span className="xh-mb">
                                DAYTON + CINCINNATI · 24/7
                            </span>
                        </span>

                        <h1 className="xh-h1 xh-dt">
                            Trusted Team
                            <br />
                            for <RollingWord />
                        </h1>
                        <h1 className="xh-h1 xh-mb">
                            Trusted Team for
                            <br />
                            <RollingWord />
                        </h1>

                        <p className="xh-lede xh-dt">
                            Fast repairs, full system replacements, routine
                            maintenance, and dependable plumbing help —
                            delivered by a team your neighbors already trust.
                        </p>
                        <p className="xh-lede xh-mb">
                            Fast repairs, replacements, maintenance, and
                            plumbing help from a team your neighbors trust.
                        </p>

                        <div className="xh-cta-row">
                            <button
                                type="button"
                                className="xh-btn-green"
                                onClick={openScheduleDialog}
                            >
                                Schedule Service&nbsp;&nbsp;→
                            </button>
                            <a href={PHONE_TEL} className="xh-btn-outline">
                                Call&nbsp;{PHONE_DISPLAY}
                            </a>
                        </div>

                        <div className="xh-trust-row xh-dt">
                            <span className="xh-trust-chip">
                                <span className="stars">★★★★★</span>
                                {GOOGLE_RATING} on Google
                            </span>
                            <span className="xh-trust-chip">
                                20+ Years Locally Owned
                            </span>
                            <span className="xh-trust-chip">
                                <span className="dot" aria-hidden />
                                24/7 Emergency
                            </span>
                        </div>
                        <div className="xh-trust-row xh-mb">
                            <span className="xh-trust-chip">
                                <span className="stars">★★★★★</span>
                                {GOOGLE_RATING}
                            </span>
                            <span className="xh-trust-chip">20+ yrs</span>
                            <span className="xh-trust-chip">
                                <span className="dot" aria-hidden />
                                24/7
                            </span>
                        </div>

                        <div className="xh-van-stage xh-mb">
                            <div className="xh-slash" aria-hidden />
                            <img
                                src={ASSETS.van}
                                alt="Extreme van"
                                className="xh-van"
                            />
                        </div>
                    </div>

                    <div className="xh-van-col xh-dt">
                        <div className="xh-slash" aria-hidden />
                        <div className="xh-slash-white" aria-hidden />
                        <img
                            src={ASSETS.van}
                            alt="Extreme van"
                            className="xh-van"
                        />
                    </div>
                </div>
                <div className="xh-cut" aria-hidden />
            </section>

            <section className="xh-promise xh-dt">
                <div className="xh-promise-row">
                    <div className="xh-promise-label">THE EXTREME PROMISE</div>
                    <div className="xh-promise-items">
                        <span>
                            <b className="dia">◆</b> Licensed &amp; Insured
                        </span>
                        <span>
                            <b className="dia">◆</b> Free Replacement Estimates
                        </span>
                        <span>
                            <b className="dia">◆</b> Financing Available
                        </span>
                        <span>
                            <b className="dia">◆</b> X-Plan from $20.75/mo
                        </span>
                    </div>
                </div>
            </section>
            <section className="xh-promise-m xh-mb">
                <span>◆ Licensed &amp; Insured</span>
                <span>◆ Free Estimates</span>
                <span>◆ Financing Available</span>
                <span>◆ X-Plan $20.75/mo</span>
            </section>

            <section className="xh-svc hvac">
                <div className="xh-wrap">
                    <div className="xh-svc-head">
                        <div>
                            <div className="xh-eyebrow green">
                                OUR HVAC SERVICES
                            </div>
                            <h2 className="xh-h2 xh-dt">
                                Comfort solutions for every season of the year.
                            </h2>
                            <h2 className="xh-h2 xh-mb">
                                Comfort for every season.
                            </h2>
                            <p className="xh-svc-body xh-dt">
                                Explore our major heating, cooling, air
                                quality, and maintenance services designed to
                                keep your home comfortable year-round.
                            </p>
                        </div>
                        <a
                            href="/services"
                            className="xh-viewall xh-dt"
                        >
                            View All HVAC Services →
                        </a>
                    </div>
                    <div className="xh-card-grid">
                        {HVAC_SERVICES.map((s) => (
                            <a
                                key={s.label}
                                href={s.href}
                                className="xh-card bordered"
                            >
                                <span className="glyph-lg xh-dt">
                                    <XGlyph size={30} />
                                </span>
                                <span className="glyph-sm xh-mb">
                                    <XGlyph size={26} />
                                </span>
                                <span className="txt">
                                    <span className="t">{s.label}</span>
                                    <span className="d">{s.sub}</span>
                                    <span className="lm xh-dt">
                                        Learn more →
                                    </span>
                                </span>
                                <span className="mrow-arrow xh-mb" aria-hidden>
                                    →
                                </span>
                            </a>
                        ))}
                    </div>
                    <a href="/services" className="xh-viewall-m xh-mb">
                        View All HVAC Services →
                    </a>
                </div>
            </section>

            <section className="xh-svc soft">
                <div className="xh-wrap">
                    <div className="xh-svc-head">
                        <div>
                            <div className="xh-eyebrow purple">
                                OUR PLUMBING SERVICES
                            </div>
                            <h2 className="xh-h2 xh-dt">
                                Reliable help for your home plumbing systems.
                            </h2>
                            <h2 className="xh-h2 xh-mb">
                                Reliable home plumbing help.
                            </h2>
                            <p className="xh-svc-body xh-dt">
                                Explore our major drain, water heater, and leak
                                detection services designed to keep your
                                home's plumbing running reliably.
                            </p>
                        </div>
                        <a
                            href="/plumbing/services"
                            className="xh-viewall xh-dt"
                        >
                            View All Plumbing Services →
                        </a>
                    </div>
                    <div className="xh-card-grid plumbing">
                        {PLUMBING_SERVICES.map((s) => (
                            <a
                                key={s.label}
                                href={s.href}
                                className="xh-card flat"
                            >
                                <span className="glyph-lg xh-dt">
                                    <XGlyph size={30} />
                                </span>
                                <span className="txt">
                                    <span className="t">{s.label}</span>
                                    <span className="d xh-dt">{s.sub}</span>
                                    <span className="d xh-mb">
                                        {s.subShort}
                                    </span>
                                    <span className="lm xh-dt">
                                        Learn more →
                                    </span>
                                </span>
                            </a>
                        ))}
                    </div>
                    <a
                        href="/plumbing/services"
                        className="xh-viewall-m xh-mb"
                    >
                        View All Plumbing Services →
                    </a>
                </div>
            </section>
        </div>
    )
}


const CSS = `
.xh-root, .xh-root *{ box-sizing:border-box; font-family:${FONT_STACK} }
.xh-wrap{ max-width:1280px; margin:0 auto; padding:0 40px }

.xh-dt{ }
.xh-mb{ display:none !important }

.xh-hero{ position:relative; overflow:hidden; background:${GRADIENTS.hero}; color:#fff }

.xh-hero-mark{
  position:absolute; right:-90px; top:16px; width:620px; opacity:.07;
  transform:rotate(-8deg); filter:brightness(0) invert(1); pointer-events:none;
}
.xh-hero-grid{
  position:relative; max-width:1280px; margin:0 auto;
  display:grid; grid-template-columns:1fr .95fr; gap:32px;
  padding:56px 40px 0;
}
.xh-hero-copy{ padding-bottom:clamp(56px, 8.6vw, 110px) }
.xh-badge{
  display:inline-flex; align-items:center; gap:8px;
  border:1px solid rgba(255,255,255,.3); background:rgba(255,255,255,.1);
  border-radius:999px; padding:7px 14px; font-size:11px; font-weight:800; letter-spacing:1.6px; color:#fff;
}
.xh-badge .dot{ width:7px; height:7px; border-radius:50%; background:${COLORS.green} }
.xh-h1{
  margin:20px 0 0; font-style:italic; font-weight:900; font-size:56px; line-height:1.06;
  letter-spacing:-1px; color:#fff;
}
.xh-roll-window{
  display:inline-block; height:1.08em; overflow:hidden; vertical-align:bottom; color:${COLORS.green};
}
.xh-roll{ display:block; animation:xhRoll 9s cubic-bezier(.85,0,.15,1) infinite }
.xh-word{ display:block; height:1.08em }
@keyframes xhRoll{
  0%,17%{ transform:translateY(0) }
  22%,42%{ transform:translateY(-1.08em) }
  47%,67%{ transform:translateY(-2.16em) }
  72%,92%{ transform:translateY(-3.24em) }
  100%{ transform:translateY(-4.32em) }
}
@media (prefers-reduced-motion: reduce){
  .xh-roll{ animation:none }
}
.xh-lede{
  margin:18px 0 0; font-size:16px; line-height:1.65; color:rgba(255,255,255,.82);
  max-width:500px; font-weight:500;
}
.xh-cta-row{ display:flex; gap:12px; margin-top:28px }
.xh-btn-green{
  display:inline-flex; align-items:center; justify-content:center;
  background:${COLORS.green}; color:${COLORS.ink}; font-weight:800; font-size:15.5px;
  padding:15px 26px; border:none; border-radius:12px; cursor:pointer; text-decoration:none;
  box-shadow:0 8px 24px rgba(0,0,0,.25); font-family:inherit; transition:background .15s ease;
}
.xh-btn-green:hover{ background:${COLORS.greenHoverOnDark} }
.xh-btn-green:focus-visible{ outline:2px solid #fff; outline-offset:2px }
.xh-btn-outline{
  display:inline-flex; align-items:center; justify-content:center;
  border:1.5px solid rgba(255,255,255,.45); color:#fff; font-weight:800; font-size:15.5px;
  padding:15px 26px; border-radius:12px; text-decoration:none; background:transparent;
  transition:border-color .15s ease, color .15s ease;
}
.xh-btn-outline:hover{ border-color:${COLORS.green}; color:${COLORS.green} }
.xh-btn-outline:focus-visible{ outline:2px solid #fff; outline-offset:2px }
.xh-trust-row{ display:flex; gap:10px; margin-top:30px; flex-wrap:wrap }
.xh-trust-chip{
  display:inline-flex; align-items:center; gap:8px;
  border:1px solid rgba(255,255,255,.22); background:rgba(255,255,255,.08);
  border-radius:12px; padding:10px 14px; font-size:12.5px; font-weight:700; color:#fff;
}
.xh-trust-chip .stars{ color:${COLORS.stars}; letter-spacing:1.5px; font-size:11px }
.xh-trust-chip .dot{ width:7px; height:7px; border-radius:50%; background:${COLORS.green} }

.xh-van-col{
  position:relative; width:100%; align-self:end; min-height:0;
  aspect-ratio:569 / 480; max-height:480px;
}
.xh-van-col .xh-slash{
  position:absolute; left:-10.5%; right:-14%; bottom:20%; height:13.3%;
  background:${COLORS.green}; transform:rotate(-9deg) skewX(-16deg);
  box-shadow:0 20px 60px rgba(0,0,0,.3);
}
.xh-van-col .xh-slash-white{
  position:absolute; left:-3.5%; right:-21%; bottom:17.5%; height:3.75%;
  background:#fff; opacity:.25; transform:rotate(-9deg) skewX(-16deg);
}
.xh-van-col .xh-van{
  position:absolute; left:50%; bottom:20%; transform:translateX(-52%);
  width:104%; max-width:660px; filter:drop-shadow(0 24px 30px rgba(0,0,0,.35));
}

.xh-cut{
  position:relative; height:84px; background:#fff;
  clip-path:polygon(0 62%, 100% 0, 100% 100%, 0 100%);
}

.xh-promise{ background:#fff }
.xh-promise-row{
  max-width:1280px; margin:0 auto; display:flex; justify-content:space-between;
  align-items:center; padding:10px 40px 26px;
}
.xh-promise-label{ font-size:12px; font-weight:800; letter-spacing:1.8px; color:${COLORS.muted} }
.xh-promise-items{ display:flex; gap:26px; flex-wrap:wrap }
.xh-promise-items span{ font-size:12.5px; font-weight:700; color:${COLORS.body} }
.xh-promise-items .dia{ color:${COLORS.green}; font-weight:400 }
.xh-promise-m{
  grid-template-columns:1fr 1fr; gap:8px;
  padding:4px 20px 24px; background:#fff; font-size:11px; font-weight:700; color:${COLORS.body};
}

.xh-svc{ background:#fff; padding:60px 0 68px }
.xh-svc.soft{ background:${COLORS.softBg} }
.xh-svc-head{ display:flex; align-items:flex-end; justify-content:space-between; gap:24px; margin-bottom:26px }
.xh-eyebrow{ font-size:11.5px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px }
.xh-eyebrow.green{ color:${COLORS.greenDark} }
.xh-eyebrow.purple{ color:${COLORS.purple} }
.xh-h2{
  font-style:italic; font-weight:900; font-size:33px; letter-spacing:-.5px; line-height:1.15;
  color:${COLORS.ink}; margin:0 0 12px;
}
.xh-svc-body{ font-size:15px; line-height:1.6; font-weight:500; color:${COLORS.body}; max-width:560px; margin:0 }
.xh-viewall{
  flex:none; font-size:14px; font-weight:800; color:${COLORS.purple}; text-decoration:none;
  padding:8px 0; transition:color .15s ease;
}
.xh-viewall:hover{ color:${COLORS.greenDark} }
.xh-card-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px }
.xh-card{
  display:flex; flex-direction:column; gap:12px; text-decoration:none;
  border-radius:16px; padding:22px; background:#fff;
  transition:box-shadow .18s ease, border-color .18s ease, transform .18s ease;
}
.xh-card .txt{ display:flex; flex-direction:column; gap:6px }
.xh-card.bordered{ border:1px solid ${COLORS.border} }
.xh-card.flat{ box-shadow:0 1px 2px rgba(15,23,42,.05) }
.xh-card:hover{ box-shadow:0 12px 30px rgba(84,39,112,.12); transform:translateY(-2px) }
.xh-card.bordered:hover{ border-color:#D8CCE4 }
.xh-card .t{ font-size:16.5px; font-weight:800; color:${COLORS.ink} }
.xh-card .d{ font-size:13.5px; line-height:1.55; font-weight:500; color:${COLORS.body} }
.xh-card .lm{ font-size:13px; font-weight:800; color:${COLORS.purple}; margin-top:2px }
.xh-card:hover .lm{ color:${COLORS.greenDark} }
.xh-card:focus-visible{ outline:2px solid ${COLORS.purple}; outline-offset:2px }
.xh-viewall-m{ display:none }

@media (max-width: 899px){
  .xh-dt{ display:none !important }
  .xh-mb{ display:revert !important }

  .xh-promise-m.xh-mb{ display:grid !important }
  .xh-trust-row.xh-mb{ display:flex !important }
  .xh-van-stage.xh-mb{ display:block !important }

  .xh-wrap{ padding:0 20px }
  .xh-hero{ background:${GRADIENTS.heroMobile} }
  .xh-hero-mark{ right:-60px; top:30px; width:300px }
  .xh-hero-grid{ grid-template-columns:1fr; gap:0; padding:24px 20px 0 }
  .xh-hero-copy{ padding-bottom:0 }
  .xh-badge{ gap:7px; padding:6px 12px; font-size:10px; letter-spacing:1.3px }
  .xh-badge .dot{ width:6px; height:6px }
  .xh-h1{ margin:16px 0 0; font-size:36px; line-height:1.08; letter-spacing:-.5px }
  .xh-h1.xh-mb .xh-roll-window{ font-size:42px }
  .xh-lede{ margin:14px 0 0; font-size:14px; line-height:1.6 }
  .xh-cta-row{ flex-direction:column; gap:10px; margin-top:20px }
  .xh-btn-green{ width:100%; font-size:15px; padding:15px; min-height:48px }
  .xh-btn-outline{ width:100%; font-size:15px; padding:14px; min-height:48px }
  .xh-trust-row.xh-mb{ justify-content:center; gap:8px; margin-top:16px }
  .xh-trust-chip{ gap:6px; border-radius:10px; padding:7px 10px; font-size:11px }
  .xh-trust-chip .stars{ font-size:10px; letter-spacing:1px }
  .xh-trust-chip .dot{ width:6px; height:6px }

  .xh-van-stage.xh-mb{ position:relative; aspect-ratio:350 / 210; margin-top:10px }
  .xh-van-stage .xh-slash{
    position:absolute; left:-11.4%; right:-11.4%; bottom:25.7%; height:19%;
    background:${COLORS.green}; transform:rotate(-7deg) skewX(-14deg);
  }
  .xh-van-stage .xh-van{
    position:absolute; left:50%; bottom:26.7%; transform:translateX(-50%);
    width:100%; filter:drop-shadow(0 16px 20px rgba(0,0,0,.35));
  }
  .xh-cut{ height:44px; clip-path:polygon(0 55%, 100% 0, 100% 100%, 0 100%) }

  .xh-svc{ padding:36px 0 }
  .xh-svc.hvac{ border-top:1px solid #F1F0F4 }
  .xh-eyebrow{ font-size:10.5px; letter-spacing:1.8px; margin-bottom:0 }
  .xh-h2{ margin:8px 0 0; font-size:24px; letter-spacing:-.4px }
  .xh-svc-head{ margin-bottom:16px }

  .xh-card-grid{ grid-template-columns:1fr; gap:0 }
  .xh-card.bordered{
    flex-direction:row; align-items:center; gap:12px; border:none; border-radius:0;
    border-bottom:1px solid #F1F0F4; padding:13px 0; background:transparent;
  }
  .xh-card.bordered:hover{ box-shadow:none; transform:none }
  .xh-card.bordered .txt{ flex:1; gap:1px }
  .xh-card.bordered .t{ font-size:14.5px }
  .xh-card.bordered .d{ font-size:11.5px; line-height:1.45 }
  .xh-card.bordered .mrow-arrow{ color:${COLORS.purple}; font-weight:800 }

  .xh-card-grid.plumbing{ grid-template-columns:1fr 1fr; gap:10px; margin-top:16px }
  .xh-card.flat{ padding:14px; border-radius:14px; box-shadow:none }
  .xh-card.flat:hover{ box-shadow:none; transform:none }
  .xh-card.flat .t{ font-size:13.5px }
  .xh-card.flat .d{ font-size:11px; margin-top:3px; line-height:1.45 }

  .xh-viewall-m.xh-mb{
    display:inline-block !important; margin-top:14px;
    font-size:13px; font-weight:800; color:${COLORS.purple}; text-decoration:none;
  }
}
`

export default Hero
