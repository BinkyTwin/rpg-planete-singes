import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import os

class TiledMap:
    def __init__(self, filename):
        try:
            # Vérification que le fichier TMX existe
            abs_tmx_path = os.path.abspath(filename)
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Le fichier TMX '{filename}' n'existe pas")
            
            # Sauvegarder le répertoire de base pour les chemins relatifs
            self.base_dir = os.path.dirname(abs_tmx_path)
            
            # Charger la carte TMX
            self.map = load_pygame(filename)
            
            # Initialiser les propriétés de base
            self.width = self.map.width
            self.height = self.map.height
            self.tile_size = self.map.tilewidth
            self.pixel_width = self.width * self.tile_size
            self.pixel_height = self.height * self.tile_size
            
            print(f"Dimensions de la carte - Tuiles: {self.width}x{self.height}, Pixels: {self.pixel_width}x{self.pixel_height}")
            
        except Exception as e:
            print(f"Erreur lors du chargement de la carte: {str(e)}")
            raise

    def _get_camera_offset(self, screen, player_rect):
        """Calcule le décalage de la caméra pour centrer sur le joueur"""
        # Calculer le centre de l'écran
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculer la position cible de la caméra (centrée sur le joueur)
        target_x = player_rect.x - screen_width // 2 + self.tile_size // 2
        target_y = player_rect.y - screen_height // 2 + self.tile_size // 2
        
        # Debug: Afficher les positions de la caméra
        print(f"Camera - Target: ({target_x}, {target_y}), Screen: ({screen_width}, {screen_height})")
        print(f"Map Size: {self.pixel_width}x{self.pixel_height}, Player: ({player_rect.x}, {player_rect.y})")
        
        # Limiter la caméra aux bords de la carte
        camera_x = max(0, min(target_x, max(0, self.pixel_width - screen_width)))
        camera_y = max(0, min(target_y, max(0, self.pixel_height - screen_height)))
        
        # Debug: Afficher les offsets finaux
        print(f"Camera Offset: ({-camera_x}, {-camera_y})")
        
        # Retourner le décalage négatif pour le rendu
        return -camera_x, -camera_y

    def is_collision(self, grid_x, grid_y):
        """Vérifie s'il y a une collision à la position donnée"""
        print(f"Vérification collision à ({grid_x}, {grid_y})")
        
        # Vérifier les limites de la carte
        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            print(f"Hors limites de la carte")
            return True
            
        # Vérifier les collisions sur le calque obstacles
        obstacles_layer = self.get_layer_by_name("obstacles")
        if obstacles_layer and hasattr(obstacles_layer, 'data'):
            tile_gid = obstacles_layer.data[grid_y][grid_x]
            print(f"ID de la tuile d'obstacle : {tile_gid}")
            if tile_gid > 0:  # Si la tuile n'est pas vide
                print(f"Collision trouvée !")
                return True
        
        print(f"Pas de collision")
        return False

    def render(self, screen, camera_offset):
        """Rendu de la carte"""
        # Obtenir les dimensions de l'écran
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculer les tuiles visibles basées sur l'offset de la caméra
        start_x = max(0, -camera_offset[0] // self.tile_size)
        start_y = max(0, -camera_offset[1] // self.tile_size)
        end_x = min(self.width, (-camera_offset[0] + screen_width) // self.tile_size + 1)
        end_y = min(self.height, (-camera_offset[1] + screen_height) // self.tile_size + 1)
        
        print(f"Rendering tiles from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        print(f"Camera offset: {camera_offset}")
        
        # Dessiner chaque calque visible
        for layer in self.map.layers:
            if hasattr(layer, 'data'):  # Si c'est un calque de tuiles
                for y in range(int(start_y), int(end_y)):
                    for x in range(int(start_x), int(end_x)):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.map.get_tile_image_by_gid(gid)
                            if tile:
                                # Position de la tuile avec offset de caméra
                                pos_x = x * self.tile_size + camera_offset[0]
                                pos_y = y * self.tile_size + camera_offset[1]
                                
                                # Ne dessiner que si la tuile est visible à l'écran
                                if -self.tile_size <= pos_x <= screen_width and -self.tile_size <= pos_y <= screen_height:
                                    screen.blit(tile, (pos_x, pos_y))

    def get_layer_by_name(self, name):
        """Récupère un calque par son nom"""
        for layer in self.map.layers:
            if layer.name == name:
                return layer
        return None

    def get_collider_rects(self):
        """Retourne une liste de pygame.Rect pour toutes les tuiles avec collision"""
        collider_rects = []
        
        # Parcourir tous les calques
        for layer in self.map.layers:
            if hasattr(layer, 'data'):  # Si c'est un calque de tuiles
                for y in range(self.height):
                    for x in range(self.width):
                        tile = layer.data[y][x]
                        if tile and hasattr(tile, 'properties') and tile.properties.get('collision', False):
                            # Créer un rectangle de collision pour cette tuile
                            rect = pygame.Rect(
                                x * self.tile_size,
                                y * self.tile_size,
                                self.tile_size,
                                self.tile_size
                            )
                            collider_rects.append(rect)
        
        return collider_rects

    def is_wall(self, x, y):
        """Vérifie si la position donnée contient un mur (collision)"""
        return self.is_collision(x, y)