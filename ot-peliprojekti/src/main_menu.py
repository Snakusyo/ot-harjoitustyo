import pygame
from pygame.locals import *
from game import StrategyGame


class MainMenu():

    def __init__(self):

        pygame.init()

        #resolution and screen
        self.resx, self.resy = 1280, 720
        self.screen = pygame.display.set_mode((self.resx, self.resy))
        self.font_arial = pygame.font.SysFont("Arial", 18)
        self.game_clock = pygame.time.Clock()
        pygame.display.set_caption("ot-peliprojekti")

        #setup default values for mouseover
        self.mouseoverbutton = False

        #setup default button size
        self.button_height, self.button_width = 80, 200

        #setup default colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.lgray = (150,150,150)
        self.dgray = (50,50,50)

        self.current_menu = "Main Menu"
        self.current_buttons = None
        self.main_loop()

    def press_button(self, location: tuple):
        
        #determines what button is pressed
        x = location[0]
        y = location[1]

        for button in self.buttons:
            if x >= button.location[0] and x <= button.location[0]+button.size[0]:
                if y >= button.location[1] and y <= button.location[1]+button.size[1]:
                    button.click()
                    tteksti = button.name
                    print(tteksti)
            

    def open_menu(self, menu: str):

        #this determines what menu is opened
        pass

    def run_game(mode: int):

        #determines how to run the game
        #ie. new game, loaded game
        if mode == 0:
            StrategyGame()

    def draw_button(self, text: str, x: int, y: int):
        
        #determines what menu buttons look like
        #and where they appear

        button_tile = pygame.draw.rect(self.screen, self.lgray, (x, y, self.button_width, self.button_height))
        text = self.font_arial.render(text, True, self.black)
        button_text = self.screen.blit(text, (x+30,y+30))
        
        #lines of the button frame
        # (surface, colour, start(x,y), end(x,y), width)
        line1 = pygame.draw.line(self.screen, self.white, (x,y), (x+self.button_width, y), width=3)
        line2 = pygame.draw.line(self.screen, self.white, (x,y), (x,y+self.button_height), width=3)
        line3 = pygame.draw.line(self.screen, self.black, (x, y+self.button_height), (x+self.button_width, y+self.button_height), width=3)
        line4 = pygame.draw.line(self.screen, self.black, (x+self.button_width, y), (x+self.button_width, y+self.button_height), width=3)

        button_frame = [line1, line2, line3, line4]

        button_graphic = [button_tile, button_text, button_frame]

        return button_graphic

    def draw_menu(self, menu: str):

        #determine what to draw based on what menu
        #the player is in

        #different buttons
        newgame = Button("New Game", (540, 200), (self.button_width, self.button_height))
        loadgame = Button("Load Game", (540, 300), (self.button_width, self.button_height))
        exitgame = Button("Exit Game", (540, 400), (self.button_width, self.button_height))

        if menu == "Main Menu":
            button1 = self.draw_button(newgame.name, newgame.location[0], newgame.location[1])
            button2 = self.draw_button(loadgame.name, loadgame.location[0], loadgame.location[1])
            button3 = self.draw_button(exitgame.name, exitgame.location[0], exitgame.location[1])

            button_graphics = [button1, button2, button3]
            self.buttons = [newgame, loadgame, exitgame]
            self.button_coords = [(540,200), (540,300), (540,400)]

        return button_graphics

    def highlight_button(self, x,y):

        for coords in self.button_coords:
            if x >= coords[0] and x <= coords[0]+self.button_width:
                if y >= coords[1] and y <= coords[1]+self.button_height:
                    #setup the highlight lines (only two)
                    line1 = pygame.draw.line(self.screen, self.white, (coords[0], coords[1]+self.button_height), (coords[0]+self.button_width, coords[1]+self.button_height), width=3)
                    line2 = pygame.draw.line(self.screen, self.white, (coords[0]+self.button_width, coords[1]), (coords[0]+self.button_width, coords[1]+self.button_height), width=3)
                    #sets the current button, this is used to determine clicking
                    self.current_button = coords
                
        highlight_graphic = [line1, line2]
        return highlight_graphic


    def update_screen(self):

        #screen update happens here
        self.screen.fill(self.dgray)

        self.draw_menu(self.current_menu)

        #highlight button if it's under the mouse cursor
        if self.mouseoverbutton:
            self.highlight_button(self.mouse_position[0], self.mouse_position[1])


        pygame.display.flip()
        self.game_clock.tick(60)

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            self.mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if state[0]:
                    if self.mouseoverbutton:
                        self.press_button(self.mouse_position)

        for coords in self.button_coords:
            if self.mouse_position[0] >= coords[0] and self.mouse_position[0] <= coords[0]+self.button_width:
                if self.mouse_position[1] >= coords[1] and self.mouse_position[1] <= coords[1]+self.button_height:
                    self.mouseoverbutton = True
                    break
                else:
                    self.mouseoverbutton = False
            else:
                self.mouseoverbutton = False


    def main_loop(self):

        while True:
            self.update_screen()
            self.events()


class Button():

    def __init__(self, name: str, location: tuple, size: tuple):

        self.name = name
        self.location = location
        self.size = size

    def click(self):

        #this determines what happens when a selected button is pressed
        if self.name == "New Game":
            MainMenu.run_game(0)

    def get_button(self, coords: tuple):

        pass


if __name__ == "__main__":
    MainMenu()