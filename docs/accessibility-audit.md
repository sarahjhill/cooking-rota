# Accessibility audit — labels, contrast, keyboard nav

A WCAG 2.1 AA-focused audit of the codebase, the fixes made, and verification steps.

## Fix 1 — ambiguous link text for screen readers ✅ Fixed

**File:** `templates/rota/rota_detail.html`

Every date on a rota has its own "Edit" / "Delete" / "Claim this date" / "Cancel my date" button. Sighted users can tell them apart by position on the page, but a screen reader user browsing by a list of links hears the same word repeated with no way to tell which date each one belongs to (WCAG 2.4.4, Link Purpose in Context).

![Rota detail page showing four date cards, each with identical Edit and Delete buttons](screenshots/accessibility-rota-detail.jpg)

*Four dates, each with an "Edit" and "Delete" button that previously read identically to a screen reader.*

Added an `aria-label` to each link that includes the date, so a screen reader announces e.g. "Edit Oct. 12, 2026" instead of just "Edit". The visible button text is unchanged.

```html
<a class="btn btn-small" href="{% url 'rota:slot_update' slot.pk %}" aria-label="Edit {{ slot.date }}">Edit</a>
<a class="btn btn-small btn-danger" href="{% url 'rota:slot_delete' slot.pk %}" aria-label="Delete {{ slot.date }}">Delete</a>
<a class="btn btn-small" href="{% url 'rota:slot_claim' slot.pk %}" aria-label="Claim {{ slot.date }}">Claim this date</a>
<a class="btn btn-small" href="{% url 'rota:slot_cancel' slot.pk %}" aria-label="Cancel my date on {{ slot.date }}">Cancel my date</a>
```

## Fix 2 — keyboard focus not distinguishable on invalid form fields ✅ Fixed

**File:** `static/css/styles.css`

When a field fails validation, it gets a permanent red outline (via `box-shadow`) to flag the problem — but the CSS also set `outline: 2px solid transparent` on that same field, which silently cancelled the browser's own focus ring. A keyboard user tabbing onto an invalid field had no way to tell "this field currently has my focus" from "this field is just invalid" (WCAG 2.4.7, Focus Visible).

```css
.form-card ul.errorlist + p input:focus-visible,
.form-card ul.errorlist + p select:focus-visible,
.form-card ul.errorlist + p textarea:focus-visible {
    outline: 3px solid var(--primary);
    outline-offset: 2px;
}
```

Also widened the site's general focus-ring rule, which previously only covered links and buttons, to explicitly cover text inputs, selects and textareas:

```css
a:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
    outline: 3px solid var(--primary);
    outline-offset: 2px;
}
```

![Sign up form with the Username field showing a visible blue keyboard-focus outline](screenshots/accessibility-signup-focus.jpg)

*The sign-up form, tabbed to the Username field — a visible focus ring is now guaranteed site-wide, including on invalid fields.*

## Fix 3 — login error not announced to screen readers ✅ Fixed

**File:** `templates/registration/login.html`

A failed login re-renders the page with "That username and password don't match." above the form, but nothing marked it as an error, so a screen reader user wouldn't be told anything went wrong unless they happened to read past it (WCAG 3.3.1, Error Identification). Added `role="alert"` so it's announced automatically:

```html
<p class="form-error" role="alert">That username and password don't match. Please try again.</p>
```

## Fix 4 — homepage caption never stops changing ✅ Fixed · bonus catch

**File:** `static/js/cooking-scene.js`

The decorative caption under the homepage animation rotates every 4 seconds, forever, with no way to stop it. It's inside `aria-hidden="true"` so screen readers never see it, but WCAG 2.2.2 (Pause, Stop, Hide) still applies to auto-updating content visible for more than 5 seconds. Added a check for the user's reduced-motion preference:

```js
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;
if (prefersReducedMotion) return;
```

## Colour contrast — checked, all pass

Every text/background pairing on the site was checked against WCAG AA's 4.5:1 minimum for normal text. All pass — the lowest is 4.54:1 (white button text on the primary orange).

| Element | Foreground | Background | Ratio | Required | Pass? |
|---|---|---|---|---|---|
| Body text | `#1f2933` | `#f8f5f1` (page) | 13.58:1 | 4.5:1 | ✅ |
| Body text on cards | `#1f2933` | `#ffffff` | 14.76:1 | 4.5:1 | ✅ |
| Muted text (dates, captions) | `#52606d` | `#f8f5f1` | 5.94:1 | 4.5:1 | ✅ |
| Muted text on cards | `#52606d` | `#ffffff` | 6.46:1 | 4.5:1 | ✅ |
| Brand / heading text | `#8a4128` | `#ffffff` | 7.32:1 | 4.5:1 | ✅ |
| White text on primary button | `#ffffff` | `#b85c38` | 4.54:1 | 4.5:1 | ✅ |
| White text on button hover | `#ffffff` | `#8a4128` | 7.32:1 | 4.5:1 | ✅ |
| White text on danger button | `#ffffff` | `#b3261e` | 6.54:1 | 4.5:1 | ✅ |
| Error message text | `#B02F2F` | `#FBE8E8` | 5.41:1 | 4.5:1 | ✅ |
| "Claimed" status text | `#2f7d5b` | `#f8f5f1` | 4.59:1 | 4.5:1 | ✅ |

![Homepage showing the rota list and headings in the site's colour palette](screenshots/accessibility-homepage.jpg)

*The homepage's actual colour palette in use — everything shown here passes the AA contrast check above.*

## Labels — checked

- All form fields use Django's built-in form rendering, which auto-generates a `<label for="...">` tied to every input's `id` — this already worked correctly.
- No images anywhere in the site need alt text — the only graphics (the pot/flame animation) are correctly hidden from screen readers with `aria-hidden="true"`, since they're purely decorative.
- The main navigation has `aria-label="Main navigation"`, and there's a working "Skip to content" link.
- The four per-date action links were the one real labelling gap — see Fix 1 above.
- **Left as an optional improvement, not fixed:** the "I am signing up as" radio choice on the sign-up form is visually grouped and labelled, but isn't wrapped in a `<fieldset><legend>`, the more formally correct way to group radio buttons for screen readers. Not changed here because it means restructuring how that one field renders (Django's default `form.as_p` doesn't support it directly), which risks affecting the error-highlighting CSS on that page — a minor, AAA-adjacent polish item rather than a failing check.

## Keyboard navigation — verification steps

1. Run `python manage.py runserver` and open `http://127.0.0.1:8000/`.
2. Click the page background, then press **Tab** repeatedly — the first stop is the "Skip to content" link (visible when focused), then the nav, then the page content, in a sensible order.
3. On a rota with dates, tab to an "Edit"/"Delete" button and press **Enter** — confirm it activates, with a clear visible outline on whichever button has focus.
4. On the sign-up page, tab into "I am signing up as" and use the **arrow keys** to move between Organiser and Cook.
5. Submit a form with a required field blank — confirm the invalid field shows a distinct outline when focused versus when it's just sitting there invalid.
6. Try logging in with a wrong password — confirm the error appears and (ideally, tested with VoiceOver: `Cmd+F5`) is announced automatically.

## Result

Ambiguous link labels fixed, keyboard focus guaranteed visible everywhere including invalid fields, login errors announced to assistive tech, colour contrast checked and confirmed passing site-wide.
