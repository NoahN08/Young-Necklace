import pygame
import math
import random
from entities.enemy import Enemy
from settings import *

class SpiderBoss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, BOSS_BASE_HEALTH * 1.5, "spider_boss")
        self.rect = pygame.Rect(x - 40, y - 60, 80, 60)  # Larger hitbox
        self.speed = 180
        self.attack_cooldown = 0
        self.attack_patterns = []
        self.current_pattern = []
        self.current_attack_index = 0
        self.legs = 8
        self.web_shot_cooldown = 0
        
        # Initialize attack patterns
        self.init_attack_patterns()
        
    def init_attack_patterns(self):
        # Pattern 1: Melee combo
        self.attack_patterns.append([
            {"type": "lunge", "damage": 30, "windup": 0.5, "duration": 0.3, "cooldown": 1.0},
            {"type": "lunge", "damage": 30, "windup": 0.3, "duration": 0.3, "cooldown": 1.0},
            {"type": "slam", "damage": 50, "windup": 0.7, "duration": 0.5, "cooldown": 2.0}
        ])
        
        # Pattern 2: Web attacks
        self.attack_patterns.append([
            {"type": "web_shot", "damage": 20, "windup": 0.5, "duration": 0.5, "cooldown": 1.5},
            {"type": "web_shot", "damage": 20, "windup": 0.5, "duration": 0.5, "cooldown": 1.5},
            {"type": "web_trap", "damage": 10, "windup": 1.0, "duration": 3.0, "cooldown": 3.0}
        ])
        
        self.current_pattern = random.choice(self.attack_patterns)
        
    def ai_update(self, dt, player):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            return
            
        # Move toward player when not attacking
        if player.position.x < self.position.x:
            self.velocity.x = -self.speed
            self.facing_right = False
        else:
            self.velocity.x = self.speed
            self.facing_right = True
            
        # Jump occasionally
        if random.random() < 0.01 and self.on_ground:
            self.velocity.y = -400
            
        # Check distance to player for attacks
        dist_to_player = abs(self.position.x - player.position.x)
        if dist_to_player < 250 and self.on_ground:
            self.execute_attack(dt, player)
            
    def execute_attack(self, dt, player):
        if self.current_attack_index >= len(self.current_pattern):
            # Get a new random pattern
            self.current_pattern = random.choice(self.attack_patterns)
            self.current_attack_index = 0
            
        attack = self.current_pattern[self.current_attack_index]
        
        if attack["type"] == "lunge":
            # Lunge toward player
            direction = 1 if player.position.x > self.position.x else -1
            self.velocity.x = direction * self.speed * 2
            self.velocity.y = -100
            
            # Create attack hitbox
            attack_rect = pygame.Rect(0, 0, 100, 60)
            attack_rect.midbottom = self.rect.midbottom
            self.attacks.append({
                "rect": attack_rect,
                "damage": attack["damage"],
                "timer": attack["duration"]
            })
            
        elif attack["type"] == "slam":
            # Jump then slam down
            self.velocity.y = -500
            
            # Create AOE hitbox when landing
            if self.on_ground and self.velocity.y > 0:
                attack_rect = pygame.Rect(self.rect.x - 50, self.rect.y, self.rect.width + 100, 50)
                self.attacks.append({
                    "rect": attack_rect,
                    "damage": attack["damage"],
                    "timer": attack["duration"]
                })
                
        elif attack["type"] == "web_shot":
            # Shoot web projectile (handled in projectile system)
            pass
            
        elif attack["type"] == "web_trap":
            # Create web trap on ground (handled in trap system)
            pass
            
        # Move to next attack in pattern
        self.attack_cooldown = attack["cooldown"]
        self.current_attack_index += 1
        
    def draw(self, screen):
        # Draw spider body
        color = (70, 40, 90) if not self.invincible else (120, 80, 120)
        pygame.draw.ellipse(screen, color, self.rect)
        
        # Draw legs
        for i in range(self.legs):
            angle = i * (360 / self.legs)
            leg_length = 40
            leg_x = self.rect.centerx + math.cos(math.radians(angle)) * 30
            leg_y = self.rect.centery + math.sin(math.radians(angle)) * 30
            end_x = leg_x + math.cos(math.radians(angle)) * leg_length
            end_y = leg_y + math.sin(math.radians(angle)) * leg_length
            pygame.draw.line(screen, (90, 60, 100), (leg_x, leg_y), (end_x, end_y), 5)
            
        # Draw eyes
        eye_color = RED if not self.stunned else (200, 200, 200)
        pygame.draw.circle(screen, eye_color, (self.rect.centerx - 15, self.rect.centery - 10), 8)
        pygame.draw.circle(screen, eye_color, (self.rect.centerx + 15, self.rect.centery - 10), 8)
        
        # Draw health bar
        health_width = self.rect.width
        health_height = 10
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20, health_width * health_ratio, health_height))
