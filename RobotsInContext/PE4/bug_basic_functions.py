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
    num_obstacles = 10
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
# map_file = 'prg_ex2_map.png'
# map_image = read_map(map_file)

# make your own map
#random_map = make_map(200, 200)


# Obstacle checking
# x, y = 100, 100  # Replace with your coordinates
# if is_pixel_an_obstacle(random_map, x, y):
#     print(f"Pixel at ({x}, {y}) is black (obstacle)")
# else:
#     print(f"Pixel at ({x}, {y}) is white (free space)")

def add_edges(map, maxx, maxy):
    for i in range(maxx-2):
        map[0][i+1] = (0,0,0)
        map[maxy-1][i+1] = (0,0,0)

    for j in range(maxy-2):
        map[j+1][0] = (0,0,0)
        map[j+1][maxx-1] = (0,0,0) 

def brushfire(map, maxx, maxy):

    queue = []


    # Initialize matrix with 0s (no obstacles)
    matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    region_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]

    obstacle_index = 1
    directions = [(0,1),(0,-1),(1,0),(-1,0)] # op, ned, højre, venstre.... tror jeg

    # Loop through a specific region and update the matrix
    for i in range(maxx):
        for j in range(maxy):
            if is_pixel_an_obstacle(map, i, j):
                matrix[i][j] = 1  # Mark as obstacle

                obstacle_neighbor = False

                for neighborx, neighbory in directions:
                    neighx, neighy = i + neighborx, j + neighbory

                    if 0 <= neighx < maxx and 0 <= neighy < maxy:
                        if matrix[neighx][neighy] > 0:  # Already labeled as obstacle
                            obstacle_neighbor = True
                            region_matrix[i][j] = region_matrix[neighx][neighy]  # Assign same obstacle label
                            break

                if not obstacle_neighbor:
                    region_matrix[i][j] = obstacle_index
                    obstacle_index += 1
                    
                queue.append((i,j))
    
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
                    region_matrix[neix][neiy] = region_matrix[current_x][current_y]
                    queue.append((neix,neiy))
    
    return matrix, region_matrix

def unify_regions(matrix, region_matrix, maxx, maxy):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Op, ned, højre, venstre

    for i in range(maxx):
        for j in range(maxy):
            if matrix[i][j] == 1:  # Dette er en obstacle pixel
                current_region = region_matrix[i][j]
                
                # Tjek naboer
                for neighborx, neighbory in directions:
                    neighx, neighy = i + neighborx, j + neighbory
                    
                    if 0 <= neighx < maxx and 0 <= neighy < maxy:
                        if matrix[neighx][neighy] == 1:  # Hvis naboen også er en obstacle
                            neighbor_region = region_matrix[neighx][neighy]
                            
                            # Hvis naboen har en anden region, foren regionerne
                            if current_region != neighbor_region:
                                # Funktion som går igennem matricen og ændrer region_matrix, så det matcher
                                merge_regions(region_matrix, current_region, neighbor_region, maxx, maxy)

def merge_regions(region_matrix, region1, region2, maxx, maxy):
    # Gennemløb hele matrixen og ændr alle pixels med region2 til region1
    for i in range(maxx):
        for j in range(maxy):
            if region_matrix[i][j] == region2:
                region_matrix[i][j] = region1

# Function to visualize the matrix with colors based on distance
def visualize_matrix(matrix, maxx, maxy):
    color_map = np.zeros((maxx, maxy, 3), dtype=np.uint8)
    
    for i in range(maxx):
        for j in range(maxy):
            if matrix[i][j] == 1: # Obstacles skal være sort
                color_map[i, j] = (0, 0, 0)  
            else:
                distance = min(matrix[i][j]*3, 200) 
                color_map[i, j] = (200 - distance, 200 - distance, 255)  # Hvid til rød efter afstand til obstacle
    
    # Return the color map image
    return color_map

def visualize_region_matrix(region_matrix, maxx, maxy):
    color_map = np.zeros((maxx, maxy, 3), dtype=np.uint8)
    farver = [
    # # Pastel:
    (150, 200, 150),
    (150, 180, 255),
    (255, 255, 150),
    (255, 150, 255),
    (150, 255, 255),
    (255, 180, 200),
    (180, 150, 255),
    (180, 220, 255),
    (255, 200, 150),
    (200, 255, 180),
    (255, 160, 160),
    (180, 255, 200),
    (220, 190, 255),
    # # Kamo
    # (107, 142, 35),
    # (85, 107, 47),
    # (210, 180, 140),
    # (244, 164, 96),
    # (34, 139, 34),
    # (139, 69, 19),
    # (240, 230, 140),
    # (189, 183, 107),
    # (85, 107, 47),
    # (75, 83, 32)
]
    
    for i in range(maxx):
        for j in range(maxy):
            if matrix[i][j] == 1: # Obstacles skal være sort
                color_map[i, j] = (0, 0, 0)  
            else:
                region = region_matrix[i][j] 
                color_map[i, j] = farver[region % len(farver)]

    directions = [(0,1),(0,-1),(1,0),(-1,0)] # op, ned, højre, venstre.... tror jeg


    for i in range(maxx):
        for j in range(maxy):
            for stepx,stepy in directions:
                x, y = i+stepx, j+stepy
                if 0 <= x < maxx and 0 <= y < maxy and region_matrix[x][y] != region_matrix[i][j]:
                    color_map[i][j] = (255,255,255)

    # Return the color map image
    return color_map

sizex = 500
sizey = 500

my_map = make_map(500,500)


add_edges(my_map, sizex, sizey)

matrix, region_matrix = brushfire(my_map, sizex, sizey)

#add_edges(matrix, region_matrix, 300, 300)
unify_regions(matrix, region_matrix, sizex, sizey)

# Visualize the matrix
visualized_map = visualize_matrix(matrix, sizex, sizey)
region_map = visualize_region_matrix(region_matrix, sizex, sizey)

# Resize the image for visualization (increase scale by 2x)
scale_factor = 3
resized_brushfire_map = cv2.resize(visualized_map, (visualized_map.shape[1] * scale_factor, visualized_map.shape[0] * scale_factor), interpolation=cv2.INTER_NEAREST)
resized_region_map = cv2.resize(region_map, (region_map.shape[1] * scale_factor, region_map.shape[0] * scale_factor), interpolation=cv2.INTER_NEAREST)


# Create a named window
cv2.namedWindow('Brushfire map', cv2.WINDOW_NORMAL)
# Optionally, resize the window
cv2.resizeWindow('Brushfire map', 950, 950)  # Or use the dimensions you want
# Show the resized image
cv2.imshow('Brushfire map', resized_brushfire_map)

cv2.namedWindow('Region / GVD', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Region / GVD', 950, 950)  # Or use the dimensions you want
cv2.imshow('Region / GVD', resized_region_map)
cv2.waitKey(0)  # Wait until a key is pressed
cv2.destroyAllWindows()


# Mark a pixel on the map
#new_map = mark_pixel(random_map, x, y)
#cv2.namedWindow('Marked_Map', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Marked_Map', 300, 300) # resize the map window if necessary for marked pixels to be visible
#cv2.imshow('Marked_Map', new_map)
cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()