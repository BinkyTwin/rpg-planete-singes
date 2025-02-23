from enum import Enum
import logging
from typing import Tuple, Callable, Optional
from .animations import FadeOutAnimation

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
        if self.item_type == ItemType.WEAPON:
            return f"{self.name} (Dégâts: {self.value})"
        elif self.item_type == ItemType.ARMOR:
            return f"{self.name} (Bonus HP: +{self.value})"
        elif self.item_type == ItemType.POTION:
            return f"{self.name} (Restaure {self.value} HP)"
        return f"{self.name}"

class CollectibleItem(Item):
    """Classe de base pour tous les items collectibles sur la carte"""
    def __init__(self, name: str, item_type: ItemType, description: str, value: int, 
                 position: Tuple[int, int], image_path: str):
        super().__init__(name, item_type, description, value)
        self.position = position
        self.image_path = image_path
        self.collected = False
        self.animation = None
        self.is_animating = False

    def show(self):
        """Affiche l'item sur la carte"""
        logging.info(f"Displaying {self.name} at position {self.position} using icon {self.image_path}")

    def interact(self, player_position: Tuple[int, int], key_pressed: str, 
                confirmation_callback: Callable[[], bool]) -> Optional[bool]:
        """
        Gère l'interaction avec l'item.
        
        Args:
            player_position: Position actuelle du joueur
            key_pressed: Touche pressée par le joueur
            confirmation_callback: Fonction appelée pour confirmer la collecte
            
        Returns:
            bool ou None: True si collecté, False si refusé, None si pas d'interaction
        """
        if self.position == player_position and key_pressed.upper() == "E":
            logging.info(f"Interaction with item {self.name} initiated")
            confirmed = confirmation_callback()
            if confirmed:
                # Démarrer l'animation de collecte
                self.animation = FadeOutAnimation(duration_ms=500)
                self.animation.start()
                self.is_animating = True
                logging.info(f"Item {self.name} collection animation started")
            else:
                logging.info(f"Item {self.name} remains on map")
            return confirmed
        return None

    def update_animation(self):
        """Met à jour l'animation de l'item"""
        if self.is_animating and self.animation:
            self.animation.update()
            if self.animation.is_finished:
                self.collected = True
                self.is_animating = False
                logging.info(f"Item {self.name} collection animation finished")

def create_collectible_item(name: str, item_type: ItemType, description: str, value: int,
                          position: Tuple[int, int], image_path: str) -> CollectibleItem:
    """
    Factory function pour créer des items collectibles.
    Cette fonction permet de créer facilement de nouveaux items sans créer de nouvelles classes.
    """
    return CollectibleItem(name, item_type, description, value, position, image_path)

# Création des items via la factory
ITEMS = {
    # Items collectibles sur la carte
    "m16": create_collectible_item(
        "M16",
        ItemType.WEAPON,
        "Un fusil d'assaut puissant et précis",
        25,
        (5, 17),
        "assets/tilesets/images/items/M16_full.png"
    ),
    "banane": create_collectible_item(
        "Banane",
        ItemType.POTION,
        "Une banane bien mûre qui restaure de la santé",
        20,
        (9, 12),
        "assets/tilesets/images/items/Banana.png"
    ),
    
    # Items standards (non collectibles sur la carte)
    "épée_rouillée": Item(
        "Épée rouillée", 
        ItemType.WEAPON, 
        "Une vieille épée usée mais qui peut encore faire mal", 
        15
    ),
    "glock": Item(
        "Glock", 
        ItemType.WEAPON, 
        "Un pistolet fiable et efficace", 
        20
    ),
    "banane_plantin": Item(
        "Banane plantin", 
        ItemType.POTION, 
        "Une banane plantin qui restaure beaucoup de points de vie", 
        30
    )
}

def test_collectible_item():
    """Tests unitaires pour la classe CollectibleItem"""
    # Test 1: Création d'un item
    item = create_collectible_item(
        "Test Item",
        ItemType.WEAPON,
        "Test description",
        10,
        (1, 1),
        "test/path.png"
    )
    
    print("\n=== Tests de CollectibleItem ===")
    
    # Test des propriétés de base
    assert item.name == "Test Item", "Nom incorrect"
    assert item.item_type == ItemType.WEAPON, "Type incorrect"
    assert item.value == 10, "Valeur incorrecte"
    assert item.position == (1, 1), "Position incorrecte"
    print("[OK] Test 1: Propriétés de base correctes")
    
    # Test de l'interaction
    # Cas 1: Mauvaise position
    result = item.interact((0, 0), "E", lambda: True)
    assert result is None, "L'interaction ne devrait pas se produire à distance"
    print("[OK] Test 2: Pas d'interaction à distance")
    
    # Cas 2: Bonne position, mauvaise touche
    result = item.interact((1, 1), "A", lambda: True)
    assert result is None, "L'interaction ne devrait pas se produire avec la mauvaise touche"
    print("[OK] Test 3: Pas d'interaction avec la mauvaise touche")
    
    # Cas 3: Interaction réussie
    result = item.interact((1, 1), "E", lambda: True)
    assert result is True, "L'interaction devrait réussir"
    assert item.collected is False, "L'item ne devrait pas être collecté"
    print("[OK] Test 4: Interaction réussie")
    
    # Cas 4: Interaction refusée
    item.collected = False
    result = item.interact((1, 1), "E", lambda: False)
    assert result is False, "L'interaction devrait être refusée"
    assert item.collected is False, "L'item ne devrait pas être collecté"
    print("[OK] Test 5: Interaction refusée")
    
    print("\nTous les tests ont réussi!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_collectible_item()