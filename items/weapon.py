class Weapon:
    def __init__(self, name, weapon_type, damage, attack_speed, stamina_cost, arrows=0):
        self.name = name
        self.type = weapon_type  # sword, bow, etc.
        self.damage = damage
        self.attack_speed = attack_speed  # seconds between attacks
        self.stamina_cost = stamina_cost  # multiplier
        self.arrows = arrows  # for bows
        
        # Set description based on type
        if self.type == "sword":
            self.description = f"A {name}. Damage: {damage}, Speed: {attack_speed}s"
        elif self.type == "bow":
            self.description = f"A {name}. Damage: {damage}, Arrows: {arrows}"
        elif self.type == "quiver":
            self.description = f"Contains {arrows} arrows"
        else:
            self.description = f"A {name}"
            
    def can_attack(self):
        if self.type == "bow":
            return self.arrows > 0
        return True
        
    def use_arrow(self):
        if self.type == "bow" and self.arrows > 0:
            self.arrows -= 1
            return True
        return False
