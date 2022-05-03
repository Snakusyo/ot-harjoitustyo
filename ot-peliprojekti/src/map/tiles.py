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

        #tile location, terrain type and default values are defined here
        #the default values are then edited when the player builds something on the tile
        self.terrain = terrain
        self.location = location
        self.housetier = None
        self.graphic = None
        self.building = None
        self.road = None
        self.timer = 0
        self.income = 0
        self.population = 0

    def set_graphic(self, filename: str):
        #the graphic of the tile terrain is determined here
        self.graphic = filename

    def set_income(self, amount: int):
        #set the income for the tile
        self.income = amount

    def set_population(self, amount: int):
        #set population of tile
        self.population = amount

    def has_road(self):
        #this is called to check if tile has a road
        if self.road == None:
            return False
        else:
            return True

    def has_building(self):
        if self.building != None and self.road == None:
            type = self.building.type
        #check if tile has building
        else:
            return False
        if type != None and self.road == None:
            if type == "gather" or type == "produce" or type == "house":
                return True

            else:
                return False

        else:
            False
    
    def place_road(self, road: str):
        #add information of a road in this tile
        self.building = "road"
        self.road = road

    def update_road(self, road: str):
        #this is called when a road is added to a surrounding tile
        #to update the graphic of the road
        if self.building == "road":
            self.road = road
        else:
            pass

    def add_building(self, building: Building):
        #add information of a building in this tile
        self.building = building
        if building.type == "gather" or building.type == "produce":
            self.income = building.upkeep * -1
        if building.type == "house":
            self.housetier = 0
            self.income = 2
            self.population = 2

    def set_timer(self, time: int):
        #setting the timer for the building
        #this is increased by one every second if the tile has a building with a production interval
        #once this interval is reached, the timer is set to zero again
        self.timer = time

    def upgrade(self, building: Building):
        #this is called if a house in this tile is upgraded
        self.building = building
        self.housetier += 1
        self.income *= 2
        self.population *= 2

    def empty(self):
        #this is called when an object in this tile is destroyed
        self.building = None
        self.road = None
        self.income = 0

    def __str__(self):
        #for testing purposes only
        
        return f"Tile: {self.location}"
