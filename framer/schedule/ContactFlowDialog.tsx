import * as React from "react"

/* =====================================================================
 * Schedule Service Wizard — 4 steps + confirmation
 * Redesign per design_handoff_schedule_wizard/README.md
 * Flow: Service+Details → Time → Property+Notes (skippable) → Contact+Review → Done
 * =================================================================== */

type StepIdx = 0 | 1 | 2 | 3

/* SMS consent, A2P 10DLC. This wording is the approved text from the requirements
 * doc and is stored verbatim alongside the number and a timestamp as the TCPA
 * record. If it changes here it changes in the campaign registration too, so treat
 * it the way the widget's disclosure is treated: do not reword it locally.
 *
 * Note the wizard already asks Call / Text / Email as a *preference*. A preference
 * is not consent, and the phone placeholder already promises "we text your
 * confirmation here", so before this the site was announcing texts with no
 * disclosure attached to them at all. */
const SMS_CONSENT_TEXT =
    "Yes, text me about my service request at the number above. Consent is not a " +
    "condition of purchase. Msg & data rates may apply, message frequency varies. " +
    "Reply HELP for help or STOP to opt out. See our Privacy Policy and Terms."

type FormState = {
    service?: "heatingCooling" | "plumbing" | "quote" | "xplan"
    hvacIssue?: string
    hvacDuration?: string
    detail?: string
    answers?: Record<string, string>
    propertyType?: string
    occupant?: string
    systemAge?: string
    unitLocation?: string
    previousCustomer?: string
    apptDate?: string // ISO yyyy-mm-dd
    apptSlot?: string
    preferredContact?: "Call" | "Text" | "Email"
}

/* ---------- Design tokens (per handoff) ---------- */
const T = {
    headerGradA: "#42285C",
    headerGradB: "#331E4A",
    deepPurple: "#42285C",
    ink: "#251536",
    muted: "#7A6F8A",
    border: "#E4DEED",
    hairline: "#EFEAF4",
    surface: "#F5F2F9",
    surface2: "#F7F5FA",
    tint: "#F3FAF3",
    progressGreen: "#5BC24C",
    selGreen: "#2FA24B",
    chipGreen: "#1E7C34",
    btnGradA: "#35A94E",
    btnGradB: "#1E8A3C",
    linkGreen: "#1E8A3C",
    eyebrow: "#7ED957",
    qpBorder: "#CBE6CB",
    qpCard: "#DCEFDC",
    placeholder: "#B4AAC4",
    disabledDay: "#D5CEDF",
    dashed: "#C9BFDA",
    btnDisabled: "#DCD6E4",
    btnDisabledText: "#9E93AF",
    red: "#D2382C",
}

const FONT = "Poppins, system-ui, sans-serif"

const EMERGENCY_PHONE_DISPLAY = "(844) 584-7399"
const EMERGENCY_PHONE_TEL = "+18445847399"
const DISPATCH_FEE = "$97"

/* Dispatch-fee copy varies by service — "full system check" is HVAC language */
function feeCopy(
    service: FormState["service"],
    mobile: boolean
): string {
    const what =
        service === "plumbing"
            ? "a complete plumbing diagnosis"
            : service === "quote"
              ? "an in-home assessment"
              : service === "xplan"
                ? "your seasonal system check"
                : "a full system check"
    const short =
        service === "plumbing"
            ? "plumbing diagnosis"
            : service === "quote"
              ? "in-home assessment"
              : service === "xplan"
                ? "seasonal system check"
                : "full system check"
    return mobile
        ? `Travel + ${short}, quoted up front.`
        : `Covers your technician's travel and ${what} — quoted up front, no surprises at the door.`
}

const STEP_LABELS = ["SERVICE", "TIME", "DETAILS", "CONFIRM"]
const STEP_TITLES = [
    "What's going on?",
    "When works for you?",
    "About your home",
    "Confirm & book",
]

const TIME_SLOTS = [
    "8:00 AM – 10:00 AM",
    "10:00 AM – 12:00 PM",
    "12:00 PM – 2:00 PM",
    "2:00 PM – 4:00 PM",
]
const SLOT_SHORT: Record<string, string> = {
    [TIME_SLOTS[0]]: "8–10 AM",
    [TIME_SLOTS[1]]: "10 AM–12 PM",
    [TIME_SLOTS[2]]: "12–2 PM",
    [TIME_SLOTS[3]]: "2–4 PM",
}

const SERVICE_LABEL: Record<NonNullable<FormState["service"]>, string> = {
    heatingCooling: "Heating & Cooling",
    plumbing: "Plumbing",
    quote: "Get a Quote",
    xplan: "X-Plan Maintenance Plan",
}

/* HVAC step-1 chips (per handoff) */
const HVAC_ISSUES = [
    "No Heat",
    "No Cool",
    "Making Noise",
    "Thermostat",
    "Leaking Water",
    "Air Quality",
    "Tune-Up",
]
const HVAC_DURATIONS = ["Today", "A few days", "A week or more", "Not sure"]

/* Existing question sets, reused for Plumbing / Get a Quote / X-Plan */
const SERVICE_OPTIONS: Record<string, string[]> = {
    plumbing: [
        "Drain Cleaning",
        "Water Heater Issue",
        "Sump Pump Issue",
        "Leak Detection",
        "Gas Line Issue",
        "Water Treatment",
        "Pipe Leak",
        "General Plumbing Repair",
    ],
    quote: [
        "New System Estimate",
        "Duct Cleaning Estimate",
        "Dryer Vent Cleaning Estimate",
        "HVAC Inspection Estimate",
    ],
    xplan: [
        "Schedule Seasonal Tune-Up",
        "Enroll in Plan",
        "Questions About Benefits",
        "Billing / Payment Question",
    ],
}

type SubQuestion = {
    id: string
    label: string
    field: string
    options: string[]
    optional?: boolean
}

const DUCT_VENT_OPTIONS = ["1–10 vents", "11–20 vents", "20+ vents", "Not sure"]

/* One high-value follow-up per service, max — conversion first. */
const DETAIL_QUESTIONS: Record<string, SubQuestion[]> = {
    /* Plumbing */
    "Drain Cleaning": [
        {
            id: "which",
            label: "Which drain is affected?",
            field: "Affected drain",
            options: [
                "Kitchen",
                "Bathroom",
                "Toilet",
                "Shower / Tub",
                "Main line",
                "Multiple",
                "Not sure",
            ],
        },
    ],
    "Water Heater Issue": [
        {
            id: "problem",
            label: "What's the problem?",
            field: "Problem",
            options: [
                "No hot water",
                "Not enough hot water",
                "Leaking",
                "Other",
            ],
        },
    ],
    "Sump Pump Issue": [
        {
            id: "problem",
            label: "What's happening?",
            field: "Problem",
            options: [
                "Not running",
                "Running constantly",
                "Pit overflowing",
                "Not sure",
            ],
        },
    ],
    "Leak Detection": [
        {
            id: "where",
            label: "Where do you suspect the leak?",
            field: "Suspected location",
            options: [
                "Under a sink",
                "Wall / ceiling",
                "Floor / slab",
                "Outdoor",
                "Not sure",
            ],
        },
    ],
    "Gas Line Issue": [
        {
            id: "need",
            label: "What do you need?",
            field: "Request",
            options: [
                "Smell of gas",
                "New appliance hookup",
                "Suspected leak",
                "Other",
            ],
        },
    ],
    "Water Treatment": [
        {
            id: "interest",
            label: "What are you interested in?",
            field: "Interest",
            options: [
                "Water softener",
                "Filtration",
                "Water testing",
                "Not sure",
            ],
        },
    ],
    "Pipe Leak": [
        {
            id: "where",
            label: "Where is the leak?",
            field: "Leak location",
            options: [
                "Under a sink",
                "Wall / ceiling",
                "Basement",
                "Outdoor",
                "Not sure",
            ],
        },
    ],
    "General Plumbing Repair": [
        {
            id: "fixture",
            label: "What needs attention?",
            field: "Fixture",
            options: [
                "Faucet",
                "Toilet",
                "Garbage disposal",
                "Shower / Tub",
                "Other",
            ],
        },
    ],

    /* Get a Quote */
    "New System Estimate": [
        {
            id: "scope",
            label: "What's the quote for?",
            field: "Quote scope",
            options: [
                "AC only",
                "Furnace only",
                "Full system (AC + furnace)",
            ],
        },
    ],
    "Duct Cleaning Estimate": [
        {
            id: "vents",
            label: "Roughly how many vents?",
            field: "Vent count",
            options: DUCT_VENT_OPTIONS,
        },
    ],
    "Dryer Vent Cleaning Estimate": [],
    "HVAC Inspection Estimate": [
        {
            id: "reason",
            label: "Reason for inspection?",
            field: "Reason",
            options: [
                "Home purchase",
                "Routine check",
                "Performance concern",
                "Other",
            ],
        },
    ],

    /* X-Plan */
    "Schedule Seasonal Tune-Up": [
        {
            id: "system",
            label: "Which system?",
            field: "System",
            options: ["Heating", "Cooling", "Both"],
        },
    ],
    "Enroll in Plan": [],
}

function getSubQuestions(detail?: string): SubQuestion[] {
    if (!detail) return []
    return DETAIL_QUESTIONS[detail] || []
}

/* Step-3 option sets (per handoff — all optional) */
const AGE_OPTIONS = [
    "Under 5 years",
    "5–10 years",
    "10–15 years",
    "15+ years",
    "Not sure",
]
const UNIT_LOCATIONS = [
    "Side of house",
    "Backyard",
    "Rooftop",
    "Ground level",
    "Not sure",
]

/* HVAC-equipment questions only make sense for HVAC-related requests —
 * never for plumbing (e.g. Drain Cleaning). */
function isHvacContext(
    service?: FormState["service"],
    detail?: string
): boolean {
    if (service === "heatingCooling") return true
    if (service === "xplan") return true
    if (
        service === "quote" &&
        (detail === "New System Estimate" ||
            detail === "HVAC Inspection Estimate")
    )
        return true
    return false
}

/* ---------- Cloudinary (existing backend: 5 photos / 10MB) ---------- */
const CLOUDINARY_CLOUD = "dsbmasn0l"
const CLOUDINARY_UNSIGNED_PRESET = "images"

async function uploadPhotosToCloudinary(files: File[]): Promise<string[]> {
    const urls: string[] = []
    for (const f of files) {
        const fd = new FormData()
        fd.append("file", f)
        fd.append("upload_preset", CLOUDINARY_UNSIGNED_PRESET)
        const res = await fetch(
            `https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD}/auto/upload`,
            { method: "POST", body: fd }
        )
        if (!res.ok) throw new Error("Upload failed")
        const json = await res.json()
        urls.push(json.secure_url)
    }
    return urls
}

const FORMSPREE_ENDPOINT = "https://formspree.io/f/mqadkggp"

/* ---------- Address autocomplete (existing) ---------- */
const GOOGLE_MAPS_API_KEY = "AIzaSyABVMGJ738G-WyGCCCr_YlIk2yEGln_jeY"
const GEO_BIAS_LAT = 39.7589
const GEO_BIAS_LON = -84.1916

// Restrict suggestions to Ohio
const OHIO_BOUNDS = {
    south: 38.4,
    west: -84.82,
    north: 42.0,
    east: -80.52,
}
const OHIO_RE = /,\s*(OH\b|Ohio)/i

type AddressSuggestion = { id: string; label: string; src: "google" | "photon" }

// Set when the Maps key is rejected (bad referrer restriction, billing, etc.)
// so we stop retrying Google and use the free fallback for the session.
let googleUnavailable = false
if (typeof window !== "undefined") {
    ;(window as any).gm_authFailure = () => {
        googleUnavailable = true
        console.warn(
            "[XHAC] Google Maps auth failed — check the API key's website restrictions. Falling back to free geocoder."
        )
    }
}

let googleMapsPromise: Promise<any> | null = null
function loadGoogleMaps(key: string): Promise<any> {
    if (typeof window === "undefined") return Promise.reject()
    const w = window as any
    if (w.google?.maps?.places) return Promise.resolve(w.google)
    if (googleMapsPromise) return googleMapsPromise
    googleMapsPromise = new Promise((resolve, reject) => {
        const cbName = "__xhacGmapsInit"
        w[cbName] = () => resolve(w.google)
        const s = document.createElement("script")
        s.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(
            key
        )}&libraries=places&callback=${cbName}`
        s.async = true
        s.defer = true
        s.onerror = () => reject(new Error("Google Maps failed to load"))
        document.head.appendChild(s)
    })
    return googleMapsPromise
}

async function googlePredictions(query: string): Promise<AddressSuggestion[]> {
    const google = await loadGoogleMaps(GOOGLE_MAPS_API_KEY)
    const svc = new google.maps.places.AutocompleteService()
    return new Promise((resolve, reject) => {
        svc.getPlacePredictions(
            {
                input: query,
                componentRestrictions: { country: "us" },
                types: ["address"],
                locationRestriction: OHIO_BOUNDS,
            },
            (preds: any[], status: string) => {
                const S = google.maps.places.PlacesServiceStatus
                if (status === S.OK && preds) {
                    resolve(
                        preds
                            .filter((p) => OHIO_RE.test(p.description))
                            .map((p) => ({
                                id: p.place_id,
                                label: p.description.replace(/,\s*USA$/, ""),
                                src: "google" as const,
                            }))
                    )
                } else if (status === S.ZERO_RESULTS) {
                    resolve([])
                } else {
                    // REQUEST_DENIED / OVER_QUERY_LIMIT / etc. — treat as a
                    // real failure so the caller falls back to Photon.
                    console.warn("[XHAC] Places autocomplete status:", status)
                    reject(new Error(`Places status: ${status}`))
                }
            }
        )
    })
}

async function googlePlaceDetails(placeId: string): Promise<string | null> {
    try {
        const google = await loadGoogleMaps(GOOGLE_MAPS_API_KEY)
        const svc = new google.maps.places.PlacesService(
            document.createElement("div")
        )
        return new Promise((resolve) => {
            svc.getDetails(
                { placeId, fields: ["formatted_address"] },
                (place: any, status: string) => {
                    if (
                        status ===
                            google.maps.places.PlacesServiceStatus.OK &&
                        place?.formatted_address
                    ) {
                        resolve(
                            place.formatted_address.replace(/,\s*USA$/, "")
                        )
                    } else {
                        resolve(null)
                    }
                }
            )
        })
    } catch {
        return null
    }
}

async function photonPredictions(query: string): Promise<AddressSuggestion[]> {
    const url =
        `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}` +
        `&limit=8&lang=en&lat=${GEO_BIAS_LAT}&lon=${GEO_BIAS_LON}` +
        `&bbox=${OHIO_BOUNDS.west},${OHIO_BOUNDS.south},${OHIO_BOUNDS.east},${OHIO_BOUNDS.north}`
    const res = await fetch(url)
    if (!res.ok) return []
    const json = await res.json()
    const feats: any[] = json?.features || []
    // OSM often lacks individual address points; keep the house number the
    // customer typed and prepend it when a matched street doesn't have one.
    const typedHouseNum = (query.match(/^\s*(\d+)\s+/) || [])[1] || ""
    return feats
        .filter((f) => (f.properties?.state || "") === "Ohio")
        .map((f, i) => {
            const p = f.properties || {}
            const street = p.street || p.name || ""
            const houseNum = p.housenumber || typedHouseNum
            const line1 =
                [houseNum, street].filter(Boolean).join(" ") || p.name
            const parts = [
                line1,
                p.city || p.town || p.village || p.county,
                p.state,
                p.postcode,
            ].filter(Boolean)
            return {
                id: `${i}-${p.osm_id || line1 || ""}`,
                label: parts.join(", "),
                src: "photon" as const,
            }
        })
        .filter((s) => s.label.trim().length > 0)
        .slice(0, 5)
}

async function fetchAddressSuggestions(
    query: string
): Promise<AddressSuggestion[]> {
    if (query.trim().length < 3) return []
    try {
        if (GOOGLE_MAPS_API_KEY && !googleUnavailable)
            return await googlePredictions(query)
        return await photonPredictions(query)
    } catch {
        try {
            return await photonPredictions(query)
        } catch {
            return []
        }
    }
}

/* ---------- Tracking (existing events, re-mapped to merged steps) ---------- */
declare global {
    interface Window {
        gtag?: (...args: any[]) => void
        fbq?: (...args: any[]) => void
        google?: any
    }
}

function getDeviceType(): "Desktop" | "Tablet" | "Mobile" {
    const ua = navigator.userAgent
    if (/iPad|Tablet/i.test(ua)) return "Tablet"
    if (/Mobi|Android/i.test(ua)) return "Mobile"
    return "Desktop"
}

function storeClickIds() {
    if (typeof window === "undefined") return
    const params = new URLSearchParams(window.location.search)
    const gclid = params.get("gclid")
    const gbraid = params.get("gbraid")
    const wbraid = params.get("wbraid")
    if (gclid) localStorage.setItem("xhac_gclid", gclid)
    if (gbraid) localStorage.setItem("xhac_gbraid", gbraid)
    if (wbraid) localStorage.setItem("xhac_wbraid", wbraid)
}
storeClickIds()

/* ---------- Date helpers ---------- */
function toISO(d: Date): string {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
        2,
        "0"
    )}-${String(d.getDate()).padStart(2, "0")}`
}

function fromISO(iso: string): Date {
    const [y, m, d] = iso.split("-").map(Number)
    return new Date(y, m - 1, d)
}

function fmtDay(iso: string, style: "short" | "long" = "short"): string {
    const d = fromISO(iso)
    return d.toLocaleDateString(
        "en-US",
        style === "short"
            ? { weekday: "short", month: "short", day: "numeric" }
            : { weekday: "long" }
    )
}

function startOfToday(): Date {
    const d = new Date()
    d.setHours(0, 0, 0, 0)
    return d
}

/* Next N selectable weekdays starting tomorrow */
function upcomingWeekdays(count: number): string[] {
    const out: string[] = []
    const d = startOfToday()
    d.setDate(d.getDate() + 1)
    while (out.length < count) {
        const dow = d.getDay()
        if (dow !== 0 && dow !== 6) out.push(toISO(d))
        d.setDate(d.getDate() + 1)
    }
    return out
}

/* First 3 available slots for the quick-pick strip */
function computeQuickPicks(): { label: string; iso: string; slot: string }[] {
    const days = upcomingWeekdays(2)
    const tomorrow = toISO(
        (() => {
            const t = startOfToday()
            t.setDate(t.getDate() + 1)
            return t
        })()
    )
    const dayLabel = (iso: string) =>
        iso === tomorrow
            ? "Tomorrow"
            : fromISO(iso).toLocaleDateString("en-US", { weekday: "short" })
    return [
        {
            label: `${dayLabel(days[0])} · ${SLOT_SHORT[TIME_SLOTS[0]]}`,
            iso: days[0],
            slot: TIME_SLOTS[0],
        },
        {
            label: `${dayLabel(days[0])} · ${SLOT_SHORT[TIME_SLOTS[1]]}`,
            iso: days[0],
            slot: TIME_SLOTS[1],
        },
        {
            label: `${dayLabel(days[1])} · ${SLOT_SHORT[TIME_SLOTS[0]]}`,
            iso: days[1],
            slot: TIME_SLOTS[0],
        },
    ]
}

/* .ics download for "Add to calendar" */
function downloadICS(iso: string, slot: string, service: string) {
    const startHour: Record<string, number> = {
        [TIME_SLOTS[0]]: 8,
        [TIME_SLOTS[1]]: 10,
        [TIME_SLOTS[2]]: 12,
        [TIME_SLOTS[3]]: 14,
    }
    const d = fromISO(iso)
    const h = startHour[slot] ?? 8
    const pad = (n: number) => String(n).padStart(2, "0")
    const dt = (hh: number) =>
        `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}T${pad(
            hh
        )}0000`
    const ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Extreme Heating//Schedule//EN",
        "BEGIN:VEVENT",
        `DTSTART:${dt(h)}`,
        `DTEND:${dt(h + 2)}`,
        `SUMMARY:Extreme Heating, Air, Plumbing — ${service}`,
        `DESCRIPTION:Arrival window ${slot}. Questions? Call ${EMERGENCY_PHONE_DISPLAY}.`,
        "END:VEVENT",
        "END:VCALENDAR",
    ].join("\r\n")
    const blob = new Blob([ics], { type: "text/calendar" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "extreme-visit.ics"
    a.click()
    URL.revokeObjectURL(url)
}

/* ---------- Icons (2px stroke, deep purple, per handoff) ---------- */
function IconHVAC({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <path
                d="M4 8h16M4 12h16M4 16h16"
                stroke={T.deepPurple}
                strokeWidth="2"
                strokeLinecap="round"
            />
        </svg>
    )
}
function IconPlumb({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <circle
                cx="12"
                cy="12"
                r="8"
                stroke={T.deepPurple}
                strokeWidth="2"
            />
            <circle cx="12" cy="12" r="2" fill={T.deepPurple} />
        </svg>
    )
}
function IconQuote({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <rect
                x="5"
                y="3"
                width="14"
                height="18"
                rx="2"
                stroke={T.deepPurple}
                strokeWidth="2"
            />
            <path
                d="M9 8h6M9 12h6M9 16h4"
                stroke={T.deepPurple}
                strokeWidth="2"
                strokeLinecap="round"
            />
        </svg>
    )
}
function IconPlan({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <rect
                x="3"
                y="5"
                width="18"
                height="16"
                rx="2"
                stroke={T.deepPurple}
                strokeWidth="2"
            />
            <path
                d="M3 10h18M8 3v4M16 3v4"
                stroke={T.deepPurple}
                strokeWidth="2"
                strokeLinecap="round"
            />
        </svg>
    )
}

/* ---------- Load Poppins once ---------- */
function ensurePoppins() {
    if (typeof document === "undefined") return
    if (document.querySelector("link[data-xhac-poppins]")) return
    const l = document.createElement("link")
    l.rel = "stylesheet"
    l.href =
        "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
    l.setAttribute("data-xhac-poppins", "true")
    document.head.appendChild(l)
}

/* =====================================================================
 * Component
 * =================================================================== */
export default function ContactFlowDialog() {
    const [open, setOpen] = React.useState(false)
    const [appeared, setAppeared] = React.useState(false)

    const [step, setStep] = React.useState<StepIdx>(0)
    const [booked, setBooked] = React.useState(false)

    const [data, setData] = React.useState<FormState>({
        preferredContact: "Text",
    })
    const [noteOpen, setNoteOpen] = React.useState(false)
    const [note, setNote] = React.useState("")
    const [photos, setPhotos] = React.useState<File[]>([])
    const [firstName, setFirstName] = React.useState("")
    const [lastName, setLastName] = React.useState("")
    const [phoneDigits, setPhoneDigits] = React.useState("")
    const [email, setEmail] = React.useState("")
    const [address, setAddress] = React.useState("")
    const [feeOk, setFeeOk] = React.useState(false)
    // SMS consent for A2P 10DLC. MUST default to false: a pre-ticked consent box is
    // rejection code 30925 by itself. Deliberately NOT part of stepComplete — consent
    // is not a condition of purchase, so the wizard submits either way and the
    // customer simply does not get texted.
    const [smsOk, setSmsOk] = React.useState(false)
    const [submitting, setSubmitting] = React.useState(false)

    const [addrSuggestions, setAddrSuggestions] = React.useState<
        AddressSuggestion[]
    >([])
    const [addrLoading, setAddrLoading] = React.useState(false)
    const [addrOpen, setAddrOpen] = React.useState(false)
    const addrDebounce = React.useRef<number | null>(null)
    const addrSeq = React.useRef(0)

    const photoInputRef = React.useRef<HTMLInputElement | null>(null)

    const quickPicks = React.useMemo(computeQuickPicks, [open])

    const photoPreviews = React.useMemo(
        () => photos.map((f) => ({ file: f, url: URL.createObjectURL(f) })),
        [photos]
    )
    React.useEffect(() => {
        return () => photoPreviews.forEach((p) => URL.revokeObjectURL(p.url))
    }, [photoPreviews])

    const [vw, setVw] = React.useState<number>(
        typeof window !== "undefined" ? window.innerWidth : 1200
    )
    React.useEffect(() => {
        const onR = () => setVw(window.innerWidth)
        onR()
        window.addEventListener("resize", onR)
        return () => window.removeEventListener("resize", onR)
    }, [])
    const isMobile = vw <= 809

    React.useEffect(ensurePoppins, [])

    /* dialog open tracking (existing event) */
    const openedOnceRef = React.useRef(false)
    React.useEffect(() => {
        if (open && !openedOnceRef.current) {
            openedOnceRef.current = true
            window.gtag?.("event", "schedule_dialog_open", {
                event_category: "Schedule Engine",
                event_label: "Dialog Opened",
                device_type: getDeviceType(),
            })
        }
        if (!open) openedOnceRef.current = false
    }, [open])

    /* open bridge (existing) */
    React.useEffect(() => {
        const handler = () => {
            setOpen(true)
            setStep(0)
            setBooked(false)
            setData({ preferredContact: "Text" })
            setNoteOpen(false)
            setNote("")
            setPhotos([])
            setFirstName("")
            setLastName("")
            setPhoneDigits("")
            setEmail("")
            setAddress("")
            setFeeOk(false)
            setAddrSuggestions([])
            setAddrOpen(false)
        }
        window.addEventListener("open-contact-dialog", handler as EventListener)
        const onMessage = (e: MessageEvent) => {
            if (e?.data?.type === "open-contact-dialog") handler()
        }
        window.addEventListener("message", onMessage)
        return () => {
            window.removeEventListener(
                "open-contact-dialog",
                handler as EventListener
            )
            window.removeEventListener("message", onMessage)
        }
    }, [])

    React.useEffect(() => {
        if (open) {
            const id = requestAnimationFrame(() => setAppeared(true))
            return () => cancelAnimationFrame(id)
        } else {
            setAppeared(false)
        }
    }, [open])

    if (!open) return null

    const close = () => setOpen(false)

    /* ---------- validation + hints (per handoff) ---------- */
    const emailOk =
        email.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
    const phoneOk = phoneDigits.length === 10

    function serviceStepComplete(d: FormState): boolean {
        if (!d.service) return false
        if (d.service === "heatingCooling") return !!d.hvacIssue
        // Plumbing / Quote / X-Plan: only the sub-service is required here;
        // their follow-up questions live on the Details step (all optional).
        return !!d.detail
    }

    // Free estimates: New System, Duct Cleaning, Dryer Vent. HVAC
    // Inspection still carries the dispatch fee.
    const freeEstimate =
        data.service === "quote" &&
        data.detail !== "HVAC Inspection Estimate"
    const feeRequired = !freeEstimate

    const stepComplete: boolean[] = [
        serviceStepComplete(data),
        !!data.apptDate && !!data.apptSlot,
        true,
        Boolean(
            firstName.trim() &&
                phoneOk &&
                address.trim().length >= 5 &&
                (feeOk || !feeRequired) &&
                emailOk
        ),
    ]

    const hints: string[] = [
        !data.service
            ? "Pick a service to continue"
            : !stepComplete[0]
              ? data.service === "heatingCooling"
                  ? "Pick the issue to continue"
                  : "Pick what you need to continue"
              : "",
        !stepComplete[1] ? "Pick a day and arrival window" : "",
        "Everything here is skippable",
        !stepComplete[3]
            ? feeRequired
                ? "Add your name, mobile & address, then accept the fee"
                : "Add your name, mobile & address to book"
            : "",
    ]

    const canContinue = stepComplete[step]

    /* ---------- helpers ---------- */
    const patch = (p: Partial<FormState>) => setData((d) => ({ ...d, ...p }))

    /* single-select chip w/ toggle-deselect (per handoff) */
    const toggle = (key: keyof FormState, value: string) =>
        setData((d) => ({
            ...d,
            [key]: (d[key] as any) === value ? undefined : value,
        }))

    const toggleAnswer = (id: string, value: string) =>
        setData((d) => {
            const answers = { ...(d.answers || {}) }
            if (answers[id] === value) delete answers[id]
            else answers[id] = value
            return { ...d, answers }
        })

    function formatPhone(d: string): string {
        const s = d.replace(/\D/g, "").slice(0, 10)
        if (s.length <= 3) return s
        if (s.length <= 6) return `${s.slice(0, 3)}-${s.slice(3)}`
        return `${s.slice(0, 3)}-${s.slice(3, 6)}-${s.slice(6)}`
    }

    function onAddressChange(v: string) {
        setAddress(v)
        setAddrOpen(true)
        if (addrDebounce.current) window.clearTimeout(addrDebounce.current)
        if (v.trim().length < 3) {
            setAddrSuggestions([])
            setAddrLoading(false)
            return
        }
        setAddrLoading(true)
        addrDebounce.current = window.setTimeout(async () => {
            const seq = ++addrSeq.current
            const results = await fetchAddressSuggestions(v)
            if (seq === addrSeq.current) {
                setAddrSuggestions(results)
                setAddrLoading(false)
            }
        }, 280)
    }

    async function selectAddress(sugg: AddressSuggestion) {
        setAddress(sugg.label)
        setAddrSuggestions([])
        setAddrOpen(false)
        // Upgrade to the full formatted address (incl. ZIP) — Google results only.
        if (sugg.src === "google") {
            const full = await googlePlaceDetails(sugg.id)
            if (full) setAddress(full)
        }
    }

    const goNext = () => setStep((s) => Math.min(s + 1, 3) as StepIdx)
    const goBack = () => setStep((s) => Math.max(s - 1, 0) as StepIdx)

    /* ---------- submit (existing Formspree handoff) ---------- */
    async function bookVisit() {
        if (submitting || !canContinue) return
        setSubmitting(true)

        const serviceLabel =
            (data.service ? SERVICE_LABEL[data.service] : "") || ""
        const serviceRequired =
            data.service === "heatingCooling"
                ? data.hvacIssue || ""
                : data.detail || ""

        let photoUrls: string[] = []
        try {
            if (photos?.length) {
                photoUrls = await uploadPhotosToCloudinary(photos)
            }
        } catch (e) {
            console.warn("Photo upload failed:", e)
        }

        const fd = new FormData()
        fd.set("First Name", firstName.trim())
        fd.set("Last Name", lastName.trim())
        fd.set("Phone Number", formatPhone(phoneDigits))
        if (email.trim()) fd.set("Email", email.trim())
        fd.set("Service Address", address.trim())
        // SMS consent is deliberately NOT sent to Formspree (removed 2026-08-13).
        // The checkbox still renders and still governs whether we may text this
        // person, but nothing about it leaves the browser any more, so there is
        // currently no stored record of who agreed. If that record is needed as
        // the TCPA proof, it has to be captured somewhere first — reinstating
        // these four fields is the smallest way back:
        //   "SMS Consent"           smsOk ? "YES" : "NO"      (always, both ways)
        //   "SMS Consent Timestamp" new Date().toISOString()  (only when true)
        //   "SMS Consent Page"      window.location.href      (only when true)
        //   "SMS Consent Text"      SMS_CONSENT_TEXT          (only when true)
        if (data.previousCustomer)
            fd.set("Previous Customer", data.previousCustomer)
        if (data.preferredContact)
            fd.set("Preferred Contact Method", data.preferredContact)
        fd.set("Issue", serviceLabel)
        fd.set("Service Required", serviceRequired)
        if (data.service === "heatingCooling" && data.hvacDuration)
            fd.set(`${serviceRequired} – How long`, data.hvacDuration)
        getSubQuestions(data.detail).forEach((q) => {
            const v = data.answers?.[q.id]
            if (v) fd.set(`${serviceRequired} – ${q.field}`, v)
        })
        if (data.propertyType) fd.set("Property Type", data.propertyType)
        if (data.occupant)
            fd.set(
                "Occupant Role",
                data.occupant === "Owner / Landlord"
                    ? "Owner / Landlord"
                    : data.occupant
            )
        if (data.systemAge)
            fd.set(
                data.service === "plumbing"
                    ? "Approximate age of home"
                    : "Approximate age of system",
                data.systemAge
            )
        if (data.unitLocation) fd.set("Unit Location", data.unitLocation)
        fd.set(
            "Requested Date",
            data.apptDate ? fmtDay(data.apptDate, "short") : ""
        )
        fd.set("Requested Time Window", data.apptSlot || "")
        fd.set(
            "Dispatch Fee Acknowledged",
            freeEstimate
                ? "N/A (free estimate)"
                : feeOk
                  ? `Yes (${DISPATCH_FEE})`
                  : "No"
        )
        if (note.trim()) fd.set("message", note.trim())
        photoUrls.forEach((u) => fd.append("Attached Images", u))

        let ok = false,
            errText = ""
        try {
            const res = await fetch(FORMSPREE_ENDPOINT, {
                method: "POST",
                body: fd,
                headers: { Accept: "application/json" },
            })
            ok = res.ok
            if (!ok) {
                try {
                    const j = await res.json()
                    errText =
                        j?.errors?.map((e: any) => e.message).join(" ") ||
                        "Server returned an error."
                } catch {
                    errText = "Server returned an error."
                }
            }
        } catch {
            errText = "Network error. Please check your connection."
        }

        setSubmitting(false)
        if (ok) {
            window.gtag?.("event", "schedule_form_submit", {
                event_category: "Schedule Engine",
                event_label: "Form Submitted",
                device_type: getDeviceType(),
            })
            try {
                window.fbq?.("track", "Lead", {
                    event_source: "schedule_engine",
                    device_type: getDeviceType(),
                })
            } catch (err) {
                console.warn("Meta fbq error", err)
            }
            setBooked(true)
        } else {
            alert(errText || "There was a problem submitting your request.")
        }
    }

    /* ---------- shared bits ---------- */
    const chip = (
        selected: boolean,
        label: string,
        onClick: () => void,
        key?: string
    ) => (
        <button
            key={key ?? label}
            className={"xw-chip" + (selected ? " sel" : "")}
            onClick={onClick}
        >
            {selected ? "✓  " + label : label}
        </button>
    )

    const groupLabel = (text: string, optional?: boolean) => (
        <div className="xw-glabel">
            {text}
            {optional ? <span className="opt"> — optional</span> : null}
        </div>
    )

    const svcCards = [
        {
            key: "heatingCooling" as const,
            name: "Heating & Cooling",
            sub: "Repair or tune-up",
            icon: <IconHVAC />,
        },
        {
            key: "plumbing" as const,
            name: "Plumbing",
            sub: "Leaks, drains, heaters",
            icon: <IconPlumb />,
        },
        {
            key: "quote" as const,
            name: "Get a Quote",
            sub: "New system estimate",
            icon: <IconQuote />,
        },
        {
            key: "xplan" as const,
            name: "X-Plan",
            sub: "Membership & tune-ups",
            icon: <IconPlan />,
        },
    ]

    /* summary values for step 4 + done */
    const svcSummary = data.service
        ? `${SERVICE_LABEL[data.service].replace(" Maintenance Plan", "")}${
              data.service === "heatingCooling"
                  ? data.hvacIssue
                      ? " · " + data.hvacIssue
                      : ""
                  : data.detail
                    ? " · " + data.detail
                    : ""
          }`
        : ""
    const whenSummary =
        data.apptDate && data.apptSlot
            ? `${fmtDay(data.apptDate)} · ${SLOT_SHORT[data.apptSlot]}`
            : ""
    const homeSummary = [data.propertyType, data.occupant]
        .filter(Boolean)
        .join(" · ")

    /* =================================================================== */
    return (
        <div
            className="xw-root"
            role="dialog"
            aria-modal="true"
            style={{
                position: "fixed",
                inset: 0,
                zIndex: 9999,
                fontFamily: FONT,
            }}
        >
            <style>{XW_CSS}</style>

            {/* backdrop */}
            <div
                onClick={close}
                style={{
                    position: "absolute",
                    inset: 0,
                    background:
                        "linear-gradient(160deg, rgba(36,21,51,.92), rgba(58,35,82,.92))",
                    backdropFilter: "blur(6px)",
                    WebkitBackdropFilter: "blur(6px)",
                    opacity: appeared ? 1 : 0,
                    transition: "opacity 240ms ease",
                }}
            />

            {/* modal */}
            <div
                className="xw-modal"
                style={{
                    opacity: appeared ? 1 : 0,
                    transform: appeared
                        ? "translateY(0) scale(1)"
                        : "translateY(12px) scale(0.985)",
                }}
                onPointerDown={(e) => e.stopPropagation()}
                onPointerUp={(e) => e.stopPropagation()}
                onClick={(e) => e.stopPropagation()}
            >
                {/* ---------- HEADER ---------- */}
                <div className="xw-header">
                    {isMobile ? (
                        /* Compact mobile header (mockups 1c) */
                        <>
                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >
                                <div className="xw-eyebrow">
                                    Schedule Service
                                </div>
                                <button
                                    className="xw-close"
                                    onClick={close}
                                    aria-label="Close"
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="xw-title">
                                {booked
                                    ? "You're booked!"
                                    : STEP_TITLES[step]}
                            </div>
                            <div className="xw-progress">
                                {STEP_LABELS.map((label, i) => {
                                    const done2 = booked || i < step
                                    const cur = !booked && i === step
                                    const clickable = !booked && i < step
                                    return (
                                        <div
                                            key={label}
                                            className={
                                                "xw-seg" +
                                                (clickable ? " click" : "")
                                            }
                                            onClick={() =>
                                                clickable &&
                                                setStep(i as StepIdx)
                                            }
                                        >
                                            <div
                                                className="bar"
                                                style={{
                                                    background:
                                                        done2 || cur
                                                            ? T.progressGreen
                                                            : "rgba(255,255,255,.18)",
                                                }}
                                            />
                                        </div>
                                    )
                                })}
                                {!booked && (
                                    <div className="xw-stepcount">
                                        {step + 1} of 4
                                    </div>
                                )}
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="xw-headtop">
                                <div style={{ minWidth: 0 }}>
                                    <div className="xw-eyebrow">
                                        Schedule Service
                                    </div>
                                    <div className="xw-title">
                                        {booked
                                            ? "You're booked!"
                                            : STEP_TITLES[step]}
                                    </div>
                                </div>
                                <div className="xw-headright">
                                    {!booked && (
                                        <a
                                            className="xw-emergency"
                                            href={`tel:${EMERGENCY_PHONE_TEL}`}
                                        >
                                            <span className="dot" />
                                            Emergency?{" "}
                                            {EMERGENCY_PHONE_DISPLAY}
                                        </a>
                                    )}
                                    <button
                                        className="xw-close"
                                        onClick={close}
                                        aria-label="Close"
                                    >
                                        ✕
                                    </button>
                                </div>
                            </div>

                            <div className="xw-progress">
                                {STEP_LABELS.map((label, i) => {
                                    const done2 = booked || i < step
                                    const cur = !booked && i === step
                                    const clickable = !booked && i < step
                                    return (
                                        <div
                                            key={label}
                                            className={
                                                "xw-seg" +
                                                (clickable ? " click" : "")
                                            }
                                            onClick={() =>
                                                clickable &&
                                                setStep(i as StepIdx)
                                            }
                                        >
                                            <div
                                                className="bar"
                                                style={{
                                                    background:
                                                        done2 || cur
                                                            ? T.progressGreen
                                                            : "rgba(255,255,255,.18)",
                                                }}
                                            />
                                            <div
                                                className="lab"
                                                style={{
                                                    color: booked
                                                        ? "rgba(255,255,255,.65)"
                                                        : cur
                                                          ? "#fff"
                                                          : done2
                                                            ? "rgba(255,255,255,.65)"
                                                            : "rgba(255,255,255,.45)",
                                                }}
                                            >
                                                {label}
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        </>
                    )}
                </div>

                {/* ---------- BODY ---------- */}
                <div className="xw-body">
                    {isMobile && !booked && (
                        <div className="xw-mpillwrap">
                            <a
                                className="xw-mpill"
                                href={`tel:${EMERGENCY_PHONE_TEL}`}
                            >
                                <span className="dot" />
                                Emergency? Tap to call
                            </a>
                        </div>
                    )}
                    {/* ============ DONE ============ */}
                    {booked ? (
                        <div className="xw-done xw-fade">
                            <div className="xw-donecheck">✓</div>
                            <div className="xw-doneh">
                                See you{" "}
                                {data.apptDate
                                    ? fmtDay(data.apptDate, "long")
                                    : "soon"}
                                {firstName.trim()
                                    ? `, ${firstName.trim()}`
                                    : ""}
                                !
                            </div>
                            <div className="xw-donesub">
                                {[svcSummary, whenSummary && whenSummary]
                                    .filter(Boolean)
                                    .join(" · ")}
                            </div>
                            <div className="xw-donesub">
                                Confirmation texted to{" "}
                                {formatPhone(phoneDigits)} — reply there to
                                reschedule anytime.
                            </div>
                            <div className="xw-donebtns">
                                <button
                                    className="xw-outline"
                                    onClick={() =>
                                        data.apptDate &&
                                        data.apptSlot &&
                                        downloadICS(
                                            data.apptDate,
                                            data.apptSlot,
                                            svcSummary
                                        )
                                    }
                                >
                                    Add to calendar
                                </button>
                                <button className="xw-cta" onClick={close}>
                                    Done
                                </button>
                            </div>
                            <div className="xw-donefoot">
                                Need it sooner? Call{" "}
                                <a
                                    href={`tel:${EMERGENCY_PHONE_TEL}`}
                                    style={{
                                        color: T.red,
                                        fontWeight: 600,
                                        textDecoration: "none",
                                    }}
                                >
                                    {EMERGENCY_PHONE_DISPLAY}
                                </a>
                            </div>
                        </div>
                    ) : (
                        <>
                            {/* ============ STEP 1: SERVICE ============ */}
                            {step === 0 && (
                                <div
                                    className="xw-fade"
                                    style={{ display: "grid", gap: 20 }}
                                >
                                    <div className="xw-svcrow">
                                        {svcCards.map((c) => {
                                            const sel =
                                                data.service === c.key
                                            return (
                                                <button
                                                    key={c.key}
                                                    className={
                                                        "xw-svc" +
                                                        (sel ? " sel" : "")
                                                    }
                                                    onClick={() =>
                                                        patch({
                                                            service: c.key,
                                                            hvacIssue:
                                                                undefined,
                                                            hvacDuration:
                                                                undefined,
                                                            detail: undefined,
                                                            answers: {},
                                                            systemAge:
                                                                undefined,
                                                            unitLocation:
                                                                undefined,
                                                        })
                                                    }
                                                >
                                                    <span className="tile">
                                                        {c.icon}
                                                    </span>
                                                    <span className="nm">
                                                        {c.name}
                                                    </span>
                                                    <span className="sb">
                                                        {c.sub}
                                                    </span>
                                                </button>
                                            )
                                        })}
                                    </div>

                                    {data.service === "heatingCooling" && (
                                        <div
                                            className="xw-fade"
                                            style={{
                                                display: "grid",
                                                gap: 18,
                                            }}
                                        >
                                            <div>
                                                {groupLabel(
                                                    "What's the issue?"
                                                )}
                                                <div className="xw-chips">
                                                    {HVAC_ISSUES.map((o) =>
                                                        chip(
                                                            data.hvacIssue ===
                                                                o,
                                                            o,
                                                            () =>
                                                                toggle(
                                                                    "hvacIssue",
                                                                    o
                                                                )
                                                        )
                                                    )}
                                                </div>
                                            </div>
                                            <div>
                                                {groupLabel(
                                                    "How long has it been happening?",
                                                    true
                                                )}
                                                <div className="xw-chips">
                                                    {HVAC_DURATIONS.map((o) =>
                                                        chip(
                                                            data.hvacDuration ===
                                                                o,
                                                            o,
                                                            () =>
                                                                toggle(
                                                                    "hvacDuration",
                                                                    o
                                                                )
                                                        )
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    {data.service &&
                                        data.service !== "heatingCooling" && (
                                            <div
                                                className="xw-fade"
                                                style={{
                                                    display: "grid",
                                                    gap: 18,
                                                }}
                                            >
                                                <div>
                                                    {groupLabel(
                                                        "What do you need?"
                                                    )}
                                                    <div className="xw-chips">
                                                        {SERVICE_OPTIONS[
                                                            data.service
                                                        ].map((o) =>
                                                            chip(
                                                                data.detail ===
                                                                    o,
                                                                o,
                                                                () =>
                                                                    patch({
                                                                        detail:
                                                                            data.detail ===
                                                                            o
                                                                                ? undefined
                                                                                : o,
                                                                        answers:
                                                                            {},
                                                                    })
                                                            )
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                    {stepComplete[0] && (
                                        <div className="xw-micro">
                                            That's everything we need to route
                                            the right technician. Next: pick
                                            your time.
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ============ STEP 2: TIME ============ */}
                            {step === 1 && (
                                <div
                                    className="xw-fade"
                                    style={{ display: "grid", gap: 20 }}
                                >
                                    {/* quick-pick strip */}
                                    {isMobile ? (
                                        (() => {
                                            const qp = quickPicks[0]
                                            const sel =
                                                data.apptDate === qp.iso &&
                                                data.apptSlot === qp.slot
                                            return (
                                                <button
                                                    className="xw-qpnext"
                                                    onClick={() =>
                                                        patch({
                                                            apptDate: qp.iso,
                                                            apptSlot: qp.slot,
                                                        })
                                                    }
                                                >
                                                    <span>
                                                        <span className="l1">
                                                            ⚡ Next available
                                                        </span>
                                                        <span className="l2">
                                                            {qp.label}
                                                        </span>
                                                    </span>
                                                    <span
                                                        className={
                                                            "pill" +
                                                            (sel
                                                                ? " on"
                                                                : "")
                                                        }
                                                    >
                                                        {sel
                                                            ? "✓ Selected"
                                                            : "Select"}
                                                    </span>
                                                </button>
                                            )
                                        })()
                                    ) : (
                                    <div className="xw-qp">
                                        <div className="qplabel">
                                            ⚡ Next available
                                        </div>
                                        <div className="qprow">
                                            {quickPicks.map((qp) => {
                                                const sel =
                                                    data.apptDate ===
                                                        qp.iso &&
                                                    data.apptSlot === qp.slot
                                                return (
                                                    <button
                                                        key={qp.label}
                                                        className={
                                                            "xw-qpchip" +
                                                            (sel
                                                                ? " sel"
                                                                : "")
                                                        }
                                                        onClick={() =>
                                                            patch({
                                                                apptDate:
                                                                    qp.iso,
                                                                apptSlot:
                                                                    qp.slot,
                                                            })
                                                        }
                                                    >
                                                        {sel
                                                            ? "✓ " + qp.label
                                                            : qp.label}
                                                    </button>
                                                )
                                            })}
                                        </div>
                                    </div>
                                    )}

                                    <div className="xw-timecols">
                                        {/* calendar */}
                                        <div>
                                            {groupLabel("Or pick a day")}
                                            {isMobile ? (
                                                <div className="xw-daystrip">
                                                    {upcomingWeekdays(10).map(
                                                        (iso) => {
                                                            const d =
                                                                fromISO(iso)
                                                            const sel =
                                                                data.apptDate ===
                                                                iso
                                                            return (
                                                                <button
                                                                    key={iso}
                                                                    className={
                                                                        "xw-stripday" +
                                                                        (sel
                                                                            ? " sel"
                                                                            : "")
                                                                    }
                                                                    onClick={() =>
                                                                        patch(
                                                                            {
                                                                                apptDate:
                                                                                    iso,
                                                                            }
                                                                        )
                                                                    }
                                                                >
                                                                    <span className="wd">
                                                                        {d.toLocaleDateString(
                                                                            "en-US",
                                                                            {
                                                                                weekday:
                                                                                    "short",
                                                                            }
                                                                        )}
                                                                    </span>
                                                                    <span className="dn">
                                                                        {d.getDate()}
                                                                    </span>
                                                                </button>
                                                            )
                                                        }
                                                    )}
                                                </div>
                                            ) : (
                                                <WizardCalendar
                                                    value={data.apptDate}
                                                    onSelect={(iso) =>
                                                        patch({
                                                            apptDate: iso,
                                                        })
                                                    }
                                                />
                                            )}
                                        </div>

                                        {/* windows */}
                                        <div>
                                            {groupLabel(
                                                data.apptDate
                                                    ? `Arrival window · ${fmtDay(
                                                          data.apptDate
                                                      )}`
                                                    : "Arrival window"
                                            )}
                                            <div
                                                style={{
                                                    display: "grid",
                                                    gap: 10,
                                                }}
                                            >
                                                {TIME_SLOTS.map((slot) => {
                                                    const sel =
                                                        data.apptSlot === slot
                                                    return (
                                                        <button
                                                            key={slot}
                                                            className={
                                                                "xw-window" +
                                                                (sel
                                                                    ? " sel"
                                                                    : "")
                                                            }
                                                            onClick={() =>
                                                                patch({
                                                                    apptSlot:
                                                                        slot,
                                                                })
                                                            }
                                                        >
                                                            <span>
                                                                {slot}
                                                            </span>
                                                            {sel && (
                                                                <span>✓</span>
                                                            )}
                                                        </button>
                                                    )
                                                })}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="xw-micro">
                                        Appointments are Monday–Friday. We'll
                                        confirm your exact arrival time by
                                        text.
                                    </div>
                                </div>
                            )}

                            {/* ============ STEP 3: DETAILS (skippable) ============ */}
                            {step === 2 && (
                                <div
                                    className="xw-fade"
                                    style={{ display: "grid", gap: 20 }}
                                >
                                    <div className="xw-proprow">
                                        <div>
                                            {groupLabel("Property")}
                                            <div className="xw-chips">
                                                {[
                                                    "Residential",
                                                    "Commercial",
                                                ].map((o) =>
                                                    chip(
                                                        data.propertyType ===
                                                            o,
                                                        o,
                                                        () =>
                                                            toggle(
                                                                "propertyType",
                                                                o
                                                            )
                                                    )
                                                )}
                                            </div>
                                        </div>
                                        <div>
                                            {groupLabel("You are the…")}
                                            <div className="xw-chips">
                                                {[
                                                    "Owner / Landlord",
                                                    "Tenant",
                                                ].map((o) =>
                                                    chip(
                                                        data.occupant === o,
                                                        o,
                                                        () =>
                                                            toggle(
                                                                "occupant",
                                                                o
                                                            )
                                                    )
                                                )}
                                            </div>
                                        </div>
                                    </div>

                                    {isHvacContext(
                                        data.service,
                                        data.detail
                                    ) && (
                                        <div>
                                            {groupLabel(
                                                "Approximate age of system — skip if unsure"
                                            )}
                                            <div className="xw-chips">
                                                {AGE_OPTIONS.map((o) =>
                                                    chip(
                                                        data.systemAge === o,
                                                        o,
                                                        () =>
                                                            toggle(
                                                                "systemAge",
                                                                o
                                                            )
                                                    )
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {isHvacContext(
                                        data.service,
                                        data.detail
                                    ) &&
                                        data.service !== "xplan" && (
                                            <div>
                                                {groupLabel(
                                                    "Where is the unit?",
                                                    true
                                                )}
                                                <div className="xw-chips">
                                                    {UNIT_LOCATIONS.map((o) =>
                                                        chip(
                                                            data.unitLocation ===
                                                                o,
                                                            o,
                                                            () =>
                                                                toggle(
                                                                    "unitLocation",
                                                                    o
                                                                )
                                                        )
                                                    )}
                                                </div>
                                            </div>
                                        )}

                                    {/* Service-specific follow-up — one per service, optional */}
                                    {data.service !== "heatingCooling" &&
                                        getSubQuestions(data.detail).map(
                                            (q) => (
                                                <div key={q.id}>
                                                    {groupLabel(q.label, true)}
                                                    <div className="xw-chips">
                                                        {q.options.map((o) =>
                                                            chip(
                                                                data.answers?.[
                                                                    q.id
                                                                ] === o,
                                                                o,
                                                                () =>
                                                                    toggleAnswer(
                                                                        q.id,
                                                                        o
                                                                    )
                                                            )
                                                        )}
                                                    </div>
                                                </div>
                                            )
                                        )}

                                    {/* note & photos */}
                                    {!noteOpen ? (
                                        <button
                                            className="xw-noterow"
                                            onClick={() => setNoteOpen(true)}
                                        >
                                            <span className="plus">+</span>
                                            <span>
                                                <span className="nt">
                                                    Add a note or photos
                                                    (optional)
                                                </span>
                                                <span className="ns">
                                                    Anything that helps the
                                                    tech arrive prepared — up
                                                    to 5 photos
                                                </span>
                                            </span>
                                        </button>
                                    ) : (
                                        <div
                                            className="xw-fade"
                                            style={{
                                                display: "grid",
                                                gap: 10,
                                            }}
                                        >
                                            <textarea
                                                className="xw-input"
                                                rows={3}
                                                placeholder="Briefly describe the issue or request…"
                                                value={note}
                                                onChange={(e) =>
                                                    setNote(
                                                        e.currentTarget.value
                                                    )
                                                }
                                                style={{
                                                    resize: "vertical",
                                                }}
                                                onKeyDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                                onPointerDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                            />
                                            <button
                                                className="xw-upload"
                                                onClick={() =>
                                                    photoInputRef.current?.click()
                                                }
                                            >
                                                Upload photos · up to 5, 10MB
                                                each
                                            </button>
                                            <input
                                                ref={photoInputRef}
                                                type="file"
                                                accept="image/*"
                                                multiple
                                                style={{ display: "none" }}
                                                onChange={(e) => {
                                                    const MAX_FILES = 5
                                                    const MAX_MB = 10
                                                    const picked = Array.from(
                                                        e.currentTarget
                                                            .files || []
                                                    )
                                                    const fresh =
                                                        picked.filter(
                                                            (f) =>
                                                                f.size <=
                                                                MAX_MB *
                                                                    1024 *
                                                                    1024
                                                        )
                                                    setPhotos((prev) => {
                                                        const merged = [
                                                            ...prev,
                                                            ...fresh,
                                                        ].reduce<File[]>(
                                                            (acc, f) => {
                                                                const key = `${f.name}_${f.size}_${f.lastModified}`
                                                                if (
                                                                    !acc.some(
                                                                        (
                                                                            x
                                                                        ) =>
                                                                            `${x.name}_${x.size}_${x.lastModified}` ===
                                                                            key
                                                                    )
                                                                ) {
                                                                    acc.push(
                                                                        f
                                                                    )
                                                                }
                                                                return acc
                                                            },
                                                            []
                                                        )
                                                        return merged.slice(
                                                            0,
                                                            MAX_FILES
                                                        )
                                                    })
                                                    if (
                                                        photoInputRef.current
                                                    )
                                                        photoInputRef.current.value =
                                                            ""
                                                }}
                                            />
                                            {!!photos.length && (
                                                <div
                                                    style={{
                                                        display: "flex",
                                                        flexWrap: "wrap",
                                                        gap: 8,
                                                    }}
                                                >
                                                    {photoPreviews.map(
                                                        (p, i) => (
                                                            <div
                                                                key={i}
                                                                className="xw-thumb"
                                                            >
                                                                <img
                                                                    src={
                                                                        p.url
                                                                    }
                                                                    alt={`upload ${
                                                                        i + 1
                                                                    }`}
                                                                />
                                                                <button
                                                                    onClick={() =>
                                                                        setPhotos(
                                                                            (
                                                                                prev
                                                                            ) =>
                                                                                prev.filter(
                                                                                    (
                                                                                        _,
                                                                                        idx
                                                                                    ) =>
                                                                                        idx !==
                                                                                        i
                                                                                )
                                                                        )
                                                                    }
                                                                >
                                                                    ×
                                                                </button>
                                                            </div>
                                                        )
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ============ STEP 4: CONFIRM ============ */}
                            {step === 3 && (
                                <div className="xw-fade xw-confcols">
                                    {/* form */}
                                    <div
                                        className="xw-c-form"
                                        style={{ display: "grid", gap: 12 }}
                                    >
                                        {groupLabel("Your details")}
                                        <div className="xw-namerow">
                                            <input
                                                className="xw-input"
                                                placeholder="First name"
                                                value={firstName}
                                                onChange={(e) =>
                                                    setFirstName(
                                                        e.currentTarget.value
                                                    )
                                                }
                                                onKeyDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                                onPointerDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                            />
                                            <input
                                                className="xw-input"
                                                placeholder="Last name"
                                                value={lastName}
                                                onChange={(e) =>
                                                    setLastName(
                                                        e.currentTarget.value
                                                    )
                                                }
                                                onKeyDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                                onPointerDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                            />
                                        </div>
                                        <input
                                            className="xw-input"
                                            placeholder="Mobile — we text your confirmation here"
                                            inputMode="numeric"
                                            pattern="[0-9]*"
                                            value={formatPhone(phoneDigits)}
                                            onChange={(e) => {
                                                const only =
                                                    e.currentTarget.value
                                                        .replace(/\D/g, "")
                                                        .slice(0, 10)
                                                setPhoneDigits(only)
                                            }}
                                            onKeyDownCapture={(e) =>
                                                e.stopPropagation()
                                            }
                                            onPointerDownCapture={(e) =>
                                                e.stopPropagation()
                                            }
                                        />
                                        {/* SMS consent. Sits DIRECTLY beneath the
                                            mobile field, which is where a reviewer
                                            looks for it and where it is legible as
                                            applying to that number. Unchecked by
                                            default and never gates submission. */}
                                        <div className="xw-sms">
                                            <button
                                                type="button"
                                                className="xw-sms-btn"
                                                role="checkbox"
                                                aria-checked={smsOk}
                                                aria-describedby="xw-sms-copy"
                                                onClick={() =>
                                                    setSmsOk((v) => !v)
                                                }
                                            >
                                                <span
                                                    className={
                                                        "box" +
                                                        (smsOk ? " on" : "")
                                                    }
                                                    aria-hidden="true"
                                                >
                                                    {smsOk ? "\u2713" : ""}
                                                </span>
                                            </button>
                                            <label
                                                id="xw-sms-copy"
                                                className="xw-sms-copy"
                                                onClick={() =>
                                                    setSmsOk((v) => !v)
                                                }
                                            >
                                                Yes, text me about my service
                                                request at the number above.
                                                Consent is not a condition of
                                                purchase. Msg &amp; data rates
                                                may apply, message frequency
                                                varies. Reply HELP for help or
                                                STOP to opt out. See our{" "}
                                                <a
                                                    href="https://www.extremeheating.com/privacy"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    onClick={(e) =>
                                                        e.stopPropagation()
                                                    }
                                                >
                                                    Privacy Policy
                                                </a>{" "}
                                                and{" "}
                                                <a
                                                    href="https://www.extremeheating.com/terms"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    onClick={(e) =>
                                                        e.stopPropagation()
                                                    }
                                                >
                                                    Terms
                                                </a>
                                                .
                                            </label>
                                        </div>
                                        <input
                                            className="xw-input"
                                            type="email"
                                            placeholder="Email (optional)"
                                            value={email}
                                            onChange={(e) =>
                                                setEmail(
                                                    e.currentTarget.value
                                                )
                                            }
                                            onKeyDownCapture={(e) =>
                                                e.stopPropagation()
                                            }
                                            onPointerDownCapture={(e) =>
                                                e.stopPropagation()
                                            }
                                        />
                                        <div
                                            style={{ position: "relative" }}
                                        >
                                            <input
                                                className="xw-input"
                                                placeholder="Service address"
                                                value={address}
                                                autoComplete="off"
                                                onChange={(e) =>
                                                    onAddressChange(
                                                        e.currentTarget.value
                                                    )
                                                }
                                                onFocus={() => {
                                                    if (
                                                        addrSuggestions.length
                                                    )
                                                        setAddrOpen(true)
                                                }}
                                                onBlur={() =>
                                                    setTimeout(
                                                        () =>
                                                            setAddrOpen(
                                                                false
                                                            ),
                                                        150
                                                    )
                                                }
                                                onKeyDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                                onPointerDownCapture={(e) =>
                                                    e.stopPropagation()
                                                }
                                            />
                                            {addrOpen &&
                                                (addrLoading ||
                                                    addrSuggestions.length >
                                                        0) && (
                                                    <div className="xw-addrdrop">
                                                        {addrLoading && (
                                                            <div className="ld">
                                                                Searching
                                                                addresses…
                                                            </div>
                                                        )}
                                                        {addrSuggestions.map(
                                                            (s) => (
                                                                <div
                                                                    key={s.id}
                                                                    className="it"
                                                                    onMouseDown={(
                                                                        e
                                                                    ) => {
                                                                        e.preventDefault()
                                                                        selectAddress(
                                                                            s
                                                                        )
                                                                    }}
                                                                >
                                                                    {s.label}
                                                                </div>
                                                            )
                                                        )}
                                                    </div>
                                                )}
                                        </div>

                                        <div>
                                            {groupLabel("Reach me by")}
                                            <div className="xw-chips">
                                                {(
                                                    [
                                                        "Call",
                                                        "Text",
                                                        "Email",
                                                    ] as const
                                                ).map((m) =>
                                                    chip(
                                                        data.preferredContact ===
                                                            m,
                                                        m,
                                                        () =>
                                                            patch({
                                                                preferredContact:
                                                                    m,
                                                            })
                                                    )
                                                )}
                                            </div>
                                        </div>
                                    </div>

                                    {/* summary + fee */}
                                        <div className="xw-summary xw-c-summary">
                                            <div className="sh">
                                                Your visit
                                            </div>
                                            {svcSummary && (
                                                <div className="row">
                                                    <span>Service</span>
                                                    <b>{svcSummary}</b>
                                                </div>
                                            )}
                                            {whenSummary && (
                                                <div className="row">
                                                    <span>When</span>
                                                    <b>{whenSummary}</b>
                                                </div>
                                            )}
                                            {homeSummary && (
                                                <div className="row">
                                                    <span>Home</span>
                                                    <b>{homeSummary}</b>
                                                </div>
                                            )}
                                            <div className="links">
                                                <button
                                                    onClick={() =>
                                                        setStep(0)
                                                    }
                                                >
                                                    Edit service ›
                                                </button>
                                                <button
                                                    onClick={() =>
                                                        setStep(1)
                                                    }
                                                >
                                                    Edit time ›
                                                </button>
                                            </div>
                                        </div>

                                        {feeRequired ? (
                                            <div className="xw-fee xw-c-fee">
                                                <div className="fh">
                                                    <span className="amt">
                                                        {DISPATCH_FEE}
                                                    </span>
                                                    <span className="lbl">
                                                        dispatch & diagnostic
                                                    </span>
                                                </div>
                                                <div className="fb">
                                                    {feeCopy(
                                                        data.service,
                                                        isMobile
                                                    )}
                                                </div>
                                                <button
                                                    className="fack"
                                                    onClick={() =>
                                                        setFeeOk((v) => !v)
                                                    }
                                                >
                                                    <span
                                                        className={
                                                            "box" +
                                                            (feeOk
                                                                ? " on"
                                                                : "")
                                                        }
                                                    >
                                                        {feeOk ? "✓" : ""}
                                                    </span>
                                                    Sounds good
                                                </button>
                                            </div>
                                        ) : (
                                            <div className="xw-fee xw-c-fee xw-free">
                                                <div className="fh">
                                                    <span className="amt">
                                                        Free
                                                    </span>
                                                    <span className="lbl">
                                                        estimate visit
                                                    </span>
                                                </div>
                                                <div className="fb">
                                                    {isMobile
                                                        ? "No charge for this visit — no obligation."
                                                        : "There's no charge for this visit — we'll assess your home and give you an up-front quote with no obligation."}
                                                </div>
                                            </div>
                                        )}
                                </div>
                            )}
                        </>
                    )}
                </div>

                {/* ---------- FOOTER ---------- */}
                {!booked && (
                    <div className="xw-footer">
                        {step > 0 ? (
                            <button className="xw-back" onClick={goBack}>
                                ‹ Back
                            </button>
                        ) : (
                            <span />
                        )}
                        <div className="xw-footright">
                            {hints[step] && (
                                <span className="xw-hint">{hints[step]}</span>
                            )}
                            {step === 3 ? (
                                <button
                                    className="xw-cta book"
                                    disabled={!canContinue || submitting}
                                    onClick={bookVisit}
                                >
                                    {submitting ? (
                                        <span className="xw-spin" />
                                    ) : (
                                        "Book my visit →"
                                    )}
                                </button>
                            ) : (
                                <button
                                    className="xw-cta"
                                    disabled={!canContinue}
                                    onClick={goNext}
                                >
                                    Continue
                                </button>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

/* ---------- Desktop calendar (Mon–Fri, per handoff spec) ---------- */
function WizardCalendar({
    value,
    onSelect,
}: {
    value?: string
    onSelect: (iso: string) => void
}) {
    const today = React.useMemo(startOfToday, [])
    const minSelectable = React.useMemo(() => {
        const d = new Date(today)
        d.setDate(d.getDate() + 1)
        return d
    }, [today])
    const curIdx = today.getFullYear() * 12 + today.getMonth()
    const maxIdx = curIdx + 2

    const [view, setView] = React.useState({
        y: today.getFullYear(),
        m: today.getMonth(),
    })
    const viewIdx = view.y * 12 + view.m
    const canPrev = viewIdx > curIdx
    const canNext = viewIdx < maxIdx

    const weeks = React.useMemo(() => {
        const daysInMonth = new Date(view.y, view.m + 1, 0).getDate()
        const rows: (Date | null)[][] = []
        let week: (Date | null)[] = [null, null, null, null, null]
        for (let day = 1; day <= daysInMonth; day++) {
            const d = new Date(view.y, view.m, day)
            const dow = d.getDay()
            if (dow === 0 || dow === 6) continue
            week[dow - 1] = d
            if (dow === 5) {
                rows.push(week)
                week = [null, null, null, null, null]
            }
        }
        if (week.some(Boolean)) rows.push(week)
        return rows
    }, [view])

    const monthLabel = new Date(view.y, view.m, 1).toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
    })

    const shift = (delta: number) =>
        setView((v) => {
            const i = v.y * 12 + v.m + delta
            return { y: Math.floor(i / 12), m: ((i % 12) + 12) % 12 }
        })

    return (
        <div className="xw-cal">
            <div className="ch">
                <button
                    className="nav"
                    disabled={!canPrev}
                    onClick={() => canPrev && shift(-1)}
                    aria-label="Previous month"
                >
                    ‹
                </button>
                <div className="mo">{monthLabel}</div>
                <button
                    className="nav"
                    disabled={!canNext}
                    onClick={() => canNext && shift(1)}
                    aria-label="Next month"
                >
                    ›
                </button>
            </div>
            <div className="wk">
                {["Mon", "Tue", "Wed", "Thu", "Fri"].map((d) => (
                    <div key={d}>{d}</div>
                ))}
            </div>
            <div style={{ display: "grid", gap: 4 }}>
                {weeks.map((week, wi) => (
                    <div key={wi} className="row5">
                        {week.map((d, ci) => {
                            if (!d) return <div key={ci} />
                            const iso = toISO(d)
                            const selectable =
                                d.getTime() >= minSelectable.getTime()
                            const sel = iso === value
                            return (
                                <button
                                    key={ci}
                                    className={
                                        "day" +
                                        (sel ? " sel" : "") +
                                        (!selectable ? " off" : "")
                                    }
                                    disabled={!selectable}
                                    onClick={() => onSelect(iso)}
                                >
                                    {d.getDate()}
                                </button>
                            )
                        })}
                    </div>
                ))}
            </div>
        </div>
    )
}

/* ---------- Styles (design tokens per handoff) ---------- */
const XW_CSS = `
.xw-root, .xw-root *{ box-sizing:border-box; font-family:${FONT} }

.xw-modal{
  position:relative; margin:40px auto; width:960px; max-width:calc(100vw - 24px);
  max-height:calc(100vh - 80px); background:#fff; border-radius:20px; overflow:hidden;
  box-shadow:0 24px 80px rgba(0,0,0,.45); display:flex; flex-direction:column;
  transition:opacity 220ms cubic-bezier(.2,.8,.2,1), transform 300ms cubic-bezier(.2,.8,.2,1);
}

/* header */
.xw-header{ background:linear-gradient(180deg, ${T.headerGradA}, ${T.headerGradB}); padding:22px 28px 18px; flex-shrink:0 }
.xw-headtop{ display:flex; align-items:flex-start; justify-content:space-between; gap:14px }
.xw-eyebrow{ font:600 10.5px ${FONT}; letter-spacing:.22em; text-transform:uppercase; color:${T.eyebrow} }
.xw-title{ font:600 25px/1.2 ${FONT}; color:#fff; margin-top:3px }
.xw-headright{ display:flex; align-items:center; gap:10px; flex-shrink:0 }
.xw-emergency{
  display:inline-flex; align-items:center; gap:7px; background:#fff; border-radius:999px;
  padding:7px 14px; font:600 12px ${FONT}; color:${T.red}; text-decoration:none; white-space:nowrap;
}
.xw-emergency .dot{ width:8px; height:8px; border-radius:999px; background:${T.red} }
.xw-close{
  width:32px; height:32px; border-radius:999px; border:none; background:rgba(255,255,255,.14);
  color:#fff; cursor:pointer; display:grid; place-items:center; font-size:14px;
}
.xw-progress{ display:flex; gap:10px; margin-top:16px }
.xw-seg{ flex:1 }
.xw-seg.click{ cursor:pointer }
.xw-seg .bar{ height:4px; border-radius:2px; transition:background 200ms ease }
.xw-seg .lab{ margin-top:7px; font:600 10px ${FONT}; letter-spacing:.14em; text-align:center }
.xw-stepcount{ margin-left:6px; flex:none; font:600 10.5px ${FONT}; color:rgba(255,255,255,.7); white-space:nowrap }

/* mobile in-body emergency pill (mockups 1c) */
.xw-mpillwrap{ display:flex; justify-content:center; margin-bottom:14px }
.xw-mpill{
  display:inline-flex; align-items:center; gap:6px; background:#FDF1F0; border-radius:999px;
  padding:6px 13px; font:600 11px ${FONT}; color:${T.red}; text-decoration:none;
}
.xw-mpill .dot{ width:7px; height:7px; border-radius:50%; background:${T.red} }

/* mobile single next-available card (mockups 1c) */
.xw-qpnext{
  width:100%; display:flex; align-items:center; justify-content:space-between; gap:10px;
  border:1px solid ${T.qpCard}; background:${T.tint}; border-radius:12px; padding:12px 14px;
  cursor:pointer; text-align:left;
}
.xw-qpnext .l1{ display:block; font:600 11px ${FONT}; letter-spacing:.04em; text-transform:uppercase; color:${T.chipGreen} }
.xw-qpnext .l2{ display:block; font:600 13.5px ${FONT}; color:${T.ink}; margin-top:2px }
.xw-qpnext .pill{
  flex:none; background:#fff; border:1px solid ${T.qpBorder}; border-radius:999px;
  padding:7px 14px; font:600 12px ${FONT}; color:${T.ink};
}
.xw-qpnext .pill.on{ border:2px solid ${T.selGreen}; padding:6px 13px; color:${T.chipGreen} }

/* body */
.xw-body{ padding:26px 28px 24px; overflow:auto; -webkit-overflow-scrolling:touch; overscroll-behavior:contain; flex:1 1 auto; min-height:0 }
.xw-glabel{ font:600 14px ${FONT}; color:${T.ink}; margin-bottom:10px }
.xw-glabel .opt{ font-weight:500; color:${T.muted} }
.xw-micro{ font:400 12px ${FONT}; color:${T.muted} }
.xw-chips{ display:flex; flex-wrap:wrap; gap:9px }

/* chips */
.xw-chip{
  border:1px solid ${T.border}; border-radius:999px; padding:9px 18px;
  font:500 13px ${FONT}; color:${T.ink}; background:#fff; cursor:pointer;
  transition:border-color .12s ease, background .12s ease;
}
.xw-chip:hover{ border-color:${T.dashed} }
.xw-chip.sel{ border:2px solid ${T.selGreen}; background:${T.tint}; padding:8px 17px; font-weight:600; color:${T.chipGreen} }

/* service cards */
.xw-svcrow{ display:flex; gap:12px }
.xw-svc{
  flex:1; border:1px solid ${T.border}; border-radius:14px; padding:19px 16px; background:#fff;
  display:grid; justify-items:center; gap:8px; cursor:pointer; text-align:center;
  transition:border-color .12s ease, background .12s ease;
}
.xw-svc:hover{ border-color:${T.dashed} }
.xw-svc.sel{ border:2px solid ${T.selGreen}; background:${T.tint}; padding:18px 15px }
.xw-svc .tile{ width:44px; height:44px; border-radius:12px; background:${T.surface}; display:grid; place-items:center }
.xw-svc .nm{ font:600 14.5px ${FONT}; color:${T.ink} }
.xw-svc .sb{ font:400 11.5px ${FONT}; color:${T.muted} }

/* quick picks */
.xw-qp{ border:1px solid ${T.qpCard}; background:${T.tint}; border-radius:14px; padding:16px 18px }
.xw-qp .qplabel{ font:600 13px ${FONT}; color:${T.chipGreen}; margin-bottom:10px }
.xw-qp .qprow{ display:flex; flex-wrap:wrap; gap:9px }
.xw-qpchip{
  background:#fff; border:1px solid ${T.qpBorder}; border-radius:999px; padding:9px 18px;
  font:500 13px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-qpchip.sel{ border:2px solid ${T.selGreen}; padding:8px 17px; font-weight:600; color:${T.chipGreen} }

/* time layout */
.xw-timecols{ display:grid; grid-template-columns:1.15fr 1fr; gap:28px; align-items:start }

/* calendar */
.xw-cal{ border:1px solid ${T.border}; border-radius:14px; padding:14px }
.xw-cal .ch{ display:flex; align-items:center; justify-content:space-between; margin-bottom:10px }
.xw-cal .mo{ font:600 14px ${FONT}; color:${T.ink} }
.xw-cal .nav{
  width:28px; height:28px; border-radius:999px; border:1px solid ${T.border}; background:#fff;
  color:${T.deepPurple}; cursor:pointer; display:grid; place-items:center; font-size:15px; line-height:1;
}
.xw-cal .nav:disabled{ opacity:.35; cursor:default }
.xw-cal .wk{ display:grid; grid-template-columns:repeat(5,1fr); margin-bottom:6px }
.xw-cal .wk div{ text-align:center; font:600 10.5px ${FONT}; letter-spacing:.1em; color:${T.muted}; text-transform:uppercase }
.xw-cal .row5{ display:grid; grid-template-columns:repeat(5,1fr); gap:4px }
.xw-cal .day{
  border:none; background:transparent; padding:9px 0; text-align:center; border-radius:10px;
  font:500 13px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-cal .day:hover:not(:disabled){ background:${T.surface} }
.xw-cal .day.off{ color:${T.disabledDay}; cursor:default }
.xw-cal .day.sel{ background:${T.deepPurple}; color:#fff; font-weight:600 }

/* mobile day strip (mockups 1c: 5 equal cells, selected = deep purple) */
.xw-daystrip{ display:flex; gap:7px; overflow-x:auto; padding-bottom:6px; -webkit-overflow-scrolling:touch }
.xw-stripday{
  flex:0 0 calc(20% - 5.6px); border:1px solid ${T.border}; border-radius:12px; background:#fff;
  padding:9px 4px; display:grid; justify-items:center; gap:2px; cursor:pointer;
}
.xw-stripday .wd{ font:600 9.5px ${FONT}; letter-spacing:.06em; text-transform:uppercase; color:${T.muted} }
.xw-stripday .dn{ font:600 14px ${FONT}; color:${T.ink} }
.xw-stripday.sel{ border:2px solid ${T.deepPurple}; background:${T.deepPurple}; padding:8px 3px }
.xw-stripday.sel .wd{ color:rgba(255,255,255,.7) }
.xw-stripday.sel .dn{ color:#fff }

/* arrival windows */
.xw-window{
  width:100%; display:flex; align-items:center; justify-content:space-between;
  border:1px solid ${T.border}; border-radius:12px; padding:13px 16px; background:#fff;
  font:500 13.5px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-window:hover{ border-color:${T.dashed} }
.xw-window.sel{ border:2px solid ${T.selGreen}; background:${T.tint}; padding:12px 15px; font-weight:600; color:${T.chipGreen} }

/* step 3 */
.xw-proprow{ display:grid; grid-template-columns:auto auto; gap:36px; justify-content:start }
.xw-noterow{
  width:100%; display:flex; align-items:center; gap:12px; text-align:left;
  border:1.5px dashed ${T.dashed}; border-radius:12px; padding:14px 18px; background:#fff; cursor:pointer;
}
.xw-noterow .plus{ width:30px; height:30px; border-radius:999px; background:${T.surface}; display:grid; place-items:center; font:600 16px ${FONT}; color:${T.deepPurple}; flex-shrink:0 }
.xw-noterow .nt{ display:block; font:600 13px ${FONT}; color:${T.deepPurple} }
.xw-noterow .ns{ display:block; font:400 11.5px ${FONT}; color:${T.muted}; margin-top:2px }
.xw-upload{
  border:1.5px dashed ${T.dashed}; border-radius:12px; padding:12px 16px; background:#fff;
  font:600 12.5px ${FONT}; color:${T.deepPurple}; cursor:pointer;
}
.xw-thumb{ position:relative; width:84px; height:84px; border-radius:10px; overflow:hidden; border:1px solid ${T.border} }
.xw-thumb img{ width:100%; height:100%; object-fit:cover; display:block }
.xw-thumb button{
  position:absolute; top:3px; right:3px; width:20px; height:20px; border:none; border-radius:999px;
  background:rgba(255,255,255,.92); color:${T.deepPurple}; font-weight:700; cursor:pointer; line-height:1;
}

/* inputs */
.xw-input{
  width:100%; border:1px solid ${T.border}; border-radius:11px; padding:13px 15px;
  font:400 13px ${FONT}; color:${T.ink}; background:#fff;
}
.xw-input::placeholder{ color:${T.placeholder} }
.xw-input:focus{ outline:2px solid ${T.selGreen}; outline-offset:0; border-color:transparent }

/* step 4 */
.xw-confcols{
  display:grid; grid-template-columns:1.3fr 1fr; gap:26px; align-items:start;
  grid-template-areas:"form summary" "form fee";
}
.xw-c-form{ grid-area:form }
.xw-c-summary{ grid-area:summary }
.xw-c-fee{ grid-area:fee; align-self:start }
.xw-namerow{ display:grid; grid-template-columns:1fr 1fr; gap:10px }
.xw-addrdrop{
  position:absolute; top:calc(100% + 4px); left:0; right:0; z-index:20; background:#fff;
  border:1px solid ${T.border}; border-radius:11px; box-shadow:0 14px 34px rgba(37,21,54,.18);
  overflow:hidden; max-height:240px; overflow-y:auto;
}
.xw-addrdrop .ld{ padding:10px 12px; font:400 12.5px ${FONT}; color:${T.muted} }
.xw-addrdrop .it{ padding:10px 12px; font:400 13px ${FONT}; color:${T.ink}; cursor:pointer; border-bottom:1px solid ${T.hairline} }
.xw-addrdrop .it:hover{ background:${T.surface} }

.xw-summary{ background:${T.surface2}; border-radius:14px; padding:18px 20px }
.xw-summary .sh{ font:600 14px ${FONT}; color:${T.ink}; margin-bottom:10px }
.xw-summary .row{ display:flex; justify-content:space-between; gap:14px; padding:5px 0 }
.xw-summary .row span{ font:400 12.5px ${FONT}; color:${T.muted} }
.xw-summary .row b{ font:600 12.5px ${FONT}; color:${T.ink}; text-align:right }
.xw-summary .links{ display:flex; gap:14px; margin-top:10px }
.xw-summary .links button{ border:none; background:none; padding:0; font:600 11.5px ${FONT}; color:${T.linkGreen}; cursor:pointer }

.xw-fee{ background:#fff; border:1px solid ${T.border}; border-radius:14px; padding:16px 20px }
.xw-fee .fh{ display:flex; align-items:baseline; gap:8px }
.xw-fee .amt{ font:700 21px ${FONT}; color:${T.ink} }
.xw-fee .lbl{ font:600 12.5px ${FONT}; color:${T.ink} }
.xw-fee .fb{ font:400 11.5px/1.6 ${FONT}; color:${T.muted}; margin-top:6px }
.xw-fee .fack{
  display:flex; align-items:center; gap:9px; margin-top:12px; border:none; background:none;
  padding:0; font:500 12px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-fee .box{
  width:20px; height:20px; border-radius:6px; border:2px solid ${T.dashed}; display:grid;
  place-items:center; color:#fff; font-size:12px; flex-shrink:0;
}
.xw-fee .box.on{ background:${T.selGreen}; border-color:${T.selGreen} }
.xw-fee.xw-free{ border:1px solid ${T.qpCard}; background:${T.tint} }
.xw-fee.xw-free .amt{ color:${T.chipGreen} }

/* SMS consent. Reuses the fee checkbox's box geometry so the two read as the same
   control, but the copy is legal text rather than a label: smaller, muted, and
   allowed to wrap to several lines. The whole label toggles, which is what people
   expect from a checkbox, while the two links stopPropagation so tapping Privacy
   Policy opens it instead of silently ticking the box. */
.xw-sms{ display:flex; align-items:flex-start; gap:9px; margin-top:10px }
.xw-sms-btn{
  border:none; background:none; padding:0; margin:0; cursor:pointer; flex-shrink:0;
  line-height:0; margin-top:1px;
}
.xw-sms .box{
  width:20px; height:20px; border-radius:6px; border:2px solid ${T.dashed}; display:grid;
  place-items:center; color:#fff; font-size:12px; flex-shrink:0;
}
.xw-sms .box.on{ background:${T.selGreen}; border-color:${T.selGreen} }
.xw-sms-btn:focus-visible .box{ outline:2px solid ${T.deepPurple}; outline-offset:2px }
.xw-sms-copy{
  font:400 11.5px/1.5 ${FONT}; color:${T.muted}; cursor:pointer; margin:0;
}
.xw-sms-copy a{ color:${T.linkGreen}; text-decoration:underline }

/* footer */
.xw-footer{
  border-top:1px solid ${T.hairline}; padding:16px 28px; display:flex; align-items:center;
  justify-content:space-between; gap:12px; background:#fff; flex-shrink:0;
}
.xw-back{ border:none; background:none; padding:6px 4px; font:600 13.5px ${FONT}; color:${T.muted}; cursor:pointer }
.xw-footright{ display:flex; align-items:center; gap:14px }
.xw-hint{ font:500 12.5px ${FONT}; color:${T.muted} }
.xw-cta{
  border:none; border-radius:999px; padding:13px 30px; font:600 14.5px ${FONT}; color:#fff;
  background:linear-gradient(135deg, ${T.btnGradA}, ${T.btnGradB}); cursor:pointer;
  transition:filter .15s ease;
}
.xw-cta.book{ padding:14px 34px }
.xw-cta:hover:not(:disabled){ filter:brightness(1.05) }
.xw-cta:disabled{ background:${T.btnDisabled}; color:${T.btnDisabledText}; cursor:default }
.xw-outline{
  border:1.5px solid ${T.deepPurple}; border-radius:999px; padding:12px 26px; background:#fff;
  font:600 14px ${FONT}; color:${T.deepPurple}; cursor:pointer;
}
.xw-spin{
  display:inline-block; width:16px; height:16px; border-radius:50%;
  border:2px solid rgba(255,255,255,.45); border-top-color:#fff;
  animation:xwspin 800ms linear infinite; vertical-align:middle;
}

/* done */
.xw-done{ text-align:center; padding:26px 10px 12px; display:grid; justify-items:center; gap:10px }
.xw-donecheck{
  width:64px; height:64px; border-radius:999px; background:${T.tint}; border:2px solid ${T.selGreen};
  display:grid; place-items:center; font-size:26px; color:${T.chipGreen};
}
.xw-doneh{ font:600 22px ${FONT}; color:${T.ink} }
.xw-donesub{ font:400 13.5px ${FONT}; color:${T.muted} }
.xw-donebtns{ display:flex; gap:12px; margin-top:8px; flex-wrap:wrap; justify-content:center }
.xw-donefoot{ font:400 12.5px ${FONT}; color:${T.muted}; margin-top:6px }

@keyframes xwspin{ to{ transform:rotate(360deg) } }
@keyframes xwfade{ from{ opacity:0; transform:translateY(6px) } to{ opacity:1; transform:none } }
.xw-fade{ animation:xwfade .18s ease both }

/* ---- Mobile (mockups 1c, 390px) ---- */
@media (max-width: 809px){
  .xw-modal{ margin:12px auto; max-width:calc(100vw - 16px); max-height:calc(100dvh - 24px); border-radius:20px }

  /* compact header: eyebrow + close on one row, title, thin segments + "1 of 4" */
  .xw-header{ padding:18px 20px 16px }
  .xw-eyebrow{ font-size:9.5px; letter-spacing:.2em }
  .xw-title{ font-size:21px; margin-top:4px }
  .xw-close{ width:28px; height:28px; font-size:13px }
  .xw-progress{ gap:6px; margin-top:14px; align-items:center }

  .xw-body{ padding:18px 20px 20px }

  /* 2×2 service cards, smaller tiles, no subtitles */
  .xw-svcrow{ display:grid; grid-template-columns:1fr 1fr; gap:10px }
  .xw-svc{ padding:15px 12px }
  .xw-svc.sel{ padding:14px 11px }
  .xw-svc .tile{ width:38px; height:38px; border-radius:11px }
  .xw-svc.sel .tile{ background:#fff; border:1px solid ${T.qpCard} }
  .xw-svc .nm{ font-size:13px }
  .xw-svc .sb{ display:none }

  /* chips */
  .xw-chip{ padding:10px 15px; font-size:12.5px }
  .xw-chip.sel{ padding:9px 14px; font-size:12.5px }
  .xw-glabel{ font-size:13.5px }

  /* time step stacks; windows tighten */
  .xw-timecols{ grid-template-columns:1fr; gap:16px }
  .xw-window{ padding:13px 15px; font-size:13px }
  .xw-window.sel{ padding:12px 14px }

  /* step 3 */
  .xw-proprow{ grid-template-columns:1fr; gap:16px }

  /* confirm: summary → form → fee (name fields stay side-by-side) */
  .xw-confcols{ grid-template-columns:1fr; grid-template-areas:"summary" "form" "fee"; gap:14px }
  .xw-namerow{ gap:9px }
  .xw-summary{ padding:14px 16px }
  .xw-summary .links{ margin-top:8px }
  .xw-fee{ padding:14px 16px }
  .xw-fee .amt{ font-size:19px }

  /* 16px inputs prevent iOS focus-zoom (deliberate deviation from the
     mock's 12.5px — zooming would break the layout on every field tap) */
  .xw-input{ font-size:16px; padding:13px 14px }

  /* footer: Back + full-width CTA */
  .xw-footer{ padding:14px 20px calc(18px + env(safe-area-inset-bottom)) }
  .xw-footright{ flex:1; display:flex }
  .xw-hint{ display:none }
  .xw-cta, .xw-cta.book{ flex:1; min-width:0; padding:15px 0 }
  .xw-back{ padding:0 8px; font-size:13px }

  /* done screen buttons full width */
  .xw-donebtns{ width:100%; flex-direction:column }
  .xw-donebtns .xw-cta, .xw-donebtns .xw-outline{ width:100% }
}
`
