import os
from datetime import datetime
from scripts.config import STATS_SVG_PATH, STREAK_SVG_PATH, LANGUAGES_SVG_PATH
from scripts.github_graphql import fetch_graphql_data, calculate_streak, aggregate_languages
from scripts.svg import SVGDocument
from scripts.utils import logger

PAD    = 20
GAP    = 12
TW     = 760

def make_sparkline(weeks_data, x_min, x_max, y_min, y_max):
    last_12 = weeks_data[-12:]
    totals  = [sum(d.get("contributionCount",0) for d in w.get("contributionDays",[])) for w in last_12]
    n = len(totals)
    if n < 2: return "","", (0,0)
    lo, hi = min(totals), max(totals)
    rng = hi-lo if hi!=lo else 1
    pts = []
    dx  = (x_max-x_min)/(n-1)
    for i,v in enumerate(totals):
        pts.append((x_min+i*dx, y_max-(v-lo)/rng*(y_max-y_min)))
    line = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(n-1):
        p0,p1 = pts[i],pts[i+1]
        cx = p0[0]+(p1[0]-p0[0])/2
        line += f"C {cx:.1f},{p0[1]:.1f} {cx:.1f},{p1[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} "
    area = f"{line} L {pts[-1][0]:.1f},{y_max} L {pts[0][0]:.1f},{y_max} Z"
    return line, area, pts[-1]


def generate_stats_svg(data):
    logger.info(f"Generating stats.svg -> {STATS_SVG_PATH}")
    repos       = data.get("repositories",{})
    total_repos = repos.get("totalCount",0)
    total_stars = sum(n.get("stargazerCount",0) for n in repos.get("nodes",[]))
    coll        = data.get("contributionsCollection",{})
    commits     = coll.get("totalCommitContributions",0)
    prs         = data.get("pullRequests",{}).get("totalCount",0)
    followers   = data.get("followers",{}).get("totalCount",0)
    following   = data.get("following",{}).get("totalCount",0)
    weeks       = coll.get("contributionCalendar",{}).get("weeks",[])
    line_path, area_path, last_pt = make_sparkline(weeks,248,430,52,130)

    STATS = [
        ("Commits (Past Year)", commits,     "M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-.5 5h1v6l4.25 2.55-.5.87-4.75-2.87V7z"),
        ("Repositories",        total_repos, "M4 4h16v16H4V4zm2 2v12h12V6H6z"),
        ("Total Stars",         total_stars, "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"),
        ("Pull Requests",       prs,         "M11 18H3v-2h8zm0-4H3v-2h8zm0-4H3V8h8zm10 0v10l-4-4-4 4V10zm-4-6l4 4H13z"),
        ("Followers",           followers,   "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"),
    ]

    CARD_H = PAD + 20 + GAP + len(STATS)*26 + GAP + 24 + PAD
    extra = """
    .sparkline-line{fill:none;stroke:var(--accent);stroke-width:2px;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:800;stroke-dashoffset:800;animation:drawLine 2s .3s forwards;}
    .sparkline-area{fill:var(--sparkline-fill);}
    .sparkline-dot{fill:var(--accent);stroke:var(--bg-card);stroke-width:1.5px;}
    .sparkline-grid{stroke:var(--border);stroke-dasharray:2 4;stroke-width:1px;}
    .stat-label{font-family:'JetBrains Mono',sans-serif;font-size:12px;fill:var(--text-muted);}
    .stat-val{font-family:'JetBrains Mono',sans-serif;font-size:12px;font-weight:700;fill:var(--accent);}
    .stat-icon{fill:var(--accent);}
    @keyframes drawLine{to{stroke-dashoffset:0;}}
    """
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[] "
    svg = SVGDocument(TW, CARD_H, subset_chars=charset, extra_styles=extra)
    svg.add_element(f'<rect x=".5" y=".5" width="{TW-1}" height="{CARD_H-1}" class="card" />')
    svg.add_element(f'<text x="{PAD}" y="{PAD+14}" class="title">Developer Statistics</text>')

    for i,(label,val,icon_d) in enumerate(STATS):
        y = PAD+20+GAP+i*26+16
        svg.add_element(f'<path d="{icon_d}" transform="translate({PAD},{y-13}) scale(.6)" class="stat-icon" />')
        svg.add_element(f'<text x="{PAD+18}" y="{y}" class="stat-label">{label}</text>')
        svg.add_element(f'<text x="190" y="{y}" class="stat-val">{val:,}</text>')

    SPK_X1,SPK_X2 = 248,430
    SPK_Y1,SPK_Y2 = PAD+36,PAD+116
    svg.add_element(f'<text x="{SPK_X1}" y="{PAD+18}" class="stat-label">Weekly Activity</text>')
    svg.add_element(f'<text x="{SPK_X1}" y="{PAD+30}" class="stat-label" font-size="9">Past 12 Weeks</text>')
    for gy in [SPK_Y1,(SPK_Y1+SPK_Y2)//2,SPK_Y2]:
        svg.add_element(f'<line x1="{SPK_X1}" y1="{gy}" x2="{SPK_X2}" y2="{gy}" class="sparkline-grid" />')
    if line_path:
        svg.add_element(f'<path d="{area_path}" class="sparkline-area" />')
        svg.add_element(f'<path d="{line_path}" class="sparkline-line" />')
        svg.add_element(f'<circle cx="{last_pt[0]:.1f}" cy="{last_pt[1]:.1f}" r="3.5" class="sparkline-dot" />')

    leg_y = CARD_H-PAD-4
    svg.add_element(f'<rect x="{SPK_X1}" y="{leg_y-14}" width="{SPK_X2-SPK_X1}" height="20" fill="none" stroke="var(--border)" stroke-width=".5" rx="4" />')
    svg.add_element(f'<text x="{SPK_X1+8}" y="{leg_y}" class="stat-label" font-size="10">Followers: <tspan class="stat-val" font-size="10">{followers}</tspan></text>')
    svg.add_element(f'<text x="{SPK_X1+105}" y="{leg_y}" class="stat-label" font-size="10">Following: <tspan class="stat-val" font-size="10">{following}</tspan></text>')
    svg.save(STATS_SVG_PATH)


def generate_streak_svg(data):
    """Pure static text — no clipPath, no group transforms. 100% GitHub-safe."""
    logger.info(f"Generating streak.svg -> {STREAK_SVG_PATH}")
    cal    = data.get("contributionsCollection",{}).get("contributionCalendar",{})
    weeks  = cal.get("weeks",[])
    streak = calculate_streak(weeks)
    cur    = streak["current_streak"]
    lng    = streak["longest_streak"]
    total  = cal.get("totalContributions",0)
    today  = streak["today_contributions"]

    def fmt(sk, ek, cnt):
        if cnt == 0: return "No active streak"
        s = datetime.strptime(streak[sk],"%Y-%m-%d").strftime("%b %d")
        e = datetime.strptime(streak[ek],"%Y-%m-%d").strftime("%b %d")
        return f"{s} - {e}"

    subs = [fmt("current_start","current_end",cur), fmt("longest_start","longest_end",lng), f"Today: {today} conts"]
    labels = ["CURRENT STREAK","LONGEST STREAK","TOTAL COMMITS"]
    values = [cur, lng, total]
    colors = ["#E36C2F","#4DA269","#8A63D2"]

    CARD_H = 130
    extra = """
    .sk-label{font-family:'JetBrains Mono',sans-serif;font-size:9px;font-weight:700;fill:var(--text-muted);letter-spacing:1px;}
    .sk-num{font-family:'JetBrains Mono',sans-serif;font-size:36px;font-weight:800;}
    .sk-sub{font-family:'JetBrains Mono',sans-serif;font-size:9px;fill:var(--text-muted);}
    .sk-div{stroke:var(--border);stroke-width:1px;}
    """
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[] "
    svg = SVGDocument(TW, CARD_H, subset_chars=charset, extra_styles=extra)
    svg.add_element(f'<rect x=".5" y=".5" width="{TW-1}" height="{CARD_H-1}" class="card" />')

    COL_W = TW // 3
    for i,(label,val,sub,col) in enumerate(zip(labels,values,subs,colors)):
        # All coords absolute — no group transform
        cx = i*COL_W + COL_W//2
        if i > 0:
            svg.add_element(f'<line x1="{i*COL_W}" y1="15" x2="{i*COL_W}" y2="{CARD_H-15}" class="sk-div" />')
        svg.add_element(f'<text x="{cx}" y="28" text-anchor="middle" class="sk-label">{label}</text>')
        svg.add_element(f'<text x="{cx}" y="82" text-anchor="middle" class="sk-num" fill="{col}">{val:,}</text>')
        svg.add_element(f'<text x="{cx}" y="104" text-anchor="middle" class="sk-sub">{sub}</text>')

    svg.save(STREAK_SVG_PATH)


def generate_languages_svg(data):
    logger.info(f"Generating languages.svg -> {LANGUAGES_SVG_PATH}")
    repos = data.get("repositories",{})
    languages, total_bytes = aggregate_languages(repos)
    top = languages[:10]
    ROWS   = (len(top)+1)//2
    ROW_H  = 26
    BAR_H  = 10
    CARD_H = PAD+18+GAP+BAR_H+GAP+ROWS*ROW_H+PAD

    extra = """
    .lg-title{font-family:'JetBrains Mono',sans-serif;font-size:13px;font-weight:700;fill:var(--text);}
    .lg-name{font-family:'JetBrains Mono',sans-serif;font-size:11px;font-weight:600;fill:var(--text);}
    .lg-pct{font-family:'JetBrains Mono',sans-serif;font-size:10px;fill:var(--text-muted);}
    """
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., :;%#&_+-()[] "
    svg = SVGDocument(TW, CARD_H, subset_chars=charset, extra_styles=extra)
    svg.add_element(f'<rect x=".5" y=".5" width="{TW-1}" height="{CARD_H-1}" class="card" />')
    svg.add_element(f'<text x="{PAD}" y="{PAD+13}" class="lg-title">Top Languages</text>')

    if not top:
        svg.add_element(f'<text x="{PAD}" y="60" class="lg-name">No language data.</text>')
        svg.save(LANGUAGES_SVG_PATH)
        return

    BAR_X = PAD
    BAR_W = TW-PAD*2
    BAR_Y = PAD+18+GAP
    svg.add_element(f'<rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" fill="var(--border)" rx="4" />')
    cx = BAR_X
    for lang in top:
        pct = lang["size"]/total_bytes if total_bytes else 0
        sw  = round(pct*BAR_W,2)
        if sw < 1: continue
        svg.add_element(f'<rect x="{cx}" y="{BAR_Y}" width="{sw}" height="{BAR_H}" fill="{lang["color"]}" rx="2" />')
        cx += sw

    ROW_Y0 = BAR_Y+BAR_H+GAP+12
    C1 = PAD
    C2 = TW//2+PAD//2
    HALF = TW//2-PAD*2

    for idx,lang in enumerate(top):
        col = C1 if idx%2==0 else C2
        row = idx//2
        y   = ROW_Y0+row*ROW_H
        pct = f"{lang['percent']}%"
        svg.add_element(f'<circle cx="{col+5}" cy="{y-4}" r="5" fill="{lang["color"]}" />')
        svg.add_element(f'<text x="{col+18}" y="{y}" class="lg-name">{lang["name"]}</text>')
        svg.add_element(f'<text x="{col+HALF}" y="{y}" text-anchor="end" class="lg-pct">{pct}</text>')

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
