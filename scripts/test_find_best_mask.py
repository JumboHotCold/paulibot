import cv2
import numpy as np

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
base_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP (1).png"

img = cv2.imread(img_path)
base = cv2.imread(base_path)

# Let's perform an ABSOLUTE difference, but only keep pixels that are distinctly GREEN
diff = cv2.absdiff(img, base)
# Convert diff to grayscale to see the magnitude of change
gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

# Threshold to find pixels that actually changed
_, changed_mask = cv2.threshold(gray_diff, 10, 255, cv2.THRESH_BINARY)

# Now, out of all changed pixels, which ones are green in the pathway image?
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Grass HSV: [54, 242, 121]
# We want anything that is green but NOT the grass.
# Or, let's just use the strict HSV of the changed pixels!!!
changed_hsv = hsv[changed_mask > 0]
if len(changed_hsv) > 0:
    median_h = np.median(changed_hsv[:, 0])
    median_s = np.median(changed_hsv[:, 1])
    median_v = np.median(changed_hsv[:, 2])
    print(f"Median HSV of drawn lines: H={median_h}, S={median_s}, V={median_v}")
    
    # We can create a mask around this median!
    lower = np.array([max(0, median_h - 15), max(0, median_s - 50), max(0, median_v - 50)])
    upper = np.array([min(179, median_h + 15), min(255, median_s + 50), min(255, median_v + 50)])
    
    final_mask = cv2.inRange(hsv, lower, upper)
    
    # Let's also intersect it with the `changed_mask` just in case
    # This guarantees we ONLY get the manually drawn lines!
    strict_drawn_pathway = cv2.bitwise_and(final_mask, changed_mask)
    
    print("Drawn pathway pixels:", np.sum(strict_drawn_pathway > 0))
    cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_TRUE_PATH_MASK.png", strict_drawn_pathway)
