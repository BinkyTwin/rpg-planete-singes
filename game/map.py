from typing import List, Optional, Tuple
from enum import Enum
from random import choice
import pygame
from .layer_manager import LayerManager, LayerType

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
        
        # Initialisation du gestionnaire de calques
        self.layer_manager = LayerManager(width, height)
        
        # Position initiale du joueur (1, 12) comme spécifié
        self.player_pos = (1, 12)
        self.pnjs = []  # Liste pour stocker tous les PNJ
        
        # Chargement des tiles
        self._load_tiles()
        
    def _load_tiles(self):
        """Charge les tiles pour chaque calque"""
        # Charger les tiles du sol
        ground_tiles = [
            "assets/tiles/ground/grass.png",
            "assets/tiles/ground/dirt.png",
            "assets/tiles/ground/path.png"
        ]
        self.layer_manager.load_tiles(LayerType.GROUND, ground_tiles)
        
        # Charger les tiles de collision
        collision_tiles = [
            "assets/tiles/collision/rock.png",
            "assets/tiles/collision/wall.png"
        ]
        self.layer_manager.load_tiles(LayerType.COLLISION, collision_tiles)
        
        # Charger les tiles d'arbres
        tree_tiles = [
            "assets/tiles/tree/tree1.png",
            "assets/tiles/tree/tree2.png",
            "assets/tiles/tree/tree3.png"
        ]
        self.layer_manager.load_tiles(LayerType.TREE, tree_tiles)

    def is_valid_position(self, x: int, y: int) -> bool:
        """Vérifie si une position est valide sur la carte"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        # Vérifier s'il y a une collision à cette position
        return not self.layer_manager.is_collision(x, y)

    def add_pnj(self, pnj: 'PNJ'):
        """Ajoute un PNJ à la map"""
        # Si c'est le premier PNJ, le traiter comme le PNJ principal
        if not self.pnjs:
            self.pnj = pnj
            self.npc_pos = (pnj.tile_x, pnj.tile_y)
        
        self.pnjs.append(pnj)
        self.layer_manager.add_npc(pnj.tile_x, pnj.tile_y)
        pnj.map = self

    def remove_pnj(self):
        """Retire le PNJ de la map"""
        if self.pnj:
            self.layer_manager.remove_npc(self.pnj.tile_x, self.pnj.tile_y)
            if self.pnj in self.pnjs:
                self.pnjs.remove(self.pnj)
            self.pnj = None
            self.npc_pos = None

    def move_player(self, dx: int, dy: int) -> tuple[bool, str, Optional[Tuple[int, int]], bool]:
        """
        Déplace le joueur selon les deltas donnés
        Retourne (succès, message, position_item, rencontre_pnj)
        """
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # Vérifier les limites de la carte
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False, "Cette zone n'est pas accessible.", None, False

        # Vérifier s'il y a une collision
        if self.layer_manager.is_collision(new_x, new_y):
            return False, "Un obstacle bloque le passage.", None, False
        
        # Vérifie si la nouvelle position est le PNJ
        if self.pnj and self.pnj.is_visible and (new_x, new_y) == (self.pnj.tile_x, self.pnj.tile_y):
            return True, "", None, True

        # Met à jour la position du joueur
        self.player_pos = (new_x, new_y)
        
        # Vérifie si le joueur est sur un arbre (calque de profondeur)
        is_on_tree = self.layer_manager.is_tree(new_x, new_y)
        
        return True, "", None, False

    def render(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Rend la carte à l'écran"""
        # Rendre le calque de sol
        self.layer_manager.render_layer(screen, LayerType.GROUND, camera_x, camera_y)
        
        # Rendre le calque de collision
        self.layer_manager.render_layer(screen, LayerType.COLLISION, camera_x, camera_y)
        
        # Rendre le calque d'arbres
        self.layer_manager.render_layer(screen, LayerType.TREE, camera_x, camera_y)

        # Rendre tous les PNJ
        for pnj in self.pnjs:
            if pnj.is_visible:
                pnj.render(screen, camera_x, camera_y)

    def render_debug_info(self, screen):
        """Affiche les informations de débogage, notamment les coordonnées de la souris"""
        mouse_pos = pygame.mouse.get_pos()
        # Convertir les coordonnées de l'écran en coordonnées de la grille
        tile_size = 32  # Taille d'une tuile en pixels
        grid_x = mouse_pos[0] // tile_size
        grid_y = mouse_pos[1] // tile_size
        
        # Créer le texte à afficher
        debug_font = pygame.font.Font(None, 24)
        debug_text = f"Pos: ({mouse_pos[0]}, {mouse_pos[1]}) | Tuile: ({grid_x}, {grid_y})"
        text_surface = debug_font.render(debug_text, True, (255, 255, 255))
        
        # Ajouter un fond semi-transparent pour une meilleure lisibilité
        text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 6))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(128)
        screen.blit(text_bg, (5, 5))
        screen.blit(text_surface, (10, 8))

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
        for row in self.layer_manager.get_layer(LayerType.GROUND):
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
                if (self.layer_manager.is_empty(x, y) and 
                    0 < distance <= max_distance):
                    valid_positions.append((x, y))

        return valid_positions

    def generate_default_map(self):
        """Génère une carte par défaut avec quelques éléments"""
        # Ajoute des murs sur les bords
        for x in range(self.width):
            self.layer_manager.add_collision(x, 0)
            self.layer_manager.add_collision(x, self.height-1)
        for y in range(self.height):
            self.layer_manager.add_collision(0, y)
            self.layer_manager.add_collision(self.width-1, y)

        # Ajoute quelques arbres et de l'eau (ajusté pour la nouvelle taille)
        self.layer_manager.add_tree(3, 3)
        self.layer_manager.add_tree(4, 3)
        self.layer_manager.add_tree(5, 3)
        self.layer_manager.add_water(8, 6)
        self.layer_manager.add_water(8, 7)
        self.layer_manager.add_water(8, 8)

        # Place le joueur
        self.player_pos = (1, 1)

        # Place le PNJ à une distance maximale de 7 cases (augmenté pour la carte plus grande)
        valid_positions = self.get_valid_npc_positions(7)
        if valid_positions:
            x, y = choice(valid_positions)
            self.npc_pos = (x, y)
            self.layer_manager.add_npc(x, y)
