import pygame
from pygame.locals import *
from map.tiles import Tile
from random import randint

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

        #setup default colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.lgray = (150,150,150)
        self.mgray = (100,100,100)
        self.dgray = (50,50,50)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)

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

        self.create_map(self.map_info)
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
                    maprow.append(randint(0,1))
            maplist.append(maprow)

        print(maplist)
        return maplist

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
                self.draw_tile(self.map[row][tile], i*self.tilesize, u*self.tilesize)
                screenrow.append(self.map[row][tile])
                row += 1
            self.tiles_on_screen.append(screenrow)
            tile += 1
        if self.mouseovertile:
            #highlight tile under the mouse cursor
            self.highligh_tile(self.current_tile, self.white)

        if self.current_tool:
            if self.current_tool.is_active():
                self.draw_tool(self.current_tool)

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


            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if state[0]:
                    if self.mouseoverbutton:
                        self.current_button.click()

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
                        self.tooltip_active = False
                else:
                    self.mouseoverbutton = False
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
                            self.tooltip_active = False
                    else:
                        self.mouseoverbutton = False
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

        #are windows or menus open
        if self.current_button:
            if self.current_button.type == "main":
                if self.current_button.is_active():
                    self.open_menu(self.current_button.menu)
                    self.menu_location = self.current_button.location
                else:
                    self.close_menu()

    def create_map(self, map: list):
        
        #map information is extracted from an array and converted into Tile class objects
        y = 0
        for row in map:
            newrow = []
            x = 0
            for item in row:
                newrow.append(Tile((x, y), item))
                x += 1
            y += 1
            self.map.append(newrow)

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
        #colours are placeholders for final graphic
        
        if tile.terrain == 0:
            colour = self.blue
        if tile.terrain == 1:
            colour = self.green
        if tile.terrain == 2:
            colour = self.dgray

        tile_graphic = pygame.draw.rect(self.screen, (colour), (x, y, self.tilesize, self.tilesize))

    def highligh_tile(self, tile: Tile, colour: tuple):
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
        houses = UIButton("Houses", (580, 640), (70,70), "main")
        houses.menu_addbutton("House", 0)
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

        #draw the button frame
        line1 = pygame.draw.line(self.screen, self.white, (x,y), (x+sx, y), width=3)
        line2 = pygame.draw.line(self.screen, self.white,(x, y+sy), (x,y), width=3) 
        line3 = pygame.draw.line(self.screen, self.black,(x, y+sy), (x+sx, y+sy), width=3)
        line4 = pygame.draw.line(self.screen, self.black, (x+sx, y), (x+sx, y+sy), width=3)
        text = self.font_arial.render(button.keybind_text, True, self.black)
        frame_text = self.screen.blit(text,(x+5, y+5))

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
                new_button = UIButton(item[0], (x,y), (70,70), "sub")
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

    def tools(self):
        #game tools defined here

        build = GameTool("Build", 0)
        build.create_button((850, 660), (50,50))
        demolish = GameTool("Demolish", 0)
        demolish.create_button((910, 660), (50,50))
        upgrade = GameTool("Upgrade", 0)
        upgrade.create_button((970, 660),(50,50))

        self.player_tools = [build, demolish, upgrade]
        for tool in self.player_tools:
            self.ui_buttons.append(tool.button)

    def open_tool(self, tool):
        tool.set_active(True)

    def draw_tool(self, tool):
        #graphics for the selected tool

        if self.current_tool == "build":
            self.highligh_tile()
        if self.current_tool == "demolish":
            pass
        if self.current_tool == "upgrade":
            pass

    def draw_ui(self):

        self.bottombar()
        for button in self.ui_buttons:
            self.draw_button(button)
        if self.menu_open:
            for mbutton in self.ui_menu_buttons:
                self.draw_button(mbutton)
        for tool in self.player_tools:
            self.draw_button(tool.button)

    def flash_border(self, colour: tuple):

        #highlights border in colour based on events such as errors or level ups
        pass

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

    def click(self):

        if self.passive == False:
            if self.active:
                self.active = False
            else:
                self.active = True


    def menu_addbutton(self, name: str, tier: int):

        #add a button to the pop up menu
        #tier indicates at what population tier this button is unlocked
        self.menu.append((name, tier))

    def set_graphic(self, image: str):
        #set an image to show on the button
        pass

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
    
    def click(self):
        if self.active == False:
            self.set_active(True)
        else:
            self.set_active(False)

    def is_active(self):
        return self.active

    def set_active(self, value: bool):
        self.active = value

    def set_keybind(self, key: pygame.key, text: str):
        self.keybind = key
        self.keybind_text = text

    def create_button(self, location: tuple, size: tuple):
        self.button = UIButton(self.name, location, size, "main")

    def __str__(self):

        return f"Tool: {self.name}"


if __name__ == "__main__":
    StrategyGame()