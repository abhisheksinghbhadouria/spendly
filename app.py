import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key-not-for-production"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method != "POST":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.", name=name, email=email)
    if not email:
        return render_template("register.html", error="Email address is required.", name=name, email=email)
    if "@" not in email or "." not in email.split("@")[-1]:
        return render_template("register.html", error="Enter a valid email address.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    password_hash = generate_password_hash(password)
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template(
            "register.html",
            error="An account with that email already exists.",
            name=name,
            email=email,
        )
    finally:
        conn.close()

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method != "POST":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    finally:
        conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.", email=email)

    session.clear()
    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

PROFILE_USER = {
    "name": "Demo User",
    "email": "demo@spendly.com",
    "member_since": "June 2026",
}

PROFILE_TRANSACTIONS = [
    {"date": "2026-07-15", "description": "Grocery run", "category": "Food", "amount": 54.20},
    {"date": "2026-07-13", "description": "Metro card top-up", "category": "Transport", "amount": 40.00},
    {"date": "2026-07-10", "description": "Electricity bill", "category": "Bills", "amount": 85.50},
    {"date": "2026-07-08", "description": "Lunch with coworkers", "category": "Food", "amount": 18.75},
    {"date": "2026-07-03", "description": "Movie tickets", "category": "Entertainment", "amount": 32.00},
]

PROFILE_CATEGORIES = [
    {"name": "Bills", "amount": 85.50, "percent": 37, "width_class": "w40"},
    {"name": "Food", "amount": 72.95, "percent": 32, "width_class": "w30"},
    {"name": "Transport", "amount": 40.00, "percent": 17, "width_class": "w20"},
    {"name": "Entertainment", "amount": 32.00, "percent": 14, "width_class": "w10"},
]

PROFILE_STATS = {
    "total_spent": 230.45,
    "transaction_count": 5,
    "top_category": "Bills",
}

CATEGORY_COLORS = {c["name"]: i % 4 + 1 for i, c in enumerate(PROFILE_CATEGORIES)}


def _initials(name):
    parts = name.split()
    letters = (parts[0][0] + parts[-1][0]) if len(parts) > 1 else parts[0][:2]
    return letters.upper()


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        user=PROFILE_USER,
        initials=_initials(PROFILE_USER["name"]),
        stats=PROFILE_STATS,
        transactions=PROFILE_TRANSACTIONS,
        categories=PROFILE_CATEGORIES,
        category_colors=CATEGORY_COLORS,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
