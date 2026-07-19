import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "spendly.db")

CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
"""

CREATE_EXPENSES_SQL = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

# (category, amount, description, day_of_month) — day_of_month kept <= 28
# so every entry is valid even in a non-leap February.
SAMPLE_EXPENSES = [
    ("Food", 54.20, "Grocery run", 2),
    ("Transport", 40.00, "Metro card top-up", 5),
    ("Bills", 85.50, "Electricity bill", 8),
    ("Health", 22.10, "Pharmacy purchase", 11),
    ("Entertainment", 32.00, "Movie tickets", 14),
    ("Shopping", 129.99, "Headphones", 17),
    ("Other", 15.00, "Miscellaneous", 21),
    ("Food", 18.75, "Lunch with coworkers", 25),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute(CREATE_USERS_SQL)
        conn.execute(CREATE_EXPENSES_SQL)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cur.lastrowid

        today = date.today()
        for category, amount, description, day in SAMPLE_EXPENSES:
            expense_date = date(today.year, today.month, day).isoformat()
            conn.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, amount, category, expense_date, description),
            )
        conn.commit()
    finally:
        conn.close()
