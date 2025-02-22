from enum import Enum
import logging

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

class M16(Item):
    def __init__(self, name, position, image_path):
        super().__init__(name, ItemType.WEAPON, "Un fusil d'assaut puissant et précis", 25)
        self.position = position
        self.image_path = image_path
        self.collected = False

    def show(self):
        # Afficher l'item sur la map (simulation via logging)
        logging.info(f"Displaying {self.name} at position {self.position} using icon {self.image_path}")

    def interact(self, player_position, key_pressed, confirmation_callback):
        """
        Détecte l'interaction du joueur avec l'item.
        Si le joueur est sur la même position et appuie sur 'E', la fonction de confirmation est appelée.
        Si la confirmation renvoie True, l'item est marqué comme collecté.
        """
        if self.position == player_position and key_pressed.upper() == "E":
            logging.info("Interaction with item %s initiated", self.name)
            confirmed = confirmation_callback()
            if confirmed:
                self.collected = True
                logging.info("Item %s collected.", self.name)
            else:
                logging.info("Item %s remains on map.", self.name)
            return confirmed
        return None


def example_integration():
    """
    Exemple d'intégration de la logique de l'item M16 dans une scène de jeu.
    Simule la présence du joueur sur la même tuile et son interaction via la touche 'E'.
    """
    # Position du joueur simulée
    player_position = (5, 17)

    # Création de l'item M16
    m16 = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
    m16.show()

    # Simuler l'appui sur la touche 'E'
    key = "E"

    # Fonction de confirmation simulée (ici, toujours 'oui')
    def confirmation():
        return True  

    result = m16.interact(player_position, key, confirmation)
    if result is True:
        print("Item collected and added to inventory.")
    elif result is False:
        print("Item remains on map.")
    else:
        print("No interaction occurred.")


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
    ),
    "m16": M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
} 


if __name__ == '__main__':
    # Configurer le logging pour afficher les messages dans la console
    logging.basicConfig(level=logging.INFO)
    example_integration()