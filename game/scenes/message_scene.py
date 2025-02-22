import pygame
import os
from .base_scene import BaseScene

class MessageScene(BaseScene):
    def __init__(self, screen, game_state, message, display_manager=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        self.message = message
        
        # Tailles de base pour les polices
        self.base_title_size = 48
        self.base_text_size = 32
        self.update_fonts()
        
        # Couleurs
        self.text_color = (255, 255, 0)  # Jaune pour le texte
        self.selected_color = (255, 255, 255)  # Blanc pour la sélection
        
        # Image de fond
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        wallpaper_path = os.path.join(self.base_path, "assets", "wallpaper.png")
        self.background = pygame.image.load(wallpaper_path)
        
        # Bouton retour
        self.return_rect = pygame.Rect(
            screen.get_width() // 2 - 100,
            screen.get_height() - 80,
            200,
            40
        )
        self.return_alpha = 255  # Toujours visible
        
    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            title_size = self.display_manager.get_scaled_font_size(self.base_title_size)
            text_size = self.display_manager.get_scaled_font_size(self.base_text_size)
        else:
            title_size = self.base_title_size
            text_size = self.base_text_size
            
        self.title_font = pygame.font.SysFont("arial", title_size)
        self.text_font = pygame.font.SysFont("arial", text_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.return_rect.collidepoint(event.pos):
                    return 'menu'  # Retour au menu principal
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return 'menu'  # Retour au menu principal
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            # Mettre à jour la position du bouton retour
            self.return_rect.centerx = self.screen.get_width() // 2
            self.return_rect.bottom = self.screen.get_height() - 80
        return None

    def update(self):
        pass

    def render(self, screen):
        # Redimensionner l'image de fond
        scaled_bg = pygame.transform.scale(self.background, screen.get_size())
        screen.blit(scaled_bg, (0, 0))
        
        # Création d'une surface semi-transparente pour améliorer la lisibilité
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 128 pour semi-transparent
        screen.blit(overlay, (0, 0))
        
        # Message principal
        text = self.text_font.render(self.message, True, self.text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        
        # Rectangle semi-transparent derrière le texte
        padding = 20
        bg_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + (padding * 2),
            text_rect.height + (padding * 2)
        )
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (255, 255, 255, 40), bg_surface.get_rect(), border_radius=5)
        screen.blit(bg_surface, bg_rect)
        screen.blit(text, text_rect)
        
        # Bouton retour
        button_surface = pygame.Surface((self.return_rect.width, self.return_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (255, 255, 255, 80), button_surface.get_rect(), border_radius=5)
        screen.blit(button_surface, self.return_rect)
        
        return_text = self.text_font.render("Retour", True, self.selected_color)
        return_text_rect = return_text.get_rect(center=self.return_rect.center)
        screen.blit(return_text, return_text_rect)
