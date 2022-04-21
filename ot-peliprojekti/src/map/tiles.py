#This program holds values tiles of the map
#Values include:
#Building on tile
#Building consist of the tile it was built on and the rotation of the building. This means

#Terrain type and properties
#Location of the tile

#Tiles will be added to an array upon starting a game
#The game map will be created and updated based on the values in each tile
from objects.buildings import Building
class Tile():

    def __init__(self, location: tuple, terrain: int):

        #this is the terrain type of the tile
        # 0 = water
        # 1 = grass
        # 2 = rock
        #more added later
        self.terrain = terrain
        self.location = location
        self.housetier = None
        self.graphic = None
        self.building = None
        self.road = None

    def set_graphic(self, filename: str):
        self.graphic = filename

    def has_road(self):
        if self.road == None:
            return False
        else:
            return True
    
    def place_road(self, road: str):
        self.building = "road"
        self.road = road

    def update_road(self, road: str):
        if self.building == "road":
            self.road = road
        else:
            pass

    def add_building(self, building: Building):
        self.building = building
        if building.type == "house":
            self.housetier = 0

    def upgrade(self, building: Building):
        self.building = building
        self.housetier += 1

    def empty(self):
        self.building = None
        self.road = None

    def __str__(self):
        
        return f"Tile: {self.location}"
