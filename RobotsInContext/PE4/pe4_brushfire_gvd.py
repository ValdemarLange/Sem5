"""
Det bare lækker kode - Bill Gates formentlig
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
    pixel_color = map[y, x]
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

# ----------------- Tilføjer obstacles langs kanten af mappet. Nødvendigt for GVD virker ------------------------------
def add_edges(map, maxx, maxy):
    for i in range(maxx-1): # bredden
        map[0][i] = (0,0,0) #ØVERST ?
        map[maxy-1][i] = (0,0,0)

    for j in range(maxy-1): # Højden
        map[j][0] = (0,0,0) # Venstre ?
        map[j][maxx-1] = (0,0,0) #Højre ?

    map[0][0] = (255,255,255)       # Fjern hjørner for simplere GVD.. ikke fortæl nogen
    map[0][maxx-1] = (255,255,255)
    map[maxy-1][0] = (255,255,255)
    map[maxy-1][maxx-1] = (255,255,255)
    
# ----------------- Brushfire metoden - Gemmer afstand til nærmeste obstacle i "matrix" vha. kø-system ----------------
def brushfire(map, maxx, maxy):

    queue = []
    
    matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    region_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]

    obstacle_index = 1
    directions = [(0,1),(0,-1),(1,0),(-1,0)] # op, ned, højre, venstre.... tror jeg... forkert, din spade

    for x in range(maxx): #bredden (x)
        for y in range(maxy): #højden ( y)
            if is_pixel_an_obstacle(map, x, y):
                matrix[y][x] = 1  # Marker som obstacle

                obstacle_neighbor = False

                for neighborx, neighbory in directions:
                    neighx, neighy = x + neighborx, y + neighbory

                    if 0 <= neighx < maxx and 0 <= neighy < maxy:
                        if matrix[neighy][neighx] > 0:  
                            obstacle_neighbor = True
                            region_matrix[y][x] = region_matrix[neighy][neighx]  # samme obstacle 
                            break

                if not obstacle_neighbor:
                    region_matrix[y][x] = obstacle_index
                    obstacle_index += 1
                    
                queue.append((y,x))
    
    while queue:
        current_pixel = queue.pop(0)
        current_y, current_x = current_pixel
        for stepx,stepy in directions: # nei = neighbor x/y
            neix = current_x + stepx
            neiy = current_y + stepy

            if 0 <= neix < maxx and 0 <= neiy < maxy:

                if matrix[neiy][neix] == 0:
                    matrix[neiy][neix] = matrix[current_y][current_x] + 1
                    region_matrix[neiy][neix] = region_matrix[current_y][current_x]
                    queue.append((neiy,neix))
    
    return matrix, region_matrix

# ----------------- Find sammenhængende obstacles og kald metoden til sammekobling ------------------------------------
def unify_regions(matrix, region_matrix, maxx, maxy):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Op, ned, højre, venstre

    for x in range(maxx):
        for y in range(maxy):
            if matrix[y][x] == 1:  # Dette er en obstacle pixel
                current_region = region_matrix[y][x]
                
                # Tjek naboer
                for neighbory, neighborx in directions:
                    neighy, neighx = y + neighbory, x + neighborx
                    
                    if 0 <= neighy < maxy and 0 <= neighx < maxx:
                        if matrix[neighy][neighx] == 1:  # Hvis naboen også er en obstacle
                            neighbor_region = region_matrix[neighy][neighx]
                            
                            # Hvis naboen har en anden region, foren regionerne
                            if current_region != neighbor_region:
                                # Funktion som går igennem matricen og ændrer region_matrix, så det matcher
                                merge_regions(region_matrix, current_region, neighbor_region, maxx, maxy)

# ----------------- Koble sammenhængende obstacles til samme region ---------------------------------------------------
def merge_regions(region_matrix, region1, region2, maxx, maxy):
    # Gennemløb hele matrixen og ændr alle pixels med region2 til region1
    for x in range(maxx):
        for y in range(maxy):
            if region_matrix[y][x] == region2:
                region_matrix[y][x] = region1

# ----------------- Visualiser brushfire matricen. Jo længere fra en obstacle jo mere rød :))  ------------------------
def visualize_matrix(matrix, maxx, maxy):
    color_map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    
    for x in range(maxx):
        for y in range(maxy):
            if matrix[y][x] == 1: # Obstacles skal være sort
                color_map[y, x] = (0, 0, 0)  
            else:
                distance = min(matrix[y][x]*1.5, 200) 
                color_map[y, x] = (200 - distance, 200 - distance, 255)  # Hvid til rød efter afstand til obstacle
    
    return color_map

# ----------------- Visualisere alle regionerne med farver samt grænselinjer (GVD roadmap) ----------------------------
def visualize_region_matrix(matrix, region_matrix, maxx, maxy):
    color_map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    voronoi_lines = np.zeros((maxy, maxx), dtype=np.uint8)
    
    farver = [          # Pastel farver
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
    (255, 210, 180)
]
    # Obstacles sort og farvelæg alle regionerne
    for x in range(maxx):
        for y in range(maxy):
            if matrix[y][x] == 1: # Obstacles skal være sort
                color_map[y, x] = (0, 0, 0)  
            else:
                color_map[y, x] = farver[region_matrix[y][x] % len(farver)]

    directions = [(0,1),(0,-1),(1,0),(-1,0)] # op, ned, højre, venstre.... tror jeg... Det faktisk højre, venstre, ned, op

    # Tegn stregerne op på grænserne mellem regioner samt gem deres koordinater i voronoi_lines
    for x in range(maxx):
        for y in range(maxy):
            for stepx,stepy in directions:
                neiy, neix = y+stepy, x+stepx
                if 0 <= neiy < maxy and 0 <= neix < maxx and region_matrix[y][x] != region_matrix[neiy][neix]:
                    color_map[y][x] = (60,60,60)
                    voronoi_lines[y][x] = 1

    return color_map, voronoi_lines

# ----------------- Finder den korteste direkte linje fra start/slut punkter til roadmappet ---------------------------
def find_near_vor(voronoi_lines, starty, startx, goaly, goalx, maxx, maxy, map):
    vor_x_s = 0
    vor_y_s = 0
    lowest_dist_s = maxx*maxy
    vor_x_e = 0
    vor_y_e = 0
    lowest_dist_e = maxx*maxy    

    for x in range(maxx):
        for y in range(maxy):
            if int(voronoi_lines[y, x]) == 1:
                dist = np.sqrt((y-starty) ** 2 + (x-startx) ** 2)
                dist_e = np.sqrt((y-goaly) ** 2 + (x-goalx) ** 2)
                if dist < lowest_dist_s:
                    vor_y_s = y
                    vor_x_s = x 
                    lowest_dist_s = dist
                if dist_e < lowest_dist_e:
                    vor_y_e = y
                    vor_x_e = x
                    lowest_dist_e = dist_e

    return vor_y_s, vor_x_s, vor_y_e, vor_x_e
                
# ----------------- Finder den korteste rute langs roadmappet og kalder visualisering af den --------------------------
def path_planner(voronoi_lines, starty, startx, goaly, goalx, maxx, maxy, map):
    path_start_y, path_start_x, path_goal_y, path_goal_x = find_near_vor(voronoi_lines, starty, startx, goaly, goalx, maxx, maxy, map)
    queue = []
    cell_visited = [[None for _ in range(maxx)] for _ in range(maxy)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Op, ned, højre, venstre


    queue.append((path_start_y, path_start_x))
    cell_visited[path_start_y][path_start_x] = (path_start_y, path_start_x) # Start forældre

    while queue:
        current_y, current_x = queue.pop(0)

        if (current_y, current_x) == (path_goal_y, path_goal_x):
            cv2.line(map, (startx,starty),(path_start_x,path_start_y),(0,0,255))
            cv2.line(map, (goalx,goaly),(path_goal_x,path_goal_y),(0,0,255))

            map_out = visualize_path(cell_visited, path_start_y, path_start_x, path_goal_y, path_goal_x, map)
            return map_out
       
        for stepy,stepx in directions: # nei = neighbor x/y
            neiy = current_y + stepy
            neix = current_x + stepx

            if 0 <= neiy < maxy and 0 <= neix < maxx:
                if voronoi_lines[neiy, neix] == 1 and cell_visited[neiy][neix] is None:
                    queue.append((neiy,neix))
                    cell_visited[neiy][neix] = (current_y, current_x)
                    
    print("no path")
    
    map_out = visualize_path(cell_visited, path_start_y, path_start_x, path_goal_y, path_goal_x, map)
    return map_out

# ----------------- Tegner faktisk ruten op langs voronoi linjerne ----------------------------------------------------
def visualize_path(cell_visited, starty, startx, goaly, goalx, map):
    current = (goaly, goalx)

    if cell_visited[goaly][goalx] is None:
        print("no path found.")
        return map

    while current != (starty, startx):
        map[current[0]][current[1]] = (255,0,0)
        current = cell_visited[current[0]][current[1]]

    return map

# ----------------- Indlæs / generer map ------------------------------------------------------------------------------
#map_file = 'prg_ex2_map.png'
#map_file = 'map_hestesko.png'
#map_image = read_map(map_file)
map_image = make_map(600, 500)
height, width, _ = map_image.shape

# ----------------- Udfør brushfire algoritemen og vis den i nyt vindue -----------------------------------------------
add_edges(map_image, width, height)
brushfire_matrix, region_matrix = brushfire(map_image, width, height)
brushfire_map = visualize_matrix(brushfire_matrix, width, height)
cv2.imshow('Brushfire Map', brushfire_map)
cv2.moveWindow('Brushfire Map', 100, 0)
cv2.waitKey(0)

# ----------------- Generer GVD udfra regioner og vis i nyt vindue ----------------------------------------------------
unify_regions(brushfire_matrix, region_matrix, width, height)
region_map, voronoi_lines = visualize_region_matrix(brushfire_matrix, region_matrix, width, height)
cv2.imshow('Region Map', region_map) 
cv2.moveWindow('Region Map', 125+width, 0)
cv2.waitKey(0)

# ----------------- Find korteste rute og vis den i nyt vindue ------------------------------
start = (25, 100) # y, x
goal = (505, 330)
path_map = path_planner(voronoi_lines, start[0], start[1], goal[0], goal[1], width, height, map_image)
cv2.imshow('Route Map', path_map)
cv2.moveWindow('Route Map', 150+2*width, 0)


cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()

