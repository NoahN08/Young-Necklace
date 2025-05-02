class Inventory:
    def __init__(self):
        self.weapons = []
        self.armor = []
        self.consumables = []
        
    def add_item(self, item):
        if item.type in ["sword", "bow", "quiver"]:
            self.weapons.append(item)
        elif item.type in ["helmet", "chest", "gloves", "boots"]:
            self.armor.append(item)
        else:
            self.consumables.append(item)
            
    def has_weapon(self, weapon_name):
        return any(w.name == weapon_name for w in self.weapons)
        
    def get_weapon(self, weapon_name):
        for weapon in self.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

