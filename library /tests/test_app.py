"""Automated test suite for Lumina Library backend and HTTP API."""

import http.cookiejar
import json
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as lumina_app
import database
from catalog import GENRES, get_books
from translator import SUPPORTED_LANGUAGES, translate_text


class LuminaLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.TemporaryDirectory()
        database.DB_PATH = Path(cls.tmp_dir.name) / "test_library.db"
        database.init_db()

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), lumina_app.LibraryHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp_dir.cleanup()

    def _opener(self):
        jar = http.cookiejar.CookieJar()
        return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def test_catalog_covers_many_genres(self):
        self.assertGreaterEqual(len(GENRES), 12)
        all_books = get_books()
        self.assertGreaterEqual(len(all_books), 14)
        scifi = get_books(genre="scifi-fantasy")
        self.assertTrue(any(b["id"] == "silent-orbit" for b in scifi))
        searched = get_books(query="Kyoto")
        self.assertEqual(len(searched), 1)
        self.assertEqual(searched[0]["id"], "gardens-of-kyoto")

    def test_translator_curated_and_adaptive(self):
        self.assertGreaterEqual(len(SUPPORTED_LANGUAGES), 8)
        curated = translate_text("Hello world", "es", book_id="silent-orbit", chapter_number=1)
        self.assertEqual(curated["mode"], "curated")
        self.assertIn("Estación Meridiano", curated["translated"])

        adaptive = translate_text("A quiet morning in the library", "fr")
        self.assertEqual(adaptive["mode"], "adaptive")
        self.assertIn("bibliothèque", adaptive["translated"])

        rtl = translate_text("A quiet book", "ar")
        self.assertTrue(rtl["lang"]["rtl"])

    def test_http_endpoints_and_subscription_unlock(self):
        opener = self._opener()

        # 1. HTML, dedicated /login page, cover SVG & CSS served cleanly
        with opener.open(f"{self.base_url}/") as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            self.assertIn("Library Hub", html)

        with opener.open(f"{self.base_url}/login") as resp:
            self.assertEqual(resp.status, 200)
            login_html = resp.read().decode("utf-8")
            self.assertIn("Sign In to Library Hub", login_html)

        with opener.open(f"{self.base_url}/static/covers/silent-orbit.svg") as resp:
            self.assertEqual(resp.status, 200)
            svg_body = resp.read().decode("utf-8")
            self.assertIn("<svg", svg_body)

        with opener.open(f"{self.base_url}/static/css/styles.css") as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/css", resp.headers.get("Content-Type", ""))

        # 2. WAV chime audio endpoint works
        with opener.open(f"{self.base_url}/api/audio/chime") as resp:
            self.assertEqual(resp.status, 200)
            wav_bytes = resp.read()
            self.assertTrue(wav_bytes.startswith(b"RIFF"))

        # 3. Bootstrap & translated book chapter
        with opener.open(f"{self.base_url}/api/bootstrap") as resp:
            boot = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(len(boot["plans"]), 3)
            self.assertGreaterEqual(len(boot["books"]), 14)

        with opener.open(f"{self.base_url}/api/books/clockwork-alibi?lang=es") as resp:
            book_data = json.loads(resp.read().decode("utf-8"))["book"]
            # Free guest gets Ch 1 unlocked, Ch 2 locked before subscription
            self.assertTrue(book_data["chapters"][0]["unlocked"])
            self.assertFalse(book_data["chapters"][1]["unlocked"])

        # 4. Login with Library Hub demo user
        login_req = urllib.request.Request(
            f"{self.base_url}/api/auth/login",
            data=json.dumps({"email": "demo@libraryhub.com", "password": "library123"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(login_req) as resp:
            login_res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(login_res["user"]["plan_id"], "free")

        # 4b. Save reading progress, study note, and book review
        prog_req = urllib.request.Request(
            f"{self.base_url}/api/progress",
            data=json.dumps({"book_id": "silent-orbit", "chapter_number": 2, "percent": 100}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(prog_req) as resp:
            prog_res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(prog_res["progress"][0]["book_id"], "silent-orbit")

        note_req = urllib.request.Request(
            f"{self.base_url}/api/notes",
            data=json.dumps({"book_id": "silent-orbit", "chapter_number": 1, "note_text": "Great sci-fi opening"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(note_req) as resp:
            note_res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(len(note_res["notes"]), 1)

        rev_req = urllib.request.Request(
            f"{self.base_url}/api/books/silent-orbit/reviews",
            data=json.dumps({"rating": 5, "comment": "Loved the translation and audio!"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(rev_req) as resp:
            rev_res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(rev_res["reviews"][0]["rating"], 5)

        # 5. Bookmark toggle
        bm_req = urllib.request.Request(
            f"{self.base_url}/api/bookmarks/toggle",
            data=json.dumps({"book_id": "silent-orbit", "chapter_number": 1}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(bm_req) as resp:
            bm_res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(bm_res["saved"])

        # 6. Subscribe to Plus Reader with READ20 promo code
        sub_req = urllib.request.Request(
            f"{self.base_url}/api/subscribe",
            data=json.dumps(
                {
                    "plan_id": "plus",
                    "billing_cycle": "monthly",
                    "payment_method": "card",
                    "card_number": "4242424242424242",
                    "promo_code": "READ20",
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(sub_req) as resp:
            sub_res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(sub_res["status"], "paid")
            self.assertAlmostEqual(sub_res["amount"], 7.99, places=2)
            self.assertEqual(sub_res["user"]["plan_id"], "plus")

        # 7. Verify Chapter 2 of Plus book is now unlocked!
        with opener.open(f"{self.base_url}/api/books/clockwork-alibi?lang=en") as resp:
            unlocked_data = json.loads(resp.read().decode("utf-8"))["book"]
            self.assertTrue(unlocked_data["chapters"][1]["unlocked"])

    def test_port_fallback_when_address_in_use(self):
        # Occupy the current test server's port and ensure create_server picks the next free port
        fallback_server = lumina_app.create_server(host="127.0.0.1", port=self.port)
        try:
            self.assertNotEqual(fallback_server.server_address[1], self.port)
            self.assertGreater(fallback_server.server_address[1], self.port)
        finally:
            fallback_server.server_close()


if __name__ == "__main__":
    unittest.main()
