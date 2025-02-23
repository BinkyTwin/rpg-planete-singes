import pygame
import os
from .base_scene import BaseScene

class MessageScene(BaseScene):
    def __init__(self, screen, game_state, message, display_manager=None, dialogue_getter=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        self.message = message
        self.dialogue_getter = dialogue_getter
        
        # Tailles de base pour les polices
        self.base_font_size = 24
        self.base_text_size = 20
        self.update_fonts()
        
        # Couleurs
        self.text_color = (255, 255, 255)  # Blanc pour le texte
        self.button_color = (70, 70, 70, 200)  # Gris foncé semi-transparent pour le bouton
        self.button_hover_color = (90, 90, 90, 220)  # Gris plus clair pour le survol
        self.button_text_color = (255, 255, 255)  # Blanc pour le texte du bouton
        self.dialog_bg_color = (40, 40, 40, 180)  # Fond de la boîte de dialogue
        self.dialog_border_color = (100, 100, 100, 255)  # Bordure de la boîte de dialogue
        
        # Dimensions de la boîte de dialogue
        self.padding = 20
        self.button_padding = 10
        
        # Calcul des dimensions du texte
        self.text_surface = self.text_font.render(message, True, self.text_color)
        text_width = self.text_surface.get_width()
        text_height = self.text_surface.get_height()
        
        # Dimensions de la boîte de dialogue
        dialog_width = min(500, max(300, text_width + self.padding * 2))
        dialog_height = text_height + self.padding * 3 + 40  # Extra space for button
        
        self.dialog_rect = pygame.Rect(
            (screen.get_width() - dialog_width) // 2,
            (screen.get_height() - dialog_height) // 2,
            dialog_width,
            dialog_height
        )
        
        # Bouton Quitter
        button_width = 120
        button_height = 35
        self.quit_button = pygame.Rect(
            self.dialog_rect.centerx - button_width // 2,
            self.dialog_rect.bottom - button_height - 15,
            button_width,
            button_height
        )
        self.quit_button_hover = False
        
        # Texte du bouton
        self.quit_text = self.text_font.render("Quitter", True, self.button_text_color)
        self.quit_text_hover = self.text_font.render("Quitter", True, (200, 200, 200))

    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            font_size = self.display_manager.get_scaled_font_size(self.base_font_size)
            text_size = self.display_manager.get_scaled_font_size(self.base_text_size)
        else:
            font_size = self.base_font_size
            text_size = self.base_text_size
            
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_font = pygame.font.SysFont("arial", text_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.quit_button.collidepoint(event.pos):
                    return 'game'
        elif event.type == pygame.MOUSEMOTION:
            self.quit_button_hover = self.quit_button.collidepoint(event.pos)
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            # Recalculer les dimensions et positions
            self.text_surface = self.text_font.render(self.message, True, self.text_color)
            text_width = self.text_surface.get_width()
            text_height = self.text_surface.get_height()
            
            dialog_width = min(500, max(300, text_width + self.padding * 2))
            dialog_height = text_height + self.padding * 3 + 40
            
            self.dialog_rect = pygame.Rect(
                (self.screen.get_width() - dialog_width) // 2,
                (self.screen.get_height() - dialog_height) // 2,
                dialog_width,
                dialog_height
            )
            
            button_width = 120
            button_height = 35
            self.quit_button.centerx = self.dialog_rect.centerx
            self.quit_button.bottom = self.dialog_rect.bottom - 15
        return None

    def update(self):
        pass

    def render(self, screen):
        # Assombrir légèrement le fond du jeu
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))  # Noir très légèrement transparent
        screen.blit(overlay, (0, 0))
        
        # Créer la surface de la boîte de dialogue avec transparence
        dialog_surface = pygame.Surface(self.dialog_rect.size, pygame.SRCALPHA)
        
        # Dessiner le fond de la boîte avec un dégradé
        for i in range(self.dialog_rect.height):
            alpha = min(180, 150 + i // 2)  # Dégradé de transparence
            pygame.draw.line(dialog_surface, (*self.dialog_bg_color[:3], alpha),
                           (0, i), (self.dialog_rect.width, i))
        
        # Ajouter une bordure élégante
        pygame.draw.rect(dialog_surface, self.dialog_border_color, dialog_surface.get_rect(), 2, border_radius=10)
        
        # Rendu du message avec gestion du retour à la ligne
        words = self.message.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = self.text_font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()
            
            if current_width + word_width > self.dialog_rect.width - self.padding * 2:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Afficher les lignes de texte
        y_offset = self.padding
        for line in lines:
            line_surface = self.text_font.render(line, True, self.text_color)
            text_rect = line_surface.get_rect(centerx=self.dialog_rect.width // 2, top=y_offset)
            dialog_surface.blit(line_surface, text_rect)
            y_offset += line_surface.get_height() + 5
        
        # Dessiner le bouton avec un effet de profondeur
        button_relative_rect = pygame.Rect(
            self.quit_button.x - self.dialog_rect.x,
            self.quit_button.y - self.dialog_rect.y,
            self.quit_button.width,
            self.quit_button.height
        )
        
        # Effet d'ombre du bouton
        shadow_rect = button_relative_rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(dialog_surface, (30, 30, 30, 150), shadow_rect, border_radius=5)
        
        # Corps du bouton
        button_color = self.button_hover_color if self.quit_button_hover else self.button_color
        pygame.draw.rect(dialog_surface, button_color, button_relative_rect, border_radius=5)
        
        # Bordure brillante du bouton
        if self.quit_button_hover:
            pygame.draw.rect(dialog_surface, (120, 120, 120, 255), button_relative_rect, 2, border_radius=5)
        else:
            pygame.draw.rect(dialog_surface, (90, 90, 90, 255), button_relative_rect, 2, border_radius=5)
        
        # Texte du bouton avec effet de brillance
        text_to_use = self.quit_text_hover if self.quit_button_hover else self.quit_text
        text_rect = text_to_use.get_rect(center=button_relative_rect.center)
        dialog_surface.blit(text_to_use, text_rect)
        
        # Afficher la boîte de dialogue
        screen.blit(dialog_surface, self.dialog_rect)
