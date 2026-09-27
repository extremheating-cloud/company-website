import * as React from "react"
import {
    COLORS,
    FONT_STACK,
    ensureMontserrat,
} from "https://framer.com/m/Theme-cgWgED.js@B2PNlINgwl1DTpD88aOo"

// Manufacturer logos, supplied by the client from each brand's dealer portal.
// Transparent PNGs, full colour — the grey is a CSS filter, so a pre-greyed logo
// could never light up on hover. Transparent padding was trimmed off each canvas
// so object-fit compares the marks themselves rather than three different canvases.
const BRAND_COMMIT = "c83bf3b6254c9bd3dbc1bd101024085c183abd20" // pin to a commit SHA after pushing changed assets
const BRAND_CDN =
    "https://cdn.jsdelivr.net/gh/extremheating-cloud/company-website@" +
    BRAND_COMMIT +
    "/assets/brands/"

// `scale` is optical balance, not a bug. object-fit normalises each logo's bounding
// box, so a wide wordmark ends up width-constrained and renders visibly smaller than
// a squarer mark beside it. Nudge these per brand once the real files are in — 1 is
// the baseline, 1.15 makes a mark bigger, 0.9 smaller. Judge it by eye at desktop
// width; every logo row needs this.
const BRANDS = [
    { name: "Trane", file: "trane.png", scale: 1 },
    { name: "Ruud", file: "ruud.png", scale: 1 },
    { name: "Daikin", file: "daikin.png", scale: 1 },
]

function Brands() {
    React.useEffect(ensureMontserrat, [])

    return (
        <section className="br-section" aria-labelledby="br-heading">
            <style>{CSS}</style>
            <div className="br-wrap">
                <div className="br-head">
                    <div className="br-eyebrow">EQUIPMENT WE INSTALL</div>
                    <h2 className="br-h2" id="br-heading">
                        The brands we stand behind.
                    </h2>
                    <p className="br-body">
                        We install and service Trane, Ruud, and Daikin systems —
                        and we repair every major brand, whoever put it in.
                    </p>
                </div>

                {/* A list, because it is one: three names of equal standing.
                    Alt text carries the brand name, so the row is readable with
                    images off or by a screen reader. */}
                <ul className="br-row">
                    {BRANDS.map((b) => (
                        <li
                            className="br-item"
                            key={b.name}
                            style={{ "--s": b.scale ?? 1 } as React.CSSProperties}
                        >
                            <img
                                className="br-logo"
                                src={BRAND_CDN + b.file}
                                alt={b.name}
                                loading="lazy"
                                decoding="async"
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </section>
    )
}

const CSS = `
/* Same reset the other homepage components use — Framer's page styles otherwise
   leak into the list and the box model. */
.br-section, .br-section *{ box-sizing:border-box; font-family:${FONT_STACK} }
.br-section{
  background:#fff; color:${COLORS.ink};
  padding:56px 0;
}
.br-wrap{ max-width:1280px; margin:0 auto; padding:0 40px }

.br-head{ text-align:center; max-width:640px; margin:0 auto }
.br-eyebrow{
  font-size:11.5px; font-weight:800; letter-spacing:2px; color:${COLORS.purple};
}
.br-h2{
  margin:10px 0 0; font-style:italic; font-weight:900; font-size:30px;
  letter-spacing:-.6px; color:${COLORS.ink};
}
.br-body{
  margin:12px 0 0; font-size:15px; line-height:1.6; font-weight:500; color:${COLORS.body};
}

/* Capped well below the 1280 wrap: at full width the three marks drift so far apart
   they stop reading as a set. */
.br-row{
  list-style:none; margin:36px auto 0; padding:0; max-width:880px;
  display:grid; grid-template-columns:repeat(3,1fr);
  align-items:center; gap:24px;
}
.br-item{ display:flex; align-items:center; justify-content:center; min-height:88px }

.br-logo{
  max-width:calc(200px * var(--s, 1)); width:100%;
  height:calc(52px * var(--s, 1)); object-fit:contain; display:block;
  filter:grayscale(1) opacity(.55);
  transition:filter .22s ease, transform .22s ease;
}

/* Hover-to-colour only where hovering exists. On a phone there is no hover state
   to discover, so the logos would be permanently grey — these render in full
   colour on touch instead. */
@media (hover:hover) and (pointer:fine){
  .br-logo:hover{ filter:none; transform:scale(1.03) }
}
@media (hover:none){
  .br-logo{ filter:none }
}

@media (prefers-reduced-motion:reduce){
  .br-logo{ transition:none }
  .br-logo:hover{ transform:none }
}

@media (max-width:899px){
  .br-section{ padding:40px 0 }
  .br-wrap{ padding:0 20px }
  .br-h2{ font-size:24px }
  .br-row{ gap:16px 12px; margin-top:26px }
  .br-item{ min-height:64px }
  .br-logo{ height:calc(38px * var(--s, 1)); max-width:calc(150px * var(--s, 1)) }
}
@media (max-width:479px){
  /* Three across gets too small to read a wordmark; two up, one centred below. */
  .br-row{ grid-template-columns:repeat(2,1fr) }
  .br-item:last-child{ grid-column:1 / -1 }
}
`

export default Brands
