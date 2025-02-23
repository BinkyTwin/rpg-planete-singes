import unittest
import pygame
from unittest.mock import Mock
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.pnj2 import PNJ2

class TestPNJ2(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        pygame.init()
        # Créer un PNJ2 à une position fixe (10, 10)
        self.pnj2 = PNJ2((10, 10))
        
        # Créer un joueur factice avec des coordonnées modifiables
        self.player = Mock()
        self.player.x = 10
        self.player.y = 10

    def test_initialization(self):
        """Test de l'initialisation correcte du PNJ2"""
        self.assertEqual(self.pnj2.tile_x, 10)
        self.assertEqual(self.pnj2.tile_y, 10)
        self.assertEqual(self.pnj2.sprite_name, 'gorille.png')
        self.assertIsNone(self.pnj2.dialogue_system)
        self.assertFalse(self.pnj2.is_in_dialogue)
        self.assertEqual(self.pnj2.current_direction, "down")
        self.assertEqual(self.pnj2.TILE_SIZE, 32)

    def test_direction_update_right(self):
        """Test de la mise à jour de la direction vers la droite"""
        self.player.x = 15  # Joueur à droite du PNJ
        self.player.y = 10
        self.pnj2.can_trigger_dialogue(self.player)
        self.assertEqual(self.pnj2.current_direction, "right")

    def test_direction_update_left(self):
        """Test de la mise à jour de la direction vers la gauche"""
        self.player.x = 5  # Joueur à gauche du PNJ
        self.player.y = 10
        self.pnj2.can_trigger_dialogue(self.player)
        self.assertEqual(self.pnj2.current_direction, "left")

    def test_direction_update_down(self):
        """Test de la mise à jour de la direction vers le bas"""
        self.player.x = 10
        self.player.y = 15  # Joueur en dessous du PNJ
        self.pnj2.can_trigger_dialogue(self.player)
        self.assertEqual(self.pnj2.current_direction, "down")

    def test_direction_update_up(self):
        """Test de la mise à jour de la direction vers le haut"""
        self.player.x = 10
        self.player.y = 5  # Joueur au-dessus du PNJ
        self.pnj2.can_trigger_dialogue(self.player)
        self.assertEqual(self.pnj2.current_direction, "up")

    def test_diagonal_movement(self):
        """Test de la direction avec un mouvement diagonal"""
        # Le PNJ devrait choisir la direction avec la plus grande différence
        self.player.x = 15
        self.player.y = 12
        self.pnj2.can_trigger_dialogue(self.player)
        self.assertEqual(self.pnj2.current_direction, "right")

    def test_no_dialogue_trigger(self):
        """Test que le dialogue ne peut jamais être déclenché"""
        # Test à différentes positions
        test_positions = [(11, 10), (9, 10), (10, 11), (10, 9), (15, 15)]
        
        for x, y in test_positions:
            self.player.x = x
            self.player.y = y
            self.assertFalse(self.pnj2.can_trigger_dialogue(self.player))

    def test_dialogue_methods(self):
        """Test que toutes les méthodes de dialogue sont désactivées"""
        self.assertIsNone(self.pnj2.start_dialogue())
        self.assertIsNone(self.pnj2.next_message())
        self.assertTrue(self.pnj2.is_dialogue_finished())

if __name__ == '__main__':
    unittest.main() 