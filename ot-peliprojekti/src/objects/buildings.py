#This program assigns properties and values to different building types in the game

class Building():

    def __init__(self, name: str, type: str, tier: int, pop: int):

        self.name = name
        #houses are the only buildings the player can upgrade FOR NOW
        if type == "house":
            self.canup = True
        else:
            self.canup = False
        #determines what tier the building unlocks in
        self.tier = tier
        #determine how many people needed to unlock building
        #None for houses
        self.population_need = pop


        self.goodneeds = []
        self.production = None
        self.gametool = None
        self.graphic = None
        self.type = type
        self.road_graphic = None
        self.size = 1
        self.surface = 1
        self.upkeep = 0
        self.building_cost = 0
        self.materialneeds = {"Timber": 0, "Steel": 0}
        self.upgrade_cost = {"Timber": 0, "Steel": 0}

    def set_production(self, name: str, time: int):
        #name of product and time (in seconds) it takes to produce
        self.production = (name, time)

    def set_upgrade_cost(self, material: str, amount: int):
        #this is used to set the upgrade cost of a building
        self.upgrade_cost[material] = amount

    def set_surface(self, surface: int):
        #set surface type that building can be built on
        #default is 1 (grass) but for mines this is called to set it to 2 (mountain)
        self.surface = surface

    def set_building_cost(self, cost: int):
        #cost of building the building in cash
        #default is 0 (for houses)
        #for production and gathering buildings this will be called
        self.building_cost = cost

    def set_materialneeds(self, name: str, amount: int):
        #set the amount of materials needed to build structure
        self.materialneeds[name] = amount
        

    def set_upkeep(self, value: int):
        #determine the upkeep cost of the building
        self.upkeep = value

    def set_size(self, value: int):
        #set the size of the building
        #this implies width and height in tiles
        #NYI - may be implemented at a later time
        self.size = value

    def set_graphic(self, filename: str):
        #this is going to be a call from the main game
        #the graphic here is pulled to be drawn on screen
        self.graphic = filename

    def set_road_graphics(self, name: str):
        #this name stands for the name of the graphics in a dictionary in the main game
        self.road_graphic = name

    def add_requirement(self, good: str):
        #set how many and what goods the building requires to produce goods
        self.goodneeds.append(good)

    def set_population_need(self, amount: int):
        self.population_need = amount

    def produce_goods(self, amount: int):

        pass

    def __str__(self):

        return f"Building: {self.name}"