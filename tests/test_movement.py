import unittest
import pygame
from game.player import Player
from game.map import Map
from game.layer_manager import LayerManager, LayerType
from game.factions import FactionName

class TestMovement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # Créer une surface de test globale
        cls.test_surface = pygame.Surface((32, 32))
        cls.test_surface.fill((255, 255, 255))  # Remplir en blanc

    def setUp(self):
        self.screen = pygame.Surface((800, 600))
        
        # Créer une méthode de remplacement pour load_tiles
        def mock_load_tiles(self, layer_type, tile_paths):
            self.tiles[layer_type] = [TestMovement.test_surface]
        
        # Sauvegarder l'ancienne méthode
        self.original_load_tiles = LayerManager.load_tiles
        # Remplacer par notre mock
        LayerManager.load_tiles = mock_load_tiles
        
        # Créer une méthode de remplacement pour _load_character_sprites
        def mock_load_character_sprites(self, race):
            return {
                "down": [TestMovement.test_surface],
                "up": [TestMovement.test_surface],
                "left": [TestMovement.test_surface],
                "right": [TestMovement.test_surface]
            }
            
        # Sauvegarder l'ancienne méthode
        self.original_load_character_sprites = Player._load_character_sprites
        # Remplacer par notre mock
        Player._load_character_sprites = mock_load_character_sprites
        
        self.map = Map(20, 20)  # Crée une carte 20x20
        self.player = Player("Test", 1, 12, "chimpanze", FactionName.VEILLEURS)

    def test_player_movement(self):
        """Test des déplacements basiques du joueur"""
        # Test déplacement vers la droite
        initial_x = self.player.x
        self.player.move(1, 0)
        self.assertEqual(self.player.x, initial_x + self.player.speed)
        self.assertEqual(self.player.direction, "right")

        # Test déplacement vers la gauche
        self.player.move(-1, 0)
        self.assertEqual(self.player.x, initial_x)
        self.assertEqual(self.player.direction, "left")

    def test_collision_detection(self):
        """Test des collisions avec les obstacles"""
        # Ajoute un obstacle
        self.map.layer_manager.set_tile(LayerType.COLLISION, 2, 12, 1)
        
        # Essaie de se déplacer dans l'obstacle
        result = self.map.move_player(1, 0)
        self.assertFalse(result[0])  # Le mouvement devrait échouer

    def test_map_boundaries(self):
        """Test des limites de la carte"""
        # Essaie de sortir de la carte
        self.map.player_pos = (0, 0)  # Position le joueur au bord de la carte
        result = self.map.move_player(-1, 0)  # Essaie de sortir de la carte
        self.assertFalse(result[0])  # Le mouvement devrait échouer

    def test_tree_layer(self):
        """Test du calque d'arbres"""
        # Ajoute un arbre
        self.map.layer_manager.set_tile(LayerType.TREE, 2, 12, 1)
        
        # Vérifie que le joueur peut marcher sur le calque d'arbres
        result = self.map.move_player(1, 0)
        self.assertTrue(result[0])  # Le mouvement devrait réussir
        self.assertTrue(self.map.layer_manager.is_tree(2, 12))  # Devrait être sur un arbre

    def test_initial_position(self):
        """Test de la position initiale"""
        # Vérifie que la position initiale est correcte
        self.assertEqual(self.map.player_pos, (1, 12))
        
        # Vérifie que la position initiale n'est pas sur une collision
        self.assertFalse(self.map.layer_manager.is_collision(1, 12))

    def tearDown(self):
        # Restaurer les méthodes originales
        LayerManager.load_tiles = self.original_load_tiles
        Player._load_character_sprites = self.original_load_character_sprites

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
