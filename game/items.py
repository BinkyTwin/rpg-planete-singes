from enum import Enum

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    MISC = "misc"

class Item:
    def __init__(self, name: str, item_type: ItemType, description: str, value: int):
        self.name = name
        self.item_type = item_type
        self.description = description
        self.value = value  # Dégâts pour WEAPON, bonus HP pour ARMOR, restauration HP pour POTION

    def __str__(self):
        if self.item_type == ItemType.WEAPON:
            return f"{self.name} (Dégâts: {self.value})"
        elif self.item_type == ItemType.ARMOR:
            return f"{self.name} (Bonus HP: +{self.value})"
        elif self.item_type == ItemType.POTION:
            return f"{self.name} (Restaure {self.value} HP)"

# Objets prédéfinis avec leurs effets
ITEMS = {
    # Armes (value = dégâts)
    "épée_rouillée": Item(
        "Épée rouillée", 
        ItemType.WEAPON, 
        "Une vieille épée usée mais qui peut encore faire mal", 
        15
    ),
    "m4": Item(
        "M4", 
        ItemType.WEAPON, 
        "Un fusil d'assaut puissant et précis", 
        25
    ),
    "glock": Item(
        "Glock", 
        ItemType.WEAPON, 
        "Un pistolet fiable et efficace", 
        20
    ),
    
    # Armures (value = bonus HP)
    "armure_cuir": Item(
        "Armure en cuir", 
        ItemType.ARMOR, 
        "Une protection basique mais efficace", 
        20
    ),
    "gilet_pare_balles": Item(
        "Gilet pare-balles", 
        ItemType.ARMOR, 
        "Une protection moderne contre les projectiles", 
        35
    ),
    
    # Potions (value = HP restaurés)
    "banane": Item(
        "Banane", 
        ItemType.POTION, 
        "Une banane bien mûre qui restaure des points de vie", 
        20
    ),
    "banane_plantin": Item(
        "Banane plantin", 
        ItemType.POTION, 
        "Une banane plantin rare et nourrissante", 
        30
    )
} 