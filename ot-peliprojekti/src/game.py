import pygame
from pygame.locals import *
from map.tiles import Tile

class StrategyGame():

    #running the game happens here
    
    def __init__(self):

        pygame.init()
        
        self.font_arial = pygame.font.SysFont("Arial", 22)
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280,720))

        pygame.display.set_caption("ot-peliprojekti")


        #everything under this is currently for testing purposes only
        
        self.map_info = [\
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] \
                ]

        self.create_map(self.map_info)
        self.main_loop()


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
        pygame.display.flip()



    def events(self):

        #events such as player input are tracked here

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

    def create_map(self, map: list):
        
        #map information is extracted from an array and converted into Tile class objects

        self.map = []

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
        pass

    def draw_tile(self, tile: Tile, x: int, y: int):
        
        #the map tiles are drawn here
        #colours are placeholders for final graphic
        
        if tile.terrain == 0:
            colour = (0,0,255)
        if tile.terrain == 1:
            colour = (0,255,0)
        if tile.terrain == 2:
            colour = (155,155,155)

        tile_graphic = pygame.draw.rect(self.screen, (colour), (x, y, 16, 16))

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