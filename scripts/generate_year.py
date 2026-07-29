import os
from datetime import datetime
from scripts.config import YEAR_SVG_PATH, THEME
from scripts.github_graphql import fetch_graphql_data
from scripts.svg import SVGDocument
from scripts.utils import logger

def get_contribution_level(count):
    """Maps contribution count to a level from 0 to 4."""
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 8:
        return 3
    else:
        return 4

def generate_year_svg(data):
    """Generates the year.svg contribution heatmap file."""
    logger.info(f"Generating year.svg -> {YEAR_SVG_PATH}")
    
    col_coll = data.get("contributionsCollection", {})
    calendar = col_coll.get("contributionCalendar", {})
    weeks = calendar.get("weeks", [])
    total_conts = calendar.get("totalContributions", 0)
    
    cell_size    = 13
    cell_spacing  = 3
    left_padding  = 38
    top_padding   = 42
    right_padding = 22
    
    # Tight width/height from actual data — no artificial minimum
    num_weeks = len(weeks) if weeks else 53
    graph_w   = left_padding + num_weeks * (cell_size + cell_spacing)
    graph_h   = top_padding  + 7 * (cell_size + cell_spacing)
    width     = graph_w + right_padding
    height    = graph_h + 50  # space for legend + timestamp
    
    dark = THEME["dark"]
    light = THEME["light"]
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    extra_styles = f"""
    :root {{
        --l0: {dark["heatmap"][0]};
        --l1: {dark["heatmap"][1]};
        --l2: {dark["heatmap"][2]};
        --l3: {dark["heatmap"][3]};
        --l4: {dark["heatmap"][4]};
    }}
    @media (prefers-color-scheme: light) {{
        :root {{
            --l0: {light["heatmap"][0]};
            --l1: {light["heatmap"][1]};
            --l2: {light["heatmap"][2]};
            --l3: {light["heatmap"][3]};
            --l4: {light["heatmap"][4]};
        }}
    }}
    .day-cell {{
        width: {cell_size}px;
        height: {cell_size}px;
        rx: 2px;
        ry: 2px;
        opacity: 0;
        animation: fadeInSquare 0.4s ease-out forwards;
        transition: transform 0.15s ease, filter 0.15s ease, fill 0.15s ease;
        transform-box: fill-box;
        transform-origin: center;
    }}
    .day-cell:hover {{
        transform: scale(1.4);
        filter: brightness(1.2) drop-shadow(0 0 2px var(--accent));
        cursor: pointer;
    }}
    .level-0 {{ fill: var(--l0); }}
    .level-1 {{ fill: var(--l1); }}
    .level-2 {{ fill: var(--l2); }}
    .level-3 {{ fill: var(--l3); }}
    .level-4 {{ fill: var(--l4); }}
    
    .current-day-pulse {{
        stroke: var(--accent);
        stroke-width: 1px;
        animation: pulseToday 1.8s ease-in-out infinite;
    }}
    
    .label-month {{
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 10px;
        fill: var(--text-muted);
    }}
    .label-day {{
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 9px;
        fill: var(--text-muted);
    }}
    
    @keyframes fadeInSquare {{
        to {{ opacity: 1; }}
    }}
    @keyframes pulseToday {{
        0%, 100% {{ stroke-opacity: 0.4; stroke-width: 1px; }}
        50% {{ stroke-opacity: 1.0; stroke-width: 2.2px; filter: drop-shadow(0 0 2px var(--accent)); }}
    }}
    """
    
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[]"
    svg = SVGDocument(width, height, subset_chars=charset, extra_styles=extra_styles)
    
    svg.add_element(f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" class="card" />')
    
    svg.add_element(f"""
    <text x="20" y="25" class="title">Yearly Contributions</text>
    <text x="180" y="24" class="label" font-size="11">{total_conts:,} contributions in the past year</text>
    """)
    
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for name, row_idx in day_labels:
        y = top_padding + row_idx * (cell_size + cell_spacing) + 9
        svg.add_element(f'<text x="12" y="{y}" class="label-day">{name}</text>')
        
    prev_month = None
    month_labels = []
    
    for col_idx, week in enumerate(weeks):
        days = week.get("contributionDays", [])
        
        if days:
            first_day_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
            month_name = first_day_date.strftime("%b")
            
            if month_name != prev_month:
                x_pos = left_padding + col_idx * (cell_size + cell_spacing)
                if not month_labels or (x_pos - month_labels[-1][1]) > 35:
                    month_labels.append((month_name, x_pos))
                    prev_month = month_name
                    
        for day in days:
            row_idx = day["weekday"]
            count = day["contributionCount"]
            level = get_contribution_level(count)
            is_today = (day["date"] == today_str)
            
            x = left_padding + col_idx * (cell_size + cell_spacing)
            y = top_padding + row_idx * (cell_size + cell_spacing)
            
            anim_delay = col_idx * 12 + row_idx * 4
            
            pulse_class = " current-day-pulse" if is_today else ""
            
            svg.add_element(
                f'<rect x="{x}" y="{y}" class="day-cell level-{level}{pulse_class}" '
                f'style="animation-delay: {anim_delay}ms;" />'
            )
            
    for month_name, x_pos in month_labels:
        svg.add_element(f'<text x="{x_pos}" y="35" class="label-month">{month_name}</text>')
        
    legend_x = width - 140
    legend_y = height - 24
    svg.add_element(f"""
    <text x="{legend_x - 32}" y="{legend_y + 9}" class="label-day" font-size="10">Less</text>
    <rect x="{legend_x}" y="{legend_y}" width="{cell_size}" height="{cell_size}" class="day-cell level-0" style="animation-delay: 0ms;" />
    <rect x="{legend_x + 13}" y="{legend_y}" width="{cell_size}" height="{cell_size}" class="day-cell level-1" style="animation-delay: 0ms;" />
    <rect x="{legend_x + 26}" y="{legend_y}" width="{cell_size}" height="{cell_size}" class="day-cell level-2" style="animation-delay: 0ms;" />
    <rect x="{legend_x + 39}" y="{legend_y}" width="{cell_size}" height="{cell_size}" class="day-cell level-3" style="animation-delay: 0ms;" />
    <rect x="{legend_x + 52}" y="{legend_y}" width="{cell_size}" height="{cell_size}" class="day-cell level-4" style="animation-delay: 0ms;" />
    <text x="{legend_x + 68}" y="{legend_y + 9}" class="label-day" font-size="10">More</text>
    """)
    
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    svg.add_element(f"""
    <text x="20" y="{legend_y + 9}" class="label-day" font-size="9" fill="var(--text-muted)">
        Last updated: {update_date} UTC
    </text>
    """)
    
    svg.save(YEAR_SVG_PATH)

def main():
    try:
        data = fetch_graphql_data()
        generate_year_svg(data)
        logger.info("Yearly contribution heatmap SVG updated successfully.")
    except Exception as e:
        logger.error(f"Error generating yearly heatmap SVG: {e}")
        raise e

if __name__ == "__main__":
    main()
