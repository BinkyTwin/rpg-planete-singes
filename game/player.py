import os 
import pygame
from .factions import FactionName, FACTIONS
from .inventory import Inventory

class Player:
    RACES = {
        'chimpanze': {
            'agilite': 8,
            'force': 6,
            'intelligence': 7,
            'furtivite': 6,
            'diplomatie': 8
        },
        'gorille': {
            'agilite': 5,
            'force': 9,
            'intelligence': 6,
            'furtivite': 4,
            'diplomatie': 5
        },
        'orang outan': {
            'agilite': 6,
            'force': 7,
            'intelligence': 9,
            'furtivite': 5,
            'diplomatie': 7
        },
        'bonobo': {
            'agilite': 7,
            'force': 5,
            'intelligence': 7,
            'furtivite': 9,
            'diplomatie': 9
        },
        'singe hurleur': {
            'agilite': 8,
            'force': 6,
            'intelligence': 6,
            'furtivite': 7,
            'diplomatie': 6
        }
    }
    FACTIONS = {
        "Les Veilleurs des Montagnes",
        "Le Cercle des Ombres",
        "Le Clan des Brumes",
        "Les Enfants de la Forêt"
    }

    def __init__(self, name, x, y, race, faction: FactionName):
        # nom du joueur
        self.name = name

        # position du joueur
        self.x = x
        self.y = y
        
        # Vitesse et animation
        self.speed = 1  # Vitesse de déplacement en tiles
        self.direction = "down"  # Direction actuelle (down, up, left, right)
        self.animation_frame = 0  # Frame actuelle de l'animation
        self.animation_speed = 0.2  # Vitesse de l'animation
        self.is_moving = False
        self.sprite_size = 64  # Taille des sprites en pixels
        
        # Chargement des sprites
        self.sprites = self._load_character_sprites(race)
        
        # race du joueur
        if race not in self.RACES:
            raise ValueError(f"Race invalide. Choisissez parmi : {', '.join(self.RACES.keys())}")
        self.race = race
        self.race_stats = self.RACES[race].copy() # stats de la race

        # Faction du joueur
        self.faction = faction
        self.faction_obj = FACTIONS[faction]

        # points de vie du joueur
        self.hp = 100

        # points d'expérience du joueur
        self.xp = 0

        # Ajout de l'inventaire
        self.inventory = Inventory()

    def _load_character_sprites(self, race):
        """Charge les sprites du personnage en fonction de sa race"""
        sprites = {}
        
        # Mapping des noms de fichiers pour chaque race
        race_files = {
            'chimpanze': 'chimpanze.png',
            'gorille': 'gorille.png',
            'orang outan': 'orang outan.png',
            'bonobo': 'bonobo.png',
            'singe hurleur': 'singe hurleur.png'
        }
        
        # Vérifier que la race est valide et a un fichier correspondant
        if race not in race_files:
            raise ValueError(f"Race invalide ou sprite non trouvé pour {race}")
            
        # Obtenir le chemin absolu du projet
        current_file = os.path.abspath(__file__)  # Chemin du fichier player.py
        game_dir = os.path.dirname(current_file)   # Dossier game/
        project_dir = os.path.dirname(game_dir)    # Dossier racine du projet
            
        # Charger le sprite de base
        sprite_path = os.path.join(project_dir, "assets", "character", race_files[race])
        print(f"Tentative de chargement du sprite : {sprite_path}")
        print(f"Le fichier existe ? {os.path.exists(sprite_path)}")
        
        if not os.path.exists(sprite_path):
            raise ValueError(f"Sprite non trouvé : {sprite_path}")
            
        # Charger l'image de base
        base_sprite = pygame.image.load(sprite_path).convert_alpha()
        sprite_width = base_sprite.get_width() // 4  # 4 frames par direction
        sprite_height = base_sprite.get_height() // 4  # 4 directions
        
        # Découper le spritesheet pour chaque direction et frame
        directions = ["down", "left", "right", "up"]
        for dir_idx, direction in enumerate(directions):
            sprites[direction] = []
            for frame in range(4):
                # Extraire la frame du spritesheet
                frame_surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                frame_surface.blit(base_sprite, 
                                 (0, 0), 
                                 (frame * sprite_width, dir_idx * sprite_height, 
                                  sprite_width, sprite_height))
                sprites[direction].append(frame_surface)
        
        return sprites

    def update(self, dt):
        """Met à jour l'état du joueur"""
        if self.is_moving:
            self.animation_frame += self.animation_speed * dt
            if self.animation_frame >= len(self.sprites[self.direction]):
                self.animation_frame = 0
                
    def get_current_sprite(self):
        """Retourne le sprite actuel en fonction de la direction et de l'animation"""
        frame = int(self.animation_frame) % len(self.sprites[self.direction])
        return self.sprites[self.direction][frame]

    def move(self, dx, dy):
        """Déplace le joueur avec la gestion de la direction et de l'animation"""
        if dx != 0 or dy != 0:
            self.is_moving = True
            
            # Mise à jour de la direction
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"
                
            # Mise à jour de la position avec la vitesse
            self.x += dx * self.speed
            self.y += dy * self.speed
        else:
            self.is_moving = False
            self.animation_frame = 0

    def print_player(self):
        print(f"Nom : {self.name}")
        print(f"Position : ({self.x}, {self.y})")
        print(f"Race : {self.race}")
        print(f"Points de vie : {self.hp}")
        print(f"Expérience : {self.xp}")
        print("\nStatistiques de race :")
        for stat, value in self.race_stats.items():
            print(f"- {stat.capitalize()} : {value}")
        print(f"Slots d'inventaire : {len(self.inventory.get_items())}/{self.inventory.max_slots}")

    def get_relation_with(self, other_faction: FactionName):
        """Retourne la relation entre la faction du joueur et une autre faction"""
        return self.faction_obj.get_relation(other_faction)
