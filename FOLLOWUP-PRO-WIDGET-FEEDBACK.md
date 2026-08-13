# Chat widget: bugs and design requests

From: Extreme Heating, Air, Plumbing (extremeheating.com)
Widget: `chat-widget.js` from `followup-pro-37ed6.web.app`, custom element `<extreme-chat>`
Date: 2026-08-12

We are integrating the chat widget as opt-in path 2 in our A2P 10DLC registration, so it
runs on every page of the site. In getting it to sit correctly on mobile we found a few
real bugs and a set of design differences we would like resolved upstream.

Right now we are patching all of this from our own page by appending a stylesheet to the
widget's open shadow root. That works, but it is fragile: it breaks silently the moment
you rename an internal class, and it means every one of your customers who wants the
widget to match their site has to do the same thing. We would rather delete our patch.

Everything below was measured in a browser at a 390px viewport, `devicePixelRatio` 2,
against the build live on 2026-08-12.

---

## 1. The consent disclosure renders at the wrong size and color

**Priority: high. This one is compliance-adjacent.**

Your stylesheet asks for the consent paragraph to be fine print:

```css
.fine { margin:0 0 12px; font-size:12px; font-weight:400; line-height:1.45; color:var(--exc-slate); }
```

It never gets it. The element is `<p class="fine" id="exc-consent">` inside `.card`, and
this rule also matches:

```css
.card p { margin:0 0 12px; font-size:14px; font-weight:400; line-height:1.5; color:var(--exc-ink); }
```

`.card p` has specificity (0,1,1). `.fine` has (0,1,0). `.card p` wins regardless of source
order, so the disclosure renders at **14px in full ink `#0F172A`**, identical to body copy.

Measured consequence at 390px: the consent block is **147px tall**, which is the single
largest element in the gate form and about 23% of the card's height. It reads as the main
content of the form rather than as a disclosure attached to the Send button.

**Fix:** raise the specificity so your own intent applies.

```css
.card p.fine { font-size:12px; line-height:1.45; color:var(--exc-slate); }
```

**One request on top of the fix.** We are currently rendering it at 12.5px rather than
your 12px. A carrier reviewer looks at this disclosure when approving the campaign, and a
disclosure they have to squint at is a different category of problem from one that is
merely large. Somewhere in the 12px to 13px range with `--exc-slate` is right. Please do
not go below 12px, and please keep the Privacy Policy and Terms links underlined and in
brand purple rather than inheriting slate. `#64748B` on white is 4.76:1, which clears
WCAG AA for normal text, so the token itself is fine.

---

## 2. The consent line spells our company name differently from the rest of the widget

**Priority: high. This one is a compliance issue, not a style preference.**

The widget header renders our name correctly:

> Extreme Heating, Air, Plumbing

The consent disclosure inside the gate form does not:

> By sending this you agree Extreme Heating, Air **&** Plumbing may text you about your
> request at the number above.

Our trading name uses a comma, not an ampersand. The header appears to take the name from
our tenant configuration while the consent template has it separately, so the two have
drifted.

**Fix:** the consent template should use the same tenant name field the header uses, so
this cannot drift again for us or for anyone else.

Please tell us when this ships. That disclosure text is quoted character for character in
our A2P 10DLC campaign registration as the stored TCPA record, so our registration text has
to be updated in the same window as your change. We do not want the site and the
registration disagreeing on any character of it, in either direction.

---

## 3. Nothing in the fullscreen phone layout accounts for the safe area

**Priority: high. The widget is visibly broken on every notched iPhone.**

In fullscreen mode the panel is pinned to all four edges:

```css
.wrap[data-fullscreen="true"] .panel { right:0; bottom:0; left:0; top:0; height:100%; border-radius:0; }
```

But neither the header nor the footer pads for the inset:

```css
.hdr  { padding:14px 12px 14px 16px; }   /* no env(safe-area-inset-top) */
.foot { padding:0 14px 10px; }            /* no env(safe-area-inset-bottom) */
```

So on any device with a notch or a Dynamic Island the header title and the call and close
buttons sit under the status bar, and the footer line sits under the home indicator. This
does not reproduce in a desktop browser's device emulation, which is probably why it has
survived. It reproduces on real hardware every time.

**Fix:**

```css
.wrap[data-fullscreen="true"] .hdr  { padding-top: calc(14px + env(safe-area-inset-top)); }
.wrap[data-fullscreen="true"] .foot { padding-bottom: calc(10px + env(safe-area-inset-bottom)); }
```

Worth auditing `.composer` and `.lock` for the same thing, since both sit at the bottom
edge depending on state.

---

## 4. The launcher cannot be repositioned, and it outranks everything on the page

**Priority: medium. We have worked around it, but the workaround should not be necessary.**

The launcher is `position:fixed` with hardcoded offsets, and the host element carries
`z-index: 2147483000`. On our site that produced three collisions:

1. It sat on top of our sticky mobile call bar and clipped the label of the button underneath.
2. It sat on top of our mobile navigation menu when open, covering a button and a line of text.
3. It sat on top of our booking wizard, where a tap would have opened a chat conversation
   in the middle of someone booking an appointment.

None of these are your fault in the sense that the widget is behaving as written. The
problem is that an integrator has no supported way to say "not there" or "not right now."

We fixed it ourselves because you expose `part="launcher"`, and in the shadow cascade
normal declarations from the outer document beat the shadow tree's own rules. This is what
we run:

```css
@media (max-width: 809px) {
  /* seat the launcher inside our own bottom dock */
  extreme-chat::part(launcher) {
    box-sizing: border-box;
    width: 46px; height: 46px;
    right: 21px; bottom: calc(21px + env(safe-area-inset-bottom));
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.24);
    box-shadow: none;
  }
  /* and get it out of the way when one of our own modals owns the screen */
  .xh-menu-open extreme-chat::part(launcher) { display: none; }
  html:has(.xw-root) extreme-chat::part(launcher) { display: none; }
}
```

That `part` attribute is the single most useful thing in the widget for integrators, and we
would not have been able to ship without it. Thank you for it.

**Requests:**

- Keep `part="launcher"`. Please treat it as a public API.
- Consider whether `z-index: 2147483000` needs to be that high. It guarantees the widget
  wins against the host page's own modals, which is the wrong default: a site's own booking
  flow or navigation should be able to sit above a collapsed chat launcher.
- A documented offset hook would be friendlier than making integrators discover `::part`.
  Something like `bottom: var(--exc-launcher-bottom, 20px)` and
  `right: var(--exc-launcher-right, 20px)` on `.launcher` would cover most cases, since
  custom properties pierce the shadow boundary and are much easier to document than parts.

---

## 5. Design changes we would like upstream

None of these are bugs. They are the differences between the widget's default look and the
rest of our site, and they are what we are currently patching. If you would rather keep
your defaults and give us a supported theming surface instead, see section 6, and we will
happily move to that.

### Corner radii

Inputs use `border-radius: 4px`, the primary button uses `8px`, and the composer textarea
uses `8px`. Our site uses 12px on every input and button, and 16 to 18px on cards. The 4px
inputs are the single most obviously foreign element in the widget.

Requested: `12px` on `.fld input`, `.fld textarea`, `.composer textarea` and `.btn`.

### Type weights

Headings and buttons are `font-weight: 700`. Our brand uses 800 for both. `--exc-font` is
already Montserrat, which has the weight, so this is a one-line change per selector.

Requested: `.hdr-title`, `.card h3` and `.btn` at 800, with `letter-spacing:-.02em` on the
two headings.

### The gate form is a container drawn twice

`.log` has `background: var(--exc-cloud)` (`#F9FAFB`) and `.card` sits inside it with a
white background, a 1px border, a box shadow, and a green gradient rule via `.card::before`.
On a fullscreen phone panel that is a bordered card floating on a background one shade off
from itself, and the header already has its own green gradient rule 20px above the card's.

Requested: drop the border and the `::before` gradient on `.card`, keep the shadow, and let
the radius do the separating. The cloud backdrop should stay, because behind message
bubbles that contrast is doing real work. It is only under the gate card that it reads as
redundant.

### The header subtitle wraps and the status dot mis-centers

`.hdr-id` gets 254px at a 390px viewport, and our subtitle string is 48 characters, so
`.hdr-sub` wraps to two lines. Because `.hdr-sub` is `display:flex` with default
`align-items:center`, the green `.dot` then centers itself vertically against the
two-line block instead of sitting on the first line. That is what makes the header look
unfinished. The wrap itself is fine.

Requested: `align-items: flex-start` on `.hdr-sub`, with a small `margin-top` on `.dot` to
optically align it to the first line's cap height.

### The bottom edge stacks three full-width strips

Depending on state, `.lock`, `.composer` and `.foot` can all be present, each full width
with its own `border-top`. `.lock` in particular is 14px, weight 600, in full brand purple,
which gives a hint the same visual weight as a primary action.

Requested: `.lock` as secondary text rather than purple, around 12.5px in `--exc-slate`,
with the icon matching. That alone settles the bottom edge down.

### Keep as is

The 16px font size on inputs is correct and should not be reduced. Anything smaller and iOS
zooms the page on focus. We left it alone deliberately and mention it only so a future
type-scale pass does not shrink it.

---

## 6. What we would actually prefer: a theming surface

Everything in section 5 is us imposing our brand on your component, and it is reasonable
for you to say no to some of it. What would solve the underlying problem for every customer
is a supported way to theme the widget from outside without reaching into internals.

You are most of the way there already. `:host` exposes a good token set:

```
--exc-purple, --exc-purple-deep, --exc-purple-tint,
--exc-green, --exc-green-text, --exc-green-tint,
--exc-ink, --exc-slate, --exc-border, --exc-cloud, --exc-white,
--exc-danger, --exc-font, --exc-shadow
```

Custom properties pierce the shadow boundary, so these already work from the host page, and
ours were configured correctly out of the box. The gap is that the tokens are all color,
type family and shadow. There is nothing for shape, weight or spacing, which is where the
mismatch with a host site actually shows up.

Suggested additions, all with sensible defaults so nothing changes for existing customers:

| Token | Controls | Suggested default |
| --- | --- | --- |
| `--exc-radius-input` | inputs and composer textarea | `4px` |
| `--exc-radius-btn` | primary button | `8px` |
| `--exc-radius-card` | gate card | `14px` |
| `--exc-radius-bubble` | message bubbles | `14px` |
| `--exc-weight-heading` | `.hdr-title`, `.card h3` | `700` |
| `--exc-weight-btn` | `.btn` | `700` |
| `--exc-launcher-bottom` | launcher offset | `20px` |
| `--exc-launcher-right` | launcher offset | `20px` |

If you shipped that table, we would delete our entire patch and configure the widget with
about eight lines of CSS, and so could everyone else.

A documented list of `part` attributes would be the alternative, or a complement. Today
`launcher` is the only one. `panel`, `header`, `card`, `composer` and `launcher` would cover
essentially every integration need.

---

## Appendix: what we are running today

This is appended as a single `style` element to the widget's open shadow root, after your
own stylesheet, so it wins on order wherever specificity ties. We do not fork the script:
the build we load is yours from your CDN, byte for byte. No DOM is added, moved or
relabeled, no text is edited, and the consent wording is untouched.

We are not using `!important` anywhere, deliberately, because it would also override your
own state rules for errors, disabled buttons and focus.

```css
/* header */
.hdr { padding:13px 10px 13px 16px; gap:8px; }
.hdr-title { font-size:15.5px; font-weight:800; letter-spacing:-.02em; }
.hdr-sub { align-items:flex-start; font-size:11.5px; line-height:1.35; gap:7px; }
.hdr-sub .dot { margin-top:4px; box-shadow:0 0 0 3px rgba(97,188,71,.22); }
.hdr-btn { width:40px; height:40px; border-radius:10px; }
.wrap[data-fullscreen="true"] .hdr { padding-top:calc(13px + env(safe-area-inset-top)); }

/* one surface, not two */
.log { padding:14px 14px 8px; }
.card { border:0; border-radius:16px; padding:16px 15px; box-shadow:0 2px 14px rgba(15,23,42,.08); }
.card::before { display:none; }
.card h3 { font-size:17px; font-weight:800; letter-spacing:-.02em; margin:0 0 6px; }
.card p { font-size:14px; line-height:1.5; margin:0 0 14px; }

/* fields */
.fld { margin:0 0 12px; }
.fld label { font-size:12px; font-weight:700; letter-spacing:.01em; color:var(--exc-slate); margin:0 0 5px; }
.fld input, .fld textarea, .composer textarea { border-radius:12px; border:1.5px solid var(--exc-border); padding:12px 13px; }
.fld textarea { min-height:82px; line-height:1.5; }

/* the disclosure: your intent, applied */
.card p.fine { font-size:12.5px; line-height:1.55; color:var(--exc-slate); margin:0 0 14px; }
.card p.fine a { color:var(--exc-purple); font-weight:700; text-decoration:underline; text-underline-offset:2px; }

/* CTA */
.card-actions { margin-top:2px; }
.btn { font-size:15.5px; font-weight:800; letter-spacing:0; border-radius:12px; min-height:48px;
       box-shadow:0 2px 12px rgba(95,41,128,.26); }

/* bottom edge */
.lock { font-size:12.5px; font-weight:700; color:var(--exc-slate); padding:12px; }
.lock svg { width:15px; height:15px; stroke:var(--exc-slate); }
.composer { padding:10px 12px; }
.send { width:46px; height:46px; }
.foot { font-size:11.5px; padding:0 14px 12px; }
.foot a { font-weight:700; }
.wrap[data-fullscreen="true"] .foot { padding-bottom:calc(12px + env(safe-area-inset-bottom)); }

/* bubbles */
.bub { font-size:14.5px; border-radius:14px; }
```

---

## Summary of what we are asking for

| # | Item | Type | Priority |
| --- | --- | --- | --- |
| 2 | Consent line uses the wrong company name | Compliance bug | High |
| 1 | `.card p` overrides `.fine`, disclosure renders at body size | Bug | High |
| 3 | Fullscreen layout ignores `env(safe-area-inset-*)` | Bug | High |
| 4 | Launcher position is fixed and `z-index` outranks the host page | API gap | Medium |
| 5 | Radii, weights, doubled container, header dot, bottom edge | Design | Medium |
| 6 | Shape and weight tokens, documented parts | API request | Medium |

Items 1, 2 and 3 we would like fixed regardless of what happens with the rest. Item 2 needs
a heads up on timing, because our A2P registration text has to move with it.

Happy to jump on a call, and happy to test any build before it ships.
