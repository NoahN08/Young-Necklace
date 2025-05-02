import pygame
from settings import *
from entities.player import Player
from levels.tutorial import TutorialLevel
from levels.cave import CaveLevel
from levels.forest import ForestLevel
from ui.menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Elden Ring 2D")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        
        # Game states
        self.main_menu = MainMenu(self)
        self.tutorial_level = TutorialLevel(self)
        self.cave_level = CaveLevel(self)
        self.forest_level = ForestLevel(self)
        self.current_level = None
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            if self.state == "menu":
                self.main_menu.update(dt)
                self.main_menu.draw(self.screen)
            elif self.state == "tutorial":
                self.current_level = self.tutorial_level
                self.current_level.update(dt)
                self.current_level.draw(self.screen)
            elif self.state == "cave":
                self.current_level = self.cave_level
                self.current_level.update(dt)
                self.current_level.draw(self.screen)
            elif self.state == "forest":
                self.current_level = self.forest_level
                self.current_level.update(dt)
                self.current_level.draw(self.screen)
                
            pygame.display.flip()
            
    def change_state(self, new_state):
        self.state = new_state
        if new_state != "menu":
            if new_state == "tutorial":
                self.tutorial_level.reset()
            elif new_state == "cave":
                self.cave_level.reset()
            elif new_state == "forest":
                self.forest_level.reset()

if __name__ == "__main__":
    game = Game()
    game.run()
