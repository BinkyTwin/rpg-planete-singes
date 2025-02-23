import pygame
import os
import sys 
from .base_scene import BaseScene
from game.combat_system import CombatSystem
import random

class MessageScene(BaseScene):
    def __init__(self, screen, game_state, message, display_manager=None, dialogue_getter=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        # Si le message est None, utiliser un message par défaut
        self.message = message if message is not None else "Message non disponible"
        self.dialogue_getter = dialogue_getter
        self.combat_system = CombatSystem()
        self.combat_log = []
        self.is_defeated = False
        
        # -- Polices de base --
        self.base_font_size = 24
        self.base_text_size = 20
        self.update_fonts()
        
        # -- Couleurs / design de la boîte --
        # On s'inspire du second snippet
        self.bg_color = (50, 50, 50)                # Fond de la boîte
        self.dialog_border_color = (255, 255, 255)  # Bordure blanche
        self.text_color = (255, 255, 255)
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.button_text_color = (255, 255, 255)
        
        # -- Dimensions de la boîte de dialogue --
        self.padding = 20
        
        # =============================
        #  BOUTONS DE COMBAT
        # =============================
        self.combat_buttons = []
        combat_actions = ["Attaquer", "Se défendre", "Fuir"]
        
        # Largeur/hauteur fixes pour chaque bouton
        combat_button_width = 100
        combat_button_height = 40
        for action in combat_actions:
            text_surf = self.text_font.render(action, True, self.button_text_color)
            text_surf_hover = self.text_font.render(action, True, (200, 200, 200))
            self.combat_buttons.append({
                'rect': pygame.Rect(0, 0, combat_button_width, combat_button_height),
                'text': action,
                'hover': False,
                # On stocke le rendu sous forme de liste pour pouvoir dessiner plusieurs lignes si besoin
                'lines_surface': [text_surf],
                'lines_surface_hover': [text_surf_hover]
            })

        # =============================
        #  BOUTONS DE DÉFAITE
        # =============================
        self.defeat_buttons = []
        defeat_actions = ["Quitter"]  # On ne garde que le bouton Quitter
        
        # Dimensions du bouton
        defeat_button_width = 100
        defeat_button_height = 40  # Hauteur standard car plus besoin de 2 lignes
        for action in defeat_actions:
            surf = self.text_font.render(action, True, self.button_text_color)
            surf_hover = self.text_font.render(action, True, (200, 200, 200))
            
            self.defeat_buttons.append({
                'rect': pygame.Rect(0, 0, defeat_button_width, defeat_button_height),
                'text': action,
                'hover': False,
                'lines_surface': [surf],
                'lines_surface_hover': [surf_hover]
            })

        # =============================
        #  BOUTON "QUITTER" (hors défaite)
        # =============================
        self.quit_button = pygame.Rect(0, 0, 100, 40)
        self.quit_button_hover = False
        quit_surf = self.text_font.render("Quitter", True, self.button_text_color)
        quit_surf_hover = self.text_font.render("Quitter", True, (200, 200, 200))
        self.quit_lines_surface = [quit_surf]
        self.quit_lines_surface_hover = [quit_surf_hover]
        
        # Contiendra le texte wrapé du message principal
        self.wrapped_lines = []
        
        # Calcul initial de la taille de la boîte
        self.update_dialog_dimensions()

    # --------------------------------------------------------------------
    #   FONCTIONS UTILITAIRES
    # --------------------------------------------------------------------
    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle."""
        if self.display_manager:
            font_size = self.display_manager.get_scaled_font_size(self.base_font_size)
            text_size = self.display_manager.get_scaled_font_size(self.base_text_size)
        else:
            font_size = self.base_font_size
            text_size = self.base_text_size
            
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_font = pygame.font.SysFont("arial", text_size)

    def _wrap_text(self, text, font, max_width):
        """
        Découpe 'text' en plusieurs lignes pour ne pas dépasser 'max_width'.
        Retourne (lines, total_height, max_line_width).
        """
        # S'assurer que le texte est une chaîne de caractères
        if not isinstance(text, str):
            text = str(text)
            
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        line_height = font.get_linesize()
        total_height = 0

        for word in words:
            # Rendu provisoire pour connaître la largeur
            word_surface = font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()

            if current_width + word_width > max_width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
                total_height += line_height
            else:
                current_line.append(word)
                current_width += word_width

        # Dernière ligne
        if current_line:
            lines.append(" ".join(current_line))
            total_height += line_height

        # Calcul de la largeur maximale réelle
        max_line_width = 0
        for line in lines:
            line_surface = font.render(line, True, self.text_color)
            if line_surface.get_width() > max_line_width:
                max_line_width = line_surface.get_width()

        return lines, total_height, max_line_width

    def update_dialog_dimensions(self):
        """Met à jour la taille de la boîte de dialogue et la position des boutons en fonction du texte."""
        max_dialog_inner_width = 500 - self.padding * 2

        # Wrap du message
        self.wrapped_lines, wrapped_text_height, max_line_width = self._wrap_text(
            self.message,
            self.text_font,
            max_dialog_inner_width
        )

        # Calcul final
        self.dialog_width = min(500, max(300, max_line_width + self.padding * 2))
        self.dialog_height = wrapped_text_height + self.padding * 3 + 160

        # Centrage de la boîte
        self.dialog_rect = pygame.Rect(
            (self.screen.get_width() - self.dialog_width) // 2,
            (self.screen.get_height() - self.dialog_height) // 2,
            self.dialog_width,
            self.dialog_height
        )

        # Placement des boutons
        button_spacing = 20
        if not self.is_defeated:
            combat_button_width = self.combat_buttons[0]['rect'].width
            combat_button_height = self.combat_buttons[0]['rect'].height
            total_buttons_width = (combat_button_width * 3) + (button_spacing * 2)
            start_x = self.dialog_rect.centerx - total_buttons_width // 2

            for i, button in enumerate(self.combat_buttons):
                button['rect'] = pygame.Rect(
                    start_x + (combat_button_width + button_spacing) * i,
                    self.dialog_rect.bottom - combat_button_height - 60,
                    combat_button_width,
                    combat_button_height
                )

            # Bouton Quitter
            self.quit_button.centerx = self.dialog_rect.centerx
            self.quit_button.bottom = self.dialog_rect.bottom - 15

        else:
            defeat_button_width = self.defeat_buttons[0]['rect'].width
            defeat_button_height = self.defeat_buttons[0]['rect'].height
            defeat_button_count = len(self.defeat_buttons)
            total_defeat_width = defeat_button_count * defeat_button_width + (defeat_button_count - 1) * button_spacing
            start_x_defeat = self.dialog_rect.centerx - total_defeat_width // 2

            for i, button in enumerate(self.defeat_buttons):
                button['rect'] = pygame.Rect(
                    start_x_defeat + i * (defeat_button_width + button_spacing),
                    self.dialog_rect.bottom - defeat_button_height - 60,
                    defeat_button_width,
                    defeat_button_height
                )

    # --------------------------------------------------------------------
    #   LOGIQUE DE COMBAT
    # --------------------------------------------------------------------
    def handle_combat_action(self, action):
        if not self.game_state.player:
            print("DEBUG: Pas de joueur trouvé")
            return
        
        if not hasattr(self.game_state, 'pnj2'):
            print("DEBUG: PNJ2 non trouvé")
            return

        if self.is_defeated:
            return None

        self.combat_log = []

        if action == "Attaquer":
            weapon = None
            if hasattr(self.game_state.player, 'inventory'):
                weapon = self.game_state.player.inventory.get_equipped_weapon()

            damage_player, is_enemy_dead = self.combat_system.attack(
                self.game_state.player,
                self.game_state.pnj2,
                weapon,
                False
            )
            self.combat_log.append(f"Vous attaquez et infligez {damage_player} dégâts !")
            self.combat_log.append(f"PNJ2 HP: {self.game_state.pnj2.hp}/{self.game_state.pnj2.max_hp}")
            if is_enemy_dead:
                self.combat_log.append("Victoire ! Le PNJ2 est vaincu !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'

            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,
                False
            )
            self.combat_log.append(f"L'ennemi riposte et vous inflige {damage_enemy} dégâts !")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")
            if is_player_dead:
                self.handle_player_death("Défaite ! Vous avez été vaincu !")
                return None

        elif action == "Se défendre":
            self.combat_log.append("Vous vous mettez en position défensive.")
            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,
                True
            )
            self.combat_log.append("Le PNJ2 attaque, mais vous bloquez la majorité des dégâts !")
            self.combat_log.append(f"Vous ne subissez que {damage_enemy} dégâts.")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")
            if is_player_dead:
                self.handle_player_death("Défaite ! Vous avez été vaincu malgré votre défense !")
                return None

        elif action == "Fuir":
            if random.random() < 0.5:
                self.combat_log.append("Vous réussissez à fuir le combat !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'
            else:
                self.combat_log.append("Vous n'arrivez pas à fuir !")
                damage_enemy, is_player_dead = self.combat_system.attack(
                    self.game_state.pnj2,
                    self.game_state.player,
                    self.game_state.pnj2.held_item,
                    False
                )
                self.combat_log.append(f"Le PNJ2 vous attaque pendant votre fuite et inflige {damage_enemy} dégâts !")
                self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")
                if is_player_dead:
                    self.handle_player_death("Défaite ! Vous avez été vaincu en essayant de fuir !")
                    return None

        # Mettre à jour le message avec le nouveau combat_log
        self.message = "\n".join(self.combat_log)
        self.update_dialog_dimensions()

    def handle_player_death(self, death_message):
        """Gère la mort du joueur"""
        self.combat_log = [death_message]
        self.message = "\n".join(self.combat_log)
        self.is_defeated = True
        self.game_state.game_over = True
        self.update_dialog_dimensions()

    # --------------------------------------------------------------------
    #   GESTION DES ÉVÉNEMENTS
    # --------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if not self.is_defeated:
                    # Bouton "Quitter" en mode non-défaite
                    if self.quit_button.collidepoint(event.pos):
                        return 'game'
                    # Boutons de combat
                    for button in self.combat_buttons:
                        if button['rect'].collidepoint(event.pos):
                            return self.handle_combat_action(button['text'])
                else:
                    # Boutons de défaite
                    for button in self.defeat_buttons:
                        if button['rect'].collidepoint(event.pos):
                            if button['text'] == "Quitter":
                                print("Fermeture du jeu...")
                                # Fermeture propre de Pygame
                                pygame.quit()
                                # Sortie du programme
                                sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            if not self.is_defeated:
                self.quit_button_hover = self.quit_button.collidepoint(event.pos)
                for button in self.combat_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
            else:
                for button in self.defeat_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            self.update_dialog_dimensions()
        return None

    def update(self):
        pass

    # --------------------------------------------------------------------
    #   RENDU
    # --------------------------------------------------------------------
    def render(self, screen):
        """
        Version sans fond noir couvrant tout l'écran
        et avec un design de boîte inspiré de 'DialogBox'.
        """
        # 1) On ne dessine plus d'arrière-plan noir sur tout l'écran.
        #    (Si vous souhaitez un overlay semi-transparent, décommentez ceci :)
        #
        # overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        # overlay.fill((0, 0, 0, 128))  # un voile semi-transparent
        # screen.blit(overlay, (0, 0))
        
        # 2) On crée une surface pour la boîte
        dialog_surface = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))
        dialog_surface.fill(self.bg_color)  # Fond uni
        # Bordure blanche
        pygame.draw.rect(
            dialog_surface,
            self.dialog_border_color,
            dialog_surface.get_rect(),
            width=2,         # Épaisseur de la bordure
            border_radius=10 # Coins arrondis
        )

        # 3) Affichage du texte principal (wrapé)
        y_offset = self.padding
        for line in self.wrapped_lines:
            line_surface = self.text_font.render(line, True, self.text_color)
            text_rect = line_surface.get_rect(centerx=self.dialog_rect.width // 2, top=y_offset)
            dialog_surface.blit(line_surface, text_rect)
            y_offset += line_surface.get_height() + 5

        # 4) Choix des boutons à afficher
        if self.is_defeated:
            buttons_to_render = self.defeat_buttons
        else:
            buttons_to_render = self.combat_buttons

        # 5) Dessin des boutons
        for button in buttons_to_render:
            # Ombre légère (optionnel)
            shadow_rect = button['rect'].copy()
            shadow_rect.x -= self.dialog_rect.x
            shadow_rect.y -= self.dialog_rect.y
            shadow_rect.y += 2  # décalage vertical
            pygame.draw.rect(dialog_surface, (30, 30, 30), shadow_rect, border_radius=5)
            
            # Corps du bouton
            button_rect = button['rect'].copy()
            button_rect.x -= self.dialog_rect.x
            button_rect.y -= self.dialog_rect.y
            color = self.button_hover_color if button['hover'] else self.button_color
            pygame.draw.rect(dialog_surface, color, button_rect, border_radius=5)
            
            # Bordure
            pygame.draw.rect(dialog_surface, (255, 255, 255), button_rect, 1, border_radius=5)
            
            # Texte (multilignes)
            lines = button['lines_surface_hover'] if button['hover'] else button['lines_surface']
            total_lines_height = sum(s.get_height() for s in lines)
            current_y = button_rect.centery - total_lines_height // 2
            for surf in lines:
                line_rect = surf.get_rect(centerx=button_rect.centerx, y=current_y)
                dialog_surface.blit(surf, line_rect)
                current_y += surf.get_height()

        # 6) Bouton "Quitter" (si pas en défaite)
        if not self.is_defeated:
            button_relative_rect = pygame.Rect(
                self.quit_button.x - self.dialog_rect.x,
                self.quit_button.y - self.dialog_rect.y,
                self.quit_button.width,
                self.quit_button.height
            )
            # Ombre
            shadow_rect = button_relative_rect.copy()
            shadow_rect.y += 2
            pygame.draw.rect(dialog_surface, (30, 30, 30), shadow_rect, border_radius=5)
            
            # Corps
            color = self.button_hover_color if self.quit_button_hover else self.button_color
            pygame.draw.rect(dialog_surface, color, button_relative_rect, border_radius=5)
            
            # Bordure
            pygame.draw.rect(dialog_surface, (255, 255, 255), button_relative_rect, 1, border_radius=5)
            
            # Texte (monoligne)
            lines = self.quit_lines_surface_hover if self.quit_button_hover else self.quit_lines_surface
            total_lines_height = sum(s.get_height() for s in lines)
            current_y = button_relative_rect.centery - total_lines_height // 2
            for surf in lines:
                line_rect = surf.get_rect(centerx=button_relative_rect.centerx, y=current_y)
                dialog_surface.blit(surf, line_rect)
                current_y += surf.get_height()

        # 7) On blit la boîte sur l'écran
        screen.blit(dialog_surface, self.dialog_rect)
