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

# Theme Configuration
THEME = {
    "dark": {
        "bg": "#0d1117",
        "bg_card": "#161b22",
        "border": "#30363d",
        "text": "#c9d1d9",
        "text_muted": "#8b949e",
        "accent": "#58a6ff",
        "accent_green": "#3fb950",
        "accent_purple": "#bc8cff",
        "accent_orange": "#f0883e",
        "sparkline": "#58a6ff",
        "sparkline_fill": "rgba(88, 166, 255, 0.05)",
        "heatmap": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    },
    "light": {
        "bg": "#ffffff",
        "bg_card": "#f6f8fa",
        "border": "#d0d7de",
        "text": "#24292f",
        "text_muted": "#57606a",
        "accent": "#0969da",
        "accent_green": "#1a7f37",
        "accent_purple": "#8250df",
        "accent_orange": "#bc4c00",
        "sparkline": "#0969da",
        "sparkline_fill": "rgba(9, 105, 218, 0.05)",
        "heatmap": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
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
    "width": 90,               # Width in characters
    "height": 0,                # Auto-calculate
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
    "⚡ Passionate about full stack web development and problem solving...",
    "💻 React, TypeScript, PHP, Python, C++, SQL, Rust...",
    "🚀 Turning complex ideas into elegant, production-ready code."
]

# Featured Projects Config
PROJECTS_LIST = [
    {
        "title": "Algo Union",
        "description": "Interactive DS & Algorithms learning platform featuring code playgrounds and live tracing.",
        "stack": ["TypeScript", "React", "Express", "MongoDB"],
        "status": "production",
        "stars": 24,
        "color": "#3178c6",
        "logo_text": "AU"
    },
    {
        "title": "Django E-Commerce",
        "description": "Multi-tenant merchant storefront engine integrating Stripe checkout and analytics boards.",
        "stack": ["Python", "Django", "PostgreSQL", "Tailwind"],
        "status": "active",
        "stars": 15,
        "color": "#092e20",
        "logo_text": "DE"
    },
    {
        "title": "Rust DSA",
        "description": "High-performance structures and algorithms library built using idiomatic, safe Rust compiler constraints.",
        "stack": ["Rust", "Cargo", "Github Actions"],
        "status": "stable",
        "stars": 12,
        "color": "#dee5e6",
        "logo_text": "RD"
    }
]
