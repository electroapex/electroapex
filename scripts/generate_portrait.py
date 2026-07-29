import os
import shutil
import numpy as np
from PIL import Image
from scripts.config import PORTRAIT, THEME, FONT_FAMILY
from scripts.svg import SVGDocument
from scripts.fonts import get_font_style
from scripts.utils import logger

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
    if os.path.exists(PORTRAIT["input_path"]):
        return PORTRAIT["input_path"]
    
    for path in PORTRAIT["backup_input_paths"]:
        if os.path.exists(path):
            logger.info(f"Found input image at backup path: {path}")
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
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return table[image]
        
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def process_image(img_path):
    """Processes the image and extracts ASCII text lines."""
    logger.info(f"Processing image for ASCII generation: {img_path}")
    
    try:
        pil_img = Image.open(img_path)
    except Exception as e:
        logger.error(f"Failed to load image {img_path}: {e}")
        return None
        
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

    img_rgba = np.array(pil_img)
    
    if img_rgba.shape[2] == 4:
        alpha = img_rgba[:, :, 3] / 255.0
        bg = np.zeros(img_rgba[:, :, :3].shape, dtype=np.uint8)
        for c in range(3):
            bg[:, :, c] = (img_rgba[:, :, c] * alpha + bg[:, :, c] * (1.0 - alpha)).astype(np.uint8)
        img_rgb = bg
    else:
        img_rgb = img_rgba[:, :, :3]

    if cv2 is not None:
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    else:
        gray = (0.2989 * img_rgb[:,:,0] + 0.5870 * img_rgb[:,:,1] + 0.1140 * img_rgb[:,:,2]).astype(np.uint8)

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

    if cv2 is not None:
        logger.info("Applying CLAHE...")
        clahe = cv2.createCLAHE(
            clipLimit=PORTRAIT["clahe_clip_limit"], 
            tileGridSize=PORTRAIT["clahe_tile_grid_size"]
        )
        equalized = clahe.apply(smoothed)
    else:
        equalized = smoothed

    logger.info(f"Applying gamma correction (gamma={PORTRAIT['gamma']})...")
    gamma_corrected = apply_gamma(equalized, PORTRAIT["gamma"])
    
    orig_h, orig_w = gamma_corrected.shape
    aspect = orig_h / orig_w
    
    target_w = PORTRAIT["width"]
    target_h = PORTRAIT["height"]
    if target_h <= 0:
        target_h = int(target_w * aspect * PORTRAIT["char_aspect"])
        
    logger.info(f"Resizing ASCII grid to {target_w}x{target_h} (aspect factor {PORTRAIT['char_aspect']})")
    
    if cv2 is not None:
        resized = cv2.resize(gamma_corrected, (target_w, target_h), interpolation=cv2.INTER_AREA)
    else:
        res_pil = Image.fromarray(gamma_corrected).resize((target_w, target_h), Image.Resampling.LANCZOS)
        resized = np.array(res_pil)
        
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
    
    ascii_lines = []
    cx, cy = width / 2.0, height / 2.0
    rx, ry = width * 0.35, height * 0.45
    ramp = PORTRAIT["density_ramp"]
    
    for y in range(height):
        row = []
        for x in range(width):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = dx*dx + dy*dy
            if dist <= 1.0:
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
    /* Pulse glow effect on text grid */
    @keyframes pulse-glow {{
        0%, 100% {{ opacity: 0.85; filter: drop-shadow(0 0 1px var(--accent)); }}
        50% {{ opacity: 1.0; filter: drop-shadow(0 0 3px var(--accent)); }}
    }}
    .ascii-container {{
        animation: pulse-glow 4s ease-in-out infinite;
    }}
    .scan-line {{
        fill: var(--accent);
        opacity: 0.6;
        filter: url(#scan-glow);
    }}
    """
    
    subset_chars = PORTRAIT["density_ramp"] + "1234567890abcdefghijklmnopqrstuvwxyz"
    
    svg = SVGDocument(svg_w, svg_h, subset_chars=subset_chars, extra_styles=extra_styles)
    
    # Add filter for scanline glow
    svg.add_def("""
    <filter id="scan-glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
    """)
    
    # Add grouping element for animation
    svg_content = ['<g class="ascii-container">', f'<text x="10" y="15" class="ascii-art">']
    for idx, line in enumerate(ascii_lines):
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
        svg_content.append(f'<tspan x="10" dy="{char_h}px" class="ascii-row">{escaped_line}</tspan>')
    svg_content.append('</text>')
    svg_content.append('</g>')
    
    # Add scanline overlay
    svg_content.append(f"""
    <!-- Vertical scanning beam -->
    <rect x="10" y="10" width="{svg_w - 20}" height="2" class="scan-line">
        <animate attributeName="y" values="10; {svg_h - 10}; 10" dur="6s" repeatCount="indefinite" />
    </rect>
    """)
    
    svg.add_element("\n".join(svg_content))
    svg.save(PORTRAIT["output_path"])
    logger.info(f"ASCII portrait successfully saved to {PORTRAIT['output_path']}")

if __name__ == "__main__":
    main()
