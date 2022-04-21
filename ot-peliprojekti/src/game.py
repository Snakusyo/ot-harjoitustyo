from argparse import ONE_OR_MORE
from tracemalloc import start
from turtle import up
import pygame
from pygame.locals import *
from map.tiles import Tile
from random import randint
from random import choice
from objects.buildings import Building

class StrategyGame():

    #running the game happens here
    
    def __init__(self):

        pygame.init()
        
        #this is placeholder for resolution and tilesize
        self.resx = 1280
        self.resy = 720
        self.tilesize = 40

        #this is placeholder for camera
        self.camera_position = [10, 10]
        self.camera_right, self.camera_down, self.camera_left, self.camera_up = False, False, False, False

        #keybindings are going in their own class in UI, these are placeholders
        #REMOVE
        self.keybind_up = pygame.K_w
        self.keybind_down = pygame.K_s
        self.keybind_left = pygame.K_a
        self.keybind_right = pygame.K_d
        
        #set mouseover to false at first
        #this will change when events are checked
        self.mouseovertile, self.mouseoverbutton = False, False
        #set default state of the UI
        self.current_button = None
        self.menu_open = False
        self.current_menu = None
        self.tooltip_active = False
        self.window_open = False
        self.ui_menu_buttons = []
        self.current_tool = None
        self.current_tile = None
        self.current_tool_building = None
        self.ui_icons = []

        #setup default colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.lgray = (150,150,150)
        self.mgray = (100,100,100)
        self.dgray = (50,50,50)
        self.red = (255,0,0)
        self.green = (0,125,0)
        self.blue = (0,0,180)

        #some default values for new game setup
        self.population_tier = 0


        self.font_arial = pygame.font.SysFont("Arial", 22)
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.resx,self.resy))

        pygame.display.set_caption("ot-peliprojekti")


        #everything under this is currently for testing purposes only
        self.map = []
        self.mapsize = 128
        self.map_info = self.generate_map(self.mapsize)

        self.load_graphics()
        self.load_icons()
        self.create_map(self.map_info)
        self.load_buildings()
        self.load_roads()
        self.buttons()
        self.tools()
        self.main_loop()

    def generate_map(self, size: int):

        #this method is only for testing purposes at the moment
        #it will generate map info as a list

        maplist = []

        for i in range(size):

            #this first part makes sure the edge of the map is always water
            maprow = []
            for u in range(size):
                if i == 0 or i == (size-1):
                    maprow.append(0)
                elif u == 0 or u == (size-1):
                    maprow.append(0)

                else:
                    maprow.append(1)
            maplist.append(maprow)

        return maplist

    def load_graphics(self):
        grass1 = pygame.image.load("src/images/grass1.png")
        grass2 = pygame.image.load("src/images/grass2.png")
        grass3 = pygame.image.load("src/images/grass3.png")
        grass4 = pygame.image.load("src/images/grass4.png")
        self.graphics_grass = [grass1, grass2, grass3, grass4]
        ocean1 = pygame.image.load("src/images/ocean1.png")
        ocean2 = pygame.image.load("src/images/ocean2.png")
        ocean3 = pygame.image.load("src/images/ocean3.png")
        self.graphics_ocean = [ocean1, ocean2, ocean3]
        mountain1 = pygame.image.load("src/images/mountain1.png")
        mountain2 = pygame.image.load("src/images/mountain2.png")
        mountain3 = pygame.image.load("src/images/mountain3.png")
        self.graphics_mountain = [mountain1, mountain2, mountain3]

    def load_icons(self):
        road = pygame.image.load("src/images/road_icon.png")
        houses = pygame.image.load("src/images/houses_icon.png")
        dirtroad = pygame.image.load("src/images/dirtroad_icon.png")
        housesmall = pygame.image.load("src/images/housesmall_icon.png")

        self.ui_icons = {"Road": road, "Houses": houses, "Dirt Road": dirtroad, "Small House": housesmall}

    def load_roads(self):
        dirtroad = Building("Dirt Road", "road", 0, None)
        self.buildings.append(dirtroad)
        road_none = pygame.image.load("src/images/roadnone.png")
        road_one_north = pygame.image.load("src/images/roadonen.png")
        road_one_east = pygame.image.load("src/images/roadonee.png")
        road_one_west = pygame.image.load("src/images/roadonew.png")
        road_one_south = pygame.image.load("src/images/roadones.png")
        road_two_straight_vertical = pygame.image.load("src/images/roadtwostraightv.png")
        road_two_straight_horizontal = pygame.image.load("src/images/roadtwostraighth.png")
        road_two_angle_northeast = pygame.image.load("src/images/roadtwoanglene.png")
        road_two_angle_northwest = pygame.image.load("src/images/roadtwoanglenw.png")
        road_two_angle_southeast = pygame.image.load("src/images/roadtwoanglese.png")
        road_two_angle_southwest = pygame.image.load("src/images/roadtwoanglesw.png")
        road_three_north = pygame.image.load("src/images/roadthreen.png")
        road_three_east = pygame.image.load("src/images/roadthreee.png")
        road_three_west = pygame.image.load("src/images/roadthreew.png")
        road_three_south = pygame.image.load("src/images/roadthrees.png")
        road_four = pygame.image.load("src/images/roadfour.png")

        self.roads = {"solo": road_none, "north": road_one_north, "east": road_one_east, "west": road_one_west, "south": road_one_south, \
            "vertical": road_two_straight_vertical, "horizontal": road_two_straight_horizontal, "northeast": road_two_angle_northeast,\
                "northwest": road_two_angle_northwest, "southeast": road_two_angle_southeast, "southwest": road_two_angle_southwest, \
                "tnorth": road_three_north, "teast": road_three_east, "twest": road_three_west, "tsouth": road_three_south, "cross": road_four}


    def load_buildings(self):

        housesmall = Building("Small House", "house", 0, None)
        housesmall.set_graphic(pygame.image.load("src/images/housesmall.png"))
        housemedium = Building("Medium House", "house", 1, None)
        housemedium.set_graphic(pygame.image.load("src/images/housemedium.png"))
        houselarge = Building("Large House", "house", 2, None)

        woodcutter = Building("Woodcutter", "gather", 1, 0)
        woodcutter.set_production("Logs", 5)

        mineiron = Building("Iron Mine", "gather", 2, 500)
        mineiron.set_production("Iron", 15)
        minecoal = Building("Coal Mine", "gather", 2, 500)
        minecoal.set_production("Coal", 15)

        farmgrain = Building("Grain Farm", "gather", 1, 200)
        farmgrain.set_production("Grain", 30)
        farmsheep = Building("Sheep Farm", "gather", 1, 100)
        farmsheep.set_production("Wool", 30)

        sawmill = Building("Sawmill", "produce", 1, 0)
        sawmill.add_requirement("Logs", 1)
        sawmill.set_production("Timber", 5)

        knitter = Building("Knitter", "produce", 1, 100)
        knitter.add_requirement("Wool", 1)
        knitter.set_production("Clothing", 15)
        millflour = Building("Flour Mill", "produce", 1, 200)
        millflour.add_requirement("Grain", 1)
        millflour.set_production("Flour", 15)
        bakery = Building("Bakery", "produce", 1, 200)
        bakery.add_requirement("Flour", 1)
        bakery.set_production("Bread", 15)

        furnace = Building("Furnace", "produce", 2, 500)
        furnace.add_requirement("Coal", 2)
        furnace.add_requirement("Iron", 2)
        furnace.set_production("Steel", 30)

        self.buildings = [\
            housesmall, housemedium, houselarge, \
                woodcutter, mineiron, minecoal, farmgrain, farmsheep, \
                    sawmill, knitter, millflour, bakery, furnace]
        

    def new_game(self):

        #this function will reset all in game statistics and values
        #now the player chooses their name, map, and other properties of the new game
        #after this the start_game function is called
        pass

    def load_game(self):

        #this function will set in game statistics and values to those of a saved game
        #this information is read from a savefile created through the save_game method
        #after this the start_game function is called normally
        pass

    def save_game(self):

        #this saves the current game
        #game information is extracted into a file that can be accessed by the load_game method
        pass

    def start_game(self, map: list, player: dict):

        #map is loaded into the game with the create_map function
        #state determines if a new game is started, or a game is loaded
        #player information is entered in a dictionary
        #this includes information such as player name, balance, buildings owned etc.
        pass

    def update_screen(self):

        #what ever happens on the screen is drawn here
        self.tiles_on_screen = []
        self.screen.fill(self.black)

        #define how tiles are pulled from the map (list)
        tile = self.camera_position[0]
        for i in range(int(self.resx/self.tilesize)):
            screenrow = []
            row = self.camera_position[1]
            
            for u in range(int(self.resy/self.tilesize)):
                
                #draw the tiles based on the camera position
                #tiles are drawn from left to right and then from up to down
                #camera position is defined by what tiles are shown on screen

                self.draw_tile(self.map[tile][row], i*self.tilesize, u*self.tilesize)
                screenrow.append(self.map[tile][row])
                row += 1
            self.tiles_on_screen.append(screenrow)
            tile += 1
        if self.mouseovertile:
            #highlight tile under the mouse cursor
            if self.current_tool != None:
                if self.current_tool.active:
                    self.tool_highlight_tile(self.current_tile, self.current_tool.colour)
                else:
                    self.highlight_tile(self.current_tile, self.white)
            else:
                self.highlight_tile(self.current_tile, self.white)

        if self.menu_open:
            self.draw_menu(self.current_menu)
        self.draw_ui()
        if self.mouseoverbutton: 
            self.highlight_button(self.current_button)   
        if self.tooltip_active:
            self.draw_tooltip(self.current_button.name)
        

        pygame.display.flip()
        self.game_clock.tick(60)





    def events(self):

        #events such as player input are tracked here

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #player keyboard input is tracked here

            if event.type == pygame.KEYDOWN:

                #general input is here
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                #camera movement keys here
                if event.key == self.keybind_up:
                    self.camera_up = True
                if event.key == self.keybind_down:
                    self.camera_down = True
                if event.key == self.keybind_left:
                    self.camera_left = True
                if event.key == self.keybind_right:
                    self.camera_right = True
                if event.key == K_t:
                    print(f"current tool: {self.current_tool}")
                    print(f"building: {self.current_tool_building}")
                if event.key == K_y:
                    print(f"Tile Info: \n \
                    Terrain = {self.current_tile.terrain} \n \
                        Building = {self.current_tile.building} \n \
                            Location = {self.current_tile.location} \n \
                                Road = {self.current_tile.has_road()}")
                #placeholder
                if event.key == K_r:
                    self.build_road(self.current_tile)

            if event.type == pygame.KEYUP:
                if event.key == self.keybind_up:
                    self.camera_up = False
                if event.key == self.keybind_down:
                    self.camera_down = False
                if event.key == self.keybind_left:
                    self.camera_left = False
                if event.key == self.keybind_right:
                    self.camera_right = False

            #mouse position is checked here
            self.mouse_position = pygame.mouse.get_pos()


            #mouse click is checked here
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if state[0]:
                    #if a button is clicked
                    if self.mouseoverbutton:
                        self.current_button.click()
                    #if a tile is clicked
                    elif self.mouseovertile:
                        if self.menu_open:
                            self.close_menu()
                        #if the a tool is active
                        if self.current_tool != None:
                            if self.current_tool.name == "Build":
                                if self.current_tile.building == None:
                                    self.build(self.current_tool_building)
                            if self.current_tool.name == "Demolish":
                                self.current_tile.empty()
                                self.update_roads()
                            if self.current_tool.name == "Upgrade":
                                if self.current_tile.housetier == 0:
                                    self.current_tile.upgrade(self.buildings[1])
                            if self.current_tool.name == "Build Road":
                                self.build_road(self.current_tile)
                                self.update_roads()
                        else:
                            pass

                    if self.current_button:
                        if self.current_button.type == "main":
                            if self.current_button.is_active():
                                self.open_menu(self.current_button.menu)
                                self.menu_location = self.current_button.location
                        elif self.current_button.type == "tool":
                            if self.current_button.tool != None:
                                self.current_tool = self.current_button.tool
                        elif self.current_button.type == "building":
                            self.current_tool_building = self.current_button.building
                            self.current_tool = self.player_tools[2]
                        elif self.current_button.type == "road":
                            self.current_tool_building = self.current_button.building
                            self.current_tool = self.player_tools[3]

            #right click will close menus and exit tools
                if state[2]:
                    if self.menu_open:
                        self.close_menu()
                    if self.current_tool != None:
                        self.close_tool()

            #if mouse position is on a tile, that tile should be highligted
            if self.mouse_position[0] >= 0 and self.mouse_position[1] >= 0:
                if self.mouse_position[0] < self.resx and self.mouse_position[1] < self.resy:
                    self.mouseovertile = True
                    #determine what tile is under the mouse
                    #first determine what tile on screen is under the mouse
                    tilex = int(self.mouse_position[0]/self.tilesize)
                    tiley = int(self.mouse_position[1]/self.tilesize)
                    #then define what is that tile's location on the whole map
                    maptilex = tilex+self.camera_position[0]
                    maptiley = tiley+self.camera_position[1]
                    self.current_tile = self.map[maptilex][maptiley]


                else:
                    self.mouseovertile = False
            else:
                self.mouseovertile = False

            #if mouse position is on a ui button, set mouseover to that button
            for button in self.ui_buttons:
                if self.mouse_position[0] >= button.location[0] and self.mouse_position[0] <= button.location[0]+button.size[0]:
                    if self.mouse_position[1] >= button.location[1] and self.mouse_position[1] <= button.location[1]+button.size[1]:
                        self.mouseoverbutton = True
                        self.mouseovertile = False
                        self.current_button = button
                        self.tooltip_active = True
                        break
                    else:
                        self.mouseoverbutton = False
                        self.current_button = None
                        self.tooltip_active = False
                else:
                    self.mouseoverbutton = False
                    self.current_button = None
                    self.tooltip_active = False

            #same for menu buttons
            if self.menu_open:
                for button in self.ui_menu_buttons:
                    if self.mouse_position[0] >= button.location[0] and self.mouse_position[0] <= button.location[0]+button.size[0]:
                        if self.mouse_position[1] >= button.location[1] and self.mouse_position[1] <= button.location[1]+button.size[1]:
                            self.mouseoverbutton = True
                            self.mouseovertile = False
                            self.current_button = button
                            self.tooltip_active = True
                            break
                        else:
                            self.mouseoverbutton = False
                            self.current_button = None
                            self.tooltip_active = False
                    else:
                        self.mouseoverbutton = False
                        self.current_button = False
                        self.tooltip_active = False
            

        #check if player input is doing anything
        #check if player input is doing anything
        #check if player input is doing anything

        #is the camera moving
        if self.camera_up:
            self.move_camera("up")
        if self.camera_down:
            self.move_camera("down")
        if self.camera_left:
            self.move_camera("left")
        if self.camera_right:
            self.move_camera("right")





    def create_map(self, map: list):
        
        #map information is extracted from an array and converted into Tile class objects
        y = 0
        for row in map:
            newrow = []
            x = 0
            for item in row:
                newtile = Tile((x, y), item)
                if newtile.terrain == 0:
                    newtile.set_graphic(choice(self.graphics_ocean))
                if newtile.terrain == 1:
                    newtile.set_graphic(choice(self.graphics_grass))
                if newtile.terrain == 2:
                    newtile.set_graphic(choice(self.graphics_mountain))
                newrow.append(newtile)

                x += 1
            y += 1
            self.map.append(newrow)

    def build(self, building: Building):
        #build selected building to selected tile
        tile = self.current_tile
        if tile.terrain == 1 and tile.building == None and tile.has_road() == False:
            tile.add_building(building)
        else:
            pass

    def select_road(self, tile: Tile):

        x, y = tile.location[0], tile.location[1]
        #surrounding 4 tiles are checked for roads
        east = self.check_for_road((x, y-1))
        north = self.check_for_road((x+1, y))
        south = self.check_for_road((x-1, y))
        west = self.check_for_road((x, y+1))

        surrounding_tiles = [north, west, east, south]
        if surrounding_tiles.count(True) == 4:
            #if all four tiles have road, full crossroads is chosen
            return "cross"

        elif surrounding_tiles.count(True) == 3:
            #if three tiles have road, a t-crossing is chosen
            #rotation of road is checked based on what tiles have road
            #if a tile has no road, the rotation will face the opposite to that tile
            if north == False:
                return "tnorth"
            elif south == False:
                return "tsouth"
            elif east == False:
                return "teast"
            elif west == False:
                return "twest"

        elif surrounding_tiles.count(True) == 2:
            #if two tiles have road, a straight road or a 90 degree angle is chosen
            #road type and rotation is checked based on what tiles have road
            if north and south:
                return "vertical"
            elif east and west:
                return "horizontal"

            elif north:
                if west:
                    return "southeast"
                elif east:
                    return "southwest"

            elif south:
                if west:
                    return "northeast"
                elif east:
                    return "northwest"

        elif surrounding_tiles.count(True) == 1:
            #if only one surrounding tile has road, a deadend road is chosen
            if south:
                return "north"
            elif east:
                return "west"
            elif west:
                return "east"
            elif north:
                return "south"

        if surrounding_tiles.count(True) == 0:
            #if no surrounding tiles have road, a lonely little patch of road is chosen. Hopefully they'll have some friends soon!
            return "solo"

    def build_road(self, tile: Tile):
        #builds a road on selected tile
        road = self.select_road(tile)
        tile.place_road(road)

    def update_roads(self):
        #updates all the tiles with roads to match possible new roads
        for row in self.map:
            for tile in row:
                if tile.has_road():
                    self.build_road(tile)


    def check_for_road(self, location: tuple):
        #checks tile for road based on tile location
        for row in self.map:
            for tile in row:
                if tile.location == location:
                    return tile.has_road()

    def get_production(self):
        
        #get production from buildings that produce goods
        pass

    def get_taxes(self):

        #get taxes from houses
        pass

    def update_player(self):

        #update the player statistics
        pass

    def move_camera(self, direction: str):

        #camera can be moved up, down, left or right
        if direction == "up" and self.camera_position[1] > 0:
            self.camera_position[1] -= 1
        if direction == "down" and self.camera_position[1] < self.mapsize-self.resy/self.tilesize:
            self.camera_position[1] += 1
        if direction == "left" and self.camera_position[0] > 0:
            self.camera_position[0] -= 1
        if direction == "right" and self.camera_position[0] < self.mapsize-self.resx/self.tilesize:
            self.camera_position[0] += 1

    def draw_tile(self, tile: Tile, x: int, y: int):
        
        #the map tiles are drawn here
        
        graphic = tile.graphic

        tile_graphic = self.screen.blit(graphic, (x, y))
        if tile.building != None and tile.building != "road":
            self.screen.blit(tile.building.graphic, (x, y))
        
        elif tile.has_road():
            self.screen.blit(self.roads[tile.road], (x, y))
            

    def highlight_tile(self, tile: Tile, colour: tuple):
        #this method is called when a tile on screen needs to be highlighted

        linewidth = 3
        s = self.tilesize
        x = tile.location[1]-self.camera_position[0]
        y = tile.location[0]-self.camera_position[1]

        line1 = pygame.draw.line(self.screen, colour, (x*s, y*s), (x*s+s, y*s), width=linewidth)
        line2 = pygame.draw.line(self.screen, colour, (x*s, y*s),(x*s, y*s+s), width=linewidth)
        line3 = pygame.draw.line(self.screen, colour, (x*s, y*s+s),(x*s+s, y*s+s),width=linewidth)
        line4 = pygame.draw.line(self.screen, colour, (x*s+s, y*s),(x*s+s, y*s+s),width=linewidth)
        
    def bottombar(self):

        #bottom bar in the UI, this has no functionality, only graphic
        #buttons are defined in the buttons and draw_button functions

        bottombar_background1 = pygame.draw.rect(self.screen, self.dgray, (0, self.resy-20, self.resx, 20))
        bottombar_background2 = pygame.draw.rect(self.screen, self.mgray, (0, self.resy-16, self.resx, 16))
        bottombar_foreground = pygame.draw.rect(self.screen, self.lgray, (0, self.resy-12, self.resx, 12))

        bottombar = [bottombar_background1, bottombar_background2, bottombar_foreground]

        return bottombar

    def topbar(self):

        #top bar in the UI, this is where player and city statistics are displayed
        pass

    def buttons(self):

        #define the default buttons on the UI
        road = UIButton("Road", (500, 640), (70,70), "main")
        road.menu_addbutton("Dirt Road", 0)
        road.set_graphic(self.ui_icons["Road"])
        houses = UIButton("Houses", (580, 640), (70,70), "main")
        houses.menu_addbutton("Small House", 0)
        houses.set_graphic(self.ui_icons["Houses"])
        gathering = UIButton("Gathering", (660, 640), (70,70), "main")
        gathering.menu_addbutton("Woodcutter", 0)
        gathering.menu_addbutton("Grain Farm", 1)
        gathering.menu_addbutton("Sheep Farm", 0)
        gathering.menu_addbutton("Iron Mine", 1)
        gathering.menu_addbutton("Coal Mine", 1)
        production = UIButton("Production", (740, 640), (70,70), "main")
        production.menu_addbutton("Sawmill", 0)
        production.menu_addbutton("Steel Factory", 1)
        production.menu_addbutton("Windmill", 1)
        production.menu_addbutton("Bakery", 1)
        production.menu_addbutton("Knitter", 0)
        self.ui_buttons = [road, houses, gathering, production]

    def draw_button(self, button):

        x, sx = button.location[0], button.size[0]
        y, sy = button.location[1], button.size[1]
        button_fill = pygame.draw.rect(self.screen, self.lgray, (x, y, sx, sy))
        if button.graphic != None:
            icon = button.graphic
            self.screen.blit(icon, (x+15, y+15))

        #draw the button frame
        line1 = pygame.draw.line(self.screen, self.white, (x,y), (x+sx, y), width=3)
        line2 = pygame.draw.line(self.screen, self.white,(x, y+sy), (x,y), width=3) 
        line3 = pygame.draw.line(self.screen, self.black,(x, y+sy), (x+sx, y+sy), width=3)
        line4 = pygame.draw.line(self.screen, self.black, (x+sx, y), (x+sx, y+sy), width=3)
        text = self.font_arial.render(button.keybind_text, True, self.black)
        frame_text = self.screen.blit(text,(x+5, y+5))
        icon = button.graphic

    def highlight_button(self, button):
        #this method is called when a button needs to be highlighted
        #it is called from the update_screen function

        x, y, sx, sy = button.location[0], button.location[1], button.size[0], button.size[1]
        #setup two white lines to block black ones
        line1 = pygame.draw.line(self.screen, self.white, (x, y+sy), (x+sx, y+sy), width=3)
        line2 = pygame.draw.line(self.screen, self.white, (x+sx, y), (x+sx, y+sy), width=3)

    def draw_tooltip(self, text: str):

        sizex = 150
        sizey = 60
        x = 1100
        y = 650
        frame_width = 3

        title = self.font_arial.render(text, True, self.black)

        tooltip_frame = pygame.draw.rect(self.screen, self.black, (x-frame_width, y-sizey-frame_width, sizex+frame_width*2, sizey+frame_width*2))
        tooltip_box = pygame.draw.rect(self.screen, self.lgray, (x, y-sizey, sizex, sizey))
        tooltip_text = self.screen.blit(title, (x+20, y-40))

    def open_menu(self, menu: list):

        #opens a menu based on what button was clicked
        button = self.current_button
        if button.is_active():
            self.menu_open = True
            self.current_menu = menu
            self.menu_buttons(menu)
        else:
            self.close_menu()


    def draw_menu(self, menu: list):

        if len(menu) > 0:
            x = self.menu_location[0]
            y = self.menu_location[1]
            edgey = y-80*len(self.current_menu)
            menu_frame = pygame.draw.rect(self.screen, self.black, (x-13,edgey-13,93,80*len(menu)+10))
            menu_inner = pygame.draw.rect(self.screen, self.mgray, (x-10, edgey-10, 87, 80*len(menu)+4))

        
    def menu_buttons(self, menu: list):

        #this is called when a menu is open
        #to determine if menu buttons are active
        #menu buttons are then created into UIButton class objects
        #to be interactable

        button = self.current_button
        x = button.location[0]
        y = button.location[1]-80*len(button.menu)

        for item in menu:
            if item[1] >= self.population_tier:
                #create a new button for the ui to recognize
                if item[0] == "Dirt Road":
                    new_button = UIButton(item[0], (x,y), (70,70), "road")
                    new_button.set_tool(self.player_tools[3])
                    new_button.set_graphic(self.ui_icons["Dirt Road"])
                else:
                    new_button = UIButton(item[0], (x,y), (70,70), "building")
                    new_button.set_tool(self.player_tools[2])
                    new_button.set_graphic(self.ui_icons[item[0]])
                for building in self.buildings:
                    if building.name == item[0]:
                        new_button.set_building(building)
                self.ui_menu_buttons.append(new_button)
                
                y += 80
        

    def close_menu(self):
        self.menu_open = False
        self.current_menu = None
        #self.current_button.set_active(False)
        for button in self.ui_buttons:
            button.set_active(False)
            self.ui_menu_buttons = []

    def open_window(self, name: str):
        
        #opens a new window in game
        pass

    def tool_highlight_tile(self, tile: Tile, colour: tuple):
        #if a tool is selected, the highlighting of tiles will be different
        linewidth = 3
        s = self.tilesize
        x = tile.location[1]-self.camera_position[0]
        y = tile.location[0]-self.camera_position[1]

        line1 = pygame.draw.line(self.screen, colour, (x*s, y*s), (x*s+s, y*s), width=linewidth)
        line2 = pygame.draw.line(self.screen, colour, (x*s, y*s),(x*s, y*s+s), width=linewidth)
        line3 = pygame.draw.line(self.screen, colour, (x*s, y*s+s),(x*s+s, y*s+s),width=linewidth)
        line4 = pygame.draw.line(self.screen, colour, (x*s+s, y*s),(x*s+s, y*s+s),width=linewidth)

        #this is used to calculate points for the lines that fill the tile
        variable = 2

        #their starting point is upleft and their end point is downright
        #splitline splits the tile from (x,y) to (x+tilesize, y+tilesize)
        splitline = pygame.draw.line(self.screen, colour, (x*s, y*s), (x*s+s, y*s+s), width=1)
        for line in range(int(s/2)):
            pygame.draw.line(self.screen, colour, (x*s+variable, y*s), (x*s+s, y*s+s-variable), width=1)
            pygame.draw.line(self.screen, colour, (x*s, y*s+s-variable), (x*s+variable, y*s+s), width=1)
            variable += 2


    def tools(self):
        #game tools defined here

        build = GameTool("Build", 0)
        build.set_colour((0,0,255))
        build_road = GameTool("Build Road", 0)
        build_road.set_colour((0,255,255))
        demolish = GameTool("Demolish", 0)
        demolish.create_button((910, 660), (50,50), "tool")
        demolish.button.set_tool(demolish)
        demolish.set_colour((255,128,0))
        upgrade = GameTool("Upgrade", 0)
        upgrade.create_button((970, 660),(50,50), "tool")
        upgrade.button.set_tool(upgrade)
        upgrade.set_colour((0,255,0))

        self.player_tools = [demolish, upgrade, build, build_road]
        self.ui_buttons.append(demolish.button)
        self.ui_buttons.append(upgrade.button)

    def open_tool(self, tool):
        tool.set_active(True)

    def close_tool(self):
        for tool in self.player_tools:
            tool.set_active(False)
        self.current_tool = None

    def draw_ui(self):

        self.bottombar()
        for button in self.ui_buttons:
            self.draw_button(button)
        if self.menu_open:
            for mbutton in self.ui_menu_buttons:
                self.draw_button(mbutton)

    def main_loop(self):

        #the main loop of the game runs here
        while True:
            self.update_screen()
            self.events()


class UIButton():

    def __init__(self, name: str, location: tuple, size: tuple, type: str):

        self.name = name
        self.location = location
        self.size = size
        self.menu = []
        self.tooltip = []
        self.type = type
        self.active = False
        self.passive = False
        self.keybind = None
        self.keybind_text = None
        self.graphic = None
        self.tool = None
        self.building = None

    def click(self):

        if self.active:
            self.active = False
        else:
            self.active = True

        if self.type == "tool":
            self.tool.set_active(True)
        if self.type == "building":
            self.tool.set_active(True)
        if self.type == "road":
            self.tool.set_active(True)

    def set_building(self, building: Building):
        #sets a building to match a button
        self.building = building


    def menu_addbutton(self, name: str, tier: int):

        #add a button to the pop up menu
        #tier indicates at what population tier
        #this button is unlocked
        self.menu.append((name, tier))


    def set_tool(self, tool):
        self.tool = tool

    def set_graphic(self, image: str):
        self.graphic = image

    def tooltip_addline(self, text: str):
        
        #add a line of text in the tooltip
        self.tooltip.append(text)

    def set_keybind(self, key: pygame.key, text: str):
        self.keybind = key
        self.keybind_text = text

    def set_active(self, value: bool):

        #set the menu status to value
        self.active = value

    def is_active(self):

        #check current menu status
        return self.active

    def __str__(self):

        return f"Button: {self.name}"

class GameTool():

    def __init__(self, name: str, admin: bool):
        self.name = name
        self.admin = admin
        self.active = False
        self.keybind = None
        self.keybind_text = None
        self.button = None
        self.colour = None
    
    def is_active(self):
        return self.active

    def set_colour(self, colour: tuple):
        #set the colour of the highlight when using tool
        self.colour = colour

    def set_active(self, value: bool):
        self.active = value

    def set_keybind(self, key: pygame.key, text: str):
        self.keybind = key
        self.keybind_text = text

    def create_button(self, location: tuple, size: tuple, type: str):
        self.button = UIButton(self.name, location, size, type)

    def __str__(self):

        return f"Tool: {self.name}"


if __name__ == "__main__":
    StrategyGame()