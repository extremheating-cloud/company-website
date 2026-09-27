# Google Tag Map: extremeheating.com

**Call:** Mon Sep 28, 2026, 12:00pm ET · **Case** 9-2701000041001 · **Ads account** 887-338-2120
**Campaign flagged:** Dayton & Cincinnati Demand Gen | Heating, Cooling, & Plumbing

---

## The diagnosis (checked in the live accounts, Sep 27)

**The Demand Gen campaign has recorded 0 conversions since it launched on Aug 20.** It has spent **$4,048** in the last 30 days (Aug 28–Sep 26) and got 390k impressions. Google's own diagnostic on it reads *"Your campaign may not reach stabilized performance,"* with the fix listed as **"Conversion goals: Improve tag performance,"** and estimated conversions **"Low."**

Why, in order:

1. **It bids on the wrong goal.** The campaign-specific goal is **Phone call leads only**. Five of that goal's six primary actions are *calls from ad extensions*, which come from Search, not from YouTube, Discover or Gmail where Demand Gen runs. The only one it could actually earn is "Website Calls -- (844) 584-7399."
2. **The account expects enhanced conversions from GTM, and GTM has nothing to give.** Goals → Settings says *"Managed through Google Tag Manager."* The GTM container has no Google Ads tag and no user-data variable.
3. **Bookings reach no campaign.** The action that counted bookings ("Schedule Service", imported from GA4) sits in the **Submit lead form** goal, which **0 of 56 campaigns** use, and it has stopped receiving data since the ServiceTitan switch. Meanwhile the **Book appointment** goal, used by **40 of 56 campaigns**, contains only a dead action.

This predates the ServiceTitan switch. The campaign was set up this way on Aug 20.

---

## 0. What's in the accounts

### GTM `GTM-TG8GZWXC`: live version 2, published Dec 9, 2025

The whole container is **1 tag, 1 trigger and 0 variables.** Backup: `~/Downloads/GTM-TG8GZWXC_v2.json`.

| Tag | Type | Fires on | Problem |
|---|---|---|---|
| Broccoli Booking Completed | GA4 Event `broccoli_booking_completed` | Custom event `bookingCompleted` | **Measurement ID is set to `{{Event}}`**, which resolves to the event name, not `G-GCH0RVQ88Y`. The event is sent nowhere |

No Google Ads tags, no GA4 config, no conversion linker, no `tel:` click trigger, and nothing listening for ServiceTitan. **GTM can't cause double counting.**

### Google Ads 887-338-2120: goals

| Goal | Used by | Primary actions | Status | Results (Aug) |
|---|---|---|---|---|
| **Phone call lead** | 42 of 56 campaigns | 6 | Needs attention | 176 |
| **Book appointment** | 40 of 56 campaigns | **0** | **Misconfigured** | **0** |
| Submit lead form | **0 of 56** campaigns | 2 | Needs attention | 16 |
| Get directions | 0 of 56 | 1 | Active | 68 |
| Page view | 0 of 56 | 1 | Active | 82 |

### The actions inside the goals that matter

| Action | Goal | Primary? | Source | Conv. | Status |
|---|---|---|---|---|---|
| DAY (937) 431-7399 (ad extension) | Phone call lead | Primary | Call from Ads | 73.35 | Active |
| Cin (513) 640-7399 (ad extension) | Phone call lead | Primary | Call from Ads | 49.27 | Active |
| **Website Calls -- (844) 584-7399** | Phone call lead | Primary | Website | **26.00** | **Active**: the forwarding-number swap works |
| Plumbing (513) 214-0392 (ad extension) | Phone call lead | Primary | Call from Ads | 18.98 | Active |
| Phone call (call only ads) \| Both | Phone call lead | Primary | Call from Ads | 9.00 | Active |
| Business profile - Tracked call | Phone call lead | Primary | Other | 0 | Awaiting conversions |
| **Phone call (website) actual** | Phone call lead | Secondary | Website | **0** | Awaiting: almost certainly the click conversion nothing calls |
| **Schedule service** (lowercase s) | Book appointment | **Secondary** | Website | **0** | **Misconfigured** |
| **Schedule Service** (capital S) | Submit lead form | Primary | **GA4 import** | **15.60** | **Awaiting conversions**, stopped since the ServiceTitan switch |
| Lead form - Submit | Submit lead form | Primary | Google hosted | 0 | Awaiting conversions |

### Settings (Goals → Settings)

| Setting | Value |
|---|---|
| Enhanced conversions | **"Managed through Google Tag Manager. Recording Enhanced Conversions."** GTM has no Ads tag to record them |
| Enhanced conversions for leads | **Not configured yet** |
| Call conversion action | **Not set yet** |
| Customer data terms | Accepted |

### Demand Gen campaign 24159969587

| | |
|---|---|
| Conversion goal | **Campaign-specific: Phone call leads** |
| Bidding | Maximize conversions, no target CPA |
| Budget / start | $120/day, started **Aug 20, 2026**, runs Mon–Fri |
| View-through conversion optimization | On (beta) |
| Last 30 days | **$4,048.63 · 390,227 impr · 0 conversions** |
| Google's diagnostic | "May not reach stabilized performance" → **Improve tag performance**. Estimated conversions: **Low** |

### ServiceTitan scheduler: events it pushes to `dataLayer`

Captured on the live site from a real test booking on Sep 27 (appointment 150981661, Aaron to cancel). Every event has `event_category: "Scheduling Pro - Booking"` and `schedulerName: "Website Scheduler"`.

| Order | `event` | `event_label` | `value` |
| --- | --- | --- | --- |
| 1 | `BookingStarted` | | |
| 2 | `BookingProcessStarted` | | |
| 3 | `BookingAddressSelected` | | |
| 4 | `BookingIssueStarted` | `HVAC` | |
| 5 | `BookingIssueCompleted` | `HVAC` | issue id, plus `issuePath` |
| 6 | `BookingSchedule` | `Timeslot` | e.g. `Tue, Sep 29, 12 PM - 4 PM` |
| 7 | `BookingDetailsMore` | | |
| 8 | **`BookingBooked`** | `Appointment id` | **the ServiceTitan appointment id** |

**`BookingBooked` is the conversion event.** Its `value` is the appointment id, which makes a clean `transaction_id` for dedup. It is not a dollar value.

**None of these reach Google today.** They're plain `dataLayer` objects, which gtag.js ignores; only a GTM trigger would pick them up, and GTM has none. During the test booking the only GA4 hit was `page_view`, and nothing went to Ads.

**No email or phone in any event**, so enhanced conversions can't read them from `dataLayer`.

---

## 1. Stack

| | |
|---|---|
| Platform | Static HTML generated by a Python builder (`builder/`). No CMS, no database. |
| Hosting | Cloudflare Pages. Build `python3 builder/build_site.py`, output `site/`, branch `main`. |
| Where every tag lives | **One file:** `builder/analytics.py` (`HEAD` and `BODY_START`) |
| How it reaches every page | `builder/shell.py:1381` puts `analytics.HEAD` at the end of `<head>`. `builder/shell.py:1384` puts `analytics.BODY_START` right after `<body>`. |
| Coverage | Checked all **320** built pages (319 + 404). GTM, GA4 gtag and Ads gtag are on **320/320**, all in `<head>`. |

---

## 2. What loads

| Tag | ID | File:line | Notes |
|---|---|---|---|
| Google Tag Manager | `GTM-TG8GZWXC` | `analytics.py:50-56` (head), `:132-135` (noscript) | Container contents are **not in this repo** |
| GA4 via gtag.js | `G-GCH0RVQ88Y` | `analytics.py:58`, config `:65` | Loaded directly, outside GTM |
| Google Ads via gtag.js | `AW-974361798` | `analytics.py:59`, config `:66` | gtag.js is loaded **twice** (two script tags) |
| Ads: phone-click conversion | `AW-974361798/mAc6CKqtoa0bEMapztAD` | `analytics.py:71-85` | `gtag_report_conversion()`, **never called** |
| Ads: calls from website | `AW-974361798/mC9aCLvK9rkbEMapztAD` | `analytics.py:88-90` | `phone_conversion_number: '(844) 584-7399'`, Google forwarding-number swap |
| Meta Pixel | `1116748220634990` | `analytics.py:93-109` | PageView on every page, Lead on wizard submit |
| Broccoli widget | `c5182eae-…` | `analytics.py:137` | Pushes its own events to `dataLayer` |
| ServiceTitan scheduler | `sched_vszsnfpi7yf7bi6g6l1nslt0` | `analytics.py:145` | **Primary booking.** Pushes events to `dataLayer` |
| ServiceTitan legacy iframe | tenant `770617940` | `analytics.py:168-227` | Broccoli's hook only, not on our buttons |
| FollowUp Pro chat | n/a | `analytics.py:159` | **Pushes nothing** to Google or Meta |
| Backup booking wizard | n/a | `framer/schedule/ContactFlowDialog.tsx` | gtag events + Meta Lead, fallback only |

No CallRail, CallTrackingMetrics, or other call tracking. No Microsoft, TikTok, LinkedIn, Hotjar or Clarity tags.

---

## 3. Conversion points

| Conversion | Where on site | How it fires today | Event / send_to | Ads conversion fires? |
|---|---|---|---|---|
| **Phone click** | 2,289 `tel:` links on 320 pages: header, footer, hero, content, mobile menu. 2,255 go to (844) 584-7399; 34 go to the four office lines | **Nothing fires on click.** `gtag_report_conversion()` exists but no link calls it | would be `AW-974361798/mAc6CKqtoa0bEMapztAD` | **No**, from code. Check GTM for a click trigger |
| **Calls from website** | "(844) 584-7399" as text on 319 pages | gtag swaps the number for ad clickers, and Google counts the call | `AW-974361798/mC9aCLvK9rkbEMapztAD` | **Unclear.** Config is present; depends on the Ads conversion action. Office numbers are not swapped |
| **Booking: ServiceTitan** (primary since 2026-09-21) | Every Schedule button (7 on the homepage) calls `ScheduleEngine.show()`, `chrome.py:786` | ST pushes `{event, event_category, event_label, schedulerName, uniqueEventId, value}` to `dataLayer` from its iframe | Completion is **`BookingBooked`** (captured Sep 27, see §0) | **No.** gtag.js ignores these and GTM has no trigger |
| **Booking: our wizard** (fallback, only when ST fails to load) | Same buttons | After a successful Formspree POST (`formspree.io/f/mqadkggp`): `gtag('event','schedule_form_submit')` **with no `send_to`**, plus Meta `Lead` | `schedule_form_submit`, `ContactFlowDialog.tsx:1128` | **GA4 only**, unless it's a GA4 key event imported into Ads. Inline success message, no thank-you page |
| Wizard opened | Same | `gtag('event','schedule_dialog_open')` | `ContactFlowDialog.tsx:856` | GA4 only |
| **Chat** (FollowUp Pro) | Bottom right, every page | Fires nothing | n/a | **No** |
| Text Us | Footer | Opens the SMS app, no event | n/a | No |
| Financing apply | `/financing-options`, outbound to `wpcu.merchantlinq.com` | No event | n/a | No |
| X-Plan join | `/maintenance` "Join X-Plan" goes to the pricing section, then a Schedule button | Same as booking | n/a | See booking |
| Contact form | None. `/contact` has phone, map and a Schedule button | n/a | n/a | n/a |
| Thank-you pages | **None exist.** The wizard and ServiceTitan both confirm inline | n/a | n/a | n/a |

---

## 4. Checklist

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | Google tag on every page, in `<head>`, before conversion events | **PASS** | 320/320. It sits at the end of `<head>` after CSS and schema; Google recommends as high as possible |
| 2 | Enhanced conversions enabled in the tag | **FAIL** | Ads says *"Managed through Google Tag Manager"*, but GTM has no Ads tag and no user-data variable, and the code sends no `user_data`. EC for leads: *Not configured yet* |
| 3 | Forms send email + phone into the conversion | **FAIL** | The wizard has name, phone and email in memory but sends a bare event. ServiceTitan keeps them inside its iframe, so our page never sees them |
| 4 | Consent Mode | **ABSENT** | No `gtag('consent', …)`. The privacy policy's open notes already flag the Ohio consent question for counsel |
| 5 | `send_to` values in code | **Matched** | `mC9aCLvK9rkbEMapztAD` = "Website Calls -- (844) 584-7399" (26 conv, working). `mAc6CKqtoa0bEMapztAD` = almost certainly "Phone call (website) actual" (Secondary, 0, never called). Confirm the second one's label on the call |
| 6 | No duplicate tags | **PASS** | GTM carries no GA4 or Ads tags, so nothing doubles. gtag.js is loaded twice (two script tags), which is redundant but harmless |
| 7 | `tel:` conversion fires on click, once | **FAIL** | Doesn't fire at all from code. The function is correct (fires on the call, not on load) but nothing calls it |

---

## 5. Consolidation

The code is **already in one place**: `builder/analytics.py`, injected on every page by one line in `shell.py`. There are no scattered snippets.

The real split is **GTM vs hard-coded gtag.** Pick one owner:

- **GTM owns it (recommended for this call).** Google support works in the GTM UI, and changes go live without a site deploy. Move the GA4 config, the Ads config and the conversions into GTM, then delete `analytics.py:57-91` (the gtag block, the phone-click function and the forwarding-number config).
- **Code owns it.** Keep gtag in `analytics.py` and remove the GA4 and Ads tags from GTM.

Don't choose until you've seen what's inside `GTM-TG8GZWXC`.

---

## 6. Branch, backup, local

| | |
|---|---|
| Backup tag | `pre-google-tag-2026-09-28` → commit `a967898` (equals `main`, pushed) |
| Branch | `google-tag-implementation`, off `main`, pushed |
| Preview | Cloudflare builds the branch at `https://google-tag-implementation.company-website-4vm.pages.dev`. It fires the **real** tags, so test traffic lands in the real GA4 and Ads |
| Edit tags | `builder/analytics.py` |
| Edit wizard events | `framer/schedule/ContactFlowDialog.tsx`, then `npm run build:schedule` |
| Roll back | `git checkout main`, or `git reset --hard pre-google-tag-2026-09-28` |

Run it locally:

```bash
python3 builder/build_site.py
python3 -m http.server 8099 --directory site
```

Open `http://localhost:8099`, then connect Tag Assistant (tagassistant.google.com) to that URL.

---

## 7. Outside the repo: back these up separately

- **GTM container `GTM-TG8GZWXC`**: Admin, Export Container. **Do this before the call.**
- **Google Ads conversion actions**: screenshot Goals, Conversions and each action's settings.
- **GA4 key events**: screenshot Admin, Events.
- ServiceTitan scheduler settings, Broccoli widget settings, Formspree form `mqadkggp`.
- The site itself needs no extra backup: Cloudflare Pages keeps every deployment and can roll back from Deployments.

---

## 8. What's still open

Answered on Sep 27: the GTM contents, which conversion actions exist, what Demand Gen bids on, the enhanced conversions setting, and when the problem started (Aug 20).

Still open:

1. ~~ServiceTitan's booking-complete event name.~~ **Answered Sep 27: `BookingBooked`** (see §0).
2. **Can ServiceTitan hand the customer's email and phone to the page?** Its `dataLayer` events carry neither. Ask ServiceTitan whether there's another hook; otherwise EC for bookings needs a different route.
3. **Confirm `mAc6CKqtoa0bEMapztAD` is "Phone call (website) actual".** Open that action in Ads and check its tag label.
4. **Why "Schedule service" (Book appointment goal) is Misconfigured.** Click its Troubleshoot link on the call.

## 9. Questions to put to Google on the call

1. Demand Gen bids only on **Phone call leads**, and five of its six primary actions are ad-extension calls it can't generate. Should it bid on a **booking** goal instead?
2. Enhanced conversions say **"Managed through GTM"**, but GTM has no Ads tag. Should EC be moved to the Google tag in code, or should an Ads conversion tag go into GTM?
3. Bookings now happen in **ServiceTitan's iframe**, which pushes **`BookingBooked`** (value = appointment id) to `dataLayer` on completion, and nothing reaches Google. Should a GTM trigger on `BookingBooked` fire the Ads conversion, and how do we get enhanced conversions when the event carries no email or phone?
4. There are two near-duplicate actions: **"Schedule Service"** (GA4 import, Primary, in a goal no campaign uses) and **"Schedule service"** (Secondary, Misconfigured, in the goal 40 campaigns use). Which one should survive?
