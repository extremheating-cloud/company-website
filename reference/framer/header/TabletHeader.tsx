import * as React from "react"
import { addPropertyControls, ControlType } from "framer"
import DesktopHeader from "https://framer.com/m/DesktopHeader-hFmeRV.js@6DqbibpVzy8mnOapthhU"

type Props = {
    headerOffset?: number
    solid?: boolean
}

function TabletHeader({
    headerOffset = 84,
    solid = false,
}: Props) {
    return (
        <div className="xhac-tabwrap">
            <style>{CSS}</style>
            <DesktopHeader
                headerOffset={headerOffset}
                solid={solid}
            />
        </div>
    )
}

const CSS = `

.xhac-tabwrap .xhac-bar{ padding:16px 24px; gap:14px }
.xhac-tabwrap .xhac-logo{ height:42px }
.xhac-tabwrap .xhac-nav-strip{ gap:15px; padding:0 4px }
.xhac-tabwrap .xhac-nav-link{ font-size:13.5px; padding:14px 1px; gap:4px }
.xhac-tabwrap .xhac-nav-link .bar{ bottom:-16px }
.xhac-tabwrap .xhac-bar-right{ gap:12px }

.xhac-tabwrap .xhac-phone{ display:none }
.xhac-tabwrap .xhac-phone-icon{ display:flex }
.xhac-tabwrap .xhac-cta{ font-size:13.5px; padding:11px 15px }

.xhac-tabwrap .xm-grid{ grid-template-columns:1.1fr 1fr; gap:28px; padding:24px 24px 28px }
.xhac-tabwrap .xm-grid.locations{ grid-template-columns:1.1fr 1fr }
.xhac-tabwrap .xm-aside{ grid-column:1 / -1; flex-direction:row }
.xhac-tabwrap .xm-aside .xm-promo{ flex:1 }
`

addPropertyControls(TabletHeader as any, {
    solid: {
        type: ControlType.Boolean,
        title: "Solid Purple",
        defaultValue: false,
    },
})

export default TabletHeader
