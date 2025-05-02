import pygame
import random
from entities.enemy import Enemy
from settings import *

class EliteSkeleton(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, BOSS_BASE_HEALTH, "elite_skeleton")
        self.rect = pygame.Rect(x - 30, y - 70, 60, 70)  # Taller hitbox
        self.speed = 160
        self.attack_cooldown = 0
        self.attack_patterns = []
        self.current_pattern = []
        self.current_attack_index = 0
        
        # Shield mechanics
        self.shield_health = 50
        self.max_shield_health = 50
        self.shield_cooldown = 0
        self.shield_regen_time = 5.0
        
        # Initialize attack patterns
        self.init_attack_patterns()
        
    def init_attack_patterns(self):
        # Pattern 1: Shield bash combo
        self.attack_patterns.append([
            {"type": "shield_bash", "damage": 25, "windup": 0.5, "duration": 0.3, "cooldown": 1.0},
            {"type": "sword_slash", "damage": 30, "windup": 0.3, "duration": 0.2, "cooldown": 1.0},
            {"type": "shield_slam", "damage": 40, "windup": 0.7, "duration": 0.4, "cooldown": 1.5}
        ])
        
        # Pattern 2: Ranged attacks
        self.attack_patterns.append([
            {"type": "bone_throw", "damage": 20, "windup": 0.4, "duration": 0.5, "cooldown": 1.0},
            {"type": "bone_throw", "damage": 20, "windup": 0.4, "duration": 0.5, "cooldown": 1.0},
            {"type": "bone_storm", "damage": 15, "windup": 1.0, "duration": 2.0, "cooldown": 3.0}
        ])
        
        self.current_pattern = random.choice(self.attack_patterns)
        
    def ai_update(self, dt, player):
        # Regenerate shield if broken
        if self.shield_health <= 0 and self.shield_cooldown > 0:
            self.shield_cooldown -= dt
            if self.shield_cooldown <= 0:
                self.shield_health = self.max_shield_health
                
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
            
        # Check distance to player for attacks
        dist_to_player = abs(self.position.x - player.position.x)
        if dist_to_player < 200:
            self.execute_attack(dt, player)
            
    def execute_attack(self, dt, player):
        if self.current_attack_index >= len(self.current_pattern):
            # Get a new random pattern
            self.current_pattern = random.choice(self.attack_patterns)
            self.current_attack_index = 0
            
        attack = self.current_pattern[self.current_attack_index]
        
        if attack["type"] == "shield_bash":
            # Bash with shield
            direction = 1 if player.position.x > self.position.x else -1
            self.velocity.x = direction * self.speed * 1.5
            
            # Create attack hitbox
            attack_rect = pygame.Rect(0, 0, 80, 60)
            if direction > 0:
                attack_rect.midleft = self.rect.midright
            else:
                attack_rect.midright = self.rect.midleft
            self.attacks.append({
                "rect": attack_rect,
                "damage": attack["damage"],
                "timer": attack["duration"]
            })
            
        elif attack["type"] == "sword_slash":
            # Slash with sword
            direction = 1 if player.position.x > self.position.x else -1
            
            # Create attack hitbox
            attack_rect = pygame.Rect(0, 0, 100, 40)
            if direction > 0:
                attack_rect.midleft = self.rect.midright
            else:
                attack_rect.midright = self.rect.midleft
            self.attacks.append({
                "rect": attack_rect,
                "damage": attack["damage"],
                "timer": attack["duration"]
            })
            
        elif attack["type"] == "shield_slam":
            # Jump and slam with shield
            self.velocity.y = -400
            
            # Create AOE hitbox when landing
            if self.on_ground and self.velocity.y > 0:
                attack_rect = pygame.Rect(self.rect.x - 30, self.rect.y, self.rect.width + 60, 40)
                self.attacks.append({
                    "rect": attack_rect,
                    "damage": attack["damage"],
                    "timer": attack["duration"]
                })
                
        elif attack["type"] == "bone_throw":
            # Throw a bone projectile (handled in projectile system)
            pass
            
        elif attack["type"] == "bone_storm":
            # Create multiple bone projectiles (handled in projectile system)
            pass
            
        # Move to next attack in pattern
        self.attack_cooldown = attack["cooldown"]
        self.current_attack_index += 1
        
    def take_damage(self, damage):
        # Shield absorbs damage first
        if self.shield_health > 0:
            self.shield_health -= damage
            if self.shield_health <= 0:
                self.shield_cooldown = self.shield_regen_time
                damage = abs(self.shield_health)  # Remaining damage goes to health
                self.shield_health = 0
            else:
                return False
                
        # Apply remaining damage to health
        return super().take_damage(damage)
        
    def draw(self, screen):
        # Draw skeleton body
        body_color = (200, 200, 200) if not self.invincible else (230, 230, 230)
        pygame.draw.rect(screen, body_color, self.rect)
        
        # Draw shield if active
        if self.shield_health > 0:
            shield_rect = pygame.Rect(self.rect.x - 10, self.rect.y - 10, 
                                    self.rect.width + 20, self.rect.height + 20)
            pygame.draw.rect(screen, (150, 150, 200, 150), shield_rect, 3)
            
        # Draw sword
        sword_rect = pygame.Rect(0, 0, 60, 15)
        if self.facing_right:
            sword_rect.midleft = self.rect.midright
        else:
            sword_rect.midright = self.rect.midleft
        pygame.draw.rect(screen, (180, 180, 180), sword_rect)
        
        # Draw health bar
        health_width = self.rect.width + 40
        health_height = 10
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.rect.x - 20, self.rect.y - 30, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.rect.x - 20, self.rect.y - 30, health_width * health_ratio, health_height))
        
        # Draw shield bar if active
        if self.shield_health > 0:
            shield_ratio = self.shield_health / self.max_shield_health
            pygame.draw.rect(screen, (70, 70, 150), (self.rect.x - 20, self.rect.y - 20, health_width, health_height))
            pygame.draw.rect(screen, BLUE, (self.rect.x - 20, self.rect.y - 20, health_width * shield_ratio, health_height))
