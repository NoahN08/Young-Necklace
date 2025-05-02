
import pygame
import random
from settings import *
from entities.enemy import Enemy

class Skeleton(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 50, "skeleton")
        self.speed = 120
        self.attack_cooldown = 0
        self.attack_range = 60
        
    def update(self, dt, player):
        super().update(dt, player)
        
        # Basic AI movement
        direction = player.position - self.position
        distance = direction.length()
        
        if distance < self.attack_range and self.attack_cooldown <= 0:
            # Attack player
            attack_rect = pygame.Rect(self.rect.x - 10, self.rect.y, 
                                    self.rect.width + 20, self.rect.height)
            self.attacks.append({
                "rect": attack_rect,
                "damage": 10,
                "timer": 0.2
            })
            self.attack_cooldown = 1.5
        elif distance < 300:
            # Move towards player
            if direction.length() > 0:
                direction = direction.normalize()
            self.velocity.x = direction.x * self.speed
            self.facing_right = direction.x > 0
        else:
            self.velocity.x = 0
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
    def draw(self, screen):
        color = (200, 200, 200) if not self.invincible else (230, 230, 230)
        pygame.draw.rect(screen, color, self.rect)
