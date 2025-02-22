import unittest
import pygame
import os
from game.tiled_map import TiledMap

class TestMapLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation une seule fois pour toute la classe de test"""
        pygame.init()
        pygame.display.set_mode((800, 600))

    def setUp(self):
        """Initialisation avant chaque test"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_path = os.path.join(base_path, "assets", "mapV3.tmx")
        self.screen = pygame.Surface((800, 600))

    def test_map_loading(self):
        """Test du chargement de la nouvelle carte"""
        # Charger la carte
        tiled_map = TiledMap(self.map_path)
        
        # Vérifier les dimensions
        self.assertEqual(tiled_map.width, 30)
        self.assertEqual(tiled_map.height, 30)
        self.assertEqual(tiled_map.tile_size, 32)
        
        # Vérifier le tileset
        self.assertTrue("OGAtilesetsremixed" in tiled_map.map.tilesets[0].source)

    def test_layer_existence(self):
        """Test de l'existence des calques nécessaires"""
        tiled_map = TiledMap(self.map_path)
        
        # Vérifier les calques
        layers = [layer.name for layer in tiled_map.map.layers]
        self.assertIn("arrière plan", layers)
        
    def test_spawn_position(self):
        """Test de la position de spawn en bas de la carte"""
        tiled_map = TiledMap(self.map_path)
        
        # La position de spawn devrait être en bas de la carte
        spawn_x = 15  # Centre horizontal (30/2)
        spawn_y = 28  # Près du bas (30-2)
        
        # Vérifier que cette position est valide (pas de collision)
        self.assertFalse(tiled_map.is_collision(spawn_x, spawn_y))

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
