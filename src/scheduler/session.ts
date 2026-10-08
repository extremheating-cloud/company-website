/* Session reporting for the Schedule Service wizard.
 *
 * Each open of the dialog is one session. The wizard reports the steps the
 * visitor reaches, the facts they settle and how they leave, so the office
 * can see every booking and every abandoned session with the step it was
 * closed on (FollowUp Pro's schedulerSession merges each event into
 * webSchedulerActivity/{sessionId}).
 *
 * Everything here is fire and forget: a report that fails is never shown and
 * never slows or blocks the visitor, so every send swallows its own errors. */

// The wizard's progress bar draws these same labels, so they live here once.
export const STEP_LABELS = ["YOU", "SERVICE", "TIME", "CONFIRM"] as const
export type StepLabel = (typeof STEP_LABELS)[number]

export type SessionEvent = "open" | "step" | "field" | "close" | "unload" | "booked"
export type ClosedWith = "x" | "escape" | "backdrop" | "navigation" | "unload"
export type LookupStatus = "found" | "new" | "office" | "invalid" | "unavailable" | "out_of_area"

export type SessionData = {
    phone?: string
    zip?: string
    propertyType?: "home" | "business"
    lookupStatus?: LookupStatus
    locationKey?: string
    firstName?: string
    lastName?: string
    email?: string
    service?: string
    serviceLabel?: string
    systemAge?: string
    window?: { date: string; label: string; start: string }
    closedWith?: ClosedWith
    jobNumber?: string
}

export type SessionBody = {
    sessionId: string
    event: SessionEvent
    step: number
    stepLabel: StepLabel
    at: number
    page: string
    data: SessionData
}

const ID_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
const ID_LENGTH = 24

// 64 symbols, so the low six bits of a random byte pick one without bias.
export function newSessionId(): string {
    let bytes: Uint8Array | null = null
    try {
        const c = (globalThis as any).crypto
        if (c && typeof c.getRandomValues === "function") bytes = c.getRandomValues(new Uint8Array(ID_LENGTH))
    } catch {
        bytes = null
    }
    let out = ""
    for (let i = 0; i < ID_LENGTH; i++) {
        const n = bytes ? bytes[i] : Math.floor(Math.random() * 256)
        out += ID_ALPHABET[n & 63]
    }
    return out
}

type Session = { id: string; url: string; settled: boolean }
let current: Session | null = null

/* A new session for a new open. The base is the wizard's own API base, so a
 * test page that points the scheduler elsewhere points the reports there too. */
export function startSession(apiBase: string): string {
    current = { id: newSessionId(), url: String(apiBase).replace(/\/+$/, "") + "/schedulerSession", settled: false }
    return current.id
}

export function currentSessionId(): string | undefined {
    return current ? current.id : undefined
}

/* The server already holds the outcome once a booking, a callback or an
 * out-of-area answer comes back, so a later close is not an abandonment and
 * is not reported. */
export function settleSession(): void {
    if (current) current.settled = true
}

export function endSession(): void {
    current = null
}

const LOOKUP_STATUSES = new Set(["found", "new", "office", "invalid", "unavailable", "out_of_area"])
const CLOSED_WITH = new Set(["x", "escape", "backdrop", "navigation", "unload"])

function text(v: unknown, max: number): string | undefined {
    if (v === undefined || v === null) return undefined
    const s = String(v).trim().slice(0, max)
    return s ? s : undefined
}

/* Only the keys the contract names, each in its own shape; the server drops
 * anything else anyway, so sending less keeps the beacon small. */
export function cleanData(d?: SessionData | null): SessionData {
    const out: SessionData = {}
    if (!d || typeof d !== "object") return out
    const phone = String(d.phone ?? "").replace(/\D/g, "")
    if (phone.length === 10) out.phone = phone
    const zip = String(d.zip ?? "").replace(/\D/g, "")
    if (zip.length === 5) out.zip = zip
    if (d.propertyType === "home" || d.propertyType === "business") out.propertyType = d.propertyType
    if (d.lookupStatus && LOOKUP_STATUSES.has(d.lookupStatus)) out.lookupStatus = d.lookupStatus
    const loc = text(d.locationKey, 200)
    if (loc) out.locationKey = loc
    const first = text(d.firstName, 60)
    if (first) out.firstName = first
    const last = text(d.lastName, 60)
    if (last) out.lastName = last
    const email = text(d.email, 120)
    if (email) out.email = email
    const service = text(d.service, 80)
    if (service) out.service = service
    const serviceLabel = text(d.serviceLabel, 120)
    if (serviceLabel) out.serviceLabel = serviceLabel
    const age = text(d.systemAge, 40)
    if (age) out.systemAge = age
    if (d.window && typeof d.window === "object") {
        const w = { date: text(d.window.date, 10) || "", label: text(d.window.label, 40) || "", start: text(d.window.start, 40) || "" }
        if (w.date || w.label || w.start) out.window = w
    }
    if (d.closedWith && CLOSED_WITH.has(d.closedWith)) out.closedWith = d.closedWith
    const job = text(d.jobNumber, 40)
    if (job) out.jobNumber = job
    return out
}

function pageNow(): string {
    try {
        const l = (globalThis as any).location
        if (!l) return ""
        return (String(l.pathname || "") + String(l.search || "")).slice(0, 200)
    } catch {
        return ""
    }
}

export function buildBody(sessionId: string, event: SessionEvent, step: number, data?: SessionData | null): SessionBody {
    const s = Math.min(3, Math.max(0, Math.floor(Number(step) || 0)))
    return { sessionId, event, step: s, stepLabel: STEP_LABELS[s], at: Date.now(), page: pageNow(), data: cleanData(data) }
}

/* sendBeacon with a text/plain Blob first: no preflight, and it survives the
 * page going away. fetch with keepalive is the fallback, except for "unload",
 * which by contract goes by beacon only. Returns whether a send was handed to
 * the browser, which is all a caller can know; nothing waits on it. */
export function sendEvent(event: SessionEvent, step: number, data?: SessionData | null): boolean {
    const s = current
    if (!s) return false
    if (s.settled && (event === "close" || event === "unload")) return false
    let json: string
    try {
        json = JSON.stringify(buildBody(s.id, event, step, data))
    } catch {
        return false
    }
    try {
        const nav = (globalThis as any).navigator
        if (nav && typeof nav.sendBeacon === "function" && nav.sendBeacon(s.url, new Blob([json], { type: "text/plain" }))) return true
    } catch {
        // a refused or throwing beacon falls through to fetch
    }
    if (event === "unload") return false
    try {
        const f = (globalThis as any).fetch
        if (typeof f !== "function") return false
        const p = f(s.url, { method: "POST", body: json, headers: { "Content-Type": "text/plain" }, keepalive: true, credentials: "omit" })
        if (p && typeof p.catch === "function") p.catch(() => {})
        return true
    } catch {
        return false
    }
}
