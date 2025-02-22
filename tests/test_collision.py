import unittest
import pygame
import pytmx
from game.collision_manager import CollisionManager

class TestCollisionManager(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        pygame.init()
        self.tile_size = 32
        
        # Création d'une mini-map de test 3x3
        self.map_data = {
            'collisions': [
                [0, 1, 0],  # 0 = pas de collision, 1 = collision
                [0, 0, 1],
                [1, 0, 1]
            ],
            'three': [
                [0, 0, 0],  # 0 = pas d'arbre, 1 = arbre
                [0, 0, 1],
                [1, 0, 0]
            ]
        }
        
        self.collision_manager = CollisionManager(self.map_data, self.tile_size)

    def test_basic_collision(self):
        """Test de collision basique avec un mur"""
        # Test position sans collision
        self.assertFalse(self.collision_manager.is_collision(0, 0))
        
        # Test position avec collision (mur)
        self.assertTrue(self.collision_manager.is_collision(1, 0))

    def test_map_boundaries(self):
        """Test des collisions avec les limites de la map"""
        # Test hors limites
        self.assertTrue(self.collision_manager.is_collision(-1, 0))
        self.assertTrue(self.collision_manager.is_collision(0, -1))
        self.assertTrue(self.collision_manager.is_collision(3, 0))
        self.assertTrue(self.collision_manager.is_collision(0, 3))

    def test_movement_validation(self):
        """Test de validation des mouvements"""
        # Test mouvement valide
        current_pos = (0, 0)
        new_pos = (0, 1)  # Mouvement vers une case libre
        self.assertTrue(self.collision_manager.can_move_to(current_pos, new_pos))
        
        # Test mouvement invalide (vers un mur)
        current_pos = (0, 1)
        new_pos = (2, 1)  # Mouvement vers une case avec collision
        self.assertFalse(self.collision_manager.can_move_to(current_pos, new_pos))

    def test_get_valid_move(self):
        """Test de l'obtention d'un mouvement valide"""
        # Test mouvement déjà valide
        current_pos = (0, 0)
        desired_pos = (0, 1)  # Mouvement vers une case libre
        result = self.collision_manager.get_valid_move(current_pos, desired_pos)
        self.assertEqual(result, desired_pos)
        
        # Test mouvement invalide (doit retourner la position actuelle)
        current_pos = (0, 1)
        desired_pos = (2, 1)  # Position avec collision
        result = self.collision_manager.get_valid_move(current_pos, desired_pos)
        self.assertEqual(result, current_pos)

    def test_layer_interaction(self):
        """Test des interactions avec les différents calques"""
        # Test position sur calque "three"
        self.assertTrue(self.collision_manager.is_on_tree(2, 1))
        self.assertFalse(self.collision_manager.is_on_tree(0, 0))
        
        # Test position sur calque "sol" (implicite, pas de collision ni d'arbre)
        self.assertTrue(self.collision_manager.is_on_ground(0, 1))
        self.assertFalse(self.collision_manager.is_on_ground(2, 1))  # Position avec arbre

if __name__ == '__main__':
    unittest.main()
