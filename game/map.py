from typing import List, Optional, Tuple
from enum import Enum
from random import choice

class TileType(Enum):
    EMPTY = "."      # Case vide
    WALL = "#"       # Mur
    PLAYER = "@"     # Joueur
    ITEM = "i"       # Objet
    ENEMY = "E"      # Ennemi
    TREE = "T"       # Arbre
    WATER = "~"      # Eau
    NPC = "P"        # PNJ changé en P

class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[str]] = [[TileType.EMPTY.value for _ in range(width)] for _ in range(height)]
        self.player_pos = (1, 1)  # Position initiale du joueur
        # Le PNJ sera placé lors de la génération de la carte
        self.npc_pos = None

    def is_valid_position(self, x: int, y: int) -> bool:
        """Vérifie si une position est valide sur la carte"""
        return 0 <= x < self.width and 0 <= y < self.height

    def add_item(self, tile_type: TileType, x: int, y: int) -> bool:
        """Ajoute un élément sur la carte à la position donnée"""
        if not self.is_valid_position(x, y):
            return False
        self.grid[y][x] = tile_type.value
        return True

    def remove_item(self, x: int, y: int) -> bool:
        """Retire un élément de la carte à la position donnée"""
        if not self.is_valid_position(x, y):
            return False
        self.grid[y][x] = TileType.EMPTY.value
        return True

    def move_player(self, dx: int, dy: int) -> tuple[bool, str, Optional[Tuple[int, int]], bool]:
        """
        Déplace le joueur selon les deltas donnés
        Retourne (succès, message, position_item, rencontre_pnj)
        """
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if not self.is_valid_position(new_x, new_y):
            return False, "Halte soldat ! Vous ne pouvez pas quitter la zone sécurisée.", None, False
        
        # Vérifie si la nouvelle position est le PNJ
        if (new_x, new_y) == self.npc_pos:
            return True, "", None, True

        # Vérifie si la nouvelle position n'est pas un mur
        if self.grid[new_y][new_x] == TileType.WALL.value:
            return False, "Un mur vous bloque le passage, impossible d'aller par là.", None, False

        # Vérifie si la nouvelle position contient un item
        found_item = None
        if self.grid[new_y][new_x] == TileType.ITEM.value:
            found_item = (new_x, new_y)

        # Efface l'ancienne position du joueur
        self.grid[self.player_pos[1]][self.player_pos[0]] = TileType.EMPTY.value
        
        # Met à jour la nouvelle position
        self.player_pos = (new_x, new_y)
        self.grid[new_y][new_x] = TileType.PLAYER.value
        return True, "", found_item, False

    def display(self):
        """Affiche la carte avec sa légende"""
        print("\n=== Carte ===")
        print("\nLégende :")
        print(f"{TileType.PLAYER.value} - Votre position")
        print(f"{TileType.WALL.value} - Mur")
        print(f"{TileType.TREE.value} - Arbre")
        print(f"{TileType.WATER.value} - Eau")
        print(f"{TileType.ENEMY.value} - Ennemi")
        print(f"{TileType.ITEM.value} - Objet")
        print(f"{TileType.NPC.value} - PNJ")
        print(f"{TileType.EMPTY.value} - Case vide")
        
        print("\nCarte :")
        print("=" * (self.width * 2 + 1))
        for row in self.grid:
            print("|" + " ".join(row) + "|")
        print("=" * (self.width * 2 + 1))

    def get_valid_npc_positions(self, max_distance: int = 5) -> List[Tuple[int, int]]:
        """Trouve toutes les positions valides pour le PNJ à une distance maximale donnée"""
        valid_positions = []
        player_x, player_y = self.player_pos

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Calcule la distance de Manhattan
                distance = abs(x - player_x) + abs(y - player_y)
                # Vérifie si la position est vide et à la bonne distance
                if (self.grid[y][x] == TileType.EMPTY.value and 
                    0 < distance <= max_distance):
                    valid_positions.append((x, y))

        return valid_positions

    def generate_default_map(self):
        """Génère une carte par défaut avec quelques éléments"""
        # Ajoute des murs sur les bords
        for x in range(self.width):
            self.add_item(TileType.WALL, x, 0)
            self.add_item(TileType.WALL, x, self.height-1)
        for y in range(self.height):
            self.add_item(TileType.WALL, 0, y)
            self.add_item(TileType.WALL, self.width-1, y)

        # Ajoute quelques arbres et de l'eau
        self.add_item(TileType.TREE, 3, 3)
        self.add_item(TileType.TREE, 4, 3)
        self.add_item(TileType.WATER, 6, 4)
        self.add_item(TileType.WATER, 6, 5)

        # Place le joueur
        self.add_item(TileType.PLAYER, 1, 1)
        self.player_pos = (1, 1)

        # Place le PNJ à une distance maximale de 5 cases
        valid_positions = self.get_valid_npc_positions(5)
        if valid_positions:
            x, y = choice(valid_positions)  # Utilise random.choice
            self.npc_pos = (x, y)
            self.add_item(TileType.NPC, x, y)
