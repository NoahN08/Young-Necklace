import pygame
from settings import *
from entities.player import Player
from entities.spider_boss import SpiderBoss
from levels.level import Level
from ui.hud import HUD
from ui.menu import GameOverMenu

class TutorialLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((50, 100, 200))  # Mountain sky background
        
        # Create ground/platforms
        self.ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        self.platforms = [
            pygame.Rect(100, 500, 200, 20),
            pygame.Rect(400, 400, 200, 20),
            pygame.Rect(700, 300, 200, 20),
            pygame.Rect(1000, 400, 200, 20)
        ]
        
        # Create player
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.player_start_pos = pygame.Vector2(100, SCREEN_HEIGHT - 100)
        
        # Create boss
        self.boss = SpiderBoss(1000, SCREEN_HEIGHT - 100)
        self.boss_intro_done = False
        
        # UI
        self.hud = HUD(self.player)
        self.game_over_menu = GameOverMenu(self.game)
        
        # Tutorial messages
        self.tutorial_messages = [
            "Move: A and D keys",
            "Jump: W key",
            "Roll: Space (Gives brief invincibility)",
            "Attack: Left Mouse Button",
            "Block: Right Mouse Button (Time it for a parry)",
            "Defeat the Spider Queen!"
        ]
        self.current_message = 0
        self.message_timer = 0
        self.message_duration = 5
        
    def update(self, dt):
        # Update tutorial messages
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0 and self.current_message < len(self.tutorial_messages) - 1:
                self.current_message += 1
                self.message_timer = self.message_duration
                
        # Boss intro
        if not self.boss_intro_done and self.player.position.x > 300:
            self.boss_intro_done = True
            self.current_message = len(self.tutorial_messages) - 1
            self.message_timer = self.message_duration
            
        # Update entities
        self.player.update(dt)
        self.boss.update(dt, self.player)
        
        # Check for player death
        if self.player.health <= 0:
            self.game_over_menu.active = True
            
        # Check for boss death
        if self.boss.health <= 0:
            self.game.change_state("cave")
            
        # Handle collisions
        self.handle_collisions()
        
    def handle_collisions(self):
        # Ground collision
        if self.player.rect.colliderect(self.ground_rect):
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
                
        # Player attacks boss
        if self.player.attacking:
            attack_rect, damage = self.player.attack()
            if attack_rect and attack_rect.colliderect(self.boss.rect):
                self.boss.take_damage(damage)
                
        # Boss attacks player
        for attack in self.boss.attacks:
            if attack['rect'].colliderect(self.player.rect):
                parried = self.player.take_damage(attack['damage'])
                if parried:
                    self.boss.take_damage(attack['damage'] * PARRY_DAMAGE_RETURN)
                    
    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw platforms and ground
        pygame.draw.rect(screen, (100, 70, 40), self.ground_rect)
        for platform in self.platforms:
            pygame.draw.rect(screen, (120, 80, 50), platform)
            
        # Draw entities
        self.boss.draw(screen)
        self.player.draw(screen)
        
        # Draw HUD
        self.hud.draw(screen)
        
        # Draw tutorial message
        if self.message_timer > 0:
            font = pygame.font.SysFont(None, 36)
            text = font.render(self.tutorial_messages[self.current_message], True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            
        # Draw game over menu if active
        if self.game_over_menu.active:
            self.game_over_menu.draw(screen)
            
    def reset(self):
        self.player.position = self.player_start_pos
        self.player.health = self.player.max_health
        self.player.stamina = self.player.max_stamina
        self.player.mana = self.player.max_mana
        self.boss.reset()
        self.boss_intro_done = False
        self.current_message = 0
        self.message_timer = self.message_duration
        self.game_over_menu.active = False
