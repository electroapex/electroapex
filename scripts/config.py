import os

# GitHub Username
GITHUB_USERNAME = "electroapex"

# Repository Name
GITHUB_REPO = "electroapex"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Ensure folders exist
for folder in [ASSETS_DIR, IMAGES_DIR, FONTS_DIR]:
    os.makedirs(folder, exist_ok=True)

# GitHub Token for local running
GITHUB_TOKEN = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")

# Font Settings
FONT_FAMILY = "JetBrains Mono"
FONT_URL = "https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/JetBrainsMono/Ligatures/Regular/JetBrainsMonoNerdFont-Regular.ttf"
FONT_FILENAME = "JetBrainsMono-Regular.ttf"
FONT_PATH = os.path.join(FONTS_DIR, FONT_FILENAME)

# Theme Configuration (Linear/Vercel Inspired Ultra-Premium Theme)
THEME = {
    "dark": {
        "bg": "#000000",
        "bg_card": "#0F0F11",
        "border": "#262628",
        "text": "#EEEEEE",
        "text_muted": "#8A8F98",
        "accent": "#5E6AD2",
        "accent_green": "#4DA269",
        "accent_purple": "#8A63D2",
        "accent_orange": "#E36C2F",
        "sparkline": "#5E6AD2",
        "sparkline_fill": "rgba(94, 106, 210, 0.1)",
        "heatmap": ["#161b22", "#1d2539", "#2e3b5e", "#445588", "#5E6AD2"],
    },
    "light": {
        "bg": "#FFFFFF",
        "bg_card": "#F7F7F9",
        "border": "#EBEBEF",
        "text": "#111113",
        "text_muted": "#687076",
        "accent": "#5E6AD2",
        "accent_green": "#2F8E4B",
        "accent_purple": "#793EE8",
        "accent_orange": "#C54E00",
        "sparkline": "#5E6AD2",
        "sparkline_fill": "rgba(94, 106, 210, 0.1)",
        "heatmap": ["#ebedf0", "#d5daf2", "#b0bce6", "#8b9fd9", "#5E6AD2"],
    }
}

# ASCII Portrait Configuration
PORTRAIT = {
    "input_path": os.path.join(IMAGES_DIR, "portrait.jpg"),
    "backup_input_paths": [
        os.path.join(IMAGES_DIR, "portrait.png"),
        os.path.join(ASSETS_DIR, "M Huzaifa Hafeez.png")
    ],
    "output_path": os.path.join(ASSETS_DIR, "portrait.svg"),
    "width": 90,
    "height": 0,
    "char_aspect": 0.55,
    "density_ramp": " .`:-=+*cs#%@",
    "bilateral_d": 9,
    "bilateral_sigma_color": 75,
    "bilateral_sigma_space": 75,
    "clahe_clip_limit": 2.0,
    "clahe_tile_grid_size": (8, 8),
    "gamma": 1.2,
    "animation_speed": "0.08s",
}

# SVG File Outputs
STATS_SVG_PATH = os.path.join(ASSETS_DIR, "stats.svg")
STREAK_SVG_PATH = os.path.join(ASSETS_DIR, "streak.svg")
LANGUAGES_SVG_PATH = os.path.join(ASSETS_DIR, "languages.svg")
YEAR_SVG_PATH = os.path.join(ASSETS_DIR, "year.svg")
BACKGROUND_SVG_PATH = os.path.join(ASSETS_DIR, "background.svg")
TYPING_SVG_PATH = os.path.join(ASSETS_DIR, "typing.svg")
DIVIDER_SVG_PATH = os.path.join(ASSETS_DIR, "divider.svg")
PROJECTS_SVG_PATH = os.path.join(ASSETS_DIR, "projects.svg")

# Headings SVG Mapping
HEADINGS = {
    "about": os.path.join(ASSETS_DIR, "heading-about.svg"),
    "projects": os.path.join(ASSETS_DIR, "heading-projects.svg"),
    "contact": os.path.join(ASSETS_DIR, "heading-contact.svg")
}

# Terminal Typing Lines
TYPING_LINES = [
    "Hey 👋, I'm M. Huzaifa Hafeez",
    "💻 Full Stack Developer & Open Source Enthusiast...",
    "🚀 Exploring Cloud & DevOps..."
]

# Featured Projects Config
PROJECTS_LIST = [
    {
        "title": "Boiler Plate Generator",
        "description": "Stub accelerator & runtime generator program to speed up bootstrapping.",
        "stack": ["Python", "Cli", "Automation"],
        "status": "active",
        "stars": 18,
        "color": "#00D4AA",
        "logo_text": "BP"
    },
    {
        "title": "Accounting Application",
        "description": "Cross-platform accounting tool for general purposes and expense audits.",
        "stack": ["React", "Electron", "SQLite"],
        "status": "active",
        "stars": 12,
        "color": "#38B2AC",
        "logo_text": "AC"
    },
    {
        "title": "Image & Video Editor",
        "description": "Rock-solid free media editing application built on top of ffmpeg pipelines.",
        "stack": ["Node.js", "FFmpeg", "Electron"],
        "status": "stable",
        "stars": 14,
        "color": "#8250df",
        "logo_text": "IE"
    },
    {
        "title": "eCommerce Builder",
        "description": "Engine for launching independent, SEO-optimized merchant platforms.",
        "stack": ["React", "Express", "PostgreSQL"],
        "status": "stable",
        "stars": 20,
        "color": "#bc4c00",
        "logo_text": "EC"
    },
    {
        "title": "Job Aggregator",
        "description": "Unified platform aggregating developer vacancies with quick-apply workflows.",
        "stack": ["Next.js", "Django", "Postgres"],
        "status": "production",
        "stars": 22,
        "color": "#00599c",
        "logo_text": "JA"
    }
]
