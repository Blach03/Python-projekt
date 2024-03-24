def generate_map():

    from random import randint,choices

    n=101

    map = [[0]*n for _ in range(n)]


    a = randint(0,3)
    b = randint(0,3)
    weights=[15, 15, 15, 15]
    weights[a]+=25
    weights[b]+=15


    map[50][50]=1


    curr_location = [50,50]
    neigh = [(-1,0),(1,0),(0,-1),(0,1)]
    for i in range(50):
        for el in neigh:
            if map[curr_location[0]+el[0]][curr_location[1]+el[1]] == 0:
                x = randint(0,3)
                if x == 0:
                    map[curr_location[0]+el[0]][curr_location[1]+el[1]] = 1
        x = choices([0,1,2,3], weights)[0]
        curr_location = [curr_location[0]+neigh[x][0],curr_location[1]+neigh[x][1]]
        map[curr_location[0]][curr_location[1]] = 1

    map[curr_location[0]][curr_location[1]] = 2
    map[50][50] = 3



    def remove_unnecessary_rows_columns(map):
        rows_to_keep = [i for i, row in enumerate(map) if any(row)]
        cols_to_keep = [j for j in range(len(map[0])) if any(map[i][j] for i in rows_to_keep)]

        new_map = [[map[i][j] for j in cols_to_keep] for i in rows_to_keep]

        return new_map

    map = remove_unnecessary_rows_columns(map)
    
    end = 0
    start = 0
    a=len(map)
    b=len(map[0])
    for i in range(a):
        for j in range(b):
            if map[i][j] == 2:
                end = [i,j]
            if map[i][j] == 3:
                start = [i,j]

    return map, start, end

def generate_rooms(map, start):
    tile = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',
    ]
    n = len(map)
    m = len(map[0])
    rooms = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if map[i][j] >= 1:
                tilemap = tile.copy()
                if map[i][j-1] >= 1:
                    for k in range(6,9):
                        row = list(tilemap[k])
                        row[0] = "."
                        tilemap[k] = ''.join(row)
                if map[i-1][j] >= 1:
                    row = list(tilemap[0])
                    for k in range(8,12):
                        row[k] = "."
                    tilemap[0] = ''.join(row)
                if i + 1 < n:
                    if map[i+1][j] >= 1:
                        row = list(tilemap[-1])
                        for k in range(8,12):
                            row[k] = "."
                        tilemap[-1] = ''.join(row)
                if j + 1 < m:
                    if map[i][j+1] >= 1:
                        for k in range(6,9):
                            row = list(tilemap[k])
                            row[-1] = "."
                            tilemap[k] = ''.join(row)
                tilemap = generate_room(tilemap)
                rooms[i][j] = tilemap
    row = list(rooms[start[0]][start[1]][7])
    row[9] = "P"
    rooms[start[0]][start[1]][7] = ''.join(row)
    return rooms


def generate_room(room):
    from random import randint
    a1 = [".....", 
         "....B", 
         "....B", 
         "....B", 
         ".BBBB"] #5x5
    a2 = ["...B.", 
         "...B.", 
         "...BB", 
         ".BBB.",
         "..B.."] #5x5
    a3 = [".....", 
         "..B..", 
         "BBBBB", 
         "....B", 
         "....B"] #5x5
    a4 = ["...B.", 
         "...BB", 
         "....B", 
         "BB...",
         ".BB.."]
    b1 = [".....", 
         "B....", 
         "B....", 
         "B....", 
         "BBBB."] #5x5
    b2 = [".B...", 
         ".B...", 
         "BB...", 
         ".BBB.",
         "..B.."] #5x5
    b3 = [".....", 
         "..B..", 
         "BBBBB", 
         "B....", 
         "B...."] #5x5
    b4 = [".B...", 
         "BB...", 
         "B....", 
         "...BB",
         "..BB."]
    c1 = [".BBBB", 
         "....B", 
         "....B", 
         "....B", 
         "....."] #5x5
    c2 = [".B...", 
         ".BBB.", 
         "...BB", 
         "...B.",
         "...B."] #5x5
    c3 = ["....B", 
         "....B", 
         "BBBBB", 
         "..B..", 
         "....."] #5x5
    c4 = [".BB..", 
         "BB...", 
         "....B", 
         "...BB",
         "...B."]
    d1 = ["BBBB.", 
         "B....", 
         "B....", 
         "B....", 
         "....."] #5x5
    d2 = [".B...", 
         ".BBB.", 
         "BB...", 
         ".B...",
         ".B..."] #5x5
    d3 = ["B....", 
         "B....", 
         "BBBBB", 
         "..B..", 
         "....."] #5x5
    d4 = ["..BB.", 
         "...BB", 
         "B....", 
         "BB...",
         ".B..."]
    corner1 = [a1,a2,a3,a4]
    corner2 = [c1,c2,c3,c4]
    corner3 = [b1,b2,b3,b4]
    corner4 = [d1,d2,d3,d4]
    options = [corner1,corner2,corner3,corner4]
    corners = [(1,1), (1,9), (14,1), (14,9)]
    for i in range(4):
        x = randint(0,3)
        
        shape = options[i][x]
        coords = corners[i]
        for j in range(5):
            row = list(room[coords[1]+j])
            for k in range(5):
                row[coords[0] + k] = shape[j][k]
            room[coords[1]+j] = ''.join(row)

    e1 = ["....", 
         "....", 
         "BBBB", 
         "....", 
         "...."] #4x5
    e2 = ["....", 
         "B..B", 
         "BBBB", 
         "B..B", 
         "...."] #4x5
    e3 = ["....", 
         "....", 
         ".BB.", 
         "....", 
         "...."] #4x5
    e4 = ["....", 
         "B..B", 
         "B..B", 
         "B..B", 
         "...."]
    f1 = [".....",  
         ".BBB.", 
         "....."]
    f2 = [".....", 
         "..B..", 
         "....."] #5x3
    f3 = [".....", 
         ".....", 
         "....."]
    mid1 = [e1,e2,e3,e4]
    mid2 = [f1,f2,f3]
    options = [mid1,mid2]
    corners = [(8,1), (14,6), (8,9), (1,6)]
    for i in range(4):
        if i%2 == 0:
            x = randint(0,3)
        else:
            x = randint(0,2)
        
        shape = options[i%2][x]
        coords = corners[i]
        if i%2 == 0:
            for j in range(5):
                row = list(room[coords[1]+j])
                for k in range(4):
                    row[coords[0] + k] = shape[j][k]
                room[coords[1]+j] = ''.join(row)
        else:
            for j in range(3):
                row = list(room[coords[1]+j])
                for k in range(5):
                    row[coords[0] + k] = shape[j][k]
                room[coords[1]+j] = ''.join(row)
    return room
