import urllib.request
import base64

def get_icon_base64(tech_name):
    url = f"https://skillicons.dev/icons?i={tech_name}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            svg_data = response.read()
            b64 = base64.b64encode(svg_data).decode('utf-8')
            return f"data:image/svg+xml;base64,{b64}"
    except Exception as e:
        print(f"Failed for {tech_name}: {e}")
        return None

print(get_icon_base64("react")[:100])
