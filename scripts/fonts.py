import os
import urllib.request
import base64
from scripts.config import FONT_URL, FONT_PATH, FONTS_DIR, FONT_FAMILY
from scripts.utils import logger, retry_api

@retry_api(retries=3, delay=5)
def download_font():
    """Downloads the JetBrains Mono font if not already present."""
    if os.path.exists(FONT_PATH):
        logger.info(f"Font already exists at {FONT_PATH}")
        return

    logger.info(f"Downloading font from {FONT_URL}...")
    req = urllib.request.Request(
        FONT_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req) as response:
        with open(FONT_PATH, "wb") as f:
            f.write(response.read())
    logger.info("Font downloaded successfully.")

def subset_font(text_characters):
    """
    Subsets the downloaded font using fontTools to include only the required characters.
    Saves it as a woff2 file and returns the base64 encoded string.
    """
    download_font()
    
    woff2_path = os.path.splitext(FONT_PATH)[0] + ".woff2"
    
    try:
        from fontTools.ttLib import TTFont
        from fontTools.subset import Subsetter
        
        logger.info(f"Subsetting font for characters: {text_characters}")
        
        # Load the font and set up subsetter
        font = TTFont(FONT_PATH)
        subsetter = Subsetter()
        subsetter.populate(text=text_characters)
        subsetter.subset(font)
        
        # Save as WOFF2 flavor
        font.flavor = "woff2"
        font.save(woff2_path)
        logger.info(f"Subsetted font saved to {woff2_path}")
        
        # Read and encode to base64
        with open(woff2_path, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        return font_base64
        
    except ImportError:
        logger.warning("fontTools or brotli not installed. Using raw font base64 without subsetting.")
        # Fall back to base64 encoding the whole TTF file if we can't subset it
        with open(FONT_PATH, "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode("utf-8")
        return font_base64
    except Exception as e:
        logger.error(f"Error during font subsetting: {e}")
        # Try returning raw if possible
        if os.path.exists(FONT_PATH):
            with open(FONT_PATH, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        raise e

def get_font_style(subset_chars=None):
    """Generates the CSS @font-face style string containing the base64 font."""
    if not subset_chars:
        # Default character set to support standard ASCII characters and common additions
        subset_chars = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            " .,:;!@#$%^&*()_+-=[]{}|<>?/~\\'`\"⚡💻🚀"
        )
    
    try:
        b64_font = subset_font(subset_chars)
        return f"""
@font-face {{
    font-family: '{FONT_FAMILY}';
    src: url(data:font/woff2;charset=utf-8;base64,{b64_font}) format('woff2');
    font-weight: normal;
    font-style: normal;
}}
"""
    except Exception as e:
        logger.error(f"Failed to generate font style: {e}")
        # Return fallback font style mapping to system mono
        return f"/* Font load failure: {e} */"
