# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a personal expense tracker built as a step-by-step Flask learning project. `app.py` and `database/db.py` contain comments like `# Students will implement these` / `# Students will write this file in Step 1`, and several routes are intentionally unimplemented placeholders — treat these as scaffolding to be filled in, not bugs.

## Commands

```bash
# Activate the existing venv (already created, Python 3.11)
source venv/Scripts/activate        # bash/Git Bash
venv\Scripts\Activate.ps1           # PowerShell

# Install dependencies
pip install -r requirements.txt

# Run the dev server (debug mode, autoreload)
python app.py                       # serves on http://127.0.0.1:5001
```

There are no test files in the repo yet, even though `pytest` and `pytest-flask` are listed in `requirements.txt` — they're installed in anticipation of tests being added, not for an existing suite.

## Architecture

- **Single-file Flask app** (`app.py`): all routes are defined directly on one `Flask(__name__)` instance — no blueprints. Routes fall into two groups:
  - Implemented: `/`, `/register`, `/login`, `/terms`, `/privacy` — each just calls `render_template(...)`.
  - Placeholders: `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` — return a bare string like `"Add expense — coming in Step 7"`. When implementing one of these, replace the stub with real logic rather than treating the string as intentional.

- **Database layer** (`database/db.py`): currently just a comment block, not yet implemented. It's designed to hold three functions:
  - `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
  - `init_db()` — creates tables with `CREATE TABLE IF NOT EXISTS`
  - `seed_db()` — inserts sample dev data
  There's no ORM in use or planned — this is raw `sqlite3`.

- **Templates** (`templates/`): Jinja2 with inheritance from `templates/base.html`, which defines the shared page shell (navbar, `<main>`, footer, font/CSS links) and exposes four blocks: `title`, `head`, `content`, `scripts`. Every page template extends `base.html` and fills `content` at minimum. Use the `head`/`scripts` blocks for page-scoped `<style>`/`<script>` (see `landing.html`'s modal) rather than editing `base.html` or `static/js/main.js`, unless the change is genuinely site-wide.

- **Styling** (`static/css/style.css`): a single stylesheet, no preprocessor or build step. All design tokens (colors, fonts, radii, max-widths) are CSS custom properties on `:root` — reuse these (`var(--accent)`, `var(--ink-muted)`, `var(--paper-card)`, etc.) instead of hardcoding values. Fonts are DM Serif Display (headings/display text, loaded via `--font-display`) and DM Sans (body/UI text, `--font-body`), pulled from Google Fonts in `base.html`. CSS is organized in banner-commented sections per page area (Navbar, Hero, Mock card, Features, CTA, Auth pages, Legal pages, Footer, Responsive) — add new rules under the appropriately named section rather than appending to the end of the file.

- **No JS framework**: `static/js/main.js` is an empty placeholder for future site-wide JS. Project convention is vanilla JS only — no bundler, no framework, no external script dependencies.

- **Port**: the dev server runs on `5001`, not Flask's default `5000` (set via `app.run(debug=True, port=5001)` in `app.py`).
