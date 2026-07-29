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
    """Generates a beautiful self-contained technical skills grid SVG card with 3D Holographic effects."""
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating 3D skills.svg -> {filepath}")
    
    width = 775
    height = 650
    
    extra_styles = """
    .skill-cat-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 700;
        fill: var(--accent);
        filter: drop-shadow(0px 0px 4px var(--accent-purple));
    }
    
    /* 3D Glass Badge Styles */
    .badge-group {
        transform-box: fill-box;
        transform-origin: center;
        transition: transform 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
    }
    
    .badge-group:hover .badge-glass {
        fill: rgba(255, 255, 255, 0.15);
        stroke: var(--accent);
    }
    
    .badge-group:hover .badge-glow-bg {
        opacity: 0.8;
    }
    
    .badge-group:hover {
        transform: scale(1.15) translateY(-5px);
    }
    
    .badge-text {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 11px;
        font-weight: 700;
        fill: var(--text);
    }
    
    .cat-border {
        stroke: rgba(255,255,255,0.1);
        stroke-width: 1px;
        fill: rgba(0,0,0,0.2);
        rx: 12px;
    }
    
    /* Connections */
    .tech-connection {
        fill: none;
        stroke: url(#connection-grad);
        stroke-width: 1.5px;
        stroke-dasharray: 4 8;
        animation: flowLight 2s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes flowLight {
        to { stroke-dashoffset: -24; }
    }
    
    @keyframes float1 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-4px) rotate(1deg); } }
    @keyframes float2 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-3px) rotate(-1deg); } }
    @keyframes float3 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-5px) rotate(0.5deg); } }
    
    /* Holographic Background */
    .holo-grid {
        fill: url(#gridPattern);
        opacity: 0.15;
    }
    
    .scanner-beam {
        fill: url(#scannerGrad);
        animation: scan 8s ease-in-out infinite alternate;
        opacity: 0.3;
    }
    
    @keyframes scan {
        0% { transform: translateY(-100px); }
        100% { transform: translateY(800px); }
    }
    """
    
    charset = (
        "FrontendBackendDatabasesMobileCross-PlatformDevOpsToolsDesignProgrammingLanguagesBuildCodeQuality"
        "HTML5CSS3JavaScriptReactNext.jsReduxBootstrapTailwindCSSSassElectronZustandTanStackQueryjQueryVue.js"
        "Node.jsExpress.jsDjangoFlaskLaravelRuby RailsPHPPythonMySQLPostgreSQLMongoDBSQLiteMariaDBC++C#RustViteWebpackESLintPrettier"
        "FlutterDartAndroidKotlinJavaGitDockerLinuxBashFirebaseHerokuPuppeteer"
        "FigmaIllustratorPhotoshopAdobeXD"
        "0123456789.,:;+-_()[]/ "
    )
    
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    
    # --- DEFS: 3D Filters, Gradients, and Patterns ---
    svg.add_def("""
    <linearGradient id="badge-glass-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="rgba(255,255,255,0.08)" />
        <stop offset="100%" stop-color="rgba(255,255,255,0.02)" />
    </linearGradient>
    <linearGradient id="badge-edge-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="rgba(255,255,255,0.4)" />
        <stop offset="100%" stop-color="rgba(255,255,255,0.05)" />
    </linearGradient>
    <filter id="badge-shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000" flood-opacity="0.8"/>
    </filter>
    <linearGradient id="connection-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="var(--accent)" />
        <stop offset="100%" stop-color="var(--accent-purple)" />
    </linearGradient>
    <pattern id="gridPattern" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="var(--accent)" stroke-width="0.5" stroke-dasharray="2 2" opacity="0.3"/>
    </pattern>
    <linearGradient id="scannerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="transparent" />
        <stop offset="50%" stop-color="var(--accent)" stop-opacity="0.5" />
        <stop offset="100%" stop-color="transparent" />
    </linearGradient>
    """)
    
    # --- BACKGROUND ELEMENTS ---
    svg.add_element(f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" class="card" />')
    svg.add_element(f'<rect x="0" y="0" width="{width}" height="{height}" class="holo-grid" />')
    
    # Ambient glowing orbs in background
    svg.add_element('<circle cx="150" cy="150" r="100" fill="var(--accent-purple)" opacity="0.05" filter="blur(40px)" />')
    svg.add_element('<circle cx="600" cy="450" r="120" fill="var(--accent)" opacity="0.05" filter="blur(50px)" />')
    
    # Scanner beam
    svg.add_element(f'<rect x="0" y="0" width="{width}" height="60" class="scanner-beam" />')
    
    # --- CATEGORIES AND SKILLS ---
    categories = [
        {
            "title": "Programming Languages",
            "x": 20, "y": 20, "w": 355, "h": 90,
            "skills": [
                ("C", "#a8b9cc"), ("C++", "#00599c"), ("C#", "#239120"),
                ("Python", "#3776ab"), ("PHP", "#777bb4"), ("Rust", "#dea584")
            ]
        },
        {
            "title": "Frontend",
            "x": 20, "y": 125, "w": 355, "h": 165,
            "skills": [
                ("HTML5", "#e34f26"), ("CSS3", "#1572b6"), 
                ("JavaScript", "#f7df1e"), ("React", "#20232a"), 
                ("Next.js", "#000000"), ("Vue.js", "#4fc08d"),
                ("jQuery", "#0769ad"),
                ("Redux", "#593d88"), ("Zustand", "#443e38"),
                ("React Router", "#ca4245"), ("TanStack Query", "#ff4154"),
                ("Bootstrap", "#563d7c"), ("Tailwind CSS", "#38b2ac"), 
                ("Sass", "#cc6699"), ("Electron", "#47848f")
            ]
        },
        {
            "title": "Build Tools &amp; Code Quality",
            "x": 20, "y": 305, "w": 355, "h": 85,
            "skills": [
                ("Vite", "#646cff"), ("Webpack", "#8dd6f9"),
                ("ESLint", "#4b32c3"), ("Prettier", "#f7b93e")
            ]
        },
        {
            "title": "Backend &amp; Databases",
            "x": 395, "y": 20, "w": 355, "h": 165,
            "skills": [
                ("Node.js", "#339933"), ("Express.js", "#000000"), 
                ("Django", "#092e20"), ("Flask", "#000000"), 
                ("Laravel", "#ff2d20"), 
                ("MySQL", "#4479a1"), ("PostgreSQL", "#316192"), 
                ("MongoDB", "#4ea94b"), ("SQLite", "#07405e"), 
                ("MariaDB", "#003545")
            ]
        },
        {
            "title": "Mobile &amp; Cross-Platform",
            "x": 395, "y": 200, "w": 355, "h": 85,
            "skills": [
                ("Flutter", "#02569b"), ("Dart", "#0175c2"), 
                ("Android", "#3ddc84"), ("Kotlin", "#7f52ff"), 
                ("Java", "#ed8b00")
            ]
        },
        {
            "title": "DevOps &amp; Tools",
            "x": 395, "y": 300, "w": 355, "h": 125,
            "skills": [
                ("Git", "#f05032"), ("Docker", "#2496ed"), 
                ("Linux", "#fcc624"), ("Bash", "#4eaa25"), 
                ("Firebase", "#ffca28"), ("Heroku", "#430098"), 
                ("Puppeteer", "#40b5a4")
            ]
        },
        {
            "title": "Design",
            "x": 395, "y": 440, "w": 355, "h": 90,
            "skills": [
                ("Figma", "#f24e1e"), ("Illustrator", "#ff9a00"), 
                ("Photoshop", "#31a8ff"), ("Adobe XD", "#ff61f6")
            ]
        }
    ]
    
    # Store calculated positions for connections
    badge_positions = {}
    
    badge_index = 0
    # First Pass: Calculate coordinates and draw boxes
    rendered_badges = []
    
    for cat in categories:
        svg.add_element(f'<rect x="{cat["x"]}" y="{cat["y"]}" width="{cat["w"]}" height="{cat["h"]}" class="cat-border" />')
        svg.add_element(f'<text x="{cat["x"] + 15}" y="{cat["y"] + 24}" class="skill-cat-title">{cat["title"]}</text>')
        
        curr_x = cat["x"] + 15
        curr_y = cat["y"] + 42
        line_height = 30
        
        for name, color in cat["skills"]:
            text_len = len(name)
            badge_w = text_len * 7 + 26
            
            if curr_x + badge_w > cat["x"] + cat["w"] - 15:
                curr_x = cat["x"] + 15
                curr_y += line_height
                
            cx = curr_x + badge_w/2
            cy = curr_y + 11
            badge_positions[name] = (cx, cy)
            
            anim_class = f"float{(badge_index % 3) + 1}"
            anim_delay = (badge_index * 0.15)
            badge_index += 1
            
            b64_img = get_icon_base64(name)
            logo_svg = f'<image href="{b64_img}" x="{curr_x + 4}" y="{curr_y + 4}" width="14" height="14" />' if b64_img else f'{logo_svg}'
            
            # The holographic 3D card
            rendered_badges.append(f"""
            <g class="badge-group" style="animation: {anim_class} 4s ease-in-out infinite {anim_delay}s;">
                <!-- Outer Glow -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="{color}" opacity="0" filter="blur(8px)" class="badge-glow-bg" transition="opacity 0.3s" />
                
                <!-- Main Glass Pane with shadow -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="url(#badge-glass-grad)" filter="url(#badge-shadow)" />
                
                <!-- Specular Highlight Top Border -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="none" stroke="url(#badge-edge-grad)" stroke-width="1.5" class="badge-glass" />
                
                <!-- Color Dot / Logo Indicator -->
                {logo_svg}
                
                <!-- Text -->
                <text x="{curr_x + 20}" y="{curr_y + 15}" class="badge-text">{name}</text>
            </g>
            """)
            
            curr_x += badge_w + 10
            
    # Draw connections (lines) behind the badges
    connections = [
        ("React", "Next.js"), ("React", "Redux"), ("React", "Zustand"), 
        ("React", "React Router"), ("React", "TanStack Query"), 
        ("Vite", "React"), ("Webpack", "React"), ("PHP", "Laravel")
    ]
    
    for start, end in connections:
        if start in badge_positions and end in badge_positions:
            x1, y1 = badge_positions[start]
            x2, y2 = badge_positions[end]
            # Draw curved bezier path
            cx1, cy1 = x1, y1 + (y2 - y1)/2
            cx2, cy2 = x2, y1 + (y2 - y1)/2
            svg.add_element(f'<path d="M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}" class="tech-connection" />')
            
    # Add rendered badges on top
    for b in rendered_badges:
        svg.add_element(b)
        
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
