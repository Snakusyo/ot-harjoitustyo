import pygame
from pygame.locals import *
from pyrfc3339 import generate
from map.tiles import Tile
from random import randint

from mapmaker.mapmaker import generate_map

class StrategyGame():

    #running the game happens here
    
    def __init__(self):

        pygame.init()
        
        #this is placeholder for resolution and tilesize
        self.resx = 1280
        self.resy = 720
        self.tilesize = 16

        #this is placeholder for camera
        self.camera_position = [10, 10]
        self.camera_right, self.camera_down, self.camera_left, self.camera_up = False, False, False, False

        self.font_arial = pygame.font.SysFont("Arial", 22)
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.resx,self.resy))

        pygame.display.set_caption("ot-peliprojekti")


        #everything under this is currently for testing purposes only
        self.map = []
        self.mapsize = 128
        self.map_info = generate_map(self.mapsize)

        self.create_map(self.map_info)
        self.main_loop()

    def generate_map(self, size: int):

        #this method is only for testing purposes at the moment
        #it will generate map info as a list

        maplist = []

        for i in range(size):

            maprow = []
            for u in range(size):
                if i == 0 or i == (size-1):
                    maprow.append(0)
                elif u == 0 or u == (size-1):
                    maprow.append(0)

                else:
                    maprow.append(1)

        return maplist

    def main_menu(self):

        #this is used when loading the main menu
        #will be included later
        pass

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
        
        self.screen.fill((0,0,0))

        row = self.camera_position[0]
        for i in range(int(self.resx/self.tilesize)):
            tile = self.camera_position[1]
            
            for u in range(int(self.resy/self.tilesize)):
                
                #draw the tiles based on the camera position
                #camera position is defined by what tiles are shown on screen
                self.draw_tile(self.map[row][tile], i*self.tilesize, u*self.tilesize)
                tile += 1

            row += 1

        pygame.display.flip()
        self.game_clock.tick(60)





    def events(self):

        #events such as player input are tracked here

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                #camera movement keys here
                if event.key == pygame.K_UP:
                    self.camera_up = True
                if event.key == pygame.K_DOWN:
                    self.camera_down = True
                if event.key == pygame.K_LEFT:
                    self.camera_left = True
                if event.key == pygame.K_RIGHT:
                    self.camera_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.camera_up = False
                if event.key == pygame.K_DOWN:
                    self.camera_down = False
                if event.key == pygame.K_LEFT:
                    self.camera_left = False
                if event.key == pygame.K_RIGHT:
                    self.camera_right = False


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
            colour = (0,0,255)
        if tile.terrain == 1:
            colour = (0,255,0)
        if tile.terrain == 2:
            colour = (155,155,155)

        tile_graphic = pygame.draw.rect(self.screen, (colour), (x, y, self.tilesize, self.tilesize))

        return tile_graphic

    def draw_ui(self):

        #the user interface is drawn here
        pass

    def flash_border(self, colour: tuple):

        #highlights border in colour based on events such as errors or level ups
        pass

    def main_loop(self):

        #the main loop of the game runs here
        while True:
            self.update_screen()
            self.events()


if __name__ == "__main__":
    StrategyGame()