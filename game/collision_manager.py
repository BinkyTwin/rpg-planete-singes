class CollisionManager:
    def __init__(self, tiled_map, tile_size):
        """
        Initialise le gestionnaire de collisions
        
        Args:
            tiled_map (TiledMap): Objet TiledMap contenant les données de la map
            tile_size (int): Taille d'une tuile en pixels
        """
        self.tiled_map = tiled_map
        self.tile_size = tile_size
        self.map_width = tiled_map.tmx_data.width
        self.map_height = tiled_map.tmx_data.height

    def is_collision(self, grid_x, grid_y):
        """
        Vérifie s'il y a une collision à la position donnée
        
        Args:
            grid_x (int): Position X en coordonnées grille
            grid_y (int): Position Y en coordonnées grille
            
        Returns:
            bool: True s'il y a collision, False sinon
        """
        # Vérifier les limites de la map
        if not self._is_within_bounds(grid_x, grid_y):
            return True
            
        # Vérifier s'il y a un mur
        collision_layer = self.tiled_map.get_layer_by_name('collisions')
        if collision_layer:
            # Convertir les coordonnées négatives en positives
            map_x = grid_x % self.map_width
            map_y = grid_y % self.map_height
            
            # Vérifier s'il y a une tuile de collision à cette position
            for x, y, gid in collision_layer:
                if x == map_x and y == map_y and gid:
                    return True
        return False

    def can_move_to(self, current_pos, new_pos):
        """
        Vérifie si un mouvement est valide
        
        Args:
            current_pos (tuple): Position actuelle (x, y)
            new_pos (tuple): Nouvelle position désirée (x, y)
            
        Returns:
            bool: True si le mouvement est valide, False sinon
        """
        new_x, new_y = new_pos
        
        # Vérifier si la nouvelle position est dans les limites
        if not self._is_within_bounds(new_x, new_y):
            return False
            
        # Vérifier s'il y a une collision à la nouvelle position
        if self.is_collision(new_x, new_y):
            return False
            
        return True

    def get_valid_move(self, current_pos, desired_pos):
        """
        Retourne une position valide la plus proche de la position désirée
        
        Args:
            current_pos (tuple): Position actuelle (x, y)
            desired_pos (tuple): Position désirée (x, y)
            
        Returns:
            tuple: Position valide (x, y)
        """
        if self.can_move_to(current_pos, desired_pos):
            return desired_pos
        return current_pos

    def is_on_tree(self, grid_x, grid_y):
        """
        Vérifie si la position est sur un arbre
        
        Args:
            grid_x (int): Position X en coordonnées grille
            grid_y (int): Position Y en coordonnées grille
            
        Returns:
            bool: True si sur un arbre, False sinon
        """
        if not self._is_within_bounds(grid_x, grid_y):
            return False
            
        tree_layer = self.tiled_map.get_layer_by_name('three')
        if tree_layer:
            # Convertir les coordonnées négatives en positives
            map_x = grid_x % self.map_width
            map_y = grid_y % self.map_height
            
            # Vérifier s'il y a un arbre à cette position
            for x, y, gid in tree_layer:
                if x == map_x and y == map_y and gid:
                    return True
        return False

    def is_on_ground(self, grid_x, grid_y):
        """
        Vérifie si la position est sur le sol (pas de collision ni d'arbre)
        
        Args:
            grid_x (int): Position X en coordonnées grille
            grid_y (int): Position Y en coordonnées grille
            
        Returns:
            bool: True si sur le sol, False sinon
        """
        if not self._is_within_bounds(grid_x, grid_y):
            return False
            
        # Une position est sur le sol si elle n'a ni collision ni arbre
        return (not self.is_collision(grid_x, grid_y) and 
                not self.is_on_tree(grid_x, grid_y))

    def _is_within_bounds(self, grid_x, grid_y):
        """
        Vérifie si une position est dans les limites de la map
        
        Args:
            grid_x (int): Position X en coordonnées grille
            grid_y (int): Position Y en coordonnées grille
            
        Returns:
            bool: True si dans les limites, False sinon
        """
        # Convertir les coordonnées négatives en positives
        map_x = grid_x % self.map_width
        map_y = grid_y % self.map_height
        
        return (0 <= map_x < self.map_width and 
                0 <= map_y < self.map_height)
