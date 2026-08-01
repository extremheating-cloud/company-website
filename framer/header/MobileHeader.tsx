import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { addPropertyControls, ControlType } from "framer"
import {
    COLORS,
    GRADIENTS,
    FONT_STACK,
    ensureMontserrat,
    PHONE_DISPLAY,
    PHONE_TEL,
} from "https://framer.com/m/Theme-cgWgED.js@GwatL2Kitrjudg5Q2oQf"

type VariantName = "Phone:Open" | "Phone:Closed"

type Props = {
    startVariant: VariantName
    showOpenButton: boolean
    openButtonLabel: string
    phoneNumber: string
    useScheduleButton: boolean
}

const GOOGLE_RATING = "4.9"

const LOGO_TIGHT =
    "https://cdn.jsdelivr.net/gh/extremheating-cloud/company-website@c83bf3b6254c9bd3dbc1bd101024085c183abd20/assets/brand/logo-white-tight.png"

function openTop(href: string) {
    try {
        if (window.top) window.top.location.href = href
        else window.location.href = href
    } catch {
        window.location.href = href
    }
}

function dispatchToParentOrSelf(eventName: string) {
    try {
        try {
            if (window.parent && window.parent !== window) {
                window.parent.dispatchEvent(
                    new (window.parent as any).CustomEvent(eventName)
                )
                return
            }
        } catch {}
        window.dispatchEvent(new CustomEvent(eventName))
    } catch {}
}

type LinkItem = { label: string; href: string }
type MenuSection = {
    id: string
    title: string
    core: LinkItem[]
    coreLabel: string
    additional: LinkItem[]
    allLabel: string
    allHref: string
}

const SECTIONS: MenuSection[] = [
    {
        id: "plumbing",
        title: "Plumbing",
        coreLabel: "CORE SERVICES",
        core: [
            { label: "Clogged Drain", href: "/plumbing/clogged-drain" },
            { label: "Water Heaters", href: "/plumbing/water-heater/overview" },
            { label: "Sewer Line", href: "/plumbing/sewer-line/overview" },
            { label: "Sump Pump", href: "/plumbing/sump-pump/overview" },
            { label: "Gas Line", href: "/plumbing/gas-line/overview" },
        ],
        additional: [
            {
                label: "Emergency Plumbing",
                href: "/plumbing/emergency-plumbing",
            },
            { label: "Leak Detection", href: "/plumbing/leak-detection" },
            { label: "Water Treatment", href: "/plumbing/water-treatment" },
            { label: "Toilet Repair", href: "/plumbing/toilet-repair" },
        ],
        allLabel: "All Plumbing Services →",
        allHref: "/plumbing/services",
    },
    {
        id: "hvac",
        title: "Heating & Air",
        coreLabel: "CORE SERVICES",
        core: [
            { label: "Air Conditioning", href: "/air-conditioning" },
            { label: "Furnace & Heating", href: "/furnace-heating" },
            { label: "Heat Pump", href: "/heat-pump" },
            { label: "Duct Cleaning", href: "/duct-cleaning" },
            { label: "Indoor Air Quality", href: "/indoor-air-quality" },
        ],
        additional: [
            { label: "Maintenance Plans", href: "/maintenance" },
            { label: "Inspections", href: "/inspection" },
            { label: "Thermostat", href: "/thermostat" },
            { label: "Humidifier", href: "/humidifier" },
        ],
        allLabel: "All HVAC Services →",
        allHref: "/services",
    },
]

const PLAIN_ROWS: (LinkItem & { badge?: string })[] = [
    { label: "Locations", href: "/locations" },
    { label: "Specials", href: "/specials", badge: "SAVE" },
    { label: "About", href: "/about" },
]

function MobileHeader({
    startVariant = "Phone:Closed",
    showOpenButton = true,
    openButtonLabel = "Menu",
    phoneNumber = PHONE_DISPLAY,
    useScheduleButton = true,
}: Props) {
    const [variant, setVariant] = React.useState<VariantName>(startVariant)
    const [expanded, setExpanded] = React.useState<string | null>(null)

    React.useEffect(ensureMontserrat, [])

    const isOpen = variant === "Phone:Open"
    const open = () => setVariant("Phone:Open")
    const close = () => {
        setVariant("Phone:Closed")
        setExpanded(null)
    }
    const toggle = () => (isOpen ? close() : open())

    React.useEffect(() => {
        if (!isOpen) return
        const prev = document.body.style.overflow
        document.body.style.overflow = "hidden"
        return () => {
            document.body.style.overflow = prev
        }
    }, [isOpen])

    const onSchedule = (e?: React.SyntheticEvent) => {
        e?.preventDefault?.()
        e?.stopPropagation?.()
        close()
        dispatchToParentOrSelf("open-contact-dialog")
    }

    const go = (href: string) => (e: React.MouseEvent) => {
        e.preventDefault()
        close()
        openTop(href)
    }

    const telHref =
        phoneNumber === PHONE_DISPLAY
            ? PHONE_TEL
            : `tel:1${phoneNumber.replace(/\D/g, "").replace(/^1/, "")}`

    return (
        <div className="mxx-root">
            <style>{CSS}</style>

            {showOpenButton && (
                <div className="mxx-bar">
                    <a
                        href="/"
                        onClick={go("/")}
                        aria-label="Extreme Heating, Air, Plumbing — Home"
                    >
                        <img
                            src={LOGO_TIGHT}
                            alt="Extreme"
                            className="mxx-bar-logo"
                        />
                    </a>
                    <div className="mxx-bar-right">
                        <a
                            href={telHref}
                            className="mxx-phone-btn"
                            aria-label={`Call ${phoneNumber}`}
                        >
                            <svg
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                aria-hidden
                            >
                                <path
                                    d="M5 4h4l2 5-2.5 1.5a12 12 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"
                                    fill={COLORS.ink}
                                />
                            </svg>
                        </a>
                        <button
                            type="button"
                            className="mxx-trigger"
                            onClick={toggle}
                            aria-label={openButtonLabel}
                            aria-expanded={isOpen}
                        >
                            <span className="l" aria-hidden />
                        </button>
                    </div>
                </div>
            )}

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="mxx-overlay"
                        role="dialog"
                        aria-modal="true"
                        initial={{ opacity: 0, y: 14 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 14 }}
                        transition={{ duration: 0.25, ease: "easeOut" }}
                    >

                        <div className="mxx-top">
                            <a href="/" onClick={go("/")}>
                                <img
                                    src={LOGO_TIGHT}
                                    alt="Extreme Heating, Air, Plumbing"
                                    className="mxx-logo"
                                />
                            </a>
                            <button
                                type="button"
                                className="mxx-close"
                                onClick={close}
                                aria-label="Close menu"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="mxx-scroll">
                            <nav>
                                {SECTIONS.map((s) => {
                                    const isExp = expanded === s.id
                                    return (
                                        <div key={s.id}>
                                            <button
                                                type="button"
                                                className="mxx-row"
                                                aria-expanded={isExp}
                                                onClick={() =>
                                                    setExpanded((cur) =>
                                                        cur === s.id
                                                            ? null
                                                            : s.id
                                                    )
                                                }
                                            >
                                                <span>{s.title}</span>
                                                <span
                                                    className={
                                                        "mxx-caret" +
                                                        (isExp ? " on" : "")
                                                    }
                                                >
                                                    {isExp ? "▴" : "▾"}
                                                </span>
                                            </button>
                                            <AnimatePresence initial={false}>
                                                {isExp && (
                                                    <motion.div
                                                        initial={{
                                                            height: 0,
                                                            opacity: 0,
                                                        }}
                                                        animate={{
                                                            height: "auto",
                                                            opacity: 1,
                                                        }}
                                                        exit={{
                                                            height: 0,
                                                            opacity: 0,
                                                        }}
                                                        transition={{
                                                            duration: 0.22,
                                                        }}
                                                        style={{
                                                            overflow: "hidden",
                                                        }}
                                                    >
                                                        <div className="mxx-inset">
                                                            <div className="mxx-mini">
                                                                {s.coreLabel}
                                                            </div>
                                                            <div className="mxx-grid">
                                                                {s.core.map(
                                                                    (l) => (
                                                                        <a
                                                                            key={
                                                                                l.href
                                                                            }
                                                                            href={
                                                                                l.href
                                                                            }
                                                                            onClick={go(
                                                                                l.href
                                                                            )}
                                                                        >
                                                                            {
                                                                                l.label
                                                                            }
                                                                        </a>
                                                                    )
                                                                )}
                                                            </div>
                                                            <div className="mxx-mini">
                                                                ADDITIONAL
                                                            </div>
                                                            <div className="mxx-grid">
                                                                {s.additional.map(
                                                                    (l) => (
                                                                        <a
                                                                            key={
                                                                                l.href
                                                                            }
                                                                            href={
                                                                                l.href
                                                                            }
                                                                            onClick={go(
                                                                                l.href
                                                                            )}
                                                                        >
                                                                            {
                                                                                l.label
                                                                            }
                                                                        </a>
                                                                    )
                                                                )}
                                                            </div>
                                                            <a
                                                                className="mxx-all"
                                                                href={s.allHref}
                                                                onClick={go(
                                                                    s.allHref
                                                                )}
                                                            >
                                                                {s.allLabel}
                                                            </a>
                                                        </div>
                                                    </motion.div>
                                                )}
                                            </AnimatePresence>
                                        </div>
                                    )
                                })}

                                {PLAIN_ROWS.map((r) => (
                                    <a
                                        key={r.href}
                                        className="mxx-row"
                                        href={r.href}
                                        onClick={go(r.href)}
                                    >
                                        <span>
                                            {r.label}
                                            {r.badge && (
                                                <span className="mxx-save">
                                                    {r.badge}
                                                </span>
                                            )}
                                        </span>
                                    </a>
                                ))}
                            </nav>
                        </div>

                        <div className="mxx-pinned">
                            {useScheduleButton && (
                                <button
                                    type="button"
                                    className="mxx-cta"
                                    onClick={onSchedule}
                                >
                                    Schedule Service&nbsp;&nbsp;→
                                </button>
                            )}
                            <a href={telHref} className="mxx-call">
                                Call {phoneNumber}
                            </a>
                            <div className="mxx-trust">
                                <span className="s">★★★★★</span>
                                {GOOGLE_RATING} on Google
                                <span className="dot">·</span>20+ yrs
                                <span className="dot">·</span>24/7
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {isOpen && <KeyHandler onEscape={close} />}
        </div>
    )
}

function KeyHandler({ onEscape }: { onEscape: () => void }) {
    React.useEffect(() => {
        const onKey = (e: KeyboardEvent) => {
            if (e.key === "Escape") onEscape()
        }
        document.addEventListener("keydown", onKey)
        return () => document.removeEventListener("keydown", onKey)
    }, [onEscape])
    return null
}

const CSS = `
.mxx-root, .mxx-root *, .mxx-overlay, .mxx-overlay *{ box-sizing:border-box; font-family:${FONT_STACK} }

.mxx-bar{
  display:flex; align-items:center; justify-content:space-between;
  padding:14px 20px; background:transparent;
}
.mxx-bar > a, .mxx-top > a{ display:flex; align-items:center; align-self:center; line-height:0 }
.mxx-bar-logo{ width:min(52vw,200px); height:auto; display:block; margin:3px 0 0 -6px }
.mxx-bar-right{ display:flex; align-items:center; gap:10px }
.mxx-phone-btn{
  width:44px; height:44px; border-radius:12px; background:${COLORS.green};
  display:flex; align-items:center; justify-content:center; text-decoration:none;
  transition:background .15s ease;
}
.mxx-phone-btn:active{ background:${COLORS.greenHoverOnDark} }
.mxx-trigger{
  width:44px; height:44px; border:1.5px solid rgba(255,255,255,.4); border-radius:12px;
  background:transparent; cursor:pointer; display:flex; align-items:center; justify-content:center;
}
.mxx-trigger .l{
  display:block; width:18px; height:2px; background:#fff;
  box-shadow:0 5px 0 #fff, 0 -5px 0 #fff;
}

.mxx-overlay{
  position:fixed; inset:0; z-index:9500; display:flex; flex-direction:column;
  background:${GRADIENTS.heroMobile}; color:#fff;
}
.mxx-top{
  display:flex; align-items:center; justify-content:space-between;
  padding:14px 20px; border-bottom:1px solid rgba(255,255,255,.12); flex-shrink:0;
}
.mxx-logo{ width:min(52vw,200px); height:auto; display:block; margin:3px 0 0 -6px }
.mxx-close{
  width:44px; height:44px; border:1.5px solid rgba(255,255,255,.45); border-radius:11px;
  background:transparent; color:#fff; font-size:16px; cursor:pointer; display:grid; place-items:center;
}
.mxx-close:active, .mxx-trigger:active{ transform:scale(.96) }

.mxx-scroll{ flex:1; overflow:auto; -webkit-overflow-scrolling:touch; padding:4px 20px 16px }

.mxx-row{
  width:100%; display:flex; align-items:center; justify-content:space-between; gap:10px;
  padding:16px 2px; min-height:44px; background:none; border:none; cursor:pointer;
  border-bottom:1px solid rgba(255,255,255,.12); text-decoration:none;
  font:italic 900 19px ${FONT_STACK}; color:#fff; text-align:left;
}
.mxx-row:focus-visible{ outline:2px solid #fff; outline-offset:-2px }
.mxx-caret{ font-style:normal; font-size:13px; color:rgba(255,255,255,.55) }
.mxx-caret.on{ color:${COLORS.green} }
.mxx-save{
  display:inline-block; margin-left:10px; vertical-align:middle;
  background:${COLORS.green}; color:${COLORS.ink};
  font:800 9.5px ${FONT_STACK}; letter-spacing:1px; border-radius:5px; padding:3px 7px;
}

.mxx-inset{
  margin:12px 0 16px; background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12);
  border-radius:14px; padding:16px 16px 14px;
}
.mxx-mini{
  font:800 9.5px ${FONT_STACK}; letter-spacing:1.6px; color:${COLORS.greenHoverOnDark};
  margin:0 0 8px;
}
.mxx-mini + .mxx-mini{ margin-top:14px }
.mxx-grid{ display:grid; grid-template-columns:1fr 1fr; gap:2px 12px; margin-bottom:12px }
.mxx-grid a{
  display:flex; align-items:center; min-height:40px; padding:4px 2px;
  font:600 13px ${FONT_STACK}; color:rgba(255,255,255,.92); text-decoration:none;
}
.mxx-grid a:active{ color:${COLORS.greenHoverOnDark} }
.mxx-all{
  display:inline-block; font:800 13px ${FONT_STACK}; color:${COLORS.greenHoverOnDark};
  text-decoration:none; padding:6px 2px; min-height:32px;
}

.mxx-pinned{
  flex-shrink:0; background:rgba(15,23,42,.25); border-top:1px solid rgba(255,255,255,.12);
  padding:14px 20px calc(14px + env(safe-area-inset-bottom)); display:grid; gap:10px;
}
.mxx-cta{
  width:100%; min-height:48px; border:none; border-radius:12px; cursor:pointer;
  background:${COLORS.green}; color:${COLORS.ink}; font:800 15.5px ${FONT_STACK};
  transition:background .15s ease;
}
.mxx-cta:active{ background:${COLORS.greenHoverOnDark} }
.mxx-call{
  width:100%; min-height:48px; display:flex; align-items:center; justify-content:center;
  border:1.5px solid rgba(255,255,255,.45); border-radius:12px; color:#fff;
  font:800 15px ${FONT_STACK}; text-decoration:none;
}
.mxx-call:active{ border-color:${COLORS.green}; color:${COLORS.green} }
.mxx-trust{
  display:flex; align-items:center; justify-content:center; gap:8px;
  font:700 12px ${FONT_STACK}; color:rgba(255,255,255,.82);
}
.mxx-trust .s{ color:${COLORS.stars}; letter-spacing:1px }
.mxx-trust .dot{ color:rgba(255,255,255,.4) }
`

addPropertyControls(MobileHeader as any, {
    startVariant: {
        type: ControlType.Enum,
        title: "Start",
        options: ["Phone:Closed", "Phone:Open"],
        optionTitles: ["Phone:Closed", "Phone:Open"],
        defaultValue: "Phone:Closed",
    },
    showOpenButton: {
        type: ControlType.Boolean,
        title: "Header Bar",
        defaultValue: true,
    },
    openButtonLabel: {
        type: ControlType.String,
        title: "Label",
        defaultValue: "Menu",
        hidden(props) {
            return !props.showOpenButton
        },
    },
    phoneNumber: {
        type: ControlType.String,
        title: "Phone",
        defaultValue: PHONE_DISPLAY,
    },
    useScheduleButton: {
        type: ControlType.Boolean,
        title: "Schedule CTA",
        defaultValue: true,
    },
})

export default MobileHeader
