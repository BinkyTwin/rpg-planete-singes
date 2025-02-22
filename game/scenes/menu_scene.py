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
        self.base_menu_size = 32
        self.update_fonts()
        
        # Options du menu
        self.menu_options = ["Nouvelle Partie", "Charger Partie", "Options", "Quitter"]
        self.selected_option = 0
        self.hovered_option = -1  # Pour le survol de la souris
        
        # Couleurs
        self.text_color = (255, 255, 0)  # Jaune pour le texte
        self.selected_color = (255, 255, 255)  # Blanc pour la sélection
        
        # Image de fond
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        wallpaper_path = os.path.join(self.base_path, "assets", "wallpaper.png")
        self.background = pygame.image.load(wallpaper_path)
        
        # Alphas pour les animations
        self.menu_alphas = [255] * len(self.menu_options)  # Toujours visible

    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            title_size = self.display_manager.get_scaled_font_size(self.base_title_size)
            menu_size = self.display_manager.get_scaled_font_size(self.base_menu_size)
        else:
            title_size = self.base_title_size
            menu_size = self.base_menu_size
            
        self.title_font = pygame.font.SysFont("arial", title_size)
        self.menu_font = pygame.font.SysFont("arial", menu_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Gérer le survol
            mouse_pos = pygame.mouse.get_pos()
            menu_start_y = self.screen.get_height() // 2
            spacing = self.menu_font.get_height() * 1.5
            
            self.hovered_option = -1
            for i, option in enumerate(self.menu_options):
                text_rect = pygame.Rect(
                    self.screen.get_width() // 2 - 100,  # Rectangle plus large que le texte
                    menu_start_y + i * spacing - 20,     # Un peu plus haut que le texte
                    200,                                 # Largeur fixe
                    40                                   # Hauteur fixe
                )
                if text_rect.collidepoint(mouse_pos):
                    self.hovered_option = i
                    break
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered_option != -1:  # Clic gauche
                self.selected_option = self.hovered_option
                return self._handle_option_selection()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                return self._handle_option_selection()
                
        # Si la fenêtre est redimensionnée, mettre à jour les polices
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            
        return None

    def _handle_option_selection(self):
        """Gère la sélection d'une option du menu"""
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

    def show_message(self, message):
        """Affiche un message temporaire au centre de l'écran"""
        # Créer une surface semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Noir semi-transparent
        
        # Rendre le message
        text = self.menu_font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Afficher le tout
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        
        # Attendre un peu
        pygame.time.wait(1500)

    def update(self):
        # Les rectangles sont toujours visibles, pas besoin de mettre à jour les alphas
        pass

    def handle_selection(self):
        pass

    def render(self, screen):
        # Redimensionner l'image de fond pour qu'elle remplisse l'écran
        scaled_bg = pygame.transform.scale(self.background, screen.get_size())
        screen.blit(scaled_bg, (0, 0))
        
        # Création d'une surface semi-transparente pour améliorer la lisibilité du texte
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 128 pour semi-transparent
        screen.blit(overlay, (0, 0))
        
        # Titre du jeu
        title_text = self.title_font.render("La Planète des Singes", True, self.text_color)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(title_text, title_rect)
        
        # Options du menu
        menu_start_y = screen.get_height() // 2
        spacing = self.menu_font.get_height() * 1.5
        
        for i, option in enumerate(self.menu_options):
            # Créer le rectangle
            text_rect = pygame.Rect(
                screen.get_width() // 2 - 100,
                menu_start_y + i * spacing - 20,
                200,
                40
            )
            
            # Créer une surface semi-transparente pour le rectangle
            button_surface = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
            
            # Le rectangle est toujours visible avec une opacité de base
            if i == self.selected_option:
                # Rectangle blanc semi-transparent pour la sélection
                pygame.draw.rect(button_surface, (255, 255, 255, 80), button_surface.get_rect(), border_radius=5)
            else:
                # Rectangle blanc très légèrement visible pour les autres options
                pygame.draw.rect(button_surface, (255, 255, 255, 40), button_surface.get_rect(), border_radius=5)
            
            screen.blit(button_surface, text_rect)
            
            # Dessiner le texte
            color = self.selected_color if i == self.selected_option else self.text_color
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, menu_start_y + i * spacing))
            screen.blit(text, text_rect)