# SME code review — findings

**Community Cooking Rota · SME code review · 22/09/2026**

Written up after walking through the live app as your Subject Matter Expert reviewer, following the demo script from *ct-cb-019 — Prepare and run the SME code review demo*. Both items below are now logged as real GitHub issues, labelled `sme-feedback`.

## 00 · What was reviewed

I walked the app the way a real user would, not the way a developer would: registering, creating a rota as an Organiser, claiming a slot as a Cook, and cancelling that claim — the same loop covered in the demo script, plus a look at the new calendar-grid view on the rota detail page.

## 01 · What's working well

> **The core loop holds together.** Register → create rota → claim → cancel all worked exactly as intended, with no dead ends or confusing states. The calendar grid makes it immediately obvious which dates are open versus claimed, and the permission checks (an organiser can't edit someone else's rota, a cook can't cancel someone else's claim) behaved correctly when I tried to break them.

## 02 · Feedback logged

Two things stood out as genuine gaps for how this app would actually get used — both written up as issues on your repo, in the same shape you'll use for your real SME session.

### No way to contact the cook or organiser from a rota page — Medium priority

**What I found** Once a Cook claims a date, there's no way for them to ask the organiser a question ("what time should I drop this off?"), or for the organiser to reach the cook if plans change. The rota page shows an address and dietary notes, but no phone or email for either side.

**Why it matters** Real meal trains run on exactly this kind of back-and-forth. This is the more consequential of the two — it's a real usability gap in the core "someone signs up to help" flow.

**Possible fix** Show the organiser's email or phone to the cook once they've claimed a slot, without exposing it publicly to everyone browsing the rota.

**Logged as** [Issue #15](https://github.com/sarahjhill/cooking-rota/issues/15)

### Claimed slots show a date but no time — Low priority

**What I found** A real meal rota usually needs a rough drop-off time, not just a day — "Tuesday" isn't enough on its own; people want to know roughly when to expect it or when to drop it round.

**Why it matters** Smaller than the contact-details gap, but still a genuine piece of missing information for how the app gets used day to day.

**Possible fix** The `Slot` model currently only has a date field. Adding an optional time (or even just a free-text "preferred time" note) would cover this without forcing precision nobody has yet.

**Logged as** [Issue #16](https://github.com/sarahjhill/cooking-rota/issues/16)

## 03 · Next steps

1. Decide for each issue: fix now, fix later, or won't fix (comment why, then close it) — see *ct-cb-019, step 04* for the full triage process
2. If you're doing either, add it as a task in Project OS under the phase it fits best — likely **4. Notifications** for the contact-details one, and **3. Core CRUD** or **5. Testing & QA** for the slot-time one
3. Link the GitHub issue under that task's **Linked documents** and set a realistic priority — Medium and Low suggested above, but it's your call

> **Why only two.** This was a walkthrough of what's built so far, not an exhaustive audit — the two things above are the gaps a real first-time user would actually hit, not a list of everything that could theoretically be improved. That's deliberate: a short, honest list you'll actually act on beats a long one that gets ignored.

---

**Sarah J Hill** — Dragon Fire Design
sarahjhill.com · sarah@sarahjhill.com
Community Cooking Rota · Code Institute Full-Stack Capstone
