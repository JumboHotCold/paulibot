import cv2
import numpy as np

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Target color: [141, 187, 130]
target = np.array([141, 187, 130], dtype=np.int16)
img_int = img_rgb.astype(np.int16)

dist = np.abs(img_int - target)
mask = (np.max(dist, axis=2) < 20).astype(np.uint8) * 255

print("Pixels matching [141, 187, 130]:", np.sum(mask > 0))

# Perform distance transform max to see if it's a "thin" line or a thick blob
dist_transform = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
print("Max thickness of these pixels:", np.max(dist_transform))

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_SUSPECT_GREEN.png", mask)
