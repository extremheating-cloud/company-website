// Tests for session.ts, the wizard's session reporting. They run the real
// module: esbuild (the compiler that builds the bundle) turns it into a temp
// file, and every body is read back from the Blob or the fetch body through
// JSON.parse, the way the server reads it. The browser pieces the module
// touches (navigator.sendBeacon, fetch, location) are stubbed per test.
import { test, beforeEach, after } from "node:test"
import assert from "node:assert/strict"
import { createRequire } from "node:module"
import { mkdtempSync, rmSync } from "node:fs"
import { tmpdir } from "node:os"
import path from "node:path"
import { fileURLToPath, pathToFileURL } from "node:url"

const require = createRequire(import.meta.url)
const esbuild = require("esbuild")

const here = path.dirname(fileURLToPath(import.meta.url))
const dir = mkdtempSync(path.join(tmpdir(), "xh-session-"))
const outfile = path.join(dir, "session.mjs")
await esbuild.build({
    entryPoints: [path.join(here, "..", "session.ts")],
    outfile,
    bundle: true,
    format: "esm",
    platform: "neutral",
    target: "es2018",
    logLevel: "silent",
})
const S = await import(pathToFileURL(outfile).href)
after(() => rmSync(dir, { recursive: true, force: true }))

const API = "https://us-central1-followup-pro-37ed6.cloudfunctions.net"
const ENDPOINT = API + "/schedulerSession"
const BODY_KEYS = ["at", "data", "event", "page", "sessionId", "step", "stepLabel"]
// The server's own check on a session id.
const SERVER_ID = /^[A-Za-z0-9_-]{16,64}$/

function setGlobal(name, value) {
    Object.defineProperty(globalThis, name, { value, configurable: true, writable: true })
}

/* beacon: "ok" (queued), "refused" (sendBeacon returns false), "throws", or
 * "missing" (no sendBeacon at all). fetchImpl replaces the fetch answer. */
function browser({ beacon = "ok", fetchImpl, pathname = "/furnace-repair", search = "?gclid=test" } = {}) {
    const sent = { beacons: [], fetches: [] }
    const nav = {}
    if (beacon !== "missing") {
        nav.sendBeacon = (url, blob) => {
            sent.beacons.push({ url, blob })
            if (beacon === "throws") throw new Error("beacon blew up")
            return beacon === "ok"
        }
    }
    setGlobal("navigator", nav)
    setGlobal("fetch", (url, init) => {
        sent.fetches.push({ url, init })
        return fetchImpl ? fetchImpl() : Promise.resolve({ ok: true, status: 204 })
    })
    setGlobal("location", { pathname, search })
    return sent
}

async function beaconBody(entry) {
    return JSON.parse(await entry.blob.text())
}

beforeEach(() => S.endSession())

test("a session id is 24 characters the server accepts, and each open gets a new one", () => {
    browser()
    const a = S.startSession(API)
    const b = S.startSession(API)
    assert.match(a, /^[A-Za-z0-9_-]{24}$/)
    assert.match(b, /^[A-Za-z0-9_-]{24}$/)
    assert.match(a, SERVER_ID)
    assert.notEqual(a, b)
    assert.equal(S.currentSessionId(), b)
})

test("without crypto the id still comes out right, from Math.random", () => {
    const saved = Object.getOwnPropertyDescriptor(globalThis, "crypto")
    setGlobal("crypto", undefined)
    try {
        for (let i = 0; i < 50; i++) assert.match(S.newSessionId(), /^[A-Za-z0-9_-]{24}$/)
    } finally {
        Object.defineProperty(globalThis, "crypto", saved)
    }
})

test("the body has exactly the contract's keys, by beacon as text/plain", async () => {
    const sent = browser()
    const id = S.startSession(API)
    const before = Date.now()
    const ok = S.sendEvent("field", 0, { phone: "937-555-0110", zip: "45459", propertyType: "home" })
    assert.equal(ok, true)
    assert.equal(sent.fetches.length, 0)
    assert.equal(sent.beacons.length, 1)
    assert.equal(sent.beacons[0].url, ENDPOINT)
    assert.equal(sent.beacons[0].blob.type, "text/plain")
    const body = await beaconBody(sent.beacons[0])
    assert.deepEqual(Object.keys(body).sort(), BODY_KEYS)
    assert.equal(body.sessionId, id)
    assert.equal(body.event, "field")
    assert.equal(body.step, 0)
    assert.equal(body.stepLabel, "YOU")
    assert.ok(body.at >= before && body.at <= Date.now())
    assert.equal(body.page, "/furnace-repair?gclid=test")
    assert.deepEqual(body.data, { phone: "9375550110", zip: "45459", propertyType: "home" })
})

test("data keeps only the contract's keys, each in its own shape and length", async () => {
    const sent = browser()
    S.startSession(API)
    S.sendEvent("field", 0, {
        firstName: "  Owen  ",
        lastName: "T".repeat(80),
        email: "o".repeat(130) + "@example.com",
        lookupStatus: "new",
        propertyType: "Residential", // the wizard's own word, not the contract's: dropped
        customerName: "Learned From Lookup", // never part of the contract: dropped
        phone: "55501", // not ten digits: dropped
        zip: "4545", // not five digits: dropped
    })
    const body = await beaconBody(sent.beacons[0])
    assert.deepEqual(body.data, {
        firstName: "Owen",
        lastName: "T".repeat(60),
        email: "o".repeat(120),
        lookupStatus: "new",
    })
})

test("every step carries its label, and a step outside 0..3 is held to the ends", async () => {
    const sent = browser()
    S.startSession(API)
    for (const step of [0, 1, 2, 3, 7, -1]) S.sendEvent("step", step)
    const bodies = await Promise.all(sent.beacons.map(beaconBody))
    assert.deepEqual(bodies.map((b) => [b.step, b.stepLabel]), [
        [0, "YOU"], [1, "SERVICE"], [2, "TIME"], [3, "CONFIRM"], [3, "CONFIRM"], [0, "YOU"],
    ])
    assert.deepEqual(bodies[0].data, {})
})

// The wizard's own age and window labels use an en dash ("10\u201315 years",
// "8am\u201312pm"); written as escapes so this file holds none.
test("service, window, close and booked bodies", async () => {
    const sent = browser()
    S.startSession(API)
    S.sendEvent("field", 1, { service: "hvac:no_heat", serviceLabel: "Heating & Cooling · No Heat", systemAge: "10\u201315 years" })
    S.sendEvent("field", 2, { window: { date: "2026-10-09", label: "8am\u201312pm", start: "2026-10-09T12:00:00.000Z" } })
    S.sendEvent("close", 2, { closedWith: "backdrop" })
    S.sendEvent("booked", 3, { jobNumber: 12345 })
    const [svc, win, close, booked] = await Promise.all(sent.beacons.map(beaconBody))
    assert.deepEqual(svc.data, { service: "hvac:no_heat", serviceLabel: "Heating & Cooling · No Heat", systemAge: "10\u201315 years" })
    assert.deepEqual(win.data, { window: { date: "2026-10-09", label: "8am\u201312pm", start: "2026-10-09T12:00:00.000Z" } })
    assert.equal(close.event, "close")
    assert.equal(close.stepLabel, "TIME")
    assert.deepEqual(close.data, { closedWith: "backdrop" })
    assert.equal(booked.event, "booked")
    assert.deepEqual(booked.data, { jobNumber: "12345" })
})

test("the page is the path and query, at most 200 characters", async () => {
    const sent = browser({ pathname: "/schedule", search: "?q=" + "x".repeat(400) })
    S.startSession(API)
    S.sendEvent("open", 0)
    const body = await beaconBody(sent.beacons[0])
    assert.equal(body.page.length, 200)
    assert.ok(body.page.startsWith("/schedule?q=xxx"))
})

test("a refused beacon falls back to fetch with keepalive and the same body", async () => {
    const sent = browser({ beacon: "refused" })
    const id = S.startSession(API)
    assert.equal(S.sendEvent("step", 1), true)
    assert.equal(sent.beacons.length, 1)
    assert.equal(sent.fetches.length, 1)
    const { url, init } = sent.fetches[0]
    assert.equal(url, ENDPOINT)
    assert.equal(init.method, "POST")
    assert.equal(init.keepalive, true)
    assert.equal(init.headers["Content-Type"], "text/plain")
    const body = JSON.parse(init.body)
    assert.deepEqual(Object.keys(body).sort(), BODY_KEYS)
    assert.equal(body.sessionId, id)
    assert.equal(body.stepLabel, "SERVICE")
})

test("no sendBeacon, or one that throws, also falls back to fetch", () => {
    for (const beacon of ["missing", "throws"]) {
        const sent = browser({ beacon })
        S.startSession(API)
        assert.equal(S.sendEvent("open", 0), true, beacon)
        assert.equal(sent.fetches.length, 1, beacon)
        assert.equal(sent.fetches[0].init.keepalive, true, beacon)
    }
})

test("a failing fetch is swallowed: no throw, no unhandled rejection", async () => {
    let unhandled = null
    const onUnhandled = (err) => { unhandled = err }
    process.on("unhandledRejection", onUnhandled)
    try {
        browser({ beacon: "refused", fetchImpl: () => Promise.reject(new Error("offline")) })
        S.startSession(API)
        assert.equal(S.sendEvent("step", 2), true)
        browser({ beacon: "refused", fetchImpl: () => { throw new Error("blocked") } })
        S.startSession(API)
        assert.equal(S.sendEvent("step", 2), false)
        browser({ beacon: "throws", fetchImpl: () => { throw new Error("blocked") } })
        S.startSession(API)
        assert.doesNotThrow(() => S.sendEvent("close", 1, { closedWith: "x" }))
        await new Promise((r) => setTimeout(r, 20))
        assert.equal(unhandled, null)
    } finally {
        process.off("unhandledRejection", onUnhandled)
    }
})

test("unload goes by beacon only: a refused beacon is not retried by fetch", async () => {
    const sent = browser({ beacon: "refused" })
    S.startSession(API)
    assert.equal(S.sendEvent("unload", 2, { closedWith: "unload" }), false)
    assert.equal(sent.beacons.length, 1)
    assert.equal(sent.fetches.length, 0)
    const body = await beaconBody(sent.beacons[0])
    assert.equal(body.event, "unload")
    assert.deepEqual(body.data, { closedWith: "unload" })
})

test("with no session nothing is sent at all", () => {
    const sent = browser()
    assert.equal(S.currentSessionId(), undefined)
    for (const ev of ["open", "step", "field", "close", "unload", "booked"]) assert.equal(S.sendEvent(ev, 0, { zip: "45459" }), false)
    S.startSession(API)
    S.endSession()
    assert.equal(S.sendEvent("close", 1, { closedWith: "x" }), false)
    assert.equal(sent.beacons.length, 0)
    assert.equal(sent.fetches.length, 0)
})

test("after a booking or a callback answer, close and unload are dropped but the rest still goes", async () => {
    const sent = browser()
    S.startSession(API)
    S.settleSession()
    assert.equal(S.sendEvent("close", 3, { closedWith: "x" }), false)
    assert.equal(S.sendEvent("unload", 3, { closedWith: "unload" }), false)
    assert.equal(S.sendEvent("booked", 3, { jobNumber: "778899" }), true)
    assert.equal(sent.beacons.length, 1)
    assert.equal((await beaconBody(sent.beacons[0])).event, "booked")
    // A new open is a new session, not settled.
    S.startSession(API)
    assert.equal(S.sendEvent("close", 0, { closedWith: "x" }), true)
})
