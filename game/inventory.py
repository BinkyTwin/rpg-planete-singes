from typing import List, Optional
from .items import Item, ItemType

class Inventory:
    def __init__(self, max_slots: int = 15):
        self.max_slots = max_slots
        self.items: List[Item] = []
        self.equipped_item: Optional[Item] = None  # Item actuellement équipé

    def add_item(self, item: Item) -> bool:
        """
        Ajoute un item à l'inventaire si il y a de la place
        Retourne True si l'ajout est réussi, False sinon
        """
        if len(self.items) < self.max_slots:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item: Item) -> bool:
        """
        Retire un item de l'inventaire
        Si l'item est équipé, il est déséquipé
        """
        if item in self.items:
            if self.equipped_item == item:
                self.equipped_item = None
            self.items.remove(item)
            return True
        return False

    def equip_item(self, item: Item) -> bool:
        """
        Équipe un item s'il est dans l'inventaire
        Pour les potions, elles sont équipées temporairement avant d'être consommées
        """
        if item not in self.items and item.item_type != ItemType.POTION:
            return False

        self.equipped_item = item
        return True

    def unequip_item(self) -> Optional[Item]:
        """Déséquipe l'item actuel"""
        previous_item = self.equipped_item
        self.equipped_item = None
        return previous_item

    def get_equipped_item(self) -> Optional[Item]:
        """
        Retourne l'item équipé
        Si une potion est équipée et qu'elle n'est plus dans l'inventaire, elle est déséquipée
        """
        if self.equipped_item and self.equipped_item.item_type == ItemType.POTION:
            if self.equipped_item not in self.items:
                self.equipped_item = None
        return self.equipped_item

    def get_items(self) -> List[Item]:
        """Retourne la liste des items dans l'inventaire"""
        return self.items

    def get_free_slots(self) -> int:
        """Retourne le nombre de slots libres"""
        return self.max_slots - len(self.items)

    def is_full(self) -> bool:
        """Vérifie si l'inventaire est plein"""
        return len(self.items) >= self.max_slots

    def clear(self):
        """Vide l'inventaire"""
        self.items.clear()
