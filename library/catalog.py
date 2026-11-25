"""Book catalog spanning all major genres with full readable chapters."""

GENRES = [
    {"id": "all", "name": "All Genres", "icon": "📚"},
    {"id": "fiction", "name": "Fiction", "icon": "📖"},
    {"id": "scifi-fantasy", "name": "Sci-Fi & Fantasy", "icon": "🚀"},
    {"id": "science-tech", "name": "Science & Tech", "icon": "🔬"},
    {"id": "mystery-thriller", "name": "Mystery & Thriller", "icon": "🕵️"},
    {"id": "history-bio", "name": "History & Biography", "icon": "🏛️"},
    {"id": "self-help", "name": "Self-Help & Mindset", "icon": "🌱"},
    {"id": "business-finance", "name": "Business & Finance", "icon": "📈"},
    {"id": "philosophy-classics", "name": "Philosophy & Classics", "icon": "🦉"},
    {"id": "poetry-drama", "name": "Poetry & Drama", "icon": "🎭"},
    {"id": "young-adult", "name": "Young Adult", "icon": "✨"},
    {"id": "children", "name": "Children's Tales", "icon": "🦊"},
]

BOOKS = [
    {
        "id": "silent-orbit",
        "title": "The Silent Orbit",
        "author": "Elena Vance",
        "genre": "scifi-fantasy",
        "genre_label": "Sci-Fi & Fantasy",
        "tier": "free",
        "rating": 4.8,
        "reviews_count": 1240,
        "year": 2024,
        "pages": 312,
        "audio_minutes": 410,
        "has_audiobook": True,
        "narrator": "Clara Sterling",
        "cover_gradient": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
        "cover_accent": "#7dd3fc",
        "description": "When an orbital cartographer intercepts a repeating harmonic signal from beyond Neptune, she uncovers an archive left by Earth's earliest deep-space probes—and a message meant for the next century.",
        "tags": ["Space Exploration", "First Contact", "Hard Sci-Fi"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Listening at the Rim",
                "duration_min": 14,
                "content": (
                    "The radio dishes at Station Meridian never truly slept; they turned slowly against the stars like patient sunflowers chasing an invisible sun. "
                    "Dr. Maya Lin adjusted her headset as the telemetry stream scrolled across the amber monitor. "
                    "At 03:14 UTC, a faint mathematical pulse broke through the cosmic background hiss—three prime numbers followed by a silence that felt almost deliberate.\n\n"
                    "She leaned closer to the console and isolated the frequency band. Standard orbital beacons drifted with solar wind, yet this signal held steady to the tenth decimal place. "
                    "Outside the observation dome, Saturn hung like a carved pearl in black velvet, reminding her how far humanity had traveled and how little it still understood.\n\n"
                    "By dawn, the decoded header revealed coordinates pointing not to a distant galaxy, but to an abandoned relay built eighty years earlier. "
                    "Someone—or something—had been waiting for anyone patient enough to listen."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: The Glass Archive",
                "duration_min": 16,
                "content": (
                    "Docking with the derelict relay required steady thrusters and steadier nerves. Inside the unpressurized hull, dust floated like frozen snow in the beam of Maya's helmet lamp. "
                    "The central core held crystalline storage wafers etched with languages from every continent on Earth.\n\n"
                    "When her portable terminal linked to the core, a calm voice filled her suit speakers—not an alien intelligence, but the preserved recording of the station's original architect. "
                    "The message spoke of curiosity as humanity's brightest compass, urging future explorers to carry knowledge forward rather than fear the unknown."
                ),
            },
        ],
    },
    {
        "id": "gardens-of-kyoto",
        "title": "Autumn Gardens of Kyoto",
        "author": "Haruki Takahashi",
        "genre": "fiction",
        "genre_label": "Fiction",
        "tier": "free",
        "rating": 4.9,
        "reviews_count": 2180,
        "year": 2023,
        "pages": 248,
        "audio_minutes": 325,
        "has_audiobook": True,
        "narrator": "Kenji Sato",
        "cover_gradient": "linear-gradient(135deg, #4a1c1c 0%, #8b3a2b 55%, #d97706 100%)",
        "cover_accent": "#fde68a",
        "description": "A restorative novel about a master carpenter who returns to his family's wooden teahouse in Kyoto and discovers unspoken letters tucked beneath the floorboards.",
        "tags": ["Literary Fiction", "Japan", "Family"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Cedar and Rain",
                "duration_min": 12,
                "content": (
                    "October rain arrived in Kyoto softly, tapping a quiet rhythm across the clay roof tiles of the old cedar teahouse. "
                    "Renji set down his canvas tool bag and breathed in the familiar scent of aged cypress, roasted green tea, and damp moss.\n\n"
                    "Thirty years had passed since he had apprenticed beside his grandfather in this very courtyard. The maple tree by the stone lantern had grown tall enough to brush the eaves, "
                    "and its crimson leaves carpeted the stepping stones like a painted scroll.\n\n"
                    "As Renji pried open a warped floorboard near the hearth, he spotted a linen envelope tied with indigo thread. Inside lay forty years of reflections on patience, craft, and the courage to begin again."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: The Tea Master's Ledger",
                "duration_min": 15,
                "content": (
                    "Each page of the ledger recorded not prices or debts, but the names of neighbors who had shared shelter during winter storms. "
                    "Renji realized his grandfather had measured wealth in quiet kindnesses rather than coin.\n\n"
                    "By evening, the neighborhood baker stopped by with warm chestnuts, and the teahouse lantern glowed once more against the dusk."
                ),
            },
        ],
    },
    {
        "id": "pythonic-intelligence",
        "title": "Architectures of Intelligence",
        "author": "Dr. Aris Thorne",
        "genre": "science-tech",
        "genre_label": "Science & Tech",
        "tier": "plus",
        "rating": 4.7,
        "reviews_count": 890,
        "year": 2025,
        "pages": 390,
        "audio_minutes": 510,
        "has_audiobook": True,
        "narrator": "Marcus Reid",
        "cover_gradient": "linear-gradient(135deg, #134e5e 0%, #1b4332 60%, #2d6a4f 100%)",
        "cover_accent": "#a7f3d0",
        "description": "A crystal-clear journey from classical algorithms and information theory to modern distributed computing, told through stories of the pioneers who built our digital world.",
        "tags": ["Computer Science", "AI", "Engineering"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Patterns in the Noise",
                "duration_min": 18,
                "content": (
                    "Every breakthrough in computing begins with a simple question: how do we represent thought in a form a machine can manipulate reliably? "
                    "From Jacquard's punched cards to Claude Shannon's insight that logic could ride on electrical switches, abstraction has always been our sharpest lever.\n\n"
                    "When engineers design software today, they stand atop decades of layered ideas—memory hierarchies, error-correcting codes, and clean protocols that let billions of devices converse in milliseconds. "
                    "Understanding these foundations transforms code from fragile instructions into resilient architecture."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Thinking in Systems",
                "duration_min": 16,
                "content": (
                    "Great systems fail gracefully. Rather than assuming hardware never falters or networks never stall, resilient engineers build feedback loops, timeouts, and observability into the very fabric of an application.\n\n"
                    "Clarity of design is not an aesthetic luxury; it is the surest defense against complexity."
                ),
            },
        ],
    },
    {
        "id": "clockwork-alibi",
        "title": "The Clockwork Alibi",
        "author": "Nadia Mercer",
        "genre": "mystery-thriller",
        "genre_label": "Mystery & Thriller",
        "tier": "plus",
        "rating": 4.6,
        "reviews_count": 1540,
        "year": 2024,
        "pages": 340,
        "audio_minutes": 445,
        "has_audiobook": True,
        "narrator": "Evelyn Shaw",
        "cover_gradient": "linear-gradient(135deg, #1f1c2c 0%, #432c51 55%, #734b6d 100%)",
        "cover_accent": "#f9a8d4",
        "description": "A watchmaker vanishes from a locked Geneva atelier during the winter solstice, leaving behind twelve synchronized pocket watches—each stopped at a different minute.",
        "tags": ["Locked Room", "Detective", "Suspense"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Twelve Stopped Minutes",
                "duration_min": 15,
                "content": (
                    "Snow muffled the cobblestones of Old Geneva as Inspector Claire Moreau stepped into the watchmaker's workshop. "
                    "Brass gears gleamed under green banker's lamps, and the air smelled faintly of machine oil and espresso.\n\n"
                    "On the velvet workbench sat twelve gold pocket watches arranged in a crescent. Every clock on the wall ticked steadily toward midnight, yet the twelve watches had stopped at precisely spaced intervals.\n\n"
                    "Moreau slipped on her cotton gloves and examined the nearest dial. Someone had staged an alibi so intricate it could only unravel from the inside."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: The Mainspring Cipher",
                "duration_min": 17,
                "content": (
                    "Under a jeweler's loupe, the inside casing of the seventh watch revealed microscopic engravings—not serial numbers, but train departure times across three Alpine borders.\n\n"
                    "Moreau realized the watchmaker had not been kidnapped at all; he had left a mechanical map for the only detective patient enough to read time backwards."
                ),
            },
        ],
    },
    {
        "id": "empires-of-silk",
        "title": "Empires of Silk and Compass",
        "author": "Prof. Tariq Al-Mansoor",
        "genre": "history-bio",
        "genre_label": "History & Biography",
        "tier": "free",
        "rating": 4.8,
        "reviews_count": 970,
        "year": 2023,
        "pages": 420,
        "audio_minutes": 560,
        "has_audiobook": True,
        "narrator": "Omar Sharif Jr.",
        "cover_gradient": "linear-gradient(135deg, #3c1e08 0%, #7c3f11 55%, #b45309 100%)",
        "cover_accent": "#fcd34d",
        "description": "How caravan routes, maritime astrolabes, and translating scholars connected Baghdad, Samarkand, Venice, and Xi'an into the first global network of ideas.",
        "tags": ["World History", "Silk Road", "Cultural Exchange"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Crossroads of Paper and Stars",
                "duration_min": 17,
                "content": (
                    "Long before undersea fiber-optic cables linked continents, merchants and astronomers carried discoveries across deserts and monsoon seas. "
                    "In ninth-century Baghdad, the House of Wisdom gathered manuscripts from Greece, Persia, and India, translating geometry, medicine, and astronomy into a shared scientific language.\n\n"
                    "Paper mills along the Silk Road lowered the cost of books, turning rare royal treasures into companions for students and travelers alike. "
                    "Every city along the route became a living library where stories, spices, and star charts changed hands."
                ),
            },
        ],
    },
    {
        "id": "atomic-calm",
        "title": "The Architecture of Calm",
        "author": "Dr. Maya Bennett",
        "genre": "self-help",
        "genre_label": "Self-Help & Mindset",
        "tier": "free",
        "rating": 4.9,
        "reviews_count": 3420,
        "year": 2024,
        "pages": 224,
        "audio_minutes": 295,
        "has_audiobook": True,
        "narrator": "Maya Bennett",
        "cover_gradient": "linear-gradient(135deg, #1b4332 0%, #40916c 60%, #74c69d 100%)",
        "cover_accent": "#ecfdf5",
        "description": "Practical neuroscience and gentle daily rituals for reclaiming focus, reducing digital fatigue, and building sustainable creative energy.",
        "tags": ["Mindfulness", "Habits", "Focus"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Quiet Mornings",
                "duration_min": 11,
                "content": (
                    "Attention is not an infinite reservoir; it is a garden that reflects what we choose to water first thing in the morning. "
                    "When our waking minutes begin with urgent notifications, our nervous system spends the rest of the day defending against imaginary fires.\n\n"
                    "By protecting even twenty unhurried minutes—for reading, stretching, or watching morning light cross the floor—we train our minds to respond thoughtfully rather than reactively. "
                    "Small, consistent rituals outlast dramatic resolutions every single time."
                ),
            },
        ],
    },
    {
        "id": "compounding-craft",
        "title": "Compounding Craft",
        "author": "Julian Brooks",
        "genre": "business-finance",
        "genre_label": "Business & Finance",
        "tier": "plus",
        "rating": 4.7,
        "reviews_count": 1120,
        "year": 2025,
        "pages": 286,
        "audio_minutes": 360,
        "has_audiobook": True,
        "narrator": "David Vance",
        "cover_gradient": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%)",
        "cover_accent": "#bfdbfe",
        "description": "How independent founders, sustainable businesses, and thoughtful investors create enduring value without burning out.",
        "tags": ["Strategy", "Finance", "Entrepreneurship"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Value Over Velocity",
                "duration_min": 14,
                "content": (
                    "Speed attracts headlines, but durability wins decades. The healthiest organizations rarely chase every passing trend; instead, they obsess over solving one real problem with unmistakable craft.\n\n"
                    "Financial resilience begins with understanding cash flow, respecting customer trust, and reinvesting steadily in people and product quality. "
                    "When incentives align with long-term usefulness, growth becomes a natural consequence rather than a frantic sprint."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Margins of Safety",
                "duration_min": 15,
                "content": (
                    "Great operators plan for calm weather and stormy quarters alike. Keeping healthy reserves allows a team to think clearly, say no to distracting shortcuts, and honor commitments to customers."
                ),
            },
        ],
    },
    {
        "id": "meditations-modern",
        "title": "Letters from a Quiet Porch",
        "author": "Seneca & Aurelius (Modern Edition)",
        "genre": "philosophy-classics",
        "genre_label": "Philosophy & Classics",
        "tier": "free",
        "rating": 4.9,
        "reviews_count": 4100,
        "year": 2022,
        "pages": 196,
        "audio_minutes": 250,
        "has_audiobook": True,
        "narrator": "Arthur Pendelton",
        "cover_gradient": "linear-gradient(135deg, #292524 0%, #57534e 60%, #78716c 100%)",
        "cover_accent": "#fef3c7",
        "description": "A freshly translated and annotated companion of timeless Stoic wisdom on resilience, gratitude, and living with purpose.",
        "tags": ["Stoicism", "Classic", "Wisdom"],
        "chapters": [
            {
                "number": 1,
                "title": "Letter 1: On Time and Attention",
                "duration_min": 10,
                "content": (
                    "We are not given a short life, but we make it short when we scatter our hours across things that bring neither joy nor growth. "
                    "Guard your time as closely as you would guard your home.\n\n"
                    "No storm lasts forever, and no praise or blame from a stranger alters the truth of your character. Begin each day with clarity, act with fairness, and greet the evening with peace."
                ),
            },
        ],
    },
    {
        "id": "lantern-sonnets",
        "title": "Songs of the Lantern Keeper",
        "author": "Amelia Solis",
        "genre": "poetry-drama",
        "genre_label": "Poetry & Drama",
        "tier": "free",
        "rating": 4.8,
        "reviews_count": 640,
        "year": 2024,
        "pages": 142,
        "audio_minutes": 180,
        "has_audiobook": True,
        "narrator": "Amelia Solis",
        "cover_gradient": "linear-gradient(135deg, #311042 0%, #6d28d9 60%, #a855f7 100%)",
        "cover_accent": "#f3e8ff",
        "description": "Lyrical verses and spoken-word meditations celebrating oceans, city twilight, and the quiet resilience of everyday dreamers.",
        "tags": ["Poetry", "Spoken Word", "Lyrical"],
        "chapters": [
            {
                "number": 1,
                "title": "Poem I: Harbor at Dawn",
                "duration_min": 8,
                "content": (
                    "Before the ferries wake the bay,\n"
                    "The silver water holds the sky.\n"
                    "A single gull writes arcs of gray,\n"
                    "While sleepy lanterns say goodbye.\n\n"
                    "We carry light in pocket glass,\n"
                    "Small sparks against the longest night,\n"
                    "And learn as quiet seasons pass,\n"
                    "That shared warmth doubles in its flight."
                ),
            },
        ],
    },
    {
        "id": "starlight-academy",
        "title": "The Mapmakers of Starlight",
        "author": "Leo Carter",
        "genre": "young-adult",
        "genre_label": "Young Adult",
        "tier": "plus",
        "rating": 4.8,
        "reviews_count": 1850,
        "year": 2025,
        "pages": 328,
        "audio_minutes": 395,
        "has_audiobook": True,
        "narrator": "Zoe Harper",
        "cover_gradient": "linear-gradient(135deg, #0c4a6e 0%, #0284c7 55%, #38bdf8 100%)",
        "cover_accent": "#fef08a",
        "description": "At an academy perched atop floating sea cliffs, sixteen-year-old cartographer Tessa discovers an island that only appears when three friends read the same compass.",
        "tags": ["Adventure", "Friendship", "YA Fantasy"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: The Ink That Glowed",
                "duration_min": 13,
                "content": (
                    "Tessa never meant to spill lapis ink over the Headmaster's brass astrolabe, yet the moment the blue droplet touched the engraving, lines of golden coastline bloomed across the blank parchment.\n\n"
                    "Her best friend Sam leaned over the desk, eyes wide. No archipelago on any official chart looked like that—crescent bays curled around a volcano that wasn't on any map.\n\n"
                    "If the island moved with the tides, they had until Friday's high water to find a boat—and a crew brave enough to sail beyond the cliffs."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Tide-Chart Harbor",
                "duration_min": 14,
                "content": (
                    "At low tide, the sea caves below the academy echoed with bell buoys and lantern light. Sam unrolled the glowing parchment against the hull of an old skiff, watching the golden lines shift as the moon rose."
                ),
            },
        ],
    },
    {
        "id": "fox-who-borrowed-stars",
        "title": "Pip the Fox & the Moonlit Library",
        "author": "Clara Meadow",
        "genre": "children",
        "genre_label": "Children's Tales",
        "tier": "free",
        "rating": 4.9,
        "reviews_count": 2650,
        "year": 2024,
        "pages": 96,
        "audio_minutes": 95,
        "has_audiobook": True,
        "narrator": "Clara Meadow",
        "cover_gradient": "linear-gradient(135deg, #7c2d12 0%, #ea580c 55%, #fb923c 100%)",
        "cover_accent": "#fff7ed",
        "description": "A heartwarming bedtime adventure about a curious little fox who opens a hollow-oak library for owls, hedgehogs, and fireflies.",
        "tags": ["Bedtime Story", "Animals", "Family Read"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Acorn Bookmarks",
                "duration_min": 9,
                "content": (
                    "Deep in Whispering Woods, inside the cozy roots of Old Oak, Pip the little red fox swept the floor with his fluffy tail. "
                    "Tonight was opening night for the Forest Library!\n\n"
                    "Barnaby Owl brought books about cloud shapes, while Hazel Hedgehog delivered tiny dictionaries wrapped in clover leaves. "
                    "Fireflies floated near the ceiling like warm golden reading lamps, and every creature curled up together to hear a story before sleep."
                ),
            },
        ],
    },
    {
        "id": "neural-symphony",
        "title": "The Neural Symphony",
        "author": "Dr. Priya Nair",
        "genre": "science-tech",
        "genre_label": "Science & Tech",
        "tier": "audiobook_pro",
        "rating": 4.9,
        "reviews_count": 780,
        "year": 2025,
        "pages": 364,
        "audio_minutes": 490,
        "has_audiobook": True,
        "narrator": "Priya Nair",
        "cover_gradient": "linear-gradient(135deg, #064e3b 0%, #0d9488 55%, #2dd4bf 100%)",
        "cover_accent": "#ccfbf1",
        "description": "How music, memory, and rhythm reshape the human brain—an immersive blend of neuroscience and studio audio storytelling.",
        "tags": ["Neuroscience", "Music", "Audiobook Original"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Why Rhythm Moves Us",
                "duration_min": 16,
                "content": (
                    "Long before a child speaks a full sentence, they sway to a steady beat. Neuroimaging reveals that listening to a familiar melody lights up motor centers, memory hubs, and emotional pathways all at once.\n\n"
                    "Sound is not passive entertainment; it is an evolutionary bridge that synchronizes human minds across generations."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Memory in Harmony",
                "duration_min": 18,
                "content": (
                    "Patients who struggle to recall recent dates can often sing every verse of a childhood song. Rhythm creates structured anchors in the hippocampus, turning fleeting sound into durable memory."
                ),
            },
        ],
    },
    {
        "id": "shadow-lighthouse",
        "title": "Voices of the North Lighthouse",
        "author": "Henrik Lindqvist",
        "genre": "mystery-thriller",
        "genre_label": "Mystery & Thriller",
        "tier": "audiobook_pro",
        "rating": 4.8,
        "reviews_count": 1030,
        "year": 2025,
        "pages": 356,
        "audio_minutes": 470,
        "has_audiobook": True,
        "narrator": "Henrik Lindqvist",
        "cover_gradient": "linear-gradient(135deg, #111827 0%, #374151 55%, #6b7280 100%)",
        "cover_accent": "#fca5a5",
        "description": "An audio journalist travels to a remote Nordic sea stack to restore reel-to-reel tapes from 1974—and hears a voice that was never recorded on the manifest.",
        "tags": ["Nordic Noir", "Audio Drama", "Mystery"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Reel Seven",
                "duration_min": 17,
                "content": (
                    "Salt spray rattled the lighthouse windows as Astrid threaded magnetic tape onto the vintage recorder. "
                    "Outside, the North Sea churned steel-gray against the basalt cliff.\n\n"
                    "The keeper's log from November 1974 listed only two people on the island. Yet as the reels spun, a third voice whispered clear instructions into the microphone—warning someone to guard the tide gate before midnight."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Echoes in the Foghorn",
                "duration_min": 16,
                "content": (
                    "Astrid checked the frequency spectrum on her field laptop. Beneath the static of the 1974 storm, a rhythmic Morse pulse repeated every forty seconds—identical to the harbor beacon still blinking outside."
                ),
            },
        ],
    },
    {
        "id": "kitchen-alchemist",
        "title": "Salt, Saffron & Sunlight",
        "author": "Elena Rossi",
        "genre": "fiction",
        "genre_label": "Fiction",
        "tier": "plus",
        "rating": 4.7,
        "reviews_count": 910,
        "year": 2024,
        "pages": 292,
        "audio_minutes": 370,
        "has_audiobook": True,
        "narrator": "Sofia Conti",
        "cover_gradient": "linear-gradient(135deg, #713f12 0%, #ca8a04 55%, #eab308 100%)",
        "cover_accent": "#fef9c3",
        "description": "Set in a sunlit coastal village in Sicily, three generations of women revive a seaside bakery using handwritten recipes and resilience.",
        "tags": ["Coastal", "Culinary Fiction", "Heartwarming"],
        "chapters": [
            {
                "number": 1,
                "title": "Chapter 1: Warm Brioche at Sunrise",
                "duration_min": 13,
                "content": (
                    "At five in the morning, the Mediterranean smelled of lemon blossom and sea salt. Lucia dusted flour across the marble counter and opened the wooden shutters toward the harbor.\n\n"
                    "Inside her grandmother's recipe notebook, margins held notes about harvests, friendships, and the secret to dough that rises even on stormy mornings."
                ),
            },
            {
                "number": 2,
                "title": "Chapter 2: Saffron Harvest",
                "duration_min": 14,
                "content": (
                    "By noon, fishermen and schoolteachers alike gathered beneath the striped awning for almond pastries and bitter espresso, trading stories that kept the tiny coastal town alive."
                ),
            },
        ],
    },
]


def get_book_cover_image(book_id):
    return f"/static/covers/{book_id}.svg"


for _b in BOOKS:
    _b["cover_image"] = get_book_cover_image(_b["id"])


def get_books(genre=None, query=None, tier=None, audio_only=False):
    """Filter books by genre, search query, tier, or audiobook availability."""
    results = BOOKS
    if genre and genre != "all":
        results = [b for b in results if b["genre"] == genre]
    if tier and tier != "all":
        results = [b for b in results if b["tier"] == tier]
    if audio_only:
        results = [b for b in results if b["has_audiobook"]]
    if query:
        q = query.strip().lower()
        results = [
            b
            for b in results
            if q in b["title"].lower()
            or q in b["author"].lower()
            or q in b["genre_label"].lower()
            or q in b["description"].lower()
            or any(q in tag.lower() for tag in b["tags"])
        ]
    return results


def get_book_by_id(book_id):
    """Return a single book dict or None."""
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None
