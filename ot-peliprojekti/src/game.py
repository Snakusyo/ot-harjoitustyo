import pygame
from pygame.locals import *

class StrategyGame():

    #running the game happens here
    
    def __init__(self):

        pygame.init()
        
        self.font_arial = pygame.font.SysFont("Arial", 22)
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1280,720))

        pygame.display.set_caption("ot-peliprojekti")


    def draw_screen(self):

        #this is where drawing and updating the screen happens
        pass
        #adjusting the camera should also be here
        #drawing the user interface happens last so that it remains on top

    def events(self):

        #game events such as calculations and player input take place here
        pass

    def main_loop(self):

        #the main loop of the game runs here

        self.draw_screen()
        self.events()


if __name__ == "__main__":
    StrategyGame()