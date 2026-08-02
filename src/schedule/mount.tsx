/* Self-hosted entry point for the schedule wizard.
 *
 * On Framer the dialog was mounted by the page itself and OpenContactDialog.tsx was
 * the override that fired the event. Off Framer nothing mounts it, so every Schedule
 * button was dispatching `open-contact-dialog` into an empty room. This file is the
 * missing half: it creates a host node, renders the dialog into it, and only then
 * tells the page the dialog is listening.
 *
 * ContactFlowDialog registers its own window listener, so there is nothing to wire
 * up here beyond ordering. Child effects run before parent effects, so by the time
 * Boot's effect fires the dialog's listener is already attached — that is what makes
 * it safe to replay a click that happened while this bundle was still downloading.
 *
 * Build: npm run build:schedule  (writes assets/js/schedule.js)
 */
import * as React from "react"
import { createRoot } from "react-dom/client"
import ContactFlowDialog from "../../framer/schedule/ContactFlowDialog"

const HOST_ID = "xh-schedule-root"

function open() {
    window.dispatchEvent(new CustomEvent("open-contact-dialog"))
}

function Boot() {
    React.useEffect(() => {
        const w = window as any
        w.XHSchedule = { open }
        // A click that arrived before the bundle finished loading is queued by the
        // loader in chrome.py rather than dropped.
        if (w.__xhScheduleWanted) {
            w.__xhScheduleWanted = false
            open()
        }
    }, [])
    return <ContactFlowDialog />
}

function mount() {
    if (document.getElementById(HOST_ID)) return
    const host = document.createElement("div")
    host.id = HOST_ID
    document.body.appendChild(host)
    createRoot(host).render(<Boot />)
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true })
} else {
    mount()
}
