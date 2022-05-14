from random import randint
from sys import maxsize

#TESTING MAP GENERATION

class MapGenerator():

    def __init__(self, size: int):

        #default values for map are set here
        #the border determines how many tiles at the edge of the map must be ocean tiles before adding land
        self.border = 3
        #variance determines how much difference in size there is within lengths of rows of tiles
        self.variance = 4
        #size determines width and height of map
        #in the generate_map function, it is determined that the minimum size of map is 64
        #this may be changed but making it smaller may brake the map generation!
        self.size = size

    def generate_map(self, size: int):

        #minimum size for map is 64
        #this ensures all the other methods are working
        #64 is just made up for safe measure
        if size < 64:
            return False
        map = []
        #create a size*size array of 0's
        #this will be read as an ocean the size of the entire map
        for i in range(size):
            maprow = []
            for u in range(size):
                maprow.append(0)
            map.append(maprow)
        
        return(map)


    def add_island(self, map: list):

        #border size
        b = self.border
        #maximum variance in rows next to each other
        v = self.variance
        #lenght of map and row
        s = len(map)

        #maximum size of island in tiles
        #s^2-(2sb-2*(b*(s-2b)))
        #this ensures that the island fits the map while having the borders
        #probably not needed
        maxs = int((s*s)-(2*s*b)-2*(b*(s-2*b)))
        #minimum size of island in tiles
        #this ensures that the island is always at least a certain portion (50% of playable area) of the map and
        #not too small
        mins = int(maxs/2)
        #maximum length of one island row (height/width)
        maxd = s-(2*b)
        #minimum length of one island row (height/width)
        mind = v+b

        #the island is generated here
        for row in range(s):
            #width of island in this row
            width = randint(mind, maxd)
            #start index of island in this row
            start = randint(b, s-b-width)
            #only generate island inside borders
            if b < row < s-b:
                try:
                    #island width in the last row
                    lastwidth = map[row-1].count(1)
                    #island starting index in the last row
                    laststart = map[row-1].index(1)
                except ValueError:
                    #if last row doesn't have land, add land
                    map[row] = self.generate_island_row(b, width, start, map[row])
                

                if lastwidth > 0:
                    #width of island in this row if last row already has island
                    width = randint(lastwidth-int(v/2), lastwidth+int(v/2))
                    #same for starting index
                    start = randint(laststart-v, laststart+v)

                map[row] = self.generate_island_row(b, width, start, map[row])

        return map

    def generate_island_row(self, border: int, width: int, start: int, row: list):
        #set single letters to make the equations easier to read
        b = border
        w = width
        s = start

        #don't add land to borders
        #this ensures starting point is always after the border
        if s < b:
            s = b
        elif s > len(row)-b:
            s = len(row)-b-w

        for tile in range(len(row)):
            #this ensures ending point for land is always before the border
            if tile >= len(row)-b:
                row[tile] = 0
            #add a 1 into the starting point of the island
            elif tile == s:
                    row[tile] = 1
            #add a 1 into this tile if it meets the requirements
            elif 0 < row.count(1) < w:
                    row[tile] = 1
        return row


    def add_mountain_or_lake(self, map: list, type: str):

        border = self.border
        if type == "mountain":
            #2's are read as mountain tiles in game
            x = 2
        if type == "lake":
            #0's are water
            x = 0

        #maximum size for mountains and lakes is 8*8
        #minimum size is 4*4
        size = randint(4,8)
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
            for tile in range(len(map[row])):
                if last_possible_tile == 0:
                    if int(len(map[row])/2) < tile < len(map[row])-border:
                        if map[row][tile] == 0:
                            last_possible_tile = tile-2-size

        starting_tile = randint(first_possible_tile, last_possible_tile)

        #this is where the mountain/lake is generated
        for i in range(size):
            for u in range(size):
                if (i == 0 or i == size-1) and (u == 0 or u == size-1):
                    pass
                else:
                    map[starting_row+i][starting_tile+u] = x

        return map


    def get_map(self):

        #determine maximum and minimum size for island
        #this is used to ensure the island isn't too small or too big
        max_size = int((self.size*self.size)-(2*self.size*self.border)-2*(self.border*(self.size-2*self.border)))
        min_size = int(max_size/2)
        while True:
            #generate an empty ocean
            ocean = self.generate_map(self.size)
            island_size = 0
            #generate an island on the ocean
            map_with_island = self.add_island(ocean)
            for row in map_with_island:
                island_size += row.count(1)

            #assure island meets size requirements
            if min_size <= island_size <= max_size:
                break

        #possibly add a couple of lakes on the map
        self.add_mountain_or_lake(map_with_island, "lake")
        self.add_mountain_or_lake(map_with_island, "lake")

        #add a mountain to map
        mountain = False
        while mountain == False:
            mountain_tiles = 0
            for row in map_with_island:
                for tile in row:
                    if tile == 2:
                        mountain_tiles += 1

            if mountain_tiles > 0:
                break
            else:
                self.add_mountain_or_lake(map_with_island, "mountain")

        #turn the map 90 degrees because "oops"
        newmap = []
        for x in range(self.size):
            newrow = []
            for y in range(self.size):
                newrow.append(map_with_island[y][x])
            newmap.append(newrow)

        return newmap

MapGenerator(128).get_map()
