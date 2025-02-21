import pygame
import os
from .base_scene import BaseScene
from game.tiled_map import TiledMap

class GameScene(BaseScene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        # Utilisation d'une police système
        self.font = pygame.font.SysFont("arial", 36)
        self.title_font = pygame.font.SysFont("arial", 48)
        # Obtenir le chemin de base du projet
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        map_path = os.path.join(self.base_path, "assets", "mapv2.tmx")
        self.tiled_map = TiledMap(map_path)
        self.collision_rects = self.tiled_map.get_collider_rects()
        
        # Variables pour l'animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # Millisecondes entre chaque frame
        self.last_direction = "down"  # Direction par défaut
        
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
            if key == pygame.K_z:
                dy = -1
                self.last_direction = "up"
            elif key == pygame.K_s:
                dy = 1
                self.last_direction = "down"
            elif key == pygame.K_q:
                dx = -1
                self.last_direction = "left"
            elif key == pygame.K_d:
                dx = 1
                self.last_direction = "right"
            
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
                # Mettre à jour l'animation
                self.animation_timer = pygame.time.get_ticks()
                self.animation_frame = (self.animation_frame + 1) % 4
                
    def update(self):
        # Mettre à jour l'animation si le joueur se déplace
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer >= self.animation_speed:
            self.animation_timer = current_time
            self.animation_frame = (self.animation_frame + 1) % 4
                
    def render(self):
        # Affichage de la carte
        map_surface = self.tiled_map.make_map()
        self.screen.blit(map_surface, (0, 0))
        
        # Affichage du joueur avec son sprite animé
        if self.game_state.player:
            # Obtenir le sprite actuel
            current_sprite = self.game_state.player.sprites[self.last_direction][self.animation_frame]
            
            # Calculer la position du joueur en pixels
            # Centre le sprite sur la tile
            player_x = self.game_state.player.x * self.tiled_map.tmx_data.tilewidth
            player_y = self.game_state.player.y * self.tiled_map.tmx_data.tileheight
            
            # Ajuster la position pour centrer le sprite plus grand sur la tile
            sprite_offset_x = (self.game_state.player.sprite_size - self.tiled_map.tmx_data.tilewidth) // 2
            sprite_offset_y = (self.game_state.player.sprite_size - self.tiled_map.tmx_data.tileheight) // 2
            
            player_pos = (
                player_x - sprite_offset_x,
                player_y - sprite_offset_y
            )
            
            # Afficher le sprite
            self.screen.blit(current_sprite, player_pos)
            
        # DEBUG: Affichage des rectangles de collision
        # for rect in self.collision_rects:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect, 1) 