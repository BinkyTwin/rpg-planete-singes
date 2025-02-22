import pygame
from game.factions import Faction
import os
import math
from game.dialogue_system import DialogueSystem

class PNJ:
    # Distance en pixels à laquelle le dialogue peut être déclenché
    DIALOGUE_TRIGGER_DISTANCE = 64  # 2 tuiles (32 * 2)
    TILE_SIZE = 32  # Taille d'une tuile en pixels
    SPRITE_SIZE = 64  # Taille d'un sprite (modifié à 64 pour correspondre à la taille réelle du sprite)

    def __init__(self, position):
        self.tile_x, self.tile_y = position
        self.faction = None
        self.sprite_name = 'orang outan.png'  # Correction: ajout de l'espace au lieu du underscore
        self.sprites = self._load_sprite_sheet()
        self.current_direction = "down"
        self.animation_frame = 0
        self.dialogue_system = DialogueSystem()
        self.is_visible = True
        self.map = None
        self.is_in_dialogue = False  # Nouveau: pour suivre l'état du dialogue
        
    def _load_sprite_sheet(self):
        """Charge et découpe le sprite sheet en frames d'animation"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sprite_path = os.path.join(base_path, 'assets', 'character', self.sprite_name)
        
        # Debug: afficher les informations sur le fichier
        print(f"Tentative de chargement du sprite depuis: {sprite_path}")
        print(f"Le fichier existe: {os.path.exists(sprite_path)}")
        if os.path.exists(sprite_path):
            print(f"Taille du fichier: {os.path.getsize(sprite_path)} bytes")
        
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            sprites = {
                "down": [],
                "left": [],
                "right": [],
                "up": []
            }
            
            # Dimensions correctes pour le découpage
            frame_width = sprite_sheet.get_width() // 4
            frame_height = sprite_sheet.get_height() // 4
            
            for row, direction in enumerate(["down", "left", "right", "up"]):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                # Ne prendre que la première frame de chaque direction pour éviter l'animation
                frame.blit(sprite_sheet, (0, 0), 
                         (0, row * frame_height, frame_width, frame_height))
                # Utiliser la même frame 4 fois pour maintenir la compatibilité
                sprites[direction] = [frame] * 4
            
            return sprites
        except pygame.error as e:
            print(f"Erreur lors du chargement du sprite {self.sprite_name}: {e}")
            fallback = pygame.Surface((self.SPRITE_SIZE, self.SPRITE_SIZE), pygame.SRCALPHA)
            fallback.fill((255, 0, 255, 128))
            return {"down": [fallback] * 4, "left": [fallback] * 4, "right": [fallback] * 4, "up": [fallback] * 4}

    def sync_faction(self, player):
        """Synchronise la faction du PNJ avec celle du joueur"""
        self.faction = player.faction

    def can_trigger_dialogue(self, player):
        """Vérifie si le joueur est assez proche pour déclencher le dialogue"""
        pnj_x = self.tile_x * self.TILE_SIZE
        pnj_y = self.tile_y * self.TILE_SIZE
        
        distance = math.sqrt((player.x * self.TILE_SIZE - pnj_x) ** 2 + 
                           (player.y * self.TILE_SIZE - pnj_y) ** 2)
        
        dx = player.x * self.TILE_SIZE - pnj_x
        dy = player.y * self.TILE_SIZE - pnj_y
        
        if abs(dx) > abs(dy):
            self.current_direction = "right" if dx > 0 else "left"
        else:
            self.current_direction = "down" if dy > 0 else "up"
            
        return distance <= self.DIALOGUE_TRIGGER_DISTANCE

    def start_dialogue(self):
        """Démarre le dialogue avec le PNJ"""
        self.is_in_dialogue = True
        return self.dialogue_system.start_dialogue()

    def next_message(self):
        """Passe au message suivant du dialogue"""
        message = self.dialogue_system.next_message()
        if message is None and self.dialogue_system.is_dialogue_finished():
            self.is_in_dialogue = False
            self.remove_from_map()
            if self.map:
                self.map.remove_pnj()
        return message

    def is_dialogue_finished(self):
        """Vérifie si le dialogue est terminé"""
        return self.dialogue_system.is_dialogue_finished()

    def get_pixel_position(self):
        """Retourne la position en pixels du PNJ"""
        return (self.tile_x * self.TILE_SIZE, self.tile_y * self.TILE_SIZE)

    def render(self, screen, camera_x=0, camera_y=0):
        """Rend le PNJ sur l'écran en tenant compte de la caméra"""
        if not self.is_visible:
            return

        screen_x = self.tile_x * self.TILE_SIZE - camera_x
        screen_y = self.tile_y * self.TILE_SIZE - camera_y
        
        screen_rect = screen.get_rect()
        sprite_rect = pygame.Rect(screen_x, screen_y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        
        if screen_rect.colliderect(sprite_rect):
            # Toujours utiliser la frame 0 pour un sprite statique
            current_sprite = self.sprites[self.current_direction][0]
            screen.blit(current_sprite, (screen_x, screen_y))

    def remove_from_map(self):
        """Retire le PNJ de la map"""
        self.is_visible = False