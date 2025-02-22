import unittest
import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.tiled_map import TiledMap
from game.display_manager import DisplayManager

class TestMapDisplay(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display_manager = DisplayManager()
        
        # Chemin vers la carte de test
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_path = os.path.join(self.base_path, "assets", "mapV3.tmx")
        self.tiled_map = TiledMap(self.map_path)

    def test_map_dimensions(self):
        """Vérifie que la carte est correctement dimensionnée"""
        # La carte doit avoir les dimensions spécifiées dans le fichier TMX
        self.assertEqual(self.tiled_map.width, 30)  # Largeur en tuiles
        self.assertEqual(self.tiled_map.height, 30)  # Hauteur en tuiles
        self.assertEqual(self.tiled_map.tile_size, 32)  # Taille des tuiles

    def test_map_scaling(self):
        """Vérifie que la carte est correctement mise à l'échelle"""
        # Calculer l'échelle attendue
        map_width = self.tiled_map.width * self.tiled_map.tile_size
        map_height = self.tiled_map.height * self.tiled_map.tile_size
        
        scale_x = self.screen_width / map_width
        scale_y = self.screen_height / map_height
        expected_scale = min(scale_x, scale_y)
        
        # Vérifier que l'échelle calculée par DisplayManager est correcte
        self.display_manager.update_scale(self.screen_width, self.screen_height, map_width, map_height)
        self.assertAlmostEqual(self.display_manager.scale_x, expected_scale, places=2)
        self.assertAlmostEqual(self.display_manager.scale_y, expected_scale, places=2)

    def test_map_position(self):
        """Vérifie que la carte est correctement positionnée"""
        # La carte doit être centrée si elle est plus petite que l'écran
        map_width = self.tiled_map.width * self.tiled_map.tile_size
        map_height = self.tiled_map.height * self.tiled_map.tile_size
        
        self.display_manager.update_scale(self.screen_width, self.screen_height, map_width, map_height)
        scaled_width = map_width * self.display_manager.scale_x
        scaled_height = map_height * self.display_manager.scale_y
        
        # Calculer les offsets attendus pour centrer la carte
        expected_offset_x = (self.screen_width - scaled_width) // 2
        expected_offset_y = (self.screen_height - scaled_height) // 2
        
        # Vérifier que les offsets sont corrects
        self.assertEqual(self.display_manager.offset_x, expected_offset_x)
        self.assertEqual(self.display_manager.offset_y, expected_offset_y)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
