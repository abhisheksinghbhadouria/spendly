# Spec: Login and Logout

## Overview
This step wires up real authentication for Spendly. The `/login` page already renders a form (built in Step 2 alongside registration), but it only accepts `GET` — submitting it does nothing. This feature adds session-based login so a registered user can sign in with their email and password, and a working `/logout` that ends that session. It also makes the navbar session-aware so the rest of the app (and future steps like profile and expenses) can tell whether a visitor is authenticated. This is the third step of the roadmap, immediately after registration, and every later step that needs to know "who is the current user" (profile, expenses) depends on the session established here.

## Depends on
- Step 1 — Database setup (complete). Requires the `users` table and `get_db()` from `database/db.py`.
- Step 2 — Registration (complete). Requires real user rows with hashed passwords to log in against.

## Routes
- `GET /login` — renders the sign-in form — public (already implemented, unchanged)
- `POST /login` — validates credentials against the `users` table, starts a session on success, re-renders the form with an error on failure — public
- `GET /logout` — clears the session and redirects to `/login` — logged-in (also safe to hit while logged out; just redirects)

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already has every column authentication needs. Verified against `database/db.py`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` — make the navbar session-aware: when `session` contains a logged-in user, show a "Log out" link (`/logout`) in place of the "Sign in" / "Get started" links
  - `templates/login.html` — no structural changes; the existing `{% if error %}` block already covers invalid-credentials errors

## Files to change
- `app.py` —
  - set `app.secret_key` (required for Flask's signed session cookie; none is currently configured)
  - change `/login` to accept `GET` and `POST`; on `POST`, look up the user by email, verify the password with `check_password_hash`, and on success store `session['user_id']` and redirect to `/profile`; on failure re-render `login.html` with a generic error
  - implement `/logout` to clear the session and redirect to `/login`
- `templates/base.html` — conditional navbar block described above
- `static/css/style.css` — only if the logged-in nav state needs a style not already covered by existing `.nav-links` / `.nav-cta` rules; reuse existing classes and CSS variables first

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` ships alongside `generate_password_hash`, already installed and already used in `database/db.py` and Step 2.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (verify with `check_password_hash`, never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `session['user_id']` in the session — never the password hash or full user row
- Strip whitespace from the submitted email before lookup, consistent with registration's handling
- On failed login (unknown email OR wrong password), show the same generic "Invalid email or password" error in both cases — never reveal which one was wrong
- `/logout` must call `session.clear()`, not just remove a single key, so no stale session data survives
- `/logout` must not error when hit with no active session — it should just redirect to `/login`
- Do not implement `/profile`'s real content, route protection (`login_required`), or expenses in this step — those belong to later steps; `/profile` remains the existing placeholder string response, just now reachable as the post-login redirect target

## Definition of done
- [ ] `GET /login` still renders the form with no errors
- [ ] `POST /login` with the seeded demo account (`demo@spendly.com` / `demo123`) redirects to `/profile` and sets a session cookie
- [ ] `POST /login` with a wrong password does not set a session and re-renders `login.html` with an "Invalid email or password" error
- [ ] `POST /login` with an email that doesn't exist does not set a session and shows the same generic error as a wrong password
- [ ] After a successful login, the navbar shows "Log out" instead of "Sign in" / "Get started" on every page
- [ ] Visiting `/logout` clears the session, redirects to `/login`, and the navbar reverts to "Sign in" / "Get started"
- [ ] Visiting `/logout` with no active session does not raise an error and redirects to `/login`
- [ ] All SQL statements in the new code use `?` parameter placeholders, no string formatting
- [ ] App starts with `python app.py` without errors and all previously working routes (`/`, `/register`, `/terms`, `/privacy`) are unaffected
