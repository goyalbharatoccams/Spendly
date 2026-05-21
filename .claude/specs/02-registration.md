# Spec: Registration

## Overview
This step wires up the registration form so users can create a Spendly account. The `GET /register` route and `register.html` template already exist; this feature adds the `POST /register` handler, two DB helpers (`create_user` and `get_user_by_email`), a `SECRET_KEY` for Flask sessions (needed for flash messages), and fixes the hardcoded form action URL. On success the user is redirected to the login page; on failure the form re-renders with an inline error and the previously entered name/email preserved.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` table, `init_db()`)

## Routes
- `GET /register` — render registration form — public (already exists, no change needed)
- `POST /register` — validate form, create user, redirect to login — public

## Database changes
No new tables or columns. The `users` table from Step 01 already has all required columns.

Two new helpers are needed in `database/db.py`:
- `get_user_by_email(email)` — returns the matching `users` row or `None`
- `create_user(name, email, password_hash)` — inserts a new user row, returns the new `id`

## Templates
- **Modify:** `templates/register.html`
  - Replace hardcoded `action="/register"` with `action="{{ url_for('register') }}"`
  - Repopulate `name` and `email` inputs with `value="{{ name or '' }}"` / `value="{{ email or '' }}"` so values survive a failed submission
  - The `{% if error %}` block is already present — no change needed there

## Files to change
- `app.py` — add `POST /register` route; import `redirect`, `url_for`, `request`, `flash`, `session` from Flask; set `app.secret_key`
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — fix hardcoded URL; add `value` attributes to name/email inputs

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before storing
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic lives in `database/db.py` only — the route function must not contain raw SQL
- Use `abort()` for unexpected HTTP errors — not bare string returns
- `SECRET_KEY` must be set on `app` before any `flash()` call; use a hard-coded dev string for now (e.g. `"dev-secret-change-in-prod"`)
- After a successful registration, use `redirect(url_for('login'))` — do not auto-login in this step
- Minimum password length: 8 characters (validate server-side)

## Definition of done
- [ ] Submitting the form with valid data creates a row in `users` and redirects to `/login`
- [ ] Submitting with an email that already exists re-renders the form with an error message and the entered name/email still filled in
- [ ] Submitting with a password shorter than 8 characters re-renders the form with an error
- [ ] Submitting with any blank field re-renders the form with an error
- [ ] The stored `password_hash` is not the plain-text password (verify in DB)
- [ ] The form `action` uses `url_for('register')` — no hardcoded `/register` URL
- [ ] App starts without errors and `GET /register` still works as before
