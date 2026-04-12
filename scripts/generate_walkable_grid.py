"""
Green Pathway Extractor & Walkable Grid Generator
==================================================
Processes ST.PAUL MAP_PATHWAY.png to create a binary walkable grid.
Uses PIL instead of OpenCV to avoid high memory overhead.

Usage:
  python scripts/generate_walkable_grid.py
"""

from PIL import Image
import json
import os
import sys

def main():
    # ── Paths ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    pathway_img_path = os.path.join(
        project_root, 'images', '2D_Mapping', 'ST.PAUL MAP_PATHWAY.png'
    )
    output_json_path = os.path.join(
        project_root, 'frontend', 'src', 'data', 'walkableGrid.json'
    )
    debug_mask_path = os.path.join(
        project_root, 'images', '2D_Mapping', 'DEBUG_walkable_mask.png'
    )
    
    # ══════════════════════════════════════════════════════════════════════
    # STEP 1: Load image
    # ══════════════════════════════════════════════════════════════════════
    print("[1/4] Loading image with PIL...")
    try:
        img = Image.open(pathway_img_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
        
    img = img.convert('RGB')
    width, height = img.size
    print(f"      Size: {width}x{height}")
    
    # ══════════════════════════════════════════════════════════════════════
    # STEP 2: Downsample and find green pixels
    # ══════════════════════════════════════════════════════════════════════
    DOWNSCALE = 4
    grid_width = width // DOWNSCALE
    grid_height = height // DOWNSCALE
    print(f"[2/4] Downsampling to {grid_width}x{grid_height}...")
    
    # Resize to box to get average colors per block
    small_img = img.resize((grid_width, grid_height), Image.Resampling.BOX)
    pixels = small_img.load()
    
    # We want a strict green threshold in RGB
    # The drawing is pure, solid green on the map.
    # Typical RGB for the green: R < 100, G > 100, B < 100
    rows = []
    walkable_count = 0
    
    debug_img = Image.new('L', (grid_width, grid_height))
    debug_pixels = debug_img.load()
    
    print("[3/4] Extracting green pixels...")
    for y in range(grid_height):
        row_str = ""
        for x in range(grid_width):
            r, g, b = pixels[x, y]
            
            # Is it predominantly green?
            # Must have more green than red+blue combined (or fairly close), and fairly bright
            is_green = g > 120 and g > r * 1.5 and g > b * 1.3
            
            if is_green:
                row_str += "1"
                walkable_count += 1
                debug_pixels[x, y] = 255
            else:
                row_str += "0"
                debug_pixels[x, y] = 0
                
        rows.append(row_str)
        
    total_cells = grid_width * grid_height
    print(f"      Walkable cells: {walkable_count} ({walkable_count/total_cells*100:.2f}%)")
    
    # ══════════════════════════════════════════════════════════════════════
    # STEP 3: Export Grid
    # ══════════════════════════════════════════════════════════════════════
    print("[4/4] Exporting...")
    grid_data = {
        'width': grid_width,
        'height': grid_height,
        'originalWidth': width,
        'originalHeight': height,
        'downscale': DOWNSCALE,
        'rows': rows,
    }
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w') as f:
        json.dump(grid_data, f)
        
    # Scale up debug mask and save
    debug_full = debug_img.resize((width, height), Image.Resampling.NEAREST)
    debug_full.save(debug_mask_path)
    
    print("Done!")

if __name__ == "__main__":
    main()
