import cv2
import numpy as np
from collections import Counter

img = cv2.imread(r'C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png')
if img is None:
    print("Could not load image.")
else:
    # Convert to RGB (OpenCV uses BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Let's count pixel colors to find the exact green
    pixels = img_rgb.reshape(-1, 3)
    counts = Counter(map(tuple, pixels))
    
    print("Most common colors:")
    for color, count in counts.most_common(10):
        print(f"Color: {color}, Count: {count}")
    
