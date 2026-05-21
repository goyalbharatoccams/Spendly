# Spec: Edit Expense

## Overview
This step lets logged-in users update an existing expense through a form at `/expenses/<id>/edit`. The route currently returns a raw string stub. This feature replaces it with a real GET+POST handler: GET fetches the expense, verifies ownership, and renders a form pre-filled with the existing values; POST validates the input, updates the row via new DB helpers, and redirects back to `/profile`. It also protects against horizontal privilege escalation — a user must own the expense to edit it.

## Depends on
- Step 01 — Database setup (`expenses` table, `get_db()`)
- Step 03 — Login (`session["user_id"]` contract)
- Step 04 — Profile (`/profile` redirect target after save; edit links live on the expense table there)
- Step 07 — Add Expense (establishes the form pattern and category list this feature mirrors)

## Routes
- `GET /expenses/<int:expense_id>/edit` — render edit form pre-filled with existing expense data — logged-in only
- `POST /expenses/<int:expense_id>/edit` — validate and update expense, redirect to `/profile` — logged-in only

## Database changes
No new tables or columns. Two new helpers needed in `database/db.py`:
- `get_expense_by_id(expense_id)` — returns the single expense row matching `id`, or `None` if not found
- `update_expense(expense_id, user_id, amount, category, date, description)` — updates the matching row only when `user_id` matches (ownership check in SQL via `WHERE id = ? AND user_id = ?`); returns the number of rows affected

## Templates
- **Create:** `templates/edit_expense.html` — extends `base.html`; form with amount, category (select), date, description (optional); inline error display; cancel link back to `/profile`; fields pre-filled with existing values on GET and with submitted values on failed POST
- **Modify:** `templates/profile.html` — add an "Edit" link/button per expense row pointing to `url_for("edit_expense", expense_id=expense.id)`

## Files to change
- `app.py` — replace raw-string stub with combined GET+POST handler; add session guard; add ownership check (404 if expense not found, 403 if user doesn't own it); import `get_expense_by_id` and `update_expense` from `database.db`
- `database/db.py` — add `get_expense_by_id()` and `update_expense()`
- `templates/profile.html` — add Edit action link per expense row
- `static/css/style.css` — reuse or extend existing form styles; add any edit-specific overrides

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with werkzeug (no change here, rule applies globally)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session guard: `if not session.get("user_id"): return redirect(url_for("login"))`
- Ownership check: use `abort(403)` if the expense exists but belongs to a different user; use `abort(404)` if the expense doesn't exist at all
- The ownership check must happen in the SQL (`WHERE id = ? AND user_id = ?`) not just in Python — do not fetch all expenses and filter in memory
- DB logic in `database/db.py` only — no raw SQL in routes
- Category must be validated server-side against the fixed list: `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`
- Amount must be a positive number (> 0) — validate server-side
- Date must be a non-empty string in `YYYY-MM-DD` format — strip before storing
- Description is optional — store `None` if blank
- On success: `redirect(url_for("profile"))`
- On failure: re-render the form with `error=` and previously submitted `amount`, `category`, `date`, `description` preserved (not the original DB values)

## Definition of done
- [ ] Visiting `/expenses/<id>/edit` without being logged in redirects to `/login`
- [ ] Visiting `/expenses/999/edit` (non-existent ID) returns 404
- [ ] Visiting another user's expense edit URL returns 403
- [ ] `GET /expenses/<id>/edit` renders the form with all fields pre-filled from the database
- [ ] Submitting with a blank or zero amount re-renders the form with an error and previously entered values preserved
- [ ] Submitting with an invalid category re-renders with an error
- [ ] Submitting with a blank date re-renders with an error
- [ ] Submitting valid data updates the row in `expenses` and redirects to `/profile`
- [ ] The updated expense reflects the new values on `/profile`
- [ ] Description is optional — clearing it and saving stores `None` without error
- [ ] The "Cancel" link returns to `/profile` without saving any changes
- [ ] An "Edit" link is visible per expense row on `/profile` and navigates to the correct edit URL
