export const COLORS = {
    purple: "#542770",
    purpleLight: "#5E2C7E",
    purpleDark: "#3A1A4E",
    purpleXplanDark: "#3E1C54",
    green: "#6BB85C",
    greenHoverOnDark: "#8FD481",
    greenDark: "#4E9B41",
    greenTint: "#EEF7EC",
    footerGreenHeading: "#8FD481",
    ink: "#0F172A",
    body: "#475569",
    muted: "#94A3B8",
    border: "#E7E7EA",
    softBg: "#F7F6FA",
    purpleTint: "#F4F1F8",
    stars: "#F6A723",
    promoGreenHeadline: "#3D7A33",
}

export const GRADIENTS = {
    hero: "linear-gradient(180deg, #5E2C7E 0%, #542770 45%, #3A1A4E 100%)",
    heroMobile: "linear-gradient(180deg, #5E2C7E 0%, #542770 50%, #3A1A4E 100%)",
    xplan: "linear-gradient(135deg, #5E2C7E, #542770 45%, #3E1C54)",
    footerAccent: "linear-gradient(90deg, #6BB85C, #542770)",
}

export const SHADOWS = {
    cardHover: "0 12px 30px rgba(84,39,112,.12)",
    greenGlowLight: "0 6px 18px rgba(107,184,92,.35)",
    greenGlowHero: "0 8px 24px rgba(0,0,0,.25)",
    van: "drop-shadow(0 24px 30px rgba(0,0,0,.35))",
    dropdown: "0 30px 60px rgba(15,23,42,.3)",
    xplanCard: "0 20px 50px rgba(15,23,42,.25)",
}

export const RADII = {
    button: 11,
    card: 16,
    panel: 22,
    pill: 999,
}

export const FONT_STACK =
    '"Montserrat", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'

export function ensureMontserrat() {
    if (typeof document === "undefined") return
    if (document.querySelector("link[data-xhac-montserrat]")) return
    const l = document.createElement("link")
    l.rel = "stylesheet"
    l.href =
        "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&display=swap"
    l.setAttribute("data-xhac-montserrat", "true")
    document.head.appendChild(l)
}

export const PHONE_DISPLAY = "(844) 584-7399"
export const PHONE_TEL = "tel:18445847399"

const CDN = "https://cdn.jsdelivr.net/gh/extremheating-cloud/extreme-assets@main/images/brand"
export const ASSETS = {
    logoWhite: `${CDN}/logo-white.png`,
    xMark: `${CDN}/x-mark.png`,
    van: "https://cdn.jsdelivr.net/gh/extremheating-cloud/extreme-assets@403e2bee79/images/brand/van.png",
}

export function openScheduleDialog() {
    try {
        if (
            typeof window !== "undefined" &&
            window.parent &&
            window.parent !== window
        ) {
            window.parent.dispatchEvent(
                new (window.parent as any).CustomEvent("open-contact-dialog")
            )
            return
        }
    } catch {}
    window.dispatchEvent(new CustomEvent("open-contact-dialog"))
}
