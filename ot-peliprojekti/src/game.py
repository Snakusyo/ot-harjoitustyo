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

    def new_game(self, map: list):

        #this function will reset all in game statistics and values
        #the map is used to call the start_game function
        pass

    def start_game(self):

        pass

    def update_screen(self):

        self.screen.fill((0,0,0))
        pygame.display.flip()

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

    def create_map(self, map: list):
        
        self.map = []

        for row in map:
            for item in row:
                item = Tile(item)

        for value in self.map:
            for thing in value:
                print(thing)


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

    def draw_tile(self, tile: Tile):
        
        #the map tiles are drawn here
        pass

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