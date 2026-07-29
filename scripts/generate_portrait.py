import os
import shutil
import numpy as np
from PIL import Image
from scripts.config import PORTRAIT, THEME, FONT_FAMILY
from scripts.svg import SVGDocument
from scripts.fonts import get_font_style
from scripts.utils import logger

# Try loading cv2 and rembg, handling imports gracefully if they are missing
try:
    import cv2
except ImportError:
    cv2 = None

try:
    from rembg import remove
except ImportError:
    remove = None

def find_input_image():
    """Finds the first existing portrait image path from configured paths."""
    # First check default input
    if os.path.exists(PORTRAIT["input_path"]):
        return PORTRAIT["input_path"]
    
    # Check backup paths
    for path in PORTRAIT["backup_input_paths"]:
        if os.path.exists(path):
            logger.info(f"Found input image at backup path: {path}")
            # Copy to default input path for consistency
            try:
                shutil.copy(path, PORTRAIT["input_path"])
                return PORTRAIT["input_path"]
            except Exception as e:
                logger.error(f"Failed to copy {path} to {PORTRAIT['input_path']}: {e}")
                return path
                
    return None

def apply_gamma(image, gamma=1.0):
    """Applies gamma correction to a grayscale image."""
    if cv2 is None:
        # Fallback numpy-only implementation of gamma correction
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return table[image]
        
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def process_image(img_path):
    """Processes the image and extracts ASCII text lines."""
    logger.info(f"Processing image for ASCII generation: {img_path}")
    
    # Load image using Pillow
    try:
        pil_img = Image.open(img_path)
    except Exception as e:
        logger.error(f"Failed to load image {img_path}: {e}")
        return None
        
    # Step 1: Remove background using rembg
    bg_removed = False
    if remove is not None:
        try:
            logger.info("Removing background with rembg...")
            pil_img = remove(pil_img)
            bg_removed = True
        except Exception as e:
            logger.warning(f"rembg background removal failed: {e}. Proceeding with raw image.")
    else:
        logger.warning("rembg is not installed. Skipping background removal.")

    # Convert to RGBA numpy array
    img_rgba = np.array(pil_img)
    
    # If background removed, transparency should be handled. Let's composite it on a white/black background.
    # For grayscale calculation, we place it on a black background
    if img_rgba.shape[2] == 4:
        alpha = img_rgba[:, :, 3] / 255.0
        # Create a black background
        bg = np.zeros(img_rgba[:, :, :3].shape, dtype=np.uint8)
        for c in range(3):
            bg[:, :, c] = (img_rgba[:, :, c] * alpha + bg[:, :, c] * (1.0 - alpha)).astype(np.uint8)
        img_rgb = bg
    else:
        img_rgb = img_rgba[:, :, :3]

    # Convert to grayscale
    if cv2 is not None:
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    else:
        # Manual RGB to Grayscale conversion
        gray = (0.2989 * img_rgb[:,:,0] + 0.5870 * img_rgb[:,:,1] + 0.1140 * img_rgb[:,:,2]).astype(np.uint8)

    # Step 2: Apply Bilateral Filtering to smooth flat areas and keep edges crisp
    if cv2 is not None:
        logger.info("Applying bilateral filtering...")
        smoothed = cv2.bilateralFilter(
            gray, 
            PORTRAIT["bilateral_d"], 
            PORTRAIT["bilateral_sigma_color"], 
            PORTRAIT["bilateral_sigma_space"]
        )
    else:
        smoothed = gray

    # Step 3: Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    if cv2 is not None:
        logger.info("Applying CLAHE...")
        clahe = cv2.createCLAHE(
            clipLimit=PORTRAIT["clahe_clip_limit"], 
            tileGridSize=PORTRAIT["clahe_tile_grid_size"]
        )
        equalized = clahe.apply(smoothed)
    else:
        equalized = smoothed

    # Step 4: Apply Gamma correction to adjust brightness/midtones
    logger.info(f"Applying gamma correction (gamma={PORTRAIT['gamma']})...")
    gamma_corrected = apply_gamma(equalized, PORTRAIT["gamma"])
    
    # Calculate target dimensions
    orig_h, orig_w = gamma_corrected.shape
    aspect = orig_h / orig_w
    
    target_w = PORTRAIT["width"]
    target_h = PORTRAIT["height"]
    if target_h <= 0:
        # height = width * aspect * char_aspect
        target_h = int(target_w * aspect * PORTRAIT["char_aspect"])
        
    logger.info(f"Resizing ASCII grid to {target_w}x{target_h} (aspect factor {PORTRAIT['char_aspect']})")
    
    # Resize to ASCII dimensions
    if cv2 is not None:
        resized = cv2.resize(gamma_corrected, (target_w, target_h), interpolation=cv2.INTER_AREA)
    else:
        # Resize using PIL fallback
        res_pil = Image.fromarray(gamma_corrected).resize((target_w, target_h), Image.Resampling.LANCZOS)
        resized = np.array(res_pil)
        
    # Map pixels to ASCII
    ramp = PORTRAIT["density_ramp"]
    ramp_len = len(ramp)
    
    ascii_lines = []
    for r in range(target_h):
        line_chars = []
        for c in range(target_w):
            val = resized[r, c]
            idx = int((val / 255.0) * (ramp_len - 1))
            line_chars.append(ramp[idx])
        ascii_lines.append("".join(line_chars))
        
    return ascii_lines

def generate_fallback_portrait():
    """Generates a stylish mock ASCII art fallback if no portrait image is found."""
    logger.warning("Generating geometric placeholder ASCII portrait...")
    width = PORTRAIT["width"]
    height = int(width * 0.7 * PORTRAIT["char_aspect"])
    
    # Create a simple geometric sphere pattern using density mapping
    ascii_lines = []
    cx, cy = width / 2.0, height / 2.0
    rx, ry = width * 0.35, height * 0.45
    ramp = PORTRAIT["density_ramp"]
    
    for y in range(height):
        row = []
        for x in range(width):
            # Calculate distance from center
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                # Value is 1 at center, 0 at boundary
                val = 1.0 - dist
                idx = int(val * (len(ramp) - 1))
                row.append(ramp[idx])
            else:
                row.append(" ")
        ascii_lines.append("".join(row))
    return ascii_lines

def main():
    img_path = find_input_image()
    if img_path:
        ascii_lines = process_image(img_path)
    else:
        logger.warning(f"No portrait image found in config.py paths. Creating fallback.")
        ascii_lines = generate_fallback_portrait()
        
    if not ascii_lines:
        ascii_lines = generate_fallback_portrait()
        
    # Create the SVG file
    # We will compute font parameters
    # Font size 8px, letter spacing 4.8px. Width = target_w * 4.8, Height = target_h * 9.6
    char_w = 4.8
    char_h = 8.5
    
    cols = len(ascii_lines[0])
    rows = len(ascii_lines)
    
    svg_w = int(cols * char_w) + 20
    svg_h = int(rows * char_h) + 20
    
    extra_styles = f"""
    .ascii-art {{
        font-family: '{FONT_FAMILY}', monospace;
        font-size: {char_h}px;
        line-height: {char_h}px;
        fill: var(--accent);
        letter-spacing: 0px;
    }}
    .ascii-row {{
        white-space: pre;
    }}
    /* Subtly animate the lines for a matrix/hologram glowing look */
    @keyframes pulse-glow {{
        0%, 100% {{ opacity: 0.85; filter: drop-shadow(0 0 1px var(--accent)); }}
        50% {{ opacity: 1.0; filter: drop-shadow(0 0 3px var(--accent)); }}
    }}
    .ascii-container {{
        animation: pulse-glow 4s ease-in-out infinite;
    }}
    """
    
    # Construct character list to subset JetBrains Mono correctly
    subset_chars = PORTRAIT["density_ramp"] + "1234567890abcdefghijklmnopqrstuvwxyz"
    
    svg = SVGDocument(svg_w, svg_h, subset_chars=subset_chars, extra_styles=extra_styles)
    
    # Add grouping element for animation
    svg_content = ['<g class="ascii-container">', f'<text x="10" y="15" class="ascii-art">']
    for idx, line in enumerate(ascii_lines):
        # Escape XML entities in ASCII
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
        svg_content.append(f'<tspan x="10" dy="{char_h}px" class="ascii-row">{escaped_line}</tspan>')
    svg_content.append('</text>')
    svg_content.append('</g>')
    
    svg.add_element("\n".join(svg_content))
    
    # Save the output file
    svg.save(PORTRAIT["output_path"])
    logger.info(f"ASCII portrait successfully saved to {PORTRAIT['output_path']}")

if __name__ == "__main__":
    main()
