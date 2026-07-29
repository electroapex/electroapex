import os
import urllib.request
import base64
from scripts.config import ASSETS_DIR, HEADINGS, BACKGROUND_SVG_PATH, TYPING_SVG_PATH
from scripts.svg import SVGDocument
from scripts.utils import logger

def generate_heading_svg(text, filepath):
    """Generates a responsive heading SVG with a professional gradient underline."""
    logger.info(f"Generating heading SVG: '{text}' -> {filepath}")
    
    text_len = len(text)
    svg_width = max(200, text_len * 15 + 40)
    svg_height = 55
    
    extra_styles = """
    .heading-text {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 22px;
        font-weight: 700;
        fill: var(--text);
    }
    .heading-prefix {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 22px;
        font-weight: 700;
        fill: var(--accent);
    }
    .heading-line {
        stroke: url(#heading-grad);
        stroke-width: 3px;
        stroke-linecap: round;
        stroke-dasharray: 300;
        stroke-dashoffset: 300;
        animation: drawUnderline 1.2s ease-out forwards;
    }
    @keyframes drawUnderline {
        to { stroke-dashoffset: 0; }
    }
    """
    
    svg = SVGDocument(svg_width, svg_height, subset_chars=text + "#/ >", extra_styles=extra_styles)
    svg.add_def("""
    <linearGradient id="heading-grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="var(--accent)" stop-opacity="1" />
        <stop offset="40%" stop-color="var(--accent-purple)" stop-opacity="0.8" />
        <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
    </linearGradient>
    """)
    
    svg.add_element(f"""
    <text x="10" y="32">
        <tspan class="heading-prefix">## </tspan>
        <tspan class="heading-text">{text}</tspan>
    </text>
    <line x1="10" y1="42" x2="{svg_width - 10}" y2="42" class="heading-line" />
    """)
    
    svg.save(filepath)

def generate_typing_svg():
    """Generates a highly realistic, interactive infinite terminal simulator SVG."""
    logger.info(f"Generating infinite terminal typing SVG -> {TYPING_SVG_PATH}")
    width = 775
    height = 200
    
    extra_styles = """
    .terminal-body {
        fill: url(#card-bg-grad);
        stroke: url(#card-border-grad);
        stroke-width: 1.5px;
        rx: 12px;
    }
    .terminal-header {
        fill: #161b22;
        stroke: var(--border);
        stroke-width: 1px;
    }
    .terminal-dot {
        r: 6px;
    }
    .terminal-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        fill: var(--text);
    }
    .term-prompt { fill: var(--accent-green); font-weight: bold; }
    .term-user { fill: var(--accent); font-weight: bold; }
    .term-keyword { fill: var(--accent-purple); }
    .term-string { fill: var(--accent-orange); }
    .term-symbol { fill: var(--text-muted); }
    
    .spinner-arc {
        fill: none;
        stroke: var(--accent);
        stroke-width: 2px;
        stroke-linecap: round;
        transform-origin: 35px 82px;
    }
    .progress-bar-fill {
        fill: var(--accent-green);
        rx: 2px;
    }
    .progress-bar-track {
        fill: rgba(255, 255, 255, 0.05);
        rx: 2px;
    }
    .cursor-block {
        fill: var(--accent);
    }
    """
    
    charset = (
        "electroapex@github:~$ npx profile --runFetching stats from GraphQL..."
        "Loading metrics[============>] 100% Success! Loaded 14 assets, 42 repos, 752 commits."
        "Status: Active | Language Stack: HTML, CSS, JS, TS, React, Node, Python, PHP, SQL & More..."
        "Hey I'm M. Huzaifa HafeezFull Stack DeveloperOpen Source EnthusiastExploring Cloud DevOps"
        "0123456789.:;+-_()[]/|\\ "
    )
    
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    
    svg.add_element(f"""
    <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="terminal-body" />
    <path d="M 0.5,8 A 8,8 0 0,1 8,0.5 L {width - 8},0.5 A 8,8 0 0,1 {width - 0.5},8 L {width - 0.5},30 L 0.5,30 Z" class="terminal-header" />
    <circle cx="20" cy="15" class="terminal-dot" fill="#ff5f56" />
    <circle cx="40" cy="15" class="terminal-dot" fill="#ffbd2e" />
    <circle cx="60" cy="15" class="terminal-dot" fill="#27c93f" />
    <text x="{width // 2}" y="20" fill="var(--text-muted)" font-family="sans-serif" font-size="11" text-anchor="middle" font-weight="600">bash - electroapex@terminal</text>
    """)
    
    svg.add_element(f"""
    <text x="25" y="55" class="terminal-text">
        <tspan class="term-user">electroapex</tspan><tspan class="term-symbol">@</tspan><tspan class="term-prompt">github</tspan><tspan class="term-symbol">:~$ </tspan>
    </text>
    """)
    
    svg.add_def("""
    <clipPath id="term-clip-1">
        <rect x="180" y="40" height="22" width="0">
            <animate attributeName="width" values="0;135;135;135;0;0" keyTimes="0;0.12;0.78;0.88;0.96;1" dur="16s" repeatCount="indefinite" />
        </rect>
    </clipPath>
    """)
    
    svg.add_element(f"""
    <text x="180" y="55" class="terminal-text" clip-path="url(#term-clip-1)">
        <tspan class="term-keyword">npx</tspan> profile --run
    </text>
    """)
    
    svg.add_element(f"""
    <rect x="180" y="43" width="8" height="14" class="cursor-block">
        <animate attributeName="x" values="180;315;315;315;180;180" keyTimes="0;0.12;0.78;0.88;0.96;1" dur="16s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />
        <animate attributeName="visibility" values="visible;hidden;visible" keyTimes="0;0.17;1" dur="16s" repeatCount="indefinite" />
    </rect>
    """)
    
    svg.add_element(f"""
    <g>
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.17;0.18;0.76;0.78;1" dur="16s" repeatCount="indefinite" />
        <path d="M 35 77 A 5 5 0 1 1 34.9 77" class="spinner-arc" stroke-dasharray="10 5">
            <animateTransform attributeName="transform" type="rotate" from="0 35 82" to="360 35 82" dur="1s" repeatCount="indefinite" />
        </path>
        <text x="50" y="87" class="terminal-text" fill="var(--text-muted)">Fetching metrics from GraphQL...</text>
        <rect x="35" y="102" width="150" height="6" class="progress-bar-track" />
        <rect x="35" y="102" width="0" height="6" class="progress-bar-fill">
            <animate attributeName="width" values="0;0;150;150;0;0" keyTimes="0;0.22;0.36;0.76;0.78;1" dur="16s" repeatCount="indefinite" />
        </rect>
        <text x="195" y="108" class="terminal-text" fill="var(--accent-green)" font-weight="bold">
            <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.34;0.36;0.76;0.78" dur="16s" repeatCount="indefinite" />
            100%
        </text>
    </g>
    """)
    
    svg.add_element(f"""
    <g>
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.38;0.40;0.76;0.78;1" dur="16s" repeatCount="indefinite" />
        <text x="25" y="132" class="terminal-text" fill="var(--accent)">
            &gt; Success! Loaded 14 assets, 42 repos, 752 commits.
        </text>
        <text x="25" y="152" class="terminal-text" fill="var(--text-muted)">
            &gt; Status: <tspan class="term-prompt">Active</tspan> | Language Stack: <tspan class="term-keyword">HTML, CSS, JS, TS, React, Node, Python, PHP, SQL &amp; More...</tspan>
        </text>
    </g>
    """)
    
    svg.add_element(f"""
    <g>
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.44;0.46;0.76;0.78;1" dur="16s" repeatCount="indefinite" />
        <text x="25" y="177" class="terminal-text">
            <tspan class="term-user">electroapex</tspan><tspan class="term-symbol">@</tspan><tspan class="term-prompt">github</tspan><tspan class="term-symbol">:~$ </tspan>
        </text>
        <rect x="180" y="165" width="8" height="14" class="cursor-block">
            <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />
        </rect>
    </g>
    """)
    
    svg.save(TYPING_SVG_PATH)

def generate_background_svg():
    """Generates a professional developer header banner SVG."""
    logger.info(f"Generating background SVG -> {BACKGROUND_SVG_PATH}")
    width = 954
    height = 130
    
    extra_styles = """
    .banner-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 26px;
        font-weight: 800;
        fill: url(#text-grad);
        letter-spacing: 4px;
        opacity: 0;
        transform: translateY(-10px);
        animation: bannerFadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
    }
    .banner-subtitle {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 13px;
        fill: #8b949e;
        letter-spacing: 2px;
        opacity: 0;
        transform: translateY(-10px);
        animation: bannerFadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.5s forwards;
    }
    .banner-tag {
        opacity: 0;
        animation: bannerFadeInSimple 0.8s ease-out 0.8s forwards;
    }
    .banner-grid {
        stroke: rgba(255, 255, 255, 0.03);
        stroke-width: 1px;
    }
    @keyframes bannerFadeIn {
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes bannerFadeInSimple {
        to { opacity: 0.7; }
    }
    """
    
    svg = SVGDocument(width, height, subset_chars="Hey I'm M. Huzaifa HafeezFull Stack DeveloperOpen Source EnthusiastExploring Cloud DevOps", extra_styles=extra_styles)
    svg.add_def("""
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="60%" stop-color="#0d1117" />
        <stop offset="100%" stop-color="#1e152a" />
    </linearGradient>
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00D4AA" />
        <stop offset="50%" stop-color="#bc8cff" />
        <stop offset="100%" stop-color="#ff7b72" />
    </linearGradient>
    <pattern id="banner-grid-pat" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" class="banner-grid" />
    </pattern>
    """)
    
    svg.add_element(f"""
    <rect width="{width}" height="{height}" fill="url(#bg-grad)" />
    <rect width="{width}" height="{height}" fill="url(#banner-grid-pat)" />
    <circle cx="10%" cy="50%" r="90" fill="#00D4AA" opacity="0.08" filter="blur(20px)" />
    <circle cx="85%" cy="30%" r="80" fill="#bc8cff" opacity="0.08" filter="blur(20px)" />
    
    <g transform="translate(45, 0)">
        <text x="0" y="60" class="banner-title">M. HUIZAIFA HAFEEZ</text>
        <text x="0" y="88" class="banner-subtitle">Full Stack Developer &amp; Open Source Enthusiast</text>
        <text x="0" y="108" font-family="'JetBrains Mono'" font-size="10" fill="#00D4AA" class="banner-tag">&lt;developer status="active" /&gt;</text>
    </g>
    """)
    svg.save(BACKGROUND_SVG_PATH)


def get_icon_base64(tech_name):
    mapping = {
        "HTML5": "html", "CSS3": "css", "Node.js": "nodejs", 
        "Express.js": "express", "React Router": "react", 
        "Tailwind CSS": "tailwindcss", "C++": "cpp", "C#": "cs", 
        "Vue.js": "vue", "Adobe XD": "xd", "TanStack Query": "react"
    }
    clean_name = mapping.get(tech_name, tech_name.lower().replace(" ", "").replace(".", ""))
    url = f"https://skillicons.dev/icons?i={clean_name}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            b64 = base64.b64encode(response.read()).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    except Exception:
        return None

def generate_skills_svg():
    """Generates the ultimate clean, professional skills grid SVG."""
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating ultimate skills.svg -> {filepath}")
    
    # ── Layout constants ──────────────────────────────────────────
    PAD       = 18   # outer padding on all sides
    GAP       = 14   # gap between categories in same column
    PILL_H    = 32   # pill height
    PILL_R    = 7    # pill corner radius
    PILL_GAP  = 8    # horizontal gap between pills
    ROW_GAP   = 8    # vertical gap between pill rows
    LOGO_SZ   = 18   # logo image size
    COL_GAP   = 20   # gap between left and right column
    FONT_SIZE = 12   # pill text font size
    CHAR_W    = 7.0  # approximate character width in pixels

    # ── Category definitions ─────────────────────────────────────
    LEFT_CATS = [
        {
            "title": "Programming Languages",
            "accent": "#5E6AD2",
            "skills": [
                ("C","#a8b9cc"),("C++","#00599c"),("C#","#239120"),
                ("Python","#3776ab"),("PHP","#777bb4"),("Rust","#dea584"),
            ]
        },
        {
            "title": "Frontend Development",
            "accent": "#4DA269",
            "skills": [
                ("HTML5","#e34f26"),("CSS3","#1572b6"),("JavaScript","#f7df1e"),
                ("React","#61dafb"),("Next.js","#ffffff"),("Vue.js","#4fc08d"),
                ("jQuery","#0769ad"),("Redux","#764abc"),("Zustand","#5c5c5c"),
                ("React Router","#ca4245"),("TanStack Query","#ff4154"),
                ("Bootstrap","#7952b3"),("Tailwind CSS","#38b2ac"),
                ("Sass","#cc6699"),("Electron","#47848f"),
            ]
        },
        {
            "title": "Build &amp; Code Quality",
            "accent": "#E36C2F",
            "skills": [
                ("Vite","#646cff"),("ESLint","#4b32c3"),("Prettier","#f7b93e"),
            ]
        },
    ]
    RIGHT_CATS = [
        {
            "title": "Backend &amp; Databases",
            "accent": "#8A63D2",
            "skills": [
                ("Node.js","#339933"),("Express.js","#ffffff"),("Django","#092e20"),
                ("Laravel","#ff2d20"),("MySQL","#4479a1"),("PostgreSQL","#316192"),
                ("MongoDB","#4ea94b"),("SQLite","#07405e"),("MariaDB","#003545"),
            ]
        },
        {
            "title": "Mobile Development",
            "accent": "#E36C2F",
            "skills": [
                ("Kotlin","#7f52ff"),("Java","#ed8b00"),
            ]
        },
        {
            "title": "DevOps &amp; Infrastructure",
            "accent": "#4DA269",
            "skills": [
                ("Linux","#fcc624"),("Bash","#4eaa25"),
            ]
        },
        {
            "title": "Design Tools",
            "accent": "#5E6AD2",
            "skills": [
                ("Figma","#f24e1e"),("Illustrator","#ff9a00"),
                ("Photoshop","#31a8ff"),("Adobe XD","#ff61f6"),
            ]
        },
    ]

    # ── Pre-fetch all icons ───────────────────────────────────────
    all_skills = {}
    for cat in LEFT_CATS + RIGHT_CATS:
        for name, _ in cat["skills"]:
            if name not in all_skills:
                all_skills[name] = get_icon_base64(name)

    # ── Helper: compute how many pixel-rows a skill list needs ───
    def compute_cat_height(skills, col_w):
        usable = col_w - PAD * 2
        cx, rows = 0, 1
        for name, _ in skills:
            pw = max(len(name) * CHAR_W + 36, 60)
            if cx > 0 and cx + pw > usable:
                rows += 1
                cx = 0
            cx += pw + PILL_GAP
        # title(20) + underline_gap(10) + rows*(PILL_H+ROW_GAP) - last ROW_GAP + bottom_pad(10)
        return 20 + 10 + rows * (PILL_H + ROW_GAP) - ROW_GAP + 10

    # ── Compute column widths & heights ──────────────────────────
    TOTAL_W   = 760
    COL_W     = (TOTAL_W - PAD * 2 - COL_GAP) // 2   # ~351px each

    def col_total_h(cats):
        h = PAD
        for i, cat in enumerate(cats):
            h += compute_cat_height(cat["skills"], COL_W)
            if i < len(cats) - 1:
                h += GAP
        return h + PAD

    left_h  = col_total_h(LEFT_CATS)
    right_h = col_total_h(RIGHT_CATS)
    height  = max(left_h, right_h)

    # ── SVG styles ───────────────────────────────────────────────
    extra_styles = """
    .sk-cat-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 13px;
        font-weight: 700;
        fill: #e6edf3;
        letter-spacing: 0.3px;
    }
    .sk-pill {
        fill: #0F0F11;
        stroke: #262628;
        stroke-width: 1px;
    }
    .sk-pill-text {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 12px;
        font-weight: 500;
        fill: #c9d1d9;
    }
    .sk-sep {
        stroke: #262628;
        stroke-width: 1px;
    }
    """

    charset = (
        "FrontendBackendDatabasesMobileDevOpsProgrammingLanguagesBuildCodeQuality"
        "DesignToolsInfrastructureDevelopment"
        "HTML5CSS3JavaScriptReactNextjsReduxBootstrapTailwindCSSSassElectronZustandTanStackQueryjQueryVuejs"
        "NodejsExpressjsDjangoLaravelPHPPythonMySQLPostgreSQLMongoDBSQLiteMariaDBCRustViteESLintPrettier"
        "KotlinJavaGitDockerLinuxBashFirebaseHerokuPuppeteer"
        "FigmaIllustratorPhotoshopAdobeXD"
        "0123456789.,:;+-_&()[]/ "
    )

    svg = SVGDocument(TOTAL_W, height, subset_chars=charset, extra_styles=extra_styles)
    svg.add_element(f'<rect x="0" y="0" width="{TOTAL_W}" height="{height}" fill="transparent" />')

    # ── Vertical separator between columns ───────────────────────
    sep_x = PAD + COL_W + COL_GAP // 2
    svg.add_element(f'<line x1="{sep_x}" y1="{PAD}" x2="{sep_x}" y2="{height - PAD}" class="sk-sep" />')

    # ── Render a column of categories ────────────────────────────
    def render_column(cats, col_x, col_w):
        cy = PAD
        anim_idx = 0
        for cat in cats:
            accent = cat["accent"]
            title  = cat["title"]

            # Category title with accent dot
            svg.add_element(f'<circle cx="{col_x + 4}" cy="{cy + 10}" r="3" fill="{accent}" />')
            svg.add_element(f'<text x="{col_x + 14}" y="{cy + 15}" class="sk-cat-title">{title}</text>')

            # Underline accent
            svg.add_element(f'<line x1="{col_x}" y1="{cy + 22}" x2="{col_x + col_w}" y2="{cy + 22}" stroke="{accent}" stroke-width="0.5" opacity="0.3" />')

            px = col_x
            py = cy + 32
            usable = col_w

            for name, color in cat["skills"]:
                pw = max(len(name) * CHAR_W + 36, 60)
                if px > col_x and px + pw > col_x + usable:
                    px  = col_x
                    py += PILL_H + ROW_GAP

                delay_ms = anim_idx * 35
                b64  = all_skills.get(name)
                logo = (f'<image href="{b64}" x="{px+8}" y="{py+7}" width="{LOGO_SZ}" height="{LOGO_SZ}" />'
                        if b64 else
                        f'<circle cx="{px+17}" cy="{py+{PILL_H}//2}" r="5" fill="{color}" />')

                svg.add_element(f"""
                <g>
                    <rect x="{px}" y="{py}" width="{pw}" height="{PILL_H}" rx="{PILL_R}" class="sk-pill">
                        <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay_ms}ms" fill="freeze" />
                    </rect>
                    {logo}
                    <text x="{px+33}" y="{py+PILL_H//2+5}" class="sk-pill-text" opacity="0">
                        {name}
                        <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay_ms+80}ms" fill="freeze" />
                    </text>
                </g>""")

                px += pw + PILL_GAP
                anim_idx += 1

            # advance cy
            rows_used = 1
            test_px = col_x
            for name, _ in cat["skills"]:
                pw = max(len(name) * CHAR_W + 36, 60)
                if test_px > col_x and test_px + pw > col_x + usable:
                    rows_used += 1
                    test_px = col_x
                test_px += pw + PILL_GAP

            cy += 20 + 10 + rows_used * (PILL_H + ROW_GAP) + GAP

    render_column(LEFT_CATS,  PAD,            COL_W)
    render_column(RIGHT_CATS, PAD + COL_W + COL_GAP, COL_W)

    svg.save(filepath)


def generate_all_headings():
    """Generates all configured heading SVGs, background, typing, and skills cards."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    for name, path in HEADINGS.items():
        display_name = name.capitalize()
        if name == "about":
            display_name = "About Me"
        elif name == "projects":
            display_name = "Featured Projects"
        elif name == "contact":
            display_name = "Get in Touch"
        generate_heading_svg(display_name, path)
        
    generate_heading_svg("Professional Experience", os.path.join(ASSETS_DIR, "heading-experience.svg"))
    generate_heading_svg("Technical Skills", os.path.join(ASSETS_DIR, "heading-skills.svg"))
    
    generate_typing_svg()
    generate_background_svg()
    generate_skills_svg()

if __name__ == "__main__":
    generate_all_headings()
