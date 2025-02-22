import pygame
import os
from .base_scene import BaseScene
from game.tiled_map import TiledMap

class GameScene(BaseScene):
    def __init__(self, screen, game_state, display_manager=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        
        # Utilisation d'une police système avec taille de base
        self.base_font_size = 24
        self.base_title_size = 36
        self.update_fonts()
        
        # Obtenir le chemin de base du projet
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        map_path = os.path.join(self.base_path, "assets", "mapV3.tmx")
        self.tiled_map = TiledMap(map_path)
        self.collision_rects = self.tiled_map.get_collider_rects()
        
        # Position initiale du joueur (en bas de la carte)
        if self.game_state.player:
            # Position en tuiles (15, 28) - centre horizontal, près du bas
            self.game_state.player.x = 15 * self.tiled_map.tile_size
            self.game_state.player.y = 28 * self.tiled_map.tile_size
            self.game_state.player.rect.x = self.game_state.player.x
            self.game_state.player.rect.y = self.game_state.player.y
        
        # Mode debug
        self.debug_mode = True
        
        # Test initial des coordonnées
        self.test_coordinates()

        # Variables pour l'animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # Millisecondes entre chaque frame
        self.last_direction = "down"  # Direction par défaut
        
    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            font_size = self.display_manager.get_scaled_font_size(self.base_font_size)
            title_size = self.display_manager.get_scaled_font_size(self.base_title_size)
        else:
            font_size = self.base_font_size
            title_size = self.base_title_size
            
        self.font = pygame.font.SysFont("arial", font_size)
        self.title_font = pygame.font.SysFont("arial", title_size)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'menu'
            # Toggle debug mode with F3
            elif event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
            # Gestion du mouvement du joueur
            elif event.key in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]:
                self.handle_player_movement(event.key)
                
        # Si la fenêtre est redimensionnée, mettre à jour les polices
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            
        return None

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
                new_x * self.tiled_map.tile_size,
                new_y * self.tiled_map.tile_size,
                self.tiled_map.tile_size,
                self.tiled_map.tile_size
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
                
    def test_coordinates(self):
        """Test du système de coordonnées"""
        # Coordonnées de test
        test_screen_x, test_screen_y = 24, 343
        
        # Test 1: Conversion écran -> grille
        grid_x, grid_y = self.screen_to_grid(test_screen_x, test_screen_y)
        print(f"Test 1: Screen ({test_screen_x}, {test_screen_y}) -> Grid ({grid_x}, {grid_y})")
        
        # Test 2: Conversion grille -> écran
        back_screen_x, back_screen_y = self.grid_to_screen(grid_x, grid_y)
        print(f"Test 2: Grid ({grid_x}, {grid_y}) -> Screen ({back_screen_x}, {back_screen_y})")
        
        # Test 3: Vérification de la cohérence
        if abs(test_screen_x - back_screen_x) > 32 or abs(test_screen_y - back_screen_y) > 32:
            print("ERREUR: La conversion aller-retour n'est pas cohérente!")
        
    def screen_to_grid(self, screen_x, screen_y):
        """Convertit les coordonnées écran en coordonnées grille"""
        # Taille des tuiles
        tile_size = self.tiled_map.tile_size
        
        # Position de la caméra (centre de l'écran)
        camera_x = self.screen.get_width() // 2
        camera_y = self.screen.get_height() // 2
        
        # Position relative à la caméra
        rel_x = screen_x - camera_x
        rel_y = screen_y - camera_y
        
        # Conversion en coordonnées grille
        grid_x = rel_x // tile_size
        grid_y = rel_y // tile_size
        
        return grid_x, grid_y
        
    def grid_to_screen(self, grid_x, grid_y):
        """Convertit les coordonnées grille en coordonnées écran"""
        # Taille des tuiles
        tile_size = self.tiled_map.tile_size
        
        # Position de la caméra (centre de l'écran)
        camera_x = self.screen.get_width() // 2
        camera_y = self.screen.get_height() // 2
        
        # Conversion en coordonnées écran
        screen_x = (grid_x * tile_size) + camera_x
        screen_y = (grid_y * tile_size) + camera_y
        
        return screen_x, screen_y

    def render(self, screen):
        """Rendu de la scène de jeu"""
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Dessiner la carte
        if self.tiled_map:
            self.tiled_map.render(screen, self.game_state.player, self.display_manager)
            
            # Afficher les informations de débogage
            if self.debug_mode:
                # Position de la souris
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.display_manager:
                    mouse_x, mouse_y = self.display_manager.unscale_pos((mouse_x, mouse_y))
                grid_x, grid_y = self.screen_to_grid(mouse_x, mouse_y)
                
                debug_lines = [
                    f"Écran: ({int(mouse_x)}, {int(mouse_y)})",
                    f"Grille: ({grid_x}, {grid_y})",
                    f"Mode: {'Plein écran' if self.display_manager and self.display_manager.is_fullscreen else 'Fenêtré'}",
                    f"Échelle: {self.display_manager.scale_x:.2f}x" if self.display_manager else "Échelle: 1.0x"
                ]
                
                # Créer un fond semi-transparent
                padding = 10
                line_height = self.font.get_height()
                max_width = max(self.font.size(line)[0] for line in debug_lines)
                bg_height = (len(debug_lines) * line_height) + (padding * 2)
                
                bg_surface = pygame.Surface((max_width + padding * 2, bg_height))
                bg_surface.fill((0, 0, 0))
                bg_surface.set_alpha(128)
                screen.blit(bg_surface, (0, 0))
                
                # Afficher le texte
                y = padding
                for line in debug_lines:
                    text = self.font.render(line, True, (255, 255, 255))
                    screen.blit(text, (padding, y))
                    y += line_height
                    
        # Affichage du joueur avec son sprite animé
        if self.game_state.player:
            # Obtenir le sprite actuel
            current_sprite = self.game_state.player.sprites[self.last_direction][self.animation_frame]
            
            # Calculer la position du joueur en pixels
            # Centre le sprite sur la tile
            player_x = self.game_state.player.x * self.tiled_map.tile_size
            player_y = self.game_state.player.y * self.tiled_map.tile_size
            
            # Ajuster la position pour centrer le sprite plus grand sur la tile
            sprite_offset_x = (self.game_state.player.sprite_size - self.tiled_map.tile_size) // 2
            sprite_offset_y = (self.game_state.player.sprite_size - self.tiled_map.tile_size) // 2
            
            player_pos = (
                player_x - sprite_offset_x,
                player_y - sprite_offset_y
            )
            
            # Afficher le sprite
            screen.blit(current_sprite, player_pos)
            
        # DEBUG: Affichage des rectangles de collision
        # for rect in self.collision_rects:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect, 1) 