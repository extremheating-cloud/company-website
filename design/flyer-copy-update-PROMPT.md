# Follow-up prompt — update the Extreme Rewards flyer copy

Paste everything below the line into a Claude session that has the `extreme-brand` skill
available. It is written to be self-contained.

---

Load the `extreme-brand` skill and read `references/programs.md` in full, plus
`references/color.md`, `references/typography.md`, `references/logo.md` and
`references/applications.md`.

We are updating the **Extreme Rewards bi-fold and tri-fold brochures**. The referral program
was redesigned and the flyers now carry the wrong offer. They have not gone to press in the
new form yet. The QR code on the piece points at `extremeheating.com/referral`, and that web
page has already been rebuilt on the new program — **the flyer and the page must say exactly
the same thing.** Treat the web page as the reference implementation.

## What the program is now

Two numbers that mirror each other. That mirror is the whole idea — a referrer who earns less
than their friend saved feels short-changed, and an offer with more than two numbers in it
does not survive being repeated to a neighbour.

**Headline, verbatim:**

> Give $250. Get $250.

**Supporting line, verbatim:**

> Whatever they save, you earn.

**The two cases:**

- They're getting a **new heating, cooling, or plumbing system** → they save **$250**, you earn **$250**
- **Any other repair or installation** → they save **$100**, you earn **$100**

Rewards are paid as **Visa gift cards**. There is **no limit on how many friends you can refer**.

**Approved long copy** for a panel with room (use as-is):

> **Refer a friend. Whatever they save, you earn.**
>
> Send someone our way and they'll get $250 off a new heating, cooling, or plumbing system, or
> $100 off any repair or installation. When the job's finished, you get the same amount on a
> Visa gift card. Refer as many friends as you like.

**Approved short copy** for an invoice footer or back panel:

> Know someone who needs us? Send them $250 off a new system — and earn $250 yourself when the
> job's done.

**Required terms line — must appear verbatim, in any panel with room for fine print:**

> New customers only. Referral must be named when the job is booked. Reward issued within 90
> days of job completion. See full terms at extremeheating.com/terms.

State the 90-day window wherever there is room. Someone who expects a card in two weeks and
waits eleven calls the office annoyed; someone told 90 days who gets it in three is delighted.

## The mechanism — do not soften this

The reward is triggered when **the referred customer names the referrer at the time they
book**. There is no form, no code, no link to track, and no retroactive claims. If the flyer
gives the referrer one instruction, it is:

> Tell your friend to mention your name when they book.

Any layout that implies handing over the flyer, scanning the QR, or submitting something is
what earns the reward will generate payout disputes. The QR is a *destination*, not a
mechanism.

## Remove from the current flyers

Every one of these is now wrong:

- The old headline **"Give $500. Get $250."**
- **$500 off** a new system → it is $250
- **$50 off** everything else → it is $100
- The job-type payout tiers (**$25 / $100 / $200**) — the tier structure is gone from the
  customer offer entirely
- The **+$30 X-Plan member** bonus — removed from the program
- The **+$20 X-Plan signup** bonus — removed from the program
- Any "bonuses stack" or "up to" laddering language built on those tiers

"Up to $250" remains accurate and is still approved phrasing where it reads better than the
flat number.

## Never print these

`programs.md` has an internal-only section. None of it goes on a customer-facing piece:

- Spend backstop thresholds (the $4,500 / $500 invoice floors)
- The internal job-type qualification table
- Gift card activation cost, batching cadence, or that 90 days is an outer commitment
- Tax handling, W-9 or 1099 mechanics
- Cost per acquisition or lead economics
- ServiceTitan or business-unit mechanics

Also: **never mention tiers, spend thresholds, or job-type lists.** If the copy needs to
explain how the amount is decided, the answer is "whatever your friend saves, you earn."

## If the flyer also mentions X-Plan

- Pricing is **$249/year or $20.75/month**. Do not write "per system" — that is not a
  confirmed term.
- Lead with the **Zero Risk Investment**, and never state it without **both** conditions: the
  years must be **consecutive**, and it caps at **$2,500 or 10 years**, whichever comes first.
  Dropping either creates a dispute at the moment a customer is buying a system.
- The accrual **follows the person, not the property.** Never write "transfers with your home"
  or "100% Transferable" — that claim has been retired.
- X-Plan is under review for a bundled HVAC + plumbing redesign at a higher price point. The
  numbers above are correct for anything written today, but re-check `programs.md` before the
  piece actually goes to press.

## Brand constraints

- **Montserrat only**, weights 400–800. No second typeface.
- **Extreme Purple `#5F2980`** — CMYK `76 / 100 / 0 / 0`. **Extreme Green `#61BC47`** —
  CMYK `62 / 0 / 89 / 0`. No third brand colour; extend with neutrals.
- Keep purple dominant, roughly **70% purple / 20% neutral / 10% green**. A piece that reads as
  majority green is off-brand.
- Body copy in ink `#0F172A`, not purple.
- **Green `#61BC47` is not a text colour on a white background** (2.39:1). Use `#3F852B` for
  green type on light stock. Full-strength green is for fills, bars, rules and icons.
- **Logo:** purple-wordmark file on white backgrounds, white-wordmark file on everything else.
  **Never place either lockup on green** — the descriptor line is green in both files and
  disappears. Use the **`.eps` vector** files from `assets/logo/` for print, never the PNG, and
  never anything from `assets/logo/archive/`.
- Never rebuild the EXTREME wordmark in Montserrat. It is custom lettering.
- Write **X-Plan** and **Extreme Rewards** exactly — no ™, ®, or ℠, no quotation marks.
- Banned: "Learn More", exclamation points, world-class, cutting-edge, best-in-class,
  state-of-the-art, utilize, leverage, fear-selling, fake scarcity.
- Pair any claim with a verified proof point ("90% same-day service", "over 20 years",
  "25k+ jobs completed", "24/7 emergency service").

## Phone number — check this before you set type

`programs.md` is explicit: the main line **937.431.7399 is not used on tracked campaign
material**. Printed pieces carry their own call-tracking number, and putting the main line on a
tracked piece breaks attribution for the whole run. Get the call-tracking number for this
brochure from whoever is running the campaign. Do not substitute the website's (844) number
without confirming it is the right tracked line for print.

## QR code

Points to `https://www.extremeheating.com/referral`. Confirm the code resolves before release.
If a `/refer` → `/referral` redirect has been added as a safety net, `/refer` is also valid —
verify rather than assume.

## Deliverable

Updated copy for both the bi-fold and the tri-fold, laid out panel by panel, with the terms
line placed in a panel that has room for it. Flag anything you cannot source from
`programs.md` rather than writing around it — do not invent an amount, a condition, a
deadline, or a term.
