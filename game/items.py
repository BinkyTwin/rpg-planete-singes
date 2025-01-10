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
        self.value = value

    def __str__(self):
        return f"{self.name} ({self.item_type.value})"

# Quelques objets prédéfinis 
ITEMS = {
    "épée_rouillée": Item("Épée rouillée", ItemType.WEAPON, "Une vieille épée usée", 10),
    "m4": Item("M4", ItemType.WEAPON, "Un fusil d'assaut", 20),
    "glock": Item("Glock", ItemType.WEAPON, "Un pistolet", 15),
    "banane": Item("Banane", ItemType.POTION, "Une banane bien mûre qui restaure 20 points de vie", 20),
    "banane_plantin": Item("Banane plantin", ItemType.POTION, "Une banane plantin qui restaure 30 points de vie", 30),
    "armure_cuir": Item("Armure en cuir", ItemType.ARMOR, "Protection basique", 20),
    "pierre_précieuse": Item("Pierre précieuse", ItemType.MISC, "Une gemme brillante", 50)
} 