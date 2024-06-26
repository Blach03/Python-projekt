import json
from random import choices, randint

from config import ROOMS_DATA

data = json.load(open(ROOMS_DATA))


def generate_map() -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    """Generates matrix with room types indicated by numbers"""
    n = 101
    shops = 0
    map = [[0] * n for _ in range(n)]

    a, b = randint(0, 3), randint(0, 3)
    weights = [15, 15, 15, 15]
    weights[a] += 25
    weights[b] += 15

    map[50][50] = 1

    curr_location = [50, 50]
    neigh = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(40):
        for el in neigh:
            if map[curr_location[0] + el[0]][curr_location[1] + el[1]] == 0:
                if randint(0, 3) == 0:
                    map[curr_location[0] + el[0]][curr_location[1] + el[1]] = 1
        x = choices([0, 1, 2, 3], weights)[0]
        curr_location = [curr_location[0] + neigh[x][0], curr_location[1] + neigh[x][1]]
        if map[curr_location[0]][curr_location[1]] == 0:
            map[curr_location[0]][curr_location[1]] = 1
        if 5 < i:
            x = randint(0, 15)
            if x == 1:
                map[curr_location[0]][curr_location[1]] = 1.2  # shop
                shops += 1
        if i == 30 and shops == 0:
            map[curr_location[0]][curr_location[1]] = 1.2  # pity shop so that there is at least 1
    map[curr_location[0]][curr_location[1]] = 2
    map[50][50] = 3

    def remove_unnecessary_rows_columns() -> list[list[int]]:
        rows_to_keep = [i for i, row in enumerate(map) if any(row)]
        cols_to_keep = [
            j for j in range(len(map[0])) if any(map[i][j] for i in rows_to_keep)
        ]
        new_map = [[map[i][j] for j in cols_to_keep] for i in rows_to_keep]
        return new_map

    map = remove_unnecessary_rows_columns()

    end, start = 0, 0
    a, b = len(map), len(map[0])
    for i in range(a):
        for j in range(b):
            if map[i][j] == 2:
                end = (i, j)
            if map[i][j] == 3:
                start = (i, j)

    return map, start, end


def generate_rooms(map: list[list[int]]) -> list[list[int]]:
    """Generates doorways and enemies for each room"""
    n, m = len(map), len(map[0])
    rooms = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if map[i][j] >= 1:
                if map[i][j] == 1.2:
                    tile = data["shop"].copy()
                else:
                    tile = data["empty"].copy()
                if map[i][j] == 2:
                    tile[7] = tile[7][: 10] + "E" + tile[7][11 :]
                if map[i][j - 1] >= 1:
                    for k in range(6, 9):
                        tile[k] = "." + tile[k][1:]
                if map[i - 1][j] >= 1:
                    tile[0] = data["doorway"]
                if i + 1 < n and map[i + 1][j] >= 1:
                    tile[-1] = data["doorway"]
                if j + 1 < m and map[i][j + 1] >= 1:
                    for k in range(6, 9):
                        tile[k] = tile[k][:-1] + "."
                if map[i][j] != 1.2 and map[i][j] != 2:
                    tile = generate_room(tile)
                rooms[i][j] = tile
    return rooms


def generate_room(room: list[str]) -> list[str]:
    """Generates walls in the room"""
    def add_shape(j_length: int, k_length: int):
        for j in range(j_length):
            row = list(room[coords[1] + j])
            for k in range(k_length):
                row[coords[0] + k] = shape[j][k]
            room[coords[1] + j] = "".join(row)

    for i in range(4):
        x = randint(0, 3)
        shape = data["corner_options"][i][x]
        coords = data["corner_corners"][i]
        add_shape(5, 5)

    for i in range(4):
        x = randint(0, 3) if i % 2 == 0 else randint(0, 2)
        shape = data["mid_options"][i % 2][x]
        coords = data["mid_corners"][i]
        add_shape(5, 4) if i % 2 == 0 else add_shape(3, 5)

    return room
