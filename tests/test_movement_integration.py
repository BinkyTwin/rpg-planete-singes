import unittest
import pygame
import os
from game.tiled_map import TiledMap
from game.coordinate_system import CoordinateSystem
from game.collision_manager import CollisionManager
from game.player import Player
from game.scenes.game_scene import GameScene
from game.factions import FactionName

class TestMovementIntegration(unittest.TestCase):
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
        
        # Charger la map
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_path = os.path.join(base_path, "assets", "mapv2.tmx")
        self.tiled_map = TiledMap(self.map_path)
        
        # Créer les systèmes nécessaires
        self.coord_system = CoordinateSystem(self.screen_width, self.screen_height, self.tile_size)
        self.collision_manager = CollisionManager(self.tiled_map, self.tile_size)
        
        # Créer un joueur pour les tests
        self.player = Player(
            name="Test Player",
            x=-12 * self.tile_size,  # Position initiale en x
            y=1 * self.tile_size,    # Position initiale en y
            race="gorille",          # Race par défaut pour les tests
            faction=FactionName.VEILLEURS  # Faction par défaut
        )

    def test_initial_spawn(self):
        """Test du spawn initial aux coordonnées (-12, 1)"""
        # Vérifier la position initiale du joueur
        grid_x, grid_y = self.coord_system.screen_to_grid(self.player.x, self.player.y)
        self.assertEqual(grid_x, -12)
        self.assertEqual(grid_y, 1)
        
        # Vérifier que la position initiale est valide (pas de collision)
        self.assertFalse(
            self.collision_manager.is_collision(grid_x, grid_y),
            "La position initiale ne devrait pas être sur une collision"
        )

    def test_movement_input(self):
        """Test du déplacement complet (input -> mouvement -> rendu)"""
        # Position initiale
        initial_x = self.player.x
        initial_y = self.player.y
        
        # Simuler un mouvement vers la droite
        keys = {pygame.K_d: True}  # Touche D enfoncée
        self.player.update(keys, self.collision_manager)
        
        # Vérifier que le joueur s'est déplacé vers la droite
        self.assertGreater(self.player.x, initial_x)
        self.assertEqual(self.player.y, initial_y)  # Y ne devrait pas changer
        
        # Vérifier que la nouvelle position est valide
        grid_x, grid_y = self.coord_system.screen_to_grid(self.player.x, self.player.y)
        self.assertFalse(
            self.collision_manager.is_collision(grid_x, grid_y),
            "La nouvelle position ne devrait pas être sur une collision"
        )

    def test_camera_player_sync(self):
        """Test de la synchronisation caméra/joueur"""
        # Rendre la scène
        self.tiled_map.render(self.screen, self.player)
        
        # Le joueur devrait être au centre de l'écran
        screen_center_x = self.screen_width // 2
        screen_center_y = self.screen_height // 2
        
        # Obtenir la position du joueur sur l'écran
        offset_x, offset_y = self.tiled_map._get_camera_offset(self.screen, self.player)
        player_screen_x = self.player.x + offset_x
        player_screen_y = self.player.y + offset_y
        
        # Vérifier que le joueur est bien centré (à 16 pixels près - demi-tuile)
        self.assertAlmostEqual(player_screen_x, screen_center_x - self.tile_size // 2, delta=16)
        self.assertAlmostEqual(player_screen_y, screen_center_y - self.tile_size // 2, delta=16)

    def test_layer_transitions(self):
        """Test des transitions entre calques"""
        # Position initiale
        initial_x = self.player.x
        initial_y = self.player.y
        
        # Déplacer le joueur sur un arbre
        tree_layer = self.tiled_map.get_layer_by_name('three')
        if tree_layer:
            # Trouver une position avec un arbre
            for x, y, gid in tree_layer:
                if gid:  # Si il y a un arbre
                    # Convertir en coordonnées écran
                    tree_screen_x = x * self.tile_size
                    tree_screen_y = y * self.tile_size
                    
                    # Placer le joueur à cette position
                    self.player.x = tree_screen_x
                    self.player.y = tree_screen_y
                    break
        
        # Rendre la scène avant et après
        self.tiled_map.render(self.screen, self.player)
        screen_before = pygame.Surface((self.screen_width, self.screen_height))
        screen_before.blit(self.screen, (0, 0))
        
        # Déplacer le joueur derrière l'arbre
        self.player.y += self.tile_size
        self.screen.fill((0, 0, 0))
        self.tiled_map.render(self.screen, self.player)
        
        # Les rendus devraient être différents
        pixels_before = pygame.surfarray.array3d(screen_before)
        pixels_after = pygame.surfarray.array3d(self.screen)
        self.assertFalse(
            (pixels_before == pixels_after).all(),
            "Le rendu devrait changer quand le joueur passe derrière un arbre"
        )

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
