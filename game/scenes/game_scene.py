import pygame
from .base_scene import BaseScene

class GameScene(BaseScene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.map_image = pygame.image.load("assets/map.png")
        self.player_image = pygame.Surface((32, 32))  # Placeholder pour l'image du joueur
        self.player_image.fill((255, 0, 0))  # Rectangle rouge pour le joueur
        
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
            
            # Mise à jour de la position du joueur
            # Ajoutez ici la logique de collision
                
    def render(self):
        # Affichage de la carte
        self.screen.blit(self.map_image, (0, 0))
        
        # Affichage du joueur
        if self.game_state.player:
            player_pos = (
                self.game_state.player.x * 32,  # 32 est la taille d'une tuile
                self.game_state.player.y * 32
            )
            self.screen.blit(self.player_image, player_pos) 