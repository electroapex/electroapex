import os
from datetime import datetime
from scripts.config import STATS_SVG_PATH, STREAK_SVG_PATH, LANGUAGES_SVG_PATH
from scripts.github_graphql import fetch_graphql_data, calculate_streak, aggregate_languages
from scripts.svg import SVGDocument
from scripts.utils import logger

def make_animated_counter(value, x, y, id_prefix, font_size=13, line_height=14, char_w=7.8, alignment="left"):
    """
    Generates a clip-pathed slot-machine rolling counter for a number using SMIL.
    Returns (defs_list, elements_list, total_width)
    """
    val_str = f"{value:,}" if isinstance(value, int) else str(value)
    defs = []
    elems = []
    
    # Calculate offset if aligned right or center
    total_w = sum((char_w * 0.5 if c in (",", ".") else char_w) for c in val_str)
    
    start_x = x
    if alignment == "right":
        start_x = x - total_w
    elif alignment == "center":
        start_x = x - total_w / 2
        
    curr_x = start_x
    for idx, char in enumerate(val_str):
        if char.isdigit():
            digit = int(char)
            clip_id = f"clip-{id_prefix}-{idx}"
            
            defs.append(f"""
            <clipPath id="{clip_id}">
                <rect x="{curr_x}" y="{y - font_size + 1}" width="{char_w + 0.5}" height="{line_height}" />
            </clipPath>
            """)
            
            tspans = "\n".join(f'<tspan x="{curr_x}" dy="{0 if d == 0 else line_height}">{d}</tspan>' for d in range(10))
            
            elems.append(f"""
            <g clip-path="url(#{clip_id})">
                <text x="{curr_x}" y="{y}" class="value">
                    {tspans}
                    <animateTransform 
                        attributeName="transform" 
                        type="translate" 
                        from="0, 0" 
                        to="0, {-digit * line_height}" 
                        dur="2.2s" 
                        begin="0.2s" 
                        fill="freeze" 
                        keyTimes="0; 1" 
                        keySplines="0.25 0.1 0.25 1" 
                        calcMode="spline" 
                    />
                </text>
            </g>
            """)
            curr_x += char_w
        else:
            w_c = char_w * 0.5 if char in (",", ".") else char_w
            elems.append(f'<text x="{curr_x}" y="{y}" class="value">{char}</text>')
            curr_x += w_c
            
    return defs, elems, total_w

def make_sparkline(weeks_data, x_min=240, x_max=420, y_min=50, y_max=120):
    """
    Computes a smooth cubic bezier SVG path representing the contributions of the last 12 weeks.
    Returns path for the line, path for the filled area, and the last point's coordinates (for a pulse dot).
    """
    last_12_weeks = weeks_data[-12:]
    totals = []
    for week in last_12_weeks:
        week_total = sum(day.get("contributionCount", 0) for day in week.get("contributionDays", []))
        totals.append(week_total)
        
    n_points = len(totals)
    if n_points < 2:
        return "", "", (0, 0)
        
    val_min = min(totals)
    val_max = max(totals)
    val_range = val_max - val_min if val_max > val_min else 1
    
    points = []
    dx = (x_max - x_min) / (n_points - 1)
    for i, val in enumerate(totals):
        x = x_min + i * dx
        y = y_max - ((val - val_min) / val_range) * (y_max - y_min)
        points.append((x, y))
        
    line_path = f"M {points[0][0]},{points[0][1]} "
    for i in range(len(points) - 1):
        p0 = points[i]
        p1 = points[i+1]
        cp1_x = p0[0] + (p1[0] - p0[0]) / 2.0
        cp1_y = p0[1]
        cp2_x = p0[0] + (p1[0] - p0[0]) / 2.0
        cp2_y = p1[1]
        line_path += f"C {cp1_x},{cp1_y} {cp2_x},{cp2_y} {p1[0]},{p1[1]} "
        
    area_path = f"{line_path} L {points[-1][0]},{y_max} L {points[0][0]},{y_max} Z"
    
    return line_path, area_path, points[-1]

def generate_stats_svg(data):
    """Generates the stats.svg file."""
    logger.info(f"Generating stats.svg -> {STATS_SVG_PATH}")
    
    repos = data.get("repositories", {})
    total_repos = repos.get("totalCount", 0)
    total_stars = sum(node.get("stargazerCount", 0) for node in repos.get("nodes", []))
    
    col_coll = data.get("contributionsCollection", {})
    commits_year = col_coll.get("totalCommitContributions", 0)
    prs = data.get("pullRequests", {}).get("totalCount", 0)
    followers = data.get("followers", {}).get("totalCount", 0)
    following = data.get("following", {}).get("totalCount", 0)
    
    weeks = col_coll.get("contributionCalendar", {}).get("weeks", [])
    line_path, area_path, last_pt = make_sparkline(weeks)
    
    extra_styles = """
    .sparkline-line {
        fill: none;
        stroke: var(--accent);
        stroke-width: 2.5px;
        stroke-linecap: round;
        stroke-linejoin: round;
        filter: drop-shadow(0 0 2px var(--accent));
        stroke-dasharray: 600;
        stroke-dashoffset: 600;
        animation: drawSparkline 2s cubic-bezier(0.4, 0, 0.2, 1) 0.5s forwards;
    }
    .sparkline-area {
        fill: var(--sparkline-fill);
        stroke: none;
        opacity: 0;
        animation: fadeInElement 1s ease-out 1.8s forwards;
    }
    .sparkline-pulse {
        fill: var(--accent);
        stroke: var(--bg-card);
        stroke-width: 1.5px;
        opacity: 0;
        animation: fadeInElement 0.5s ease-out 2.2s forwards;
    }
    .sparkline-grid {
        stroke: var(--border);
        stroke-dasharray: 2 4;
        stroke-width: 1px;
    }
    .stat-icon {
        fill: var(--accent);
    }
    .stat-row {
        opacity: 0;
        animation: slideInLeft 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
    }
    
    @keyframes drawSparkline {
        to { stroke-dashoffset: 0; }
    }
    @keyframes fadeInElement {
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-15px); }
        to { opacity: 1; transform: translateX(0); }
    }
    """
    
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[]"
    svg = SVGDocument(450, 200, subset_chars=charset, extra_styles=extra_styles)
    
    # Base Cards
    svg.add_element('<rect x="0.5" y="0.5" width="449" height="199" class="card" />')
    svg.add_element('<text x="25" y="35" class="title">Developer Statistics</text>')
    
    stats_y_start = 65
    dy = 24
    
    stats_items = [
        ("Commits (Past Year)", commits_year, "commits", "M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.579.688.481C19.137 20.162 22 16.418 22 12c0-5.523-4.477-10-10-10z"),
        ("Repositories", total_repos, "repos", "M4 4h16v16H4zm2 2v12h12V6z"),
        ("Total Stars", total_stars, "stars", "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"),
        ("Pull Requests", prs, "prs", "M11 18H3v-2h8zm0-4H3v-2h8zm0-4H3V8h8zm10 0v10l-4-4-4 4V10zm-4-6l4 4H13z"),
        ("Followers", followers, "followers", "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z")
    ]
    
    for idx, (label, val, prefix, path) in enumerate(stats_items):
        y = stats_y_start + idx * dy
        anim_delay = idx * 100
        
        # Build rolling counter elements
        c_defs, c_elems, _ = make_animated_counter(val, 180, y, f"stat-{prefix}", font_size=13, line_height=14, char_w=7.8)
        for d_def in c_defs:
            svg.add_def(d_def)
            
        svg.add_element(f"""
        <g class="stat-row" style="animation-delay: {anim_delay}ms;">
            <path d="{path}" transform="translate(25, {y-12}) scale(0.6)" class="stat-icon" />
            <text x="45" y="{y}" class="label">{label}</text>
            {"".join(c_elems)}
        </g>
        """)
        
    svg.add_element("""
    <text x="240" y="35" class="label" font-size="11">Weekly Activity</text>
    <text x="240" y="47" class="label" font-size="9" fill="var(--text-muted)">Past 12 Weeks</text>
    
    <line x1="240" y1="50" x2="420" y2="50" class="sparkline-grid" />
    <line x1="240" y1="85" x2="420" y2="85" class="sparkline-grid" />
    <line x1="240" y1="120" x2="420" y2="120" class="sparkline-grid" />
    """)
    
    if line_path:
        svg.add_element(f'<path d="{area_path}" class="sparkline-area" />')
        svg.add_element(f'<path d="{line_path}" class="sparkline-line" />')
        svg.add_element(f"""
        <circle cx="{last_pt[0]}" cy="{last_pt[1]}" r="4" class="sparkline-pulse">
            <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
        </circle>
        """)
        
    # Legend
    svg.add_element(f"""
    <rect x="240" y="145" width="180" height="35" fill="none" stroke="var(--border)" stroke-width="0.5" rx="4" />
    <text x="250" y="166" class="label" font-size="10">Followers: <tspan class="value" font-size="10">{followers}</tspan></text>
    <text x="340" y="166" class="label" font-size="10">Following: <tspan class="value" font-size="10">{following}</tspan></text>
    """)

    svg.save(STATS_SVG_PATH)

def generate_streak_svg(data):
    """Generates the streak.svg file."""
    logger.info(f"Generating streak.svg -> {STREAK_SVG_PATH}")
    
    calendar_weeks = data.get("contributionsCollection", {}).get("contributionCalendar", {}).get("weeks", [])
    streak_data = calculate_streak(calendar_weeks)
    
    current_streak = streak_data["current_streak"]
    current_range = ""
    if current_streak > 0:
        start_dt = datetime.strptime(streak_data["current_start"], "%Y-%m-%d")
        end_dt = datetime.strptime(streak_data["current_end"], "%Y-%m-%d")
        current_range = f"{start_dt.strftime('%b %d')} - {end_dt.strftime('%b %d')}"
        
    longest_streak = streak_data["longest_streak"]
    longest_range = ""
    if longest_streak > 0:
        start_dt = datetime.strptime(streak_data["longest_start"], "%Y-%m-%d")
        end_dt = datetime.strptime(streak_data["longest_end"], "%Y-%m-%d")
        longest_range = f"{start_dt.strftime('%b %d')} - {end_dt.strftime('%b %d')}"
        
    total_conts = data.get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", 0)
    today_conts = streak_data["today_contributions"]
    
    extra_styles = """
    .streak-num {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 30px;
        font-weight: 800;
        fill: var(--accent);
    }
    .streak-title {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 11px;
        font-weight: 600;
        fill: var(--text-muted);
    }
    .streak-range {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 9px;
        fill: var(--text-muted);
    }
    .divider {
        stroke: var(--border);
        stroke-width: 1px;
    }
    .streak-item {
        opacity: 0;
        animation: slideInUp 0.6s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
    }
    .streak-icon-flame {
        fill: var(--accent-orange);
        transform-box: fill-box;
        transform-origin: center;
        animation: flickerFlame 1.8s ease-in-out infinite;
    }
    .streak-icon-trophy {
        fill: var(--accent-green);
        transform-box: fill-box;
        transform-origin: center;
        animation: scaleTrophy 2s ease-in-out infinite;
    }
    .streak-icon-star {
        fill: var(--accent-purple);
        transform-box: fill-box;
        transform-origin: center;
        animation: rotateStar 3s linear infinite;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes flickerFlame {
        0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 1px var(--accent-orange)); }
        50% { transform: scale(1.08) rotate(-3deg); filter: drop-shadow(0 0 4px var(--accent-orange)); }
    }
    @keyframes scaleTrophy {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.06) translateY(-1px); }
    }
    @keyframes rotateStar {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    """
    
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[]"
    svg = SVGDocument(450, 165, subset_chars=charset, extra_styles=extra_styles)
    
    svg.add_element('<rect x="0.5" y="0.5" width="449" height="164" class="card" />')
    
    flame_path = "M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10c0-1.85-.5-3.58-1.38-5.07-.63 1.25-1.5 2.37-2.62 3.25C17.25 9.25 16 8 16 8s-.75.75-1.25 1.75C13.5 8 12.5 6 12.5 6s-.5.75-1 1.75C10.5 6.5 9 5 9 5s-.5 1-1.25 2.5C7.25 6 6 4.5 6 4.5S5.5 6 5.5 7.5c0 3 2.5 5.5 5.5 5.5 1 0 1.5-.5 2-.75.25.5.5 1.25.5 2.25 0 2.5-2 4.5-4.5 4.5-.5 0-.75.25-.75.5 0 .5.75.5 1.5.5 3.5 0 6.5-2.5 6.5-6 0-1.5-.75-2.75-1.5-3.75z"
    trophy_path = "M19 2H5v3H2v3c0 2.2 1.8 4 4 4h1.2c.4 1.5 1.5 2.7 3 3.1V18H7v2h10v-2h-3.2v-2.9c1.5-.4 2.6-1.6 3-3.1H18c2.2 0 4-1.8 4-4V5h-3V2zM4 8V6h2v3c0 .6-.4 1-1 1s-1-.4-1-1zm14 1V6h2v3c0 .6-.4 1-1 1s-1-.4-1-1z"
    star_icon = "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
    
    # 1. Current Streak Rolling Counter setup
    c_defs, c_elems, _ = make_animated_counter(current_streak, 65, 80, "streak-current", font_size=30, line_height=32, char_w=18.0)
    for d_def in c_defs: svg.add_def(d_def)
    
    # 2. Longest Streak Rolling Counter setup
    l_defs, l_elems, _ = make_animated_counter(longest_streak, 60, 80, "streak-longest", font_size=30, line_height=32, char_w=18.0)
    for d_def in l_defs: svg.add_def(d_def)
    
    # 3. Total contributions Rolling Counter setup
    t_defs, t_elems, _ = make_animated_counter(total_conts, 55, 80, "streak-total", font_size=30, line_height=32, char_w=18.0)
    for d_def in t_defs: svg.add_def(d_def)
    
    # Col 1: Current Streak
    svg.add_element(f"""
    <g class="streak-item" style="animation-delay: 0ms;" transform="translate(10, 0)">
        <path d="{flame_path}" transform="translate(30, 20) scale(0.9)" class="streak-icon-flame" />
        <text x="65" y="38" class="streak-title">CURRENT STREAK</text>
        {"".join(c_elems)}
        <text x="65" y="105" class="streak-range">{current_range if current_streak > 0 else 'No active streak'}</text>
        <text x="65" y="125" class="streak-range" fill="var(--text)">Today: {today_conts} conts</text>
    </g>
    """)
    
    svg.add_element('<line x1="155" y1="20" x2="155" y2="140" class="divider" />')
    
    # Col 2: Longest Streak
    svg.add_element(f"""
    <g class="streak-item" style="animation-delay: 150ms;" transform="translate(155, 0)">
        <path d="{trophy_path}" transform="translate(25, 20) scale(0.9)" class="streak-icon-trophy" />
        <text x="60" y="38" class="streak-title">LONGEST STREAK</text>
        {"".join(l_elems)}
        <text x="60" y="105" class="streak-range">{longest_range if longest_streak > 0 else 'No historic streak'}</text>
    </g>
    """)
    
    svg.add_element('<line x1="305" y1="20" x2="305" y2="140" class="divider" />')
    
    # Col 3: Total Contributions
    svg.add_element(f"""
    <g class="streak-item" style="animation-delay: 300ms;" transform="translate(305, 0)">
        <path d="{star_icon}" transform="translate(20, 20) scale(0.9)" class="streak-icon-star" />
        <text x="55" y="38" class="streak-title">TOTAL CONTS</text>
        {"".join(t_elems)}
        <text x="55" y="105" class="streak-range">Yearly Contributions</text>
    </g>
    """)
    
    svg.save(STREAK_SVG_PATH)

def generate_languages_svg(data):
    """Generates the languages.svg file."""
    logger.info(f"Generating languages.svg -> {LANGUAGES_SVG_PATH}")
    
    repos = data.get("repositories", {})
    languages, total_bytes = aggregate_languages(repos)
    
    extra_styles = """
    .lang-progress-bg {
        fill: var(--border);
        rx: 5px;
    }
    .lang-item-name {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 13px;
        font-weight: 600;
        fill: var(--text);
    }
    .lang-item-percent {
        font-family: 'JetBrains Mono', -apple-system, sans-serif;
        font-size: 12px;
        fill: var(--text-muted);
    }
    .lang-row {
        opacity: 0;
        animation: slideInLeft 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-12px); }
        to { opacity: 1; transform: translateX(0); }
    }
    """
    
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[]"
    svg = SVGDocument(450, 200, subset_chars=charset, extra_styles=extra_styles)
    
    svg.add_element('<rect x="0.5" y="0.5" width="449" height="199" class="card" />')
    svg.add_element('<text x="25" y="35" class="title">Top Languages</text>')
    
    if not languages:
        svg.add_element('<text x="25" y="80" class="label">No language data found.</text>')
        svg.save(LANGUAGES_SVG_PATH)
        return
        
    bar_width = 400
    bar_x = 25
    bar_y = 55
    bar_h = 10
    
    current_x = bar_x
    drawn_segments = []
    
    top_languages = languages[:5]
    
    for idx, lang in enumerate(top_languages):
        lang_pct = lang["size"] / total_bytes if total_bytes > 0 else 0
        w = lang_pct * bar_width
        if w < 1:
            continue
            
        drawn_segments.append(f"""
        <rect x="{current_x}" y="{bar_y}" width="0" height="{bar_h}" fill="{lang['color']}">
            <animate attributeName="width" from="0" to="{w}" dur="1.2s" fill="freeze" />
        </rect>
        """)
        current_x += w
        
    svg.add_element(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_h}" class="lang-progress-bg" />')
    
    for seg in drawn_segments:
        svg.add_element(seg)
        
    col1_x = 25
    col2_x = 225
    y_start = 90
    dy = 28
    
    for idx, lang in enumerate(languages[:8]):
        col = col1_x if idx % 2 == 0 else col2_x
        row = idx // 2
        y = y_start + row * dy
        anim_delay = idx * 80
        
        svg.add_element(f"""
        <g class="lang-row" style="animation-delay: {anim_delay}ms;">
            <circle cx="{col + 8}" cy="{y - 4}" r="6" fill="{lang["color"]}" />
            <text x="{col + 24}" y="{y}" class="lang-item-name">{lang["name"]}</text>
            <text x="{col + 140}" y="{y}" class="lang-item-percent">{lang["percent"]}%</text>
        </g>
        """)
        
    svg.save(LANGUAGES_SVG_PATH)

def main():
    try:
        data = fetch_graphql_data()
        generate_stats_svg(data)
        generate_streak_svg(data)
        generate_languages_svg(data)
        logger.info("Stats SVGs updated successfully.")
    except Exception as e:
        logger.error(f"Error generating statistics SVGs: {e}")
        raise e

if __name__ == "__main__":
    main()
