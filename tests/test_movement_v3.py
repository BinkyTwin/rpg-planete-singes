import unittest
import pygame
import os
from game.tiled_map import TiledMap
from game.player import Player
from game.factions import FactionName
from game.coordinate_system import CoordinateSystem

class TestMovementV3(unittest.TestCase):
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
        self.tile_size = 32
        
        # Charger la carte
        self.tiled_map = TiledMap(self.map_path)
        
        # Créer le système de coordonnées
        self.coord_system = CoordinateSystem(800, 600, self.tile_size)
        
        # Position initiale en bas de la carte
        spawn_x = 15 * self.tile_size  # Centre horizontal
        spawn_y = 28 * self.tile_size  # Près du bas
        
        # Créer le joueur
        self.player = Player(
            name="Test Player",
            x=spawn_x,
            y=spawn_y,
            race="gorille",
            faction=FactionName.VEILLEURS
        )

    def test_initial_spawn(self):
        """Test de la position initiale en bas de la carte"""
        # Convertir la position du joueur en coordonnées grille
        grid_x = self.player.x // self.tile_size
        grid_y = self.player.y // self.tile_size
        
        # Vérifier la position
        self.assertEqual(grid_x, 15)  # Centre horizontal
        self.assertEqual(grid_y, 28)  # Près du bas
        
        # Vérifier que la position est valide
        self.assertFalse(self.tiled_map.is_collision(grid_x, grid_y))

    def test_diagonal_movement(self):
        """Test du mouvement diagonal"""
        initial_x = self.player.x
        initial_y = self.player.y
        
        # Simuler un mouvement diagonal (haut-droite)
        keys = {pygame.K_d: True, pygame.K_z: True}
        self.player.update(keys)
        
        # Le mouvement diagonal devrait être normalisé (vitesse * sqrt(2)/2)
        dx = self.player.x - initial_x
        dy = self.player.y - initial_y
        
        # La distance diagonale devrait être égale dans les deux directions
        self.assertAlmostEqual(abs(dx), abs(dy), delta=0.1)
        
        # La vitesse diagonale devrait être environ 0.7071 (1/sqrt(2)) fois la vitesse normale
        expected_speed = self.tile_size * 0.7071
        self.assertAlmostEqual(abs(dx), expected_speed, delta=1)

    def test_camera_bounds(self):
        """Test des limites de la caméra aux bords de la carte"""
        # Déplacer le joueur vers le coin supérieur gauche
        self.player.x = 0
        self.player.y = 0
        
        # Rendre la scène
        self.tiled_map.render(self.screen, self.player)
        
        # Vérifier que le joueur est visible et pas hors de l'écran
        player_screen_x = self.player.x + self.tiled_map._get_camera_offset(self.screen, self.player)[0]
        player_screen_y = self.player.y + self.tiled_map._get_camera_offset(self.screen, self.player)[1]
        
        self.assertGreaterEqual(player_screen_x, 0)
        self.assertGreaterEqual(player_screen_y, 0)

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
