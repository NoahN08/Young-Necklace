import pygame
from settings import *
from entities.entity import Entity
from items.weapon import Weapon
from items.inventory import Inventory

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_BASE_HEALTH, "player")
        self.speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE
        self.stamina = PLAYER_BASE_STAMINA
        self.max_stamina = PLAYER_BASE_STAMINA
        self.mana = PLAYER_BASE_MANA
        self.max_mana = PLAYER_BASE_MANA
        
        # Stats
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.dexterity = 10
        self.vigor = 10
        
        # Combat
        self.attacking = False
        self.blocking = False
        self.rolling = False
        self.invincible = False
        self.roll_timer = 0
        self.invincibility_timer = 0
        self.attack_cooldown = 0
        self.parry_window = 0.1
        self.parry_timer = 0
        
        # Equipment
        self.weapon = Weapon("Wooden Sword", "sword", 10, 1.0, 0.5)
        self.inventory = Inventory()
        self.equipped_armor = []
        
        # Gold
        self.gold = 0
        
    def update(self, dt):
        # Handle timers
        if self.roll_timer > 0:
            self.roll_timer -= dt
            if self.roll_timer <= 0:
                self.rolling = False
                
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
                
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        if self.parry_timer > 0:
            self.parry_timer -= dt
            if self.parry_timer <= 0:
                self.blocking = False
                
        # Handle movement
        keys = pygame.key.get_pressed()
        
        if not self.attacking and not self.rolling:
            if keys[pygame.K_a]:
                self.velocity.x = -self.speed
                self.facing_right = False
            elif keys[pygame.K_d]:
                self.velocity.x = self.speed
                self.facing_right = True
            else:
                self.velocity.x = 0
                
            if keys[pygame.K_w] and self.on_ground:
                self.velocity.y = -self.jump_force
                self.on_ground = False
                
        # Apply gravity
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt
        
        # Update rect
        self.rect.midbottom = self.position
        
    def roll(self):
        if not self.rolling and self.stamina >= 20:
            self.rolling = True
            self.invincible = True
            self.roll_timer = PLAYER_ROLL_DURATION
            self.invincibility_timer = PLAYER_INVINCIBILITY_DURATION
            self.stamina -= 20
            # Add roll momentum
            roll_direction = 1 if self.facing_right else -1
            self.velocity.x = roll_direction * self.speed * 1.5
            self.velocity.y = -100  # Small hop
            
    def attack(self):
        if not self.attacking and self.attack_cooldown <= 0 and self.stamina >= 10:
            self.attacking = True
            self.attack_cooldown = self.weapon.attack_speed
            self.stamina -= 10
            # Return the attack hitbox and damage
            attack_rect = pygame.Rect(0, 0, 50, 30)
            if self.facing_right:
                attack_rect.midleft = self.rect.midright
            else:
                attack_rect.midright = self.rect.midleft
            return attack_rect, self.calculate_damage()
        return None, 0
        
    def block(self):
        if not self.blocking and self.stamina >= 5:
            self.blocking = True
            self.parry_timer = self.parry_window
            
    def calculate_damage(self):
        base_damage = self.weapon.damage
        strength_bonus = base_damage * (self.strength * 0.02)
        dexterity_bonus = base_damage * (self.dexterity * 0.01)
        return base_damage + strength_bonus + dexterity_bonus
    
    def take_damage(self, damage):
        if self.invincible:
            return False
            
        if self.blocking:
            # Check if parry
            if self.parry_timer > 0:
                damage_taken = damage * (1 - PARRY_DAMAGE_REDUCTION)
                self.health -= damage_taken
                self.invincible = True
                self.invincibility_timer = 0.5
                return True  # Parry successful
            else:
                damage_taken = damage * (1 - BLOCK_DAMAGE_REDUCTION)
                self.health -= damage_taken
                self.stamina -= damage * 0.5
        else:
            self.health -= damage
            
        self.invincible = True
        self.invincibility_timer = PLAYER_INVINCIBILITY_DURATION
        
        if self.health <= 0:
            self.die()
            
        return False
        
    def die(self):
        # Handle player death
        self.health = self.max_health
        # Respawn logic would be handled by the level
        
    def increase_stat(self, stat):
        cost = self.get_stat_cost(stat)
        if self.gold >= cost:
            self.gold -= cost
            setattr(self, stat, getattr(self, stat) + 1)
            
            # Update max stats based on vigor
            if stat == "vigor":
                self.max_health = PLAYER_BASE_HEALTH + (self.vigor * 5)
                self.health = self.max_health
            elif stat == "strength":
                pass  # Strength affects damage in calculate_damage
            elif stat == "intelligence":
                self.max_mana = PLAYER_BASE_MANA + (self.intelligence * 3)
                self.mana = self.max_mana
            elif stat == "agility":
                self.max_stamina = PLAYER_BASE_STAMINA + (self.agility * 3)
                self.stamina = self.max_stamina
            elif stat == "dexterity":
                pass  # Dexterity affects damage in calculate_damage
                
    def get_stat_cost(self, stat):
        current_value = getattr(self, stat)
        base_cost = BASE_STAT_COST
        return int(base_cost * (STAT_COST_INCREASE ** (current_value - 10)))
        
    def draw(self, screen):
        # Simple player drawing
        color = (200, 100, 50) if not self.invincible else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw weapon if attacking
        if self.attacking:
            attack_rect = pygame.Rect(0, 0, 50, 20)
            if self.facing_right:
                attack_rect.midleft = self.rect.midright
            else:
                attack_rect.midright = self.rect.midleft
            pygame.draw.rect(screen, (150, 150, 150), attack_rect)
