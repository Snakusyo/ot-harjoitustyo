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

    def set_production(self, name: str, time: int):
        #name of product and time (in seconds) it takes to produce
        self.production = (name, time)

    def set_surface(self, surface: int):
        self.surface = surface

    def set_balance(self, value: int):
        #value for how much does the building make or take money
        #houses will have positive values, while most other buildings have negative
        pass

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

    def add_requirement(self, good: str, amount: int):
        #set how many and what goods the building requires to produce goods
        self.goodneeds.append((good, amount))

    def set_population_need(self, amount: int):
        self.population_need = amount

    def gather_goods(self, workforce: bool):

        #This will gather raw materials for eligible buildings
        #If workforce is insufficient, value of gathered materials will be 0
        pass


    def produce_goods(self, workforce: bool, materials: bool):

        #This will count production for eligible buildings
        #If number of materials and/or workforce is insufficient, production will be 0
        pass


    def tax_residents(self):

        #This will tax residents in houses
        #House level and available goods/services will be used to calculate tax income
        pass

    def __str__(self):

        return f"Building: {self.name}"