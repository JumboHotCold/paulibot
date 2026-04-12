import cv2
import numpy as np
import heapq

def skeletonize_mask(binary_grid):
    """
    Reduces the thick green pathways into a 1-pixel wide skeleton to force
    routing along the precise CENTER of the roads.
    """
    # Skeletonize using OpenCV morphological operations
    # First, close small holes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.morphologyEx(binary_grid * 255, cv2.MORPH_CLOSE, kernel)
    
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    done = False
    
    # Standard morphological skeletonization
    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        
        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
            
    # Dilate the skeleton slightly so it allows some diagonal movements/robustness
    # (A 1-pixel skeleton can sometimes break continuous 8-way paths)
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    skel_thick = cv2.dilate(skel, kernel_dilate)
    
    return (skel_thick > 0).astype(np.uint8)

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array([45, 100, 40])
upper_green = np.array([75, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
binary_grid = (mask > 0).astype(np.uint8)

# Run Skeletonization
skeleton_grid = skeletonize_mask(binary_grid)

# Save visualization of the skeleton
cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_SKELETON.png", skeleton_grid * 255)
print("Skeleton grid generated with", np.sum(skeleton_grid > 0), "walkable pixels.")
