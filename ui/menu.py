import pygame
from settings import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font_large.render("Elden Ring 2D", True, (200, 150, 50))
        self.start_text = self.font.render("Start Game", True, WHITE)
        self.quit_text = self.font.render("Quit", True, WHITE)
        self.selected = 0
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.selected > 0:
            self.selected -= 1
        if keys[pygame.K_s] and self.selected < 1:
            self.selected += 1
            
        if keys[pygame.K_RETURN]:
            if self.selected == 0:
                self.game.change_state("tutorial")
            else:
                self.game.running = False
                
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw title
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 100))
        
        # Draw menu options
        start_color = (255, 255, 100) if self.selected == 0 else WHITE
        quit_color = (255, 255, 100) if self.selected == 1 else WHITE
        
        start_text = self.font.render("Start Game", True, start_color)
        quit_text = self.font.render("Quit", True, quit_color)
        
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 360))
        
        # Draw controls hint
        font_small = pygame.font.SysFont(None, 24)
        controls = font_small.render("Use W/S to select, Enter to confirm", True, (150, 150, 150))
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 500))

class GameOverMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.font_large = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font_large.render("You Died", True, RED)
        self.retry_text = self.font.render("Retry", True, WHITE)
        self.quit_text = self.font.render("Quit to Menu", True, WHITE)
        self.selected = 0
        
    def update(self, dt):
        if not self.active:
            return
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.selected > 0:
            self.selected -= 1
        if keys[pygame.K_s] and self.selected < 1:
            self.selected += 1
            
        if keys[pygame.K_RETURN]:
            if self.selected == 0:
                self.active = False
                self.game.current_level.reset()
            else:
                self.active = False
                self.game.change_state("menu")
                
    def draw(self, screen):
        if not self.active:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 200))
        
        # Draw menu options
        retry_color = (255, 255, 100) if self.selected == 0 else WHITE
        quit_color = (255, 255, 100) if self.selected == 1 else WHITE
        
        retry_text = self.font.render("Retry", True, retry_color)
        quit_text = self.font.render("Quit to Menu", True, quit_color)
        
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 350))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 420))
        
        # Draw controls hint
        font_small = pygame.font.SysFont(None, 24)
        controls = font_small.render("Use W/S to select, Enter to confirm", True, (150, 150, 150))
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 500))

class VictoryMenu(GameOverMenu):
    def __init__(self, game):
        super().__init__(game)
        self.title = self.font_large.render("Victory Achieved", True, (255, 215, 0))
        
    def draw(self, screen):
        if not self.active:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 200))
        
        # Draw menu options
        retry_color = (255, 255, 100) if self.selected == 0 else WHITE
        quit_color = (255, 255, 100) if self.selected == 1 else WHITE
        
        retry_text = self.font.render("Play Again", True, retry_color)
        quit_text = self.font.render("Quit to Menu", True, quit_color)
        
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 350))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 420))
        
        # Draw victory message
        font_small = pygame.font.SysFont(None, 24)
        message = font_small.render("You have conquered all challenges!", True, (200, 200, 200))
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 280))

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

class InventoryMenu:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.selected_item = 0
        self.current_tab = "weapons"  # weapons, armor, consumables
        
    def update(self, dt):
        if not self.active:
            return
            
        keys = pygame.key.get_pressed()
        
        # Change tabs
        if keys[pygame.K_a] and self.current_tab == "armor":
            self.current_tab = "weapons"
            self.selected_item = 0
        elif keys[pygame.K_a] and self.current_tab == "consumables":
            self.current_tab = "armor"
            self.selected_item = 0
        elif keys[pygame.K_d] and self.current_tab == "weapons":
            self.current_tab = "armor"
            self.selected_item = 0
        elif keys[pygame.K_d] and self.current_tab == "armor":
            self.current_tab = "consumables"
            self.selected_item = 0
            
        # Navigate items
        items = self.get_current_items()
        if keys[pygame.K_w] and self.selected_item > 0:
            self.selected_item -= 1
        if keys[pygame.K_s] and self.selected_item < len(items) - 1:
            self.selected_item += 1
            
        # Equip/use item
        if keys[pygame.K_RETURN] and items:
            self.use_item(items[self.selected_item])
            
        # Close menu
        if keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
            self.active = False
            
    def get_current_items(self):
        if self.current_tab == "weapons":
            return self.player.inventory.weapons
        elif self.current_tab == "armor":
            return self.player.inventory.armor
        else:
            return self.player.inventory.consumables
            
    def use_item(self, item):
        if self.current_tab == "weapons":
            # Swap current weapon
            old_weapon = self.player.weapon
            self.player.weapon = item
            self.player.inventory.weapons.remove(item)
            self.player.inventory.weapons.append(old_weapon)
        elif self.current_tab == "armor":
            # Equip armor
            pass  # Similar logic to weapons
        else:
            # Use consumable
            item.use(self.player)
            self.player.inventory.consumables.remove(item)
            
    def draw(self, screen):
        if not self.active:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title = self.font.render("Inventory", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Draw tabs
        weapons_color = (200, 150, 50) if self.current_tab == "weapons" else (150, 150, 150)
        armor_color = (200, 150, 50) if self.current_tab == "armor" else (150, 150, 150)
        consumables_color = (200, 150, 50) if self.current_tab == "consumables" else (150, 150, 150)
        
        weapons_text = self.font.render("Weapons", True, weapons_color)
        armor_text = self.font.render("Armor", True, armor_color)
        consumables_text = self.font.render("Consumables", True, consumables_color)
        
        screen.blit(weapons_text, (SCREEN_WIDTH // 2 - 250, 100))
        screen.blit(armor_text, (SCREEN_WIDTH // 2 - armor_text.get_width() // 2, 100))
        screen.blit(consumables_text, (SCREEN_WIDTH // 2 + 150, 100))
        
        # Draw items
        items = self.get_current_items()
        for i, item in enumerate(items):
            color = (255, 255, 100) if i == self.selected_item else WHITE
            item_text = self.font.render(item.name, True, color)
            screen.blit(item_text, (SCREEN_WIDTH // 2 - 200, 150 + i * 40))
            
            # Draw item info if selected
            if i == self.selected_item:
                desc_text = self.small_font.render(item.description, True, (200, 200, 200))
                screen.blit(desc_text, (SCREEN_WIDTH // 2 - 200, 190 + i * 40))
                
        # Draw current equipment
        eq_title = self.font.render("Equipped", True, (200, 200, 200))
        screen.blit(eq_title, (SCREEN_WIDTH // 2 + 100, 150))
        
        weapon_text = self.small_font.render(f"Weapon: {self.player.weapon.name}", True, WHITE)
        screen.blit(weapon_text, (SCREEN_WIDTH // 2 + 100, 200))
        
        # Draw controls
        controls = self.small_font.render("A/D: Tabs | W/S: Select | Enter: Use | Esc/I: Close", True, (150, 150, 150))
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 550))
