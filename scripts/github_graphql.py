import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from scripts.config import GITHUB_USERNAME, GITHUB_TOKEN
from scripts.utils import logger, retry_api

GRAPHQL_URL = "https://api.github.com/graphql"

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    name
    login
    followers {
      totalCount
    }
    following {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoryContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            color
            weekday
          }
        }
      }
    }
    pullRequests(first: 1) {
      totalCount
    }
    issues(first: 1) {
      totalCount
    }
    repositoryDiscussions(first: 1) {
      totalCount
    }
  }
}
"""

def get_mock_data(username):
    """Returns mock profile data to ensure local scripts work without API setup."""
    logger.warning("Using mock data as GITHUB_TOKEN is not configured or API call failed.")
    
    # Generate 365 days of contributions for mock data
    weeks = []
    base_date = datetime.now() - timedelta(days=364)
    
    # Let's mock a streak of contributions
    for w in range(53):
        days = []
        for d in range(7):
            day_date = base_date + timedelta(days=w * 7 + d)
            # Create some realistic-looking contribution patterns
            day_str = day_date.strftime("%Y-%m-%d")
            # Weekends have fewer contributions, some random days have streak
            is_active = (day_date.weekday() < 5 and (w % 4 != 0 or d % 3 != 0)) or (w > 48)
            count = 3 if is_active else 0
            color = "#26a641" if count > 0 else "#161b22"
            days.append({
                "contributionCount": count,
                "date": day_str,
                "color": color,
                "weekday": d
            })
        weeks.append({"contributionDays": days})
        
    return {
        "name": "M Huzaifa Hafeez",
        "login": username,
        "followers": {"totalCount": 142},
        "following": {"totalCount": 85},
        "repositories": {
            "totalCount": 42,
            "nodes": [
                {
                    "name": "algo-union",
                    "stargazerCount": 24,
                    "languages": {
                        "edges": [
                            {"size": 150000, "node": {"name": "TypeScript", "color": "#3178C6"}},
                            {"size": 80000, "node": {"name": "React", "color": "#61DAFB"}},
                            {"size": 20000, "node": {"name": "CSS", "color": "#563d7c"}}
                        ]
                    }
                },
                {
                    "name": "django-ecommerce",
                    "stargazerCount": 15,
                    "languages": {
                        "edges": [
                            {"size": 120000, "node": {"name": "Python", "color": "#3572A5"}},
                            {"size": 30000, "node": {"name": "HTML", "color": "#e34c26"}},
                            {"size": 15000, "node": {"name": "JavaScript", "color": "#f1e05a"}}
                        ]
                    }
                },
                {
                    "name": "rust-dsa",
                    "stargazerCount": 12,
                    "languages": {
                        "edges": [
                            {"size": 95000, "node": {"name": "Rust", "color": "#dee5e6"}},
                            {"size": 5000, "node": {"name": "Shell", "color": "#89e051"}}
                        ]
                    }
                },
                {
                    "name": "laravel-api",
                    "stargazerCount": 9,
                    "languages": {
                        "edges": [
                            {"size": 85000, "node": {"name": "PHP", "color": "#4F5D95"}},
                            {"size": 10000, "node": {"name": "Blade", "color": "#ff2d20"}}
                        ]
                    }
                }
            ]
        },
        "contributionsCollection": {
            "totalCommitContributions": 684,
            "totalPullRequestContributions": 48,
            "totalIssueContributions": 12,
            "totalRepositoryContributions": 8,
            "contributionCalendar": {
                "totalContributions": 752,
                "weeks": weeks
            }
        },
        "pullRequests": {"totalCount": 85},
        "issues": {"totalCount": 24},
        "repositoryDiscussions": {"totalCount": 6}
    }

@retry_api(retries=3, delay=5)
def fetch_graphql_data():
    """Fetches user profile metrics directly from GitHub's GraphQL endpoint."""
    if not GITHUB_TOKEN:
        logger.warning("No GitHub Token detected (GITHUB_TOKEN environment variable not set).")
        return get_mock_data(GITHUB_USERNAME)

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "electroapex-profile-generator"
    }
    
    payload = {
        "query": GRAPHQL_QUERY,
        "variables": {"username": GITHUB_USERNAME}
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(GRAPHQL_URL, data=data_bytes, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            if "errors" in result:
                logger.error(f"GraphQL Errors returned: {result['errors']}")
                raise ValueError(f"GraphQL API error: {result['errors'][0]['message']}")
                
            user_data = result.get("data", {}).get("user")
            if not user_data:
                raise ValueError("User not found in GitHub GraphQL response.")
                
            return user_data
            
    except urllib.error.HTTPError as e:
        if e.code == 401 or e.code == 403:
            logger.error(f"Authentication failure (status {e.code}). Please verify your token.")
            # Fall back to mock data so builds don't break during initial repo setups
            return get_mock_data(GITHUB_USERNAME)
        raise e
    except Exception as e:
        logger.error(f"GraphQL connection failed: {e}")
        raise e

def calculate_streak(calendar_weeks):
    """
    Calculates the current streak, longest streak, and active contribution details.
    Each week in calendar_weeks has contributionDays, list of objects:
    {contributionCount: int, date: str, color: str}
    """
    days = []
    for week in calendar_weeks:
        for day in week.get("contributionDays", []):
            days.append(day)
            
    # Sort days chronologically just in case
    days.sort(key=lambda x: x["date"])
    
    current_streak = 0
    longest_streak = 0
    
    curr_temp_streak = 0
    streak_start = None
    streak_end = None
    
    longest_start = None
    longest_end = None
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    for day in days:
        date_str = day["date"]
        count = day["contributionCount"]
        
        if count > 0:
            if curr_temp_streak == 0:
                streak_start = date_str
            curr_temp_streak += 1
            streak_end = date_str
            
            if curr_temp_streak > longest_streak:
                longest_streak = curr_temp_streak
                longest_start = streak_start
                longest_end = streak_end
        else:
            # Streak broken
            # Check if this day is today or yesterday. If yes, we don't break the current streak calculations
            # because today might not have contributions yet, and yesterday might be the last active day.
            if date_str not in (today_str, yesterday_str):
                curr_temp_streak = 0
                
    # Calculate active current streak (must end today or yesterday)
    active_current_streak = 0
    current_start = None
    current_end = None
    
    temp_streak = 0
    temp_start = None
    
    for day in days:
        count = day["contributionCount"]
        date_str = day["date"]
        
        if count > 0:
            if temp_streak == 0:
                temp_start = date_str
            temp_streak += 1
            temp_end = date_str
        else:
            if temp_streak > 0:
                # If the streak ended close enough to today
                end_dt = datetime.strptime(temp_end, "%Y-%m-%d")
                days_diff = (datetime.now() - end_dt).days
                if days_diff <= 1:
                    active_current_streak = temp_streak
                    current_start = temp_start
                    current_end = temp_end
            temp_streak = 0
            
    # Check if last run streak is still active
    if temp_streak > 0:
        active_current_streak = temp_streak
        current_start = temp_start
        current_end = temp_end
        
    return {
        "current_streak": active_current_streak,
        "current_start": current_start,
        "current_end": current_end,
        "longest_streak": longest_streak,
        "longest_start": longest_start,
        "longest_end": longest_end,
        "today_contributions": next((d["contributionCount"] for d in reversed(days) if d["date"] == today_str), 0)
    }

def aggregate_languages(repositories):
    """
    Aggregates languages across all queried repositories.
    Returns sorted list of dictionaries with language, size, percent, color, and repo_count.
    """
    lang_stats = {}
    total_bytes = 0
    
    for repo in repositories.get("nodes", []):
        repo_langs = repo.get("languages", {}).get("edges", [])
        for edge in repo_langs:
            size = edge.get("size", 0)
            lang_node = edge.get("node", {})
            name = lang_node.get("name")
            color = lang_node.get("color") or "#858585"
            
            if name:
                total_bytes += size
                if name not in lang_stats:
                    lang_stats[name] = {"size": 0, "color": color, "repos": set()}
                lang_stats[name]["size"] += size
                lang_stats[name]["repos"].add(repo["name"])
                
    result = []
    for name, stats in lang_stats.items():
        percentage = (stats["size"] / total_bytes * 100) if total_bytes > 0 else 0
        result.append({
            "name": name,
            "size": stats["size"],
            "color": stats["color"],
            "percent": round(percentage, 1),
            "repo_count": len(stats["repos"])
        })
        
    # Sort by size descending
    result.sort(key=lambda x: x["size"], reverse=True)
    return result, total_bytes
