import pygame
from settings import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
    def draw(self, screen):
        # Health bar
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(screen, RED, (20, 20, 200, 30))
        pygame.draw.rect(screen, GREEN, (20, 20, 200 * health_ratio, 30))
        health_text = self.font.render(f"HP: {int(self.player.health)}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (25, 20))
        
        # Stamina bar
        stamina_ratio = self.player.stamina / self.player.max_stamina
        pygame.draw.rect(screen, (70, 70, 70), (20, 60, 200, 20))
        pygame.draw.rect(screen, (200, 200, 50), (20, 60, 200 * stamina_ratio, 20))
        
        # Mana bar
        mana_ratio = self.player.mana / self.player.max_mana
        pygame.draw.rect(screen, (70, 70, 100), (20, 90, 200, 20))
        pygame.draw.rect(screen, BLUE, (20, 90, 200 * mana_ratio, 20))
        
        # Gold
        gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (SCREEN_WIDTH - gold_text.get_width() - 20, 20))
        
        # Weapon info
        weapon_text = self.small_font.render(f"Weapon: {self.player.weapon.name}", True, WHITE)
        screen.blit(weapon_text, (SCREEN_WIDTH - weapon_text.get_width() - 20, 60))
        
        # Controls reminder
        controls_text = self.small_font.render("I: Inventory | C: Stats (at checkpoint)", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
