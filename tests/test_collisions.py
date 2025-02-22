import unittest
import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.tiled_map import TiledMap
from game.player import Player
from game.factions import FactionName

class TestCollisions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
        # Charger la carte
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.map_path = os.path.join(self.base_path, "assets", "test_map.tmx")
        self.tiled_map = TiledMap(self.map_path)
        
        # Créer un joueur pour les tests
        start_x = 5 * self.tiled_map.tile_size
        start_y = 5 * self.tiled_map.tile_size
        self.player = Player("Test", start_x, start_y, "chimpanze", FactionName.VEILLEURS)
        self.player.rect.x = start_x
        self.player.rect.y = start_y

    def test_wall_collision(self):
        """Vérifie que le joueur ne peut pas traverser les murs"""
        # Trouver un mur dans la carte
        wall_found = False
        for y in range(self.tiled_map.height):
            for x in range(self.tiled_map.width):
                if self.tiled_map.is_wall(x, y):
                    # Placer le joueur juste à côté du mur
                    self.player.x = (x - 1) * self.tiled_map.tile_size
                    self.player.y = y * self.tiled_map.tile_size
                    self.player.rect.x = self.player.x
                    self.player.rect.y = self.player.y
                    wall_found = True
                    break
            if wall_found:
                break
                
        self.assertTrue(wall_found, "Aucun mur trouvé dans la carte")
        
        # Essayer de déplacer le joueur dans le mur
        dx = self.tiled_map.tile_size
        dy = 0
        
        # Sauvegarder la position initiale
        initial_x = self.player.x
        initial_y = self.player.y
        
        # Tenter le déplacement
        self.player.move(dx, dy, self.tiled_map)
        
        # Vérifier que le joueur n'a pas traversé le mur
        self.assertEqual(self.player.x, initial_x)
        self.assertEqual(self.player.y, initial_y)

    def test_valid_movement(self):
        """Vérifie que le joueur peut se déplacer dans les espaces vides"""
        # Trouver un espace vide
        empty_found = False
        for y in range(self.tiled_map.height):
            for x in range(self.tiled_map.width):
                if not self.tiled_map.is_wall(x, y) and not self.tiled_map.is_wall(x + 1, y):
                    # Placer le joueur dans l'espace vide
                    self.player.x = x * self.tiled_map.tile_size
                    self.player.y = y * self.tiled_map.tile_size
                    self.player.rect.x = self.player.x
                    self.player.rect.y = self.player.y
                    empty_found = True
                    break
            if empty_found:
                break
                
        self.assertTrue(empty_found, "Aucun espace vide trouvé dans la carte")
        
        # Déplacer le joueur dans l'espace vide
        dx = self.tiled_map.tile_size
        dy = 0
        
        # Sauvegarder la position initiale
        initial_x = self.player.x
        
        # Tenter le déplacement
        self.player.move(dx, dy, self.tiled_map)
        
        # Vérifier que le joueur s'est déplacé
        self.assertEqual(self.player.x, initial_x + dx)

    def test_diagonal_collision(self):
        """Vérifie que les collisions diagonales sont correctement gérées"""
        # Trouver un coin de mur
        corner_found = False
        for y in range(1, self.tiled_map.height - 1):
            for x in range(1, self.tiled_map.width - 1):
                if (self.tiled_map.is_wall(x, y) and 
                    not self.tiled_map.is_wall(x - 1, y) and 
                    not self.tiled_map.is_wall(x, y - 1)):
                    # Placer le joueur en diagonale du coin
                    self.player.x = (x - 1) * self.tiled_map.tile_size
                    self.player.y = (y - 1) * self.tiled_map.tile_size
                    self.player.rect.x = self.player.x
                    self.player.rect.y = self.player.y
                    corner_found = True
                    break
            if corner_found:
                break
                
        self.assertTrue(corner_found, "Aucun coin de mur trouvé dans la carte")
        
        # Essayer de déplacer le joueur en diagonale vers le coin
        dx = self.tiled_map.tile_size
        dy = self.tiled_map.tile_size
        
        # Sauvegarder la position initiale
        initial_x = self.player.x
        initial_y = self.player.y
        
        # Tenter le déplacement
        self.player.move(dx, dy, self.tiled_map)
        
        # Vérifier que le joueur n'a pas traversé le coin
        self.assertEqual(self.player.x, initial_x)
        self.assertEqual(self.player.y, initial_y)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
