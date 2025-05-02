import pygame
from settings import *

class Enemy:
    def __init__(self, x, y, health, enemy_type):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x - 25, y - 50, 50, 50)
        self.max_health = health
        self.health = health
        self.type = enemy_type
        self.facing_right = False
        self.on_ground = False
        self.attacks = []
        
    def update(self, dt, player):
        # Update attack timers
        for attack in self.attacks[:]:
            attack['timer'] -= dt
            if attack['timer'] <= 0:
                self.attacks.remove(attack)
                
        # Apply gravity
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt
        self.rect.midbottom = self.position
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
        
    def die(self):
        pass  # To be overridden by specific enemies
        
    def reset(self):
        self.health = self.max_health
        self.attacks = []
        self.velocity = pygame.Vector2(0, 0)
        
    def draw(self, screen):
        # Basic enemy drawing (should be overridden)
        pygame.draw.rect(screen, RED, self.rect)
