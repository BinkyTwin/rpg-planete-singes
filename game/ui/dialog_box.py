import pygame

class DialogBox:
    def __init__(self, screen, message, font_size=24, stats_text=None):
        self.screen = screen
        self.message = message
        self.stats_text = stats_text
        self.main_font = pygame.font.SysFont("arial", font_size)
        self.stats_font = pygame.font.SysFont("arial", int(font_size * 0.8))  # Police plus petite pour les stats
        self.padding = 20
        self.button_padding = 10
        self.active = True
        self.result = None
        
        # Couleurs
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.stats_color = (200, 200, 200)  # Couleur légèrement différente pour les stats
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.button_text_color = (255, 255, 255)
        
        # Création des surfaces de texte
        self.text_surface = self.main_font.render(message, True, self.text_color)
        self.stats_surface = self.stats_font.render(stats_text, True, self.stats_color) if stats_text else None
        self.yes_text = self.main_font.render("Oui", True, self.button_text_color)
        self.no_text = self.main_font.render("Non", True, self.button_text_color)
        
        # Calcul des dimensions
        text_width = max(self.text_surface.get_width(), 
                        self.stats_surface.get_width() if self.stats_surface else 0)
        self.width = max(300, text_width + self.padding * 2)
        
        # Hauteur totale incluant le texte principal, les stats et les boutons
        self.height = (self.text_surface.get_height() + 
                      (self.stats_surface.get_height() + 10 if self.stats_surface else 0) +
                      self.padding * 3 + self.yes_text.get_height())
        
        # Position de la boîte
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        
        # Création des rectangles pour les boutons
        button_y = self.y + self.height - self.yes_text.get_height() - self.padding
        button_width = 80
        gap = 20
        
        self.yes_button = pygame.Rect(
            self.x + (self.width - 2 * button_width - gap) // 2,
            button_y,
            button_width,
            self.yes_text.get_height() + self.button_padding
        )
        
        self.no_button = pygame.Rect(
            self.yes_button.right + gap,
            button_y,
            button_width,
            self.no_text.get_height() + self.button_padding
        )

    def handle_event(self, event):
        """Gère les événements de la boîte de dialogue"""
        if not self.active:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.yes_button.collidepoint(mouse_pos):
                self.result = True
                self.active = False
                return True
            elif self.no_button.collidepoint(mouse_pos):
                self.result = False
                self.active = False
                return True
        return False

    def render(self):
        if not self.active:
            return
            
        # Dessiner le fond semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner la boîte de dialogue
        pygame.draw.rect(self.screen, self.bg_color, (self.x, self.y, self.width, self.height))
        
        # Dessiner le texte principal
        text_x = self.x + (self.width - self.text_surface.get_width()) // 2
        text_y = self.y + self.padding
        self.screen.blit(self.text_surface, (text_x, text_y))
        
        # Dessiner les stats si présentes
        if self.stats_surface:
            stats_x = self.x + (self.width - self.stats_surface.get_width()) // 2
            stats_y = text_y + self.text_surface.get_height() + 10
            self.screen.blit(self.stats_surface, (stats_x, stats_y))
        
        # Dessiner les boutons avec bordures
        mouse_pos = pygame.mouse.get_pos()
        
        # Bouton Oui
        yes_color = self.button_hover_color if self.yes_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, yes_color, self.yes_button)
        pygame.draw.rect(self.screen, self.text_color, self.yes_button, 1)  # Bordure
        yes_text_x = self.yes_button.x + (self.yes_button.width - self.yes_text.get_width()) // 2
        yes_text_y = self.yes_button.y + (self.yes_button.height - self.yes_text.get_height()) // 2
        self.screen.blit(self.yes_text, (yes_text_x, yes_text_y))
        
        # Bouton Non
        no_color = self.button_hover_color if self.no_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, no_color, self.no_button)
        pygame.draw.rect(self.screen, self.text_color, self.no_button, 1)  # Bordure
        no_text_x = self.no_button.x + (self.no_button.width - self.no_text.get_width()) // 2
        no_text_y = self.no_button.y + (self.no_button.height - self.no_text.get_height()) // 2
        self.screen.blit(self.no_text, (no_text_x, no_text_y))
