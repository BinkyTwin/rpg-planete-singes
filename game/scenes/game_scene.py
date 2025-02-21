import pygame
from .base_scene import BaseScene
from game.tiled_map import TiledMap

class GameScene(BaseScene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.tiled_map = TiledMap("assets/mapv2.tmx")
        self.player_image = pygame.Surface((32, 32))  # Placeholder pour l'image du joueur
        self.player_image.fill((255, 0, 0))  # Rectangle rouge pour le joueur
        self.collision_rects = self.tiled_map.get_collider_rects()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'menu'
            # Gestion du mouvement du joueur
            elif event.key in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]:
                self.handle_player_movement(event.key)
                
    def handle_player_movement(self, key):
        if self.game_state.player:
            dx, dy = 0, 0
            if key == pygame.K_z: dy = -1
            elif key == pygame.K_s: dy = 1
            elif key == pygame.K_q: dx = -1
            elif key == pygame.K_d: dx = 1
            
            # Calcul de la nouvelle position
            new_x = self.game_state.player.x + dx
            new_y = self.game_state.player.y + dy
            
            # Création d'un rectangle pour le joueur à la nouvelle position
            new_player_rect = pygame.Rect(
                new_x * self.tiled_map.tmx_data.tilewidth,
                new_y * self.tiled_map.tmx_data.tileheight,
                self.tiled_map.tmx_data.tilewidth,
                self.tiled_map.tmx_data.tileheight
            )
            
            # Vérification des collisions
            can_move = True
            for collision_rect in self.collision_rects:
                if new_player_rect.colliderect(collision_rect):
                    can_move = False
                    break
            
            # Mise à jour de la position si aucune collision
            if can_move:
                self.game_state.player.x = new_x
                self.game_state.player.y = new_y
                
    def render(self):
        # Affichage de la carte
        map_surface = self.tiled_map.make_map()
        self.screen.blit(map_surface, (0, 0))
        
        # Affichage du joueur
        if self.game_state.player:
            player_pos = (
                self.game_state.player.x * self.tiled_map.tmx_data.tilewidth,
                self.game_state.player.y * self.tiled_map.tmx_data.tileheight
            )
            self.screen.blit(self.player_image, player_pos)
            
        # DEBUG: Affichage des rectangles de collision
        # for rect in self.collision_rects:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect, 1) 