import unittest
import pygame
import os
from game.tiled_map import TiledMap
from game.coordinate_system import CoordinateSystem

class TestLayerRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation une seule fois pour toute la classe de test"""
        pygame.init()
        # Définir un mode vidéo avant les tests
        pygame.display.set_mode((800, 600))

    def setUp(self):
        """Initialisation avant chaque test"""
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.tile_size = 32
        
        # Créer un système de coordonnées pour les tests
        self.coord_system = CoordinateSystem(self.screen_width, self.screen_height, self.tile_size)
        
        # Charger la vraie map pour les tests
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_path = os.path.join(base_path, "assets", "mapv2.tmx")
        self.tiled_map = TiledMap(self.map_path)

    def test_ground_layer_rendering(self):
        """Test du rendu du calque sol"""
        # Créer un faux joueur pour le test
        player = pygame.sprite.Sprite()
        player.rect = pygame.Rect(0, 0, 32, 32)
        player.x, player.y = 0, 0  # Position au centre
        player.image = pygame.Surface((32, 32))
        
        # Rendre la map
        self.tiled_map.render(self.screen, player)
        
        # Vérifier que le calque sol a été rendu (pixel non noir au centre)
        center_color = self.screen.get_at((self.screen_width // 2, self.screen_height // 2))
        self.assertNotEqual(center_color, (0, 0, 0, 255))  # Ne devrait pas être noir

    def test_tree_layer_depth(self):
        """Test de la profondeur du calque arbres"""
        # Créer un faux joueur pour le test
        player = pygame.sprite.Sprite()
        player.rect = pygame.Rect(0, 0, 32, 32)
        player.image = pygame.Surface((32, 32))
        
        # Test avec le joueur devant un arbre
        player.x, player.y = 0, 0
        self.tiled_map.render(self.screen, player)
        screen_before = pygame.Surface((self.screen_width, self.screen_height))
        screen_before.blit(self.screen, (0, 0))
        
        # Test avec le joueur derrière un arbre
        player.y += self.tile_size  # Déplacer le joueur derrière l'arbre
        self.screen.fill((0, 0, 0))  # Effacer l'écran
        self.tiled_map.render(self.screen, player)
        
        # Les rendus devraient être différents
        pixels_before = pygame.surfarray.array3d(screen_before)
        pixels_after = pygame.surfarray.array3d(self.screen)
        self.assertFalse(
            (pixels_before == pixels_after).all(), 
            "Les rendus devraient être différents quand le joueur change de position"
        )

    def test_camera_centering(self):
        """Test du centrage de la caméra sur le joueur"""
        # Position initiale du joueur (-12, 1)
        player = pygame.sprite.Sprite()
        player.rect = pygame.Rect(0, 0, 32, 32)
        player.x, player.y = -12 * self.tile_size, 1 * self.tile_size
        player.image = pygame.Surface((32, 32))
        player.image.fill((255, 0, 0))  # Rouge pour le test
        
        # Rendre la map
        self.tiled_map.render(self.screen, player)
        
        # Le joueur devrait être au centre de l'écran
        expected_screen_x = self.screen_width // 2 - player.rect.width // 2
        expected_screen_y = self.screen_height // 2 - player.rect.height // 2
        
        # Vérifier la position du joueur
        center_color = self.screen.get_at((expected_screen_x + 16, expected_screen_y + 16))
        self.assertEqual(center_color, (255, 0, 0))  # Devrait être rouge (couleur du joueur)

    def test_relative_positions(self):
        """Test des positions relatives joueur/arbres"""
        # Créer un faux joueur
        player = pygame.sprite.Sprite()
        player.rect = pygame.Rect(0, 0, 32, 32)
        player.image = pygame.Surface((32, 32))
        player.image.fill((255, 0, 0))  # Rouge pour le joueur
        
        # Position initiale
        player.x, player.y = 0, 0
        self.tiled_map.render(self.screen, player)
        
        # Déplacer le joueur
        player.x += self.tile_size
        old_screen = self.screen.copy()
        self.screen.fill((0, 0, 0))
        self.tiled_map.render(self.screen, player)
        
        # La nouvelle position devrait être différente
        pixels_before = pygame.surfarray.array3d(old_screen)
        pixels_after = pygame.surfarray.array3d(self.screen)
        self.assertFalse(
            (pixels_before == pixels_after).all(),
            "Les rendus devraient être différents après déplacement du joueur"
        )

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
