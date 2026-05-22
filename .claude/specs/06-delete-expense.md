# Spec: Delete Expense

## Overview
This step replaces the stub `GET /expenses/<id>/delete` route with a real
`POST /expenses/<id>/delete` endpoint that permanently removes an expense
from the database. Only the authenticated owner of the expense may delete it;
any other access results in a 403. After deletion the user is redirected back
to their profile. No confirmation page is needed — the delete button in the
profile table acts as a small inline form that POSTs directly to the route.

## Depends on
- Step 01 — Database setup (`expenses` table, `get_db()`)
- Step 04 — Profile page (`profile.html` expense table)
- Step 05 — Edit expense (establishes ownership-check pattern this step follows)

## Routes
- `POST /expenses/<id>/delete` — Delete the expense with the given id — logged-in only

The existing `GET /expenses/<int:id>/delete` stub must be replaced. The new
route accepts `POST` only; a bare `GET` to that URL should return 405.

## Database changes
No new tables or columns. One new helper function:

```python
def delete_expense(expense_id, user_id) -> int:
    # DELETE FROM expenses WHERE id = ? AND user_id = ?
    # Returns rowcount (1 on success, 0 if not found or not owner)
```

## Templates
- **Modify:** `templates/profile.html` — replace the placeholder or add a
  delete button beside each expense row. Each button must be wrapped in a
  `<form method="post" action="{{ url_for('delete_expense', expense_id=expense.id) }}">`.
  No JavaScript required; the form submits via standard HTML POST.

## Files to change
- `app.py` — replace the stub `delete_expense` route with a real POST handler
- `database/db.py` — add `delete_expense(expense_id, user_id)` helper
- `templates/profile.html` — add delete button form to each expense row
- `static/css/style.css` — add style for the delete button if needed (use
  existing `--danger` CSS variable; do not hardcode hex values)

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with werkzeug (not relevant here, listed for completeness)
- Use CSS variables — never hardcode hex values (`--danger` for the delete button)
- All templates extend `base.html`
- Route must be `POST` — do not implement as `GET`; destructive actions must
  not be triggerable via a plain link/URL visit
- Ownership check is mandatory — `abort(403)` if `expense["user_id"] != session["user_id"]`
- `abort(404)` if the expense does not exist
- After successful deletion, `redirect(url_for("profile"))`
- Import `delete_expense` in `app.py` alongside the other db helpers

## Definition of done
- [ ] Visiting `GET /expenses/<id>/delete` returns 405 (Method Not Allowed)
- [ ] POSTing to `/expenses/<id>/delete` as the owner deletes the row and redirects to `/profile`
- [ ] The deleted expense no longer appears in the profile expense table
- [ ] POSTing with a valid id but a different logged-in user returns 403
- [ ] POSTing with a non-existent id returns 404
- [ ] The profile page shows a delete button for every expense row
- [ ] No raw SQL strings or f-strings used in the new DB helper
- [ ] The delete button uses the `--danger` CSS variable for its color
