from typing import List, Tuple, Optional
from random import randint, choice, random
from .items import ITEMS, Item, ItemType
from .map import Map, TileType
from .enemy import Enemy
from .factions import FactionName, FACTIONS, FactionRelation
from .player import Player

class SpawnManager:
    def __init__(self, game_map: Map):
        self.game_map = game_map
        self.spawned_items: List[Tuple[Item, int, int]] = []  # Liste des items avec leurs positions
        self.spawned_enemies: List[Enemy] = []
        
        # Calcul du nombre maximum d'items et d'ennemis basé sur la taille de la carte
        map_size = self.game_map.width * self.game_map.height
        self.max_items = max(2, map_size // 50)  # 1 item pour 50 cases, minimum 2 items
        self.max_enemies = max(1, map_size // 100)  # 1 ennemi pour 100 cases
        
        # Probabilités de spawn
        self.spawn_weights = {
            ItemType.WEAPON: 0.35,    # 35% de chance pour les armes
            ItemType.ARMOR: 0.30,     # 30% de chance pour les armures
            ItemType.POTION: 0.35     # 35% de chance pour les potions
        }
        
        # Changement de la probabilité de spawn pour les ennemis à 100%
        self.enemy_spawn_chance = 1.0  # 100% de chance qu'un ennemi apparaisse lors d'une mise à jour

    def get_random_empty_position(self) -> Optional[Tuple[int, int]]:
        """Trouve une position vide aléatoire sur la carte"""
        empty_positions = []
        
        # Parcourt la carte pour trouver toutes les positions vides
        for y in range(1, self.game_map.height - 1):  # Évite les bords
            for x in range(1, self.game_map.width - 1):  # Évite les bords
                if self.game_map.grid[y][x] == TileType.EMPTY.value:
                    empty_positions.append((x, y))
        
        # Retourne une position aléatoire parmi les positions vides
        return choice(empty_positions) if empty_positions else None

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
        return choice(available_items)

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
        # Gestion du spawn des items
        spawn_chance = (self.max_items - len(self.spawned_items)) * 0.2
        if random() < spawn_chance:
            self.spawn_item()
            
        # Gestion du spawn des ennemis
        if len(self.spawned_enemies) < self.max_enemies and random() < self.enemy_spawn_chance:
            # On ne peut pas spawner d'ennemis car il nous manque la faction du joueur
            return

    def update_with_player_faction(self, player_faction: FactionName):
        """Met à jour le spawn manager avec la faction du joueur"""
        if len(self.spawned_enemies) < self.max_enemies:
            self.spawn_enemy(player_faction)
        
        # Gestion du spawn des items
        spawn_chance = (self.max_items - len(self.spawned_items)) * 0.2
        if random() < spawn_chance:
            self.spawn_item()

    def get_item_at_position(self, x: int, y: int) -> Optional[Item]:
        """Retourne l'item à la position donnée s'il existe"""
        for item, item_x, item_y in self.spawned_items:
            if item_x == x and item_y == y:
                return item
        return None

    def spawn_enemy(self, player_faction: FactionName) -> bool:
        """Fait apparaître un ennemi à la position (3,5) avec une faction hostile"""
        print("\nTentative de spawn d'ennemi...")  # Debug
        print(f"Faction du joueur : {player_faction.value}")  # Debug
        
        if len(self.spawned_enemies) >= self.max_enemies:
            print("Nombre maximum d'ennemis atteint")  # Debug
            return False

        # Position fixe pour l'ennemi
        x, y = 3, 5
        
        # Vérifie si la position est disponible
        if self.game_map.grid[y][x] != TileType.EMPTY.value:
            print("La position est déjà occupée")  # Debug
            return False
        
        # Sélectionne une faction hostile au joueur
        hostile_factions = [faction for faction in FactionName 
                          if FACTIONS[player_faction].get_relation(faction) == FactionRelation.HOSTILE]
        
        print(f"Factions hostiles trouvées : {[f.value for f in hostile_factions]}")  # Debug
        
        if not hostile_factions:
            print("Aucune faction hostile disponible")  # Debug
            return False
            
        enemy_faction = choice(hostile_factions)
        print(f"Faction ennemie choisie : {enemy_faction.value}")  # Debug
        
        # Sélectionne une race aléatoire
        enemy_race = choice(list(Player.RACES.keys()))
        
        # Sélectionne une arme aléatoire
        weapons = [item for item in ITEMS.values() if item.item_type == ItemType.WEAPON]
        enemy_weapon = choice(weapons) if weapons else None
        
        # Crée l'ennemi
        enemy = Enemy(
            name=f"Ennemi {enemy_race.capitalize()}", 
            faction=enemy_faction,
            x=x,
            y=y,
            race=enemy_race,
            equipped_weapon=enemy_weapon
        )
        
        # Place l'ennemi sur la carte
        self.game_map.grid[y][x] = TileType.ENEMY.value
        self.spawned_enemies.append(enemy)
        
        print(f"Un {enemy_race.capitalize()} de la faction {enemy_faction.value} est apparu en ({x}, {y})")
        if enemy_weapon:
            print(f"Il est équipé d'un(e) {enemy_weapon.name}")
        
        return True

    def spawn_enemy_middle(self, player_faction: FactionName) -> bool:
        """Fait apparaître un ennemi vers le milieu de la map"""
        if len(self.spawned_enemies) >= self.max_enemies:
            return False
        
        # Calcule une zone centrale de spawn
        middle_y = self.game_map.height // 2
        middle_x = self.game_map.width // 2
        
        # Essaie plusieurs positions dans la zone centrale
        for y_offset in range(-2, 3):  # De -2 à +2 autour du milieu
            y = middle_y + y_offset
            if y <= 0 or y >= self.game_map.height - 1:
                continue
                
            for x_offset in range(-2, 3):  # De -2 à +2 autour du milieu
                x = middle_x + x_offset
                if x <= 0 or x >= self.game_map.width - 1:
                    continue
                    
                if self.game_map.grid[y][x] == TileType.EMPTY.value:
                    # Sélectionne une faction hostile au joueur
                    hostile_factions = [faction for faction in FactionName 
                                      if FACTIONS[player_faction].get_relation(faction).value == "hostile"]
                    if not hostile_factions:
                        return False
                    
                    enemy_faction = choice(hostile_factions)
                    enemy = Enemy(f"Ennemi {len(self.spawned_enemies) + 1}", enemy_faction, x, y)
                    self.game_map.add_item(TileType.ENEMY, x, y)
                    self.spawned_enemies.append(enemy)
                    print(f"\nUn ennemi est apparu en position ({x}, {y}) !")  # Debug
                    return True
        
        print("\nImpossible de faire apparaître un ennemi au centre de la carte.")  # Debug
        return False 