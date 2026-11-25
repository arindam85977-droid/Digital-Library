"""Lumina Library — Python web server, REST API, audiobook stream, and subscription backend."""

import argparse
import errno
import io
import json
import math
import mimetypes
import os
import re
import struct
import wave
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from catalog import BOOKS, GENRES, get_book_by_id, get_books
from database import (
    PLANS,
    add_note,
    add_review,
    authenticate_user,
    can_access_book,
    create_session,
    create_user,
    delete_note,
    delete_session,
    get_book_notes,
    get_book_reviews,
    get_user_bookmarks,
    get_user_by_token,
    get_user_payments,
    get_user_progress,
    init_db,
    process_subscription_payment,
    save_reading_progress,
    toggle_bookmark,
)
from translator import SUPPORTED_LANGUAGES, UI_TRANSLATIONS, translate_text

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def build_chapter_chime_wav():
    """Synthesize a soft warm C-major triad chime WAV in pure Python."""
    sample_rate = 22050
    duration = 0.85
    num_samples = int(sample_rate * duration)
    freqs = [523.25, 659.25, 783.99]  # C5, E5, G5
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            env = math.exp(-3.8 * t) * min(1.0, t / 0.02)
            sample = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
            val = int(max(-1.0, min(1.0, sample * env * 0.4)) * 32767)
            frames.extend(struct.pack("<h", val))
        wf.writeframes(bytes(frames))
    return buf.getvalue()


CHIME_WAV_BYTES = build_chapter_chime_wav()


def serialize_book_summary(book, user=None):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "genre": book["genre"],
        "genre_label": book["genre_label"],
        "tier": book["tier"],
        "has_access": can_access_book(user, book),
        "rating": book["rating"],
        "reviews_count": book["reviews_count"],
        "year": book["year"],
        "pages": book["pages"],
        "audio_minutes": book["audio_minutes"],
        "has_audiobook": book["has_audiobook"],
        "narrator": book["narrator"],
        "cover_gradient": book["cover_gradient"],
        "cover_accent": book["cover_accent"],
        "cover_image": book.get("cover_image", f"/static/covers/{book['id']}.svg"),
        "description": book["description"],
        "tags": book["tags"],
        "chapter_count": len(book["chapters"]),
    }


class LibraryHandler(BaseHTTPRequestHandler):
    server_version = "LibraryHub/2.0"

    def log_message(self, fmt, *args):
        # Clean concise request logs
        print(f"[HTTP] {self.address_string()} - {fmt % args}")

    def _get_session_token(self):
        cookie_header = self.headers.get("Cookie")
        if not cookie_header:
            return None
        jar = cookies.SimpleCookie()
        jar.load(cookie_header)
        morsel = jar.get("lumina_session")
        return morsel.value if morsel else None

    def _current_user(self):
        return get_user_by_token(self._get_session_token())

    def _send_json(self, status, payload, extra_headers=None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, status, content_type, data):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0 or length > 1_000_000:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            html_file = TEMPLATES_DIR / "index.html"
            if not html_file.exists():
                self._send_json(404, {"error": "Template not found"})
                return
            self._send_bytes(200, "text/html; charset=utf-8", html_file.read_bytes())
            return

        if path == "/login" or path == "/login.html":
            login_file = TEMPLATES_DIR / "login.html"
            if not login_file.exists():
                self._send_json(404, {"error": "Login template not found"})
                return
            self._send_bytes(200, "text/html; charset=utf-8", login_file.read_bytes())
            return

        if path.startswith("/static/"):
            rel = path[len("/static/"):]
            target = (STATIC_DIR / rel).resolve()
            if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.is_file():
                self._send_json(404, {"error": "Static asset not found"})
                return
            mime, _ = mimetypes.guess_type(str(target))
            self._send_bytes(200, mime or "application/octet-stream", target.read_bytes())
            return

        if path == "/api/audio/chime":
            self._send_bytes(200, "audio/wav", CHIME_WAV_BYTES)
            return

        if path == "/api/bootstrap":
            user = self._current_user()
            bookmarks = get_user_bookmarks(user["id"]) if user else []
            payments = get_user_payments(user["id"]) if user else []
            progress = get_user_progress(user["id"]) if user else []
            self._send_json(
                200,
                {
                    "genres": GENRES,
                    "languages": SUPPORTED_LANGUAGES,
                    "ui_translations": UI_TRANSLATIONS,
                    "plans": list(PLANS.values()),
                    "user": user,
                    "bookmarks": bookmarks,
                    "payments": payments,
                    "progress": progress,
                    "books": [serialize_book_summary(b, user) for b in BOOKS],
                },
            )
            return

        if path == "/api/books":
            user = self._current_user()
            genre = qs.get("genre", ["all"])[0]
            query = qs.get("q", [""])[0]
            tier = qs.get("tier", ["all"])[0]
            audio_only = qs.get("audio_only", ["false"])[0].lower() == "true"
            filtered = get_books(genre=genre, query=query, tier=tier, audio_only=audio_only)
            self._send_json(200, {"books": [serialize_book_summary(b, user) for b in filtered]})
            return

        if path.startswith("/api/books/") and path.endswith("/reviews"):
            book_id = path[len("/api/books/"):-len("/reviews")].strip("/")
            if not get_book_by_id(book_id):
                self._send_json(404, {"error": "Book not found"})
                return
            self._send_json(200, {"reviews": get_book_reviews(book_id)})
            return

        if path == "/api/notes":
            user = self._current_user()
            if not user:
                self._send_json(200, {"notes": []})
                return
            book_id = qs.get("book_id", [""])[0]
            self._send_json(200, {"notes": get_book_notes(user["id"], book_id)})
            return

        if path.startswith("/api/books/"):
            book_id = path[len("/api/books/"):].strip("/")
            book = get_book_by_id(book_id)
            if not book:
                self._send_json(404, {"error": "Book not found"})
                return
            user = self._current_user()
            has_access = can_access_book(user, book)
            target_lang = qs.get("lang", ["en"])[0]

            chapters_out = []
            for idx, ch in enumerate(book["chapters"]):
                # Chapter 1 is always available as a free preview; remaining chapters unlock with subscription
                unlocked = has_access or idx == 0
                raw_content = ch["content"] if unlocked else (
                    ch["content"][:180] + "... [Subscribe to unlock the full chapter and audiobook.]"
                )
                tr = translate_text(raw_content, target_lang, book_id=book["id"], chapter_number=ch["number"])
                chapters_out.append(
                    {
                        "number": ch["number"],
                        "title": ch["title"],
                        "duration_min": ch["duration_min"],
                        "unlocked": unlocked,
                        "content": raw_content,
                        "translated_content": tr["translated"],
                        "translation_mode": tr["mode"],
                    }
                )

            summary = serialize_book_summary(book, user)
            summary["chapters"] = chapters_out
            summary["reviews"] = get_book_reviews(book_id)
            summary["notes"] = get_book_notes(user["id"], book_id) if user else []
            self._send_json(200, {"book": summary})
            return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        data = self._read_json_body()

        if path == "/api/translate":
            text = str(data.get("text", ""))
            target_lang = str(data.get("target_lang", "en"))
            book_id = data.get("book_id")
            chapter_number = data.get("chapter_number")
            if not text.strip():
                self._send_json(400, {"error": "Text to translate is required."})
                return
            res = translate_text(text, target_lang, book_id=book_id, chapter_number=chapter_number)
            self._send_json(200, res)
            return

        if path == "/api/auth/register":
            name = str(data.get("name", "")).strip()
            email = str(data.get("email", "")).strip()
            password = str(data.get("password", ""))
            if len(name) < 2 or "@" not in email or len(password) < 6:
                self._send_json(400, {"error": "Provide a valid name, email, and password (6+ characters)."})
                return
            user, err = create_user(name, email, password)
            if err:
                self._send_json(409, {"error": err})
                return
            token = create_session(user["id"])
            self._send_json(
                201,
                {"user": user, "bookmarks": [], "payments": []},
                extra_headers={"Set-Cookie": f"lumina_session={token}; Path=/; HttpOnly; SameSite=Lax"},
            )
            return

        if path == "/api/auth/login":
            email = str(data.get("email", "")).strip()
            password = str(data.get("password", ""))
            user = authenticate_user(email, password)
            if not user:
                self._send_json(401, {"error": "Invalid email or password."})
                return
            user.pop("password_hash", None)
            token = create_session(user["id"])
            self._send_json(
                200,
                {
                    "user": user,
                    "bookmarks": get_user_bookmarks(user["id"]),
                    "payments": get_user_payments(user["id"]),
                },
                extra_headers={"Set-Cookie": f"lumina_session={token}; Path=/; HttpOnly; SameSite=Lax"},
            )
            return

        if path == "/api/auth/logout":
            token = self._get_session_token()
            delete_session(token)
            self._send_json(
                200,
                {"ok": True},
                extra_headers={"Set-Cookie": "lumina_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"},
            )
            return

        if path == "/api/bookmarks/toggle":
            user = self._current_user()
            if not user:
                self._send_json(401, {"error": "Please sign in to save books to your shelf."})
                return
            book_id = str(data.get("book_id", ""))
            if not get_book_by_id(book_id):
                self._send_json(404, {"error": "Book not found."})
                return
            chapter_number = int(data.get("chapter_number", 1) or 1)
            saved = toggle_bookmark(user["id"], book_id, chapter_number)
            self._send_json(200, {"saved": saved, "bookmarks": get_user_bookmarks(user["id"])})
            return

        if path == "/api/progress":
            user = self._current_user()
            if not user:
                self._send_json(200, {"progress": []})
                return
            book_id = str(data.get("book_id", ""))
            if not get_book_by_id(book_id):
                self._send_json(404, {"error": "Book not found."})
                return
            ch_num = int(data.get("chapter_number", 1) or 1)
            pct = int(data.get("percent", 50) or 50)
            save_reading_progress(user["id"], book_id, ch_num, pct)
            self._send_json(200, {"progress": get_user_progress(user["id"])})
            return

        if path.startswith("/api/books/") and path.endswith("/reviews"):
            user = self._current_user()
            if not user:
                self._send_json(401, {"error": "Please sign in to post a review."})
                return
            book_id = path[len("/api/books/"):-len("/reviews")].strip("/")
            if not get_book_by_id(book_id):
                self._send_json(404, {"error": "Book not found."})
                return
            rating = int(data.get("rating", 5) or 5)
            comment = str(data.get("comment", "")).strip()
            if len(comment) < 3:
                self._send_json(400, {"error": "Please write a short review (at least 3 characters)."})
                return
            reviews = add_review(book_id, user["id"], user["name"], rating, comment)
            self._send_json(201, {"reviews": reviews})
            return

        if path == "/api/notes":
            user = self._current_user()
            if not user:
                self._send_json(401, {"error": "Please sign in to save reading notes."})
                return
            book_id = str(data.get("book_id", ""))
            ch_num = int(data.get("chapter_number", 1) or 1)
            note_text = str(data.get("note_text", "")).strip()
            if not get_book_by_id(book_id) or not note_text:
                self._send_json(400, {"error": "Valid book and note text are required."})
                return
            notes = add_note(user["id"], book_id, ch_num, note_text)
            self._send_json(201, {"notes": notes})
            return

        if path == "/api/notes/delete":
            user = self._current_user()
            if not user:
                self._send_json(401, {"error": "Sign in required."})
                return
            note_id = int(data.get("note_id", 0) or 0)
            book_id = str(data.get("book_id", ""))
            delete_note(user["id"], note_id)
            self._send_json(200, {"notes": get_book_notes(user["id"], book_id)})
            return

        if path == "/api/subscribe":
            user = self._current_user()
            if not user:
                self._send_json(401, {"error": "Please sign in or create a free account before subscribing."})
                return
            plan_id = str(data.get("plan_id", ""))
            billing_cycle = str(data.get("billing_cycle", "monthly"))
            payment_method = str(data.get("payment_method", "card"))
            card_number = re.sub(r"\D", "", str(data.get("card_number", "")))
            promo_code = str(data.get("promo_code", ""))

            if plan_id != "free" and payment_method == "card":
                if len(card_number) < 12:
                    self._send_json(400, {"error": "Enter a valid card number (at least 12 digits for demo checkout)."})
                    return
                card_last4 = card_number[-4:]
            else:
                card_last4 = card_number[-4:] if card_number else "WALLET"

            receipt, err = process_subscription_payment(
                user_id=user["id"],
                plan_id=plan_id,
                billing_cycle=billing_cycle,
                payment_method=payment_method,
                card_last4=card_last4,
                promo_code=promo_code,
            )
            if err:
                self._send_json(400, {"error": err})
                return
            receipt["payments"] = get_user_payments(user["id"])
            receipt["books"] = [serialize_book_summary(b, receipt["user"]) for b in BOOKS]
            self._send_json(200, receipt)
            return

        self._send_json(404, {"error": "Endpoint not found"})


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def create_server(host="127.0.0.1", port=None):
    """Create the HTTP server, automatically choosing the next free port if busy."""
    init_db()
    requested_port = int(os.environ.get("PORT", 8000)) if port is None else int(port)
    for candidate in range(requested_port, requested_port + 20):
        try:
            server = ReusableThreadingHTTPServer((host, candidate), LibraryHandler)
            if candidate != requested_port:
                print(f"Port {requested_port} is already in use; switched to port {candidate}.")
            return server
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
    # Final fallback: let the OS pick any available port
    server = ReusableThreadingHTTPServer((host, 0), LibraryHandler)
    print(f"Ports {requested_port}-{requested_port + 19} are busy; switched to port {server.server_address[1]}.")
    return server


def run_server(host="127.0.0.1", port=None):
    server = create_server(host=host, port=port)
    actual_port = server.server_address[1]
    print(f"Library Hub running at http://{host}:{actual_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Library Hub...")
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Library Hub web server.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=None, help="Port to bind (default: PORT env or 8000)")
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
