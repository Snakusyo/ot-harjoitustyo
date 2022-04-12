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
        self.tilesize = 64

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

        #setup default colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.lgray = (150,150,150)
        self.mgray = (100,100,100)
        self.dgray = (50,50,50)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)


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
            self.highligh_tile(self.mouse_position[0], self.mouse_position[1], self.red)


        self.draw_ui()
        if self.mouseoverbutton:
            #highlight button under the mouse cursor
            self.highlight_button(self.mouse_position[0], self.mouse_position[1])
        if self.menu_open:
            self.draw_menu()        
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
                else:
                    self.mouseovertile = False
            else:
                self.mouseovertile = False

            #if mouse position is on a ui button, that button should be highlighted
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
            if self.current_button.is_active():
                self.menu_open = True
            else:
                self.close_menu()


    def create_map(self, map: list):
        
        #map information is extracted from an array and converted into Tile class objects


        for row in map:
            newrow = []
            for item in row:
                newrow.append(Tile(item))
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

        return tile_graphic

    def highligh_tile(self, mousex: float, mousey: float, colour: tuple):
        #this method is called when a tile on screen needs to be highlighted

        linewidth = 3

        tilex = int(mousex/self.tilesize)
        tiley = int(mousey/self.tilesize)

        line1 = pygame.draw.line(self.screen, colour, (tilex*self.tilesize, tiley*self.tilesize), (tilex*self.tilesize+self.tilesize, tiley*self.tilesize), width=linewidth)
        line2 = pygame.draw.line(self.screen, colour, (tilex*self.tilesize, tiley*self.tilesize), (tilex*self.tilesize, tiley*self.tilesize+self.tilesize), width=linewidth)
        line3 = pygame.draw.line(self.screen, colour, (tilex*self.tilesize, tiley*self.tilesize+self.tilesize), (tilex*self.tilesize+self.tilesize, tiley*self.tilesize+self.tilesize), width=linewidth)
        line4 = pygame.draw.line(self.screen, colour, (tilex*self.tilesize+self.tilesize, tiley*self.tilesize), (tilex*self.tilesize+self.tilesize, tiley*self.tilesize+self.tilesize), width=linewidth)

        highlight_graphic = [line1, line2, line3, line4]
        self.highlighted_tile = (tilex, tiley)

        return highlight_graphic
        
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

        #define the buttons on the UI
        road = UIButton("Road", (500, 640), (70,70))
        road.menu_addbutton("Dirt Road", "build")
        houses = UIButton("Houses", (580, 640), (70,70))
        houses.menu_addbutton("Small House", "build")
        houses.menu_addbutton("Medium House", "build")
        houses.menu_addbutton("Large House", "build")
        gathering = UIButton("Gathering", (660, 640), (70,70))
        production = UIButton("Production", (740, 640), (70,70))
        self.ui_buttons = [road, houses, gathering, production]

    def draw_button(self, location: tuple, size:tuple):

        x = location[0]
        y = location[1]
        button_fill = pygame.draw.rect(self.screen, self.lgray, (x, y, size[0], size[1]))

        #button frame determined here
        line1 = pygame.draw.line(self.screen, self.white, (x,y), (x+size[0], y), width=3)
        line2 = pygame.draw.line(self.screen, self.white, (x,y), (x, y+size[1]), width=3)
        line3 = pygame.draw.line(self.screen, self.black, (x,y+size[1]), (x+size[0], y+size[1]), width=3)
        line4 = pygame.draw.line(self.screen, self.black, (x+size[0],y), (x+size[0], y+size[1]), width=3)
        button_frame = [line1,line2,line3,line4]
        button = [button_fill, button_frame]

        return button

    def highlight_button(self, x: int, y: int):
        #this method is called when a button on screen needs to be highlighted
        #first it checks which button is under the cursor
        for button in self.ui_buttons:
            if x >= button.location[0] and x <= button.location[0]+button.size[0]:
                if y >= button.location[1] and y <= button.location[1]+button.size[1]:
                    #setup two lines for highlight
                    line1 = pygame.draw.line(self.screen, self.white, (button.location[0], button.location[1]+button.size[1]), (button.location[0]+button.size[0], button.location[1]+button.size[1]), width=3)
                    line2 = pygame.draw.line(self.screen, self.white, (button.location[0]+button.size[0], button.location[1]), (button.location[0]+button.size[0], button.location[1]+button.size[1]), width=3)
                    self.current_button = button

        highlight_graphic = [line1, line2]
        return highlight_graphic

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
        else:
            self.close_menu()

    def draw_menu(self):

        button = self.current_button
        x = button.location[0]
        y = button.location[1]
        edgey = y-80*len(button.menu)
        menu_frame = pygame.draw.rect(self.screen, self.black, (x-13,edgey-13,93,80*len(button.menu)+10))
        menu_inner = pygame.draw.rect(self.screen, self.mgray, (x-10, edgey-10, 87, 80*len(button.menu)+4))

        self.draw_button

        #
        #
        #
        # YOU ARE HERE
        # FINISH THE POP UP MENU WITH THE BUTTONS
        #
        #
        #



    def close_menu(self):
        self.menu_open = False
        self.current_menu = None
        self.current_button.set_active(False)

    def open_window(self, name: str):
        
        #opens a new window in game
        pass

    def draw_ui(self):

        self.bottombar()
        for button in self.ui_buttons:
            self.draw_button(button.location, button.size)

    def flash_border(self, colour: tuple):

        #highlights border in colour based on events such as errors or level ups
        pass

    def main_loop(self):

        #the main loop of the game runs here
        while True:
            self.update_screen()
            self.events()

class UIButton():

    def __init__(self, name: str, location: tuple, size: tuple):

        self.name = name
        self.location = location
        self.size = size
        self.menu = []
        self.tooltip = []
        self.active = False
        self.passive = False

    def click(self):

        if self.passive == False:
            if self.active:
                self.active = False
            else:
                self.active = True


    def menu_addbutton(self, name: str, type: str):

        #add a button to the pop up menu
        self.menu.append((name, type))
        pass

    def tooltip_addline(self, text: str):
        
        #add a line of text in the tooltip
        self.tooltip.append(text)

    def set_active(self, value: bool):

        #set the menu status to value
        self.active = value

    def is_active(self):

        #check current menu status
        return self.active
    
    def make_passive(self):
        self.passive = True

    def __str__(self):

        return f"Button: {self.name}"


if __name__ == "__main__":
    StrategyGame()