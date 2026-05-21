# Spec: Profile

## Overview
This step implements the profile page — the first route protected by the session guard. After a successful login, users land here and see their name, email, and a table of their expenses. It is the app's main authenticated view and introduces the pattern that all future protected routes will follow: check `session["user_id"]`, redirect to `/login` if absent, otherwise load the user and render. It also adds `get_expenses_by_user_id()` to the DB layer, and updates the `base.html` navbar to show context-aware links (Sign in / Get started when logged out; Profile / Sign out when logged in).

## Depends on
- Step 01 — Database setup (`get_db()`, `users` + `expenses` tables)
- Step 02 — Registration
- Step 03 — Login (`session["user_id"]` contract, `get_user_by_id()`)

## Routes
- `GET /profile` — display user info and expense list — logged-in only (currently a raw-string stub)

## Database changes
No new tables or columns. One new helper needed in `database/db.py`:
- `get_expenses_by_user_id(user_id)` — returns all expense rows for the given user, ordered by `date DESC`

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; shows user name, email, joined date, and a table of expenses (date, category, amount, description); includes a prominent "Add expense" button pointing to `url_for('add_expense')` (stub route is fine)
- **Modify:** `templates/base.html` — update the `nav-links` block to show different links depending on session state:
  - Logged out: "Sign in" → `url_for('login')` and "Get started" → `url_for('register')` (current behaviour)
  - Logged in: "Profile" → `url_for('profile')` and "Sign out" → `url_for('logout')`

## Files to change
- `app.py` — replace raw-string `/profile` stub with a real handler: session guard + load user + load expenses + render template; add `get_expenses_by_user_id` to db import
- `database/db.py` — add `get_expenses_by_user_id(user_id)`
- `templates/base.html` — update navbar links with `{% if session.get("user_id") %}` conditional

## Files to create
- `templates/profile.html`

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with werkzeug (no change here, but rule applies globally)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives in `database/db.py` only — no raw SQL in route functions
- Session guard pattern: `if not session.get("user_id"): return redirect(url_for("login"))` — use this exact pattern; do not use `abort()`
- `get_expenses_by_user_id` must order results by `date DESC`
- The "Add expense" button must use `url_for('add_expense')` — never hardcode the URL

## Definition of done
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] After logging in, `/profile` loads without errors and shows the logged-in user's name and email
- [ ] The expense table lists the correct expenses for the logged-in user (verify with the demo user who has 8 seeded expenses)
- [ ] Expenses are ordered most-recent first
- [ ] An "Add expense" button is visible on the page
- [ ] The navbar shows "Profile" and "Sign out" links when logged in
- [ ] The navbar shows "Sign in" and "Get started" links when logged out
- [ ] Clicking "Sign out" in the navbar logs the user out and redirects to `/login`
- [ ] Two different users each see only their own expenses (not each other's)