# Spec: Registration

## Overview
This step implements account creation for Spendly. The `/register` page already renders a form, but submitting it does nothing — there is no `POST` handler, no validation, and no user is written to the database. This feature wires the existing form up to `database/db.py`'s `users` table so a visitor can create a real account with a securely hashed password, and lands them on the login page ready to sign in. It is the second step of the roadmap, immediately after the database layer, and every later step (login, profile, expenses) depends on real accounts existing.

## Depends on
- Step 1 — Database setup (complete). Requires the `users` table and `get_db()` from `database/db.py`.

## Routes
- `GET /register` — renders the registration form — public (already implemented, unchanged)
- `POST /register` — validates input, creates the user, redirects to login on success or re-renders the form with an error — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already has every column this feature needs. Verified against `database/db.py`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — show a success banner when arriving via `?registered=1` (reads `request.args`, no session/flash mechanism exists yet)

## Files to change
- `app.py` — change `/register` to accept `GET` and `POST`; on `POST`, validate fields, check for a duplicate email, hash the password, insert the user, and redirect to `/login?registered=1`; on validation failure, re-render `register.html` with an `error` message (the template already supports this)
- `templates/login.html` — add the success banner described above
- `static/css/style.css` — add an `.auth-success` rule in the existing "Auth pages" section, built from existing CSS variables (no new hex values)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already installed and already used in `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though the form has `required`/`type=email` attributes client-side — never trust client-only validation
- Name and email must be stripped of leading/trailing whitespace before validation and storage
- Enforce a minimum password length of 8 characters server-side (the field placeholder already promises this)
- On a duplicate email, re-render `register.html` with a clear error and the submitted name/email pre-filled — never leak whether the collision is on email specifically vs. a generic failure beyond what's needed for usability
- Do not implement login, sessions, or logout in this step — those belong to a later step

## Definition of done
- [ ] `GET /register` still renders the form with no errors
- [ ] Submitting valid name/email/password creates one row in `users` with a hashed (not plaintext) `password_hash`
- [ ] Submitting a duplicate email does not create a second row and re-renders `register.html` with an error
- [ ] Submitting an empty name, invalid email, or password under 8 characters does not create a row and re-renders `register.html` with an error
- [ ] A successful registration redirects to `/login?registered=1`
- [ ] `GET /login?registered=1` shows a success banner; `GET /login` (no query param) does not
- [ ] All SQL statements in the new code use `?` parameter placeholders, no string formatting
- [ ] App starts with `python app.py` without errors and all previously working routes (`/`, `/login`, `/terms`, `/privacy`) are unaffected
