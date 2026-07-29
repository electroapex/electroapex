import re

with open("scripts/generate_headings.py", "r") as f:
    content = f.read()

match = re.search(r'def generate_skills_svg\(\):.*?def generate_all_headings\(\):', content, re.DOTALL)
if not match:
    print("Could not find generate_skills_svg!")
    exit(1)

new_func = """def generate_skills_svg():
    \"\"\"Generates a clean, minimalist Vercel-style technical skills grid SVG card.\"\"\"
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating clean skills.svg -> {filepath}")
    
    width = 775
    height = 550
    
    extra_styles = \"\"\"
    .card-bg {
        fill: #0d1117;
    }
    .cat-box {
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 8px;
    }
    .skill-cat-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: #8b949e;
    }
    .pill {
        fill: rgba(255, 255, 255, 0.03);
        stroke: #30363d;
        stroke-width: 1px;
        rx: 16px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .pill-group {
        transform-box: fill-box;
        transform-origin: center;
        transition: transform 0.2s ease;
    }
    .pill-group:hover {
        transform: translateY(-2px);
    }
    .pill-group:hover .pill {
        stroke: var(--accent);
        fill: rgba(255, 255, 255, 0.1);
    }
    .pill-text {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 12px;
        font-weight: 500;
        fill: #c9d1d9;
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
    
    # Background
    svg.add_element(f'<rect x="0" y="0" width="{width}" height="{height}" class="card-bg" rx="12" stroke="#30363d" stroke-width="1" />')
    
    categories = [
        # LEFT COLUMN
        {
            "title": "Programming Languages",
            "x": 20, "y": 20, "w": 360, "h": 110,
            "skills": [
                ("C", "#a8b9cc"), ("C++", "#00599c"), ("C#", "#239120"),
                ("Python", "#3776ab"), ("PHP", "#777bb4"), ("Rust", "#dea584")
            ]
        },
        {
            "title": "Frontend",
            "x": 20, "y": 140, "w": 360, "h": 220,
            "skills": [
                ("HTML5", "#e34f26"), ("CSS3", "#1572b6"), 
                ("JavaScript", "#f7df1e"), ("React", "#20232a"), 
                ("Next.js", "#000000"), ("Vue.js", "#4fc08d"),
                ("jQuery", "#0769ad"), ("Redux", "#593d88"), 
                ("Zustand", "#443e38"), ("React Router", "#ca4245"), 
                ("TanStack Query", "#ff4154"), ("Bootstrap", "#563d7c"), 
                ("Tailwind CSS", "#38b2ac"), ("Sass", "#cc6699"), 
                ("Electron", "#47848f")
            ]
        },
        {
            "title": "Build Tools & Code Quality",
            "x": 20, "y": 370, "w": 360, "h": 110,
            "skills": [
                ("Vite", "#646cff"), ("Webpack", "#8dd6f9"),
                ("ESLint", "#4b32c3"), ("Prettier", "#f7b93e")
            ]
        },
        
        # RIGHT COLUMN
        {
            "title": "Backend & Databases",
            "x": 395, "y": 20, "w": 360, "h": 180,
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
            "x": 395, "y": 210, "w": 360, "h": 110,
            "skills": [
                ("Flutter", "#02569b"), ("Dart", "#0175c2"), 
                ("Android", "#3ddc84"), ("Kotlin", "#7f52ff"), 
                ("Java", "#ed8b00")
            ]
        },
        {
            "title": "DevOps & Tools",
            "x": 395, "y": 330, "w": 360, "h": 150,
            "skills": [
                ("Git", "#f05032"), ("Docker", "#2496ed"), 
                ("Linux", "#fcc624"), ("Bash", "#4eaa25"), 
                ("Firebase", "#ffca28"), ("Heroku", "#430098"), 
                ("Puppeteer", "#40b5a4")
            ]
        },
    ]
    
    # We add Design at the bottom to fill space if needed, or in right column
    categories.append({
        "title": "Design",
        "x": 395, "y": 490, "w": 360, "h": 40,
        "skills": [("Figma", "#f24e1e"), ("Photoshop", "#31a8ff")]
    })
    
    for cat in categories:
        svg.add_element(f'<rect x="{cat["x"]}" y="{cat["y"]}" width="{cat["w"]}" height="{cat["h"]}" class="cat-box" />')
        svg.add_element(f'<text x="{cat["x"] + 15}" y="{cat["y"] + 22}" class="skill-cat-title">{cat["title"]}</text>')
        
        curr_x = cat["x"] + 15
        curr_y = cat["y"] + 35
        line_height = 40
        
        for name, color in cat["skills"]:
            text_len = len(name)
            pill_w = text_len * 7.5 + 34
            
            if curr_x + pill_w > cat["x"] + cat["w"] - 15:
                curr_x = cat["x"] + 15
                curr_y += line_height
                
            b64_img = get_icon_base64(name)
            logo_svg = f'<image href="{b64_img}" x="{curr_x + 10}" y="{curr_y + 8}" width="16" height="16" />' if b64_img else f'<circle cx="{curr_x + 18}" cy="{curr_y + 16}" r="5" fill="{color}" />'
            
            svg.add_element(f\"\"\"
            <g class="pill-group">
                <rect x="{curr_x}" y="{curr_y}" width="{pill_w}" height="32" class="pill" />
                {logo_svg}
                <text x="{curr_x + 32}" y="{curr_y + 20}" class="pill-text">{name}</text>
            </g>
            \"\"\")
            
            curr_x += pill_w + 10
            
    svg.save(filepath)

def generate_all_headings():"""

new_content = content[:match.start()] + new_func + content[match.end()-len("\ndef generate_all_headings():"):]

with open("scripts/generate_headings.py", "w") as f:
    f.write(new_content)

print("Clean UI update successful!")
