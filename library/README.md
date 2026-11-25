# Library Hub

A Python, HTML, and CSS digital library and audiobook web application featuring illustrated book cover images, a dedicated `/login` page, multi-genre book discovery, instant chapter & UI language translation, built-in audiobook narration, study notes, reader reviews, reading progress tracking, and a persistent subscription & payment model.

## Features
- **Dedicated Login Page (`/login`)**: Full Sign In / Create Account experience with password toggle and one-click demo sign-in (`demo@libraryhub.com` / `library123`).
- **Illustrated Book Covers**: Custom SVG cover artwork for every title in `static/covers/`.
- **All Book Genres**: 14 titles across 12 categories (Fiction, Sci-Fi & Fantasy, Science & Tech, Mystery & Thriller, History & Biography, Self-Help, Business & Finance, Philosophy & Classics, Poetry & Drama, Young Adult, Children's Tales).
- **Easy Interface & Productivity**: Continue Reading strip, Daily Reading Goal tracker, live search, genre ribbon, Paper/Sepia/Night reading themes, font sizing, chapter `.txt` export, personal **Study Notes**, and **Reader Reviews & Star Ratings**.
- **Language Translation**: Switch the UI or translate any chapter into 8 languages (`English`, `Spanish`, `French`, `German`, `Hindi`, `Arabic` with RTL, `Japanese`, `Chinese`), including side-by-side **Bilingual Mode**.
- **Audiobooks Studio**: Built-in Web Speech narration in the selected language with live sentence highlighting, playback speed (`0.85x`–`1.85x`), sleep timer, chapter chime (`/api/audio/chime`), and a persistent mini-player bar.
- **Payment Subscription Model**: Monthly/Annual toggle (20% annual savings), 3 plans (`Free Reader`, `Plus Reader`, `Audiobook Pro`), promo code `READ20` (20% off), demo card/wallet checkout, SQLite invoice history, and instant chapter unlocking.

## Quick Start
```bash
python3 app.py
```
Then open the printed URL (default `http://127.0.0.1:8000`) in your browser.

## Run Tests
```bash
python3 -m unittest discover -s tests -v
```
