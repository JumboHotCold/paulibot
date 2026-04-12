import cv2
import numpy as np

path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
base = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP (1).png"

img_pathway = cv2.imread(path)
img_base = cv2.imread(base)

# Calculate difference
diff = cv2.absdiff(img_pathway, img_base)

# Strict difference -> differences greater than 100 in any channel!
mask_strict = (np.max(diff, axis=2) > 100).astype(np.uint8) * 255

walkable_count = np.sum(mask_strict > 0)
print("STRICT Changes between Base and Pathway maps:", walkable_count, "pixels")

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_DIFF_MASK_STRICT.png", mask_strict)
