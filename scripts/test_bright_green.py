import cv2
import numpy as np

img_path = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
img = cv2.imread(img_path)

if img is not None:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3)
    
    # Let's find pixels where Green is dominant
    # G > 200, R < 100, B < 100 typically means a very bright green used for markup
    mask = (pixels[:, 1] > 180) & (pixels[:, 0] < 100) & (pixels[:, 2] < 100)
    bright_green_pixels = pixels[mask]
    
    from collections import Counter
    counts = Counter(map(tuple, bright_green_pixels))
    
    print("Most common BRIGHT MARKUP GREEN colors:")
    for color, count in counts.most_common(5):
        print(f"Color: {color}, Count: {count}")
    
    total = np.sum(mask)
    print("Total bright green pixels:", total)
    
    # Save a test mask
    mask_2d = mask.reshape(img.shape[:2]).astype(np.uint8) * 255
    cv2.imwrite(r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\DEBUG_BRIGHT_GREEN.png", mask_2d)
