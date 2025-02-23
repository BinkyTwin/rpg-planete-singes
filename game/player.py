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
        self.tile_size = 32  # Taille des tuiles en pixels
        
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
        self.max_hp = 100  # Points de vie maximum
        self.hp = self.max_hp  # Points de vie actuels

        # points d'expérience du joueur
        self.xp = 0

        # Ajout de l'inventaire
        self.inventory = Inventory()

        # Rectangle de collision
        self.rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)  # Rectangle de 32x32 pixels pour le joueur
        
        # Image par défaut (un carré coloré en attendant les sprites)
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))  # Rouge pour le moment

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

    def update(self, keys, collision_manager=None, dt=1/60):
        """Met à jour l'état du joueur"""
        # Gestion du mouvement
        dx = dy = 0
        
        # Touches directionnelles
        if keys.get(pygame.K_LEFT) or keys.get(pygame.K_q):
            dx = -1
        if keys.get(pygame.K_RIGHT) or keys.get(pygame.K_d):
            dx = 1
        if keys.get(pygame.K_UP) or keys.get(pygame.K_z):
            dy = -1
        if keys.get(pygame.K_DOWN) or keys.get(pygame.K_s):
            dy = 1
            
        # Normaliser le mouvement diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071
            
        # Calculer la nouvelle position
        new_x = self.x + dx * self.speed * self.tile_size
        new_y = self.y + dy * self.speed * self.tile_size
        
        # Vérifier les collisions si un gestionnaire est fourni
        if collision_manager:
            current_pos = (self.x / self.tile_size, self.y / self.tile_size)
            new_pos = (new_x / self.tile_size, new_y / self.tile_size)
            
            if collision_manager.can_move_to(current_pos, new_pos):
                self.move(dx, dy, collision_manager)
        else:
            self.move(dx, dy, None)
            
        # Mise à jour de l'animation
        if self.is_moving:
            self.animation_frame += self.animation_speed * dt
            if self.animation_frame >= len(self.sprites[self.direction]):
                self.animation_frame = 0

    def get_current_sprite(self):
        """Retourne le sprite actuel en fonction de la direction et de l'animation"""
        frame = int(self.animation_frame) % len(self.sprites[self.direction])
        return self.sprites[self.direction][frame]

    def move(self, dx, dy, tiled_map):
        """Déplace le joueur en prenant en compte les collisions"""
        # Sauvegarder la position actuelle
        original_x = self.x
        original_y = self.y
        original_rect = self.rect.copy()
        
        # Calculer la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Tester le mouvement complet
        self.x = new_x
        self.y = new_y
        self.rect.x = int(self.x * self.tile_size)
        self.rect.y = int(self.y * self.tile_size)
        
        # Vérifier les collisions
        if tiled_map and self._check_collision(tiled_map):
            # Annuler le mouvement complet
            self.x = original_x
            self.y = original_y
            self.rect.x = original_rect.x
            self.rect.y = original_rect.y
            
        if dx != 0 or dy != 0:
            self.is_moving = True
            
            # Mise à jour de la direction
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"
                
            # Mettre à jour la position du rectangle
            self.rect.centerx = self.x * self.tile_size
            self.rect.centery = self.y * self.tile_size
        else:
            self.is_moving = False
            self.animation_frame = 0

    def _check_collision(self, tiled_map):
        """Vérifie s'il y a collision avec les murs"""
        # Obtenir les coordonnées en tuiles
        tile_x = int(self.rect.centerx / tiled_map.tile_size)
        tile_y = int(self.rect.centery / tiled_map.tile_size)
        
        # Vérifier les tuiles adjacentes
        for y in range(tile_y - 1, tile_y + 2):
            for x in range(tile_x - 1, tile_x + 2):
                if tiled_map.is_wall(x, y):
                    wall_rect = pygame.Rect(x * tiled_map.tile_size,
                                         y * tiled_map.tile_size,
                                         tiled_map.tile_size,
                                         tiled_map.tile_size)
                    if self.rect.colliderect(wall_rect):
                        return True
        return False

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
