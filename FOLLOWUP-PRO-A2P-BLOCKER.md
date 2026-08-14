# Blocker: the chat widget fails A2P review as shipped

From: Extreme Heating, Air, Plumbing (extremeheating.com)
Widget: `chat-widget.js` from `followup-pro-37ed6.web.app`
Date: 2026-08-13
Severity: blocking. Our business SMS cannot go live until this changes.

Our campaign was rejected again. The first rejection (Twilio 30909) was our fault
and we fixed it. This one is the widget.

```
Brand:      Extreme Heating Air Plumbing
TCR ID:     CBEBWJ2
Telnyx ID:  4b30019f-fcc8-b08d-9f46-5e8f9b2b6188
Status:     TELNYX_FAILED
```

The reviewer's reason, verbatim:

> The phone number field is currently mandatory and should either be made
> optional or a checkbox needs to be added (unchecked and optional) next to the
> opt-in language.

---

## What the widget does today

Measured in a logged-out browser against the live build on 2026-08-13, reading the
gate form out of the shadow root:

| Field | `id` | `required` |
| --- | --- | --- |
| First name | `exc-fname` | **true** |
| Last name | `exc-lname` | **true** |
| Mobile number | `exc-phone` | **true** |
| What's going on? | `exc-msg` | **true** |

`shadowRoot.querySelectorAll('input[type=checkbox], [role=checkbox]')` returns
**zero elements**.

So a visitor cannot send anything without providing a mobile number, and the only
consent mechanism is the act of sending. That combination is precisely what the
reviewer is objecting to: if the number is mandatory and consent is implied by
submitting, the visitor was never actually offered a choice. Consent is not a
condition of purchase, but as built it is a condition of using the widget at all.

---

## The two fixes the reviewer will accept, and which one to take

**Do not make the phone field optional.** It is technically the shorter path and
it is the wrong one. The entire purpose of this widget in our filing is opt-in
path 2 — a visitor handing us a number we may text. A widget that collects no
number is a web chat, not an SMS opt-in, and it would remove the path rather than
fix it.

**Add the checkbox.** Unchecked on load, and genuinely optional: the Send button
must stay enabled and the message must still send when it is left unticked. The
visitor simply does not get texted.

We already run exactly this pattern in our own booking form on the same site, and
it has not been challenged by either reviewer. If it is useful as a reference:

- state initialises to `false`, with no attribute or effect that pre-ticks it
- it is deliberately absent from the form's completion check, so it can never gate
  submission
- `role="checkbox"`, `aria-checked`, and `aria-describedby` pointing at the
  disclosure text
- the submission records the boolean either way, plus a timestamp, the page URL,
  and the disclosure string as rendered

That last point matters more than it looks. Storing the disclosure verbatim with
the record is what makes it a consent record rather than a claim about one.

---

## What this changes for the filing, which is why we need timing from you

Right now our registration says, for opt-in path 2:

> "The visitor's affirmative act of sending the message is the opt-in, and we
> store the disclosure text verbatim with the number and a timestamp."

If you add a checkbox, that sentence stops being true — the opt-in becomes the
tick, not the send. **So the widget change and our registration text have to move
together.** If you ship first, our filing describes a widget that no longer
exists; if we file first, we describe one that does not exist yet.

Please tell us:

1. Whether you are adding the checkbox, and roughly when.
2. The exact label text it will carry, so we can quote it character for character
   in the resubmission. If you want a starting point, this is the wording our own
   form uses and it has cleared review:

   > Yes, text me about my service request at the number above. Consent is not a
   > condition of purchase. Msg & data rates may apply, message frequency varies.
   > Reply HELP for help or STOP to opt out. See our Privacy Policy and Terms.

3. Whether the stored consent record will distinguish ticked from unticked. A
   record that cannot tell the two apart is not usable as a TCPA record.

We are not patching this on our side. Your consent string is quoted in the filing
and forking the script to change it would break the one thing the filing is
asserting. Reporting it instead, as agreed.

---

## Unrelated, and not blocking

Our texting number changed on 2026-08-13 when we moved from Twilio to Telnyx. It
is now **(937) 977-1464**. The old number, (937) 744-7148, does not exist on the
new account.

This does not affect your embed: `data-phone` is the call fallback and is
deliberately our office line, **(844) 584-7399**, which has not changed. Nothing
in the widget config needs editing. Flagging it only so nobody "helpfully"
updates `data-phone` to the texting number.
