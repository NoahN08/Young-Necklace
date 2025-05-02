from entities.entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self, x, y, health, enemy_type):
        super().__init__(x, y, health, enemy_type)
        self.attacks = []  # List of active attacks
        self.stun_meter = 0
        self.stun_threshold = 100  # Default value
        self.stunned = False
        self.stun_timer = 0
        
    def update(self, dt, player):
        super().update(dt)
        
        # Update attack timers
        for attack in self.attacks[:]:
            attack['timer'] -= dt
            if attack['timer'] <= 0:
                self.attacks.remove(attack)
                
        # Skip AI if stunned
        if self.stunned:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.stunned = False
                self.stun_meter = 0
            return
            
        # Implement enemy-specific AI in child classes
        self.ai_update(dt, player)
        
    def ai_update(self, dt, player):
        pass  # To be implemented by child classes
        
    def take_damage(self, damage):
        super().take_damage(damage)
        self.stun_meter += damage
        if self.stun_meter >= self.stun_threshold:
            self.stunned = True
            self.stun_timer = STUN_DURATION
            
    def draw(self, screen):
        super().draw(screen)
        
        # Draw stun meter if above 0
        if self.stun_meter > 0:
            stun_width = 50
            stun_height = 5
            stun_ratio = min(self.stun_meter / self.stun_threshold, 1.0)
            pygame.draw.rect(screen, (150, 150, 255), (self.rect.x, self.rect.y - 20, stun_width, stun_height))
            pygame.draw.rect(screen, BLUE, (self.rect.x, self.rect.y - 20, stun_width * stun_ratio, stun_height))
