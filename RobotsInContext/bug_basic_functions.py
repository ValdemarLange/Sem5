"""
Building block functions to use for the bug algorithm
read map from image
make your own map with randomly generate obstacles
query whether a pixel is white or black (traversable or obstacle)
mark the pixel a different colour to show goal, trajectory, etc.
"""
import cv2
# if you have trouble with importing cv2, you might have an outdated version of numpy that does not agree with cv2. try running "pip install --upgrade numpy" in a terminal and then run again.
import numpy as np

def read_map(file):
    # Read the color map image
    map_image = cv2.imread(file)
    
    # View map - comment out if viewing is not necessary
    cv2.imshow("Map", map_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return map_image


def make_map(height, width):
    map_image = np.ones((height, width, 3), dtype=np.uint8) * 255
    num_obstacles = 5
    obstacle_size = 40  # Size of each square obstacle
    for _ in range(num_obstacles):
        # Generate random coordinates for the obstacle
        x = np.random.randint(0, width - obstacle_size)
        y = np.random.randint(0, height - obstacle_size)
        
        # Draw the obstacle on the map
        map_image[y:y+obstacle_size, x:x+obstacle_size] = (0, 0, 0)
    cv2.imshow("Generated Map", map_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return map_image


def is_pixel_an_obstacle(map, x, y):
    # Get the pixel color at coordinates (x, y)
    pixel_color = map[y, x]
    # returns true if the pixel is black or close to black
    return np.all(pixel_color < 20)


def mark_pixel(map, x, y):
    # Make a copy of the map to avoid modifying the original image - if needed
    marked_map = map.copy()
    red = (0, 0, 255)
    marked_map[x, y] = red  
    return marked_map


# How to use:
# Read the map
map_file = 'prg_ex2_map.png'
map_image = read_map(map_file)

# make your own map
random_map = make_map(200, 200)


# Obstacle checking
x, y = 100, 100  # Replace with your coordinates
if is_pixel_an_obstacle(random_map, x, y):
    print(f"Pixel at ({x}, {y}) is black (obstacle)")
else:
    print(f"Pixel at ({x}, {y}) is white (free space)")

start_point = [50,50]
end_point = [150,150]




# Mark a pixel on the map
new_map = mark_pixel(random_map, x, y)
cv2.namedWindow('Marked_Map', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Marked_Map', 800, 800) # resize the map window if necessary for marked pixels to be visible
cv2.imshow('Marked_Map', new_map)
cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()