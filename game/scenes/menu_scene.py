import pygame
import sys
from .base_scene import BaseScene

class MenuScene(BaseScene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        # Utilisation d'une police plus élégante
        try:
            self.font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 36)
            self.title_font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 48)
        except:
            # Fallback sur une police système si le fichier n'est pas trouvé
            self.font = pygame.font.SysFont("arial", 36)
            self.title_font = pygame.font.SysFont("arial", 48)

        self.menu_items = [
            "Nouvelle Partie",
            "Quitter"
        ]
        self.selected_item = 0
        # Chargement et redimensionnement du fond d'écran
        self.background = pygame.image.load("assets/wallpaper.png")
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        
        # Animation des boutons
        self.button_hover_alpha = [0] * len(self.menu_items)
        self.button_rects = []
        center_x = self.screen.get_width() // 2
        for i in range(len(self.menu_items)):
            text = self.font.render(self.menu_items[i], True, (255, 255, 255))
            rect = text.get_rect(center=(center_x, 250 + i * 50))
            rect.inflate_ip(40, 20)  # Rectangle plus grand pour un meilleur effet
            self.button_rects.append(rect)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                return self.handle_selection()
        
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    self.selected_item = i
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_item = i
                        return self.handle_selection()
    
    def update(self):
        # Animation fluide des boutons
        for i in range(len(self.menu_items)):
            if i == self.selected_item:
                self.button_hover_alpha[i] = min(self.button_hover_alpha[i] + 20, 255)
            else:
                self.button_hover_alpha[i] = max(self.button_hover_alpha[i] - 20, 0)
                    
    def handle_selection(self):
        if self.selected_item == 0:
            return 'character_creation'
        elif self.selected_item == 1:
            pygame.quit()
            sys.exit()
                    
    def render(self):
        # Affichage du fond d'écran
        self.screen.blit(self.background, (0, 0))
        
        # Création d'une surface semi-transparente pour améliorer la lisibilité du texte
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 128 pour semi-transparent
        self.screen.blit(overlay, (0, 0))
        
        # Affichage du titre
        title = self.title_font.render("La Planète des Singes - RPG", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Affichage des options du menu
        for i, (item, rect) in enumerate(zip(self.menu_items, self.button_rects)):
            # Dessiner le fond du bouton avec animation
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, (255, 255, 255, self.button_hover_alpha[i] // 3), 
                           button_surface.get_rect(), border_radius=10)
            self.screen.blit(button_surface, rect)
            
            # Dessiner le texte
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect) 