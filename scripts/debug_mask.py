import cv2
import numpy as np

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)

# Let's save just the green mask so we visually know what we're routing over.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([45, 100, 40])
upper_green = np.array([75, 255, 255])
mask_hsv = cv2.inRange(hsv, lower_green, upper_green)

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_MASK_HSV.png", mask_hsv)

# Let's also do a strict RGB distance mask for ONLY the exact green [29, 121, 6]
# BGR is [6, 121, 29]
# We allow a small tolerance of 10 in B, G, R
bgr = np.array([6, 121, 29], dtype=np.int16)
img_int = img.astype(np.int16)

dist = np.abs(img_int - bgr)
# max difference across channels <= 30
strict_mask = (np.max(dist, axis=2) <= 40).astype(np.uint8) * 255

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_MASK_STRICT_RGB.png", strict_mask)

print("Saved DEBUG_MASK_HSV.png with", np.sum(mask_hsv > 0), "walkable pixels")
print("Saved DEBUG_MASK_STRICT_RGB.png with", np.sum(strict_mask > 0), "walkable pixels")
