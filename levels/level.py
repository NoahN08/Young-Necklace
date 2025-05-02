import pygame
from settings import *

class Level:
    def __init__(self, game):
        self.game = game
        self.background = None
        self.player = None
        self.enemies = []
        
    def update(self, dt):
        pass
        
    def draw(self, screen):
        pass
        
    def handle_collisions(self):
        pass
        
    def reset(self):
        pass
