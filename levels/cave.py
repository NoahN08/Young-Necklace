import pygame
import random
from settings import *
from entities.player import Player
from entities.skeleton import Skeleton
from entities.elite_skeleton import EliteSkeleton
from items.weapon import Weapon
from levels.level import Level
from ui.hud import HUD
from ui.menu import GameOverMenu, StatMenu

class CaveLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((20, 20, 30))  # Dark cave background
        
        # Create cave layout
        self.ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        self.platforms = [
            pygame.Rect(200, 500, 150, 20),
            pygame.Rect(400, 400, 150, 20),
            pygame.Rect(600, 550, 150, 20),
            pygame.Rect(800, 450, 150, 20),
            pygame.Rect(1000, 350, 150, 20)
        ]
        
        # Pit trap
        self.pit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, 200, 50)
        
        # Create player
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.player_start_pos = pygame.Vector2(100, SCREEN_HEIGHT - 100)
        
        # Create enemies
        self.enemies = []
        self.spawn_enemies()
        
        # Create elite skeleton (boss)
        self.elite_skeleton = EliteSkeleton(1100, SCREEN_HEIGHT - 100)
        self.elite_defeated = False
        
        # UI
        self.hud = HUD(self.player)
        self.game_over_menu = GameOverMenu(self.game)
        self.stat_menu = StatMenu(self.player)
        
        # Checkpoint
        self.checkpoint = pygame.Rect(300, SCREEN_HEIGHT - 100, 50, 50)
        self.reached_checkpoint = False
        self.show_checkpoint_message = False
        self.checkpoint_message_timer = 0
        
        # Pit fall transition
        self.falling = False
        self.fall_timer = 0
        self.fall_duration = 1.5
        
    def spawn_enemies(self):
        # Spawn regular skeletons
        for i in range(5):
            x = random.randint(200, SCREEN_WIDTH - 200)
            y = SCREEN_HEIGHT - 100
            skeleton = Skeleton(x, y)
            self.enemies.append(skeleton)
            
    def update(self, dt):
        # Check for pit fall
        if not self.falling and self.player.rect.colliderect(self.pit_rect):
            self.falling = True
            self.fall_timer = self.fall_duration
            
        if self.falling:
            self.fall_timer -= dt
            if self.fall_timer <= 0:
                self.game.change_state("forest")
            return
                
        # Update player
        self.player.update(dt)
        
        # Check for checkpoint
        if not self.reached_checkpoint and self.player.rect.colliderect(self.checkpoint):
            self.reached_checkpoint = True
            self.show_checkpoint_message = True
            self.checkpoint_message_timer = 3.0
            self.player_start_pos = pygame.Vector2(self.checkpoint.x + 25, self.checkpoint.y)
            
        if self.show_checkpoint_message:
            self.checkpoint_message_timer -= dt
            if self.checkpoint_message_timer <= 0:
                self.show_checkpoint_message = False
                
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player)
            if enemy.health <= 0:
                # Chance to drop items
                if random.random() < RARE_DROP_CHANCE:
                    self.player.inventory.add_item(Weapon("Bow", "bow", 15, 1.5, 1.0))
                self.enemies.remove(enemy)
                
        # Update elite skeleton
        if not self.elite_defeated:
            self.elite_skeleton.update(dt, self.player)
            if self.elite_skeleton.health <= 0:
                self.elite_defeated = True
                # Guaranteed drop
                self.player.inventory.add_item(Weapon("Arrow Quiver", "quiver", 0, 0, 0, arrows=50))
                # Chance for epic drop
                if random.random() < EPIC_DROP_CHANCE:
                    self.player.inventory.add_item(Weapon("Skeletal Cleaver", "sword", 30, 1.2, 0.7))
                    
        # Check for player death
        if self.player.health <= 0:
            self.game_over_menu.active = True
            
        # Handle collisions
        self.handle_collisions()
        
    def handle_collisions(self):
        # Ground collision
        if self.player.rect.colliderect(self.ground_rect) and not self.player.rect.colliderect(self.pit_rect):
            self.player.position.y = self.ground_rect.top - self.player.rect.height / 2
            self.player.velocity.y = 0
            self.player.on_ground = True
            
        # Platform collisions
        self.player.on_ground = False
        for platform in self.platforms:
            if (self.player.rect.colliderect(platform) and 
                self.player.velocity.y > 0 and 
                self.player.rect.bottom > platform.top + 5):
                self.player.position.y = platform.top - self.player.rect.height / 2
                self.player.velocity.y = 0
                self.player.on_ground = True
                
        # Player attacks enemies
        if self.player.attacking:
            attack_rect, damage = self.player.attack()
            for enemy in self.enemies:
                if attack_rect and attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(damage)
                    
            if not self.elite_defeated and attack_rect and attack_rect.colliderect(self.elite_skeleton.rect):
                self.elite_skeleton.take_damage(damage)
                
        # Enemy attacks player
        for enemy in self.enemies:
            for attack in enemy.attacks:
                if attack['rect'].colliderect(self.player.rect):
                    parried = self.player.take_damage(attack['damage'])
                    if parried:
                        enemy.take_damage(attack['damage'] * PARRY_DAMAGE_RETURN)
                        
        if not self.elite_defeated:
            for attack in self.elite_skeleton.attacks:
                if attack['rect'].colliderect(self.player.rect):
                    parried = self.player.take_damage(attack['damage'])
                    if parried:
                        self.elite_skeleton.take_damage(attack['damage'] * PARRY_DAMAGE_RETURN)
                        
    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw cave features
        pygame.draw.rect(screen, (50, 40, 30), self.ground_rect)
        for platform in self.platforms:
            pygame.draw.rect(screen, (60, 50, 40), platform)
            
        # Draw pit
        pygame.draw.rect(screen, BLACK, self.pit_rect)
        
        # Draw checkpoint
        if not self.reached_checkpoint:
            pygame.draw.rect(screen, (100, 200, 100), self.checkpoint)
            
        # Draw entities
        for enemy in self.enemies:
            enemy.draw(screen)
            
        if not self.elite_defeated:
            self.elite_skeleton.draw(screen)
            
        self.player.draw(screen)
        
        # Draw HUD
        self.hud.draw(screen)
        
        # Draw checkpoint message
        if self.show_checkpoint_message:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Checkpoint Reached! Press 'C' to level up stats", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            
        # Draw game over menu if active
        if self.game_over_menu.active:
            self.game_over_menu.draw(screen)
            
        # Draw stat menu if active
        if self.stat_menu.active:
            self.stat_menu.draw(screen)
            
    def reset(self):
        self.player.position = self.player_start_pos
        self.player.health = self.player.max_health
        self.player.stamina = self.player.max_stamina
        self.player.mana = self.player.max_mana
        
        # Reset enemies
        self.enemies = []
        self.spawn_enemies()
        
        # Reset elite skeleton
        if not self.elite_defeated:
            self.elite_skeleton.reset()
            
        self.game_over_menu.active = False
        self.stat_menu.active = False
        self.falling = False
