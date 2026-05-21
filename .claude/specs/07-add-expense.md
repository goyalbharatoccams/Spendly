# Spec: Add Expense

## Overview
This step lets logged-in users record a new expense through a form at `/expenses/add`. The route currently returns a raw string stub. This feature replaces it with a real GET+POST handler: GET renders the form pre-filled with today's date; POST validates the input, inserts the row via a new `add_expense()` DB helper, and redirects back to `/profile`. It is the first step where users write data to the `expenses` table themselves.

## Depends on
- Step 01 — Database setup (`expenses` table, `get_db()`)
- Step 03 — Login (`session["user_id"]` contract)
- Step 04 — Profile (`/profile` redirect target after save)

## Routes
- `GET /expenses/add` — render add-expense form — logged-in only (currently a raw-string stub)
- `POST /expenses/add` — validate and insert expense, redirect to `/profile` — logged-in only

## Database changes
No new tables or columns. One new helper needed in `database/db.py`:
- `add_expense(user_id, amount, category, date, description)` — inserts one row into `expenses`, returns the new `id`

## Templates
- **Create:** `templates/add_expense.html` — extends `base.html`; form with amount, category (select), date, description (optional); inline error display; cancel link back to `/profile`

## Files to change
- `app.py` — replace raw-string stub with combined GET+POST handler; add session guard; import `add_expense` from `database.db`
- `database/db.py` — add `add_expense()`
- `static/css/style.css` — add styles for the add-expense form page

## Files to create
- `templates/add_expense.html`

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with werkzeug (no change here, rule applies globally)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session guard: `if not session.get("user_id"): return redirect(url_for("login"))`
- DB logic in `database/db.py` only — no raw SQL in the route
- Category must be validated server-side against the fixed list: `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`
- Amount must be a positive number (> 0) — validate server-side; the input type="number" alone is not sufficient
- Date must be a non-empty string in `YYYY-MM-DD` format — pass it through as-is after stripping
- Description is optional — store `None` if blank
- On success: `redirect(url_for("profile"))`
- On failure: re-render the form with `error=`, and previously entered `amount`, `category`, `date`, `description` preserved

## Definition of done
- [ ] Visiting `/expenses/add` without being logged in redirects to `/login`
- [ ] `GET /expenses/add` renders the form with today's date pre-filled in the date input
- [ ] Submitting with a blank or zero amount re-renders the form with an error
- [ ] Submitting with an invalid category (e.g. manually crafted POST) re-renders with an error
- [ ] Submitting with a blank date re-renders with an error
- [ ] Submitting valid data inserts a row in `expenses` and redirects to `/profile`
- [ ] The new expense appears at the top of the expense table on `/profile` (most-recent first)
- [ ] Description is optional — submitting without it still works
- [ ] Previously entered values are preserved in the form after a failed submission
- [ ] The "Cancel" link returns to `/profile` without any changes