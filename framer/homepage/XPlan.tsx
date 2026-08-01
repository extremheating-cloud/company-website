import * as React from "react"
import {
    COLORS,
    GRADIENTS,
    SHADOWS,
    FONT_STACK,
    ensureMontserrat,
    ASSETS,
    openScheduleDialog,
} from "https://framer.com/m/Theme-cgWgED.js@B2PNlINgwl1DTpD88aOo"

const PERKS = [
    "Priority Scheduling",
    "Reduced Service Fee",
    "15% Off All Repairs",
    "5-Year Repair Warranty",
]

const INCLUDES = [
    "Two Safety & Performance Visits a Year",
    "Multi-Point Air Conditioner Tune-Up and Service",
    "Calibrate Refrigerant Charge up to 1 lb Included",
    "Heating System Safety Checkup and Service",
    "Detailed Evaluation and Efficiency Measurements",
    "Airflow Adjustments as Needed",
    "Thermostat Calibration and Configuration",
    "Professional Recommendations to Prolong Equipment Life",
]

function XPlan() {
    React.useEffect(ensureMontserrat, [])

    return (
        <section className="xp-section">
            <style>{CSS}</style>
            <div className="xp-wrap">
                <div className="xp-panel">
                    <img
                        className="xp-mark"
                        src={ASSETS.logoWhite}
                        alt=""
                        aria-hidden
                    />
                    <div className="xp-grid">
                        <div className="xp-left">
                            <div className="xp-eyebrow">X-PLAN MEMBERSHIP</div>
                            <h2 className="xp-h2">
                                The smart way to protect your home's comfort
                                &amp; savings.
                            </h2>
                            <div className="xp-zri">
                                <div className="xp-zri-label">
                                    ZERO RISK INVESTMENT
                                </div>
                                <p className="xp-zri-copy">
                                    100% of the investment of your X-Plan
                                    membership in consecutive years is applied
                                    toward your end-of-life equipment
                                    replacement — up to $2,500 or 10 years.
                                </p>
                            </div>
                            <p className="xp-body">
                                Two visits a year keep your system running
                                efficiently and catch small problems while
                                they're still small.
                            </p>
                            <div className="xp-chips">
                                {PERKS.map((p) => (
                                    <span key={p} className="xp-chip">
                                        {p}
                                    </span>
                                ))}
                            </div>
                            <div className="xp-price-row">
                                <span className="xp-price">
                                    $249<span className="per">/year</span>
                                </span>
                                <span className="xp-alt">
                                    or $20.75/month
                                </span>
                                <button
                                    type="button"
                                    className="xp-join"
                                    onClick={openScheduleDialog}
                                >
                                    Join X-Plan&nbsp;&nbsp;→
                                </button>
                            </div>
                        </div>

                        <div className="xp-card">
                            <div className="xp-card-label">
                                WHAT'S INCLUDED
                            </div>
                            <ul className="xp-list">
                                {INCLUDES.map((item) => (
                                    <li key={item}>
                                        <span className="chk" aria-hidden>
                                            ✓
                                        </span>
                                        {item}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}


const CSS = `
.xp-section, .xp-section *{ box-sizing:border-box; font-family:${FONT_STACK} }
.xp-section{ background:#fff; padding:34px 0 60px }
.xp-wrap{ max-width:1280px; margin:0 auto; padding:0 40px }

.xp-panel{
  position:relative; overflow:hidden; border-radius:24px; padding:46px;
  background:${GRADIENTS.xplan}; color:#fff;
}
.xp-mark{
  position:absolute; right:-40px; bottom:-46px; width:340px; opacity:.06;
  pointer-events:none; filter:brightness(0) invert(1);
}
.xp-grid{
  position:relative; display:grid; grid-template-columns:1.08fr .92fr; gap:44px; align-items:center;
}

.xp-eyebrow{
  font-size:11.5px; font-weight:800; letter-spacing:2px; text-transform:uppercase;
  color:${COLORS.greenHoverOnDark}; margin-bottom:12px;
}
.xp-h2{
  font-style:italic; font-weight:900; font-size:33px; letter-spacing:-.5px; line-height:1.18;
  color:#fff; margin:0 0 14px;
}
/* Zero Risk Investment leads the section per programs.md — it is the only benefit
   competitors don't also offer. Both conditions (consecutive years, $2,500 or 10
   years) must appear wherever the accrual is stated. */
.xp-zri{
  background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.28);
  border-left:4px solid ${COLORS.green}; border-radius:14px; padding:16px 18px; margin:0 0 16px;
}
.xp-zri-label{ font-size:10.5px; font-weight:800; letter-spacing:1.8px; color:${COLORS.greenHoverOnDark} }
.xp-zri-copy{ margin:6px 0 0; font-size:14.5px; line-height:1.6; font-weight:600; color:#fff }
.xp-body{ font-size:15px; line-height:1.65; font-weight:500; color:rgba(255,255,255,.85); margin:0 0 18px }
.xp-chips{ display:flex; flex-wrap:wrap; gap:9px; margin-bottom:22px }
.xp-chip{
  border:1px solid rgba(255,255,255,.3); background:rgba(255,255,255,.1);
  border-radius:999px; padding:8px 14px; font-size:12.5px; font-weight:700;
}
.xp-price-row{ display:flex; align-items:center; gap:16px; flex-wrap:wrap }
.xp-price{ font-style:italic; font-weight:900; font-size:34px; letter-spacing:-.5px }
.xp-price .per{ font-size:16px; font-weight:700; font-style:normal; opacity:.85; margin-left:2px }
.xp-alt{ font-size:13.5px; font-weight:700; color:rgba(255,255,255,.75) }
.xp-join{
  display:inline-flex; align-items:center; justify-content:center; min-height:44px;
  background:${COLORS.green}; color:${COLORS.ink}; font-weight:800; font-size:15px;
  border:none; border-radius:12px; padding:12px 24px; cursor:pointer; font-family:inherit;
  box-shadow:${SHADOWS.greenGlowLight}; transition:background .15s ease;
}
.xp-join:hover{ background:${COLORS.greenHoverOnDark} }
.xp-join:focus-visible{ outline:2px solid #fff; outline-offset:2px }

.xp-card{
  background:#fff; border-radius:16px; padding:26px 28px; color:${COLORS.ink};
  box-shadow:${SHADOWS.xplanCard};
}
.xp-card-label{
  font-size:11.5px; font-weight:800; letter-spacing:2px; color:${COLORS.purple};
  margin-bottom:14px;
}
.xp-list{
  list-style:none; margin:0; padding:0;
  display:grid; grid-template-columns:1fr 1fr; gap:9px 18px;
}
.xp-list li{
  display:flex; align-items:center; gap:9px; font-size:13.5px; font-weight:600; color:${COLORS.body};
}
/* greenDark on greenTint is 3.15:1 — white on the accessible green clears AA at 4.56:1 */
.xp-list .chk{
  width:18px; height:18px; flex:none; border-radius:999px; background:#3F852B;
  color:#fff; font-size:11px; font-weight:800; display:grid; place-items:center;
}

@media (max-width: 899px){
  .xp-section{ padding:22px 0 44px }
  .xp-wrap{ padding:0 20px }
  .xp-panel{ padding:28px 22px; border-radius:20px }
  .xp-grid{ grid-template-columns:1fr; gap:24px }
  .xp-h2{ font-size:24px }
  .xp-price-row{ gap:12px }
  .xp-join{ width:100%; min-height:48px }
  .xp-card{ padding:20px }
  .xp-list{ grid-template-columns:1fr; gap:8px }
  .xp-mark{ width:220px; right:-30px; bottom:-30px }
}
`

export default XPlan
