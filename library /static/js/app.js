/* ═══════════════════════════════════════════════════════════════
   Library Hub — React SPA  (loaded via Babel standalone)
   React 18 UMD globals: React, ReactDOM
   ═══════════════════════════════════════════════════════════════ */

const { useState, useEffect, useRef, useMemo, useCallback } = React;

/* ───── helpers ───── */
async function api(url, opts = {}) {
  const r = await fetch(url, { headers: { "Content-Type": "application/json" }, ...opts });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || "Request failed");
  return d;
}

const TIER_LABELS = { free: "Free", plus: "Plus", audiobook_pro: "Pro" };
const TIER_COLORS = { free: "badge-ok", plus: "", audiobook_pro: "" };

function stars(n) { return "★".repeat(Math.round(n)) + "☆".repeat(5 - Math.round(n)); }
function truncate(s, n = 100) { return s.length > n ? s.slice(0, n) + "…" : s; }

/* ═══════════════════ HEADER ═══════════════════ */
function Header({ view, setView, lang, setLang, languages, user, onLogout, bookmarkCount, ui }) {
  return (
    <header className="hdr">
      <div className="wrap hdr-inner">
        <a className="logo" onClick={() => setView("library")} href="#">
          <span className="logo-icon">📚</span>
          <div><span className="logo-text">Library Hub</span><span className="logo-sub">React + Python</span></div>
        </a>

        <nav className="nav">
          <button className={`nav-link ${view === "library" ? "on" : ""}`} onClick={() => setView("library")}>
            {ui.library || "Library"}
          </button>
          <button className={`nav-link ${view === "audiobooks" ? "on" : ""}`} onClick={() => setView("audiobooks")}>
            🎧 {ui.audiobooks || "Audiobooks"}
          </button>
          <button className={`nav-link ${view === "shelf" ? "on" : ""}`} onClick={() => setView("shelf")}>
            {ui.my_shelf || "My Shelf"}
            {bookmarkCount > 0 && <span className="nav-count">{bookmarkCount}</span>}
          </button>
          <button className={`nav-link ${view === "plans" ? "on" : ""}`} onClick={() => setView("plans")}>
            {ui.subscriptions || "Subscriptions"}
          </button>
        </nav>

        <div className="hdr-right">
          <div className="lang-sel">
            🌐
            <select value={lang} onChange={e => setLang(e.target.value)}>
              {languages.map(l => <option key={l.code} value={l.code}>{l.flag} {l.name}</option>)}
            </select>
          </div>
          {user ? (
            <div className="user-chip" style={{ cursor: "pointer" }} onClick={onLogout} title="Sign out">
              👤 {user.name}
            </div>
          ) : (
            <a href="/login" className="btn btn-pri btn-sm">{ui.sign_in || "Sign In"}</a>
          )}
        </div>
      </div>
    </header>
  );
}

/* ═══════════════════ HERO ═══════════════════ */
function HeroSection({ books, ui, search, setSearch, tierFilter, setTierFilter, genres, genreFilter, setGenreFilter, progressMap }) {
  const featured = books[0];
  const totalChapters = books.reduce((s, b) => s + (b.chapter_count || 0), 0);
  const readChapters = Object.keys(progressMap).length;
  const goalPct = totalChapters > 0 ? Math.min(100, Math.round((readChapters / totalChapters) * 100)) : 0;

  return (
    <section className="hero-banner">
      <div className="wrap hero-grid">
        <div>
          <span className="hero-badge">📖 {books.length} Books · 12 Genres · 8 Languages</span>
          <h1 className="hero-title">{ui.hero_title || "Discover, Read & Listen — in Any Language"}</h1>
          <p className="hero-desc">{ui.hero_desc || "Explore a curated library with audiobooks, bilingual translation, notes, and reader themes."}</p>

          <div className="search-box">
            <span>🔍</span>
            <input placeholder={ui.search_placeholder || "Search books, authors, genres…"}
                   value={search} onChange={e => setSearch(e.target.value)} />
            {search && <button className="icon-btn" onClick={() => setSearch("")} style={{background:"rgba(255,255,255,0.15)",color:"#fff"}}>✕</button>}
          </div>

          <div className="filter-row">
            {["all", "free", "plus", "audiobook_pro"].map(t => (
              <button key={t} className={`chip ${tierFilter === t ? "on" : ""}`} onClick={() => setTierFilter(t)}>
                {t === "all" ? "All Tiers" : TIER_LABELS[t]}
              </button>
            ))}
          </div>

          <div className="goal-bar">
            <div className="goal-bar-top">
              <span>📈 {ui.daily_goal || "Reading Progress"}</span>
              <span>{readChapters}/{totalChapters} chapters</span>
            </div>
            <div className="goal-track"><div className="goal-fill" style={{ width: goalPct + "%" }} /></div>
          </div>
        </div>

        {featured && (
          <div className="hero-card">
            <div style={{ fontSize: "0.78rem", fontWeight: 600, opacity: 0.7, marginBottom: 10 }}>✨ Featured Today</div>
            <div className="hero-card-inner">
              <img className="hero-cover" src={featured.cover_image} alt={featured.title} />
              <div>
                <h3>{featured.title}</h3>
                <p style={{ fontSize: "0.84rem", opacity: 0.75, margin: "4px 0 8px" }}>{featured.author}</p>
                <p style={{ fontSize: "0.82rem", opacity: 0.65 }}>{truncate(featured.description, 120)}</p>
                <div style={{ marginTop: 8, fontSize: "0.82rem" }}>
                  <span style={{ color: "#fbbf24" }}>{stars(featured.rating)}</span> {featured.rating}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Genre ribbon below hero */}
      <div className="wrap">
        <div className="genre-strip">
          {genres.map(g => (
            <button key={g.id} className={`genre-btn ${genreFilter === g.id ? "on" : ""}`}
                    onClick={() => setGenreFilter(g.id)}>
              {g.icon} {g.name}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════ CONTINUE READING ═══════════════════ */
function ContinueReading({ books, progressMap, onOpen }) {
  const inProgress = books.filter(b => progressMap[b.id]);
  if (inProgress.length === 0) return null;
  return (
    <section className="continue wrap">
      <h3 style={{ fontFamily: "var(--font-display)", marginBottom: 10 }}>📖 Continue Reading</h3>
      <div className="continue-row">
        {inProgress.map(b => {
          const p = progressMap[b.id];
          return (
            <div key={b.id} className="cont-card" onClick={() => onOpen(b.id)}>
              <img src={b.cover_image} alt={b.title} />
              <div>
                <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>{truncate(b.title, 28)}</div>
                <div style={{ fontSize: "0.76rem", color: "var(--text-secondary)" }}>Ch {p.chapter_number} · {p.percent}%</div>
                <div className="goal-track" style={{ marginTop: 4, width: 100, height: 4 }}>
                  <div className="goal-fill" style={{ width: p.percent + "%", background: "var(--accent)" }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

/* ═══════════════════ BOOK GRID ═══════════════════ */
function BookGrid({ books, onOpen, ui, sort, setSort }) {
  const sorted = useMemo(() => {
    const copy = [...books];
    if (sort === "title") copy.sort((a, b) => a.title.localeCompare(b.title));
    else if (sort === "rating") copy.sort((a, b) => b.rating - a.rating);
    else if (sort === "year") copy.sort((a, b) => b.year - a.year);
    return copy;
  }, [books, sort]);

  return (
    <section className="sec wrap">
      <div className="sec-top">
        <h2>{ui.all_books || "All Books"} <span className="muted" style={{ fontSize: "1rem" }}>({sorted.length})</span></h2>
        <div className="sort-sel">
          Sort:
          <select value={sort} onChange={e => setSort(e.target.value)}>
            <option value="default">Default</option>
            <option value="title">Title A–Z</option>
            <option value="rating">Top Rated</option>
            <option value="year">Newest</option>
          </select>
        </div>
      </div>

      {sorted.length === 0 ? (
        <div className="empty-box">
          <div style={{ fontSize: "2.5rem", marginBottom: 8 }}>📭</div>
          <h3>No books found</h3>
          <p className="muted">Try adjusting your filters or search term.</p>
        </div>
      ) : (
        <div className="grid">
          {sorted.map(b => (
            <div key={b.id} className="card">
              <div className="card-cover">
                <img src={b.cover_image} alt={b.title} />
                <div className="card-badges">
                  <span className={`badge ${b.tier === "free" ? "badge-ok" : ""}`}>{TIER_LABELS[b.tier] || b.tier}</span>
                  {b.has_audiobook && <span className="badge" style={{background:"rgba(192,88,42,0.8)"}}>🎧 Audio</span>}
                </div>
              </div>
              <div className="card-body">
                <div className="card-title">{b.title}</div>
                <div className="card-meta">
                  <span>{b.author}</span>
                  <span style={{ color: "#b8860b" }}>{stars(b.rating)} {b.rating}</span>
                </div>
                <div className="card-desc">{b.description}</div>
                <div className="tags">
                  {(b.tags || []).slice(0, 3).map(t => <span key={t} className="tag">{t}</span>)}
                </div>
                <div className="card-acts">
                  <button className="btn btn-pri btn-sm" onClick={() => onOpen(b.id)}>
                    {b.has_access ? (ui.read_now || "Read Now") : "Preview"}
                  </button>
                  {b.has_audiobook && (
                    <button className="btn btn-out btn-sm" onClick={() => onOpen(b.id, true)}>🎧</button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

/* ═══════════════════ READER MODAL ═══════════════════ */
function ReaderModal({ bookId, lang, onClose, user, onToast, startAudio, onSubscribe }) {
  const [book, setBook] = useState(null);
  const [chapter, setChapter] = useState(0);
  const [theme, setTheme] = useState("paper");
  const [fontSize, setFontSize] = useState(1.1);
  const [bilingual, setBilingual] = useState(false);
  const [tab, setTab] = useState("read"); // read | notes | reviews
  const [noteText, setNoteText] = useState("");
  const [revText, setRevText] = useState("");
  const [revRating, setRevRating] = useState(5);
  const [transLang, setTransLang] = useState(lang);
  const contentRef = useRef(null);

  useEffect(() => {
    api(`/api/books/${bookId}?lang=${transLang}`).then(d => setBook(d.book)).catch(() => {});
  }, [bookId, transLang]);

  useEffect(() => { setTransLang(lang); }, [lang]);

  useEffect(() => {
    if (contentRef.current) contentRef.current.scrollTop = 0;
  }, [chapter, tab]);

  if (!book) return (
    <div className="overlay" onClick={onClose}><div className="dialog" onClick={e=>e.stopPropagation()} style={{textAlign:"center",padding:48}}>
      <div style={{fontSize:"2rem"}}>⏳</div><p>Loading book…</p>
    </div></div>
  );

  const ch = book.chapters[chapter] || book.chapters[0];
  const themes = ["paper", "sepia", "night"];
  const LANG_NAMES = { en: "English", es: "Spanish", fr: "French", de: "German", hi: "Hindi", ar: "Arabic", ja: "Japanese", zh: "Chinese" };

  async function saveNote() {
    if (!noteText.trim()) return;
    try {
      const d = await api("/api/notes", { method: "POST", body: JSON.stringify({ book_id: book.id, chapter_number: ch.number, note_text: noteText }) });
      setBook(prev => ({ ...prev, notes: d.notes }));
      setNoteText("");
      onToast("Note saved!");
    } catch (e) { onToast(e.message); }
  }

  async function deleteNote(noteId) {
    try {
      const d = await api("/api/notes/delete", { method: "POST", body: JSON.stringify({ note_id: noteId, book_id: book.id }) });
      setBook(prev => ({ ...prev, notes: d.notes }));
    } catch (e) { onToast(e.message); }
  }

  async function postReview() {
    if (!revText.trim()) return;
    try {
      const d = await api(`/api/books/${book.id}/reviews`, { method: "POST", body: JSON.stringify({ rating: revRating, comment: revText }) });
      setBook(prev => ({ ...prev, reviews: d.reviews }));
      setRevText("");
      onToast("Review posted!");
    } catch (e) { onToast(e.message); }
  }

  async function toggleBookmark() {
    try {
      await api("/api/bookmarks/toggle", { method: "POST", body: JSON.stringify({ book_id: book.id, chapter_number: ch.number }) });
      onToast("Bookmark toggled!");
    } catch (e) { onToast(e.message); }
  }

  function exportChapter() {
    const blob = new Blob([`${ch.title}\n\n${ch.content}`], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${book.title} - ${ch.title}.txt`;
    a.click();
  }

  async function saveProgress(pct) {
    try {
      await api("/api/progress", { method: "POST", body: JSON.stringify({ book_id: book.id, chapter_number: ch.number, percent: pct }) });
    } catch {}
  }

  function handleScroll(e) {
    const el = e.target;
    const pct = Math.round((el.scrollTop / (el.scrollHeight - el.clientHeight)) * 100);
    if (pct > 0 && user) saveProgress(Math.min(100, pct));
  }

  return (
    <div className="overlay" onClick={onClose}>
      <div className={`reader th-${theme}`} onClick={e => e.stopPropagation()}>
        {/* Top bar */}
        <div className="reader-bar">
          <div className="reader-id">
            <img src={book.cover_image} alt="" />
            <div>
              <h2>{book.title}</h2>
              <p>{book.author}</p>
            </div>
          </div>
          <div className="r-ctrls">
            {/* Theme dots */}
            <div className="th-dots">
              {themes.map(t => (
                <div key={t} className={`th-dot d-${t} ${theme === t ? "on" : ""}`} onClick={() => setTheme(t)} />
              ))}
            </div>
            {/* Font size */}
            <button className="pill" onClick={() => setFontSize(f => Math.max(0.8, f - 0.1))}>A−</button>
            <button className="pill" onClick={() => setFontSize(f => Math.min(1.6, f + 0.1))}>A+</button>
            {/* Bilingual */}
            <button className={`pill ${bilingual ? "on" : ""}`} onClick={() => setBilingual(v => !v)}>
              🌐 {bilingual ? "Bilingual" : "Single"}
            </button>
            {/* Translation language */}
            <div className="pill">
              <select value={transLang} onChange={e => setTransLang(e.target.value)}>
                {Object.entries(LANG_NAMES).map(([c, n]) => <option key={c} value={c}>{n}</option>)}
              </select>
            </div>
            {/* Bookmark */}
            <button className="pill" onClick={toggleBookmark}>🔖</button>
            {/* Export */}
            <button className="pill" onClick={exportChapter}>⬇ Export</button>
            {/* Audio */}
            {book.has_audiobook && (
              <button className="pill" onClick={() => startAudio(book, chapter)}>▶ Audio</button>
            )}
            {/* Close */}
            <button className="pill" onClick={onClose}>✕</button>
          </div>
        </div>

        {/* Chapter tabs */}
        <div className="reader-bar" style={{ borderBottom: "1px solid var(--rb2)" }}>
          <div className="ch-tabs">
            {book.chapters.map((c, i) => (
              <button key={i} className={`ch-tab ${chapter === i ? "on" : ""}`} onClick={() => setChapter(i)}>
                Ch {c.number}
              </button>
            ))}
          </div>
          <div className="r-sub">
            {["read", "notes", "reviews"].map(t => (
              <button key={t} className={`ch-tab ${tab === t ? "on" : ""}`} onClick={() => setTab(t)}>
                {t === "read" ? "📖 Read" : t === "notes" ? `📝 Notes (${(book.notes || []).length})` : `⭐ Reviews (${(book.reviews || []).length})`}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {tab === "read" ? (
          <div className={`reader-content ${bilingual && transLang !== "en" ? "bi" : ""}`} ref={contentRef} onScroll={handleScroll}>
            <div className="r-pane">
              <div className="r-pane-label">{ch.title}</div>
              <div className="prose" style={{ fontSize: fontSize + "rem" }}>{ch.content}</div>
            </div>
            {bilingual && transLang !== "en" && (
              <div className="r-pane">
                <div className="r-pane-label">{LANG_NAMES[transLang] || transLang} Translation {ch.translation_mode === "curated" ? "✓" : "(auto)"}</div>
                <div className="prose" style={{ fontSize: fontSize + "rem", direction: transLang === "ar" ? "rtl" : "ltr" }}>
                  {ch.translated_content}
                </div>
              </div>
            )}
          </div>
        ) : tab === "notes" ? (
          <div className="r-extra" ref={contentRef}>
            <div className="r-extra-inner">
              <h3 style={{ fontFamily: "var(--font-display)", marginBottom: 12 }}>📝 My Notes — {ch.title}</h3>
              {user ? (
                <>
                  <div className="note-form">
                    <input placeholder="Write a note for this chapter…" value={noteText} onChange={e => setNoteText(e.target.value)}
                           onKeyDown={e => e.key === "Enter" && saveNote()} />
                    <button className="btn btn-pri btn-sm" onClick={saveNote}>Save</button>
                  </div>
                  <div className="note-list">
                    {(book.notes || []).filter(n => n.chapter_number === ch.number).map(n => (
                      <div key={n.id} className="note-item">
                        <div>
                          <div style={{ fontSize: "0.84rem" }}>{n.note_text}</div>
                          <div className="muted" style={{ fontSize: "0.74rem", marginTop: 4 }}>{n.created_at}</div>
                        </div>
                        <button className="icon-btn" onClick={() => deleteNote(n.id)}>🗑</button>
                      </div>
                    ))}
                    {(book.notes || []).filter(n => n.chapter_number === ch.number).length === 0 && (
                      <p className="muted" style={{ padding: 16 }}>No notes for this chapter yet.</p>
                    )}
                  </div>
                </>
              ) : <p className="muted">Sign in to save notes.</p>}
            </div>
          </div>
        ) : (
          <div className="r-extra" ref={contentRef}>
            <div className="r-extra-inner">
              <h3 style={{ fontFamily: "var(--font-display)", marginBottom: 12 }}>⭐ Reviews</h3>
              {user && (
                <div className="rev-form">
                  <select value={revRating} onChange={e => setRevRating(Number(e.target.value))}>
                    {[5,4,3,2,1].map(r => <option key={r} value={r}>{"★".repeat(r)} ({r})</option>)}
                  </select>
                  <input placeholder="Write your review…" value={revText} onChange={e => setRevText(e.target.value)}
                         onKeyDown={e => e.key === "Enter" && postReview()} />
                  <button className="btn btn-pri btn-sm" onClick={postReview}>Post</button>
                </div>
              )}
              <div className="note-list">
                {(book.reviews || []).map((r, i) => (
                  <div key={i} className="note-item">
                    <div>
                      <div style={{ fontWeight: 700, fontSize: "0.88rem" }}>{r.user_name} <span style={{ color: "#b8860b" }}>{"★".repeat(r.rating)}</span></div>
                      <div style={{ fontSize: "0.84rem", marginTop: 2 }}>{r.comment}</div>
                      <div className="muted" style={{ fontSize: "0.74rem", marginTop: 4 }}>{r.created_at}</div>
                    </div>
                  </div>
                ))}
                {(book.reviews || []).length === 0 && <p className="muted" style={{ padding: 16 }}>No reviews yet. Be the first!</p>}
              </div>
            </div>
          </div>
        )}

        {/* Paywall bar */}
        {!ch.unlocked && (
          <div className="paywall">
            <span>🔒 Subscribe to unlock the full chapter and audiobook.</span>
            <button className="btn btn-pri btn-sm" onClick={onSubscribe}>View Plans</button>
          </div>
        )}
      </div>
    </div>
  );
}

/* ═══════════════════ SUBSCRIPTIONS VIEW ═══════════════════ */
function SubscriptionsView({ plans, user, payments, onCheckout, ui }) {
  const [cycle, setCycle] = useState("monthly");
  return (
    <section className="sec wrap">
      <div className="plans-top">
        <span className="hero-badge" style={{background:"var(--primary-soft)",color:"var(--primary)",border:"1px solid var(--primary)",display:"inline-block"}}>💎 Subscription Plans</span>
        <h2>{ui.choose_plan || "Choose Your Reading Plan"}</h2>
        <p className="muted">Unlock the full Library Hub experience — audiobooks, bilingual translation, notes, and more.</p>
        <div className="cycle-tog">
          <button className={`cyc-btn ${cycle === "monthly" ? "on" : ""}`} onClick={() => setCycle("monthly")}>Monthly</button>
          <button className={`cyc-btn ${cycle === "annual" ? "on" : ""}`} onClick={() => setCycle("annual")}>
            Annual <span className="save-tag">Save 20%</span>
          </button>
        </div>
      </div>

      <div className="plans-row">
        {plans.map(p => {
          const price = cycle === "monthly" ? p.monthly_price : p.annual_price;
          const isPopular = p.id === "plus";
          const isCurrent = user && payments.some(pay => pay.plan_id === p.id && pay.status === "paid");
          return (
            <div key={p.id} className={`plan ${isPopular ? "pop" : ""}`}>
              {isPopular && <span className="plan-badge">🌟 Most Popular</span>}
              <h3 style={{ fontFamily: "var(--font-display)" }}>{p.name}</h3>
              <div className="plan-price">
                {price === 0 ? "Free" : `$${price.toFixed(2)}`}
                {price > 0 && <small>/{cycle === "monthly" ? "mo" : "yr"}</small>}
              </div>
              <ul className="plan-feats">
                {p.features.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
              {isCurrent ? (
                <button className="btn btn-acc btn-block" disabled>✓ Current Plan</button>
              ) : price === 0 ? (
                <button className="btn btn-out btn-block" disabled>Included</button>
              ) : (
                <button className="btn btn-pri btn-block" onClick={() => onCheckout(p, cycle)}>
                  {ui.subscribe || "Subscribe Now"}
                </button>
              )}
            </div>
          );
        })}
      </div>

      {/* Invoice history */}
      {payments.length > 0 && (
        <div className="hist-card">
          <h3 style={{ fontFamily: "var(--font-display)", marginBottom: 12 }}>📋 Invoice History</h3>
          <table className="tbl">
            <thead><tr><th>Date</th><th>Plan</th><th>Amount</th><th>Status</th></tr></thead>
            <tbody>
              {payments.map((p, i) => (
                <tr key={i}>
                  <td>{p.created_at}</td>
                  <td>{p.plan_id}</td>
                  <td>${Number(p.amount_paid).toFixed(2)}</td>
                  <td><span className="badge badge-ok">{p.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

/* ═══════════════════ CHECKOUT MODAL ═══════════════════ */
function CheckoutModal({ plan, cycle, onClose, onSuccess, onToast }) {
  const [method, setMethod] = useState("card");
  const [card, setCard] = useState("");
  const [promo, setPromo] = useState("");
  const [promoApplied, setPromoApplied] = useState(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const basePrice = cycle === "monthly" ? plan.monthly_price : plan.annual_price;
  const discount = promoApplied ? 0.20 : 0;
  const total = (basePrice * (1 - discount)).toFixed(2);

  function applyPromo() {
    if (promo.trim().toUpperCase() === "READ20") {
      setPromoApplied(true);
      onToast("🎉 Promo READ20 applied — 20% off!");
    } else {
      onToast("Invalid promo code");
    }
  }

  async function submit() {
    setErr(""); setBusy(true);
    try {
      const d = await api("/api/subscribe", {
        method: "POST",
        body: JSON.stringify({ plan_id: plan.id, billing_cycle: cycle, payment_method: method, card_number: card, promo_code: promoApplied ? "READ20" : "" })
      });
      onSuccess(d);
      onClose();
      onToast(`🎉 Subscribed to ${plan.name}!`);
    } catch (e) { setErr(e.message); } finally { setBusy(false); }
  }

  return (
    <div className="overlay" onClick={onClose}>
      <div className="dialog" onClick={e => e.stopPropagation()}>
        <div className="dialog-hdr">
          <h3>Checkout — {plan.name}</h3>
          <button className="icon-btn" onClick={onClose}>✕</button>
        </div>

        <div className="stack">
          <div className="pay-methods">
            <label className="radio-card" style={{ borderColor: method === "card" ? "var(--primary)" : "" }}>
              <input type="radio" checked={method === "card"} onChange={() => setMethod("card")} /> 💳 Card
            </label>
            <label className="radio-card" style={{ borderColor: method === "wallet" ? "var(--primary)" : "" }}>
              <input type="radio" checked={method === "wallet"} onChange={() => setMethod("wallet")} /> 📱 Wallet
            </label>
          </div>

          {method === "card" && (
            <label>Card Number
              <input placeholder="4242 4242 4242 4242" value={card} onChange={e => setCard(e.target.value)} />
            </label>
          )}

          <div className="promo-row">
            <input placeholder="Promo code (try READ20)" value={promo} onChange={e => setPromo(e.target.value)} />
            <button className="btn btn-out btn-sm" onClick={applyPromo}>Apply</button>
          </div>

          <div className="chk-sum">
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span>{plan.name} ({cycle})</span>
              <span>${basePrice.toFixed(2)}</span>
            </div>
            {promoApplied && <div style={{ display: "flex", justifyContent: "space-between", color: "var(--accent)" }}>
              <span>READ20 discount</span><span>-{(discount * 100).toFixed(0)}%</span>
            </div>}
            <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700, marginTop: 6, borderTop: "1px solid var(--border)", paddingTop: 6 }}>
              <span>Total</span><span>${total}</span>
            </div>
          </div>

          {err && <div className="form-err">{err}</div>}

          <button className="btn btn-pri btn-block" disabled={busy} onClick={submit}>
            {busy ? "Processing…" : `Pay $${total}`}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════ AUDIO PLAYER BAR ═══════════════════ */
function AudioPlayerBar({ audioBook, audioChapter, onStop }) {
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [sentenceIdx, setSentenceIdx] = useState(0);
  const [sleepMin, setSleepMin] = useState(0);
  const synthRef = useRef(null);
  const sleepRef = useRef(null);

  const ch = audioBook.chapters[audioChapter] || audioBook.chapters[0];
  const sentences = useMemo(() => ch.content.split(/(?<=[.!?])\s+/).filter(s => s.trim()), [ch]);
  const progress = sentences.length > 0 ? Math.round(((sentenceIdx + 1) / sentences.length) * 100) : 0;

  const LANG_VOICE = { en: "en-US", es: "es-ES", fr: "fr-FR", de: "de-DE", hi: "hi-IN", ar: "ar-SA", ja: "ja-JP", zh: "zh-CN" };

  function speak(idx) {
    if (idx >= sentences.length) { setPlaying(false); setSentenceIdx(0); return; }
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(sentences[idx]);
    u.rate = speed;
    u.lang = LANG_VOICE["en"] || "en-US";
    u.onend = () => { setSentenceIdx(idx + 1); speak(idx + 1); };
    synthRef.current = u;
    setSentenceIdx(idx);
    window.speechSynthesis.speak(u);
  }

  function togglePlay() {
    if (playing) {
      window.speechSynthesis.cancel();
      setPlaying(false);
    } else {
      setPlaying(true);
      speak(sentenceIdx);
    }
  }

  function prev() { const i = Math.max(0, sentenceIdx - 1); setSentenceIdx(i); if (playing) speak(i); }
  function next() { const i = Math.min(sentences.length - 1, sentenceIdx + 1); setSentenceIdx(i); if (playing) speak(i); }

  useEffect(() => {
    if (sleepMin > 0) {
      sleepRef.current = setTimeout(() => { window.speechSynthesis.cancel(); setPlaying(false); setSleepMin(0); }, sleepMin * 60000);
    }
    return () => clearTimeout(sleepRef.current);
  }, [sleepMin]);

  useEffect(() => () => window.speechSynthesis.cancel(), []);

  function handleStop() { window.speechSynthesis.cancel(); setPlaying(false); onStop(); }

  return (
    <div className="audio-bar">
      <div className="wrap audio-inner">
        <div className="a-info">
          <img src={audioBook.cover_image} alt="" />
          <div>
            <div style={{ fontWeight: 700, fontSize: "0.88rem" }}>{truncate(audioBook.title, 24)}</div>
            <div className="a-sub">{ch.title}</div>
          </div>
        </div>

        <div className="a-ctrls">
          <button className="icon-btn" onClick={prev}>⏮</button>
          <button className="play-btn" onClick={togglePlay}>{playing ? "⏸" : "▶"}</button>
          <button className="icon-btn" onClick={next}>⏭</button>
        </div>

        <div className="a-prog">
          <div className="a-status">Sentence {sentenceIdx + 1} / {sentences.length}</div>
          <div className="prog-track"><div className="prog-fill" style={{ width: progress + "%" }} /></div>
        </div>

        <div className="a-extras">
          <select value={speed} onChange={e => setSpeed(Number(e.target.value))}>
            {[0.75, 1, 1.25, 1.5, 2].map(s => <option key={s} value={s}>{s}x</option>)}
          </select>
          <select value={sleepMin} onChange={e => setSleepMin(Number(e.target.value))}>
            <option value={0}>No Timer</option>
            <option value={5}>5 min</option>
            <option value={15}>15 min</option>
            <option value={30}>30 min</option>
            <option value={60}>60 min</option>
          </select>
          <button className="icon-btn" onClick={handleStop}>✕</button>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════ TOAST ═══════════════════ */
function Toast({ msg }) {
  if (!msg) return null;
  return <div className="toast">{msg}</div>;
}

/* ═══════════════════ FOOTER ═══════════════════ */
function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-inner">
        <span>© 2024 Library Hub — React + Python Full-Stack</span>
        <span>14 Books · 12 Genres · 8 Languages</span>
      </div>
    </footer>
  );
}

/* ═══════════════════ APP (ROOT) ═══════════════════ */
function App() {
  const [view, setView] = useState("library"); // library | audiobooks | shelf | plans
  const [lang, setLang] = useState("en");
  const [search, setSearch] = useState("");
  const [tierFilter, setTierFilter] = useState("all");
  const [genreFilter, setGenreFilter] = useState("all");
  const [sort, setSort] = useState("default");

  const [genres, setGenres] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [uiStrings, setUiStrings] = useState({});
  const [plans, setPlans] = useState([]);
  const [books, setBooks] = useState([]);
  const [user, setUser] = useState(null);
  const [bookmarks, setBookmarks] = useState([]);
  const [payments, setPayments] = useState([]);
  const [progressList, setProgressList] = useState([]);

  const [readerBookId, setReaderBookId] = useState(null);
  const [checkoutPlan, setCheckoutPlan] = useState(null);
  const [checkoutCycle, setCheckoutCycle] = useState("monthly");

  const [audioBook, setAudioBook] = useState(null);
  const [audioChapter, setAudioChapter] = useState(0);

  const [toast, setToast] = useState("");
  const toastTimer = useRef(null);

  function onToast(msg) {
    setToast(msg);
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(""), 3000);
  }

  // ── Bootstrap ──
  useEffect(() => {
    api("/api/bootstrap").then(d => {
      setGenres(d.genres || []);
      setLanguages(d.languages || []);
      setUiStrings(d.ui_translations || {});
      setPlans(d.plans || []);
      setBooks(d.books || []);
      setUser(d.user || null);
      setBookmarks(d.bookmarks || []);
      setPayments(d.payments || []);
      setProgressList(d.progress || []);
    }).catch(() => {});
  }, []);

  // UI translations for selected lang
  const ui = useMemo(() => (uiStrings[lang] || uiStrings["en"] || {}), [uiStrings, lang]);

  // Progress map: { bookId: { chapter_number, percent } }
  const progressMap = useMemo(() => {
    const m = {};
    (progressList || []).forEach(p => { m[p.book_id] = p; });
    return m;
  }, [progressList]);

  // Filtered books
  const filteredBooks = useMemo(() => {
    let list = books;
    if (view === "audiobooks") list = list.filter(b => b.has_audiobook);
    if (view === "shelf") {
      const bmIds = new Set(bookmarks.map(b => b.book_id));
      list = list.filter(b => bmIds.has(b.id));
    }
    if (genreFilter && genreFilter !== "all") list = list.filter(b => b.genre === genreFilter);
    if (tierFilter && tierFilter !== "all") list = list.filter(b => b.tier === tierFilter);
    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter(b =>
        b.title.toLowerCase().includes(q) ||
        b.author.toLowerCase().includes(q) ||
        b.description.toLowerCase().includes(q) ||
        (b.tags || []).some(t => t.toLowerCase().includes(q))
      );
    }
    return list;
  }, [books, view, genreFilter, tierFilter, search, bookmarks]);

  // Open reader
  function openReader(bookId, startWithAudio) {
    setReaderBookId(bookId);
    if (startWithAudio) {
      const b = books.find(x => x.id === bookId);
      if (b) startAudio(b, 0);
    }
  }

  // Start audio
  function startAudio(book, chIdx) {
    // Fetch full book data for chapters
    api(`/api/books/${book.id}?lang=en`).then(d => {
      setAudioBook(d.book);
      setAudioChapter(chIdx || 0);
    }).catch(() => onToast("Could not load audiobook"));
  }

  // Logout
  async function handleLogout() {
    try {
      await api("/api/auth/logout", { method: "POST" });
      setUser(null);
      setBookmarks([]);
      setPayments([]);
      setProgressList([]);
      onToast("Signed out");
    } catch {}
  }

  // Checkout success
  function onCheckoutSuccess(d) {
    if (d.user) setUser(d.user);
    if (d.payments) setPayments(d.payments);
    if (d.books) setBooks(d.books);
  }

  return (
    <div>
      <Header
        view={view} setView={setView}
        lang={lang} setLang={setLang}
        languages={languages}
        user={user} onLogout={handleLogout}
        bookmarkCount={bookmarks.length}
        ui={ui}
      />

      {view !== "plans" && (
        <HeroSection
          books={filteredBooks} ui={ui}
          search={search} setSearch={setSearch}
          tierFilter={tierFilter} setTierFilter={setTierFilter}
          genres={genres} genreFilter={genreFilter} setGenreFilter={setGenreFilter}
          progressMap={progressMap}
        />
      )}

      {view !== "plans" && (
        <ContinueReading books={books} progressMap={progressMap} onOpen={openReader} />
      )}

      {view === "plans" ? (
        <SubscriptionsView
          plans={plans} user={user} payments={payments}
          onCheckout={(p, c) => { setCheckoutPlan(p); setCheckoutCycle(c); }}
          ui={ui}
        />
      ) : (
        <BookGrid
          books={filteredBooks} onOpen={openReader}
          ui={ui} sort={sort} setSort={setSort}
        />
      )}

      <Footer />

      {/* Reader modal */}
      {readerBookId && (
        <ReaderModal
          bookId={readerBookId} lang={lang}
          onClose={() => setReaderBookId(null)}
          user={user} onToast={onToast}
          startAudio={startAudio}
          onSubscribe={() => { setReaderBookId(null); setView("plans"); }}
        />
      )}

      {/* Checkout modal */}
      {checkoutPlan && (
        <CheckoutModal
          plan={checkoutPlan} cycle={checkoutCycle}
          onClose={() => setCheckoutPlan(null)}
          onSuccess={onCheckoutSuccess}
          onToast={onToast}
        />
      )}

      {/* Audio player */}
      {audioBook && (
        <AudioPlayerBar
          audioBook={audioBook} audioChapter={audioChapter}
          onStop={() => setAudioBook(null)}
        />
      )}

      <Toast msg={toast} />
    </div>
  );
}

/* ── Mount ── */
ReactDOM.createRoot(document.getElementById("root")).render(<App />);
