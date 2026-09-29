import * as React from "react"

/* ══════════════════════════════════════════════════════════════════════════
 * The Schedule Service wizard — extremeheating.com's own scheduler.
 *
 * Four steps: what's wrong, when (real ServiceTitan arrival windows), about
 * the home, and confirm. The confirm step looks the visitor up by mobile
 * number in ServiceTitan, shows the STREETS on their account (never the
 * name or the house number), and books the job the moment they confirm
 * their house number. A new customer types their address and is created in
 * ServiceTitan on booking. Everything server-side lives in FollowUp Pro's
 * web-scheduler.js; this file draws and asks.
 *
 * When the live schedule cannot be read, the wizard still takes the booking
 * as a requested time and the office confirms it. A lead is never lost.
 * ══════════════════════════════════════════════════════════════════════════ */

type StepIdx = 0 | 1 | 2 | 3

const API_BASE =
    (typeof window !== "undefined" && (window as any).XH_SCHEDULER_API) ||
    "https://us-central1-followup-pro-37ed6.cloudfunctions.net"

// Quoted verbatim in the A2P campaign filing; do not reword (the JSX label repeats it).
const SMS_CONSENT_TEXT =
    "Yes, text me about my service request at the number above. Consent is not a " +
    "condition of purchase. Msg & data rates may apply, message frequency varies. " +
    "Reply HELP for help or STOP to opt out. See our Privacy Policy and Terms."

type ServiceKey = "heatingCooling" | "plumbing" | "quote" | "xplan"

type Win = {
    label: string
    start: string
    end: string
    localStart?: string
    localEnd?: string
    remaining?: number | null
    fee: number
    afterHours?: boolean
    requested?: boolean // the live schedule was not readable; this is a request
}
type Day = { date: string; weekday: string; windows: Win[]; closed: string[] }
type Avail = {
    status: "idle" | "loading" | "ok" | "no_capacity" | "unavailable" | "callback"
    days: Day[]
    first: (Win & { date: string; weekday: string }) | null
    pricing: { dispatch: number; dispatchAfterHours: number; tuneUp: number }
    fee: "dispatch" | "tuneup" | "free" | null
    key: string
}
type LookupLoc = {
    key: string
    street: string
    city: string
    state: string
    zip: string
    hasHouseNumber: boolean
    member: boolean
}
type Lookup =
    | { status: "idle" | "checking" | "new" | "unavailable" | "invalid" }
    | { status: "office"; phone: string }
    | { status: "found"; token: string; locations: LookupLoc[]; member: boolean }

type FormState = {
    service?: ServiceKey
    hvacIssue?: string
    hvacDuration?: string
    detail?: string
    answers?: Record<string, string>
    propertyType?: string
    occupant?: string
    systemAge?: string
    unitLocation?: string
    apptDate?: string // ISO yyyy-mm-dd, company-local
    window?: Win | null
    preferredContact?: "Call" | "Text" | "Email"
    callbackTime?: string
}

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
    amber: "#9A5B00",
    amberBg: "#FFF6E5",
}

const FONT = "Poppins, system-ui, sans-serif"

const EMERGENCY_PHONE_DISPLAY = "(844) 584-7399"
const EMERGENCY_PHONE_TEL = "+18445847399"

const STEP_LABELS = ["SERVICE", "TIME", "DETAILS", "CONFIRM"]
const STEP_TITLES = [
    "What's going on?",
    "When works for you?",
    "About your home",
    "Confirm & book",
]

const SERVICE_LABEL: Record<ServiceKey, string> = {
    heatingCooling: "Heating & Cooling",
    plumbing: "Plumbing",
    quote: "Get a Quote",
    xplan: "X-Plan Maintenance Plan",
}

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

/* The server's service menu keys (web-scheduler.js SERVICES). The wizard's
 * chips map onto them here; the server decides trade, board and job type. */
const HVAC_KEY: Record<string, string> = {
    "No Heat": "hvac:no_heat",
    "No Cool": "hvac:no_cool",
    "Making Noise": "hvac:noise",
    Thermostat: "hvac:thermostat",
    "Leaking Water": "hvac:leaking",
    "Air Quality": "hvac:air_quality",
    "Tune-Up": "hvac:tune_up",
}
const DETAIL_KEY: Record<string, string> = {
    "Drain Cleaning": "plumbing:drain",
    "Water Heater Issue": "plumbing:water_heater",
    "Sump Pump Issue": "plumbing:sump",
    "Leak Detection": "plumbing:leak_detection",
    "Gas Line Issue": "plumbing:gas",
    "Water Treatment": "plumbing:water_treatment",
    "Pipe Leak": "plumbing:pipe_leak",
    "General Plumbing Repair": "plumbing:general",
    "New System Estimate": "quote:new_system",
    "Duct Cleaning Estimate": "quote:duct_cleaning",
    "Dryer Vent Cleaning Estimate": "quote:dryer_vent",
    "HVAC Inspection Estimate": "quote:inspection",
    "Schedule Seasonal Tune-Up": "xplan:tune_up",
    "Enroll in Plan": "xplan:enroll",
    "Questions About Benefits": "xplan:benefits",
    "Billing / Payment Question": "xplan:billing",
}
const CALLBACK_KEYS = new Set(["xplan:benefits", "xplan:billing"])
const FREE_KEYS = new Set([
    "quote:new_system",
    "quote:duct_cleaning",
    "quote:dryer_vent",
    "plumbing:water_treatment",
])
const TUNEUP_KEYS = new Set(["hvac:tune_up", "xplan:tune_up", "xplan:enroll"])

function serviceKeyOf(d: FormState): string {
    if (!d.service) return ""
    if (d.service === "heatingCooling") return HVAC_KEY[d.hvacIssue || ""] || ""
    return DETAIL_KEY[d.detail || ""] || ""
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
    "Drain Cleaning": [
        {
            id: "which",
            label: "Which drain is affected?",
            field: "Affected drain",
            options: ["Kitchen", "Bathroom", "Toilet", "Shower / Tub", "Main line", "Multiple", "Not sure"],
        },
    ],
    "Water Heater Issue": [
        {
            id: "problem",
            label: "What's the problem?",
            field: "Problem",
            options: ["No hot water", "Not enough hot water", "Leaking", "Other"],
        },
    ],
    "Sump Pump Issue": [
        {
            id: "problem",
            label: "What's happening?",
            field: "Problem",
            options: ["Not running", "Running constantly", "Pit overflowing", "Not sure"],
        },
    ],
    "Leak Detection": [
        {
            id: "where",
            label: "Where do you suspect the leak?",
            field: "Suspected location",
            options: ["Under a sink", "Wall / ceiling", "Floor / slab", "Outdoor", "Not sure"],
        },
    ],
    "Gas Line Issue": [
        {
            id: "need",
            label: "What do you need?",
            field: "Request",
            options: ["Smell of gas", "New appliance hookup", "Suspected leak", "Other"],
        },
    ],
    "Water Treatment": [
        {
            id: "interest",
            label: "What are you interested in?",
            field: "Interest",
            options: ["Water softener", "Filtration", "Water testing", "Not sure"],
        },
    ],
    "Pipe Leak": [
        {
            id: "where",
            label: "Where is the leak?",
            field: "Leak location",
            options: ["Under a sink", "Wall / ceiling", "Basement", "Outdoor", "Not sure"],
        },
    ],
    "General Plumbing Repair": [
        {
            id: "fixture",
            label: "What needs attention?",
            field: "Fixture",
            options: ["Faucet", "Toilet", "Garbage disposal", "Shower / Tub", "Other"],
        },
    ],
    "New System Estimate": [
        {
            id: "scope",
            label: "What's the quote for?",
            field: "Quote scope",
            options: ["AC only", "Furnace only", "Full system (AC + furnace)"],
        },
    ],
    "Duct Cleaning Estimate": [
        { id: "vents", label: "Roughly how many vents?", field: "Vent count", options: DUCT_VENT_OPTIONS },
    ],
    "Dryer Vent Cleaning Estimate": [],
    "HVAC Inspection Estimate": [
        {
            id: "reason",
            label: "Reason for inspection?",
            field: "Reason",
            options: ["Home purchase", "Routine check", "Performance concern", "Other"],
        },
    ],
    "Schedule Seasonal Tune-Up": [
        { id: "system", label: "Which system?", field: "System", options: ["Heating", "Cooling", "Both"] },
    ],
    "Enroll in Plan": [],
}

function getSubQuestions(detail?: string): SubQuestion[] {
    if (!detail) return []
    return DETAIL_QUESTIONS[detail] || []
}

const AGE_OPTIONS = ["Under 5 years", "5–10 years", "10–15 years", "15+ years", "Not sure"]
const UNIT_LOCATIONS = ["Side of house", "Backyard", "Rooftop", "Ground level", "Not sure"]
const CALLBACK_TIMES = ["Morning", "Afternoon", "Anytime"]

function isHvacContext(service?: ServiceKey, detail?: string): boolean {
    if (service === "heatingCooling") return true
    if (service === "xplan") return true
    if (service === "quote" && (detail === "New System Estimate" || detail === "HVAC Inspection Estimate")) return true
    return false
}
function asksAge(service?: ServiceKey, detail?: string): { ask: boolean; label: string } {
    if (isHvacContext(service, detail)) return { ask: true, label: "How old is the system?" }
    if (service === "plumbing" && detail === "Water Heater Issue")
        return { ask: true, label: "How old is the water heater?" }
    return { ask: false, label: "" }
}

const CLOUDINARY_CLOUD = "dsbmasn0l"
const CLOUDINARY_UNSIGNED_PRESET = "images"

async function uploadPhotosToCloudinary(files: File[]): Promise<string[]> {
    const urls: string[] = []
    for (const f of files.slice(0, 3)) {
        const fd = new FormData()
        fd.append("file", f)
        fd.append("upload_preset", CLOUDINARY_UNSIGNED_PRESET)
        const res = await fetch(`https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD}/auto/upload`, {
            method: "POST",
            body: fd,
        })
        if (!res.ok) throw new Error("Upload failed")
        const json = await res.json()
        urls.push(json.secure_url)
    }
    return urls
}

const GOOGLE_MAPS_API_KEY = "AIzaSyABVMGJ738G-WyGCCCr_YlIk2yEGln_jeY"
const GEO_BIAS_LAT = 39.7589
const GEO_BIAS_LON = -84.1916
const OHIO_BOUNDS = { south: 38.4, west: -84.82, north: 42.0, east: -80.52 }
const OHIO_RE = /,\s*(OH\b|Ohio)/i

type AddressSuggestion = { id: string; label: string; src: "google" | "photon" }
type AddressParts = { street: string; city: string; state: string; zip: string }

// Google calls window.gm_authFailure by that exact name when the key is rejected.
let googleUnavailable = false
if (typeof window !== "undefined") {
    ;(window as any).gm_authFailure = () => {
        googleUnavailable = true
        console.warn("[XHAC] Google Maps auth failed — falling back to free geocoder.")
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
        s.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&libraries=places&callback=${cbName}`
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
                    reject(new Error(`Places status: ${status}`))
                }
            }
        )
    })
}

/* The street, city, state and zip from a place, so the booking carries the
 * parts ServiceTitan wants rather than one line we have to split. */
async function googlePlaceParts(placeId: string): Promise<AddressParts | null> {
    try {
        const google = await loadGoogleMaps(GOOGLE_MAPS_API_KEY)
        const svc = new google.maps.places.PlacesService(document.createElement("div"))
        return new Promise((resolve) => {
            svc.getDetails({ placeId, fields: ["address_components"] }, (place: any, status: string) => {
                if (status !== google.maps.places.PlacesServiceStatus.OK || !place?.address_components) return resolve(null)
                const get = (type: string, short = false) => {
                    const c = place.address_components.find((x: any) => (x.types || []).includes(type))
                    return c ? (short ? c.short_name : c.long_name) : ""
                }
                const num = get("street_number"), route = get("route")
                const city = get("locality") || get("sublocality") || get("administrative_area_level_3") || get("neighborhood")
                resolve({
                    street: [num, route].filter(Boolean).join(" "),
                    city,
                    state: get("administrative_area_level_1", true),
                    zip: get("postal_code"),
                })
            })
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
    const typedHouseNum = (query.match(/^\s*(\d+)\s+/) || [])[1] || ""
    return feats
        .filter((f) => (f.properties?.state || "") === "Ohio")
        .map((f, i) => {
            const p = f.properties || {}
            const street = p.street || p.name || ""
            const houseNum = p.housenumber || typedHouseNum
            const line1 = [houseNum, street].filter(Boolean).join(" ") || p.name
            const parts = [line1, p.city || p.town || p.village || p.county, p.state, p.postcode].filter(Boolean)
            return { id: `${i}-${p.osm_id || line1 || ""}`, label: parts.join(", "), src: "photon" as const }
        })
        .filter((s) => s.label.trim().length > 0)
        .slice(0, 5)
}

async function fetchAddressSuggestions(query: string): Promise<AddressSuggestion[]> {
    if (query.trim().length < 3) return []
    try {
        if (GOOGLE_MAPS_API_KEY && !googleUnavailable) return await googlePredictions(query)
        return await photonPredictions(query)
    } catch {
        try {
            return await photonPredictions(query)
        } catch {
            return []
        }
    }
}

// One address line, so pull the parts out of "street, city, ST ZIP"
function splitAddress(raw: string): AddressParts {
    const out: AddressParts = { street: "", city: "", state: "", zip: "" }
    const s = raw.replace(/,\s*(USA|United States)\s*$/i, "")
    const zip = s.match(/\b(\d{5})(?:-\d{4})?\s*$/)
    if (zip) out.zip = zip[1]
    const parts = s
        .split(",")
        .map((p) => p.trim())
        .filter((p) => p && !/^\d{5}(-\d{4})?$/.test(p))
    const st = (parts[parts.length - 1] || "").replace(/\s*\d{5}(-\d{4})?$/, "")
    if (parts.length >= 2 && /^([A-Za-z]{2}|Ohio)$/i.test(st)) {
        out.state = /^ohio$/i.test(st) ? "OH" : st.toUpperCase()
        out.city = parts[parts.length - 2]
        if (parts.length > 2) out.street = parts.slice(0, -2).join(", ")
    } else if (parts.length === 1) {
        out.street = parts[0]
    }
    return out
}

declare global {
    interface Window {
        dataLayer?: Record<string, any>[]
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
    try {
        const params = new URLSearchParams(window.location.search)
        for (const k of ["gclid", "gbraid", "wbraid"]) {
            const v = params.get(k)
            if (v) localStorage.setItem("xhac_" + k, v)
        }
    } catch {}
}
storeClickIds()

function newId(): string {
    try {
        if (window.crypto?.randomUUID) return window.crypto.randomUUID()
    } catch {}
    return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

// Google wants E.164; anything that isn't a US number is left out
function toE164(raw: string): string | undefined {
    const d = raw.replace(/\D/g, "")
    if (d.length === 10 && /^[2-9]/.test(d)) return "+1" + d
    if (d.length === 11 && /^1[2-9]/.test(d)) return "+" + d
    return undefined
}

function fromISO(iso: string): Date {
    const [y, m, d] = iso.split("-").map(Number)
    return new Date(y, m - 1, d)
}
function toISO(d: Date): string {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`
}
function fmtDay(iso: string, style: "short" | "long" = "short"): string {
    const d = fromISO(iso)
    return d.toLocaleDateString(
        "en-US",
        style === "short" ? { weekday: "short", month: "short", day: "numeric" } : { weekday: "long", month: "long", day: "numeric" }
    )
}
function todayISO(): string {
    return toISO(new Date())
}
function tomorrowISO(): string {
    const t = new Date()
    t.setDate(t.getDate() + 1)
    return toISO(t)
}
function relDay(iso: string): string {
    if (iso === todayISO()) return "Today"
    if (iso === tomorrowISO()) return "Tomorrow"
    return fromISO(iso).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" })
}
function shortLabel(label: string): string {
    // "8am–12pm" → "8–12 AM"-ish stays readable as is; keep the server's label.
    return label.replace(/am/g, " AM").replace(/pm/g, " PM").replace(/\s+/g, " ").trim()
}
function money(n: number): string {
    return "$" + Math.round(n).toLocaleString("en-US")
}

/* Arrival windows to offer when the live schedule cannot be read: the same
 * shape as the server's, flagged `requested`. Company-local times are taken
 * from the visitor's clock, which is right for a customer in Ohio. */
function requestedWindows(): Day[] {
    const out: Day[] = []
    const d = new Date()
    d.setHours(0, 0, 0, 0)
    d.setDate(d.getDate() + 1)
    const slots: [string, number, number][] = [["8am–12pm", 8, 12], ["12pm–4pm", 12, 16], ["5pm–10pm", 17, 22]]
    while (out.length < 10) {
        const dow = d.getDay()
        if (dow !== 0 && dow !== 6) {
            const iso = toISO(d)
            out.push({
                date: iso,
                weekday: d.toLocaleDateString("en-US", { weekday: "long" }),
                windows: slots.map(([label, h1, h2]) => {
                    const s = new Date(d), e = new Date(d)
                    s.setHours(h1, 0, 0, 0)
                    e.setHours(h2, 0, 0, 0)
                    return { label, start: s.toISOString(), end: e.toISOString(), fee: h1 >= 17 ? 197 : 97, afterHours: h1 >= 17, requested: true }
                }),
                closed: [],
            })
        }
        d.setDate(d.getDate() + 1)
    }
    return out
}

function downloadICS(win: Win, service: string, address: string) {
    const pad = (n: number) => String(n).padStart(2, "0")
    const stamp = (iso: string) => {
        const d = new Date(iso)
        return `${d.getUTCFullYear()}${pad(d.getUTCMonth() + 1)}${pad(d.getUTCDate())}T${pad(d.getUTCHours())}${pad(d.getUTCMinutes())}00Z`
    }
    const ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Extreme Heating//Schedule//EN",
        "BEGIN:VEVENT",
        `DTSTART:${stamp(win.start)}`,
        `DTEND:${stamp(win.end)}`,
        `SUMMARY:Extreme Heating, Air & Plumbing — ${service}`,
        `LOCATION:${address}`,
        `DESCRIPTION:Arrival window ${win.label}. Questions? Call ${EMERGENCY_PHONE_DISPLAY}.`,
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

/* ── The API ──────────────────────────────────────────────────────────────── */
async function apiGet(path: string): Promise<any> {
    const res = await fetch(API_BASE + path, { headers: { Accept: "application/json" } })
    return res.json()
}
async function apiPost(path: string, body: any): Promise<any> {
    const res = await fetch(API_BASE + path, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(body),
    })
    const j = await res.json().catch(() => ({}))
    if (res.status === 429) return { success: false, status: "rate_limited", error: j.error }
    return j
}

const availCache = new Map<string, Avail>()
async function fetchAvailability(key: string, age?: string, member?: boolean): Promise<Avail> {
    const q = new URLSearchParams({ service: key })
    if (age) q.set("age", age)
    if (member) q.set("member", "1")
    const ck = q.toString()
    const hit = availCache.get(ck)
    if (hit && hit.status !== "unavailable") return hit
    let out: Avail
    try {
        const j = await apiGet("/schedulerAvailability?" + ck)
        if (j.status === "callback") {
            out = { status: "callback", days: [], first: null, pricing: { dispatch: 97, dispatchAfterHours: 197, tuneUp: 119 }, fee: null, key }
        } else if (j.status === "ok" || j.status === "no_capacity") {
            out = { status: j.status, days: j.days || [], first: j.first || null, pricing: j.pricing, fee: j.fee, key }
        } else {
            out = { status: "unavailable", days: [], first: null, pricing: j.pricing || { dispatch: 97, dispatchAfterHours: 197, tuneUp: 119 }, fee: j.fee || null, key }
        }
    } catch {
        out = { status: "unavailable", days: [], first: null, pricing: { dispatch: 97, dispatchAfterHours: 197, tuneUp: 119 }, fee: null, key }
    }
    availCache.set(ck, out)
    return out
}

function IconHVAC({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <path d="M4 8h16M4 12h16M4 16h16" stroke={T.deepPurple} strokeWidth="2" strokeLinecap="round" />
        </svg>
    )
}
function IconPlumb({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" stroke={T.deepPurple} strokeWidth="2" />
            <circle cx="12" cy="12" r="2" fill={T.deepPurple} />
        </svg>
    )
}
function IconQuote({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <rect x="5" y="3" width="14" height="18" rx="2" stroke={T.deepPurple} strokeWidth="2" />
            <path d="M9 8h6M9 12h6M9 16h4" stroke={T.deepPurple} strokeWidth="2" strokeLinecap="round" />
        </svg>
    )
}
function IconPlan({ dim = 22 }) {
    return (
        <svg width={dim} height={dim} viewBox="0 0 24 24" fill="none">
            <rect x="3" y="5" width="18" height="16" rx="2" stroke={T.deepPurple} strokeWidth="2" />
            <path d="M3 10h18M8 3v4M16 3v4" stroke={T.deepPurple} strokeWidth="2" strokeLinecap="round" />
        </svg>
    )
}

function ensurePoppins() {
    if (typeof document === "undefined") return
    if (document.querySelector("link[data-xhac-poppins]")) return
    const l = document.createElement("link")
    l.rel = "stylesheet"
    l.href = "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
    l.setAttribute("data-xhac-poppins", "true")
    document.head.appendChild(l)
}

type Booked = {
    status: "booked" | "received"
    jobNumber?: string
    window?: Win | null
    date?: string
    emailed?: boolean
    callback?: boolean
    address?: string
    fee?: number
}

export default function ContactFlowDialog() {
    const [open, setOpen] = React.useState(false)
    const [appeared, setAppeared] = React.useState(false)

    const [step, setStep] = React.useState<StepIdx>(0)
    const [booked, setBooked] = React.useState<Booked | null>(null)

    const [data, setData] = React.useState<FormState>({ preferredContact: "Text" })
    const [noteOpen, setNoteOpen] = React.useState(false)
    const [note, setNote] = React.useState("")
    const [photos, setPhotos] = React.useState<File[]>([])
    const [firstName, setFirstName] = React.useState("")
    const [lastName, setLastName] = React.useState("")
    const [phoneDigits, setPhoneDigits] = React.useState("")
    const [email, setEmail] = React.useState("")
    const [addrLine, setAddrLine] = React.useState("")
    const [addrParts, setAddrParts] = React.useState<AddressParts>({ street: "", city: "", state: "OH", zip: "" })
    const [unit, setUnit] = React.useState("")
    const [feeOk, setFeeOk] = React.useState(false)
    // Must start false (a pre-ticked box is A2P rejection 30925) and must never gate stepComplete.
    const [smsOk, setSmsOk] = React.useState(false)
    const [submitting, setSubmitting] = React.useState(false)
    const [submitError, setSubmitError] = React.useState("")
    const [houseError, setHouseError] = React.useState("")

    // Who: the ServiceTitan lookup on the mobile number.
    const [lookup, setLookup] = React.useState<Lookup>({ status: "idle" })
    const [locKey, setLocKey] = React.useState<string>("")
    const [houseNumber, setHouseNumber] = React.useState("")
    const [asNew, setAsNew] = React.useState(false)
    const lookupSeq = React.useRef(0)
    const lookupDebounce = React.useRef<number | null>(null)

    // When: the live schedule.
    const [avail, setAvail] = React.useState<Avail>({ status: "idle", days: [], first: null, pricing: { dispatch: 97, dispatchAfterHours: 197, tuneUp: 119 }, fee: null, key: "" })
    const availSeq = React.useRef(0)

    const [addrSuggestions, setAddrSuggestions] = React.useState<AddressSuggestion[]>([])
    const [addrLoading, setAddrLoading] = React.useState(false)
    const [addrOpen, setAddrOpen] = React.useState(false)
    const addrDebounce = React.useRef<number | null>(null)
    const addrSeq = React.useRef(0)

    const photoInputRef = React.useRef<HTMLInputElement | null>(null)
    const requestIdRef = React.useRef<string>(newId())

    const photoPreviews = React.useMemo(() => photos.map((f) => ({ file: f, url: URL.createObjectURL(f) })), [photos])
    React.useEffect(() => {
        return () => photoPreviews.forEach((p) => URL.revokeObjectURL(p.url))
    }, [photoPreviews])

    const [vw, setVw] = React.useState<number>(typeof window !== "undefined" ? window.innerWidth : 1200)
    React.useEffect(() => {
        const onR = () => setVw(window.innerWidth)
        onR()
        window.addEventListener("resize", onR)
        return () => window.removeEventListener("resize", onR)
    }, [])
    const isMobile = vw <= 809

    React.useEffect(ensurePoppins, [])

    const openedOnceRef = React.useRef(false)
    React.useEffect(() => {
        if (open && !openedOnceRef.current) {
            openedOnceRef.current = true
            ;(window.dataLayer = window.dataLayer || []).push({
                event: "Online Booking Form Opened",
                booking_source: "website_scheduler",
                device_type: getDeviceType(),
            })
        }
        if (!open) openedOnceRef.current = false
    }, [open])

    React.useEffect(() => {
        const handler = () => {
            setOpen(true)
            setStep(0)
            setBooked(null)
            setData({ preferredContact: "Text" })
            setNoteOpen(false)
            setNote("")
            setPhotos([])
            setFirstName("")
            setLastName("")
            setPhoneDigits("")
            setEmail("")
            setAddrLine("")
            setAddrParts({ street: "", city: "", state: "OH", zip: "" })
            setUnit("")
            setFeeOk(false)
            setSmsOk(false)
            setSubmitError("")
            setHouseError("")
            setLookup({ status: "idle" })
            setLocKey("")
            setHouseNumber("")
            setAsNew(false)
            setAddrSuggestions([])
            setAddrOpen(false)
            setAvail({ status: "idle", days: [], first: null, pricing: { dispatch: 97, dispatchAfterHours: 197, tuneUp: 119 }, fee: null, key: "" })
            requestIdRef.current = newId()
        }
        window.addEventListener("open-contact-dialog", handler as EventListener)
        const onMessage = (e: MessageEvent) => {
            if (e?.data?.type === "open-contact-dialog") handler()
        }
        window.addEventListener("message", onMessage)
        return () => {
            window.removeEventListener("open-contact-dialog", handler as EventListener)
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

    /* ── The live schedule: asked as soon as a service is picked, so the time
     * step opens with the windows already there. ─────────────────────────── */
    const serviceKey = serviceKeyOf(data)
    const isCallback = CALLBACK_KEYS.has(serviceKey)
    const isMember = lookup.status === "found" && !asNew && !!locKey && lookup.locations.some((l) => l.key === locKey && l.member)
    React.useEffect(() => {
        if (!open || !serviceKey || isCallback) return
        const seq = ++availSeq.current
        setAvail((a) => (a.key === serviceKey && a.status !== "idle" && a.status !== "unavailable" ? a : { ...a, status: "loading", key: serviceKey }))
        fetchAvailability(serviceKey, data.systemAge, isMember).then((a) => {
            if (seq !== availSeq.current) return
            setAvail(a)
            // A window picked for another service is not a window for this one.
            setData((d) => (d.window && d.window.requested !== (a.status !== "ok") ? { ...d, window: null, apptDate: undefined } : d))
        })
    }, [open, serviceKey, isCallback, isMember]) // eslint-disable-line react-hooks/exhaustive-deps

    if (!open) return null

    const close = () => setOpen(false)

    const emailOk = email.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
    const phoneOk = phoneDigits.length === 10

    function serviceStepComplete(d: FormState): boolean {
        if (!d.service) return false
        if (d.service === "heatingCooling") return !!d.hvacIssue
        return !!d.detail
    }

    const svcFee: "dispatch" | "tuneup" | "free" = FREE_KEYS.has(serviceKey) ? "free" : TUNEUP_KEYS.has(serviceKey) ? "tuneup" : "dispatch"
    const feeFor = (w: Win | null | undefined): number => {
        if (!w) return 0
        if (svcFee === "free") return 0
        if (svcFee === "tuneup") return isMember ? 0 : avail.pricing.tuneUp
        return w.afterHours ? avail.pricing.dispatchAfterHours : avail.pricing.dispatch
    }
    const fee = feeFor(data.window)
    const feeRequired = fee > 0

    const knownCustomer = lookup.status === "found" && !asNew
    const identityOk = knownCustomer
        ? !!locKey && (houseNumber.trim().length > 0 || !lookup.locations.find((l) => l.key === locKey)?.hasHouseNumber)
        : addrParts.street.trim().length >= 3 && addrParts.city.trim().length >= 2 && /^\d{5}$/.test(addrParts.zip)
    const blockedByOffice = lookup.status === "office" && !asNew

    const stepComplete: boolean[] = [
        serviceStepComplete(data),
        isCallback ? !!data.callbackTime : !!data.window,
        true,
        Boolean(
            firstName.trim() && lastName.trim() && phoneOk && !blockedByOffice && lookup.status !== "checking" &&
            identityOk && (feeOk || !feeRequired) && emailOk
        ),
    ]

    const hints: string[] = [
        !data.service ? "Pick a service to continue" : !stepComplete[0] ? (data.service === "heatingCooling" ? "Pick the issue to continue" : "Pick what you need to continue") : "",
        !stepComplete[1] ? (isCallback ? "Pick a good time to call" : "Pick a day and arrival window") : "",
        "Everything here is skippable",
        !stepComplete[3]
            ? blockedByOffice ? "Please call us to book this one"
            : !phoneOk ? "Add your mobile number"
            : lookup.status === "checking" ? "Checking your number…"
            : !identityOk ? (knownCustomer ? "Pick your address and confirm the house number" : "Add your service address")
            : !firstName.trim() || !lastName.trim() ? "Add your name"
            : feeRequired && !feeOk ? "Accept the visit fee to book" : ""
            : "",
    ]

    const canContinue = stepComplete[step]

    const patch = (p: Partial<FormState>) => setData((d) => ({ ...d, ...p }))
    const toggle = (key: keyof FormState, value: string) =>
        setData((d) => ({ ...d, [key]: (d[key] as any) === value ? undefined : value }))
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

    /* ── The phone lookup ──────────────────────────────────────────────────── */
    function onPhoneChange(v: string) {
        const digits = v.replace(/\D/g, "").replace(/^1(?=\d{10})/, "").slice(0, 10)
        setPhoneDigits(digits)
        setSubmitError("")
        if (lookupDebounce.current) window.clearTimeout(lookupDebounce.current)
        if (digits.length !== 10) {
            lookupSeq.current++
            setLookup({ status: "idle" })
            setLocKey("")
            setHouseNumber("")
            setAsNew(false)
            return
        }
        setLookup({ status: "checking" })
        lookupDebounce.current = window.setTimeout(async () => {
            const seq = ++lookupSeq.current
            let r: any
            try {
                r = await apiPost("/schedulerLookup", { phone: digits })
            } catch {
                r = { status: "unavailable" }
            }
            if (seq !== lookupSeq.current) return
            setLocKey("")
            setHouseNumber("")
            setAsNew(false)
            if (r.status === "found" && Array.isArray(r.locations) && r.locations.length) {
                setLookup({ status: "found", token: r.token, locations: r.locations, member: !!r.member })
                if (r.locations.length === 1) setLocKey(r.locations[0].key)
            } else if (r.status === "office") {
                setLookup({ status: "office", phone: r.phone || EMERGENCY_PHONE_DISPLAY })
            } else if (r.status === "invalid") {
                setLookup({ status: "invalid" })
            } else if (r.status === "new") {
                setLookup({ status: "new" })
            } else {
                setLookup({ status: "unavailable" })
            }
        }, 250)
    }

    function onAddressChange(v: string) {
        setAddrLine(v)
        setAddrParts((p) => ({ ...p, ...splitAddress(v), state: splitAddress(v).state || p.state || "OH" }))
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
        setAddrLine(sugg.label)
        setAddrParts((p) => ({ ...p, ...splitAddress(sugg.label) }))
        setAddrSuggestions([])
        setAddrOpen(false)
        if (sugg.src === "google") {
            const parts = await googlePlaceParts(sugg.id)
            if (parts && parts.street) {
                setAddrParts({ street: parts.street, city: parts.city, state: parts.state || "OH", zip: parts.zip })
                setAddrLine([parts.street, parts.city, [parts.state, parts.zip].filter(Boolean).join(" ")].filter(Boolean).join(", "))
            }
        }
    }

    const goNext = () => setStep((s) => Math.min(s + 1, 3) as StepIdx)
    const goBack = () => setStep((s) => Math.max(s - 1, 0) as StepIdx)

    const serviceRequired = data.service === "heatingCooling" ? data.hvacIssue || "" : data.detail || ""
    const svcSummary = data.service
        ? `${SERVICE_LABEL[data.service].replace(" Maintenance Plan", "")}${serviceRequired ? " · " + serviceRequired : ""}`
        : ""
    const whenSummary = isCallback
        ? data.callbackTime ? `We'll call · ${data.callbackTime}` : ""
        : data.window && data.apptDate ? `${relDay(data.apptDate)} · ${shortLabel(data.window.label)}` : ""
    const homeSummary = [data.propertyType, data.occupant].filter(Boolean).join(" · ")
    const chosenLoc = lookup.status === "found" ? lookup.locations.find((l) => l.key === locKey) : undefined
    const whereSummary = knownCustomer
        ? chosenLoc ? `${houseNumber.trim() ? houseNumber.trim() + " " : ""}${chosenLoc.street}, ${chosenLoc.city}` : ""
        : addrParts.street ? `${addrParts.street}${unit ? " " + unit : ""}, ${addrParts.city}` : ""

    /* ── Book ───────────────────────────────────────────────────────────────── */
    async function bookVisit() {
        if (submitting || !canContinue) return
        setSubmitting(true)
        setSubmitError("")
        setHouseError("")

        let photoUrls: string[] = []
        try {
            if (photos?.length) photoUrls = await uploadPhotosToCloudinary(photos)
        } catch (e) {
            console.warn("Photo upload failed:", e)
        }

        const answers: Record<string, string> = {}
        getSubQuestions(data.detail).forEach((q) => {
            const v = data.answers?.[q.id]
            if (v) answers[q.field] = v
        })
        if (isCallback && data.callbackTime) answers["Best time to call"] = data.callbackTime

        const body: any = {
            clientRequestId: requestIdRef.current,
            service: serviceKey,
            detail: serviceRequired,
            duration: data.service === "heatingCooling" ? data.hvacDuration || "" : "",
            answers,
            propertyType: data.propertyType || "",
            occupant: data.occupant || "",
            systemAge: data.systemAge || "",
            unitLocation: data.unitLocation || "",
            note: note.trim(),
            photos: photoUrls,
            window: data.window ? { label: data.window.label, date: data.apptDate, start: data.window.start, end: data.window.end, requested: !!data.window.requested } : null,
            firstName: firstName.trim(),
            lastName: lastName.trim(),
            phone: phoneDigits,
            email: email.trim(),
            preferredContact: data.preferredContact,
            feeOk: feeOk || !feeRequired,
            smsOk,
            smsConsentText: smsOk ? SMS_CONSENT_TEXT : "",
            member: isMember,
            page: typeof location !== "undefined" ? location.href.slice(0, 200) : "",
            website: "", // honeypot: stays empty for a person
        }
        if (knownCustomer && lookup.status === "found") {
            body.token = lookup.token
            body.locationKey = locKey
            body.houseNumber = houseNumber.trim()
            body.zip = chosenLoc?.zip || ""
        } else {
            body.address = { street: addrParts.street.trim(), unit: unit.trim(), city: addrParts.city.trim(), state: (addrParts.state || "OH").trim(), zip: addrParts.zip.trim() }
        }

        let r: any
        try {
            r = await apiPost("/schedulerBook", body)
        } catch {
            r = { success: false, status: "network" }
        }
        setSubmitting(false)

        if (r && (r.status === "booked" || r.status === "received")) {
            try {
                const addr: Record<string, string> = {
                    first_name: firstName.trim(),
                    last_name: lastName.trim(),
                    country: "US",
                }
                if (!knownCustomer) {
                    if (addrParts.street) addr.street = addrParts.street
                    if (addrParts.city) addr.city = addrParts.city
                    if (addrParts.state) addr.region = addrParts.state
                    if (addrParts.zip) addr.postal_code = addrParts.zip
                }
                const userData: Record<string, any> = { address: addr }
                if (email.trim()) userData.email = email.trim().toLowerCase()
                const phone = toE164(phoneDigits)
                if (phone) userData.phone_number = phone
                ;(window.dataLayer = window.dataLayer || []).push({
                    event: "Online Booking Completed",
                    booking_source: "website_scheduler",
                    lead_id: requestIdRef.current,
                    service: svcSummary,
                    booked_in_servicetitan: r.status === "booked",
                    job_number: r.jobNumber || "",
                    user_data: userData,
                })
            } catch (err) {
                console.warn("dataLayer push error", err)
            }
            setBooked({
                status: r.status,
                jobNumber: r.jobNumber,
                window: r.arrivalWindow ? { ...r.arrivalWindow, fee: r.fee ?? fee } : data.window,
                date: (r.arrivalWindow && r.arrivalWindow.date) || data.apptDate,
                emailed: !!r.emailed,
                callback: !!r.callback || isCallback,
                address: r.address || whereSummary,
                fee: typeof r.fee === "number" ? r.fee : fee,
            })
            return
        }
        // Another attempt gets a fresh id only when this one was refused for
        // a reason the visitor can fix; a network failure keeps it, so the
        // server can replay rather than book twice.
        if (r?.status === "house_number_mismatch") {
            setHouseError(r.error || "That house number doesn't match the address on file.")
            requestIdRef.current = newId()
        } else if (r?.status === "lookup_expired") {
            setSubmitError("Your lookup timed out — re-enter your mobile number.")
            setLookup({ status: "idle" })
            setLocKey("")
            requestIdRef.current = newId()
        } else if (r?.status === "rate_limited") {
            setSubmitError(r.error || `Too many requests just now. Give it a minute, or call ${EMERGENCY_PHONE_DISPLAY}.`)
        } else if (r?.status === "bad_request") {
            setSubmitError(r.error || "Something's missing — check the form and try again.")
            requestIdRef.current = newId()
        } else {
            setSubmitError(`We couldn't reach our scheduler. Try again, or call ${EMERGENCY_PHONE_DISPLAY} and we'll book it by phone.`)
        }
    }

    /* ── Small pieces ───────────────────────────────────────────────────────── */
    const chip = (selected: boolean, label: string, onClick: () => void, key?: string) => (
        <button key={key ?? label} className={"xw-chip" + (selected ? " sel" : "")} onClick={onClick} type="button">
            {selected ? "✓  " + label : label}
        </button>
    )

    const groupLabel = (text: string, optional?: boolean) => (
        <div className="xw-glabel">
            {text}
            {optional ? <span className="opt"> — optional</span> : null}
        </div>
    )

    const svcCards = [
        { key: "heatingCooling" as const, name: "Heating & Cooling", sub: "Repair or tune-up", icon: <IconHVAC /> },
        { key: "plumbing" as const, name: "Plumbing", sub: "Leaks, drains, heaters", icon: <IconPlumb /> },
        { key: "quote" as const, name: "Get a Quote", sub: "New system estimate", icon: <IconQuote /> },
        { key: "xplan" as const, name: "X-Plan", sub: "Membership & tune-ups", icon: <IconPlan /> },
    ]

    const ageQ = asksAge(data.service, data.detail)

    // The days the time step can show: real ones, or requested ones.
    const liveDays: Day[] = avail.status === "ok" ? avail.days : []
    const fallbackMode = avail.status === "unavailable" || avail.status === "no_capacity"
    const days: Day[] = liveDays.length ? liveDays : fallbackMode ? requestedWindows() : []
    const openDays = days.filter((d) => d.windows.length)
    const quickPicks = openDays
        .flatMap((d) => d.windows.map((w) => ({ date: d.date, win: w })))
        .slice(0, 3)
    const selectedDay = days.find((d) => d.date === data.apptDate)
    const pickWindow = (date: string, w: Win) => patch({ apptDate: date, window: w })
    const winSel = (date: string, w: Win) => data.apptDate === date && data.window?.start === w.start
    const feeTag = (w: Win) => {
        const f = feeFor(w)
        if (svcFee === "free") return "Free"
        if (svcFee === "tuneup") return isMember ? "Included" : money(f)
        return w.afterHours ? `Evening · ${money(f)}` : money(f)
    }

    const feeCopyText = (() => {
        if (svcFee === "free") return "There's no charge for this visit. Your estimate is free."
        if (svcFee === "tuneup") return isMember
            ? "Included with your X-Plan membership."
            : "Flat-rate tune-up, quoted up front. No dispatch fee on top."
        const evening = !!data.window?.afterHours
        const what = data.service === "plumbing" ? "a complete plumbing diagnosis" : "a full system check"
        return isMobile
            ? `Travel + ${data.service === "plumbing" ? "plumbing diagnosis" : "system check"}, quoted up front${evening ? " (evening rate)" : ""}.`
            : `Covers your technician's travel and ${what}${evening ? " at the evening rate" : ""} — quoted up front, no surprises at the door.`
    })()

    return (
        <div className="xw-root" role="dialog" aria-modal="true" style={{ position: "fixed", inset: 0, zIndex: 9999, fontFamily: FONT }}>
            <style>{XW_CSS}</style>

            <div
                onClick={close}
                style={{
                    position: "absolute",
                    inset: 0,
                    background: "linear-gradient(160deg, rgba(36,21,51,.92), rgba(58,35,82,.92))",
                    backdropFilter: "blur(6px)",
                    WebkitBackdropFilter: "blur(6px)",
                    opacity: appeared ? 1 : 0,
                    transition: "opacity 240ms ease",
                }}
            />

            <div
                className="xw-modal"
                style={{ opacity: appeared ? 1 : 0, transform: appeared ? "translateY(0) scale(1)" : "translateY(12px) scale(0.985)" }}
                onPointerDown={(e) => e.stopPropagation()}
                onPointerUp={(e) => e.stopPropagation()}
                onClick={(e) => e.stopPropagation()}
            >
                {/* ---------- HEADER ---------- */}
                <div className="xw-header">
                    {isMobile ? (
                        <>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <div className="xw-eyebrow">Schedule Service</div>
                                <button className="xw-close" onClick={close} aria-label="Close" type="button">✕</button>
                            </div>
                            <div className="xw-title">{booked ? (booked.status === "booked" ? "You're booked!" : "Got it!") : STEP_TITLES[step]}</div>
                            <div className="xw-progress">
                                {STEP_LABELS.map((label, i) => {
                                    const done2 = !!booked || i < step
                                    const cur = !booked && i === step
                                    const clickable = !booked && i < step
                                    return (
                                        <div key={label} className={"xw-seg" + (clickable ? " click" : "")} onClick={() => clickable && setStep(i as StepIdx)}>
                                            <div className="bar" style={{ background: done2 || cur ? T.progressGreen : "rgba(255,255,255,.18)" }} />
                                        </div>
                                    )
                                })}
                                {!booked && <div className="xw-stepcount">{step + 1} of 4</div>}
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="xw-headtop">
                                <div style={{ minWidth: 0 }}>
                                    <div className="xw-eyebrow">Schedule Service</div>
                                    <div className="xw-title">{booked ? (booked.status === "booked" ? "You're booked!" : "Got it!") : STEP_TITLES[step]}</div>
                                </div>
                                <div className="xw-headright">
                                    {!booked && (
                                        <a className="xw-emergency" href={`tel:${EMERGENCY_PHONE_TEL}`}>
                                            <span className="dot" />
                                            Emergency? {EMERGENCY_PHONE_DISPLAY}
                                        </a>
                                    )}
                                    <button className="xw-close" onClick={close} aria-label="Close" type="button">✕</button>
                                </div>
                            </div>
                            <div className="xw-progress">
                                {STEP_LABELS.map((label, i) => {
                                    const done2 = !!booked || i < step
                                    const cur = !booked && i === step
                                    const clickable = !booked && i < step
                                    return (
                                        <div key={label} className={"xw-seg" + (clickable ? " click" : "")} onClick={() => clickable && setStep(i as StepIdx)}>
                                            <div className="bar" style={{ background: done2 || cur ? T.progressGreen : "rgba(255,255,255,.18)" }} />
                                            <div className="lab" style={{ color: booked ? "rgba(255,255,255,.65)" : cur ? "#fff" : done2 ? "rgba(255,255,255,.65)" : "rgba(255,255,255,.45)" }}>
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
                            <a className="xw-mpill" href={`tel:${EMERGENCY_PHONE_TEL}`}>
                                <span className="dot" />
                                Emergency? Tap to call
                            </a>
                        </div>
                    )}

                    {/* ============ DONE ============ */}
                    {booked ? (
                        <div className="xw-done xw-fade">
                            <div className="xw-donecheck">✓</div>
                            {booked.status === "booked" ? (
                                <>
                                    <div className="xw-doneh">
                                        See you {booked.date ? fmtDay(booked.date, "long") : "soon"}
                                        {firstName.trim() ? `, ${firstName.trim()}` : ""}!
                                    </div>
                                    <div className="xw-donesub">
                                        {[svcSummary, booked.window ? `Arrival ${shortLabel(booked.window.label)}` : ""].filter(Boolean).join(" · ")}
                                    </div>
                                    {booked.address ? <div className="xw-donesub">{booked.address}</div> : null}
                                    {booked.jobNumber ? (
                                        <div className="xw-donejob">Job #{booked.jobNumber}</div>
                                    ) : null}
                                    <div className="xw-donesub">
                                        {booked.emailed
                                            ? `Confirmation sent to ${email.trim()}. `
                                            : ""}
                                        {typeof booked.fee === "number" && booked.fee > 0
                                            ? `Your technician will quote the ${money(booked.fee)} visit fee before any work begins.`
                                            : "There's no charge for this visit."}
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div className="xw-doneh">
                                        {booked.callback ? "We'll give you a call" : "We'll confirm your time shortly"}
                                        {firstName.trim() ? `, ${firstName.trim()}` : ""}
                                    </div>
                                    <div className="xw-donesub">
                                        {booked.callback
                                            ? `Someone from the office will call ${formatPhone(phoneDigits)}${data.callbackTime ? ` ${data.callbackTime.toLowerCase() === "anytime" ? "today" : "this " + data.callbackTime.toLowerCase()}` : ""}.`
                                            : `Your request is with our office. We'll confirm ${whenSummary || "your visit"} by text or phone at ${formatPhone(phoneDigits)}.`}
                                    </div>
                                </>
                            )}
                            <div className="xw-donebtns">
                                {booked.status === "booked" && booked.window ? (
                                    <button className="xw-outline" type="button" onClick={() => downloadICS(booked.window!, svcSummary, booked.address || "")}>
                                        Add to calendar
                                    </button>
                                ) : null}
                                <button className="xw-cta" onClick={close} type="button">Done</button>
                            </div>
                            <div className="xw-donefoot">
                                Need to change it? Call or text{" "}
                                <a href={`tel:${EMERGENCY_PHONE_TEL}`} style={{ color: T.red, fontWeight: 600, textDecoration: "none" }}>
                                    {EMERGENCY_PHONE_DISPLAY}
                                </a>
                            </div>
                        </div>
                    ) : (
                        <>
                            {/* ============ STEP 1: SERVICE ============ */}
                            {step === 0 && (
                                <div className="xw-fade" style={{ display: "grid", gap: 20 }}>
                                    <div className="xw-svcrow">
                                        {svcCards.map((c) => {
                                            const sel = data.service === c.key
                                            return (
                                                <button
                                                    key={c.key}
                                                    type="button"
                                                    className={"xw-svc" + (sel ? " sel" : "")}
                                                    onClick={() =>
                                                        patch({
                                                            service: c.key,
                                                            hvacIssue: undefined,
                                                            hvacDuration: undefined,
                                                            detail: undefined,
                                                            answers: {},
                                                            systemAge: undefined,
                                                            unitLocation: undefined,
                                                            window: null,
                                                            apptDate: undefined,
                                                            callbackTime: undefined,
                                                        })
                                                    }
                                                >
                                                    <span className="tile">{c.icon}</span>
                                                    <span className="nm">{c.name}</span>
                                                    <span className="sb">{c.sub}</span>
                                                </button>
                                            )
                                        })}
                                    </div>

                                    {data.service === "heatingCooling" && (
                                        <div className="xw-fade" style={{ display: "grid", gap: 18 }}>
                                            <div>
                                                {groupLabel("What's the issue?")}
                                                <div className="xw-chips">
                                                    {HVAC_ISSUES.map((o) => chip(data.hvacIssue === o, o, () => patch({ hvacIssue: data.hvacIssue === o ? undefined : o, window: null, apptDate: undefined })))}
                                                </div>
                                            </div>
                                            <div>
                                                {groupLabel("How long has it been happening?", true)}
                                                <div className="xw-chips">
                                                    {HVAC_DURATIONS.map((o) => chip(data.hvacDuration === o, o, () => toggle("hvacDuration", o)))}
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    {data.service && data.service !== "heatingCooling" && (
                                        <div className="xw-fade" style={{ display: "grid", gap: 18 }}>
                                            <div>
                                                {groupLabel("What do you need?")}
                                                <div className="xw-chips">
                                                    {SERVICE_OPTIONS[data.service].map((o) =>
                                                        chip(data.detail === o, o, () => patch({ detail: data.detail === o ? undefined : o, answers: {}, window: null, apptDate: undefined, callbackTime: undefined }))
                                                    )}
                                                </div>
                                            </div>
                                            {getSubQuestions(data.detail).map((q) => (
                                                <div key={q.id} className="xw-fade">
                                                    {groupLabel(q.label, q.optional)}
                                                    <div className="xw-chips">
                                                        {q.options.map((o) => chip(data.answers?.[q.id] === o, o, () => toggleAnswer(q.id, o), q.id + o))}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    {stepComplete[0] && (
                                        <div className="xw-micro">
                                            {isCallback
                                                ? "No visit needed for this one — next, tell us when to call."
                                                : avail.status === "loading" || avail.status === "idle"
                                                  ? "Checking our live schedule…"
                                                  : avail.status === "ok" && avail.first
                                                    ? `Next available: ${relDay(avail.first.date)}, ${shortLabel(avail.first.label)}. Next: pick your time.`
                                                    : "That's everything we need to route the right technician. Next: pick your time."}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ============ STEP 2: TIME ============ */}
                            {step === 1 && isCallback && (
                                <div className="xw-fade" style={{ display: "grid", gap: 20 }}>
                                    <div className="xw-notice">
                                        This doesn't need a visit — someone from the office will call you back.
                                    </div>
                                    <div>
                                        {groupLabel("When's a good time to call?")}
                                        <div className="xw-chips">
                                            {CALLBACK_TIMES.map((o) => chip(data.callbackTime === o, o, () => toggle("callbackTime", o)))}
                                        </div>
                                    </div>
                                </div>
                            )}
                            {step === 1 && !isCallback && (
                                <div className="xw-fade" style={{ display: "grid", gap: 20 }}>
                                    {(avail.status === "loading" || avail.status === "idle") && (
                                        <div className="xw-qp xw-skelwrap" aria-busy="true">
                                            <div className="qplabel">⚡ Checking our live schedule…</div>
                                            <div className="qprow">
                                                <span className="xw-skel" style={{ width: 150 }} />
                                                <span className="xw-skel" style={{ width: 160 }} />
                                                <span className="xw-skel" style={{ width: 140 }} />
                                            </div>
                                        </div>
                                    )}
                                    {avail.status === "unavailable" && (
                                        <div className="xw-notice warn">
                                            Our live schedule isn't loading right now. Pick a time that works and we'll confirm it by text or phone.
                                        </div>
                                    )}
                                    {avail.status === "no_capacity" && (
                                        <div className="xw-notice warn">
                                            Every online slot in the next two weeks is taken. Tell us what works and the office will find a way — or call {EMERGENCY_PHONE_DISPLAY} for the soonest visit.
                                        </div>
                                    )}
                                    {avail.status === "ok" && quickPicks.length > 0 && (
                                        isMobile ? (
                                            (() => {
                                                const qp = quickPicks[0]
                                                const sel = winSel(qp.date, qp.win)
                                                return (
                                                    <button className="xw-qpnext" type="button" onClick={() => pickWindow(qp.date, qp.win)}>
                                                        <span>
                                                            <span className="l1">⚡ Next available</span>
                                                            <span className="l2">{relDay(qp.date)} · {shortLabel(qp.win.label)}</span>
                                                        </span>
                                                        <span className={"pill" + (sel ? " on" : "")}>{sel ? "✓ Selected" : "Select"}</span>
                                                    </button>
                                                )
                                            })()
                                        ) : (
                                            <div className="xw-qp">
                                                <div className="qplabel">⚡ Next available</div>
                                                <div className="qprow">
                                                    {quickPicks.map((qp) => {
                                                        const sel = winSel(qp.date, qp.win)
                                                        const label = `${relDay(qp.date)} · ${shortLabel(qp.win.label)}`
                                                        return (
                                                            <button key={qp.date + qp.win.start} type="button" className={"xw-qpchip" + (sel ? " sel" : "")} onClick={() => pickWindow(qp.date, qp.win)}>
                                                                {sel ? "✓ " + label : label}
                                                            </button>
                                                        )
                                                    })}
                                                </div>
                                            </div>
                                        )
                                    )}

                                    {days.length > 0 && (
                                        <div className="xw-timecols">
                                            <div>
                                                {groupLabel(avail.status === "ok" ? "Or pick a day" : "Pick a day")}
                                                {isMobile ? (
                                                    <div className="xw-daystrip">
                                                        {days.slice(0, 10).map((d) => {
                                                            const sel = data.apptDate === d.date
                                                            const full = !d.windows.length
                                                            const dt = fromISO(d.date)
                                                            return (
                                                                <button
                                                                    key={d.date}
                                                                    type="button"
                                                                    className={"xw-stripday" + (sel ? " sel" : "") + (full ? " full" : "")}
                                                                    disabled={full}
                                                                    onClick={() => patch({ apptDate: d.date, window: null })}
                                                                >
                                                                    <span className="wd">{dt.toLocaleDateString("en-US", { weekday: "short" })}</span>
                                                                    <span className="dn">{dt.getDate()}</span>
                                                                    <span className="st">{full ? "Full" : d.date === todayISO() ? "Today" : dt.toLocaleDateString("en-US", { month: "short" })}</span>
                                                                </button>
                                                            )
                                                        })}
                                                    </div>
                                                ) : (
                                                    <WizardCalendar days={days} value={data.apptDate} onSelect={(iso) => patch({ apptDate: iso, window: null })} />
                                                )}
                                            </div>
                                            <div>
                                                {groupLabel(data.apptDate ? `Arrival window · ${relDay(data.apptDate)}` : "Arrival window")}
                                                {!data.apptDate ? (
                                                    <div className="xw-micro">Pick a day to see its arrival windows.</div>
                                                ) : (
                                                    <div style={{ display: "grid", gap: 9 }}>
                                                        {selectedDay?.windows.map((w) => {
                                                            const sel = winSel(selectedDay.date, w)
                                                            return (
                                                                <button key={w.start} type="button" className={"xw-window" + (sel ? " sel" : "")} onClick={() => pickWindow(selectedDay.date, w)}>
                                                                    <span>{sel ? "✓ " : ""}{shortLabel(w.label)}</span>
                                                                    <span className="fee">{feeTag(w)}</span>
                                                                </button>
                                                            )
                                                        })}
                                                        {selectedDay?.closed.map((label) => (
                                                            <button key={"c" + label} type="button" className="xw-window off" disabled>
                                                                <span>{shortLabel(label)}</span>
                                                                <span className="fee">Full</span>
                                                            </button>
                                                        ))}
                                                        {selectedDay && !selectedDay.windows.length && !selectedDay.closed.length && (
                                                            <div className="xw-micro">Nothing open this day.</div>
                                                        )}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                    {avail.status === "ok" && (
                                        <div className="xw-micro">
                                            Live from our dispatch board — what you pick here is held for you the moment you book.
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ============ STEP 3: DETAILS ============ */}
                            {step === 2 && (
                                <div className="xw-fade" style={{ display: "grid", gap: 22 }}>
                                    <div className="xw-proprow">
                                        <div>
                                            {groupLabel("Property type")}
                                            <div className="xw-chips">{["Residential", "Commercial"].map((o) => chip(data.propertyType === o, o, () => toggle("propertyType", o)))}</div>
                                        </div>
                                        <div>
                                            {groupLabel("You are the…")}
                                            <div className="xw-chips">{["Owner / Landlord", "Tenant"].map((o) => chip(data.occupant === o, o, () => toggle("occupant", o)))}</div>
                                        </div>
                                    </div>

                                    {ageQ.ask && (
                                        <div>
                                            {groupLabel(ageQ.label, true)}
                                            <div className="xw-chips">{AGE_OPTIONS.map((o) => chip(data.systemAge === o, o, () => toggle("systemAge", o)))}</div>
                                            <div className="xw-micro" style={{ marginTop: 8 }}>Helps us send a technician who knows your system's generation.</div>
                                        </div>
                                    )}

                                    {isHvacContext(data.service, data.detail) && (
                                        <div>
                                            {groupLabel("Where's the outdoor unit?", true)}
                                            <div className="xw-chips">{UNIT_LOCATIONS.map((o) => chip(data.unitLocation === o, o, () => toggle("unitLocation", o)))}</div>
                                        </div>
                                    )}

                                    {!isCallback && (
                                        <div>
                                            {groupLabel("Photos", true)}
                                            <input
                                                ref={photoInputRef}
                                                type="file"
                                                accept="image/*"
                                                multiple
                                                style={{ display: "none" }}
                                                onChange={(e) => {
                                                    const files = Array.from(e.target.files || [])
                                                    setPhotos((p) => [...p, ...files].slice(0, 3))
                                                    e.target.value = ""
                                                }}
                                            />
                                            <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
                                                {photoPreviews.map((p, i) => (
                                                    <div key={i} className="xw-thumb">
                                                        <img src={p.url} alt="" />
                                                        <button type="button" aria-label="Remove photo" onClick={() => setPhotos((ps) => ps.filter((_, j) => j !== i))}>×</button>
                                                    </div>
                                                ))}
                                                {photos.length < 3 && (
                                                    <button type="button" className="xw-upload" onClick={() => photoInputRef.current?.click()}>
                                                        + Add a photo of the problem
                                                    </button>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {!noteOpen ? (
                                        <button type="button" className="xw-noterow" onClick={() => setNoteOpen(true)}>
                                            <span className="plus">+</span>
                                            <span>
                                                <span className="nt">Add a note for the technician</span>
                                                <span className="ns">Gate codes, pets, where the unit is, anything useful</span>
                                            </span>
                                        </button>
                                    ) : (
                                        <div>
                                            {groupLabel("Note for the technician", true)}
                                            <textarea
                                                className="xw-input"
                                                rows={3}
                                                maxLength={600}
                                                value={note}
                                                onChange={(e) => setNote(e.target.value)}
                                                placeholder="Gate codes, pets, where the unit is, anything useful"
                                                style={{ resize: "vertical" }}
                                            />
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ============ STEP 4: CONFIRM ============ */}
                            {step === 3 && (
                                <div className="xw-fade xw-confcols">
                                    <div className="xw-c-form" style={{ display: "grid", gap: 14 }}>
                                        <div>
                                            {groupLabel("Mobile number")}
                                            <div style={{ position: "relative" }}>
                                                <input
                                                    className="xw-input"
                                                    inputMode="tel"
                                                    autoComplete="tel"
                                                    placeholder="937-555-0100"
                                                    value={formatPhone(phoneDigits)}
                                                    onChange={(e) => onPhoneChange(e.target.value)}
                                                />
                                                {lookup.status === "checking" && <span className="xw-inspin" aria-hidden="true" />}
                                            </div>
                                            {lookup.status === "checking" && <div className="xw-micro" style={{ marginTop: 6 }}>Checking if we've been out before…</div>}
                                            {lookup.status === "new" && <div className="xw-micro" style={{ marginTop: 6 }}>Looks like you're new here — welcome! Add your address below.</div>}
                                        </div>

                                        {lookup.status === "office" && !asNew && (
                                            <div className="xw-notice warn">
                                                We'd like to talk to you about this one — call{" "}
                                                <a href={`tel:${EMERGENCY_PHONE_TEL}`} style={{ color: T.red, fontWeight: 600 }}>{lookup.phone}</a>{" "}
                                                and we'll book it right away.
                                            </div>
                                        )}

                                        {lookup.status === "found" && !asNew && (
                                            <div className="xw-lookup xw-fade">
                                                <div className="xw-lkhead">
                                                    <span>Welcome back! Which address?</span>
                                                    {lookup.member && <span className="xw-memberchip">X-Plan member</span>}
                                                </div>
                                                <div style={{ display: "grid", gap: 8 }}>
                                                    {lookup.locations.map((l) => {
                                                        const sel = locKey === l.key
                                                        return (
                                                            <button key={l.key} type="button" className={"xw-loc" + (sel ? " sel" : "")} onClick={() => { setLocKey(l.key); setHouseError("") }}>
                                                                <span className="radio" aria-hidden="true" />
                                                                <span>
                                                                    <span className="st">{l.hasHouseNumber ? "•••• " : ""}{l.street}</span>
                                                                    <span className="ct">{[l.city, [l.state, l.zip].filter(Boolean).join(" ")].filter(Boolean).join(", ")}</span>
                                                                </span>
                                                            </button>
                                                        )
                                                    })}
                                                </div>
                                                {chosenLoc && chosenLoc.hasHouseNumber && (
                                                    <div className="xw-fade" style={{ marginTop: 12 }}>
                                                        {groupLabel("Confirm your house number")}
                                                        <input
                                                            className={"xw-input" + (houseError ? " err" : "")}
                                                            inputMode="numeric"
                                                            placeholder={`House number on ${chosenLoc.street}`}
                                                            value={houseNumber}
                                                            maxLength={8}
                                                            onChange={(e) => { setHouseNumber(e.target.value.replace(/[^0-9A-Za-z]/g, "")); setHouseError("") }}
                                                        />
                                                        {houseError && <div className="xw-fielderr">{houseError}</div>}
                                                        {!houseError && <div className="xw-micro" style={{ marginTop: 6 }}>Just so we know it's you.</div>}
                                                    </div>
                                                )}
                                                <button type="button" className="xw-linkbtn" onClick={() => { setAsNew(true); setLocKey(""); setHouseNumber("") }}>
                                                    Not you, or a different address? Book as a new address
                                                </button>
                                            </div>
                                        )}

                                        {(lookup.status === "unavailable") && (
                                            <div className="xw-micro">We couldn't check your number just now — no problem, add your address below.</div>
                                        )}

                                        <div className="xw-namerow">
                                            <div>
                                                {groupLabel("First name")}
                                                <input className="xw-input" autoComplete="given-name" placeholder="First name" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                                            </div>
                                            <div>
                                                {groupLabel("Last name")}
                                                <input className="xw-input" autoComplete="family-name" placeholder="Last name" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                                            </div>
                                        </div>

                                        {!knownCustomer && !blockedByOffice && (
                                            <>
                                                {asNew && lookup.status === "found" && (
                                                    <button type="button" className="xw-linkbtn" onClick={() => setAsNew(false)}>← Back to the addresses on file</button>
                                                )}
                                                <div style={{ position: "relative" }}>
                                                    {groupLabel("Service address")}
                                                    <input
                                                        className="xw-input"
                                                        autoComplete="off"
                                                        placeholder="Street address, City, OH ZIP"
                                                        value={addrLine}
                                                        onChange={(e) => onAddressChange(e.target.value)}
                                                        onFocus={() => addrSuggestions.length && setAddrOpen(true)}
                                                        onBlur={() => setTimeout(() => setAddrOpen(false), 160)}
                                                    />
                                                    {addrOpen && (addrLoading || addrSuggestions.length > 0) && (
                                                        <div className="xw-addrdrop">
                                                            {addrLoading && !addrSuggestions.length && <div className="ld">Searching…</div>}
                                                            {addrSuggestions.map((s) => (
                                                                <div key={s.id} className="it" onMouseDown={(e) => { e.preventDefault(); selectAddress(s) }}>{s.label}</div>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                                <div className="xw-addrgrid">
                                                    <div>
                                                        {groupLabel("Apt / unit", true)}
                                                        <input className="xw-input" placeholder="Apt 2B" value={unit} onChange={(e) => setUnit(e.target.value)} />
                                                    </div>
                                                    <div>
                                                        {groupLabel("City")}
                                                        <input className="xw-input" autoComplete="address-level2" placeholder="City" value={addrParts.city} onChange={(e) => setAddrParts((p) => ({ ...p, city: e.target.value }))} />
                                                    </div>
                                                    <div>
                                                        {groupLabel("ZIP")}
                                                        <input className="xw-input" inputMode="numeric" autoComplete="postal-code" placeholder="45400" maxLength={5} value={addrParts.zip} onChange={(e) => setAddrParts((p) => ({ ...p, zip: e.target.value.replace(/\D/g, "").slice(0, 5) }))} />
                                                    </div>
                                                </div>
                                            </>
                                        )}

                                        <div>
                                            {groupLabel("Email", true)}
                                            <input className={"xw-input" + (!emailOk ? " err" : "")} type="email" autoComplete="email" placeholder="For your confirmation" value={email} onChange={(e) => setEmail(e.target.value)} />
                                        </div>

                                        <div>
                                            {groupLabel("Preferred contact", true)}
                                            <div className="xw-chips">{(["Text", "Call", "Email"] as const).map((o) => chip(data.preferredContact === o, o, () => patch({ preferredContact: o })))}</div>
                                        </div>

                                        <div className="xw-sms">
                                            <button type="button" className="xw-sms-btn" aria-pressed={smsOk} onClick={() => setSmsOk((v) => !v)}>
                                                <span className={"box" + (smsOk ? " on" : "")}>{smsOk ? "✓" : ""}</span>
                                            </button>
                                            <p className="xw-sms-copy" onClick={() => setSmsOk((v) => !v)}>
                                                {SMS_CONSENT_TEXT.replace(" See our Privacy Policy and Terms.", " See our ")}
                                                <a href="https://www.extremeheating.com/privacy" target="_blank" rel="noopener" onClick={(e) => e.stopPropagation()}>Privacy Policy</a>
                                                {" and "}
                                                <a href="https://www.extremeheating.com/terms" target="_blank" rel="noopener" onClick={(e) => e.stopPropagation()}>Terms</a>.
                                            </p>
                                        </div>

                                        {submitError && <div className="xw-notice warn" role="alert">{submitError}</div>}
                                    </div>

                                    <div className="xw-c-summary xw-summary">
                                        <div className="sh">Your visit</div>
                                        <div className="row"><span>Service</span><b>{svcSummary || "—"}</b></div>
                                        <div className="row"><span>{isCallback ? "Call" : "When"}</span><b>{whenSummary || "—"}</b></div>
                                        {!isCallback && <div className="row"><span>Where</span><b>{whereSummary || "—"}</b></div>}
                                        {homeSummary && <div className="row"><span>Home</span><b>{homeSummary}</b></div>}
                                        {!isCallback && data.window?.requested && (
                                            <div className="xw-micro" style={{ marginTop: 8 }}>Requested time — the office will confirm it with you.</div>
                                        )}
                                        <div className="links">
                                            <button type="button" onClick={() => setStep(0)}>Change service</button>
                                            {!isCallback && <button type="button" onClick={() => setStep(1)}>Change time</button>}
                                        </div>
                                    </div>

                                    {!isCallback && (
                                        <div className={"xw-c-fee xw-fee" + (!feeRequired ? " xw-free" : "")}>
                                            <div className="fh">
                                                <span className="amt">{feeRequired ? money(fee) : isMember && svcFee === "tuneup" ? "Included" : "Free"}</span>
                                                <span className="lbl">{svcFee === "tuneup" ? "tune-up" : svcFee === "free" ? "estimate" : data.window?.afterHours ? "evening visit fee" : "visit fee"}</span>
                                            </div>
                                            <div className="fb">{feeCopyText}</div>
                                            {feeRequired && (
                                                <button type="button" className="fack" onClick={() => setFeeOk((v) => !v)}>
                                                    <span className={"box" + (feeOk ? " on" : "")}>{feeOk ? "✓" : ""}</span>
                                                    I understand the {money(fee)} {svcFee === "tuneup" ? "tune-up price" : "visit fee"}
                                                </button>
                                            )}
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
                        {step > 0 ? <button className="xw-back" onClick={goBack} type="button">← Back</button> : <span />}
                        <div className="xw-footright">
                            {hints[step] && <span className="xw-hint">{hints[step]}</span>}
                            {step === 3 ? (
                                <button className="xw-cta book" disabled={!canContinue || submitting} onClick={bookVisit} type="button">
                                    {submitting ? (
                                        <>
                                            <span className="xw-spin" /> {isCallback ? "Sending…" : "Booking…"}
                                        </>
                                    ) : isCallback ? "Request a call" : data.window?.requested ? "Request this time" : "Book my visit"}
                                </button>
                            ) : (
                                <button className="xw-cta" disabled={!canContinue} onClick={goNext} type="button">
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

/* The month view, drawn from the days the schedule returned: a day with an
 * open window is selectable, a full day says so, everything else is blank. */
function WizardCalendar({ days, value, onSelect }: { days: Day[]; value?: string; onSelect: (iso: string) => void }) {
    const byDate = React.useMemo(() => new Map(days.map((d) => [d.date, d])), [days])
    const first = days[0] ? fromISO(days[0].date) : new Date()
    const last = days.length ? fromISO(days[days.length - 1].date) : new Date()
    const minIdx = first.getFullYear() * 12 + first.getMonth()
    const maxIdx = last.getFullYear() * 12 + last.getMonth()

    const [view, setView] = React.useState({ y: first.getFullYear(), m: first.getMonth() })
    React.useEffect(() => {
        setView({ y: first.getFullYear(), m: first.getMonth() })
    }, [days.length && days[0].date]) // eslint-disable-line react-hooks/exhaustive-deps
    const viewIdx = view.y * 12 + view.m
    const canPrev = viewIdx > minIdx
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

    const monthLabel = new Date(view.y, view.m, 1).toLocaleDateString("en-US", { month: "long", year: "numeric" })
    const shift = (delta: number) =>
        setView((v) => {
            const i = v.y * 12 + v.m + delta
            return { y: Math.floor(i / 12), m: ((i % 12) + 12) % 12 }
        })

    return (
        <div className="xw-cal">
            <div className="ch">
                <button className="nav" type="button" disabled={!canPrev} onClick={() => canPrev && shift(-1)} aria-label="Previous month">‹</button>
                <div className="mo">{monthLabel}</div>
                <button className="nav" type="button" disabled={!canNext} onClick={() => canNext && shift(1)} aria-label="Next month">›</button>
            </div>
            <div className="wk">
                {["Mon", "Tue", "Wed", "Thu", "Fri"].map((d) => <div key={d}>{d}</div>)}
            </div>
            <div style={{ display: "grid", gap: 4 }}>
                {weeks.map((week, wi) => (
                    <div key={wi} className="row5">
                        {week.map((d, ci) => {
                            if (!d) return <div key={ci} />
                            const iso = toISO(d)
                            const row = byDate.get(iso)
                            const selectable = !!row && row.windows.length > 0
                            const full = !!row && !row.windows.length
                            const sel = iso === value
                            return (
                                <button
                                    key={ci}
                                    type="button"
                                    className={"day" + (sel ? " sel" : "") + (!selectable ? " off" : "") + (full ? " full" : "")}
                                    disabled={!selectable}
                                    onClick={() => onSelect(iso)}
                                    title={full ? "Full" : undefined}
                                >
                                    {d.getDate()}
                                    {selectable && !sel ? <span className="dot" /> : null}
                                </button>
                            )
                        })}
                    </div>
                ))}
            </div>
            <div className="xw-callegend"><span className="dot" /> open · <span className="fulltxt">grey</span> full</div>
        </div>
    )
}

const XW_CSS = `
.xw-root, .xw-root *{ box-sizing:border-box; font-family:${FONT} }

.xw-modal{
  position:relative; margin:40px auto; width:960px; max-width:calc(100vw - 24px);
  max-height:calc(100vh - 80px); background:#fff; border-radius:20px; overflow:hidden;
  box-shadow:0 24px 80px rgba(0,0,0,.45); display:flex; flex-direction:column;
  transition:opacity 220ms cubic-bezier(.2,.8,.2,1), transform 300ms cubic-bezier(.2,.8,.2,1);
}

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

.xw-mpillwrap{ display:flex; justify-content:center; margin-bottom:14px }
.xw-mpill{
  display:inline-flex; align-items:center; gap:6px; background:#FDF1F0; border-radius:999px;
  padding:6px 13px; font:600 11px ${FONT}; color:${T.red}; text-decoration:none;
}
.xw-mpill .dot{ width:7px; height:7px; border-radius:50%; background:${T.red} }

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

.xw-body{ padding:26px 28px 24px; overflow:auto; -webkit-overflow-scrolling:touch; overscroll-behavior:contain; flex:1 1 auto; min-height:0 }
.xw-glabel{ font:600 14px ${FONT}; color:${T.ink}; margin-bottom:10px }
.xw-glabel .opt{ font-weight:500; color:${T.muted} }
.xw-micro{ font:400 12px ${FONT}; color:${T.muted} }
.xw-chips{ display:flex; flex-wrap:wrap; gap:9px }

.xw-chip{
  border:1px solid ${T.border}; border-radius:999px; padding:9px 18px;
  font:500 13px ${FONT}; color:${T.ink}; background:#fff; cursor:pointer;
  transition:border-color .12s ease, background .12s ease;
}
.xw-chip:hover{ border-color:${T.dashed} }
.xw-chip.sel{ border:2px solid ${T.selGreen}; background:${T.tint}; padding:8px 17px; font-weight:600; color:${T.chipGreen} }

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

.xw-qp{ border:1px solid ${T.qpCard}; background:${T.tint}; border-radius:14px; padding:16px 18px }
.xw-qp .qplabel{ font:600 13px ${FONT}; color:${T.chipGreen}; margin-bottom:10px }
.xw-qp .qprow{ display:flex; flex-wrap:wrap; gap:9px }
.xw-qpchip{
  background:#fff; border:1px solid ${T.qpBorder}; border-radius:999px; padding:9px 18px;
  font:500 13px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-qpchip.sel{ border:2px solid ${T.selGreen}; padding:8px 17px; font-weight:600; color:${T.chipGreen} }
.xw-skelwrap .qplabel{ color:${T.muted} }
.xw-skel{ display:inline-block; height:36px; border-radius:999px; background:linear-gradient(90deg, #EEE9F3 25%, #F7F4FA 50%, #EEE9F3 75%); background-size:200% 100%; animation:xwshimmer 1.1s linear infinite }

.xw-notice{ border:1px solid ${T.qpCard}; background:${T.tint}; border-radius:12px; padding:12px 14px; font:500 13px/1.5 ${FONT}; color:${T.ink} }
.xw-notice.warn{ border-color:#F1D9A8; background:${T.amberBg}; color:${T.amber} }
.xw-notice.warn a{ color:${T.red} }

.xw-timecols{ display:grid; grid-template-columns:1.15fr 1fr; gap:28px; align-items:start }
.xw-timecols > div{ min-width:0 }
.xw-body > .xw-fade{ min-width:0; max-width:100% }

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
  position:relative; border:none; background:transparent; padding:9px 0 13px; text-align:center; border-radius:10px;
  font:500 13px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-cal .day:hover:not(:disabled){ background:${T.surface} }
.xw-cal .day.off{ color:${T.disabledDay}; cursor:default }
.xw-cal .day.full{ color:${T.muted}; text-decoration:line-through; opacity:.7 }
.xw-cal .day.sel{ background:${T.deepPurple}; color:#fff; font-weight:600 }
.xw-cal .day .dot{ position:absolute; left:50%; bottom:5px; width:5px; height:5px; margin-left:-2.5px; border-radius:50%; background:${T.selGreen} }
.xw-callegend{ margin-top:8px; font:400 11px ${FONT}; color:${T.muted}; display:flex; align-items:center; gap:5px }
.xw-callegend .dot{ width:6px; height:6px; border-radius:50%; background:${T.selGreen} }
.xw-callegend .fulltxt{ text-decoration:line-through }

.xw-daystrip{ display:flex; gap:7px; overflow-x:auto; padding-bottom:6px; -webkit-overflow-scrolling:touch; min-width:0; max-width:100% }
.xw-stripday{
  flex:0 0 calc(20% - 5.6px); border:1px solid ${T.border}; border-radius:12px; background:#fff;
  padding:9px 4px; display:grid; justify-items:center; gap:2px; cursor:pointer;
}
.xw-stripday .wd{ font:600 9.5px ${FONT}; letter-spacing:.06em; text-transform:uppercase; color:${T.muted} }
.xw-stripday .dn{ font:600 14px ${FONT}; color:${T.ink} }
.xw-stripday .st{ font:500 9px ${FONT}; color:${T.chipGreen} }
.xw-stripday.full{ opacity:.55; cursor:default }
.xw-stripday.full .st{ color:${T.muted} }
.xw-stripday.sel{ border:2px solid ${T.deepPurple}; background:${T.deepPurple}; padding:8px 3px }
.xw-stripday.sel .wd, .xw-stripday.sel .st{ color:rgba(255,255,255,.75) }
.xw-stripday.sel .dn{ color:#fff }

.xw-window{
  width:100%; display:flex; align-items:center; justify-content:space-between;
  border:1px solid ${T.border}; border-radius:12px; padding:13px 16px; background:#fff;
  font:500 13.5px ${FONT}; color:${T.ink}; cursor:pointer;
}
.xw-window:hover:not(:disabled){ border-color:${T.dashed} }
.xw-window .fee{ font:600 12px ${FONT}; color:${T.muted} }
.xw-window.sel{ border:2px solid ${T.selGreen}; background:${T.tint}; padding:12px 15px; font-weight:600; color:${T.chipGreen} }
.xw-window.sel .fee{ color:${T.chipGreen} }
.xw-window.off{ color:${T.disabledDay}; cursor:default; background:${T.surface2}; border-style:dashed }
.xw-window.off .fee{ color:${T.disabledDay} }

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

.xw-input{
  width:100%; border:1px solid ${T.border}; border-radius:11px; padding:13px 15px;
  font:400 13px ${FONT}; color:${T.ink}; background:#fff;
}
.xw-input::placeholder{ color:${T.placeholder} }
.xw-input:focus{ outline:2px solid ${T.selGreen}; outline-offset:0; border-color:transparent }
.xw-input.err{ border-color:${T.red} }
.xw-fielderr{ margin-top:6px; font:500 12px ${FONT}; color:${T.red} }
.xw-inspin{
  position:absolute; right:14px; top:50%; width:16px; height:16px; margin-top:-8px; border-radius:50%;
  border:2px solid ${T.border}; border-top-color:${T.selGreen}; animation:xwspin 800ms linear infinite;
}
.xw-addrgrid{ display:grid; grid-template-columns:1fr 1.4fr .9fr; gap:10px }

.xw-lookup{ border:1px solid ${T.qpCard}; background:${T.tint}; border-radius:14px; padding:14px 16px }
.xw-lkhead{ display:flex; align-items:center; justify-content:space-between; gap:10px; font:600 13.5px ${FONT}; color:${T.chipGreen}; margin-bottom:10px }
.xw-memberchip{ background:${T.deepPurple}; color:#fff; border-radius:999px; padding:4px 10px; font:600 10.5px ${FONT}; letter-spacing:.04em; text-transform:uppercase; white-space:nowrap }
.xw-loc{
  width:100%; display:flex; align-items:center; gap:12px; text-align:left; border:1px solid ${T.qpBorder};
  background:#fff; border-radius:12px; padding:11px 14px; cursor:pointer;
}
.xw-loc .radio{ width:18px; height:18px; border-radius:50%; border:2px solid ${T.dashed}; flex-shrink:0; display:grid; place-items:center }
.xw-loc.sel{ border:2px solid ${T.selGreen}; padding:10px 13px }
.xw-loc.sel .radio{ border-color:${T.selGreen} }
.xw-loc.sel .radio::after{ content:""; width:8px; height:8px; border-radius:50%; background:${T.selGreen} }
.xw-loc .st{ display:block; font:600 13.5px ${FONT}; color:${T.ink} }
.xw-loc .ct{ display:block; font:400 12px ${FONT}; color:${T.muted}; margin-top:1px }
.xw-linkbtn{ border:none; background:none; padding:8px 0 0; font:600 12px ${FONT}; color:${T.linkGreen}; cursor:pointer; text-align:left }

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
  padding:0; font:500 12px ${FONT}; color:${T.ink}; cursor:pointer; text-align:left;
}
.xw-fee .box{
  width:20px; height:20px; border-radius:6px; border:2px solid ${T.dashed}; display:grid;
  place-items:center; color:#fff; font-size:12px; flex-shrink:0;
}
.xw-fee .box.on{ background:${T.selGreen}; border-color:${T.selGreen} }
.xw-fee.xw-free{ border:1px solid ${T.qpCard}; background:${T.tint} }
.xw-fee.xw-free .amt{ color:${T.chipGreen} }

.xw-sms{ display:flex; align-items:flex-start; gap:9px; margin-top:4px }
.xw-sms-btn{ border:none; background:none; padding:0; margin:0; cursor:pointer; flex-shrink:0; line-height:0; margin-top:1px }
.xw-sms .box{
  width:20px; height:20px; border-radius:6px; border:2px solid ${T.dashed}; display:grid;
  place-items:center; color:#fff; font-size:12px; flex-shrink:0;
}
.xw-sms .box.on{ background:${T.selGreen}; border-color:${T.selGreen} }
.xw-sms-btn:focus-visible .box{ outline:2px solid ${T.deepPurple}; outline-offset:2px }
.xw-sms-copy{ font:400 11.5px/1.5 ${FONT}; color:${T.muted}; cursor:pointer; margin:0 }
.xw-sms-copy a{ color:${T.linkGreen}; text-decoration:underline }

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
  transition:filter .15s ease; white-space:nowrap;
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

.xw-done{ text-align:center; padding:26px 10px 12px; display:grid; justify-items:center; gap:10px }
.xw-donecheck{
  width:64px; height:64px; border-radius:999px; background:${T.tint}; border:2px solid ${T.selGreen};
  display:grid; place-items:center; font-size:26px; color:${T.chipGreen};
}
.xw-doneh{ font:600 22px ${FONT}; color:${T.ink} }
.xw-donesub{ font:400 13.5px ${FONT}; color:${T.muted}; max-width:520px }
.xw-donejob{ font:600 12px ${FONT}; letter-spacing:.08em; text-transform:uppercase; color:${T.chipGreen}; background:${T.tint}; border:1px solid ${T.qpCard}; border-radius:999px; padding:6px 14px }
.xw-donebtns{ display:flex; gap:12px; margin-top:8px; flex-wrap:wrap; justify-content:center }
.xw-donefoot{ font:400 12.5px ${FONT}; color:${T.muted}; margin-top:6px }

@keyframes xwspin{ to{ transform:rotate(360deg) } }
@keyframes xwfade{ from{ opacity:0; transform:translateY(6px) } to{ opacity:1; transform:none } }
@keyframes xwshimmer{ from{ background-position:200% 0 } to{ background-position:-200% 0 } }
.xw-fade{ animation:xwfade .18s ease both }
@media (prefers-reduced-motion:reduce){ .xw-fade, .xw-skel, .xw-spin, .xw-inspin{ animation:none } }

@media (max-width: 809px){
  .xw-modal{ margin:12px auto; max-width:calc(100vw - 16px); max-height:calc(100dvh - 24px); border-radius:20px }
  .xw-header{ padding:18px 20px 16px }
  .xw-eyebrow{ font-size:9.5px; letter-spacing:.2em }
  .xw-title{ font-size:21px; margin-top:4px }
  .xw-close{ width:28px; height:28px; font-size:13px }
  .xw-progress{ gap:6px; margin-top:14px; align-items:center }
  .xw-body{ padding:18px 20px 20px }
  .xw-svcrow{ display:grid; grid-template-columns:1fr 1fr; gap:10px }
  .xw-svc{ padding:15px 12px }
  .xw-svc.sel{ padding:14px 11px }
  .xw-svc .tile{ width:38px; height:38px; border-radius:11px }
  .xw-svc.sel .tile{ background:#fff; border:1px solid ${T.qpCard} }
  .xw-svc .nm{ font-size:13px }
  .xw-svc .sb{ display:none }
  .xw-chip{ padding:10px 15px; font-size:12.5px }
  .xw-chip.sel{ padding:9px 14px; font-size:12.5px }
  .xw-glabel{ font-size:13.5px }
  .xw-timecols{ grid-template-columns:1fr; gap:16px }
  .xw-window{ padding:13px 15px; font-size:13px }
  .xw-window.sel{ padding:12px 14px }
  .xw-proprow{ grid-template-columns:1fr; gap:16px }
  .xw-addrgrid{ grid-template-columns:1fr 1fr }
  .xw-addrgrid > div:first-child{ grid-column:1 / -1 }
  .xw-confcols{ grid-template-columns:1fr; grid-template-areas:"summary" "form" "fee"; gap:14px }
  .xw-namerow{ gap:9px }
  .xw-summary{ padding:14px 16px }
  .xw-summary .links{ margin-top:8px }
  .xw-fee{ padding:14px 16px }
  .xw-fee .amt{ font-size:19px }
  /* 16px stops iOS focus-zoom; don't go smaller. */
  .xw-input{ font-size:16px; padding:13px 14px }
  .xw-footer{ padding:14px 20px calc(18px + env(safe-area-inset-bottom)) }
  .xw-footright{ flex:1; display:flex }
  .xw-hint{ display:none }
  .xw-cta, .xw-cta.book{ flex:1; min-width:0; padding:15px 0 }
  .xw-back{ padding:0 8px; font-size:13px }
  .xw-donebtns{ width:100%; flex-direction:column }
  .xw-donebtns .xw-cta, .xw-donebtns .xw-outline{ width:100% }
}
`
