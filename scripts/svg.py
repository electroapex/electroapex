from scripts.config import THEME, FONT_FAMILY
from scripts.fonts import get_font_style

class SVGDocument:
    def __init__(self, width, height, embed_font=True, subset_chars=None, extra_styles=""):
        self.width = width
        self.height = height
        self.embed_font = embed_font
        self.subset_chars = subset_chars
        self.extra_styles = extra_styles
        self.elements = []
        self.defs = []
        # Add 3D Vision OS style glassmorphic gradients
        self.defs.append("""
    <linearGradient id="card-bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="var(--bg-card)" stop-opacity="0.95" />
        <stop offset="100%" stop-color="var(--bg-card)" stop-opacity="0.6" />
    </linearGradient>
    <linearGradient id="card-border-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="rgba(255,255,255,0.2)" />
        <stop offset="100%" stop-color="rgba(255,255,255,0.02)" />
    </linearGradient>
        """)

    def add_element(self, element_str):
        self.elements.append(element_str)

    def add_def(self, def_str):
        self.defs.append(def_str)

    def generate_theme_styles(self):
        """Generates CSS variable overrides for dark and light modes."""
        dark = THEME["dark"]
        light = THEME["light"]

        styles = f"""
:root {{
    --bg: {dark["bg"]};
    --bg-card: {dark["bg_card"]};
    --border: {dark["border"]};
    --text: {dark["text"]};
    --text-muted: {dark["text_muted"]};
    --accent: {dark["accent"]};
    --accent-green: {dark["accent_green"]};
    --accent-purple: {dark["accent_purple"]};
    --accent-orange: {dark["accent_orange"]};
    --sparkline: {dark["sparkline"]};
    --sparkline-fill: {dark["sparkline_fill"]};
}}

/* Light mode override */
@media (prefers-color-scheme: light) {{
    :root {{
        --bg: {light["bg"]};
        --bg-card: {light["bg_card"]};
        --border: {light["border"]};
        --text: {light["text"]};
        --text-muted: {light["text_muted"]};
        --accent: {light["accent"]};
        --accent-green: {light["accent_green"]};
        --accent-purple: {light["accent_purple"]};
        --accent-orange: {light["accent_orange"]};
        --sparkline: {light["sparkline"]};
        --sparkline-fill: {light["sparkline_fill"]};
    }}
}}

body {{
    font-family: '{FONT_FAMILY}', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--text);
    margin: 0;
}}

.card {{
    fill: url(#card-bg-grad);
    stroke: url(#card-border-grad);
    stroke-width: 1.5px;
    rx: 12px;
    filter: url(#shadow3d);
}}

.title {{
    font-size: 16px;
    font-weight: 600;
    fill: var(--accent);
}}

.label {{
    font-size: 13px;
    fill: var(--text-muted);
}}

.value {{
    font-size: 13px;
    font-weight: 600;
    fill: var(--text);
}}
"""
        if self.embed_font:
            font_face = get_font_style(self.subset_chars)
            styles = font_face + "\n" + styles

        if self.extra_styles:
            styles += "\n" + self.extra_styles

        return f"<style>\n{styles}\n</style>"

    def render(self):
        """Assembles and returns the full SVG document string."""
        style_block = self.generate_theme_styles()
        
        defs_block = ""
        if self.defs:
            defs_block = "<defs>\n" + "\n".join(self.defs) + "\n</defs>\n"

        elements_block = "\n".join(self.elements)

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="100%" style="border-radius: 8px;">
{defs_block}
{style_block}
{elements_block}
</svg>"""
        return svg_content

    def save(self, filepath):
        """Saves the SVG document to the specified filepath."""
        content = self.render()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
