import pygame
from game.pnj import PNJ
from game.items import ITEMS

class PNJ2(PNJ):
    """
    Classe PNJ2 qui hérite de PNJ.
    Cette classe représente un PNJ spécifique (gorille) sans système de dialogue.
    """
    
    def __init__(self, position):
        super().__init__(position)
        # Modification du sprite pour utiliser le gorille
        self.sprite_name = 'gorille.png'
        # Ajout de l'épée rouillée comme item décoratif
        self.held_item = ITEMS["épée_rouillée"]
        # Rechargement des sprites avec le nouveau sprite_name
        self.sprites = self._load_sprite_sheet()
        # Désactivation du système de dialogue
        self.dialogue_system = None
        self.is_in_dialogue = False
        # S'assurer que la direction est initialisée
        self.current_direction = "down"
        print(f"PNJ2 initialisé à la position ({self.tile_x}, {self.tile_y})")
        # S'assurer que TILE_SIZE est défini
        self.TILE_SIZE = 32

    def update_direction(self, player):
        """Met à jour la direction du PNJ pour qu'il regarde vers le joueur"""
        # Les coordonnées sont déjà en tuiles, pas besoin de conversion
        dx = player.x - self.tile_x
        dy = player.y - self.tile_y
        
        # Mettre à jour la direction en fonction de la plus grande différence
        if abs(dx) > abs(dy):
            self.current_direction = "right" if dx > 0 else "left"
        else:
            self.current_direction = "down" if dy > 0 else "up"

    def can_trigger_dialogue(self, player):
        """
        Surcharge pour désactiver le dialogue tout en mettant à jour la direction du PNJ
        pour qu'il regarde toujours vers le joueur.
        """
        # Debug: afficher les positions
        print(f"PNJ2 position: ({self.tile_x}, {self.tile_y})")
        print(f"Player position: ({player.x}, {player.y})")
        
        # Calculer les différences en tuiles
        dx = player.x - self.tile_x
        dy = player.y - self.tile_y
        
        # Debug: afficher les différences
        print(f"Différences - dx: {dx}, dy: {dy}")
        
        # Mettre à jour la direction en fonction de la plus grande différence
        old_direction = self.current_direction
        if abs(dx) > abs(dy):
            self.current_direction = "right" if dx > 0 else "left"
        else:
            self.current_direction = "down" if dy > 0 else "up"
            
        # Debug: afficher le changement de direction
        if old_direction != self.current_direction:
            print(f"PNJ2 change de direction: {old_direction} -> {self.current_direction}")
        
        return False

    def render(self, screen, camera_x=0, camera_y=0):
        """Surcharge du rendu pour ajouter du debug"""
        if not self.is_visible:
            return

        # Calculer la position à l'écran
        screen_x = self.tile_x * self.TILE_SIZE - camera_x
        screen_y = self.tile_y * self.TILE_SIZE - camera_y
        
        # Debug: afficher la position de rendu
        print(f"PNJ2 rendu à la position écran: ({screen_x}, {screen_y})")
        print(f"Direction actuelle: {self.current_direction}")
        
        screen_rect = screen.get_rect()
        sprite_rect = pygame.Rect(screen_x, screen_y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        
        if screen_rect.colliderect(sprite_rect):
            current_sprite = self.sprites[self.current_direction][0]
            screen.blit(current_sprite, (screen_x, screen_y))
            print("PNJ2 affiché avec succès")

    def start_dialogue(self):
        """Surcharge pour désactiver le dialogue"""
        return None

    def next_message(self):
        """Surcharge pour désactiver le dialogue"""
        return None

    def is_dialogue_finished(self):
        """Surcharge pour désactiver le dialogue"""
        return True 