"""
Det bare lækker kode - Bill Gates formentlig
"""
import cv2
# if you have trouble with importing cv2, you might have an outdated version of numpy that does not agree with cv2. try running "pip install --upgrade numpy" in a terminal and then run again.
import numpy as np

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
directions_diag = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Alle naboer

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

# --------------- Tjek om den lige linje mellem punkterne er fri for obstacles --------------------------------------
def is_line_clear(x1, y1, x2, y2):
    temp_map = np.zeros((height, width), dtype=np.uint8)
    cv2.line(temp_map, (x1,y1), (x2,y2),1,1)
    points = np.argwhere(temp_map == 1)

    for point in points:
        if is_pixel_an_obstacle(map_image, point[1], point[0]):
            return False
    return True

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

# ----------------- Tilføjer obstacles langs kanten af mappet. Nødvendigt for GVD virker ------------------------------------
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
    
# ----------------- Identificer sammenhængende obstacles og tildem dem indx nr. Vha. nabo søgning i kø system ----------------
def identify_obstacles(map, maxx, maxy):
    obstacle_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    obstacle_index = 1

    for x in range(maxx):
        for y in range(maxy):
            if is_pixel_an_obstacle(map, x, y) and obstacle_matrix[y][x] == 0: # obstacle_matrix == 0, hvis den ikke er hører til en obstacle endnu.
                queue = [(y, x)]
                obstacle_matrix[y][x] = obstacle_index

                while queue:    # Når queue er tom, så der ikke flere sammenhængende obstacle pixels
                    current_y, current_x = queue.pop(0)
                    for dx, dy in directions:
                        nx, ny = current_x + dx, current_y + dy
                        if 0 <= nx < maxx and 0 <= ny < maxy:
                            if is_pixel_an_obstacle(map, nx, ny) and obstacle_matrix[ny][nx] == 0:
                                obstacle_matrix[ny][nx] = obstacle_index
                                queue.append((ny, nx))
                
                obstacle_index += 1

    return obstacle_matrix  # Map grid hvor celler har en værdi med deres obstacle index. Ellers 0

# ---------------- Brushfire udfra obstacles, samt regions kort ---------------------------------------------------------
def brushfire_from_obstacles(obstacle_matrix, maxx, maxy):
    """
    Udfører Brushfire-algoritmen med spredning ud fra obstacles.
    """
    queue = []
    brushfire_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    region_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    
    # Smid obstacles i køen og region_matrix
    for x in range(maxx):
        for y in range(maxy):
            if obstacle_matrix[y][x] > 0:  # Hvis dette er en obstacle pixel (ID > 0)
                brushfire_matrix[y][x] = 1
                region_matrix[y][x] = obstacle_matrix[y][x]  # Brug obstacle ID som region ID
                queue.append((y, x))

    # Brushfire-algoritmen
    while queue:
        current_y, current_x = queue.pop(0)
        for dx, dy in directions:   # Loop igennem alle naboer
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < maxx and 0 <= ny < maxy:   # Indenfor mappet
                if brushfire_matrix[ny][nx] == 0:  # Hvis pixel ikke allerede er besøgt
                    brushfire_matrix[ny][nx] = brushfire_matrix[current_y][current_x] + 1
                    region_matrix[ny][nx] = region_matrix[current_y][current_x]  # Arv region ID
                    queue.append((ny, nx))

    return brushfire_matrix, region_matrix

# ----------------- Visualiser brushfire matricen. Jo længere fra en obstacle jo mere rød :))  ------------------------
def visualize_brushfire(brushfire_matrix, maxx, maxy):
    brushfire_map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    
    for x in range(maxx):
        for y in range(maxy):
            if brushfire_matrix[y][x] == 1: # Obstacles skal være sort
                brushfire_map[y, x] = (0, 0, 0)  
            else:
                distance = min(brushfire_matrix[y][x]*1.5, 200) 
                brushfire_map[y, x] = (200 - distance, 200 - distance, 255)  # Hvid til rød efter afstand til obstacle
    
    return brushfire_map


# ---------------- Finder lokale maxima ud fra brushfire matricen --------------------------------------------------------
def find_local_maxima(brushfire_matrix, maxx, maxy):
    voronoi_lines = np.zeros((maxy, maxx), dtype=np.uint8)

    for x in range(1, maxx - 1):  # Undgå kanterne
        for y in range(1, maxy - 1):  # Undgå kanterne
            current_value = brushfire_matrix[y][x]
            higher_than_neighbors = 0   # Tæl antallet af naboer som den er højere end
            lower_than_neighbors = 0    # Tæl antallet af naboer som den er lavere end

            for dx, dy in directions:   # loop gennem naboer og sammenlign deres værdi
                nx, ny = x + dx, y + dy
                if 0 <= nx < maxx and 0 <= ny < maxy:
                    neighbor_value = brushfire_matrix[ny][nx]
                    if current_value > neighbor_value:
                        higher_than_neighbors += 1
                    elif current_value < neighbor_value:
                        lower_than_neighbors += 1

            # Maksimum, hvis det er højere end mindst 1 nabo og ikke er er lavere end nogen naboer
            if higher_than_neighbors >= 1 and lower_than_neighbors ==  0: # 
                voronoi_lines[y][x] = 1     # maksimum skal være en del af voronoi linjerne.

    return voronoi_lines

# --------------- Tegner voronoi linjer ud fra regioner og tilføjer voronoi linjer fra lokale maxima, som røde linjer ----
def draw_color_map(brushfire_matrix, voronoi_lines, region_matrix, maxx, maxy):
    farver = [          # Pastel farver til regioner
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
    (255, 210, 180)]

    color_map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    for x in range(maxx):
        for y in range(maxy):
            if brushfire_matrix[y][x] == 1: # If obstacle => sort
                color_map[y][x] = (0,0,0)
            elif voronoi_lines[y][x] == 1:  # Voronoi-linje => rød
                color_map[y][x] = (0, 0, 255)  
            else:
                color_map[y][x] = farver[region_matrix[y][x] % len(farver)] # ellers tildel regions farve
            
            for stepx,stepy in directions: # Tjek om det regions grænse, i så fald => grå og tilføj til voronoi_lines mappet.
                neiy, neix = y+stepy, x+stepx
                if 0 <= neiy < maxy and 0 <= neix < maxx and region_matrix[y][x] != region_matrix[neiy][neix]:
                    color_map[y][x] = (60,60,60)
                    voronoi_lines[y][x] = 1

    return color_map

# ----------------- Find yderste koordinater af røde strukture i voronoi diagrammet ------------------------------------------
def find_edge_red(color_map, maxx, maxy):
    """
    Finder alle strukturer af røde pixels og returnerer koordinaterne for:
    - Den røde pixel med laveste x
    - Den røde pixel med højeste x
    - Den røde pixel med laveste y
    - Den røde pixel med højeste y
    En sammenhængende gruppe af røde pixel = en structure.
    """
    visited = np.zeros((maxy, maxx), dtype=bool)  # Marker hvilke pixels der er besøgt
    
    structures = []  # til at gemme koordinater af yder pixels

    for y in range(maxy):
        for x in range(maxx):
            if np.array_equal(color_map[y, x], (0, 0, 255)) and not visited[y, x]: # Tjek om pixel er rød og ikke besøgt (ny structure)
                queue = [(x, y)]
                visited[y, x] = True  # Marker pixel som besøgt
                structure_points = [(x, y)]  # Gem koordinater i denne struktur

                while queue:    # Kø for kun den ene struktur
                    cx, cy = queue.pop(0)
                    for dx, dy in directions_diag:      # Find naboer, der ikke er besøgt
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < maxx and 0 <= ny < maxy:
                            if np.array_equal(color_map[ny, nx], (0, 0, 255)) and not visited[ny, nx]:
                                queue.append((nx, ny))
                                visited[ny, nx] = True
                                structure_points.append((nx, ny))

                # Beregn yder punkter for structuren
                min_x_coord = min(structure_points, key=lambda p: p[0])
                max_x_coord = max(structure_points, key=lambda p: p[0])
                min_y_coord = min(structure_points, key=lambda p: p[1])
                max_y_coord = max(structure_points, key=lambda p: p[1])

                # Tilføj resultater for denne struktur
                structures.append({min_x_coord, min_y_coord, max_x_coord, max_y_coord})

    return structures

def find_near_vor(map, x, y, color):
    """
    Finder det nærmeste punkt på Voronoi-linjen.
    """
    if color:
        voronoi_points = np.argwhere(np.all(map == (60, 60, 60),-1))
    else:
        voronoi_points = np.argwhere(map == 1)

    # Beregn afstande til alle Voronoi-punkter
    distances = np.sqrt((voronoi_points[:, 0] - y)**2 + (voronoi_points[:, 1] - x)**2)
    closest_index = np.argmin(distances)  # Find det tætteste punkt

    return voronoi_points[closest_index][1], voronoi_points[closest_index][0]  # Returner som (vx, vy)

# ------------------- Forsøg at forbind de funde structures til hinanden og derefter til roadmap fra regions grænse ----------------
def connect_structures(color_map, structures, voronoi_lines, maxx, maxy):
    """
    Forbinder strukturer til hinanden og derefter til nærmeste Voronoi-linje.
    """
    def find_nearest(structure1, structure2):
        """
        Find det nærmeste par af punkter mellem to strukturer.
        """
        min_dist = float("inf")
        closest_pair = None

        for c1 in structure1:
            for c2 in structure2:
                dist = np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (c1, c2)

        return closest_pair
    
    # Første del: Forbind alle strukturer til hinanden hvis muligt
    connected_pairs = set()
    for i, struct1 in enumerate(structures):
        for j, struct2 in enumerate(structures):
            if i != j and (i, j) not in connected_pairs and (j, i) not in connected_pairs: # Hvis ikke: samme eller allerede forbundet par
                closest_pair = find_nearest(struct1, struct2)
                if closest_pair:
                    (x1, y1), (x2, y2) = closest_pair
                    if is_line_clear(x1, y1, x2, y2):
                        # print(f"Forbinder struct {i} og struct {j}: ({x1}, {y1}) -> ({x2}, {y2})")
                        cv2.line(color_map, (x1, y1), (x2, y2), (255, 0, 0), 1)  # Blå linje
                        cv2.line(voronoi_lines, (x1, y1), (x2, y2), 1, 1)
                        connected_pairs.add((i, j))

    # Anden del: Forbind alle strukturer til Voronoi-linjerne
    for struct in structures:
        for coords in struct:
            # Find nærmeste Voronoi-linje punkt
            vx, vy = find_near_vor(color_map,coords[0], coords[1], True)

            # Tjek, om der er en klar linje
            if is_line_clear(coords[0], coords[1], vx, vy):
                # print(f"Forbinder til Voronoi: ({coords[0]}, {coords[1]}) -> ({vx}, {vy})")
                cv2.line(color_map, (coords[0], coords[1]), (vx, vy), (0, 255, 0), 1)  # Grøn linje
                cv2.line(voronoi_lines, (coords[0], coords[1]), (vx, vy), 1, 1)  # Opdater Voronoi-linjer
                break                    
    
    # Tredje del: Lav røde, grønne og blå streger om til almindelig grå voronoi linjer
    for x in range(maxx):
        for y in range(maxy):
            if np.array_equal(color_map[y, x], (0,255,0)) or np.array_equal(color_map[y, x], (0, 0, 255)) or np.array_equal(color_map[y, x], (255, 0, 0)):
                color_map[y, x] = (60, 60, 60)

# ----------------- returnere et map, hvor voronoi_lines er tegnet op med rød -------------------------------------------------------
def visualize_voronoi(voronoi_lines, maxx, maxy):
    map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    
    for x in range(maxx):
        for y in range(maxy):
            if voronoi_lines[y][x] == 1:
                map[y, x] = (0, 0, 255)  
        
    return map


# ----------------- Finder den korteste rute langs roadmappet og kalder visualisering af den --------------------------
def path_planner(voronoi_lines, starty, startx, goaly, goalx, maxx, maxy, map):
    path_start_x, path_start_y = find_near_vor(voronoi_lines, startx, starty, False) # Find nærmeste punkt på roadmappet til startpunktet
    path_goal_x, path_goal_y = find_near_vor(voronoi_lines, goalx, goaly, False)     # ----||--- målet

    queue = []
    cell_visited = [[None for _ in range(maxx)] for _ in range(maxy)]


    queue.append((path_start_y, path_start_x))
    cell_visited[path_start_y][path_start_x] = (path_start_y, path_start_x) # Start forældre

    while queue:
        current_y, current_x = queue.pop(0)

        if (current_y, current_x) == (path_goal_y, path_goal_x):    # Hvis fundet gyldig path => tegn streger til start/goal + ruten langs roadmap
            # for y in range(maxy):         # Til at se hvad der er udforsket
            #     for x in range(maxx):
            #         if cell_visited[y][x] is not None:
            #             map[y, x] = (0, 255, 0)  # Grøn farve

            cv2.line(map, (startx,starty),(path_start_x,path_start_y),(0,0,255))
            cv2.line(map, (goalx,goaly),(path_goal_x,path_goal_y),(0,0,255))

            map_out = visualize_path(cell_visited, path_start_y, path_start_x, path_goal_y, path_goal_x, map)
            return map_out
       
        for stepy,stepx in directions_diag: # nei = neighbor x/y
            neiy = current_y + stepy
            neix = current_x + stepx

            if 0 <= neiy < maxy and 0 <= neix < maxx:
                if voronoi_lines[neiy, neix] == 1 and cell_visited[neiy][neix] is None:
                    queue.append((neiy,neix))
                    cell_visited[neiy][neix] = (current_y, current_x)
    return map

# ----------------- Tegner faktisk ruten op langs voronoi linjerne ----------------------------------------------------
def visualize_path(cell_visited, starty, startx, goaly, goalx, map):
    current = (goaly, goalx)                # Starter ved målet, altså bagfra

    if cell_visited[goaly][goalx] is None:
        print("no path found.")
        return map

    while current != (starty, startx):      # og kører ind til den rammer starten. Ved at gå til hver celles forælder celle
        map[current[0]][current[1]] = (255,0,0)
        current = cell_visited[current[0]][current[1]]

    return map

# ----------------- Indlæs / generer map ------------------------------------------------------------------------------
# map_file = 'prg_ex2_map.png'
# map_file = 'map_hestesko.png'
# map_file = 'map_spiral.png'
# map_file = 'map_spiral_cut.png'
# map_file = 'map_spiral_broke.png'
# map_file = 'map_helt_crazy.png'
map_file = 'map_stop_nu_ven.png'
# map_file = 'map_stop_nu_ven2.png' ## Virker ikke :)


map_image = read_map(map_file)
# map_image = make_map(400, 400)
height, width, _ = map_image.shape


# ----------------- Udfør brushfire algoritemen og vis den i nyt vindue -----------------------------------------------
add_edges(map_image, width, height)

obstacle_matrix = identify_obstacles(map_image, width, height)

brushfire_matrix, region_matrix = brushfire_from_obstacles(obstacle_matrix, width, height)

brushfire_map = visualize_brushfire(brushfire_matrix, width, height)
cv2.imshow('Brushfire Map', brushfire_map)
cv2.moveWindow('Brushfire Map', 100, 0)
cv2.waitKey(0)

# ----------------- Generer GVD udfra regioner og brushfire structures ----------------------------------------------------
voronoi_lines = find_local_maxima(brushfire_matrix, width, height)

roadmap = visualize_voronoi(voronoi_lines, width, height)

# Show map before connections
cv2.imshow("Voronoi lines", roadmap)
cv2.moveWindow('Voronoi lines', 125+width, 140+height)
cv2.waitKey(0)

color_map = draw_color_map(brushfire_matrix, voronoi_lines, region_matrix, width, height)

structures = find_edge_red(color_map, width, height)
connect_structures(color_map, structures, voronoi_lines, width, height)

cv2.imshow("Voronoi Diagram", color_map)
cv2.moveWindow('Voronoi Diagram', 125+width, 0)

# ----------------- Åben et vindue med kun roadmap --------------------------------------------------------------------
roadmap = visualize_voronoi(voronoi_lines, width, height)
cv2.imshow("Voronoi lines", roadmap)
cv2.moveWindow('Voronoi lines', 125+width, 140+height)
cv2.waitKey(0)

# ----------------- Find korteste rute og vis den i nyt vindue ------------------------------
start = (15, 320) # y, x
goal = (140, 174)
path_map = path_planner(voronoi_lines, start[0], start[1], goal[0], goal[1], width, height, map_image)
cv2.imshow('Route Map', path_map)
cv2.moveWindow('Route Map', 150+2*width, 0)

cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()