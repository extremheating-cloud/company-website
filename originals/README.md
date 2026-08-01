# Originals

Unedited source files for images that appear on the site in a modified form. The
folder structure mirrors `assets/`, so the original of any derived file is at the
same path.

**Nothing here is served.** It sits outside `assets/` on purpose — it should never be
referenced by a page or fetched over the CDN. These are here so a crop can be redone
without a reshoot.

| Original | Derived | What changed |
| --- | --- | --- |
| `team/*.jpg` | `assets/team/*.jpg` | Full-body frames cropped to head-and-shoulders at matching framing. The About page runs four across, and mismatched crops are the first thing you notice. |
| `brands/*.png` | `assets/brands/*.png` | Transparent padding trimmed off each canvas. Daikin's was a 3840×2160 frame with the mark floating in it, which would have rendered far smaller than the others under `object-fit: contain`. |
| `equipment/ruud-install.jpg` | `assets/equipment/ruud-install.jpg` | Cropped at the cabinet edge to remove a competitor's service sticker — "Jan AC & Heat Services", phone number and all — from the right of the frame. |

**Do not publish `equipment/ruud-install.jpg`.** It is kept only as the source for
the crop. The cropped version in `assets/` is the one that goes on pages.

Images that were used unmodified aren't duplicated here — `assets/` already holds
the original bytes. That is the case for the Trane and GE water heater install
photos.
