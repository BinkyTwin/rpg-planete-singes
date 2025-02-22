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
            
        except Exception as e:
            print(f"Erreur lors du chargement de la carte: {str(e)}")
            raise

    def _get_camera_offset(self, screen, player):
        """Calcule le décalage de la caméra pour centrer sur le joueur"""
        # Calculer le centre de l'écran
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculer la position cible de la caméra (centrée sur le joueur)
        target_x = player.x - screen_width // 2
        target_y = player.y - screen_height // 2
        
        # Limiter la caméra aux bords de la carte
        max_x = self.pixel_width - screen_width
        max_y = self.pixel_height - screen_height
        
        # Ajuster la position de la caméra
        camera_x = max(0, min(target_x, max_x))
        camera_y = max(0, min(target_y, max_y))
        
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

    def render(self, screen, player, display_manager=None):
        """Rendu de la carte"""
        # Obtenir les dimensions de l'écran
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculer les dimensions de la carte
        map_width = self.width * self.tile_size
        map_height = self.height * self.tile_size
        
        # Mettre à jour l'échelle si un DisplayManager est fourni
        if display_manager:
            display_manager.update_scale(screen_width, screen_height, map_width, map_height)
        
        # Dessiner chaque calque
        for layer in self.map.layers:
            if hasattr(layer, 'data'):  # Si c'est un calque de tuiles
                for y in range(self.height):
                    for x in range(self.width):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.map.get_tile_image_by_gid(gid)
                            if tile:
                                # Position de base de la tuile
                                pos_x = x * self.tile_size
                                pos_y = y * self.tile_size
                                
                                if display_manager:
                                    # Appliquer l'échelle et l'offset
                                    offset_x, offset_y = self._get_camera_offset(screen, player)
                                    scaled_pos = display_manager.get_scaled_pos((pos_x + offset_x, pos_y + offset_y))
                                    scaled_size = display_manager.get_scaled_size((self.tile_size, self.tile_size))
                                    
                                    # Redimensionner la tuile
                                    scaled_tile = pygame.transform.scale(tile, (int(scaled_size[0]), int(scaled_size[1])))
                                    screen.blit(scaled_tile, scaled_pos)
                                else:
                                    offset_x, offset_y = self._get_camera_offset(screen, player)
                                    screen.blit(tile, (pos_x + offset_x, pos_y + offset_y))

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