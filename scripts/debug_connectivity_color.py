import cv2
import numpy as np

# Load the mask as it is generated in the engine
img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([40, 50, 40])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
binary_grid = (mask > 0).astype(np.uint8)

gap_bridge_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
img_closed = cv2.morphologyEx(binary_grid * 255, cv2.MORPH_CLOSE, gap_bridge_kernel)

num_labels, labels = cv2.connectedComponents(img_closed)
print(f"Number of connected components after bridging: {num_labels}")

# Check our test points
# start_x=2754, start_y=620
# end_x=2117, end_y=1782
s_x, s_y = 2754, 620
e_x, e_y = 2117, 1782

def snap(x, y, labels):
    if labels[y, x] != 0:
        return x, y, labels[y, x]
    
    # Simple search for nearest label
    walkable_y, walkable_x = np.nonzero(labels)
    dist = (walkable_y - y)**2 + (walkable_x - x)**2
    idx = np.argmin(dist)
    return walkable_x[idx], walkable_y[idx], labels[walkable_y[idx], walkable_x[idx]]

sx, sy, sl = snap(s_x, s_y, labels)
ex, ey, el = snap(e_x, e_y, labels)

print(f"Start snapped to: ({sx}, {sy}) with Label={sl}")
print(f"End snapped to: ({ex}, {ey}) with Label={el}")

# Save colorized components
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
labeled_img[labels == 0] = 0

cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_COMPONENTS_COLOR.png", labeled_img)
