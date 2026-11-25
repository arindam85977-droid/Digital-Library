"""SQLite database layer for users, sessions, bookmarks, and subscription payments."""

import hashlib
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "library.db"

PLANS = {
    "free": {
        "id": "free",
        "name": "Free Reader",
        "monthly_price": 0.0,
        "annual_price": 0.0,
        "badge": "Open Access",
        "features": [
            "Access to all Open-Access & Classic eBooks",
            "Chapter 1 previews across the entire catalog",
            "Multi-language reader translation (all supported languages)",
            "Standard Audiobook playback (1.0x speed)",
        ],
    },
    "plus": {
        "id": "plus",
        "name": "Plus Reader",
        "monthly_price": 9.99,
        "annual_price": 95.90,
        "badge": "Most Popular",
        "features": [
            "Unlimited full-book access across all 12 genres",
            "Side-by-side bilingual translation mode",
            "Personal cloud bookshelf & synced bookmarks",
            "Offline chapter export & custom reader themes",
        ],
    },
    "audiobook_pro": {
        "id": "audiobook_pro",
        "name": "Audiobook Pro",
        "monthly_price": 16.99,
        "annual_price": 163.00,
        "badge": "All-Access + Audio",
        "features": [
            "Everything in Plus Reader across every genre",
            "Full Audiobook streaming & Audiobooks Pro Originals",
            "Variable speed (0.75x–2.0x), sleep timer & voice narration",
            "Multilingual spoken audio narration in 8+ languages",
        ],
    },
}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return f"{salt}${dk.hex()}"


def verify_password(password, stored):
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return secrets.compare_digest(hash_password(password, salt), stored)


def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                plan_id TEXT NOT NULL DEFAULT 'free',
                billing_cycle TEXT NOT NULL DEFAULT 'monthly',
                subscription_status TEXT NOT NULL DEFAULT 'active',
                renews_at TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS bookmarks (
                user_id INTEGER NOT NULL,
                book_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                PRIMARY KEY (user_id, book_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                plan_id TEXT NOT NULL,
                billing_cycle TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL DEFAULT 'USD',
                payment_method TEXT NOT NULL,
                card_last4 TEXT,
                promo_code TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS reading_progress (
                user_id INTEGER NOT NULL,
                book_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL DEFAULT 1,
                percent INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, book_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL DEFAULT 1,
                note_text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

        # Seed demo accounts so guests can try one-click login or register fresh
        now = datetime.now(timezone.utc).isoformat()
        for demo_name, demo_email, demo_pw in [
            ("Maya Reader", "reader@lumina.lib", "lumina123"),
            ("Alex Reader", "demo@libraryhub.com", "library123"),
        ]:
            existing = conn.execute("SELECT id FROM users WHERE email = ?", (demo_email,)).fetchone()
            if not existing:
                conn.execute(
                    """
                    INSERT INTO users (name, email, password_hash, plan_id, billing_cycle, subscription_status, created_at)
                    VALUES (?, ?, ?, 'free', 'monthly', 'active', ?)
                    """,
                    (demo_name, demo_email, hash_password(demo_pw), now),
                )
        conn.commit()


def create_user(name, email, password):
    now = datetime.now(timezone.utc).isoformat()
    email = email.strip().lower()
    with get_conn() as conn:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            return None, "An account with this email already exists."
        cur = conn.execute(
            """
            INSERT INTO users (name, email, password_hash, plan_id, billing_cycle, subscription_status, created_at)
            VALUES (?, ?, ?, 'free', 'monthly', 'active', ?)
            """,
            (name.strip(), email, hash_password(password), now),
        )
        user_id = cur.lastrowid
        conn.commit()
    return get_user_by_id(user_id), None


def authenticate_user(email, password):
    email = email.strip().lower()
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not row or not verify_password(password, row["password_hash"]):
            return None
        return dict(row)


def create_session(user_id):
    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=14)
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token, user_id, now.isoformat(), expires.isoformat()),
        )
        conn.commit()
    return token


def delete_session(token):
    if not token:
        return
    with get_conn() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()


def get_user_by_token(token):
    if not token:
        return None
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT u.* FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.token = ?
            """,
            (token,),
        ).fetchone()
        if not row:
            return None
        user = dict(row)
        user.pop("password_hash", None)
        return user


def get_user_by_id(user_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            return None
        user = dict(row)
        user.pop("password_hash", None)
        return user


def can_access_book(user, book):
    """Determine if a user's subscription grants full access to a book."""
    tier = book["tier"]
    if tier == "free":
        return True
    plan_id = user["plan_id"] if user else "free"
    if tier == "plus":
        return plan_id in ("plus", "audiobook_pro")
    if tier == "audiobook_pro":
        return plan_id == "audiobook_pro"
    return False


def process_subscription_payment(user_id, plan_id, billing_cycle, payment_method, card_last4="", promo_code=""):
    """Validate and activate a subscription plan and record a payment invoice."""
    if plan_id not in PLANS:
        return None, "Invalid subscription plan."
    if billing_cycle not in ("monthly", "annual"):
        return None, "Invalid billing cycle."

    plan = PLANS[plan_id]
    base_price = plan["annual_price"] if billing_cycle == "annual" else plan["monthly_price"]
    discount = 0.0
    promo = promo_code.strip().upper()
    if promo == "READ20" and base_price > 0:
        discount = round(base_price * 0.20, 2)
    final_amount = max(0.0, round(base_price - discount, 2))

    now = datetime.now(timezone.utc)
    renews_at = (
        (now + timedelta(days=365 if billing_cycle == "annual" else 30)).isoformat()
        if plan_id != "free"
        else None
    )
    invoice_id = f"INV-{now.strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"

    with get_conn() as conn:
        conn.execute(
            """
            UPDATE users
            SET plan_id = ?, billing_cycle = ?, subscription_status = 'active', renews_at = ?
            WHERE id = ?
            """,
            (plan_id, billing_cycle, renews_at, user_id),
        )
        conn.execute(
            """
            INSERT INTO payments (invoice_id, user_id, plan_id, billing_cycle, amount, currency, payment_method, card_last4, promo_code, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'USD', ?, ?, ?, 'paid', ?)
            """,
            (invoice_id, user_id, plan_id, billing_cycle, final_amount, payment_method, card_last4, promo, now.isoformat()),
        )
        conn.commit()

    return {
        "invoice_id": invoice_id,
        "plan": plan,
        "billing_cycle": billing_cycle,
        "amount": final_amount,
        "discount": discount,
        "renews_at": renews_at,
        "status": "paid",
        "user": get_user_by_id(user_id),
    }, None


def get_user_payments(user_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM payments WHERE user_id = ? ORDER BY id DESC LIMIT 20",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def toggle_bookmark(user_id, book_id, chapter_number=1):
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT book_id FROM bookmarks WHERE user_id = ? AND book_id = ?",
            (user_id, book_id),
        ).fetchone()
        if existing:
            conn.execute("DELETE FROM bookmarks WHERE user_id = ? AND book_id = ?", (user_id, book_id))
            conn.commit()
            return False
        conn.execute(
            "INSERT INTO bookmarks (user_id, book_id, chapter_number, created_at) VALUES (?, ?, ?, ?)",
            (user_id, book_id, chapter_number, now),
        )
        conn.commit()
        return True


def get_user_bookmarks(user_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT book_id, chapter_number, created_at FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def save_reading_progress(user_id, book_id, chapter_number, percent):
    now = datetime.now(timezone.utc).isoformat()
    pct = max(0, min(100, int(percent)))
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO reading_progress (user_id, book_id, chapter_number, percent, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, book_id) DO UPDATE SET
                chapter_number = excluded.chapter_number,
                percent = excluded.percent,
                updated_at = excluded.updated_at
            """,
            (user_id, book_id, int(chapter_number), pct, now),
        )
        conn.commit()


def get_user_progress(user_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT book_id, chapter_number, percent, updated_at FROM reading_progress WHERE user_id = ? ORDER BY updated_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def add_review(book_id, user_id, user_name, rating, comment):
    now = datetime.now(timezone.utc).isoformat()
    stars = max(1, min(5, int(rating)))
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO reviews (book_id, user_id, user_name, rating, comment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (book_id, user_id, user_name, stars, comment.strip(), now),
        )
        conn.commit()
    return get_book_reviews(book_id)


def get_book_reviews(book_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, book_id, user_name, rating, comment, created_at FROM reviews WHERE book_id = ? ORDER BY id DESC LIMIT 30",
            (book_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def add_note(user_id, book_id, chapter_number, note_text):
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO notes (user_id, book_id, chapter_number, note_text, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, book_id, int(chapter_number), note_text.strip(), now),
        )
        conn.commit()
    return get_book_notes(user_id, book_id)


def get_book_notes(user_id, book_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, book_id, chapter_number, note_text, created_at FROM notes WHERE user_id = ? AND book_id = ? ORDER BY id DESC",
            (user_id, book_id),
        ).fetchall()
        return [dict(r) for r in rows]


def delete_note(user_id, note_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (int(note_id), user_id))
        conn.commit()
