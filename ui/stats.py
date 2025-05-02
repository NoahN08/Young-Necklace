import pygame
from settings import *

class StatMenu:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.selected_stat = 0
        self.stats = ["strength", "intelligence", "agility", "dexterity", "vigor"]
        
    def update(self, dt):
        if not self.active:
            return
            
        keys = pygame.key.get_pressed()
        
        # Navigate stats
        if keys[pygame.K_w] and self.selected_stat > 0:
            self.selected_stat -= 1
        if keys[pygame.K_s] and self.selected_stat < len(self.stats) - 1:
            self.selected_stat += 1
            
        # Increase stat
        if keys[pygame.K_RETURN]:
            stat = self.stats[self.selected_stat]
            self.player.increase_stat(stat)
            
        # Close menu
        if keys[pygame.K_ESCAPE] or keys[pygame.K_c]:
            self.active = False
            
    def draw(self, screen):
        if not self.active:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title = self.font.render("Level Up Stats", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Draw stats
        for i, stat in enumerate(self.stats):
            stat_value = getattr(self.player, stat)
            cost = self.player.get_stat_cost(stat)
            
            # Highlight selected stat
            color = (255, 255, 100) if i == self.selected_stat else WHITE
            
            # Stat name and value
            stat_text = self.font.render(f"{stat.capitalize()}: {stat_value}", True, color)
            screen.blit(stat_text, (SCREEN_WIDTH // 2 - 150, 200 + i * 50))
            
            # Cost
            cost_color = (100, 255, 100) if self.player.gold >= cost else (255, 100, 100)
            cost_text = self.font.render(f"{cost} gold", True, cost_color)
            screen.blit(cost_text, (SCREEN_WIDTH // 2 + 100, 200 + i * 50))
            
        # Draw current gold
        gold_text = self.font.render(f"Your Gold: {self.player.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (SCREEN_WIDTH // 2 - gold_text.get_width() // 2, 500))
        
        # Draw controls
        controls = self.small_font.render("W/S: Select | Enter: Increase | Esc/C: Close", True, (150, 150, 150))
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 550))
