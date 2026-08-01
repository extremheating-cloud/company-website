import type { Override } from "framer"

if (typeof window !== "undefined") {
    ;(window as any).OpenContactDialog = openContactDialog

    window.addEventListener("message", (event) => {
        if (event?.data?.type === "XHAC_OPEN_CONTACT_DIALOG") {
            openContactDialog()
        }
    })
}

if (typeof window !== "undefined") {
    const w = window as any

    if (!w.__xhacScheduleBridgeInit) {
        w.__xhacScheduleBridgeInit = true

        const onCustomEventCapture = () => {
            // Allow the original schedule engine to handle this event normally
        }

        const onMessageCapture = (event: MessageEvent) => {
            try {
                if (!event?.data || event.data.type !== "open-contact-dialog")
                    return
                // Allow the original schedule engine to handle this message normally
            } catch {}
        }

        window.addEventListener(
            "open-contact-dialog",
            onCustomEventCapture as EventListener,
            true
        )
        window.addEventListener(
            "message",
            onMessageCapture as EventListener,
            true
        )
    }
}

export function openContactDialog(): Override {
    return {
        onClick() {
            window.dispatchEvent(new CustomEvent("open-contact-dialog"))
        },
        onTap() {
            window.dispatchEvent(new CustomEvent("open-contact-dialog"))
        },
    }
}
