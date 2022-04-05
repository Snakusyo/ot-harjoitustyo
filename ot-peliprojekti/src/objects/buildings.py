#This program assigns properties and values to different building types in the game


class Building():

    def __init__(self, type: tuple):

        #Different building types are defined by tuples
        #The first value in the tuple is the building type

        # 0 = Main Building
        # 1 = Road
        # 2 = House
        # 3 = Gathering building (buildings that produce goods on their own)
        # 4 = Production buildings (buildings that turn goods into other goods)
        # 5 = Service buildings

        #The second value in the tuple is the subtype of that building

        #The third value is only for buildings that can have multiple properties, such as mines and farms. If the third value is not stated, it will be a 0


        self.type = type[0]
        self.subtype = type[1]

        if type[2] == None:
            self.spectype = 0
        else:
            self.spectype = type[2]


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