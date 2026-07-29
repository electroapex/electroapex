import re
import urllib.request
import base64
import time

def get_icon_base64(tech_name):
    # Mapping for special cases
    mapping = {
        "HTML5": "html",
        "CSS3": "css",
        "Node.js": "nodejs",
        "Express.js": "express",
        "React Router": "react",
        "Tailwind CSS": "tailwindcss",
        "C++": "cpp",
        "C#": "cs",
        "Vue.js": "vue",
        "Adobe XD": "xd"
    }
    
    clean_name = mapping.get(tech_name, tech_name.lower().replace(" ", "").replace(".", ""))
    url = f"https://skillicons.dev/icons?i={clean_name}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            svg_data = response.read()
            b64 = base64.b64encode(svg_data).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    except Exception as e:
        print(f"Failed to fetch {clean_name} for {tech_name}")
        return None

with open("scripts/generate_headings.py", "r") as f:
    content = f.read()

# Add imports
if "import urllib.request" not in content:
    content = content.replace("import os", "import os\nimport urllib.request\nimport base64")

# Insert get_icon_base64 function
if "def get_icon_base64" not in content:
    func_str = """
def get_icon_base64(tech_name):
    mapping = {
        "HTML5": "html", "CSS3": "css", "Node.js": "nodejs", 
        "Express.js": "express", "React Router": "react", 
        "Tailwind CSS": "tailwindcss", "C++": "cpp", "C#": "cs", 
        "Vue.js": "vue", "Adobe XD": "xd", "TanStack Query": "react"
    }
    clean_name = mapping.get(tech_name, tech_name.lower().replace(" ", "").replace(".", ""))
    url = f"https://skillicons.dev/icons?i={clean_name}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            b64 = base64.b64encode(response.read()).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    except Exception:
        return None
"""
    content = content.replace("def generate_skills_svg():", func_str + "\ndef generate_skills_svg():")

# Replace circle with image
# Find: <circle cx="{curr_x + 11}" cy="{curr_y + 11}" r="4" fill="{color}" filter="drop-shadow(0 0 3px {color})" />
# Replace: 
# { f'<image href="{get_icon_base64(name)}" x="{curr_x + 4}" y="{curr_y + 4}" width="14" height="14" />' if get_icon_base64(name) else f'<circle cx="{curr_x + 11}" cy="{curr_y + 11}" r="4" fill="{color}" filter="drop-shadow(0 0 3px {color})" />' }

if "b64_img = get_icon_base64(name)" not in content:
    # First, modify the python loop where badges are appended
    find_str = """
            anim_delay = (badge_index * 0.15)
            badge_index += 1
            
            # The holographic 3D card"""
            
    replace_str = """
            anim_delay = (badge_index * 0.15)
            badge_index += 1
            
            b64_img = get_icon_base64(name)
            logo_svg = f'<image href="{b64_img}" x="{curr_x + 4}" y="{curr_y + 4}" width="14" height="14" />' if b64_img else f'<circle cx="{curr_x + 11}" cy="{curr_y + 11}" r="4" fill="{color}" filter="drop-shadow(0 0 3px {color})" />'
            
            # The holographic 3D card"""
    content = content.replace(find_str, replace_str)
    
    find_circle = """<circle cx="{curr_x + 11}" cy="{curr_y + 11}" r="4" fill="{color}" filter="drop-shadow(0 0 3px {color})" />"""
    replace_circle = """{logo_svg}"""
    content = content.replace(find_circle, replace_circle)

with open("scripts/generate_headings.py", "w") as f:
    f.write(content)
print("Updated successfully")
