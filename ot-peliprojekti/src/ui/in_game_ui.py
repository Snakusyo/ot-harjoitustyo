from random import randint

#TESTING MAP GENERATION

def generate_map(size: int):

    if size < 64:
        return False
    map = []
    for i in range(size):
        maprow = []
        for u in range(size):
            maprow.append(0)
        map.append(maprow)
    
    return(map)


def add_island(map: list):

    #border size
    b = 3
    #maximum variance in rows next to each other
    v = 4
    #lenght of map and row
    s = len(map)

    #minimum size of island in tiles
    #third of the map
    mins = int((s*s)/3)
    #maximum size of island in tiles
    #s^2-(2sb-2*(b*(s-2b)))
    #this ensures that the island fits the map while having the borders
    #probably not needed
    maxs = int((s*s)-(2*s*b)-2*(b*(s-2*b)))
    #maximum length of one island row (height/width)
    maxd = s-(2*b)
    #minimum length of one island row (height/width)
    mind = v+b

    #the island is generated here
    for row in range(s):
        #width of island in this row
        width = randint(mind, maxd)
        start = randint(b, s-b-width)
        #only generate island inside borders
        if b < row < s-b:
            #island width in the last row
            try:
                lastwidth = map[row-1].count(1)
                #island starting index in the last row
                laststart = map[row-1].index(1)
            except ValueError:
                map[row] = generate_island_row(b, width, start, map[row])
            
            if lastwidth > 0:
                width = randint(lastwidth-int(v/2), lastwidth+int(v/2))
                start = randint(laststart-v, laststart+v)

            map[row] = generate_island_row(b, width, start, map[row])

    return map

def generate_island_row(border: int, width: int, start: int, row: list):
    b = border
    w = width
    s = start

    if s < b:
        s = b
    elif s > len(row)-b:
        s = len(row)-b-w

    for tile in range(len(row)):
        if tile >= len(row)-b:
            row[tile] = 0
        elif tile == s:
                row[tile] = 1

        elif 0 < row.count(1) < w:
                row[tile] = 1
    return row


def add_mountain_or_lake(map: list, type: str):

    border = 3
    if type == "mountain":
        #2's are read as mountain tiles in game
        x = 2
    if type == "lake":
        #0's are water
        x = 0

    #maximum size for mountains and lakes is 8*8
    #minimum size is 2*2
    size = randint(2,8)
    first_possible_row = 0
    last_possible_row = 0

    #this is where first and last possible row for lake/mountain in map is determined
    #first and last row of island cannot have mountains/lakes
    for row in range(len(map)):
        if first_possible_row == 0:
            if border < row < int(len(map)/2):
                if 1 in map[row]:
                    first_possible_row = row+1
        elif last_possible_row == 0:
            if int(len(map)/2) < row < len(map)-border+1:
                if 1 not in map[row]:
                    last_possible_row = row-2-size
    starting_row = randint(first_possible_row, last_possible_row)
    
    first_possible_tile = 0
    last_possible_tile = 0

    #this is where first and possible tile for lake/mountain in row is determined
    #first and last tile of row cannot have mountain/lakes
    for row in range(starting_row, starting_row+size):
        for tile in range(len(map[row])):
            if first_possible_tile == 0:
                if border < tile < int(len(map[row])/2):
                    if map[row][tile] == 1:
                        first_possible_tile = tile+1
            elif last_possible_tile == 0:
                if int(len(map[row])/2) < tile < len(map[row])-border:
                    if map[row][tile] == 0:
                        last_possible_tile = tile-2-size

        starting_tile = randint(first_possible_tile, last_possible_tile)

    #this is where the mountain/lake is generated
    for i in range(size):
        for u in range(size):
            map[starting_row+i][starting_tile+u] = x

    return map


        







map_ocean = generate_map(64)
map_with_island = add_island(map_ocean)
final_map = add_mountain_or_lake(map_with_island, "mountain")


newmap = []
for x in range(64):
    newrow = []
    for y in range(64):
        newrow.append(map_with_island[y][x])
    newmap.append(newrow)

for row in final_map:
    print(row)