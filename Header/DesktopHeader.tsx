import * as React from "react"
import { addPropertyControls, ControlType } from "framer"
import {
    COLORS,
    SHADOWS,
    FONT_STACK,
    ensureMontserrat,
    PHONE_DISPLAY,
    PHONE_TEL,
    ASSETS,
    openScheduleDialog,
} from "https://framer.com/m/Theme-cgWgED.js@B2PNlINgwl1DTpD88aOo"

type MenuName = "hvac" | "plumbing" | "locations" | null

type Props = {
    headerOffset?: number

    solid?: boolean
}

const LOGO_TIGHT =
    "https://cdn.jsdelivr.net/gh/extremheating-cloud/extreme-assets@main/images/brand/logo-white-tight.png"

type CoreRow = {
    title: string
    desc: string
    href: string
    chips?: { label: string; href: string }[]
}

const HVAC_CORE: CoreRow[] = [
    {
        title: "Air Conditioning",
        desc: "Repair, replacement & tune-ups",
        href: "/air-conditioning",
    },
    {
        title: "Furnace & Heating",
        desc: "Repairs, installs & safety checks",
        href: "/furnace-heating",
        chips: [
            { label: "Overview", href: "/furnace-heating" },
            { label: "Installation", href: "/furnace-installation" },
            { label: "Repair", href: "/furnace-repair" },
        ],
    },
    {
        title: "Heat Pump",
        desc: "Year-round efficiency",
        href: "/heat-pump",
    },
    {
        title: "Duct Cleaning",
        desc: "Airflow & air balancing",
        href: "/duct-cleaning",
    },
    {
        title: "Indoor Air Quality",
        desc: "Filtration, UV & humidity control",
        href: "/indoor-air-quality",
        chips: [
            { label: "Overview", href: "/indoor-air-quality" },
            { label: "Solutions", href: "/indoor-air-quality-solutions" },
            { label: "FAQ", href: "/iaq-faq" },
        ],
    },
]

const HVAC_ADDITIONAL = [
    {
        title: "HVAC Maintenance Plans",
        href: "/maintenance",
        badge: "X-PLAN",
        desc: "Bi-annual tune-ups & priority service",
    },
    { title: "HVAC Inspections", href: "/inspection" },
    { title: "Thermostat Services", href: "/thermostat" },
    { title: "Humidifier Services", href: "/humidifier" },
]

const PLUMB_CORE: CoreRow[] = [
    {
        title: "Clogged Drain",
        desc: "Fast help for clogged & slow drains",
        href: "/plumbing/clogged-drain",
    },
    {
        title: "Water Heater",
        desc: "Repair & replacement for hot water",
        href: "/plumbing/water-heater/overview",
        chips: [
            { label: "Overview", href: "/plumbing/water-heater/overview" },
            { label: "Repair", href: "/plumbing/water-heater/repair" },
            {
                label: "Installation",
                href: "/plumbing/water-heater/installation",
            },
        ],
    },
    {
        title: "Sewer Line",
        desc: "Inspection, repair & cleaning",
        href: "/plumbing/sewer-line/overview",
        chips: [
            { label: "Overview", href: "/plumbing/sewer-line/overview" },
            { label: "Repair", href: "/plumbing/sewer-line/repair" },
            { label: "Cleaning", href: "/plumbing/sewer-line/cleaning" },
        ],
    },
    {
        title: "Sump Pump",
        desc: "Protection against basement water",
        href: "/plumbing/sump-pump/overview",
        chips: [
            { label: "Overview", href: "/plumbing/sump-pump/overview" },
            { label: "Repair", href: "/plumbing/sump-pump/repair" },
            { label: "Installation", href: "/plumbing/sump-pump/installation" },
        ],
    },
    {
        title: "Gas Line",
        desc: "Safe installation & repair",
        href: "/plumbing/gas-line/overview",
        chips: [
            { label: "Overview", href: "/plumbing/gas-line/overview" },
            { label: "Repair", href: "/plumbing/gas-line/repair" },
            { label: "Installation", href: "/plumbing/gas-line/installation" },
        ],
    },
]

const PLUMB_ADDITIONAL = [
    { title: "Emergency Plumbing", href: "/plumbing/emergency-plumbing" },
    { title: "Leak Detection", href: "/plumbing/leak-detection" },
    { title: "Water Treatment", href: "/plumbing/water-treatment" },
    { title: "Toilet Repair", href: "/plumbing/toilet-repair" },
]

const DAYTON_CITIES: [string, string][] = [
    ["dayton", "Dayton"],
    ["beavercreek", "Beavercreek"],
    ["bellbrook", "Bellbrook"],
    ["centerville", "Centerville"],
    ["englewood", "Englewood"],
    ["fairborn", "Fairborn"],
    ["franklin", "Franklin"],
    ["huber", "Huber Heights"],
    ["kettering", "Kettering"],
    ["miamisburg", "Miamisburg"],
    ["moraine", "Moraine"],
    ["oakwood", "Oakwood"],
    ["riverside", "Riverside"],
    ["springboro", "Springboro"],
    ["springfield", "Springfield"],
    ["tipp", "Tipp City"],
    ["troy", "Troy"],
    ["vandalia", "Vandalia"],
    ["xenia", "Xenia"],
]
const CINCY_CITIES: [string, string][] = [
    ["blue-ash", "Blue Ash"],
    ["cincinnati", "Cincinnati"],
    ["fairfield", "Fairfield"],
    ["lebanon", "Lebanon"],
    ["mason", "Mason"],
    ["middletown", "Middletown"],
    ["northgate", "Northgate"],
    ["sharonville", "Sharonville"],
    ["west-chester", "West Chester"],
]
const CITY_SERVICES: [string, string][] = [
    ["heating", "Heating"],
    ["cooling", "Cooling"],
    ["maintenance", "Maintenance"],
    ["duct-cleaning", "Duct Cleaning"],
    ["indoor-air-quality", "Indoor Air Quality"],
]

function XGlyph({ size = 24 }: { size?: number }) {
    const bar: React.CSSProperties = {
        position: "absolute",
        left: "50%",
        top: "50%",
        width: "100%",
        height: Math.round(size * (8 / 30)),
        borderRadius: 2,
    }
    return (
        <span
            aria-hidden
            style={{
                position: "relative",
                display: "inline-block",
                width: size,
                height: size,
                flexShrink: 0,
            }}
        >
            <span
                style={{
                    ...bar,
                    background: COLORS.purple,
                    transform: "translate(-50%,-50%) rotate(45deg)",
                }}
            />
            <span
                style={{
                    ...bar,
                    background: COLORS.green,
                    transform: "translate(-50%,-50%) rotate(-45deg)",
                }}
            />
        </span>
    )
}

function DesktopHeader({
    headerOffset = 96,
    solid = false,
}: Props) {
    const [openMenu, setOpenMenu] = React.useState<MenuName>(null)
    const rootRef = React.useRef<HTMLDivElement | null>(null)
    const navRef = React.useRef<HTMLElement | null>(null)
    const [openCity, setOpenCity] = React.useState<string | null>(null)
    const [shellTop, setShellTop] = React.useState<number>(headerOffset)
    const closeTimerRef = React.useRef<number | null>(null)

    React.useEffect(ensureMontserrat, [])

    const closeAllMenus = React.useCallback(() => {
        setOpenMenu(null)
        setOpenCity(null)
    }, [])

    const isDesktopHover = React.useCallback(() => {
        try {
            return window.matchMedia("(hover:hover) and (pointer:fine)").matches
        } catch {
            return true
        }
    }, [])

    React.useLayoutEffect(() => {
        function computeTop() {
            if (!navRef.current) return
            const rect = navRef.current.getBoundingClientRect()
            setShellTop(rect.bottom)
        }
        computeTop()
        window.addEventListener("resize", computeTop)
        window.addEventListener("scroll", computeTop)
        return () => {
            window.removeEventListener("resize", computeTop)
            window.removeEventListener("scroll", computeTop)
        }
    }, [headerOffset])

    React.useEffect(() => {
        if (!openMenu) return
        const onClick = (e: MouseEvent) => {
            if (!rootRef.current) return
            if (!rootRef.current.contains(e.target as Node)) closeAllMenus()
        }
        const onKey = (e: KeyboardEvent) => {
            if (e.key === "Escape") closeAllMenus()
        }
        const onRoute = () => closeAllMenus()
        document.addEventListener("click", onClick)
        document.addEventListener("keydown", onKey)
        window.addEventListener("popstate", onRoute)
        window.addEventListener("hashchange", onRoute)
        return () => {
            document.removeEventListener("click", onClick)
            document.removeEventListener("keydown", onKey)
            window.removeEventListener("popstate", onRoute)
            window.removeEventListener("hashchange", onRoute)
        }
    }, [openMenu, closeAllMenus])

    const toggleMenu = (menu: MenuName) =>
        setOpenMenu((cur) => (cur === menu ? null : menu))
    const cancelClose = React.useCallback(() => {
        if (closeTimerRef.current) {
            window.clearTimeout(closeTimerRef.current)
            closeTimerRef.current = null
        }
    }, [])
    const scheduleClose = React.useCallback(() => {
        if (!isDesktopHover()) return
        if (closeTimerRef.current) window.clearTimeout(closeTimerRef.current)
        closeTimerRef.current = window.setTimeout(closeAllMenus, 140)
    }, [closeAllMenus, isDesktopHover])
    const hoverOpen = (menu: MenuName) => {
        if (!isDesktopHover()) return
        cancelClose()
        setOpenMenu(menu)
    }

    const handleLinkClick = () => closeAllMenus()

    const rootClass =
        "xhac-nav-root" +
        (solid ? " is-solid" : "") +
        (openMenu ? ` menu-open menu-${openMenu}-open` : "")

    const navItem = (menu: Exclude<MenuName, null>, label: string) => {
        const isOpen = openMenu === menu
        return (
            <button
                type="button"
                className={"xhac-nav-link" + (isOpen ? " is-open" : "")}
                onClick={() => toggleMenu(menu)}
                onMouseEnter={() => hoverOpen(menu)}
                onFocus={() => setOpenMenu(menu)}
                aria-haspopup="true"
                aria-expanded={isOpen}
            >
                <span>{label}</span>
                <span className="caret">{isOpen ? "▴" : "▾"}</span>
                <span className="bar" aria-hidden />
            </button>
        )
    }

    const coreRow = (r: CoreRow) => (
        <div key={r.title} className="xm-row-wrap">
            <a href={r.href} className="xm-row" onClick={handleLinkClick}>
                <XGlyph />
                <span className="txt">
                    <span className="t">{r.title}</span>
                    <span className="d">{r.desc}</span>
                </span>
                <span className="go" aria-hidden>
                    →
                </span>
            </a>
            {r.chips && (
                <div className="xm-chips">
                    {r.chips.map((c) => (
                        <a
                            key={c.label}
                            href={c.href}
                            className="xm-chip"
                            onClick={handleLinkClick}
                        >
                            {c.label}
                        </a>
                    ))}
                </div>
            )}
        </div>
    )

    const addRow = (r: {
        title: string
        href: string
        badge?: string
        desc?: string
    }) => (
        <a
            key={r.title}
            href={r.href}
            className="xm-row slim"
            onClick={handleLinkClick}
        >
            <span className="txt">
                <span className="t">
                    {r.title}
                    {r.badge && <span className="xm-badge">{r.badge}</span>}
                </span>
                {r.desc && <span className="d">{r.desc}</span>}
            </span>
            <span className="go" aria-hidden>
                →
            </span>
        </a>
    )

    return (
        <div
            ref={rootRef}
            className={rootClass}
            onMouseLeave={scheduleClose}
            onMouseEnter={cancelClose}
        >
            <style>{CSS}</style>

            <header className="xhac-bar" ref={navRef as any}>
                <a
                    href="/"
                    className="xhac-logo-link"
                    onClick={handleLinkClick}
                    aria-label="Extreme Heating, Air, Plumbing — Home"
                >
                    <img
                        src={LOGO_TIGHT}
                        alt="Extreme Heating, Air, Plumbing"
                        className="xhac-logo"
                    />
                </a>

                <nav className="xhac-nav-strip">
                    {navItem("plumbing", "Plumbing")}
                    {navItem("hvac", "Heating & Air")}
                    {navItem("locations", "Locations")}
                    <a
                        href="/specials"
                        className="xhac-nav-link"
                        onClick={handleLinkClick}
                    >
                        <span>Specials</span>
                    </a>
                    <a
                        href="/about"
                        className="xhac-nav-link"
                        onClick={handleLinkClick}
                    >
                        <span>About</span>
                    </a>
                </nav>

                <div className="xhac-bar-right">
                    <a href={PHONE_TEL} className="xhac-phone">
                        {PHONE_DISPLAY}
                    </a>

                    <a
                        href={PHONE_TEL}
                        className="xhac-phone-icon"
                        aria-label={`Call ${PHONE_DISPLAY}`}
                    >
                        <svg
                            width="17"
                            height="17"
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
                        className="xhac-cta"
                        onClick={() => {
                            closeAllMenus()
                            openScheduleDialog()
                        }}
                    >
                        Schedule Service
                    </button>
                </div>
            </header>

            {openMenu && (
                <div
                    className="xm-scrim"
                    style={{ top: shellTop }}
                    onClick={closeAllMenus}
                    onMouseEnter={scheduleClose}
                    aria-hidden
                />
            )}

            <div
                className="xm-shell"
                style={{ top: shellTop }}
                onMouseEnter={cancelClose}
            >

                <div className="xm-panel" data-menu="hvac">
                    <div className="xm-grid">
                        <div className="xm-col">
                            <div className="xm-label">CORE SERVICES</div>
                            {HVAC_CORE.map(coreRow)}
                        </div>
                        <div className="xm-col">
                            <div className="xm-label">
                                X-PLAN &amp; ADDITIONAL SERVICES
                            </div>
                            {HVAC_ADDITIONAL.map(addRow)}
                            <div className="xm-divider" />
                            <a
                                href="/services"
                                className="xm-viewall"
                                onClick={handleLinkClick}
                            >
                                View All HVAC Services →
                            </a>
                        </div>
                        <div className="xm-aside">
                            <div className="xm-promo lav">
                                <div className="h">
                                    Interested in Financing?
                                </div>
                                <p>
                                    Spread out the cost of a new comfort system
                                    with flexible payment options that fit your
                                    budget.
                                </p>
                                <a
                                    href="/financing-options"
                                    onClick={handleLinkClick}
                                >
                                    Learn More →
                                </a>
                            </div>
                            <div className="xm-promo mint">
                                <div className="h">X-Plan Maintenance Plan</div>
                                <p>
                                    Scheduled tune-ups, priority service, and
                                    exclusive member discounts — from $20.75/mo.
                                </p>
                                <a
                                    href="/maintenance"
                                    onClick={handleLinkClick}
                                >
                                    Explore X-Plan →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="xm-panel" data-menu="plumbing">
                    <div className="xm-grid">
                        <div className="xm-col">
                            <div className="xm-label">CORE SERVICES</div>
                            {PLUMB_CORE.map(coreRow)}
                        </div>
                        <div className="xm-col">
                            <div className="xm-label">ADDITIONAL SERVICES</div>
                            {PLUMB_ADDITIONAL.map(addRow)}
                            <div className="xm-divider" />
                            <a
                                href="/plumbing/services"
                                className="xm-viewall"
                                onClick={handleLinkClick}
                            >
                                View All Plumbing Services →
                            </a>
                        </div>
                        <div className="xm-aside">
                            <div className="xm-promo lav">
                                <div className="h">
                                    Need Plumbing Help Fast?
                                </div>
                                <p>
                                    Same-day and emergency plumbing service
                                    across Dayton &amp; Cincinnati.
                                </p>
                                <button
                                    type="button"
                                    className="xm-promo-btn"
                                    onClick={() => {
                                        closeAllMenus()
                                        openScheduleDialog()
                                    }}
                                >
                                    Schedule Service →
                                </button>
                            </div>
                            <div className="xm-promo mint">
                                <div className="h">Plumbing Specials</div>
                                <p>
                                    Current offers and seasonal savings on
                                    plumbing services.
                                </p>
                                <a href="/specials" onClick={handleLinkClick}>
                                    View Specials →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="xm-panel" data-menu="locations">
                    <div className="xm-grid locations">
                        {[
                            ["DAYTON AREA", DAYTON_CITIES],
                            ["CINCINNATI AREA", CINCY_CITIES],
                        ].map(([label, cities]) => (
                            <div className="xm-col" key={label as string}>
                                <div className="xm-label">
                                    {label as string}
                                </div>
                                <div className="xm-city-grid">
                                    {(cities as [string, string][]).map(
                                        ([slug, name]) => (
                                            <div key={slug} className="xm-city">
                                                <button
                                                    type="button"
                                                    className={
                                                        "xm-city-toggle" +
                                                        (openCity === slug
                                                            ? " is-open"
                                                            : "")
                                                    }
                                                    onClick={() =>
                                                        setOpenCity((c) =>
                                                            c === slug
                                                                ? null
                                                                : slug
                                                        )
                                                    }
                                                >
                                                    {name}
                                                    <span className="c">
                                                        {openCity === slug
                                                            ? "▴"
                                                            : "▾"}
                                                    </span>
                                                </button>
                                                {openCity === slug && (
                                                    <div className="xm-chips">
                                                        {CITY_SERVICES.map(
                                                            ([s, l]) => (
                                                                <a
                                                                    key={s}
                                                                    className="xm-chip"
                                                                    href={`/locations/${slug}/${s}`}
                                                                    onClick={
                                                                        handleLinkClick
                                                                    }
                                                                >
                                                                    {l}
                                                                </a>
                                                            )
                                                        )}
                                                    </div>
                                                )}
                                            </div>
                                        )
                                    )}
                                </div>
                            </div>
                        ))}
                        <div className="xm-aside">
                            <div className="xm-promo lav">
                                <div className="h">
                                    Serving the Miami Valley
                                </div>
                                <p>
                                    Locally owned and operated across Dayton
                                    &amp; Cincinnati for over 20 years.
                                </p>
                                <a href="/locations" onClick={handleLinkClick}>
                                    All Locations →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

const CSS = `
.xhac-nav-root, .xhac-nav-root *{ box-sizing:border-box; font-family:${FONT_STACK} }
.xhac-nav-root{
  position:relative; width:100%; height:100%; min-height:100%;
  display:flex; flex-direction:column; justify-content:center;
}

.xhac-nav-root.is-solid{ background:${COLORS.purpleLight} }

.xhac-bar{
  position:relative; display:flex; align-items:center; justify-content:space-between;
  gap:24px; padding:18px 40px; background:transparent;
}
.xhac-logo-link{ flex:none; display:flex; align-items:center; line-height:0 }
.xhac-logo{ height:48px; width:auto; display:block }
.xhac-bar-right{ flex:none; display:flex; align-items:center; gap:16px }
.xhac-phone{ font:800 14.5px ${FONT_STACK}; color:#fff; text-decoration:none; white-space:nowrap }
.xhac-phone:hover{ color:${COLORS.greenHoverOnDark} }
.xhac-phone-icon{
  display:none; width:40px; height:40px; border-radius:10px; background:${COLORS.green};
  align-items:center; justify-content:center; text-decoration:none; flex:none;
  transition:background .15s ease;
}
.xhac-phone-icon:hover{ background:${COLORS.greenHoverOnDark} }

.xhac-cta{
  display:inline-flex; align-items:center; justify-content:center;
  background:${COLORS.green}; color:${COLORS.ink}; font:800 14px ${FONT_STACK};
  padding:11px 18px; border:none; border-radius:10px; cursor:pointer; white-space:nowrap;
  transition:background .15s ease;
}
.xhac-cta:hover{ background:${COLORS.greenHoverOnDark} }
.xhac-cta:focus-visible{ outline:2px solid #fff; outline-offset:2px }

.xhac-nav-strip{
  display:flex; justify-content:center; align-items:center; gap:26px; padding:0 12px;
}
.xhac-nav-link{
  position:relative; display:inline-flex; align-items:center; gap:5px; padding:16px 2px;
  border:none; background:none; cursor:pointer; font:600 14px ${FONT_STACK};
  color:#fff; text-decoration:none; white-space:nowrap; transition:color .15s ease;
}
.xhac-nav-link:hover{ color:${COLORS.greenHoverOnDark} }
.xhac-nav-link:focus-visible{ outline:2px solid #fff; outline-offset:2px; border-radius:6px }
.xhac-nav-link .caret{ font-size:9px; opacity:.8 }
.xhac-nav-link .bar{

  position:absolute; left:0; right:0; bottom:-18px; height:3px; background:${COLORS.green};
  transform:scaleX(0); transform-origin:center; transition:transform .15s ease; border-radius:2px;
}
.xhac-nav-link.is-open{ color:${COLORS.green}; font-weight:800 }
.xhac-nav-link.is-open .bar{ transform:scaleX(1) }

.xm-scrim{
  position:fixed; left:0; right:0; bottom:0; background:rgba(15,23,42,.45); z-index:9000;
}

.xm-shell{ position:fixed; left:0; right:0; z-index:9001; pointer-events:none }
.xm-panel{
  display:none; background:#fff; border-top:1px solid ${COLORS.border};
  box-shadow:${SHADOWS.dropdown}; pointer-events:auto;
  opacity:0; transform:translateY(-8px);
}
.menu-hvac-open .xm-panel[data-menu="hvac"],
.menu-plumbing-open .xm-panel[data-menu="plumbing"],
.menu-locations-open .xm-panel[data-menu="locations"]{
  display:block; animation:xmIn .15s ease-out both;
}
@keyframes xmIn{ to{ opacity:1; transform:translateY(0) } }

.xm-grid{
  max-width:1280px; margin:0 auto; padding:30px 40px 34px;
  display:grid; grid-template-columns:1.1fr 1fr 340px; gap:40px;
}
.xm-grid.locations{ grid-template-columns:1.1fr 1fr 340px }
.xm-label{
  font:800 10.5px ${FONT_STACK}; letter-spacing:1.8px; color:${COLORS.muted};
  padding-bottom:12px; border-bottom:1px solid ${COLORS.border}; margin-bottom:10px;
}

.xm-row{
  display:flex; align-items:flex-start; gap:12px; padding:11px 10px; border-radius:10px;
  text-decoration:none; transition:background .13s ease;
}
.xm-row .txt{ flex:1; display:flex; flex-direction:column; gap:2px }
.xm-row .t{ font:800 14px ${FONT_STACK}; color:${COLORS.ink}; display:flex; align-items:center; gap:8px }
.xm-row .d{ font:500 11.5px ${FONT_STACK}; color:${COLORS.body} }
.xm-row .go{ opacity:0; color:${COLORS.green}; font-weight:800; transition:opacity .13s ease }
.xm-row:hover{ background:${COLORS.purpleTint} }
.xm-row:hover .t{ color:${COLORS.purple} }
.xm-row:hover .go{ opacity:1 }
.xm-row:focus-visible{ outline:2px solid ${COLORS.purple}; outline-offset:-2px }
.xm-row.slim{ padding:10px 10px }
.xm-badge{
  background:${COLORS.greenTint}; color:${COLORS.greenDark};
  font:800 9.5px ${FONT_STACK}; letter-spacing:.6px; border-radius:5px; padding:3px 7px;
}
.xm-chips{ display:flex; flex-wrap:wrap; gap:6px; padding:2px 10px 8px 46px }
.xm-chip{
  background:${COLORS.purpleTint}; color:${COLORS.purple}; font:700 10.5px ${FONT_STACK};
  border-radius:6px; padding:5px 9px; text-decoration:none; transition:background .13s ease, color .13s ease;
}
.xm-chip:hover{ background:${COLORS.purple}; color:#fff }
.xm-divider{ height:1px; background:${COLORS.border}; margin:12px 0 }
.xm-viewall{
  display:inline-block; font:800 13px ${FONT_STACK}; color:${COLORS.purple};
  text-decoration:none; padding:6px 10px;
}
.xm-viewall:hover{ color:${COLORS.greenDark} }

.xm-aside{ display:flex; flex-direction:column; gap:14px }
.xm-promo{ border-radius:14px; padding:18px 20px }
.xm-promo.lav{ background:${COLORS.purpleTint} }
.xm-promo.mint{ background:${COLORS.greenTint} }
.xm-promo .h{ font:800 15px ${FONT_STACK}; margin-bottom:6px }
.xm-promo.lav .h{ color:${COLORS.purple} }
.xm-promo.mint .h{ color:${COLORS.promoGreenHeadline} }
.xm-promo p{ font:500 12.5px/1.55 ${FONT_STACK}; color:${COLORS.body}; margin:0 0 10px }
.xm-promo a, .xm-promo-btn{
  font:800 13px ${FONT_STACK}; color:${COLORS.purple}; text-decoration:none;
  background:none; border:none; padding:0; cursor:pointer;
}
.xm-promo.mint a{ color:${COLORS.promoGreenHeadline} }
.xm-promo a:hover, .xm-promo-btn:hover{ text-decoration:underline }

.xm-city-grid{ display:grid; grid-template-columns:1fr 1fr; gap:2px 14px }
.xm-city-toggle{
  width:100%; display:flex; align-items:center; justify-content:space-between;
  border:none; background:none; cursor:pointer; padding:8px 10px; border-radius:8px;
  font:600 13px ${FONT_STACK}; color:${COLORS.ink}; transition:background .13s ease;
}
.xm-city-toggle:hover{ background:${COLORS.purpleTint}; color:${COLORS.purple} }
.xm-city-toggle .c{ font-size:9px; color:${COLORS.muted} }
.xm-city-toggle.is-open{ color:${COLORS.purple}; font-weight:800 }
.xm-city .xm-chips{ padding:4px 10px 8px 10px }
`

addPropertyControls(DesktopHeader as any, {
    solid: {
        type: ControlType.Boolean,
        title: "Solid Purple",
        defaultValue: false,
    },
})

export default DesktopHeader
