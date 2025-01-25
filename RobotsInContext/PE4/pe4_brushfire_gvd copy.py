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
def identify_obstacles(map, maxx, maxy):
    """
    Identificer alle obstacles og tildel dem unikke ID'er.
    """
    obstacle_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    obstacle_index = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Op, ned, højre, venstre

    for x in range(maxx):
        for y in range(maxy):
            if is_pixel_an_obstacle(map, x, y) and obstacle_matrix[y][x] == 0:
                # Start en flood fill for dette obstacle
                queue = [(y, x)]
                obstacle_matrix[y][x] = obstacle_index

                while queue:
                    current_y, current_x = queue.pop(0)
                    for dx, dy in directions:
                        nx, ny = current_x + dx, current_y + dy
                        if 0 <= nx < maxx and 0 <= ny < maxy:
                            if is_pixel_an_obstacle(map, nx, ny) and obstacle_matrix[ny][nx] == 0:
                                obstacle_matrix[ny][nx] = obstacle_index
                                queue.append((ny, nx))
                
                obstacle_index += 1

    return obstacle_matrix


def brushfire_with_obstacles(map, obstacle_matrix, maxx, maxy):
    """
    Udfører Brushfire-algoritmen efter korrekt registrering af obstacles.
    """
    queue = []
    matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    region_matrix = [[0 for _ in range(maxx)] for _ in range(maxy)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Initier obstacles i køen og region_matrix
    for x in range(maxx):
        for y in range(maxy):
            if obstacle_matrix[y][x] > 0:  # Hvis dette er en obstacle pixel
                matrix[y][x] = 1
                region_matrix[y][x] = obstacle_matrix[y][x]  # Brug obstacle ID som region ID
                queue.append((y, x))

    # Brushfire-algoritmen
    while queue:
        current_pixel = queue.pop(0)
        current_y, current_x = current_pixel
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < maxx and 0 <= ny < maxy:
                if matrix[ny][nx] == 0:  # Hvis pixel ikke allerede er besøgt
                    matrix[ny][nx] = matrix[current_y][current_x] + 1
                    region_matrix[ny][nx] = region_matrix[current_y][current_x]  # Arv region ID
                    queue.append((ny, nx))

    return matrix, region_matrix

def find_local_maxima(brushfire_matrix, maxx, maxy):
    """
    Finder lokale maksima i brushfire-matrixen med et strengere kriterium.
    """
    # local_maxima = []
    voronoi_lines = np.zeros((maxy, maxx), dtype=np.uint8)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Op, ned, højre, venstre

    for x in range(1, maxx - 1):  # Undgå kanterne
        for y in range(1, maxy - 1):  # Undgå kanterne
            current_value = brushfire_matrix[y][x]
            higher_than_neighbors = 0
            lower_than_neighbors = 0

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < maxx and 0 <= ny < maxy:
                    neighbor_value = brushfire_matrix[ny][nx]
                    if current_value > neighbor_value:
                        higher_than_neighbors += 1
                    elif current_value < neighbor_value:
                        lower_than_neighbors += 1

            # Maksimum, hvis det er højere end mindst 2 naboer og ikke lavere end nogen
            if higher_than_neighbors >= 1 and lower_than_neighbors ==  0: # >=2 og == 0
                voronoi_lines[y][x] = 1

    return voronoi_lines


def visualize_voronoi(matrix, voronoi_lines, region_matrix, maxx, maxy):
    """
    Visualiserer Voronoi-linjerne oven på brushfire-matrixen.
    """
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
    (255, 210, 180)]
    color_map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    for x in range(maxx):
        for y in range(maxy):
            if matrix[y][x] == 1:
                color_map[y][x] = (0,0,0)
            elif voronoi_lines[y][x] == 1:  # Voronoi-linje
                color_map[y][x] = (0, 0, 255)  # Rød linje
            else:
                color_map[y][x] = farver[region_matrix[y][x] % len(farver)]
            
            for stepx,stepy in directions:
                neiy, neix = y+stepy, x+stepx
                if 0 <= neiy < maxy and 0 <= neix < maxx and region_matrix[y][x] != region_matrix[neiy][neix]:
                    color_map[y][x] = (60,60,60)
                    voronoi_lines[y][x] = 1

    return color_map
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

# _----------------------------------------------------------------------------------------------------------------------------------------

def find_edge_red(color_map, maxx, maxy):
    """
    Finder alle strukturer af røde pixels og returnerer koordinaterne for:
    - Den røde pixel med laveste x
    - Den røde pixel med højeste x
    - Den røde pixel med laveste y
    - Den røde pixel med højeste y

    Returnerer en liste over strukturer, hvor hver struktur indeholder:
    - min_x_coord, max_x_coord, min_y_coord, max_y_coord
    """
    visited = np.zeros((maxy, maxx), dtype=bool)  # Marker hvilke pixels der er besøgt
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Alle naboer
    structures = []  # Gem resultater for hver struktur

    for y in range(maxy):
        for x in range(maxx):
            # Tjek om pixel er rød og ikke besøgt
            if np.array_equal(color_map[y, x], (0, 0, 255)) and not visited[y, x]:
                # Start en ny struktur
                queue = [(x, y)]
                visited[y, x] = True  # Marker pixel som besøgt
                structure_points = [(x, y)]  # Gem koordinater i denne struktur

                while queue:
                    cx, cy = queue.pop(0)
                    # Find naboer, der ikke er besøgt
                    for dx, dy in directions:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < maxx and 0 <= ny < maxy:
                            if np.array_equal(color_map[ny, nx], (0, 0, 255)) and not visited[ny, nx]:
                                queue.append((nx, ny))
                                visited[ny, nx] = True
                                structure_points.append((nx, ny))

                # Beregn ekstremer for denne struktur
                min_x_coord = min(structure_points, key=lambda p: p[0])
                max_x_coord = max(structure_points, key=lambda p: p[0])
                min_y_coord = min(structure_points, key=lambda p: p[1])
                max_y_coord = max(structure_points, key=lambda p: p[1])

                # Tilføj resultater for denne struktur
                structures.append({min_x_coord, min_y_coord, max_x_coord, max_y_coord})

    return structures





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
    """
    Finder de nærmeste Voronoi-punkter til start- og målkoordinater, med tjek for fri passage.
    """
    def is_line_clear(x1, y1, x2, y2, map):
        """
        Tjekker om linjen mellem (x1, y1) og (x2, y2) krydser forhindringer.
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        # maxy, maxx = map.shape  # Få størrelsen på kortet

        while True:
            # Grænsetjek for at sikre, at koordinaterne er inde i arrayet
            if not (0 <= x1 < maxx and 0 <= y1 < maxy):
                return False  # Hvis vi går uden for kortet, er linjen ikke klar

            if np.array_equal(map[y1, x1], (0,0,0)):  # Tjek for forhindring (0 repræsenterer obstacle)
                return False
            if (x1, y1) == (x2, y2):  # Nået til destinationen
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return True

    vor_x_s = 0
    vor_y_s = 0
    lowest_dist_s = maxx * maxy
    vor_x_e = 0
    vor_y_e = 0
    lowest_dist_e = maxx * maxy    

    for x in range(maxx):
        for y in range(maxy):
            if int(voronoi_lines[y, x]) == 1:  # Punkt på Voronoi-linjen
                dist_s = np.sqrt((y - starty) ** 2 + (x - startx) ** 2)
                dist_e = np.sqrt((y - goaly) ** 2 + (x - goalx) ** 2)

                # Tjek for fri passage til startpunkt
                if dist_s < lowest_dist_s and is_line_clear(startx, starty, x, y, map):
                    vor_y_s = y
                    vor_x_s = x 
                    lowest_dist_s = dist_s

                # Tjek for fri passage til slutpunkt
                if dist_e < lowest_dist_e and is_line_clear(goalx, goaly, x, y, map):
                    vor_y_e = y
                    vor_x_e = x
                    lowest_dist_e = dist_e

    return vor_y_s, vor_x_s, vor_y_e, vor_x_e



def connect_structures(color_map, structures, voronoi_lines, maxx, maxy):
    """
    Forbinder strukturer til hinanden og derefter til nærmeste Voronoi-linje.
    """
    def is_line_clear(x1, y1, x2, y2):
        """
        Tjekker om linjen mellem (x1, y1) og (x2, y2) krydser obstacles.
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if np.array_equal(color_map[y1, x1], (0, 0, 0)):  # Obstacle pixel
                return False
            if (x1, y1) == (x2, y2):  # Reached destination
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return True

    def find_nearest(coords1, coords2):
        """
        Find det nærmeste par af punkter mellem to strukturer.
        """
        min_dist = float("inf")
        closest_pair = None

        for c1 in coords1:
            for c2 in coords2:
                dist = np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (c1, c2)

        return closest_pair

    def find_near_vor(voronoi_lines, startx, starty, maxx, maxy):
        """
        Finder det nærmeste punkt på Voronoi-linjen.
        """
        vor_x_s = 0
        vor_y_s = 0
        lowest_dist_s = maxx * maxy    

        for y in range(maxy):
            for x in range(maxx):
                if np.array_equal(color_map[y, x], (60, 60, 60)):  # Punkt på Voronoi-linjen
                    dist = np.sqrt((y - starty) ** 2 + (x - startx) ** 2)
                    if dist < lowest_dist_s:
                        vor_y_s = y
                        vor_x_s = x 
                        lowest_dist_s = dist

        return vor_x_s, vor_y_s

    # Første del: Forbind alle strukturer til hinanden
    connected_pairs = set()
    for i, struct1 in enumerate(structures):
        for j, struct2 in enumerate(structures):
            if i != j and (i, j) not in connected_pairs and (j, i) not in connected_pairs:
                closest_pair = find_nearest(struct1, struct2)
                if closest_pair:
                    (x1, y1), (x2, y2) = closest_pair
                    if is_line_clear(x1, y1, x2, y2):
                        print(f"Forbinder struct {i} og struct {j}: ({x1}, {y1}) -> ({x2}, {y2})")
                        cv2.line(color_map, (x1, y1), (x2, y2), (255, 0, 0), 1)  # Rød linje
                        cv2.line(voronoi_lines, (x1, y1), (x2, y2), 1, 1)
                        connected_pairs.add((i, j))

    # Anden del: Forbind alle strukturer til Voronoi-linjerne
    for struct in structures:
        for coords in struct:
            # Find nærmeste Voronoi-linje punkt
            vx, vy = find_near_vor(voronoi_lines, coords[0], coords[1], maxx, maxy)

            # Tjek om der er en klar linje
            if is_line_clear(coords[0], coords[1], vx, vy):
                print(f"Forbinder til Voronoi: ({coords[0]}, {coords[1]}) -> ({vx}, {vy})")
                cv2.line(color_map, (coords[0], coords[1]), (vx, vy), (0, 255, 0), 1)  # Grøn linje
                cv2.line(voronoi_lines, (coords[0], coords[1]), (vx, vy), 1, 1)
                break

    for x in range(maxx):
        for y in range(maxy):
            if np.array_equal(color_map[y, x], (0,255,0)) or np.array_equal(color_map[y, x], (0, 0, 255)) or np.array_equal(color_map[y, x], (255, 0, 0)):
                color_map[y, x] = (60, 60, 60)
        





def connect_concave_corners(region_matrix, voronoi_lines, maxx, maxy):
    """
    Forbinder hjørner i konkave obstacles til GVD, men kun hvis linjen er fri for obstacles.
    """
    def is_line_clear(x1, y1, x2, y2):
        """
        Tjekker om linjen mellem (x1, y1) og (x2, y2) krydser obstacles.
        """
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if np.array_equal(region_matrix[y1][x1], (0, 0, 0)):  # Obstacle pixel
                return False
            if (x1, y1) == (x2, y2):  # Reached destination
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return True

    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),  # Op, ned, højre, venstre
        (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonaler
    ]
    connected_points = []

    for x in range(1, maxx - 1):  # Undgå kanten
        for y in range(1, maxy - 1):  # Undgå kanten
            if not is_pixel_an_obstacle(region_matrix, x, y):
                is_corner = False
                obstacle_neighbors = 0
                diagonal_neighbors = 0
                
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < maxx and 0 <= ny < maxy:
                        if np.array_equal(region_matrix[ny][nx], (0, 0, 0)):  # Del af obstacle
                            if abs(dx) + abs(dy) == 1:  # Kun lodret/vandret nabo
                                obstacle_neighbors += 1
                            else:  # Diagonal nabo
                                diagonal_neighbors += 1

                # Hjørne detekteres kun hvis der er præcis 2 lodrette/vandrette naboer
                # og ikke flere end 1 diagonal nabo (for at undgå skæve linjer)
                if obstacle_neighbors == 2 and diagonal_neighbors > 1:
                    is_corner = True

                if is_corner:
                    connected_points.append((x, y))

    # Forbind hjørner til Voronoi-linjer
    for cx, cy in reversed(connected_points):
        closest_vor = None
        min_dist = float('inf')
        for vx in range(maxx):
            for vy in range(maxy):
                if voronoi_lines[vy][vx] == 1:
                    dist = np.sqrt((cx - vx)**2 + (cy - vy)**2)
                    if dist < min_dist:
                        # Check if the line is clear before updating closest_vor
                        if is_line_clear(cx, cy, vx, vy):
                            min_dist = dist
                            closest_vor = (vx, vy)
        if closest_vor:
            if min_dist > 5:
                cv2.line(region_matrix, (closest_vor[0], closest_vor[1]), (cx, cy), (0,0,255), 1)  # Forbind til nærmeste linje
                cv2.line(voronoi_lines, (closest_vor[0], closest_vor[1]), (cx, cy), 1, 1)
                print(f"Connected corner ({cx}, {cy}) to Voronoi line at {closest_vor}")





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


def vis_vor(voronoi_lines, maxx, maxy):
    map = np.zeros((maxy, maxx, 3), dtype=np.uint8)
    
    for x in range(maxx):
        for y in range(maxy):
            if voronoi_lines[y][x] == 1:
                map[y, x] = (0, 0, 255)  
        
    return map

# ----------------- Indlæs / generer map ------------------------------------------------------------------------------
# map_file = 'prg_ex2_map.png'
# map_file = 'map_hestesko.png'
# map_file = 'map_spiral.png'
# map_file = 'map_spiral_cut.png'
# map_file = 'map_helt_crazy.png'
map_file = 'map_stop_nu_ven.png'


map_image = read_map(map_file)
# map_image = make_map(400, 400)
height, width, _ = map_image.shape

# ----------------- Udfør brushfire algoritemen og vis den i nyt vindue -----------------------------------------------
add_edges(map_image, width, height)

obstacle_matrix = identify_obstacles(map_image, width, height)

brushfire_matrix, region_matrix = brushfire_with_obstacles(map_image, obstacle_matrix, width, height)

brushfire_map = visualize_matrix(brushfire_matrix, width, height)
cv2.imshow('Brushfire Map', brushfire_map)
cv2.moveWindow('Brushfire Map', 100, 0)
cv2.waitKey(0)

voronoi_lines = find_local_maxima(brushfire_matrix, width, height)

color_map = visualize_voronoi(brushfire_matrix, voronoi_lines, region_matrix, width, height)

structures = find_edge_red(color_map, width, height)
connect_structures(color_map, structures, voronoi_lines, width, height)

cv2.imshow("Voronoi Diagram", color_map)
cv2.moveWindow('Voronoi Diagram', 125+width, 0)


# cv2.waitKey(0)
# cv2.destroyAllWindows()


vor = vis_vor(voronoi_lines, width, height)
cv2.imshow("Voronoi lines", vor)
cv2.moveWindow('Voronoi lines', 125+width, 440)

cv2.waitKey(0)



# ----------------- Generer GVD udfra regioner og vis i nyt vindue ----------------------------------------------------
# unify_regions(brushfire_matrix, region_matrix, width, height)
# region_map, voronoi_lines = visualize_region_matrix(brushfire_matrix, region_matrix, width, height)

# connect_concave_corners(region_map, voronoi_lines, width, height)

# cv2.imshow('Region Map', region_map) 
# cv2.moveWindow('Region Map', 125+width, 0)
# cv2.waitKey(0)

# ----------------- Find korteste rute og vis den i nyt vindue ------------------------------
start = (30, 320) # y, x
goal = (140, 180)
path_map = path_planner(voronoi_lines, start[0], start[1], goal[0], goal[1], width, height, map_image)
cv2.imshow('Route Map', path_map)
cv2.moveWindow('Route Map', 150+2*width, 0)


cv2.waitKey(0) # wait key is necessary, otherwise the window closes immediately
cv2.destroyAllWindows()

