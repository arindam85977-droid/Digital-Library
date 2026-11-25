"""Generate bespoke illustrated SVG book cover images in static/covers/."""

from pathlib import Path
from catalog import BOOKS

COVERS_DIR = Path(__file__).resolve().parent / "static" / "covers"

MOTIFS = {
    "silent-orbit": """
      <circle cx="210" cy="120" r="56" fill="none" stroke="#7dd3fc" stroke-width="2" opacity="0.45"/>
      <ellipse cx="210" cy="120" rx="88" ry="26" transform="rotate(-18 210 120)" fill="none" stroke="#bae6fd" stroke-width="2.5" opacity="0.7"/>
      <circle cx="210" cy="120" r="28" fill="#38bdf8" opacity="0.85"/>
      <circle cx="70" cy="70" r="2.5" fill="#fff"/><circle cx="110" cy="48" r="1.8" fill="#fff"/>
      <circle cx="258" cy="60" r="2.2" fill="#fff"/><circle cx="60" cy="180" r="2" fill="#7dd3fc"/>
    """,
    "gardens-of-kyoto": """
      <rect x="65" y="95" width="170" height="10" rx="3" fill="#fde68a" opacity="0.85"/>
      <rect x="80" y="114" width="140" height="7" rx="2" fill="#fde68a" opacity="0.7"/>
      <rect x="95" y="105" width="12" height="95" fill="#fef3c7" opacity="0.75"/>
      <rect x="193" y="105" width="12" height="95" fill="#fef3c7" opacity="0.75"/>
      <circle cx="235" cy="65" r="26" fill="#fbbf24" opacity="0.35"/>
      <circle cx="80" cy="68" r="6" fill="#fca5a5" opacity="0.8"/><circle cx="220" cy="145" r="5" fill="#fca5a5" opacity="0.8"/>
    """,
    "pythonic-intelligence": """
      <g stroke="#a7f3d0" stroke-width="2" opacity="0.65">
        <line x1="80" y1="85" x2="150" y2="120"/><line x1="80" y1="155" x2="150" y2="120"/>
        <line x1="150" y1="120" x2="220" y2="85"/><line x1="150" y1="120" x2="220" y2="155"/>
        <line x1="80" y1="85" x2="220" y2="85"/><line x1="80" y1="155" x2="220" y2="155"/>
      </g>
      <circle cx="80" cy="85" r="10" fill="#6ee7b7"/><circle cx="80" cy="155" r="10" fill="#6ee7b7"/>
      <circle cx="150" cy="120" r="15" fill="#34d399"/><circle cx="220" cy="85" r="10" fill="#6ee7b7"/>
      <circle cx="220" cy="155" r="10" fill="#6ee7b7"/>
    """,
    "clockwork-alibi": """
      <circle cx="150" cy="125" r="58" fill="none" stroke="#f9a8d4" stroke-width="4" opacity="0.8"/>
      <circle cx="150" cy="125" r="44" fill="none" stroke="#fbcfe8" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.7"/>
      <line x1="150" y1="125" x2="150" y2="88" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
      <line x1="150" y1="125" x2="178" y2="138" stroke="#f472b6" stroke-width="3" stroke-linecap="round"/>
      <circle cx="150" cy="125" r="6" fill="#fff"/>
    """,
    "empires-of-silk": """
      <circle cx="150" cy="118" r="50" fill="none" stroke="#fcd34d" stroke-width="2.5" opacity="0.75"/>
      <polygon points="150,58 162,106 210,118 162,130 150,178 138,130 90,118 138,106" fill="#fde68a" opacity="0.82"/>
      <circle cx="150" cy="118" r="10" fill="#7c3f11"/>
    """,
    "atomic-calm": """
      <path d="M150 185 C110 140 105 90 150 55 C195 90 190 140 150 185 Z" fill="#a7f3d0" opacity="0.78"/>
      <line x1="150" y1="65" x2="150" y2="185" stroke="#064e3b" stroke-width="3" opacity="0.6"/>
      <circle cx="150" cy="120" r="68" fill="none" stroke="#ecfdf5" stroke-width="1.5" opacity="0.45"/>
    """,
    "compounding-craft": """
      <rect x="75" y="145" width="28" height="45" rx="4" fill="#93c5fd" opacity="0.65"/>
      <rect x="115" y="120" width="28" height="70" rx="4" fill="#93c5fd" opacity="0.78"/>
      <rect x="155" y="92" width="28" height="98" rx="4" fill="#bfdbfe" opacity="0.88"/>
      <rect x="195" y="60" width="28" height="130" rx="4" fill="#eff6ff" opacity="0.95"/>
    """,
    "meditations-modern": """
      <rect x="92" y="75" width="116" height="12" rx="3" fill="#fef3c7" opacity="0.85"/>
      <rect x="108" y="87" width="16" height="92" fill="#e7e5e4" opacity="0.78"/>
      <rect x="142" y="87" width="16" height="92" fill="#e7e5e4" opacity="0.78"/>
      <rect x="176" y="87" width="16" height="92" fill="#e7e5e4" opacity="0.78"/>
      <rect x="86" y="179" width="128" height="12" rx="3" fill="#fef3c7" opacity="0.85"/>
    """,
    "lantern-sonnets": """
      <line x1="150" y1="35" x2="150" y2="75" stroke="#f3e8ff" stroke-width="2.5"/>
      <rect x="122" y="75" width="56" height="78" rx="14" fill="#fef08a" opacity="0.85"/>
      <circle cx="150" cy="114" r="46" fill="#fde047" opacity="0.22"/>
      <path d="M55 185 Q100 170 150 185 T245 185" fill="none" stroke="#e9d5ff" stroke-width="3" opacity="0.7"/>
    """,
    "starlight-academy": """
      <path d="M65 155 Q115 95 160 130 T240 85" fill="none" stroke="#fef08a" stroke-width="3" stroke-dasharray="7 6"/>
      <circle cx="65" cy="155" r="7" fill="#fef08a"/><circle cx="240" cy="85" r="10" fill="#fde047"/>
      <polygon points="150,62 156,78 172,78 159,88 164,104 150,94 136,104 141,88 128,78 144,78" fill="#fff" opacity="0.85"/>
    """,
    "fox-who-borrowed-stars": """
      <circle cx="215" cy="74" r="24" fill="#fef08a" opacity="0.9"/>
      <polygon points="105,165 150,92 195,165" fill="#fed7aa" opacity="0.9"/>
      <polygon points="116,104 128,74 144,98" fill="#fdba74"/>
      <polygon points="184,104 172,74 156,98" fill="#fdba74"/>
      <circle cx="138" cy="130" r="4" fill="#431407"/><circle cx="162" cy="130" r="4" fill="#431407"/>
      <circle cx="150" cy="148" r="5" fill="#431407"/>
    """,
    "neural-symphony": """
      <path d="M50 125 Q80 65 110 125 T170 125 T230 125 T265 125" fill="none" stroke="#ccfbf1" stroke-width="4" stroke-linecap="round"/>
      <path d="M50 125 Q80 175 110 125 T170 125 T230 125 T265 125" fill="none" stroke="#5eead4" stroke-width="2.5" opacity="0.75"/>
      <circle cx="150" cy="70" r="8" fill="#99f6e4"/>
    """,
    "shadow-lighthouse": """
      <polygon points="150,74 270,40 270,108" fill="#fef08a" opacity="0.28"/>
      <polygon points="134,185 142,84 158,84 166,185" fill="#e5e7eb" opacity="0.9"/>
      <rect x="139" y="66" width="22" height="18" rx="3" fill="#fca5a5"/>
      <path d="M50 185 Q150 168 250 185" fill="none" stroke="#9ca3af" stroke-width="4"/>
    """,
    "kitchen-alchemist": """
      <circle cx="150" cy="118" r="48" fill="#fef08a" opacity="0.88"/>
      <circle cx="150" cy="118" r="64" fill="none" stroke="#fef9c3" stroke-width="2" stroke-dasharray="5 6"/>
      <path d="M60 176 Q150 154 240 176" fill="none" stroke="#fde047" stroke-width="4"/>
    """,
}


def extract_colors(gradient_str):
    import re
    colors = re.findall(r"#[0-9a-fA-F]{6}", gradient_str)
    if len(colors) >= 2:
        return colors[0], colors[-1]
    return "#1b4332", "#40916c"


def generate_all_covers():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    for book in BOOKS:
        c1, c2 = extract_colors(book["cover_gradient"])
        motif = MOTIFS.get(book["id"], '<circle cx="150" cy="120" r="45" fill="#ffffff" opacity="0.25"/>')
        title = book["title"].replace("&", "&amp;")
        author = book["author"].replace("&", "&amp;")
        genre = book["genre_label"].replace("&", "&amp;")
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 420" width="300" height="420">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="300" height="420" rx="14" fill="url(#bg)"/>
  <rect x="0" y="0" width="16" height="420" fill="#ffffff" opacity="0.14"/>
  <rect x="24" y="18" width="258" height="384" rx="10" fill="none" stroke="#ffffff" stroke-opacity="0.2" stroke-width="1.5"/>
  <text x="36" y="46" font-family="system-ui, sans-serif" font-size="11" font-weight="700" letter-spacing="1.5" fill="{book['cover_accent']}" opacity="0.95">{genre.upper()}</text>
  <g transform="translate(0, 18)">{motif}</g>
  <foreignObject x="32" y="248" width="238" height="110">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Georgia,serif;color:#ffffff;font-size:23px;font-weight:700;line-height:1.18;text-shadow:0 2px 8px rgba(0,0,0,0.35);">
      {title}
    </div>
  </foreignObject>
  <text x="34" y="384" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#ffffff" opacity="0.9">{author}</text>
</svg>
"""
        (COVERS_DIR / f"{book['id']}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    generate_all_covers()
    print(f"Generated {len(BOOKS)} book covers in {COVERS_DIR}")
