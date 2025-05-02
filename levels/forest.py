import pygame
import random
import math
from settings import *
from entities.player import Player
from entities.tree_boss import TreeBoss
from levels.level import Level
from ui.hud import HUD
from ui.menu import GameOverMenu, VictoryMenu

class ForestLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((30, 80, 40))  # Forest background
        
        # Create forest ground with roots
        self.ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        self.roots = []
        for i in range(5):
            x = random.randint(100, SCREEN_WIDTH - 100)
            width = random.randint(50, 150)
            height = random.randint(20, 40)
            self.roots.append(pygame.Rect(x, SCREEN_HEIGHT - 50 - height, width, height))
        
        # Create player
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.player_start_pos = pygame.Vector2(100, SCREEN_HEIGHT - 100)
        
        # Create tree boss
        self.tree_boss = TreeBoss(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.boss_defeated = False
        
        # UI
        self.hud = HUD(self.player)
        self.game_over_menu = GameOverMenu(self.game)
        self.victory_menu = VictoryMenu(self.game)
        
    def update(self, dt):
        # Update player
        self.player.update(dt)
        
        # Update tree boss if not defeated
        if not self.boss_defeated:
            self.tree_boss.update(dt, self.player)
            if self.tree_boss.health <= 0:
                self.boss_defeated = True
                self.victory_menu.active = True
                
        # Check for player death
        if self.player.health <= 0:
            self.game_over_menu.active = True
            
        # Handle collisions
        self.handle_collisions()
        
    def handle_collisions(self):
        # Ground collision
        if self.player.rect.colliderect(self.ground_rect):
            self.player.position.y = self.ground_rect.top - self.player.rect.height / 2
            self.player.velocity.y = 0
            self.player.on_ground = True
            
        # Root collisions (act as small platforms)
        self.player.on_ground = False
        for root in self.roots:
            if (self.player.rect.colliderect(root) and 
                self.player.velocity.y > 0 and 
                self.player.rect.bottom > root.top + 5):
                self.player.position.y = root.top - self.player.rect.height / 2
                self.player.velocity.y = 0
                self.player.on_ground = True
                
        # Player attacks boss
        if self.player.attacking and not self.boss_defeated:
            attack_rect, damage = self.player.attack()
            if attack_rect and attack_rect.colliderect(self.tree_boss.rect):
                self.tree_boss.take_damage(damage)
                
        # Boss attacks player
        if not self.boss_defeated:
            for attack in self.tree_boss.attacks:
                if attack['rect'].colliderect(self.player.rect):
                    parried = self.player.take_damage(attack['damage'])
                    if parried:
                        self.tree_boss.take_damage(attack['damage'] * PARRY_DAMAGE_RETURN)
                        
    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw ground and roots
        pygame.draw.rect(screen, (60, 40, 20), self.ground_rect)
        for root in self.roots:
            pygame.draw.rect(screen, (80, 60, 30), root)
            
        # Draw tree boss
        if not self.boss_defeated:
            self.tree_boss.draw(screen)
            
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        self.hud.draw(screen)
        
        # Draw game over menu if active
        if self.game_over_menu.active:
            self.game_over_menu.draw(screen)
            
        # Draw victory menu if active
        if self.victory_menu.active:
            self.victory_menu.draw(screen)
            
    def reset(self):
        self.player.position = self.player_start_pos
        self.player.health = self.player.max_health
        self.player.stamina = self.player.max_stamina
        self.player.mana = self.player.max_mana
        
        # Reset tree boss
        self.tree_boss.reset()
        self.boss_defeated = False
        
        self.game_over_menu.active = False
        self.victory_menu.active = False
