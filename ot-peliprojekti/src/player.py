#Player information is here




class Player():

    def __init__(self, name: str):

        self.name = name
        self.goods = {}
        self.income = 0
        self.balance = 0
        self.buildings = []

    def set_goods(self, good: str, amount: int):
        #sets goods for players storage
        self.goods[good] = amount

    def set_balance(self, amount: int):
        #update player balance
        self.balance += amount

    def add_building(self, building: str, tile: tuple):
        #creates a tuple with a building name and location (as tuple, again):
        item = (building, tile)
        self.buildings.append(item)

    def delete_building(self, location: tuple):
        #deletes player building in specified location
        for building in self.buildings:
            if building[1] == location:
                self.buildings.remove(building)
