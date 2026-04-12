import cv2
import numpy as np

path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(path)

# 1. Get the green mask
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([45, 100, 40])
upper_green = np.array([75, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)

# 2. Distance Transform
# Calculates distance to the nearest zero (edge)
dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)

print("Max distance in mask:", np.max(dist))

# 3. Filter out massive blobs!
# If the user drew a thin line, its max distance to an edge is half the line's thickness
# If the line is 20 pixels thick, max dist is ~10.
# If the open court is a 200x200 pixel blob, max dist is ~100.
# We can find all pixels that belong to a "thick" region and erase them.
# A morphological Opening with a big kernel removes thin lines and KEEPS thick blobs.
kernel_size = 25  # Any blob thicker than 25 pixels will survive
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
thick_blobs = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Remove the thick blobs from our green mask
thin_paths = cv2.subtract(mask, thick_blobs)

print("Pixels in original mask:", np.sum(mask > 0))
print("Pixels in thick blobs (like open court):", np.sum(thick_blobs > 0))
print("Pixels in thin pathways:", np.sum(thin_paths > 0))

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_THICK_BLOBS.png", thick_blobs)
cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_THIN_PATHS.png", thin_paths)
