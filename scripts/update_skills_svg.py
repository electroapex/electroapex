import re

with open("scripts/generate_headings.py", "r") as f:
    content = f.read()

# We need to find the definition of generate_skills_svg() and replace it.
# The function ends just before 'def generate_all_headings():'

match = re.search(r'def generate_skills_svg\(\):.*?def generate_all_headings\(\):', content, re.DOTALL)
if not match:
    print("Could not find generate_skills_svg!")
    exit(1)

new_func = """def generate_skills_svg():
    \"\"\"Generates a beautiful self-contained technical skills grid SVG card with 3D Holographic effects.\"\"\"
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating 3D skills.svg -> {filepath}")
    
    width = 775
    height = 650
    
    extra_styles = \"\"\"
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
    \"\"\"
    
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
    svg.add_def(\"\"\"
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
    \"\"\")
    
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
            "title": "Build Tools & Code Quality",
            "x": 20, "y": 305, "w": 355, "h": 85,
            "skills": [
                ("Vite", "#646cff"), ("Webpack", "#8dd6f9"),
                ("ESLint", "#4b32c3"), ("Prettier", "#f7b93e")
            ]
        },
        {
            "title": "Backend & Databases",
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
            "title": "Mobile & Cross-Platform",
            "x": 395, "y": 200, "w": 355, "h": 85,
            "skills": [
                ("Flutter", "#02569b"), ("Dart", "#0175c2"), 
                ("Android", "#3ddc84"), ("Kotlin", "#7f52ff"), 
                ("Java", "#ed8b00")
            ]
        },
        {
            "title": "DevOps & Tools",
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
            
            # The holographic 3D card
            rendered_badges.append(f\"\"\"
            <g class="badge-group" style="animation: {anim_class} 4s ease-in-out infinite {anim_delay}s;">
                <!-- Outer Glow -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="{color}" opacity="0" filter="blur(8px)" class="badge-glow-bg" transition="opacity 0.3s" />
                
                <!-- Main Glass Pane with shadow -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="url(#badge-glass-grad)" filter="url(#badge-shadow)" />
                
                <!-- Specular Highlight Top Border -->
                <rect x="{curr_x}" y="{curr_y}" width="{badge_w}" height="22" rx="6" fill="none" stroke="url(#badge-edge-grad)" stroke-width="1.5" class="badge-glass" />
                
                <!-- Color Dot / Logo Indicator -->
                <circle cx="{curr_x + 11}" cy="{curr_y + 11}" r="4" fill="{color}" filter="drop-shadow(0 0 3px {color})" />
                
                <!-- Text -->
                <text x="{curr_x + 20}" y="{curr_y + 15}" class="badge-text">{name}</text>
            </g>
            \"\"\")
            
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

def generate_all_headings():"""

new_content = content[:match.start()] + new_func + content[match.end()-len("\ndef generate_all_headings():"):]

with open("scripts/generate_headings.py", "w") as f:
    f.write(new_content)

print("Update successful!")
