import pygame
from settings import *

class Item:
    def __init__(self, name, item_type, description=""):
        """
        Base class for all items in the game
        
        Args:
            name (str): The name of the item
            item_type (str): The type of item (weapon, armor, consumable, etc.)
            description (str): Optional description of the item
        """
        self.name = name
        self.type = item_type
        self.description = description if description else f"A {self.name}"
        self.rarity = "common"  # common, rare, epic, legendary
        self.value = 10  # Base gold value
        self.sprite = None  # Can be set to a pygame Surface for graphical items
        self.equippable = False
        self.consumable = False
        
    def use(self, target):
        """
        Base use method - to be overridden by child classes
        Args:
            target: The entity using the item (usually the player)
        """
        print(f"Using {self.name}")
        return False  # Return True if item was consumed
        
    def draw(self, screen, x, y, width=50, height=50):
        """
        Draw the item's representation
        Args:
            screen: pygame Surface to draw on
            x, y: Position to draw at
            width, height: Dimensions of the drawn item
        """
        if self.sprite:
            scaled_sprite = pygame.transform.scale(self.sprite, (width, height))
            screen.blit(scaled_sprite, (x, y))
        else:
            # Default colored rectangle based on rarity
            colors = {
                "common": (200, 200, 200),
                "rare": (100, 100, 255),
                "epic": (180, 50, 220),
                "legendary": (255, 215, 0)
            }
            pygame.draw.rect(screen, colors.get(self.rarity, WHITE), (x, y, width, height))
            
            # Draw item initial
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.name[0].upper(), True, BLACK)
            screen.blit(text, (x + width//2 - text.get_width()//2, 
                               y + height//2 - text.get_height()//2))
            
    def set_rarity(self, rarity):
        """Set the item's rarity and adjust its value accordingly"""
        rarity_multipliers = {
            "common": 1,
            "rare": 3,
            "epic": 10,
            "legendary": 25
        }
        if rarity in rarity_multipliers:
            self.rarity = rarity
            self.value *= rarity_multipliers[rarity]
            
    def get_rarity_color(self):
        """Get the color associated with this item's rarity"""
        rarity_colors = {
            "common": (200, 200, 200),
            "rare": (100, 100, 255),
            "epic": (180, 50, 220),
            "legendary": (255, 215, 0)
        }
        return rarity_colors.get(self.rarity, WHITE)


class Weapon(Item):
    def __init__(self, name, weapon_type, damage, attack_speed, stamina_cost, **kwargs):
        """
        Weapon items that can be equipped by the player
        
        Args:
            name (str): Name of the weapon
            weapon_type (str): Type of weapon (sword, bow, etc.)
            damage (int): Base damage value
            attack_speed (float): Time between attacks in seconds
            stamina_cost (float): Stamina cost multiplier
            **kwargs: Additional properties like arrows for bows
        """
        super().__init__(name, "weapon")
        self.weapon_type = weapon_type
        self.damage = damage
        self.attack_speed = attack_speed
        self.stamina_cost = stamina_cost
        self.equippable = True
        
        # Weapon-specific properties
        self.arrows = kwargs.get("arrows", 0)  # For bows
        self.critical_chance = kwargs.get("critical_chance", 0.1)  # 10% base
        self.critical_multiplier = kwargs.get("critical_multiplier", 1.5)
        
        # Update description based on weapon stats
        self.description = (f"{self.name} ({self.weapon_type})\n"
                          f"Damage: {self.damage}\n"
                          f"Speed: {self.attack_speed}s\n")
        
        if self.weapon_type == "bow":
            self.description += f"Arrows: {self.arrows}\n"
            
    def calculate_damage(self, attacker):
        """
        Calculate damage dealt by this weapon
        Args:
            attacker: The entity wielding the weapon
        Returns:
            int: The calculated damage amount
        """
        base_damage = self.damage
        
        # Apply critical hit chance
        if random.random() < self.critical_chance:
            base_damage *= self.critical_multiplier
            return int(base_damage), True  # Return damage and critical flag
            
        return int(base_damage), False
        
    def can_attack(self):
        """Check if the weapon can be used (has arrows if bow)"""
        if self.weapon_type == "bow":
            return self.arrows > 0
        return True
        
    def use_arrow(self):
        """Consume an arrow (for bows)"""
        if self.weapon_type == "bow" and self.arrows > 0:
            self.arrows -= 1
            return True
        return False


class Armor(Item):
    def __init__(self, name, armor_type, defense, weight):
        """
        Armor items that can be equipped by the player
        
        Args:
            name (str): Name of the armor
            armor_type (str): Type (helmet, chest, gloves, boots)
            defense (int): Damage reduction value
            weight (float): Affects movement speed (0-1 scale)
        """
        super().__init__(name, "armor")
        self.armor_type = armor_type
        self.defense = defense
        self.weight = weight  # 0 = no effect, 1 = max penalty
        self.equippable = True
        
        # Update description
        self.description = (f"{self.name} ({self.armor_type})\n"
                          f"Defense: {self.defense}\n"
                          f"Weight: {self.weight:.1f}")


class Consumable(Item):
    def __init__(self, name, effect_type, potency, uses=1):
        """
        Consumable items that can be used by the player
        
        Args:
            name (str): Name of the consumable
            effect_type (str): Type of effect (health, stamina, mana, buff)
            potency (int): Strength of the effect
            uses (int): Number of uses before consumed
        """
        super().__init__(name, "consumable")
        self.effect_type = effect_type
        self.potency = potency
        self.uses = uses
        self.max_uses = uses
        self.consumable = True
        
        # Set description based on effect type
        effect_descriptions = {
            "health": f"Restores {potency} health",
            "stamina": f"Restores {potency} stamina",
            "mana": f"Restores {potency} mana",
            "buff": f"Grants {potency} temporary buff"
        }
        self.description = f"{name}: {effect_descriptions.get(effect_type, 'Mysterious effect')}"
        
        if self.uses > 1:
            self.description += f" ({self.uses} uses remaining)"
            
    def use(self, target):
        """
        Use the consumable on a target
        Args:
            target: The entity using the item
        Returns:
            bool: True if item was consumed
        """
        if self.uses <= 0:
            return False
            
        if self.effect_type == "health":
            target.health = min(target.health + self.potency, target.max_health)
        elif self.effect_type == "stamina":
            target.stamina = min(target.stamina + self.potency, target.max_stamina)
        elif self.effect_type == "mana":
            target.mana = min(target.mana + self.potency, target.max_mana)
        elif self.effect_type == "buff":
            # Apply buff logic here
            pass
            
        self.uses -= 1
        
        # Return True if fully consumed
        return self.uses <= 0


class KeyItem(Item):
    def __init__(self, name, description=""):
        """
        Special key items that can't be used but are important for progression
        
        Args:
            name (str): Name of the key item
            description (str): Description of the item's purpose
        """
        super().__init__(name, "key", description)
        self.equippable = False
        self.consumable = False
