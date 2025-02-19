from typing import List, Tuple, Optional
from random import randint, choice, random
from .items import ITEMS, Item, ItemType
from .map import Map, TileType

class SpawnManager:
    def __init__(self, game_map: Map):
        self.game_map = game_map
        self.spawned_items: List[Tuple[Item, int, int]] = []  # Liste des items avec leurs positions
        
        # Calcul du nombre maximum d'items basé sur la taille de la carte
        map_size = self.game_map.width * self.game_map.height
        self.max_items = max(2, map_size // 50)  # 1 item pour 50 cases, minimum 2 items
        
        # Probabilités de spawn par type d'item
        self.spawn_weights = {
            ItemType.WEAPON: 0.3,    # 30% de chance pour les armes
            ItemType.ARMOR: 0.2,     # 20% de chance pour les armures
            ItemType.POTION: 0.4,    # 40% de chance pour les potions
            ItemType.MISC: 0.1       # 10% de chance pour les objets divers
        }

    def get_random_empty_position(self) -> Optional[Tuple[int, int]]:
        """Trouve une position vide aléatoire sur la carte"""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            # Évite les bords de la carte
            x = randint(1, self.game_map.width - 2)
            y = randint(1, self.game_map.height - 2)
            
            # Vérifie si la position est vide et accessible
            if self.game_map.grid[y][x] == TileType.EMPTY.value:
                # Vérifie qu'il y a au moins une case vide adjacente
                adjacent_positions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                if any(self.game_map.grid[ny][nx] == TileType.EMPTY.value 
                      for nx, ny in adjacent_positions 
                      if self.game_map.is_valid_position(nx, ny)):
                    return x, y
            attempts += 1
        return None

    def select_random_item(self) -> Item:
        """Sélectionne un item aléatoire selon les probabilités définies"""
        # Filtre les items par type
        items_by_type = {type_: [] for type_ in ItemType}
        for item in ITEMS.values():
            items_by_type[item.item_type].append(item)

        # Sélectionne d'abord le type selon les poids
        rand = random()
        cumulative = 0
        selected_type = None
        for item_type, weight in self.spawn_weights.items():
            cumulative += weight
            if rand <= cumulative:
                selected_type = item_type
                break

        # Sélectionne un item aléatoire du type choisi
        available_items = items_by_type[selected_type]
        return choice(available_items) if available_items else choice(list(ITEMS.values()))

    def spawn_item(self) -> bool:
        """Tente de faire apparaître un nouvel item sur la carte"""
        if len(self.spawned_items) >= self.max_items:
            return False
            
        position = self.get_random_empty_position()
        if not position:
            return False
            
        item = self.select_random_item()
        x, y = position
        
        self.game_map.add_item(TileType.ITEM, x, y)
        self.spawned_items.append((item, x, y))
        return True

    def remove_item(self, x: int, y: int) -> Optional[Item]:
        """Retire un item de la carte et retourne l'item s'il existe"""
        for i, (item, item_x, item_y) in enumerate(self.spawned_items):
            if item_x == x and item_y == y:
                self.spawned_items.pop(i)
                self.game_map.remove_item(x, y)
                return item
        return None

    def update(self):
        """Met à jour le spawn manager (appelé périodiquement)"""
        # Probabilité de spawn augmente avec le nombre de places libres
        spawn_chance = (self.max_items - len(self.spawned_items)) * 0.2
        if random() < spawn_chance:
            self.spawn_item()

    def get_item_at_position(self, x: int, y: int) -> Optional[Item]:
        """Retourne l'item à la position donnée s'il existe"""
        for item, item_x, item_y in self.spawned_items:
            if item_x == x and item_y == y:
                return item
        return None

    def can_spawn_at(self, x: int, y: int) -> bool:
        """Vérifie si un item peut être spawné à cette position"""
        return (0 <= x < self.game_map.width and 
                0 <= y < self.game_map.height and 
                self.game_map.grid[y][x] == "." and  # Case vide
                self.game_map.grid[y][x] != "P")     # Pas sur un PNJ 