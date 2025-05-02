import pygame
from settings import *

class Entity:
    def __init__(self, x, y, health, entity_type):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x - 25, y - 50, 50, 50)  # Default size, can be overridden
        self.max_health = health
        self.health = health
        self.type = entity_type
        self.facing_right = True
        self.on_ground = False
        self.invincible = False
        self.invincibility_timer = 0
        
    def update(self, dt):
        # Update invincibility frames
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
                
        # Apply gravity
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt
        self.rect.midbottom = self.position
        
    def take_damage(self, damage):
        if self.invincible:
            return False
            
        self.health -= damage
        self.invincible = True
        self.invincibility_timer = 0.5  # Half second invincibility after being hit
        
        if self.health <= 0:
            self.die()
            return True
        return False
        
    def die(self):
        pass  # To be implemented by child classes
        
    def draw(self, screen):
        # Base entity is just a red rectangle (should be overridden)
        color = RED if not self.invincible else (255, 150, 150)
        pygame.draw.rect(screen, color, self.rect)
