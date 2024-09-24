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
    pixel_color = map[x, y]
    # returns true if the pixel is black or close to black
    return np.all(pixel_color < 20)


def mark_pixel(map, x, y):
    # Make a copy of the map to avoid modifying the original image - if needed
    marked_map = map.copy()
    red = (0, 0, 255)
    marked_map[x, y] = red  
    return marked_map

def place_obstacle_pixel(map, x, y):
    # Make a copy of the map to avoid modifying the original image - if needed
    marked_map = map.copy()
    black = (0, 0, 0)
    marked_map[x, y] = black  
    return marked_map

# How to use:
# Read the map
#map_file = 'prg_ex2_map.png'
#map_image = read_map(map_file)

# make your own map
#random_map = make_map(200, 200)


# Obstacle checking
# x, y = 100, 100  # Replace with your coordinates
# if is_pixel_an_obstacle(random_map, x, y):
#     print(f"Pixel at ({x}, {y}) is black (obstacle)")
# else:
#     print(f"Pixel at ({x}, {y}) is white (free space)")

def brushfire(map, maxx, maxy):

    queue = []


    # Initialize matrix with 0s (no obstacles)
    matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]

    # Loop through a specific region and update the matrix
    for i in range(maxx):
        for j in range(maxy):
            if is_pixel_an_obstacle(map, i, j):
                matrix[i][j] = 1  # Mark as obstacle
                queue.append((i,j))

    # pixel test
    matrix[1][10] = 1
    queue.append((1,10))

    directions = [(0,1),(0,-1),(1,0),(-1,0)] # op, ned, højre, venstre.... tror jeg

    while queue:
        current_pixel = queue.pop(0)
        current_x, current_y = current_pixel
        #print(current_x, current_y)
        for stepx,stepy in directions: # nei = neighbor x/y
            neix = current_x + stepx
            neiy = current_y + stepy

            if 0 <= neix < maxx and 0 <= neiy < maxy:

                if matrix[neix][neiy] == 0:
                    matrix[neix][neiy] = matrix[current_x][current_y] + 1
                    queue.append((neix,neiy))
    
    return matrix

# Function to visualize the matrix with colors based on distance
def visualize_matrix(matrix, maxx, maxy):
    # Get the maximum value in the matrix (for normalization)
    max_value = np.max(matrix)
    
    # Create an empty image with 3 color channels (RGB)
    color_map = np.zeros((maxx, maxy, 3), dtype=np.uint8)
    
    # Normalize the matrix values to the range [0, 255] and map them to colors
    for i in range(maxx):
        for j in range(maxy):
            # Normalize the matrix value to a grayscale intensity (0-255)
            if matrix[i][j] == 1:
                color_map[i, j] = (0, 0, 0)  # Obstacles are black
            else:
                intensity = int((matrix[i][j] / max_value) * 255)
                color_map[i, j] = (255 - intensity, 255 - intensity, 255)  # White to black gradient
    
    # Return the color map image
    return color_map

my_map = make_map(300,300)

matrix = brushfire(my_map, 300, 300)

# Visualize the matrix
visualized_map = visualize_matrix(matrix, 300, 300)

# Display the visualized map
cv2.imshow('Brushfire Visualization', visualized_map)


# Mark a pixel on the map
#new_map = mark_pixel(random_map, x, y)
#cv2.namedWindow('Marked_Map', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Marked_Map', 300, 300) # resize the map window if necessary for marked pixels to be visible
#cv2.imshow('Marked_Map', new_map)
cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()