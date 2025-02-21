import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import os

class TiledMap:
    def __init__(self, filename):
        try:
            # Vérification que le fichier TMX existe
            abs_tmx_path = os.path.abspath(filename)
            print(f"Chemin absolu TMX: {abs_tmx_path}")
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Le fichier TMX '{filename}' n'existe pas")
            
            print(f"Chargement de la carte TMX: {filename}")
            self.tmx_data = load_pygame(filename)
            
            # Vérification des tilesets
            for tileset in self.tmx_data.tilesets:
                if tileset.source:
                    tileset_path = os.path.join(os.path.dirname(filename), tileset.source)
                    abs_tileset_path = os.path.abspath(tileset_path)
                    print(f"Chemin absolu tileset: {abs_tileset_path}")
                    print(f"Vérification du tileset: {tileset_path}")
                    if not os.path.exists(tileset_path):
                        raise FileNotFoundError(f"Le fichier tileset '{tileset_path}' n'existe pas")
                
                if hasattr(tileset, 'image') and tileset.image:
                    image_rel_path = os.path.join(os.path.dirname(tileset.source), tileset.image.source)
                    image_path = os.path.join(os.path.dirname(filename), image_rel_path)
                    abs_image_path = os.path.abspath(image_path)
                    print(f"Chemin relatif image: {image_rel_path}")
                    print(f"Chemin absolu image: {abs_image_path}")
                    print(f"Vérification de l'image du tileset: {image_path}")
                    if not os.path.exists(image_path):
                        raise FileNotFoundError(f"L'image du tileset '{image_path}' n'existe pas")
                    
                    # Test de chargement de l'image
                    try:
                        test_image = pygame.image.load(image_path)
                        print(f"Test de chargement réussi pour: {image_path}")
                    except pygame.error as e:
                        print(f"Erreur lors du chargement de l'image: {str(e)}")
                        raise
            
            self.width = self.tmx_data.width * self.tmx_data.tilewidth
            self.height = self.tmx_data.height * self.tmx_data.tileheight
            self.surface = pygame.Surface((self.width, self.height))
            self.render()
            
        except Exception as e:
            print(f"Erreur lors du chargement de la carte: {str(e)}")
            raise

    def render(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * self.tmx_data.tilewidth, 
                                               y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = self.surface.copy()
        return temp_surface

    def get_tile_properties(self, x, y, layer):
        """Récupère les propriétés d'une tuile à une position donnée"""
        try:
            return self.tmx_data.get_tile_properties(x, y, layer)
        except ValueError:
            return None

    def get_layer_by_name(self, name):
        """Récupère une couche par son nom"""
        return self.tmx_data.get_layer_by_name(name)

    def get_object_by_name(self, name):
        """Récupère un objet par son nom"""
        return self.tmx_data.get_object_by_name(name)

    def get_collider_rects(self, layer_name="collisions"):
        """Récupère les rectangles de collision d'une couche"""
        collision_layer = self.get_layer_by_name(layer_name)
        collision_tiles = []
        
        if collision_layer:
            for x, y, gid in collision_layer:
                if gid:  # Si la tuile n'est pas vide
                    collision_tiles.append(pygame.Rect(
                        x * self.tmx_data.tilewidth,
                        y * self.tmx_data.tileheight,
                        self.tmx_data.tilewidth,
                        self.tmx_data.tileheight
                    ))
        
        return collision_tiles 