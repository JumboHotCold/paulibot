import cv2
import numpy as np
from collections import Counter

path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
base = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP (1).png"

img_pathway = cv2.imread(path)
img_base = cv2.imread(base)

# Convert to RGB lists
pathway_rgb = cv2.cvtColor(img_pathway, cv2.COLOR_BGR2RGB).reshape(-1, 3)
base_rgb = cv2.cvtColor(img_base, cv2.COLOR_BGR2RGB).reshape(-1, 3)

# Count colors
print("Counting pathway colors...")
pathway_counts = Counter(map(tuple, pathway_rgb))

print("Counting base colors...")
base_counts = Counter(map(tuple, base_rgb))

# Find colors that are in pathway but not base, or significantly more in pathway
print("Filtering for new colors...")
new_colors = []
for color, count in pathway_counts.items():
    # Only care about solid blocks of color, not random anti-aliased single pixels
    if count > 1000:
        base_count = base_counts.get(color, 0)
        # If the color increased massively in count, it's our drawn line
        if count > base_count + 1000:
            new_colors.append((color, count, base_count))

# Sort by the sheer amount added
new_colors.sort(key=lambda x: x[1] - x[2], reverse=True)

print("Top manually added colors (Pathway Count / Base Count):")
for color, p_count, b_count in new_colors[:20]:
    print(f"Color {color}: Pathway={p_count}, Base={b_count}")
