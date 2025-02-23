import pygame
import sys
import os
from .base_scene import BaseScene

class MenuScene(BaseScene):
    def __init__(self, screen, game_state, display_manager=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        
        # Tailles de base pour les polices
        self.base_title_size = 48
        self.base_subtitle_size = 32
        self.base_menu_size = 32
        self.update_fonts()
        
        # Options du menu
        self.menu_options = ["Nouvelle Partie", "Charger Partie", "Options", "Quitter"]
        self.selected_option = 0
        self.hovered_option = -1
        
        # Couleurs
        self.text_color = (255, 255, 255)  # Blanc pour le texte
        self.selected_color = (255, 255, 0)  # Jaune pour la sélection
        
        # Image de fond et icône
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        wallpaper_path = os.path.join(self.base_path, "assets", "wallpaper.png")
        self.background = pygame.image.load(wallpaper_path)
        
        # Configuration de l'icône de l'application
        try:
            icon_path = os.path.join(self.base_path, "assets", "logo.png")
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Erreur lors du chargement de l'icône : {e}")
        
        # Création des rectangles pour les options du menu
        self.menu_rects = []
        center_x = screen.get_width() // 2
        start_y = screen.get_height() // 2
        
        for i in range(len(self.menu_options)):
            rect = pygame.Rect(0, 0, 300, 50)  # Rectangles plus grands et uniformes
            rect.center = (center_x, start_y + i * 70)  # Plus d'espace entre les options
            self.menu_rects.append(rect)
        
        # Alphas pour les animations
        self.menu_alphas = [0] * len(self.menu_options)
        self.hover_transition_speed = 20

    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            title_size = self.display_manager.get_scaled_font_size(self.base_title_size)
            subtitle_size = self.display_manager.get_scaled_font_size(self.base_subtitle_size)
            menu_size = self.display_manager.get_scaled_font_size(self.base_menu_size)
        else:
            title_size = self.base_title_size
            subtitle_size = self.base_subtitle_size
            menu_size = self.base_menu_size
            
        self.title_font = pygame.font.SysFont("arial", title_size)
        self.subtitle_font = pygame.font.SysFont("arial", subtitle_size)
        self.menu_font = pygame.font.SysFont("arial", menu_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_option = -1
            for i, rect in enumerate(self.menu_rects):
                if rect.collidepoint(mouse_pos):
                    self.hovered_option = i
                    break
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered_option != -1:
                self.selected_option = self.hovered_option
                return self._handle_option_selection()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                return self._handle_option_selection()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            
        return None

    def _handle_option_selection(self):
        option = self.menu_options[self.selected_option]
        if option == "Nouvelle Partie":
            return 'character_creation'
        elif option == "Charger Partie":
            self.game_state.temp_message = "Aucune partie sauvegardée"
            return 'message'
        elif option == "Options":
            self.game_state.temp_message = "En cours de construction"
            return 'message'
        elif option == "Quitter":
            pygame.quit()
            sys.exit()
        return None

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Mise à jour des alphas des boutons du menu
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(mouse_pos) or i == self.selected_option:
                self.menu_alphas[i] = min(self.menu_alphas[i] + self.hover_transition_speed, 255)
            else:
                self.menu_alphas[i] = max(self.menu_alphas[i] - self.hover_transition_speed, 0)

    def render(self, screen):
        # Fond d'écran
        scaled_bg = pygame.transform.scale(self.background, screen.get_size())
        screen.blit(scaled_bg, (0, 0))
        
        # Overlay semi-transparent
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Affichage du titre et sous-titre
        title_text = self.title_font.render("Planète des Singes", True, self.text_color)
        subtitle_text = self.subtitle_font.render("RPG", True, self.selected_color)
        
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        subtitle_rect = subtitle_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4 + 50))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Rendu des options du menu
        for i, (option, rect) in enumerate(zip(self.menu_options, self.menu_rects)):
            # Surface du bouton avec animation alpha
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            
            # Couleur de fond du bouton
            if i == self.selected_option:
                bg_color = (255, 255, 255, min(80 + self.menu_alphas[i] // 2, 160))
            else:
                bg_color = (255, 255, 255, min(40 + self.menu_alphas[i] // 3, 120))
            
            # Dessin du rectangle arrondi
            pygame.draw.rect(button_surface, bg_color, button_surface.get_rect(), border_radius=10)
            screen.blit(button_surface, rect)
            
            # Texte de l'option
            color = self.selected_color if i == self.selected_option else self.text_color
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
            # Bordure du bouton
            pygame.draw.rect(screen, (255, 255, 255, min(100 + self.menu_alphas[i], 255)), 
                           rect, 2, border_radius=10)

    def show_message(self, message):
        """Affiche un message temporaire avec le même style que le reste"""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        
        # Création d'un rectangle pour le message
        msg_rect = pygame.Rect(0, 0, 400, 100)
        msg_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        
        # Surface du message
        msg_surface = pygame.Surface((msg_rect.width, msg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(msg_surface, (255, 255, 255, 40), msg_surface.get_rect(), border_radius=10)
        
        # Texte du message
        text = self.menu_font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(msg_rect.width // 2, msg_rect.height // 2))
        
        # Assemblage
        msg_surface.blit(text, text_rect)
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(msg_surface, msg_rect)
        pygame.display.flip()
        
        pygame.time.wait(1500)