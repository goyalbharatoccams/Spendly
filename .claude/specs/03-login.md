# Spec: Login and Logout

## Overview
This step makes authentication functional end-to-end. The `GET /login` route and `login.html` template already exist; this feature adds the `POST /login` handler (validates credentials, writes a Flask session), implements `GET /logout` (clears the session and redirects), and adds a `get_user_by_id()` DB helper for loading the current user from the session. On successful login the user is redirected to `/profile`; on failure the form re-renders with an error and the entered email preserved. This is the first step that writes to `flask.session`, so it also locks in the session contract (`session['user_id']`) that all future protected routes will depend on.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` table)
- Step 02 — Registration (`get_user_by_email()`, `app.secret_key`)

## Routes
- `GET /login` — render login form — public (already exists, no change needed)
- `POST /login` — validate credentials, write session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — public (currently a raw-string stub)

## Database changes
No new tables or columns. One new helper needed in `database/db.py`:
- `get_user_by_id(user_id)` — returns the matching `users` row or `None`; used to load the current user from `session['user_id']`

## Templates
- **Modify:** `templates/login.html`
  - Replace hardcoded `action="/login"` with `action="{{ url_for('login') }}"`
  - Add `value="{{ email or '' }}"` to the email input so it survives a failed submission
  - The `{% if error %}` block is already present — no change needed

## Files to change
- `app.py` — add `session` to Flask imports; add `check_password_hash` from werkzeug import; add `get_user_by_id` to db import; replace `GET /login` with combined GET+POST handler; replace raw-string `/logout` stub with real implementation
- `database/db.py` — add `get_user_by_id()`
- `templates/login.html` — fix hardcoded action URL; add `value` to email input

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives in `database/db.py` only — no raw SQL in route functions
- Use `abort()` for unexpected HTTP errors — not bare string returns
- Session key must be exactly `session['user_id']` — this is the contract all future steps depend on
- On successful login: `session['user_id'] = user['id']` then `redirect(url_for('profile'))`
- On logout: `session.clear()` then `redirect(url_for('login'))`
- Use a single generic error message for bad credentials — `"Invalid email or password."` — never reveal which field was wrong

## Definition of done
- [ ] `GET /login` still loads without errors
- [ ] Submitting blank fields re-renders the form with an error
- [ ] Submitting a valid email with the wrong password shows `"Invalid email or password."`
- [ ] Submitting a non-existent email shows `"Invalid email or password."`
- [ ] Submitting valid credentials sets `session['user_id']` and redirects to `/profile`
- [ ] The entered email is preserved in the form after a failed submission
- [ ] `GET /logout` clears the session and redirects to `/login`
- [ ] Visiting `/logout` when not logged in also redirects to `/login` without error
- [ ] The form `action` uses `url_for('login')` — no hardcoded `/login` URL