import pygame
import random
import math
from entities.enemy import Enemy
from settings import *

class TreeBoss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, BOSS_BASE_HEALTH * 2, "tree_boss")
        self.rect = pygame.Rect(x - 60, y - 400, 120, 400)  # Tall hitbox
        self.speed = 80  # Trees don't move fast!
        self.attack_cooldown = 0
        self.attack_patterns = []
        self.current_pattern = []
        self.current_attack_index = 0
        
        # Phases
        self.phase = 1
        self.phase2_threshold = self.max_health * 0.6
        self.phase3_threshold = self.max_health * 0.3
        
        # Initialize attack patterns
        self.init_attack_patterns()
        
    def init_attack_patterns(self):
        # Phase 1 patterns (basic attacks)
        self.phase1_patterns = [
            [{"type": "root_strike", "damage": 25, "windup": 0.8, "duration": 0.4, "cooldown": 2.0}],
            [{"type": "root_slam", "damage": 40, "windup": 1.0, "duration": 0.5, "cooldown": 3.0}],
            [{"type": "seed_burst", "damage": 15, "windup": 0.6, "duration": 1.0, "cooldown": 2.5}]
        ]
        
        # Phase 2 patterns (more aggressive)
        self.phase2_patterns = [
            [{"type": "root_strike", "damage": 25, "windup": 0.6, "duration": 0.4, "cooldown": 1.5},
             {"type": "root_strike", "damage": 25, "windup": 0.6, "duration": 0.4, "cooldown": 1.5}],
            [{"type": "root_slam", "damage": 40, "windup": 0.8, "duration": 0.5, "cooldown": 2.5},
             {"type": "seed_burst", "damage": 15, "windup": 0.5, "duration": 1.0, "cooldown": 2.0}]
        ]
        
        # Phase 3 patterns (desperation attacks)
        self.phase3_patterns = [
            [{"type": "root_storm", "damage": 20, "windup": 1.0, "duration": 2.0, "cooldown": 4.0}],
            [{"type": "seed_rain", "damage": 15, "windup": 0.8, "duration": 3.0, "cooldown": 5.0}]
        ]
        
        self.current_pattern = random.choice(self.phase1_patterns)
        
    def ai_update(self, dt, player):
        # Check for phase transitions
        if self.health < self.phase2_threshold and self.phase == 1:
            self.phase = 2
        elif self.health < self.phase3_threshold and self.phase == 2:
            self.phase = 3
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            return
            
        # Select appropriate pattern based on phase
        if self.phase == 1:
            patterns = self.phase1_patterns
        elif self.phase == 2:
            patterns = self.phase2_patterns
        else:
            patterns = self.phase3_patterns
            
        # If current pattern is finished, select a new one
        if self.current_attack_index >= len(self.current_pattern):
            self.current_pattern = random.choice(patterns)
            self.current_attack_index = 0
            
        # Execute current attack
        self.execute_attack(dt, player)
        
    def execute_attack(self, dt, player):
        attack = self.current_pattern[self.current_attack_index]
        
        if attack["type"] == "root_strike":
            # Strike with a root from below
            strike_x = player.position.x + random.randint(-50, 50)
            strike_rect = pygame.Rect(strike_x - 20, SCREEN_HEIGHT - 50, 40, 150)
            self.attacks.append({
                "rect": strike_rect,
                "damage": attack["damage"],
                "timer": attack["duration"]
            })
            
        elif attack["type"] == "root_slam":
            # Slam multiple roots in an area
            for i in range(3):
                strike_x = player.position.x + random.randint(-100, 100)
                strike_rect = pygame.Rect(strike_x - 25, SCREEN_HEIGHT - 50, 50, 200)
                self.attacks.append({
                    "rect": strike_rect,
                    "damage": attack["damage"],
                    "timer": attack["duration"]
                })
                
        elif attack["type"] == "seed_burst":
            # Burst seed pods in multiple directions (handled in projectile system)
            pass
            
        elif attack["type"] == "root_storm":
            # Create roots across the entire arena
            pass  # Implement multi-root attack
            
        elif attack["type"] == "seed_rain":
            # Rain seeds across the entire arena
            pass  # Implement area attack
            
        # Move to next attack in pattern
        self.attack_cooldown = attack["cooldown"]
        self.current_attack_index += 1
        
    def draw(self, screen):
        # Draw tree trunk
        trunk_color = (90, 60, 40) if not self.invincible else (120, 90, 60)
        pygame.draw.rect(screen, trunk_color, self.rect)
        
        # Draw tree canopy
        canopy_rect = pygame.Rect(self.rect.x - 60, self.rect.y - 150, 180, 150)
        canopy_color = (40, 90, 50) if not self.stunned else (80, 120, 70)
        pygame.draw.ellipse(screen, canopy_color, canopy_rect)
        
        # Draw roots (attack indicators)
        for attack in self.attacks:
            if attack["type"] in ["root_strike", "root_slam"]:
                pygame.draw.rect(screen, (120, 80, 60), attack['rect'])
                
        # Draw health bar (multiple segments for phases)
        health_width = 180
        health_height = 15
        
        # Draw background
        pygame.draw.rect(screen, RED, (self.rect.x - 30, self.rect.y - 170, health_width, health_height))
        
        # Draw current phase health
        if self.phase == 1:
            health_ratio = (self.health - self.phase2_threshold) / (self.max_health - self.phase2_threshold)
            pygame.draw.rect(screen, GREEN, (self.rect.x - 30, self.rect.y - 170, health_width * health_ratio, health_height))
        elif self.phase == 2:
            health_ratio = (self.health - self.phase3_threshold) / (self.phase2_threshold - self.phase3_threshold)
            pygame.draw.rect(screen, GREEN, (self.rect.x - 30, self.rect.y - 170, health_width * health_ratio, health_height))
            # Draw phase 1 as yellow
            phase1_ratio = (self.phase2_threshold - self.phase3_threshold) / (self.max_health - self.phase3_threshold)
            pygame.draw.rect(screen, (200, 200, 0), (self.rect.x - 30, self.rect.y - 170, health_width * phase1_ratio, health_height))
        else:
            health_ratio = self.health / self.phase3_threshold
            pygame.draw.rect(screen, GREEN, (self.rect.x - 30, self.rect.y - 170, health_width * health_ratio, health_height))
            # Draw phase 2 as yellow
            phase2_ratio = (self.phase2_threshold - self.phase3_threshold) / (self.max_health - self.phase3_threshold)
            pygame.draw.rect(screen, (200, 200, 0), (self.rect.x - 30, self.rect.y - 170, health_width * phase2_ratio, health_height))
            # Draw phase 1 as orange
            phase1_ratio = (self.max_health - self.phase2_threshold) / (self.max_health - self.phase3_threshold)
            pygame.draw.rect(screen, (255, 150, 0), (self.rect.x - 30, self.rect.y - 170, health_width * phase1_ratio, health_height))
        
        # Draw phase indicator
        font = pygame.font.SysFont(None, 24)
        phase_text = font.render(f"Phase {self.phase}", True, WHITE)
        screen.blit(phase_text, (self.rect.x + health_width // 2 - 40, self.rect.y - 190))
