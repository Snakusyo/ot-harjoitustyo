#This program holds values tiles of the map
#Values include:
#Building on tile
#Building consist of the tile it was built on and the rotation of the building. This means

#Terrain type and properties
#Location of the tile

#Tiles will be added to an array upon starting a game
#The game map will be created and updated based on the values in each tile

class Tile():

    def __init__(self, terrain: int):

        #this is the terrain type of the tile
        # 0 = water
        # 1 = grass
        # 2 = rock
        #more added later
        self.terrain = terrain
        #this includes both building type and rotation of the building
        self.building = (None, None)

    #new functions added later

    def __str__(self):
        
        return "Tile: {self.terrain}"