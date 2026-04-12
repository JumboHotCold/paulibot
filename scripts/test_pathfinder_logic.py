import cv2
import numpy as np
import heapq
from scipy.spatial import cKDTree

def generate_walkable_mask(pathway_img_path):
    """
    Step 1 & 2: Color Isolation & Binary Grid Creation
    Reads the pathway image, isolates the exact green pathways, and creates a binary grid.
    """
    img = cv2.imread(pathway_img_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {pathway_img_path}")
        
    # Convert to HSV for better color thresholding
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # We found the pure green was RGB(29, 121, 6)
    # The corresponding HSV in OpenCV is roughly H: ~54, S: ~243, V: ~121
    # We create a tight boundary around this specific green
    lower_green = np.array([45, 150, 50])
    upper_green = np.array([75, 255, 255])
    
    # Mask will be 255 for green pixels, 0 for everything else
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Binary grid (1 for walkable, 0 for impassable)
    binary_grid = (mask > 0).astype(np.uint8)
    return binary_grid

def snap_to_grid(binary_grid, point_y, point_x):
    """
    Step 4a: Snapping
    If the requested point is 0, snap it to the nearest 1.
    """
    if binary_grid[point_y, point_x] == 1:
        return (point_y, point_x)
        
    # Find all walkable coordinates
    walkable_y, walkable_x = np.nonzero(binary_grid)
    if len(walkable_y) == 0:
        raise ValueError("No walkable paths found on the map.")
        
    points = np.column_stack((walkable_y, walkable_x))
    tree = cKDTree(points)
    
    # Query nearest neighbor
    distance, index = tree.query([point_y, point_x])
    snapped_y, snapped_x = points[index]
    
    return int(snapped_y), int(snapped_x)

def run_dijkstra(binary_grid, start, end):
    """
    Step 3 & 4b: Strict Graph Building & Path Calculation using Custom Dijkstra (A*)
    """
    start = snap_to_grid(binary_grid, start[0], start[1])
    end = snap_to_grid(binary_grid, end[0], end[1])
    
    # Priority Queue for A* / Dijkstra: (cost, current_y, current_x, path)
    pq = [(0, start[0], start[1], [])]
    
    # Visited set
    visited = set()
    visited.add((start[0], start[1]))
    
    # Allowed movements: strict 4-way to avoid diagonal clipping through 0s
    # Even if 8-way is requested, strict 4-way guarantees no "corner cutting" across boundaries
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Optional 8-way with STRICT checking for touching 0s
    diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    rows, cols = binary_grid.shape
    
    # For A* heuristic
    def heuristic(y, x):
        return np.sqrt((y - end[0])**2 + (x - end[1])**2)
        
    # Best cost dictionary to avoid pushing worse paths
    best_cost = { (start[0], start[1]): 0 }
    
    while pq:
        cost, y, x, path = heapq.heappop(pq)
        
        current_path = path + [(y, x)]
        if (y, x) == end:
            return current_path
            
        # 4-way checks
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and binary_grid[ny, nx] == 1:
                new_cost = cost + 1
                if new_cost < best_cost.get((ny, nx), float('inf')):
                    best_cost[(ny, nx)] = new_cost
                    heapq.heappush(pq, (new_cost, ny, nx, current_path))
                    
        # 8-way diagonal checks (Do not allow diagonal connection if it touches a 0)
        for dy, dx in diagonals:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and binary_grid[ny, nx] == 1:
                # To move diagonally from (y,x) to (ny,nx), both adjacent orthogonal pixels must be 1
                if binary_grid[y, nx] == 1 and binary_grid[ny, x] == 1:
                    new_cost = cost + 1.414 # sqrt(2)
                    if new_cost < best_cost.get((ny, nx), float('inf')):
                        best_cost[(ny, nx)] = new_cost
                        heapq.heappush(pq, (new_cost, ny, nx, current_path))
                        
    return [] # No path found

def draw_path_on_map(base_map_path, path_coords, output_path):
    """
    Step 5: Visual Overlay
    Draws the path as a thick red line on the base map.
    """
    img = cv2.imread(base_map_path)
    if img is None or len(path_coords) == 0:
        return False
        
    # OpenCv uses (X, Y) for drawing, but our coords are (Y, X)
    pts = np.array([(x, y) for y, x in path_coords], np.int32)
    pts = pts.reshape((-1, 1, 2))
    
    # Draw a thick red line (BGR: 0, 0, 255)
    cv2.polylines(img, [pts], isClosed=False, color=(0, 0, 255), thickness=10)
    
    cv2.imwrite(output_path, img)
    return True

if __name__ == "__main__":
    # Define paths
    pathway_map = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_PATHWAY.png"
    base_map = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP (1).png"
    output_result = r"C:\Dex\CAPSTONE\paulibot\images\2D_Mapping\ST.PAUL MAP_RESULT.png"
    
    print("Generating mask...")
    grid = generate_walkable_mask(pathway_map)
    walkable_count = np.sum(grid)
    print(f"Mask generated. Found {walkable_count} walkable pixels.")
    
    # We will pick two random points to test, or some hardcoded points 
    # that are usually inside the map (we'll snap them anyway)
    start_point = (500, 500)  # (Y, X)
    end_point = (2000, 2000)  # (Y, X)
    
    # Let's dynamically pick the top-most walkable and bottom-most walkable pixel for a long path
    walkable_y, walkable_x = np.nonzero(grid)
    st = (walkable_y[0], walkable_x[0])
    en = (walkable_y[-1], walkable_x[-1])
    
    print(f"Calculating route from {st} to {en}...")
    path = run_dijkstra(grid, st, en)
    
    if path:
        print(f"Path found! Length: {len(path)} pixels. Overlaying on base map...")
        draw_path_on_map(base_map, path, output_result)
        print(f"Saved result to {output_result}")
    else:
        print("No path could be found.")
