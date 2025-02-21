import pygame
import sys
import os
from .base_scene import BaseScene
from ..player import Player
from ..factions import FactionName, FACTIONS

class CharacterCreationScene(BaseScene):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        # Utilisation d'une police système
        self.font = pygame.font.SysFont("arial", 36)
        self.title_font = pygame.font.SysFont("arial", 48)
        self.small_font = pygame.font.SysFont("arial", 24)
        
        # Obtenir le chemin de base du projet
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Configuration de base
        self.name = ""
        self.selected_race = 0
        self.selected_faction = 0
        self.creation_step = 0
        self.is_name_field_active = False
        
        # Chargement du fond d'écran
        wallpaper_path = os.path.join(self.base_path, "assets", "wallpaper.png")
        self.background = pygame.image.load(wallpaper_path)
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        
        # Configuration des listes et rectangles
        self.races = list(Player.RACES.keys())
        self.factions = list(FactionName)
        
        # Création des boutons
        self.back_button = pygame.Rect(20, 20, 100, 40)
        self.confirm_button = pygame.Rect(
            screen.get_width() // 2 - 75,
            screen.get_height() - 80,
            150, 50
        )
        
        # Alphas pour les animations
        self.back_button_alpha = 0
        self.confirm_button_alpha = 0
        self.race_alphas = [0] * len(self.races)
        self.faction_alphas = [0] * len(self.factions)
        self.hover_transition_speed = 20
        
        # Zone de saisie du nom
        name_width = 300
        name_height = 50
        self.name_input_rect = pygame.Rect(
            (screen.get_width() // 2) - (name_width // 2),
            (screen.get_height() // 2) - (name_height // 2),
            name_width, name_height
        )
        
        # Rectangles pour les options (décalés vers la gauche)
        self.race_rects = []
        self.faction_rects = []
        left_column_x = screen.get_width() // 3
        
        # Rectangle pour les races (taille inchangée)
        for i in range(len(self.races)):
            rect = pygame.Rect(0, 0, 200, 40)
            rect.center = (left_column_x, 200 + i * 50)  # Augmenté l'espacement vertical
            self.race_rects.append(rect)
        
        # Rectangle plus large pour les factions
        for i in range(len(self.factions)):
            rect = pygame.Rect(0, 0, 400, 45)  # Augmenté la largeur et la hauteur
            rect.center = (left_column_x, 200 + i * 60)  # Augmenté l'espacement vertical
            self.faction_rects.append(rect)
            
        # Zone pour les illustrations
        self.illustration_rect = pygame.Rect(
            screen.get_width() * 2 // 3,
            200,
            200,
            200
        )
        
        # Chargement et redimensionnement des illustrations des races
        self.race_illustrations = {}
        for race in self.races:
            try:
                race_image_path = os.path.join(self.base_path, "assets", f"{race}.png")
                image = pygame.image.load(race_image_path)
                scaled_image = pygame.transform.scale(image, (self.illustration_rect.width, self.illustration_rect.height))
                self.race_illustrations[race] = scaled_image
            except pygame.error as e:
                print(f"Erreur lors du chargement de l'image pour {race}: {e}")
                self.race_illustrations[race] = self.create_temp_illustration(race)

        # Chargement et redimensionnement des illustrations des factions
        self.faction_illustrations = {}
        for faction in self.factions:
            try:
                # Utilise le nom complet de la faction pour le fichier
                faction_image_path = os.path.join(self.base_path, "assets", f"{faction.value}.png")
                image = pygame.image.load(faction_image_path)
                scaled_image = pygame.transform.scale(image, (self.illustration_rect.width, self.illustration_rect.height))
                self.faction_illustrations[faction] = scaled_image
            except pygame.error as e:
                print(f"Erreur lors du chargement de l'image pour {faction.value}: {e}")
                self.faction_illustrations[faction] = self.create_temp_illustration(faction.value)

    def create_temp_illustration(self, text):
        """Crée une illustration temporaire avec un texte"""
        surface = pygame.Surface((200, 200))
        surface.fill((50, 50, 50))
        pygame.draw.rect(surface, (100, 100, 100), surface.get_rect(), 3)
        text_surface = self.small_font.render(f"Illustration pour {text}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(100, 100))
        surface.blit(text_surface, text_rect)
        return surface

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.back_button.collidepoint(event.pos):
                    if self.creation_step == 0:
                        return 'menu'
                    else:
                        self.creation_step -= 1
                        return None
                
                if self.confirm_button.collidepoint(event.pos):
                    if self.creation_step == 0 and self.name:
                        self.creation_step = 1
                    elif self.creation_step == 1:
                        self.creation_step = 2
                    elif self.creation_step == 2:
                        self.create_character()
                        return 'game'
                
                if self.creation_step == 0:
                    self.is_name_field_active = self.name_input_rect.collidepoint(event.pos)
                elif self.creation_step == 1:
                    for i, rect in enumerate(self.race_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_race = i
                elif self.creation_step == 2:
                    for i, rect in enumerate(self.faction_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_faction = i
        
        elif event.type == pygame.KEYDOWN and self.is_name_field_active:
            if event.key == pygame.K_RETURN:
                if self.name:  # Si un nom a été saisi
                    self.is_name_field_active = False
                    self.creation_step = 1  # Passe directement à l'étape suivante
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_ESCAPE:
                return 'menu'
            else:
                self.name += event.unicode
            
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Mise à jour des alphas des boutons
        for button, alpha_attr in [(self.back_button, 'back_button_alpha'),
                                 (self.confirm_button, 'confirm_button_alpha')]:
            if button.collidepoint(mouse_pos):
                setattr(self, alpha_attr, min(getattr(self, alpha_attr) + self.hover_transition_speed, 255))
            else:
                setattr(self, alpha_attr, max(getattr(self, alpha_attr) - self.hover_transition_speed, 0))
        
        # Mise à jour des alphas selon l'étape
        if self.creation_step == 1:
            for i, rect in enumerate(self.race_rects):
                if rect.collidepoint(mouse_pos):
                    self.race_alphas[i] = min(self.race_alphas[i] + self.hover_transition_speed, 255)
                else:
                    self.race_alphas[i] = max(self.race_alphas[i] - self.hover_transition_speed, 0)
        
        elif self.creation_step == 2:
            for i, rect in enumerate(self.faction_rects):
                if rect.collidepoint(mouse_pos):
                    self.faction_alphas[i] = min(self.faction_alphas[i] + self.hover_transition_speed, 255)
                else:
                    self.faction_alphas[i] = max(self.faction_alphas[i] - self.hover_transition_speed, 0)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        
        # Overlay de fond
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Bouton retour
        self.render_button(self.back_button, "Retour", self.back_button_alpha)
        
        # Bouton confirmer
        if ((self.creation_step == 0 and self.name) or 
            self.creation_step == 1 or self.creation_step == 2):
            self.render_button(self.confirm_button, "Confirmer", self.confirm_button_alpha)
        
        center_x = self.screen.get_width() // 2
        
        if self.creation_step == 0:
            # Titre
            title = self.font.render("Entrez votre nom:", True, (255, 255, 255))
            title_rect = title.get_rect(center=(center_x, self.name_input_rect.top - 50))
            self.screen.blit(title, title_rect)
            
            # Zone de saisie du nom
            pygame.draw.rect(self.screen, (30, 30, 30), self.name_input_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.name_input_rect, 2)
            
            # Texte du nom
            name_surface = self.font.render(self.name + ('|' if self.is_name_field_active else ''), True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=self.name_input_rect.center)
            self.screen.blit(name_surface, name_rect)
            
            # Indication de clic
            if not self.is_name_field_active and not self.name:
                hint = self.small_font.render("Cliquez ici pour saisir votre nom", True, (200, 200, 200))
                hint_rect = hint.get_rect(center=self.name_input_rect.center)
                self.screen.blit(hint, hint_rect)
            
        elif self.creation_step == 1:
            self.render_selection_step(
                "Choisissez votre race:",
                self.races,
                self.race_rects,
                self.race_alphas,
                self.selected_race,
                self.race_illustrations
            )
            
        elif self.creation_step == 2:
            self.render_selection_step(
                "Choisissez votre faction:",
                self.factions,
                self.faction_rects,
                self.faction_alphas,
                self.selected_faction,
                self.faction_illustrations,
                is_faction=True
            )

    def render_button(self, rect, text, alpha):
        """Rend un bouton avec animation"""
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (255, 255, 255, alpha // 3),
                        button_surface.get_rect(), border_radius=5)
        self.screen.blit(button_surface, rect)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def render_selection_step(self, title_text, items, rects, alphas, selected, illustrations, is_faction=False):
        """Rend une étape de sélection (race ou faction)"""
        # Titre
        title = self.font.render(title_text, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 3, 100))
        self.screen.blit(title, title_rect)
        
        # Options
        for i, (item, rect) in enumerate(zip(items, rects)):
            # Fond du bouton
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            alpha = 255 if i == selected else alphas[i]
            pygame.draw.rect(button_surface, (255, 255, 255, alpha // 3),
                           button_surface.get_rect(), border_radius=5)
            self.screen.blit(button_surface, rect)
            
            # Texte
            text = item.value if is_faction else item.capitalize()
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Illustration et informations
        if is_faction:
            current_faction = items[selected]
            current_illustration = illustrations[current_faction]
            
            # Affichage de l'illustration
            self.screen.blit(current_illustration, self.illustration_rect)
            
            # Création d'un rectangle pour la description
            description_rect = pygame.Rect(
                self.illustration_rect.left - 50,
                self.illustration_rect.bottom + 20,
                300,  # Largeur du rectangle
                150   # Hauteur du rectangle
            )
            
            # Dessiner le rectangle semi-transparent
            description_surface = pygame.Surface((description_rect.width, description_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(description_surface, (0, 0, 0, 128), description_surface.get_rect(), border_radius=10)
            self.screen.blit(description_surface, description_rect)
            
            # Affichage de la description de la faction
            faction_obj = FACTIONS[current_faction]
            description = faction_obj.description
            
            # Découpage de la description en lignes
            words = description.split()
            lines = []
            current_line = []
            line_width = 0
            max_width = description_rect.width - 20  # Marge de 10px de chaque côté
            
            for word in words:
                word_surface = self.small_font.render(word + " ", True, (255, 255, 255))
                word_width = word_surface.get_width()
                
                if line_width + word_width <= max_width:
                    current_line.append(word)
                    line_width += word_width
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    line_width = word_width
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Affichage de la description
            y_offset = description_rect.top + 10
            for line in lines:
                text_surface = self.small_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(midtop=(description_rect.centerx, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 25
            
        else:  # Pour les races
            current_race = items[selected]
            current_illustration = illustrations[current_race]
            
            # Affichage de l'illustration
            self.screen.blit(current_illustration, self.illustration_rect)
            
            # Création d'un rectangle pour les statistiques
            stats_rect = pygame.Rect(
                self.illustration_rect.left - 50,
                self.illustration_rect.bottom + 20,
                300,  # Largeur du rectangle
                180   # Hauteur du rectangle
            )
            
            # Dessiner le rectangle semi-transparent
            stats_surface = pygame.Surface((stats_rect.width, stats_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(stats_surface, (0, 0, 0, 128), stats_surface.get_rect(), border_radius=10)
            self.screen.blit(stats_surface, stats_rect)
            
            # Affichage des statistiques de la race
            stats = Player.RACES[current_race]
            y_offset = stats_rect.top + 10
            
            # Titre des stats
            stats_title = self.small_font.render("Statistiques:", True, (255, 255, 0))
            stats_title_rect = stats_title.get_rect(midtop=(stats_rect.centerx, y_offset))
            self.screen.blit(stats_title, stats_title_rect)
            y_offset += 30
            
            # Affichage de chaque statistique
            for stat, value in stats.items():
                # Texte de la statistique
                stat_text = f"{stat.capitalize()}: {value}"
                text_surface = self.small_font.render(stat_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(x=stats_rect.left + 20, y=y_offset)
                self.screen.blit(text_surface, text_rect)
                
                # Barre de progression
                bar_width = 120
                bar_height = 10
                bar_rect = pygame.Rect(
                    text_rect.right + 10,
                    text_rect.centery - bar_height//2,
                    bar_width,
                    bar_height
                )
                
                # Fond de la barre
                pygame.draw.rect(self.screen, (50, 50, 50), bar_rect)
                
                # Barre de progression
                progress_width = int(bar_width * (value / 10))
                progress_rect = pygame.Rect(
                    bar_rect.left,
                    bar_rect.top,
                    progress_width,
                    bar_height
                )
                
                # Couleur basée sur la valeur
                if value >= 8:
                    color = (0, 255, 0)
                elif value >= 6:
                    color = (255, 255, 0)
                else:
                    color = (255, 165, 0)
                    
                pygame.draw.rect(self.screen, color, progress_rect)
                
                y_offset += 25

    def create_character(self):
        # Création du personnage avec les choix effectués
        self.game_state.player = Player(
            name=self.name,
            x=1,  # Position initiale
            y=1,
            race=self.races[self.selected_race],
            faction=self.factions[self.selected_faction]
        ) 