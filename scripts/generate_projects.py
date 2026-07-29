import os
import textwrap
from scripts.config import PROJECTS_SVG_PATH, PROJECTS_LIST
from scripts.svg import SVGDocument
from scripts.utils import logger

def generate_projects_svg():
    """Generates the projects.svg file containing 3 premium animated project cards."""
    logger.info(f"Generating projects.svg -> {PROJECTS_SVG_PATH}")
    
    width = 775
    height = 200
    
    extra_styles = """
    .project-card-group {
        opacity: 0;
        animation: cardFadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        transform-box: fill-box;
        transform-origin: center;
        transition: transform 0.3s ease, filter 0.3s ease;
    }
    .project-card-group:hover {
        transform: scale(1.04);
        filter: drop-shadow(0 4px 12px var(--accent-glow));
        cursor: pointer;
    }
    .project-card-bg {
        fill: var(--bg-card);
        stroke: var(--border);
        stroke-width: 1px;
        rx: 8px;
        transition: stroke 0.3s ease;
    }
    .project-card-group:hover .project-card-bg {
        stroke: var(--accent);
    }
    .project-logo-circle {
        rx: 6px;
        ry: 6px;
    }
    .project-title {
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 14px;
        font-weight: 700;
        fill: var(--text);
    }
    .project-desc {
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 11px;
        fill: var(--text-muted);
    }
    .project-badge-bg {
        fill: rgba(255, 255, 255, 0.03);
        stroke: var(--border);
        stroke-width: 0.5px;
        rx: 3px;
    }
    .project-badge-text {
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 9px;
        fill: var(--text-muted);
    }
    .project-status-text {
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 9px;
        font-weight: 600;
    }
    
    @keyframes cardFadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    """
    
    # Collect all text chars for subsetting font
    chars_to_subset = (
        "AlgoUnionDjangoE-CommerceRustDSAProductionActiveStable"
        "InteractiveDSAlgorithmslearningplatformfeaturingcodoplaygroundslivetracing"
        "Multi-tenantmerchantstorefrontengineintegratingStripecheckoutandanalyticsboards"
        "High-performancestructuresandalgorithmslibrarybuiltusingidiomaticsafeRustcompilerconstraints"
        "0123456789.,:;+-_()[]/ "
    )
    
    svg = SVGDocument(width, height, subset_chars=chars_to_subset, extra_styles=extra_styles)
    
    # Glow gradient glow targets
    svg.add_def("""
    <linearGradient id="glow-card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
        <stop offset="100%" stop-color="var(--accent-purple)" stop-opacity="0" />
    </linearGradient>
    """)
    
    # Background card cover
    svg.add_element('<rect x="0.5" y="0.5" width="774" height="199" class="card" />')
    svg.add_element('<text x="25" y="32" class="title">Featured Projects</text>')
    
    # Cards layout parameters
    card_w = 230
    card_h = 135
    card_y = 48
    gap = 22
    start_x = 22
    
    for idx, proj in enumerate(PROJECTS_LIST):
        cx = start_x + idx * (card_w + gap)
        anim_delay = idx * 150
        
        # Wrapping description to lines
        wrapped_lines = textwrap.wrap(proj["description"], width=30)[:3]
        
        # Build SVG Elements for this card
        proj_elements = []
        
        # Glow overlay underneath
        proj_elements.append(f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" fill="url(#glow-card-grad)" rx="8" opacity="0.3" />')
        
        # Base Card rect
        proj_elements.append(f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" class="project-card-bg" />')
        
        # Card Logo
        proj_elements.append(f'<rect x="{cx + 15}" y="{card_y + 15}" width="24" height="24" class="project-logo-circle" fill="{proj["color"]}" opacity="0.8" />')
        proj_elements.append(f'<text x="{cx + 27}" y="{card_y + 31}" font-family="sans-serif" font-weight="bold" font-size="10" fill="#ffffff" text-anchor="middle">{proj["logo_text"]}</text>')
        
        # Title
        proj_elements.append(f'<text x="{cx + 48}" y="{card_y + 31}" class="project-title">{proj["title"]}</text>')
        
        # Description lines
        for l_idx, line in enumerate(wrapped_lines):
            dy = card_y + 54 + l_idx * 14
            proj_elements.append(f'<text x="{cx + 15}" y="{dy}" class="project-desc">{line}</text>')
            
        # Tech Badges (up to 3 horizontal)
        curr_badge_x = cx + 15
        badge_y = card_y + 105
        for tag in proj["stack"][:3]:
            tag_w = len(tag) * 6 + 10
            proj_elements.append(f'<rect x="{curr_badge_x}" y="{badge_y}" width="{tag_w}" height="14" class="project-badge-bg" />')
            proj_elements.append(f'<text x="{curr_badge_x + tag_w//2}" y="{badge_y + 10}" class="project-badge-text" text-anchor="middle">{tag}</text>')
            curr_badge_x += tag_w + 5
            
        # Status / Stars at right bottom
        status_x = cx + card_w - 75
        status_y = card_y + 24
        
        # Blinking status indicator light
        status_colors = {"production": "#3fb950", "active": "#bc8cff", "stable": "#58a6ff"}
        s_color = status_colors.get(proj["status"], "#bc8cff")
        proj_elements.append(f"""
        <circle cx="{status_x}" cy="{status_y - 3}" r="3" fill="{s_color}">
            <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
        </circle>
        <text x="{status_x + 8}" y="{status_y}" class="project-status-text" fill="{s_color}">{proj["status"].upper()}</text>
        """)
        
        # Star rating
        star_icon = "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
        star_x = cx + card_w - 45
        star_y = card_y + 115
        proj_elements.append(f"""
        <path d="{star_icon}" transform="translate({star_x}, {star_y - 10}) scale(0.4)" fill="#e3b341" />
        <text x="{star_x + 12}" y="{star_y}" font-family="sans-serif" font-size="10" font-weight="bold" fill="var(--text-muted)">{proj["stars"]}</text>
        """)
        
        # Wrap everything in a group with staggered animation
        svg.add_element(f"""
        <g class="project-card-group" style="animation-delay: {anim_delay}ms; --accent-glow: {proj['color']}33;">
            {"".join(proj_elements)}
        </g>
        """)
        
    svg.save(PROJECTS_SVG_PATH)

if __name__ == "__main__":
    generate_projects_svg()
