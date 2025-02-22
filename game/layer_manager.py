import pygame
from enum import Enum

class LayerType(Enum):
    GROUND = "ground"  # Calque de sol
    COLLISION = "collision"  # Calque de collision
    TREE = "tree"  # Calque des arbres (profondeur)
    NPC = "npc"  # Calque des PNJ

class LayerManager:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Initialisation des calques
        self.layers = {
            LayerType.GROUND: [[0 for _ in range(width)] for _ in range(height)],
            LayerType.COLLISION: [[0 for _ in range(width)] for _ in range(height)],
            LayerType.TREE: [[0 for _ in range(width)] for _ in range(height)],
            LayerType.NPC: [[0 for _ in range(width)] for _ in range(height)]
        }
        
        # Chargement des tiles
        self.tiles = {
            LayerType.GROUND: [],  # Liste des tiles de sol
            LayerType.COLLISION: [],  # Liste des tiles de collision
            LayerType.TREE: [],  # Liste des tiles d'arbres
            LayerType.NPC: []  # Liste des tiles de PNJ
        }
        
    def load_tiles(self, layer_type: LayerType, tile_paths: list):
        """Charge les tiles pour un calque spécifique"""
        for path in tile_paths:
            tile = pygame.image.load(path).convert_alpha()
            self.tiles[layer_type].append(tile)
            
    def set_tile(self, layer_type: LayerType, x: int, y: int, tile_id: int):
        """Place un tile sur un calque à une position donnée"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.layers[layer_type][y][x] = tile_id
            
    def get_tile(self, layer_type: LayerType, x: int, y: int) -> int:
        """Récupère l'ID du tile à une position donnée sur un calque"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.layers[layer_type][y][x]
        return 0
        
    def is_collision(self, x: int, y: int) -> bool:
        """Vérifie s'il y a une collision à la position donnée"""
        return self.get_tile(LayerType.COLLISION, x, y) != 0
        
    def is_tree(self, x: int, y: int) -> bool:
        """Vérifie si la position est sur un arbre (calque de profondeur)"""
        return self.get_tile(LayerType.TREE, x, y) != 0

    def add_npc(self, x: int, y: int):
        """Ajoute un PNJ sur le calque des PNJ"""
        self.set_tile(LayerType.NPC, x, y, 1)

    def remove_npc(self, x: int, y: int):
        """Retire un PNJ du calque des PNJ"""
        self.set_tile(LayerType.NPC, x, y, 0)
        
    def render_layer(self, screen: pygame.Surface, layer_type: LayerType, camera_x: int = 0, camera_y: int = 0):
        """Rend un calque spécifique à l'écran"""
        tile_size = 32  # Taille d'un tile en pixels
        
        # Calculer la zone visible
        start_x = max(0, camera_x // tile_size)
        start_y = max(0, camera_y // tile_size)
        end_x = min(self.width, (camera_x + screen.get_width()) // tile_size + 1)
        end_y = min(self.height, (camera_y + screen.get_height()) // tile_size + 1)
        
        # Rendu des tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_id = self.layers[layer_type][y][x]
                if tile_id > 0 and layer_type in self.tiles and self.tiles[layer_type]:  # Si le tile n'est pas vide et qu'il y a des tiles chargés
                    screen_x = x * tile_size - camera_x
                    screen_y = y * tile_size - camera_y
                    screen.blit(self.tiles[layer_type][tile_id - 1], (screen_x, screen_y))
