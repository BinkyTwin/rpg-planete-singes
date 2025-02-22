import unittest
import pygame
from game.coordinate_system import CoordinateSystem

class TestCoordinateSystem(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.tile_size = 32
        self.coord_system = CoordinateSystem(self.screen_width, self.screen_height, self.tile_size)

    def test_screen_to_grid(self):
        """Test de conversion des coordonnées écran vers grille"""
        # Test avec des coordonnées positives au centre
        screen_x, screen_y = 400, 300  # Centre de l'écran
        grid_x, grid_y = self.coord_system.screen_to_grid(screen_x, screen_y)
        self.assertEqual(grid_x, 0)  # Au centre, devrait être (0,0) en coordonnées grille
        self.assertEqual(grid_y, 0)

        # Test avec des coordonnées négatives
        screen_x, screen_y = 400 - 32 * 12, 300 + 32  # Pour obtenir (-12, 1)
        grid_x, grid_y = self.coord_system.screen_to_grid(screen_x, screen_y)
        self.assertEqual(grid_x, -12)
        self.assertEqual(grid_y, 1)

    def test_grid_to_screen(self):
        """Test de conversion des coordonnées grille vers écran"""
        # Test avec la position initiale du joueur (-12, 1)
        grid_x, grid_y = -12, 1
        screen_x, screen_y = self.coord_system.grid_to_screen(grid_x, grid_y)
        self.assertEqual(screen_x, 400 - 32 * 12)  # Centre - 12 tuiles
        self.assertEqual(screen_y, 300 + 32)  # Centre + 1 tuile

    def test_conversion_roundtrip(self):
        """Test de conversion aller-retour"""
        # Partir de coordonnées grille
        original_grid_x, original_grid_y = -12, 1
        
        # Convertir en coordonnées écran
        screen_x, screen_y = self.coord_system.grid_to_screen(original_grid_x, original_grid_y)
        
        # Reconvertir en coordonnées grille
        final_grid_x, final_grid_y = self.coord_system.screen_to_grid(screen_x, screen_y)
        
        # Vérifier que nous retrouvons les coordonnées originales
        self.assertEqual(original_grid_x, final_grid_x)
        self.assertEqual(original_grid_y, final_grid_y)

    def test_camera_offset(self):
        """Test du calcul du décalage de la caméra"""
        # Test avec le joueur au centre
        player_pos = (0, 0)
        offset_x, offset_y = self.coord_system.get_camera_offset(player_pos)
        self.assertEqual(offset_x, self.screen_width // 2)
        self.assertEqual(offset_y, self.screen_height // 2)

        # Test avec le joueur à (-12, 1)
        player_pos = (-12, 1)
        offset_x, offset_y = self.coord_system.get_camera_offset(player_pos)
        expected_x = self.screen_width // 2 + (-12 * self.tile_size)
        expected_y = self.screen_height // 2 + (1 * self.tile_size)
        self.assertEqual(offset_x, expected_x)
        self.assertEqual(offset_y, expected_y)

if __name__ == '__main__':
    unittest.main()
