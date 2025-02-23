import pygame
import os

class HealthDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 24)
        self.margin = 10
        
        # Charger l'image du cœur
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        heart_path = os.path.join(base_path, "assets", "images_ui", "heart.png")
        self.heart_image = pygame.image.load(heart_path)
        
        # Redimensionner l'image du cœur (30x30 pixels)
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        
    def render(self, player_hp):
        """Affiche le niveau de vie du joueur avec une icône de cœur"""
        if not hasattr(self, 'heart_image'):
            return
            
        # Préparer le texte HP
        hp_text = str(player_hp)
        text_surface = self.font.render(hp_text, True, (255, 255, 255))
        
        # Calculer la largeur totale (cœur + espace + texte)
        total_width = self.heart_image.get_width() + 5 + text_surface.get_width()
        
        # Position en bas à droite
        heart_x = self.screen.get_width() - total_width - self.margin
        heart_y = self.screen.get_height() - self.heart_image.get_height() - self.margin
        
        # Afficher l'icône de cœur
        self.screen.blit(self.heart_image, (heart_x, heart_y))
        
        # Position du texte (à droite de l'icône)
        text_x = heart_x + self.heart_image.get_width() + 5
        text_y = heart_y + (self.heart_image.get_height() - text_surface.get_height()) // 2
        
        self.screen.blit(text_surface, (text_x, text_y))
