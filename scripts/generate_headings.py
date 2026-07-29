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
    
    width = 775
    height = 480
    
    extra_styles = """
    .bg { fill: transparent; }
    .cat-title {
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 15px;
        font-weight: 700;
        fill: #e6edf3;
        letter-spacing: 0.5px;
    }
    .cat-line {
        stroke: var(--accent);
        stroke-width: 2px;
        stroke-linecap: round;
        opacity: 0.6;
    }
    .pill {
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 6px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .pill-group {
        transform-box: fill-box;
        transform-origin: center;
        transition: transform 0.2s ease;
    }
    .pill-group:hover {
        transform: translateY(-3px);
    }
    .pill-group:hover .pill {
        stroke: var(--accent);
        fill: #21262d;
    }
    .pill-text {
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: #c9d1d9;
    }
    """
    
    charset = (
        "FrontendBackendDatabasesMobileCross-PlatformDevOpsToolsDesignProgrammingLanguagesBuildCodeQuality"
        "HTML5CSS3JavaScriptReactNext.jsReduxBootstrapTailwindCSSSassElectronZustandTanStackQueryjQueryVue.js"
        "Node.jsExpress.jsDjangoLaravelRuby RailsPHPPythonMySQLPostgreSQLMongoDBSQLiteMariaDBC++C#RustViteESLintPrettier"
        "KotlinJavaGitDockerLinuxBashFirebaseHerokuPuppeteer"
        "FigmaIllustratorPhotoshopAdobeXD"
        "0123456789.,:;+-_()[]/ "
    )
    
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    
    svg.add_element(f'<rect x="0" y="0" width="{width}" height="{height}" class="bg" />')
    
    categories = [
        # LEFT COLUMN
        {
            "title": "Programming Languages",
            "x": 10, "y": 20, "w": 360, "h": 90,
            "skills": [
                ("C", "#a8b9cc"), ("C++", "#00599c"), ("C#", "#239120"),
                ("Python", "#3776ab"), ("PHP", "#777bb4"), ("Rust", "#dea584")
            ]
        },
        {
            "title": "Frontend Development",
            "x": 10, "y": 140, "w": 360, "h": 180,
            "skills": [
                ("HTML5", "#e34f26"), ("CSS3", "#1572b6"), 
                ("JavaScript", "#f7df1e"), ("React", "#20232a"), 
                ("Next.js", "#ffffff"), ("Vue.js", "#4fc08d"),
                ("jQuery", "#0769ad"), ("Redux", "#593d88"), 
                ("Zustand", "#443e38"), ("React Router", "#ca4245"), 
                ("TanStack Query", "#ff4154"), ("Bootstrap", "#563d7c"), 
                ("Tailwind CSS", "#38b2ac"), ("Sass", "#cc6699"), 
                ("Electron", "#47848f")
            ]
        },
        {
            "title": "Build & Code Quality",
            "x": 10, "y": 350, "w": 360, "h": 90,
            "skills": [
                ("Vite", "#646cff"), ("ESLint", "#4b32c3"), ("Prettier", "#f7b93e")
            ]
        },
        
        # RIGHT COLUMN
        {
            "title": "Backend & Databases",
            "x": 400, "y": 20, "w": 360, "h": 130,
            "skills": [
                ("Node.js", "#339933"), ("Express.js", "#ffffff"), 
                ("Django", "#092e20"), ("Laravel", "#ff2d20"), 
                ("MySQL", "#4479a1"), ("PostgreSQL", "#316192"), 
                ("MongoDB", "#4ea94b"), ("SQLite", "#07405e"), 
                ("MariaDB", "#003545")
            ]
        },
        {
            "title": "Mobile Development",
            "x": 400, "y": 180, "w": 360, "h": 60,
            "skills": [
                ("Kotlin", "#7f52ff"), ("Java", "#ed8b00")
            ]
        },
        {
            "title": "DevOps & Infrastructure",
            "x": 400, "y": 270, "w": 360, "h": 60,
            "skills": [
                ("Linux", "#fcc624"), ("Bash", "#4eaa25")
            ]
        },
        {
            "title": "Design Tools",
            "x": 400, "y": 360, "w": 360, "h": 90,
            "skills": [
                ("Figma", "#f24e1e"), ("Illustrator", "#ff9a00"), 
                ("Photoshop", "#31a8ff"), ("Adobe XD", "#ff61f6")
            ]
        }
    ]
    
    for cat in categories:
        # Title and underline
        svg.add_element(f'<text x="{cat["x"]}" y="{cat["y"] + 15}" class="cat-title">{cat["title"]}</text>')
        svg.add_element(f'<line x1="{cat["x"]}" y1="{cat["y"] + 25}" x2="{cat["x"] + 30}" y2="{cat["y"] + 25}" class="cat-line" />')
        
        curr_x = cat["x"]
        curr_y = cat["y"] + 40
        line_height = 42
        
        for name, color in cat["skills"]:
            text_len = len(name)
            pill_w = text_len * 7.5 + 36
            
            if curr_x + pill_w > cat["x"] + cat["w"]:
                curr_x = cat["x"]
                curr_y += line_height
                
            b64_img = get_icon_base64(name)
            logo_svg = f'<image href="{b64_img}" x="{curr_x + 10}" y="{curr_y + 8}" width="18" height="18" />' if b64_img else f'<circle cx="{curr_x + 19}" cy="{curr_y + 17}" r="6" fill="{color}" />'
            
            svg.add_element(f"""
            <g class="pill-group">
                <rect x="{curr_x}" y="{curr_y}" width="{pill_w}" height="34" class="pill" />
                {logo_svg}
                <text x="{curr_x + 36}" y="{curr_y + 22}" class="pill-text">{name}</text>
            </g>
            """)
            
            curr_x += pill_w + 12
            
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
