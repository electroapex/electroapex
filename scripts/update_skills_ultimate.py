import re

with open("scripts/generate_headings.py", "r") as f:
    content = f.read()

match = re.search(r'def generate_skills_svg\(\):.*?def generate_all_headings\(\):', content, re.DOTALL)
if not match:
    print("Could not find generate_skills_svg!")
    exit(1)

new_func = """def generate_skills_svg():
    \"\"\"Generates the ultimate clean, professional skills grid SVG.\"\"\"
    filepath = os.path.join(ASSETS_DIR, "skills.svg")
    logger.info(f"Generating ultimate skills.svg -> {filepath}")
    
    width = 775
    height = 480
    
    extra_styles = \"\"\"
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
    \"\"\"
    
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
            
            svg.add_element(f\"\"\"
            <g class="pill-group">
                <rect x="{curr_x}" y="{curr_y}" width="{pill_w}" height="34" class="pill" />
                {logo_svg}
                <text x="{curr_x + 36}" y="{curr_y + 22}" class="pill-text">{name}</text>
            </g>
            \"\"\")
            
            curr_x += pill_w + 12
            
    svg.save(filepath)

def generate_all_headings():"""

new_content = content[:match.start()] + new_func + content[match.end()-len("\ndef generate_all_headings():"):]

with open("scripts/generate_headings.py", "w") as f:
    f.write(new_content)

print("Ultimate Clean UI update successful!")
