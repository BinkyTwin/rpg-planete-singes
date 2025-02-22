import pygame

class DisplayManager:
    def __init__(self):
        """Initialise le gestionnaire d'affichage"""
        # Obtenir les informations sur l'écran
        self.screen_info = pygame.display.Info()
        self.desktop_width = self.screen_info.current_w
        self.desktop_height = self.screen_info.current_h
        
        # Dimensions initiales de la fenêtre (4:3)
        self.window_width = 800
        self.window_height = 600
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.is_fullscreen = False
        
        # Échelle et position
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
    def toggle_fullscreen(self):
        """Basculer entre le mode plein écran et fenêtré"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.desktop_width, self.desktop_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        return self.screen

    def handle_resize(self, width, height):
        """Gérer le redimensionnement de la fenêtre"""
        if not self.is_fullscreen:
            self.window_width = width
            self.window_height = height
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        return self.screen

    def update_scale(self, screen_width, screen_height, map_width, map_height):
        """Mettre à jour l'échelle en fonction des dimensions de la carte"""
        # Calculer l'échelle pour remplir l'écran
        self.scale_x = screen_width / map_width
        self.scale_y = screen_height / map_height
        
        # Calculer les offsets (pas besoin de centrer car on remplit l'écran)
        self.offset_x = 0
        self.offset_y = 0

    def get_scaled_pos(self, pos):
        """Convertir une position en coordonnées d'écran"""
        x = pos[0] * self.scale_x + self.offset_x
        y = pos[1] * self.scale_y + self.offset_y
        return (x, y)

    def unscale_pos(self, screen_pos):
        """Convertir une position d'écran en coordonnées de carte"""
        x = (screen_pos[0] - self.offset_x) / self.scale_x
        y = (screen_pos[1] - self.offset_y) / self.scale_y
        return (x, y)

    def get_scaled_size(self, size):
        """Obtenir une taille mise à l'échelle"""
        return (size[0] * self.scale_x, size[1] * self.scale_y)

    def get_scaled_font_size(self, base_size):
        """Obtenir une taille de police mise à l'échelle"""
        return int(base_size * self.scale_x)
