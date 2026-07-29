# Technical Documentation & User Guide

This guide details the setup, configuration, architecture, and troubleshooting procedures for the redesigned self-generating GitHub profile system.

---

## 1. Installation Guide

This system requires Python 3.10+, Git, and the GitHub CLI. Install all dependencies for your platform using the commands below:

### Fedora
```bash
# Install Python, pip, Git, and GitHub CLI
sudo dnf install -y python3 python3-pip git gh

# Install image processing system libraries
sudo dnf install -y mesa-libGL glib2
```

### Ubuntu / Debian
```bash
# Install Python, pip, Git, and GitHub CLI
sudo apt update
sudo apt install -y python3 python3-pip git gh

# Install image processing system libraries
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python, Git, and GitHub CLI
brew install python git gh
```

### Windows (PowerShell)
```powershell
# Install Git and Python via Winget (Windows Package Manager)
winget install -e --id Git.Git
winget install -e --id Python.Python.3.10

# Install GitHub CLI
winget install -e --id GitHub.cli
```

---

## 2. CLI Commands (Start to Finish)

Follow this exact sequence to initialize the repository, configure secrets, set up the environment, and execute the generation scripts:

### Git Initialization & Repo Setup
```bash
# Initialize git repository
git init

# Add all project files
git add .
git commit -m "Initial commit of self-generating profile system"

# Authenticate with GitHub CLI
gh auth login

# Create a new repository on GitHub
gh repo create electroapex --public --confirm

# Add the remote and push
git remote add origin https://github.com/electroapex/electroapex.git
git branch -M main
git push -u origin main
```

### Local Environment & Dependency Setup
```bash
# Create a Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
# .\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### Local Verification & SVG Generation
Before pushing to GitHub, you can test the scripts locally:
```bash
# Run the generators in sequence
export PYTHONPATH=.
python scripts/generate_headings.py
python scripts/generate_portrait.py
python scripts/generate_stats.py
python scripts/generate_year.py
python scripts/generate_projects.py
python scripts/generate_dividers.py
```

### GitHub Secrets & Actions Setup
To allow the GitHub Actions workflow to run successfully:
```bash
# Enable GitHub Actions workflows in the repo
gh workflow enable "Update Profile SVGs"

# Trigger a manual run of the workflow to verify it works on GitHub
gh workflow run update.yml
```

---

## 3. Configuration & Customization Guide

All settings are managed inside `scripts/config.py`.

### Change Username
Update `GITHUB_USERNAME` and `GITHUB_REPO` to point to your profile:
```python
GITHUB_USERNAME = "your_username"
GITHUB_REPO = "your_username"
```

### Modify Featured Projects
Add, modify, or remove projects from the `PROJECTS_LIST` inside `config.py` to change what displays inside `projects.svg`:
```python
PROJECTS_LIST = [
    {
        "title": "Project Name",
        "description": "Short description...",
        "stack": ["React", "Python"],
        "status": "production",
        "stars": 42,
        "color": "#3178c6",
        "logo_text": "PN"
    },
    # ...
]
```

### Adjust ASCII Portrait Settings
Modify the `PORTRAIT` settings inside `scripts/config.py`:
- `width`: Number of characters wide (default 90). Higher numbers increase portrait detail but increase file size.
- `density_ramp`: The characters mapping from dark to light. Standard is `" .`:-=+*cs#%@"`.
- `gamma`: Adjusts light mapping. Decreasing gamma will darken the image; increasing it will make midtones brighter.

---

## 4. Architecture & Data Flow

Below is the design detailing how the generation system works:

```mermaid
graph TD
    A[Nightly Trigger / Manual Workflow] --> B[github_graphql.py]
    B -->|GraphQL query| C[GitHub GraphQL API]
    C -->|JSON response| B
    B -->|Calculates streaks & language stats| D[generate_stats.py]
    B -->|Contribution calendar| E[generate_year.py]
    
    F[images/portrait.jpg] --> G[generate_portrait.py]
    G -->|rembg background removal| H[Grayscale + Bilateral Filter]
    H -->|CLAHE + Gamma Correction| I[ASCII characters mapping]
    I -->|SVG text writing| J[assets/portrait.svg]
    
    K[fonts.py] -->|Downloads JetBrains Mono| L[Subsets TTF to WOFF2]
    L -->|Base64 string| M[svg.py base class]
    M -->|Embeds font styles & CSS vars| J
    M -->|Embeds font styles & CSS vars| N[assets/stats.svg]
    M -->|Embeds font styles & CSS vars| O[assets/year.svg]
    
    D -->|Generates stats| N
    D -->|Generates streak| P[assets/streak.svg]
    D -->|Generates languages| Q[assets/languages.svg]
    E -->|Generates calendar| O
    R[generate_headings.py] -->|Generates headings & typing| S[assets/typing.svg]
    R -->|Generates skills grid| T[assets/skills.svg]
    
    U[generate_projects.py] -->|Generates project panels| V[assets/projects.svg]
    W[generate_dividers.py] -->|Generates particle line| X[assets/divider.svg]
```

---

## 5. Technical Details: Slot-Machine Digit Counters

Because JavaScript is forbidden on GitHub README pages, we implement rolling count-up animations for all statistics inside `stats.svg` and `streak.svg` using pure SVG/SMIL. 

1. **Digital Wheel Stacking**: The script splits each metric (like `752` commits) into individual digits.
2. **Clipping Boundary**: For each digit, it constructs a `clipPath` bounding box matching the font height.
3. **Translational Animation**: It renders a vertical column containing digits `0-9` stacked consecutively.
4. **SMIL Animation**: It applies a `<animateTransform>` translation shifting the vertical coordinate up by `-digit * digit_height` using a smooth cubic-bezier easing curve, making the counter roll when the page load caches trigger.

---

## 6. Troubleshooting & FAQ

### Issue: "cv2 module not found" or "GLX errors"
**Solution**: Ensure your host environment has mesa-libGL installed (e.g. `sudo apt install libgl1-mesa-glx`). The project uses `opencv-python-headless` in `requirements.txt` to avoid needing heavy windowing system libraries, but basic GL support is still required.

### Issue: "rembg fails to load or download u2net.onnx"
**Solution**: Upon first run, `rembg` attempts to download its background removal model `u2net.onnx` from GitHub releases. If you are offline or behind a proxy, download the file manually and place it in `~/.u2net/u2net.onnx`. If it continues to fail, `generate_portrait.py` will catch the error and process the raw image directly, preserving stability.

### Issue: GitHub Action fails with "Permission to repo denied"
**Solution**: By default, GitHub Actions workflows might run with read-only permissions. The workflow in this project explicitly requests `permissions: contents: write` which overrides this. If it still fails, go to your repository Settings -> Actions -> General -> Workflow permissions and select "Read and write permissions".
