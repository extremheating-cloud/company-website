import * as React from "react"
import { createRoot } from "react-dom/client"
import ContactFlowDialog from "./ContactFlowDialog"

const HOST_ID = "xh-schedule-root"

function open() {
    window.dispatchEvent(new CustomEvent("open-contact-dialog"))
}

function Boot() {
    React.useEffect(() => {
        const w = window as any
        w.XHSchedule = { open }
        // Replays a click queued before load; safe here because the child dialog's effect already attached its listener.
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
