import cv2
import numpy as np

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([40, 50, 40])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
binary_grid = (mask > 0).astype(np.uint8)

# Bridge gaps
gap_bridge_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
img_closed = cv2.morphologyEx(binary_grid * 255, cv2.MORPH_CLOSE, gap_bridge_kernel)

# Skeletonize
img_bin = img_closed.copy()
size = np.size(img_bin)
skel = np.zeros(img_bin.shape, np.uint8)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
done = False
while not done:
    eroded = cv2.erode(img_bin, element)
    temp = cv2.dilate(eroded, element)
    temp = cv2.subtract(img_bin, temp)
    skel = cv2.bitwise_or(skel, temp)
    img_bin = eroded.copy()
    zeros = size - cv2.countNonZero(img_bin)
    if zeros == size:
        done = True

# Dilate skeleton
kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
skel_thick = cv2.dilate(skel, kernel_dilate)

# Check connectivity
num_labels, labels = cv2.connectedComponents(skel_thick)
print(f"Number of connected components in THICK SKELETON: {num_labels}")

s_x, s_y = 2754, 620
e_x, e_y = 2117, 1782

def snap(x, y, labels):
    walkable_y, walkable_x = np.nonzero(labels)
    dist = (walkable_y - y)**2 + (walkable_x - x)**2
    idx = np.argmin(dist)
    return walkable_x[idx], walkable_y[idx], labels[walkable_y[idx], walkable_x[idx]]

sx, sy, sl = snap(s_x, s_y, labels)
ex, ey, el = snap(e_x, e_y, labels)

print(f"Start Label: {sl}")
print(f"End Label: {el}")

# Find top component sizes
unique, counts = np.unique(labels, return_counts=True)
component_sizes = sorted(zip(unique, counts), key=lambda x: x[1], reverse=True)
for label, size in component_sizes[:5]:
    if label == 0: continue
    print(f"Component {label}: {size} pixels")
