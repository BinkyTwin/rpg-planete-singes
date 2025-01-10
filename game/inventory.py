from typing import List, Optional
from .items import Item

class Inventory:
    def __init__(self, max_slots: int = 15):
        self.max_slots = max_slots
        self.items: List[Item] = []

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
        Retourne True si le retrait est réussi, False sinon
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False

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
