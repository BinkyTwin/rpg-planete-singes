class CoordinateSystem:
    def __init__(self, screen_width, screen_height, tile_size):
        """
        Initialise le système de coordonnées
        
        Args:
            screen_width (int): Largeur de l'écran en pixels
            screen_height (int): Hauteur de l'écran en pixels
            tile_size (int): Taille d'une tuile en pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.screen_center_x = screen_width // 2
        self.screen_center_y = screen_height // 2

    def screen_to_grid(self, screen_x, screen_y):
        """
        Convertit les coordonnées écran en coordonnées grille
        
        Args:
            screen_x (int): Position X en pixels sur l'écran
            screen_y (int): Position Y en pixels sur l'écran
            
        Returns:
            tuple: (grid_x, grid_y) Position en coordonnées grille
        """
        # Les coordonnées sont déjà en unités de grille * tile_size
        grid_x = screen_x // self.tile_size
        grid_y = screen_y // self.tile_size
        
        return grid_x, grid_y

    def grid_to_screen(self, grid_x, grid_y):
        """
        Convertit les coordonnées grille en coordonnées écran
        
        Args:
            grid_x (int): Position X en coordonnées grille
            grid_y (int): Position Y en coordonnées grille
            
        Returns:
            tuple: (screen_x, screen_y) Position en pixels sur l'écran
        """
        # Calculer la position en pixels par rapport au centre
        screen_x = self.screen_center_x + (grid_x * self.tile_size)
        screen_y = self.screen_center_y + (grid_y * self.tile_size)
        
        return screen_x, screen_y

    def get_camera_offset(self, player_pos):
        """
        Calcule le décalage de la caméra pour centrer sur le joueur
        
        Args:
            player_pos (tuple): Position du joueur en coordonnées grille (x, y)
            
        Returns:
            tuple: (offset_x, offset_y) Décalage en pixels
        """
        player_x, player_y = player_pos
        
        # Convertir la position du joueur en pixels et calculer le décalage
        offset_x = self.screen_center_x + (player_x * self.tile_size)
        offset_y = self.screen_center_y + (player_y * self.tile_size)
        
        return offset_x, offset_y
