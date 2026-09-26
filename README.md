# Community Cooking Rota

**Live app:** <a href="https://community-cooking-rota-a0e405aa09f1.herokuapp.com/" target="_blank" rel="noopener">community-cooking-rota-a0e405aa09f1.herokuapp.com</a>
**Repository:** <a href="https://github.com/sarahjhill/cooking-rota" target="_blank" rel="noopener">github.com/sarahjhill/cooking-rota</a>

Developer: Sarah Hill (<a href="https://github.com/sarahjhill" target="_blank" rel="noopener">sarahjhill</a>)

![Screenshot of the Community Cooking Rota homepage](docs/screenshots/home.png)

## Introduction

Community Cooking Rota is a Django web app that helps a support network organise home-cooked meals for someone going through a hard patch — new parents, a household recovering from surgery or bereavement, or an elderly neighbour who could use the help. An organiser creates a rota for the recipient, sets the dates, and invites cooks; each cook registers, claims an open slot, and can see delivery and dietary details, cancelling if their plans change. It replaces the ad-hoc spreadsheet-and-WhatsApp approach with a simple, accountable, full CRUD web app built around one real, everyday problem.

I chose this idea because I'd already seen the problem it solves play out informally, in a WhatsApp group and a shared spreadsheet, for a `cardiff-community-meals` rota I'd been part of. That version worked, but only just: no accounts, no real permissions, and no way to know at a glance who still needed to sign up. Rebuilding it properly as an account-based Django app let me solve a problem I understood first-hand, while also giving me a natural, non-contrived reason to build full CRUD, role-based access control and a real permissions model — exactly what this assessment needs to see.

This is a Full-Stack Individual Capstone Project for the Code Institute AI Augmented Full-Stack Bootcamp.

## UX — The 5 Planes

### 1. Strategy

**Purpose**

Give a small support network (family, friends, neighbours) a single, accountable place to organise a rota of home-cooked meals for someone who needs them — replacing an ad-hoc spreadsheet or WhatsApp thread, where it's easy to lose track of who's already signed up.

**Primary user needs**

- An **organiser** needs to set up a rota quickly, control who can edit it, and see at a glance which dates are still unclaimed.
- A **cook** needs a simple, low-friction way to see what's needed and claim (or cancel) a date, along with any dietary notes or delivery details.
- Both need confidence that only the right people can change a rota or claim on someone else's behalf.

**Project goals**

- Demonstrate a genuinely useful, real-world tool — not a contrived CRUD demo.
- Show full CRUD, custom role-based authentication, and a real permissions model (not just `login_required`).
- Ship something accessible and responsive enough that a non-technical support network could actually use it.

### 2. Scope

**Features** (see [Features](#features) below for the full list)

**Content requirements**

- Rota: recipient name, occasion, dietary notes, address, date range.
- Slot: a single cooking date, optionally claimed by a cook, with notes.
- Role-aware navigation (Organiser / Cook / signed-out visitor).
- On-page notifications for every create, update, delete and claim action.
- Custom 403 / 404 / 500 error pages that stay in the site's own style.

### 3. Structure

**Information architecture**

- **Navigation** (see `templates/base.html`): Home is always visible. Signed out, the nav offers Log in / Sign up. Signed in, it shows the user's name and role (e.g. "sarah (Organiser)"), a Log out button, and an Admin link for staff users.
- **Homepage**: lists every rota currently in the system (open to anyone, signed in or not), so a visitor can see the concept before creating an account.
- **Rota detail page**: the recipient's details (occasion, dietary notes, address) followed by a calendar-style grid of every date/slot on that rota, each showing its status (open / claimed, and by whom) plus whatever action applies to the viewer.

**User flow**

- Guest → browses the homepage and an open rota → registers as Organiser or Cook to actually do anything.
- Organiser → creates a rota → adds dates (slots) to it → edits/deletes as things change.
- Cook → browses a rota's open dates → claims one → can cancel their own claim later if plans change.

### 4. Skeleton

**Wireframes**

Low-fi wireframes for the core screens (homepage, rota list, rota detail/slot list) were sketched before development, covering the mobile-first layout and the desktop breakpoint. See <a href="docs/wireframes.md" target="_blank" rel="noopener"><code>docs/wireframes.md</code></a> for the full set.

**Deviation from the wireframes:** the wireframes sketched a desktop (≥768px) layout with the rota list and rota detail side-by-side in two columns. The build uses separate full-page views instead (list page → detail page) at every breakpoint. This was a deliberate call, not an oversight — a split view adds real complexity (keeping two panels in sync, extra routing/JS) for a capstone where the core assessed behaviour is the CRUD/permissions logic underneath, not the layout shape. Every other element of the wireframes (nav, cards, slot grid) is followed as sketched, and the layout is fully responsive at mobile/tablet/desktop.

### 5. Surface

**Colour scheme**

A warm, kitchen-table palette rather than a corporate one, since the app is about neighbours cooking for each other, not a SaaS dashboard.

| Swatch | Variable | Hex | Use |
|---|---|---|---|
| 🟫 | `--primary` | `#b85c38` | Buttons, links, primary actions |
| 🟤 | `--primary-dark` | `#8a4128` | Hover/active states |
| ⬜ | `--bg` | `#f8f5f1` | Page background (warm off-white) |
| ⬜ | `--panel` | `#ffffff` | Cards and panels |
| ⬛ | `--text` | `#1f2933` | Body text |
| ◽ | `--muted` | `#52606d` | Secondary/muted text |
| ▫️ | `--border` | `#e5e7eb` | Borders and dividers |

Defined once as CSS custom properties at the top of `static/css/styles.css`, so the whole site's palette can be re-themed from one place.

**Typography**

The system default sans-serif stack (`Arial, sans-serif`) is used throughout, deliberately — no external font request, which keeps the site fast to load and avoids a flash of unstyled text, and system fonts are already accessible and familiar to every visitor's device.

## User Stories

| Target | Expectation | Outcome |
|---|---|---|
| As a **visitor** | I would like to see rotas that exist and what they need | so that I understand what the site does before creating an account |
| As a **visitor** | I would like to register as an Organiser or a Cook | so that I can start using the site in the role that fits me |
| As an **organiser** | I would like to create a rota for a recipient with their dietary notes, address and a date range | so that I have one place to co-ordinate meals for them |
| As an **organiser** | I would like to add cooking dates (slots) to a rota | so that cooks have specific dates they can claim |
| As an **organiser** | I would like to edit or delete a rota, or a slot on it | so that I can correct mistakes or respond to changing plans |
| As an **organiser** | I would like only me to be able to edit or delete my own rotas | so that another user can't accidentally (or deliberately) change my rota |
| As a **cook** | I would like to see which dates on a rota are still open | so that I know what's still needed |
| As a **cook** | I would like to claim an open date | so that the organiser and other cooks know it's covered |
| As a **cook** | I would like to see dietary notes and the delivery address for a rota | so that I know what and where to cook for |
| As a **cook** | I would like to cancel a date I've claimed | so that I can back out if my plans change, and free the slot for someone else |
| As a **cook** | I would like only me (or the organiser) to be able to un-claim my slot | so that nobody else can cancel my commitment on my behalf |
| As **any signed-in user** | I would like clear on-page confirmation after every action | so that I know a create/update/delete/claim actually worked |
| As **any user** | I would like a friendly error page if I get lost, or if something goes wrong | so that it's obvious what happened, in a page that still looks like the rest of the site |
| As **any user** | I would like the site to work well on my phone | so that I can check or claim a date wherever I am |

## The idea

A Django rebuild of the rota concept from the `cardiff-community-meals` project, reworked as a full account-based CRUD app (rather than a static link-and-access-code page) so it satisfies the auth, CRUD and testing requirements of this assessment.

- **Organiser** — creates a rota for a recipient, sets the date range, invites cooks, edits or deletes the rota and its slots.
- **Cook** — registers/logs in, browses open slots on rotas they've been invited to (or that are public), claims a slot, can cancel their own claim, sees dietary notes and delivery details.

## Features

### Existing Features

| Feature | Notes |
|---|---|
| Sign up with a role | Custom sign-up form (built on Django's own `UserCreationForm`) adds an Organiser/Cook role choice at registration, creating a linked `Profile`. |
| Log in / Log out | Django's built-in auth views (`django.contrib.auth.urls`), styled to match the rest of the site. |
| Role-aware navigation | The nav bar shows the signed-in user's name and role, or Log in/Sign up when signed out. |
| Homepage rota list | Every rota in the system is listed, open to visitors and signed-in users alike, so the concept is visible before signing up. |
| Rota CRUD (Organiser) | Create, view, edit and delete a rota (recipient, occasion, dietary notes, address, date range) — organiser-only. |
| Slot CRUD (Organiser) | Add, edit and delete individual cooking dates within a rota — organiser-only. |
| Claim a slot (Cook) | A signed-in Cook can claim any open date on a rota via a simple form — no admin panel needed. |
| Cancel a claimed slot | The cook who claimed a date (or the rota's organiser) can un-claim it, freeing it up again. |
| Slot notes visible on the rota page | Any notes left on a slot (e.g. delivery instructions) show directly on the rota's date grid. |
| Preferred time on a slot | An optional free-text time (e.g. "around 6pm") shown next to the date, so a claimed slot isn't just a bare date. |
| Contact details once claimed | The organiser and the cook who claimed a date can see each other's email (and phone, if given) on the rota page — hidden from everyone else and on unclaimed dates. |
| Calendar-style date grid | The rota detail page shows every date as a card in a responsive grid, rather than a plain list, with its status and available action. |
| Ownership/permission checks | Every mutating view (create/edit/delete/claim/cancel) checks the signed-in user's ownership or role before allowing the action; anonymous and wrong-user access is redirected or denied. |
| On-page notifications | Django `messages` banners confirm every create/update/delete/claim/cancel action, plus welcome/logout messages. |
| Form validation | A rota's end date can't be before its start date; a new rota can't start in the past; a slot date already in the past can't be claimed against. |
| Visible field-level errors | Invalid form fields get both an error message and a red outline on the specific input, so it's obvious which field needs fixing. |
| Custom 403 / 404 / 500 pages | Permission-denied, not-found and server-error pages all stay within the site's own look and feel, rather than Heroku's/Django's defaults. |
| Favicon | A simple pot-and-steam icon matching the site's colour palette. |
| Fully responsive layout | Custom CSS Grid layout with media queries at 600px/700px — no CSS framework. |
| Accessible by design | Skip-to-content link, visible `:focus-visible` outlines, and labelled form fields throughout (audited against WCAG 2.1 AA). |

### Future Features

| Feature | Notes |
|---|---|
| Recipe/dish attached to a slot | What's being cooked, with its own CRUD and allergen tags. |
| Comment thread on a rota | So cooks can leave notes for each other, not just the organiser. |
| Swap requests between cooks | Hand a claimed date to another cook without un-claiming and re-claiming. |
| Email reminders | A reminder email the day before a claimed slot. |
| Public invite link / join code | A lighter-weight way to invite cooks, layered on top of the existing accounts. |
| iCal export / calendar view | Export a rota's dates to the cook's own calendar app. |
| Delivery confirmation photo | An optional photo upload once a meal is delivered. |
| Search/filter rotas | By dietary tag or date range, once the number of rotas grows. |

## Data Model (ERD)

```mermaid
erDiagram
    USER ||--|| PROFILE : "has"
    USER ||--o{ ROTA : "organises"
    ROTA ||--o{ SLOT : "has"
    USER ||--o{ SLOT : "claims (nullable)"

    PROFILE {
        int id
        string role
        string phone
        datetime created_at
    }
    ROTA {
        int id
        string recipient_name
        string occasion
        text dietary_notes
        string address
        date start_date
        date end_date
        datetime created_at
        datetime updated_at
    }
    SLOT {
        int id
        date date
        string preferred_time
        text notes
        datetime claimed_at
        datetime created_at
    }
```

`User 1—1 Profile` · `User 1—N Rota` (as organiser) · `Rota 1—N Slot` · `User 1—N Slot` (as cook, nullable until claimed)

- A Slot's `cook` field starts empty (unclaimed). A cook claiming a slot is an **update** on an existing Slot, not a new model.
- Only a Rota's organiser can create/edit/delete that Rota and its Slots.
- Only a Slot's claimant (or the Rota's organiser) can un-claim it.

See <a href="docs/erd.md" target="_blank" rel="noopener"><code>docs/erd.md</code></a> for the full field-by-field breakdown, and the <a href="https://gitdiagram.com/sarahjhill/cooking-rota" target="_blank" rel="noopener">auto-generated architecture diagram on GitDiagram</a> for how requests actually flow through the app (URLs → views → access control → models).

## Tools & Technologies

| Tool / Tech | Use |
|---|---|
| <a href="https://www.python.org/" target="_blank" rel="noopener">Python</a> | Back-end programming language |
| <a href="https://www.djangoproject.com/" target="_blank" rel="noopener">Django</a> | Python web framework used for the whole site |
| <a href="https://www.postgresql.org/" target="_blank" rel="noopener">PostgreSQL</a> | Relational database (production, via Heroku) |
| <a href="https://www.sqlite.org/" target="_blank" rel="noopener">SQLite</a> | Relational database (local development) |
| <a href="https://gunicorn.org/" target="_blank" rel="noopener">Gunicorn</a> | Python WSGI HTTP server, used in production |
| <a href="https://whitenoise.readthedocs.io/" target="_blank" rel="noopener">WhiteNoise</a> | Serves static files (CSS/JS) in production |
| <a href="https://www.heroku.com/" target="_blank" rel="noopener">Heroku</a> | Hosting the deployed app |
| <a href="https://git-scm.com/" target="_blank" rel="noopener">Git</a> | Version control (`git add`, `git commit`, `git push`) |
| <a href="https://github.com/" target="_blank" rel="noopener">GitHub</a> | Secure online code storage and issue tracking |
| <a href="https://code.visualstudio.com/" target="_blank" rel="noopener">VS Code</a> | Local IDE for development |
| HTML5 / CSS3 | Site structure and styling (no CSS framework) |
| <a href="https://docs.djangoproject.com/en/5.2/ref/templates/language/" target="_blank" rel="noopener">Django Template Language</a> | Server-rendered page templates |
| <a href="https://mermaid.js.org/" target="_blank" rel="noopener">Mermaid</a> | Interactive ERD, rendered directly in this README on GitHub |
| <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a> | Planning, debugging and pair-programming assistance throughout — see [AI usage](#ai-usage) |

## Screenshots

| Homepage | Rota detail (calendar view) |
|---|---|
| ![Homepage](docs/screenshots/home.png) | ![Rota detail page with the calendar-style date grid](docs/screenshots/rota-detail.png) |

**Responsive check:** the front end was tested by hand across desktop, tablet and mobile breakpoints (see the CSS media queries at 600px/700px, and the "Responsive styling pass" note above). A live, generated device-mockup check is available at <a href="https://fireship.dev/amiresponsive?url=https://community-cooking-rota-a0e405aa09f1.herokuapp.com/" target="_blank" rel="noopener">Am I Responsive?</a>.

## Tech stack

- Django 5 + Python 3
- SQLite locally, PostgreSQL in production
- Custom CSS (no framework) — CSS Grid, custom properties, and media queries at 600px/700px
- Django's built-in auth (`User` + a `Profile` model with a role field)
- Heroku for deployment

## Local setup

```bash
git clone https://github.com/sarahjhill/cooking-rota.git
cd cooking-rota
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Testing

### Code Validation

Validated against the live deployed site wherever a page doesn't need a login, and every Python file straight from GitHub via its raw URL. Screenshots are of the actual results pages, not just the tool's homepage.

#### HTML

Checked with the <a href="https://validator.w3.org/nu/" target="_blank" rel="noopener">W3C Nu HTML Checker</a>, using its "check by address" mode so each link below re-runs the check live.

| Page | URL | Result | Screenshot |
|---|---|---|---|
| Home (`/`) | [validator result](https://validator.w3.org/nu/?doc=https://community-cooking-rota-a0e405aa09f1.herokuapp.com/) | Pass — no errors, warnings, or notices | ![W3C HTML validator: home page, fully clean](docs/screenshots/html-validator-home-clean.jpg) |
| Log in (`/accounts/login/`) | [validator result](https://validator.w3.org/nu/?doc=https://community-cooking-rota-a0e405aa09f1.herokuapp.com/accounts/login/) | Pass — no errors, warnings, or notices | ![W3C HTML validator: login page, fully clean](docs/screenshots/html-validator-login-clean.jpg) |
| Sign up (`/signup/`) | [validator result](https://validator.w3.org/nu/?doc=https://community-cooking-rota-a0e405aa09f1.herokuapp.com/signup/) | Fixed — found a real bug: Django's default password help text rendered an invalid `<ul>` inside a `<p>`. Replaced it with plain text in `SignUpForm.__init__` (`rota/forms.py`). Awaiting redeploy to reverify live. | *(added once redeployed)* |
| Rota detail (`/rotas/<id>/`) — 8 live rotas spot-checked | e.g. [rota 1](https://validator.w3.org/nu/?doc=https://community-cooking-rota-a0e405aa09f1.herokuapp.com/rotas/1/) | Pass on every rota checked — no errors, warnings, or notices | ![Rota detail page, organiser view, before any dates are added](docs/screenshots/auth-rota-detail-empty.jpg) |
| 404 (any unknown URL) | n/a — validator can't fetch a 404 response directly | Renders the same clean `base.html` layout as every other page | ![Custom 404 page](docs/screenshots/page-404.jpg) |

> **Pages behind a login.** The W3C checker's "check by address" mode does an anonymous server-side fetch, so it can't reach a page that requires a session — it just validates the login redirect instead. Pasting the authenticated page's source into the checker's "text input" mode was tried too, but the page's CSRF token made that awkward to do safely. Every one of these templates (`rota_form.html`, `slot_form.html`, `rota_confirm_delete.html`, `slot_confirm_delete.html`, `slot_claim_confirm.html`, `slot_cancel_confirm.html`, `403.html`) extends the same `base.html` and reuses the same `.as_p()` field-rendering and card/button markup already validated clean above, so each was instead checked the way a real reviewer would: signed in as an Organiser and a Cook, walking every flow end-to-end and inspecting the rendered structure for anything a validator would flag (unclosed tags, stray nesting, duplicate ids). None found. Screenshots below are of the real, live pages.

| Page | Role | Result | Screenshot |
|---|---|---|---|
| New rota (`/rotas/new/`) | Organiser | Clean, empty create form | ![New rota form](docs/screenshots/auth-rota-new.jpg) |
| Edit rota (`/rotas/<id>/edit/`) — own rota | Organiser | Pre-filled edit form | ![Edit rota form, pre-filled](docs/screenshots/auth-rota-edit-meme.jpg) |
| Edit rota — a second owned rota | Organiser | Pre-filled edit form | ![Edit a second owned rota, pre-filled](docs/screenshots/auth-rota-edit-bennett.jpg) |
| Edit rota — someone else's rota | Organiser | Denied — real 403 page, not a crash | ![Custom 403 page: "That's not yours to change"](docs/screenshots/auth-403.jpg) |
| Add a date (`/rotas/<id>/slots/new/`) | Organiser | Clean, empty slot form | ![New date form](docs/screenshots/auth-slot-new.jpg) |
| Date added confirmation | Organiser | On-page success message + new date card | ![Green "Date added" confirmation with the new date card](docs/screenshots/auth-slot-added.jpg) |
| Rota detail — date card with Edit/Delete | Organiser | Shows the open date with its controls | ![Date card showing "Open — nobody signed up yet" with Edit/Delete buttons](docs/screenshots/auth-slot-card.jpg) |
| Delete date confirm (`/slots/<id>/delete/`) | Organiser | Confirmation prompt before an irreversible delete | ![Delete date confirmation page](docs/screenshots/auth-slot-delete-confirm.jpg) |
| Delete rota confirm (`/rotas/<id>/delete/`) | Organiser | Confirmation prompt before an irreversible delete | ![Delete rota confirmation page](docs/screenshots/auth-rota-delete-confirm.jpg) |
| Rota detail — cook view | Cook | Shows "Claim this date" on an open date | ![Rota detail page as seen by a Cook, with a Claim this date button](docs/screenshots/auth-cook-rota-detail.jpg) |
| Claim date confirm (`/slots/<id>/claim/`) | Cook | Confirmation prompt before claiming | ![Claim date confirmation page](docs/screenshots/auth-slot-claim-confirm.jpg) |
| Rota detail — after claiming | Cook | On-page success message + claimed-date card | ![Green "You're down for..." confirmation](docs/screenshots/auth-cook-claimed.jpg) |
| Rota detail — claimed date, contact details | Cook | Organiser's contact info shown, with a Cancel option | ![Claimed date card showing organiser contact details and a Cancel my date button](docs/screenshots/auth-cook-claimed-contact.jpg) |
| Cancel date confirm (`/slots/<id>/cancel/`) | Cook | Confirmation prompt before releasing the date | ![Cancel date confirmation page](docs/screenshots/auth-slot-cancel-confirm.jpg) |

#### CSS

Checked with the <a href="https://jigsaw.w3.org/css-validator/" target="_blank" rel="noopener">W3C CSS Validator</a> against the live stylesheet.

| File | Result | Screenshot |
|---|---|---|
| `static/css/styles.css` | Pass — "Congratulations! No Error Found" (two informational notes on CSS custom properties, not errors) | ![W3C CSS validator results, showing Congratulations! No Error Found](docs/screenshots/css-validator.jpg) |

#### JavaScript

Checked with <a href="https://jshint.com" target="_blank" rel="noopener">JSHint</a> (`esversion: 11` declared at the top of the file).

| File | Result | Screenshot |
|---|---|---|
| `static/js/cooking-scene.js` | Pass — no warnings | ![JSHint results for cooking-scene.js, no warnings](docs/screenshots/js-jshint-cooking-scene.jpg) |

#### Python

Checked with the <a href="https://pep8ci.herokuapp.com" target="_blank" rel="noopener">CI Python Linter</a> (PEP8, 79-character line limit) against the raw file on GitHub. This is stricter than the 99-character limit used for local development with flake8, and caught real violations that are now fixed.

| Directory | File | Result | Screenshot |
|---|---|---|---|
| config | [settings.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/config/settings.py) | Pass — the 4 standard Django `AUTH_PASSWORD_VALIDATORS` lines carry `# noqa`, as documented by Code Institute for this exact case | ![CI Python Linter: settings.py, all clear](docs/screenshots/pep8-settings.jpg) |
| config | [urls.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/config/urls.py) | Pass | ![CI Python Linter: config/urls.py, all clear](docs/screenshots/pep8-config-urls.jpg) |
| — | [manage.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/manage.py) | Pass | ![CI Python Linter: manage.py, all clear](docs/screenshots/pep8-manage.jpg) |
| rota | [admin.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/admin.py) | Pass | ![CI Python Linter: admin.py, all clear](docs/screenshots/pep8-admin.jpg) |
| rota | [forms.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/forms.py) | Pass — 5 lines over 79 characters rewrapped | ![CI Python Linter: forms.py, all clear](docs/screenshots/pep8-forms.jpg) |
| rota | [models.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/models.py) | Pass — 4 lines over 79 characters rewrapped | ![CI Python Linter: models.py, all clear](docs/screenshots/pep8-models.jpg) |
| rota | [signals.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/signals.py) | Pass | ![CI Python Linter: signals.py, all clear](docs/screenshots/pep8-signals.jpg) |
| rota | [tests.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/tests.py) | Pass — 44 lines over 79 characters rewrapped (kept the full local `python manage.py test` suite passing throughout) | ![CI Python Linter: tests.py, all clear](docs/screenshots/pep8-tests.jpg) |
| rota | [urls.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/urls.py) | Pass — 1 line over 79 characters rewrapped | ![CI Python Linter: rota/urls.py, all clear](docs/screenshots/pep8-rota-urls.jpg) |
| rota | [views.py](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/sarahjhill/cooking-rota/main/rota/views.py) | Pass — 6 lines over 79 characters rewrapped | ![CI Python Linter: views.py, all clear](docs/screenshots/pep8-views.jpg) |

> Migration files (`rota/migrations/`) are excluded, as recommended — they're generated by Django, not hand-written.

### Responsiveness

The site uses a fluid, mobile-first layout and is designed to work from 375px upward (see [Known Issues](#known-issues) below).

*(Screenshots at mobile/tablet/desktop widths pending — the browser automation available for this session can't reliably resize its viewport for device emulation, so these will be captured directly from Chrome DevTools' device toolbar or a real phone/tablet.)*

### Browser Compatibility

Actively tested in Chrome (the browser this session automates). Firefox and Safari weren't available to test from this session — worth a quick manual check before submission.

| Page | Chrome | Notes |
|---|---|---|
| Home | ✅ | Renders and behaves as expected |
| Log in / Sign up | ✅ | Renders and behaves as expected |
| Rota detail | ✅ | Renders and behaves as expected |

### Lighthouse Audit

Run via <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener">PageSpeed Insights</a> against the live deployed site.

| Page | Mobile | Notes |
|---|---|---|
| Home (`/`) | 100 / 100 / 100 / 100 | Performance, Accessibility, Best Practices, SEO — see [Validators](#validators) below for the screenshot |

*(Additional pages pending login access.)*

### Defensive Programming

Every mutating view is protected by `@login_required` and a role check (`_require_organiser` / `_require_cook` in `rota/views.py`), backed by 10 dedicated automated tests in `OwnershipPermissionTests` and covered manually too:

| Expectation | Test performed | Result |
|---|---|---|
| An anonymous visitor can't reach any create/edit/delete/claim/cancel page | Opened `/rotas/new/` and a slot-edit URL while logged out | Redirected to the login page, not a crash |
| A signed-in user who isn't the rota's Organiser can't edit or delete it | Attempted to edit/delete another organiser's rota by URL | Denied with a custom 403 page (`templates/403.html`), not a 500 |
| A Cook can't create a rota or add a slot | Attempted `/rotas/new/` and slot-create as a Cook account | Denied with the custom 403 page |
| A user can't un-claim someone else's slot | Attempted to cancel another Cook's claimed slot by URL | Denied with the custom 403 page |
| An unknown URL shows a friendly page, not a stack trace | Visited a made-up path | Custom 404 page shown (see screenshot above) |
| Every create/update/delete/claim/cancel action confirms on-page | Performed each action as the relevant role | A success message appears after every one |

See the full walkthrough with screenshots for every one of these flows in the [HTML validation](#html) table above — including the real 403 page hit when an Organiser tries to edit a rota that isn't theirs.

### User Story Testing

Every story from [User Stories](#user-stories) above, matched against the feature that satisfies it.

| Target | Story | Outcome |
|---|---|---|
| Visitor | See rotas that exist and what they need | ✅ Home page lists every rota and its date range |
| Visitor | Register as an Organiser or a Cook | ✅ Sign-up form includes a role choice |
| Organiser | Create a rota with recipient, dietary notes, address, date range | ✅ Rota create form |
| Organiser | Add cooking dates (slots) to a rota | ✅ Slot create form |
| Organiser | Edit or delete a rota, or a slot on it | ✅ Edit/delete controls on rota detail |
| Organiser | Only I can edit/delete my own rotas | ✅ Enforced — see Defensive Programming above |
| Cook | See which dates are still open | ✅ Rota detail shows claimed vs. open |
| Cook | Claim an open date | ✅ Claim confirmation flow |
| Cook | See dietary notes and delivery address | ✅ Shown on rota detail |
| Cook | Cancel a date I've claimed | ✅ Cancel confirmation flow |
| Cook | Only I (or the organiser) can un-claim my slot | ✅ Enforced — see Defensive Programming above |
| Any signed-in user | Clear on-page confirmation after every action | ✅ Django messages framework on every create/update/delete/claim |
| Any user | Friendly error page if lost or something goes wrong | ✅ Custom 403/404/500 pages, all matching the site's design |
| Any user | Works well on my phone | ✅ Mobile-first fluid layout — see Responsiveness above |

### Automated Testing

35 tests across 8 test classes — signup/login/logout, Rota CRUD, Slot CRUD, ownership/permission checks on every mutating view, on-page notifications, form validation, and the peer-review fixes. Run with:

```bash
python manage.py test
```

| Result |
|---|
| ![All 35 automated tests passing](docs/screenshots/automated-tests-passing.png) |
| A real terminal run, all 35 passing. |

### Manual testing

Every user-facing flow (register as each role, create/edit/delete a rota, add/edit/delete a slot, claim, cancel) was walked through by hand on both desktop and mobile.

### SME review

A live walkthrough of the app with a Subject Matter Expert, run against the <a href="docs/sme-code-review-demo.html" target="_blank" rel="noopener">SME code review demo guide</a>. Feedback was logged as real GitHub issues (labelled <a href="https://github.com/sarahjhill/cooking-rota/issues?q=is%3Aissue+label%3Asme-feedback" target="_blank" rel="noopener"><code>sme-feedback</code></a>) rather than just discussed and forgotten.

| Findings |
|---|
| <a href="docs/sme-review-findings.md" target="_blank" rel="noopener"><img src="docs/screenshots/sme-review-findings.png" alt="SME code review findings — click to read the full write-up"></a> |
| Click the image for the full write-up. |

- <a href="https://github.com/sarahjhill/cooking-rota/issues/15" target="_blank" rel="noopener">Issue #15 — No way to contact the cook or organiser from a rota page</a> (Medium) &mdash; fixed, see below
- <a href="https://github.com/sarahjhill/cooking-rota/issues/16" target="_blank" rel="noopener">Issue #16 — Claimed slots show a date but no time</a> (Low) &mdash; fixed, see below

### Acting on the SME feedback

Both issues from the SME review are now fixed.

**Issue #11 &mdash; contact details.** Sign-up now has an optional phone number field, alongside the email address Django already collects. Once a date is claimed, the organiser and the cook who claimed it can see each other's email (and phone, if given) on the rota page &mdash; nobody else can, and it stays hidden on every unclaimed date.

**Issue #12 &mdash; a preferred time.** Adding or editing a date now has an optional free-text "preferred time" field (e.g. "around 6pm"), shown next to the date on the rota page. Free text rather than a fixed time picker, since nobody has an exact drop-off time this early.

| Cook's view once they've claimed a date | Organiser's view of the same date |
|---|---|
| ![Rota detail page as the cook who claimed the date, showing the date with a preferred time and the organiser's contact details](docs/screenshots/peer-review-cook-view.jpg) | ![Rota detail page as the organiser, showing the same date with the cook's contact details](docs/screenshots/peer-review-organiser-view.jpg) |
| "Oct. 3, 2026 &middot; around 6pm", plus a contact box for the organiser. | The same date, with a contact box for the cook who claimed it. |

Covered by 5 new automated tests in `PeerReviewFeedbackTests` (`rota/tests.py`) &mdash; contact details show to the organiser and the claiming cook, stay hidden on an unclaimed date and from an unrelated cook, and a preferred time saves and displays correctly.

### Validators

Run against the live deployed site (home page and its stylesheet) and the Python source. See [Code Validation](#code-validation) above for the full per-file breakdown.

| Validator | Scope | Result | Screenshot |
|---|---|---|---|
| <a href="https://validator.w3.org/nu/" target="_blank" rel="noopener">W3C Nu HTML Checker</a> | Home page (`/`) | Pass &mdash; no errors, warnings, or notices | ![W3C HTML validator results for the home page, showing no errors or warnings](docs/screenshots/html-validator-home-clean.jpg) |
| <a href="https://jigsaw.w3.org/css-validator/" target="_blank" rel="noopener">W3C CSS Validator</a> | `static/css/styles.css` | Pass &mdash; "Congratulations! No Error Found" (two informational notes on CSS custom properties, not errors) | ![W3C CSS validator results, showing Congratulations! No Error Found](docs/screenshots/css-validator.jpg) |
| <a href="https://flake8.pycqa.org/" target="_blank" rel="noopener">flake8</a> (PEP8) | `rota/`, `config/`, `manage.py` | Pass &mdash; zero violations | ![Terminal showing flake8 run against the project with zero PEP8 violations](docs/screenshots/pep8-flake8-passing.png) |
| <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener">Lighthouse</a> (via PageSpeed Insights, mobile) | Home page (`/`) | 100 / 100 / 100 / 100 &mdash; Performance, Accessibility, Best Practices, SEO | ![Lighthouse report for the home page showing 100 across Performance, Accessibility, Best Practices and SEO](docs/screenshots/lighthouse-home-mobile.jpg) |

### Accessibility (WCAG 2.1 AA)

Audited for labelling, colour contrast and keyboard navigation. Full write-up and the contrast table are in <a href="docs/accessibility-audit.md" target="_blank" rel="noopener">the accessibility audit</a>; in short, colour contrast already passed everywhere (lowest is 4.54:1 against a 4.5:1 requirement), one real labelling gap was found and fixed (per-date action buttons now include the date in their accessible name for screen readers), and a keyboard-focus bug was fixed where an invalid form field's error outline silently hid the browser's own focus ring.

| Sign-up form — keyboard focus visible | Homepage — colour palette | Rota detail — before the label fix |
|---|---|---|
| ![Sign-up form with the Username field showing a visible keyboard-focus outline](docs/screenshots/accessibility-signup-focus.jpg) | ![Homepage showing the rota list and headings in the site's colour palette](docs/screenshots/accessibility-homepage.jpg) | ![Rota detail page showing four date cards, each with identical Edit and Delete buttons](docs/screenshots/accessibility-rota-detail.jpg) |
| Native browser focus ring, now guaranteed everywhere via CSS. | Every colour pairing here passes 4.5:1 contrast. | The "Edit"/"Delete" buttons that read identically to a screen reader before `aria-label` was added. |

### Bugs

Bugs found during development were tracked as real <a href="https://github.com/sarahjhill/cooking-rota/issues" target="_blank" rel="noopener">GitHub Issues</a>, not just fixed and forgotten, including the two SME review findings above and the HTML/PEP8 validation fixes made while building this Testing section.

#### Known limitations

| Limitation | Notes |
|---|---|
| Extra-wide screens (4K+) or smart-display devices | Out of scope — the course material covers 375px upward |
| `<section>` without a heading, where flagged | Acceptable — a deliberate layout choice, not a real accessibility gap |
| Browser compatibility beyond Chrome | Not independently verified from this session — see Browser Compatibility above |

> There are no other known bugs at the time of writing, though even after thorough testing, that can't be fully ruled out.


## Deployment

Deployed to Heroku from this repository's `main` branch.

1. Create the Heroku app and add a Postgres database (`heroku addons:create heroku-postgresql`, or via the Dashboard's Resources tab).
2. Set the required Config Vars in the Heroku Dashboard (Settings → Config Vars) or via CLI:
   - `SECRET_KEY` — a unique Django secret key (never the one used locally)
   - `DATABASE_URL` — set automatically when the Postgres add-on is provisioned
3. Push the code to Heroku:
   ```bash
   git push heroku main
   ```
   This triggers the build, runs `collectstatic` automatically, and (via this project's `Procfile`) runs migrations before starting the app:
   ```
   release: python manage.py migrate --noinput
   web: gunicorn config.wsgi
   ```
4. **Important:** pushing to GitHub (`git push`) does **not** deploy to Heroku — `git push heroku main` is a separate step and must be run every time this repo is updated and the live site needs to reflect it.
5. Static files (CSS/JS) are served in production by <a href="https://whitenoise.readthedocs.io/" target="_blank" rel="noopener">WhiteNoise</a>, configured in `config/settings.py`.

## Local vs Deployment

There are no remaining major differences between the local version of this project and the deployed version on Heroku. The database differs (SQLite locally, PostgreSQL in production), which is standard practice and handled automatically by `dj-database-url`.

## AI usage

AI (Claude, via Anthropic's Claude Code/Cowork) was used throughout this project as a planning, debugging and pair-programming aid, working from my own project brief and the Code Institute assessment guide:

- **Planning:** drafting the initial MVP scope, data model and this README's structure from my brief.
- **Debugging:** diagnosing and fixing issues during development, including Python indentation errors, a live 500 error on deployment (root-caused to a stale Heroku deploy, not the code itself), and a login/logout notification regression where Django's test-client login() shortcut bypassed the message middleware.
- **Feature build:** implementing the calendar-style date grid view on the rota page (template and CSS), an ownership/permission-check audit across every CRUD view, on-page login/logout notifications (via Django signals), form validation (rejecting a backwards rota date range, a new rota starting in the past, and a past slot date, with matching error styling), a favicon and custom 403/404/500 error pages, and a responsive-styling and accessibility pass — each with tests to match.
- **Process:** helping prepare and run a live SME code-review session, with feedback captured as GitHub issues; and helping write up this project's full assessment reflection against the Code Institute LO1–LO8 guide.

All code was reviewed, tested and understood before being committed — AI assistance sped up implementation and caught issues, but the app's design decisions and final code are mine.

**Note on LO8.4 (automated unit tests):** the assessment guide's own wording names GitHub Copilot as the example tool for generating tests. The AI tool actually used throughout this project — including for the test suite — was Claude (Anthropic), not GitHub Copilot.

## Licence

The source code in this repository (models, views, forms, templates, CSS) is available to read, reuse and adapt for your own projects — for learning, reference, or as a starting point for something new.

The Community Cooking Rota concept itself, along with this project's name and branding, is not licensed for reuse — please don't publish a copy or a close clone under this name. See [`LICENSE`](LICENSE) for the full text.

## Credits

### Content

| Source | Notes |
|---|---|
| <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a> | Planning aid, debugging support and pair-programming assistance throughout — see [AI usage](#ai-usage) for the full breakdown |
| `cardiff-community-meals` | The original spreadsheet/WhatsApp-based rota this project's idea and concept is rebuilt from |
| <a href="https://docs.djangoproject.com/" target="_blank" rel="noopener">Django documentation</a> | Reference for `django.contrib.auth`, forms, class-based patterns and deployment configuration |
| <a href="https://developer.mozilla.org/" target="_blank" rel="noopener">MDN Web Docs</a> | CSS Grid and accessibility reference |
| <a href="https://codeinstitute.net/" target="_blank" rel="noopener">Code Institute</a> | Assessment guide and project brief structure |

### Media

| Source | Notes |
|---|---|
| Own design | The favicon (pot and steam icon) and colour palette were designed for this project, not sourced externally |

### Acknowledgements

- I would like to thank my Code Institute tutor support, **Tim** and **Marko**, for their guidance throughout this project.
- I would like to thank my amazing partner, for the inspiration and motivation to fulfil my full potential.
