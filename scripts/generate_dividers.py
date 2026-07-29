import os
from scripts.config import DIVIDER_SVG_PATH
from scripts.svg import SVGDocument
from scripts.utils import logger

def generate_divider_svg():
    """Generates the divider.svg file containing an animated particle stream divider."""
    logger.info(f"Generating divider.svg -> {DIVIDER_SVG_PATH}")
    
    width = 775
    height = 30
    
    extra_styles = """
    .divider-line {
        fill: none;
        stroke: url(#div-grad);
        stroke-width: 1.5px;
        stroke-linecap: round;
        opacity: 0.8;
    }
    .divider-pulse {
        fill: var(--accent);
        filter: url(#pulse-glow);
    }
    .divider-star {
        fill: var(--accent-purple);
        opacity: 0.6;
    }
    """
    
    svg = SVGDocument(width, height, embed_font=False, extra_styles=extra_styles)
    
    # Custom gradients and filters
    svg.add_def("""
    <linearGradient id="div-grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="var(--border)" stop-opacity="0.2" />
        <stop offset="30%" stop-color="var(--accent)" stop-opacity="0.8" />
        <stop offset="50%" stop-color="var(--accent-purple)" stop-opacity="1" />
        <stop offset="70%" stop-color="var(--accent)" stop-opacity="0.8" />
        <stop offset="100%" stop-color="var(--border)" stop-opacity="0.2" />
    </linearGradient>
    
    <filter id="pulse-glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
    """)
    
    # Base Divider Line
    svg.add_element('<line x1="20" y1="15" x2="755" y2="15" class="divider-line" />')
    
    # Glowing sliding light beam
    svg.add_element("""
    <circle cx="20" cy="15" r="4" class="divider-pulse">
        <animate attributeName="cx" values="20; 755; 20" dur="8s" repeatCount="indefinite" />
        <animate attributeName="r" values="3; 5; 3" dur="2s" repeatCount="indefinite" />
    </circle>
    """)
    
    # Secondary sliding light beam (purple, offset delay)
    svg.add_element("""
    <circle cx="755" cy="15" r="3" fill="var(--accent-purple)" filter="url(#pulse-glow)">
        <animate attributeName="cx" values="755; 20; 755" dur="10s" repeatCount="indefinite" />
    </circle>
    """)
    
    # Floating small particles along the divider line
    particles = [
        {"x": 100, "delay": "0s"},
        {"x": 250, "delay": "0.5s"},
        {"x": 400, "delay": "1s"},
        {"x": 550, "delay": "1.5s"},
        {"x": 680, "delay": "2s"}
    ]
    for idx, p in enumerate(particles):
        svg.add_element(f"""
        <circle cx="{p['x']}" cy="15" r="1.5" class="divider-star">
            <animate attributeName="opacity" values="0.2;0.9;0.2" dur="2.5s" begin="{p['delay']}" repeatCount="indefinite" />
            <animate attributeName="r" values="1; 2; 1" dur="2.5s" begin="{p['delay']}" repeatCount="indefinite" />
        </circle>
        """)
        
    svg.save(DIVIDER_SVG_PATH)

if __name__ == "__main__":
    generate_divider_svg()
