import cv2
import numpy as np

img = cv2.imread(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_SKELETON.png", 0)
num_labels, labels = cv2.connectedComponents(img)

print(f"Number of connected components: {num_labels}")

# Count sizes
unique, counts = np.unique(labels, return_counts=True)
component_sizes = sorted(zip(unique, counts), key=lambda x: x[1], reverse=True)

print("Top component sizes (pixels):")
for label, size in component_sizes[:10]:
    if label == 0: continue # background
    print(f"Component {label}: {size} pixels")

# Check where our test points landed
# start_x=2754, start_y=620 -> labels[620, 2754]
# end_x=2117, end_y=1782 -> labels[1782, 2117]

if 0 <= 620 < labels.shape[0] and 0 <= 2754 < labels.shape[1]:
    start_label = labels[620, 2754]
    print(f"Start point label: {start_label}")
else:
    print("Start point out of bounds")

if 0 <= 1782 < labels.shape[0] and 0 <= 2117 < labels.shape[1]:
    end_label = labels[1782, 2117]
    print(f"End point label: {end_label}")
else:
    print("End point out of bounds")
