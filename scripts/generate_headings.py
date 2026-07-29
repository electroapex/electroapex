import os
from scripts.config import ASSETS_DIR, HEADINGS, TYPING_LINES, BACKGROUND_SVG_PATH, TYPING_SVG_PATH
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
    """Generates a terminal typing animation SVG."""
    logger.info(f"Generating terminal typing SVG -> {TYPING_SVG_PATH}")
    width = 775
    height = 140
    
    charset = "".join(TYPING_LINES) + "⚡💻🚀1234567890:-. _+,"
    
    extra_styles = """
    .terminal-body {
        fill: var(--bg-card);
        stroke: var(--border);
        stroke-width: 1px;
        rx: 8px;
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
    .terminal-cursor {
        fill: var(--accent);
    }
    """
    
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    svg.add_element(f"""
    <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="terminal-body" />
    <path d="M 0.5,8 A 8,8 0 0,1 8,0.5 L {width - 8},0.5 A 8,8 0 0,1 {width - 0.5},8 L {width - 0.5},30 L 0.5,30 Z" class="terminal-header" />
    <circle cx="20" cy="15" class="terminal-dot" fill="#ff5f56" />
    <circle cx="40" cy="15" class="terminal-dot" fill="#ffbd2e" />
    <circle cx="60" cy="15" class="terminal-dot" fill="#27c93f" />
    <text x="{width // 2}" y="20" fill="var(--text-muted)" font-family="sans-serif" font-size="11" text-anchor="middle" font-weight="600">bash - electroapex@terminal</text>
    """)

    char_width = 7.8
    y_starts = [58, 83, 108]
    durations = [2.0, 2.0, 2.0]
    delays = [0.2, 2.4, 4.6]
    
    for i, line in enumerate(TYPING_LINES):
        length = len(line)
        line_w = round(length * char_width, 1)
        clip_id = f"clip-line-{i}"
        
        svg.add_def(f"""
        <clipPath id="{clip_id}">
            <rect x="25" y="{y_starts[i] - 14}" height="22" width="0">
                <animate attributeName="width" from="0" to="{line_w}" dur="{durations[i]}s" begin="{delays[i]}s" fill="freeze" />
            </rect>
        </clipPath>
        """)
        
        svg.add_element(f"""
        <text x="25" y="{y_starts[i]}" class="terminal-text" clip-path="url(#{clip_id})">{line}</text>
        """)
        
        cursor_delay = delays[i]
        cursor_dur = durations[i]
        cursor_end = cursor_delay + cursor_dur
        
        if i < len(TYPING_LINES) - 1:
            next_delay = delays[i+1]
            vis_attr = f"""
            <animate attributeName="visibility" from="hidden" to="visible" begin="{cursor_delay}s" dur="{next_delay - cursor_delay}s" fill="freeze" />
            <animate attributeName="visibility" to="hidden" begin="{next_delay}s" fill="freeze" />
            """
        else:
            vis_attr = f"""
            <animate attributeName="visibility" from="hidden" to="visible" begin="{cursor_delay}s" fill="freeze" />
            """
            
        svg.add_element(f"""
        <rect x="25" y="{y_starts[i] - 12}" width="8" height="14" class="terminal-cursor">
            {vis_attr}
            <animate attributeName="x" from="25" to="{25 + line_w}" begin="{cursor_delay}s" dur="{cursor_dur}s" fill="freeze" />
            <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" begin="{cursor_end}s" />
        </rect>
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
    
    svg = SVGDocument(width, height, subset_chars="M. HUZAIFA HAFEEZFull Stack Engineer & Problem Solver", extra_styles=extra_styles)
    svg.add_def("""
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="60%" stop-color="#0d1117" />
        <stop offset="100%" stop-color="#1e152a" />
    </linearGradient>
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#58a6ff" />
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
    
    <!-- Abstract graphical glows -->
    <circle cx="10%" cy="50%" r="90" fill="#58a6ff" opacity="0.08" filter="blur(20px)" />
    <circle cx="85%" cy="30%" r="80" fill="#bc8cff" opacity="0.08" filter="blur(20px)" />
    
    <!-- Text contents -->
    <g transform="translate(45, 0)">
        <text x="0" y="60" class="banner-title">M. HUIZAIFA HAFEEZ</text>
        <text x="0" y="88" class="banner-subtitle">Full Stack Engineer &amp; Problem Solver</text>
        
        <!-- Decorative tags -->
        <text x="0" y="108" font-family="'JetBrains Mono'" font-size="10" fill="#3fb950" class="banner-tag">&lt;developer status="active" /&gt;</text>
    </g>
    """)
    svg.save(BACKGROUND_SVG_PATH)

def generate_skills_svg():
    """Generates a beautiful self-contained technical skills grid SVG card."""
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating skills.svg -> {filepath}")
    
    width = 775
    height = 240
    
    extra_styles = """
    .skill-cat-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 700;
        fill: var(--accent);
    }
    .badge-group {
        opacity: 0;
        animation: fadeInBadge 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        transform-box: fill-box;
        transform-origin: center;
        transition: transform 0.2s ease, filter 0.2s ease;
    }
    .badge-group:hover {
        transform: scale(1.08);
        filter: drop-shadow(0 0 3px var(--accent)) brightness(1.1);
        cursor: pointer;
    }
    .badge-rect {
        fill: var(--bg-card);
        stroke: var(--border);
        stroke-width: 1px;
        rx: 4px;
        transition: stroke 0.2s ease, fill 0.2s ease;
    }
    .badge-group:hover .badge-rect {
        stroke: var(--accent);
        fill: rgba(88, 166, 255, 0.05);
    }
    .badge-text {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 11px;
        font-weight: 600;
        fill: var(--text);
    }
    .cat-border {
        stroke: var(--border);
        stroke-width: 0.5px;
        fill: none;
        rx: 6px;
    }
    @keyframes fadeInBadge {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    """
    
    # Compile text characters for font subsetting
    charset = (
        "LanguagesFrameworksDatabasesTools"
        "JavaScriptTypeScriptPythonJavaC++C#RustPHPKotlinHTML5CSS3SassSQLBash"
        "ReactVue.jsNode.jsExpressDjangoLaravelElectronTailwindCSSBootstrapRedux"
        "PostgreSQLMySQLMariaDBMongoDBFirebase"
        "GitGitHubVSCodeIntelliJIDEAFigmaPostmanLinuxVim"
        "0123456789.,:;+-_()[]/ "
    )
    
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    svg.add_element('<rect x="0.5" y="0.5" width="774" height="239" class="card" />')
    
    # Categories definition with coordinate logic and items
    categories = [
        {
            "title": "Languages",
            "x": 20, "y": 20, "w": 360, "h": 90,
            "skills": [
                ("JavaScript", "#f7df1e"), ("TypeScript", "#3178c6"), 
                ("Python", "#3776ab"), ("C++", "#00599c"), 
                ("Rust", "#dee5e6"), ("PHP", "#777bb4"), 
                ("SQL", "#4479a1"), ("Bash", "#4eaa25")
            ]
        },
        {
            "title": "Frameworks & Libraries",
            "x": 395, "y": 20, "w": 360, "h": 90,
            "skills": [
                ("React", "#61dafb"), ("Vue.js", "#4fc08d"), 
                ("Node.js", "#339933"), ("Django", "#092e20"), 
                ("Laravel", "#ff2d20"), ("Tailwind CSS", "#06b6d4"),
                ("Redux", "#764abc")
            ]
        },
        {
            "title": "Databases & Storage",
            "x": 20, "y": 130, "w": 360, "h": 90,
            "skills": [
                ("PostgreSQL", "#4169e1"), ("MySQL", "#4479a1"), 
                ("MongoDB", "#47a248"), ("Firebase", "#ffca28"),
                ("MariaDB", "#003545")
            ]
        },
        {
            "title": "Tools & Developer OS",
            "x": 395, "y": 130, "w": 360, "h": 90,
            "skills": [
                ("Git", "#f05032"), ("GitHub", "#c9d1d9"), 
                ("VS Code", "#007acc"), ("Figma", "#f24e1e"), 
                ("Postman", "#ff6c37"), ("Linux", "#fcc624"),
                ("Vim", "#019733")
            ]
        }
    ]
    
    badge_index = 0
    for cat in categories:
        # Category block border
        svg.add_element(f'<rect x="{cat["x"]}" y="{cat["y"]}" width="{cat["w"]}" height="{cat["h"]}" class="cat-border" />')
        # Category Title
        svg.add_element(f'<text x="{cat["x"] + 15}" y="{cat["y"] + 24}" class="skill-cat-title">{cat["title"]}</text>')
        
        curr_x = cat["x"] + 15
        curr_y = cat["y"] + 38
        line_height = 24
        
        for name, color in cat["skills"]:
            text_len = len(name)
            badge_w = text_len * 7 + 26
            
            if curr_x + badge_w > cat["x"] + cat["w"] - 15:
                curr_x = cat["x"] + 15
                curr_y += line_height
                
            # Staggered animation delay
            anim_delay = badge_index * 25
            badge_index += 1
            
            # Wrap in group for animations
            svg.add_element(f"""
            <g class="badge-group" style="animation-delay: {anim_delay}ms;">
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="18" class="badge-rect" />
                <circle cx="{curr_x + 9}" cy="{curr_y + 9}" r="4" fill="{color}" />
                <text x="{curr_x + 19}" y="{curr_y + 13}" class="badge-text">{name}</text>
            </g>
            """)
            
            curr_x += badge_w + 8
            
    svg.save(filepath)

def generate_all_headings():
    """Generates all configured heading SVGs, background, typing, and skills cards."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Write default headings
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
