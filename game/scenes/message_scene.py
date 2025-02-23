import pygame
import os
import sys 
from .base_scene import BaseScene
from game.combat_system import CombatSystem
from game.ui.inventory_display import InventoryDisplay
import game.quest_system as quest_system
import random

class MessageScene(BaseScene):
    def __init__(self, screen, game_state, message, display_manager=None, dialogue_getter=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        # Si le message est None, utiliser un message par défaut
        self.message = message if message is not None else "Vous êtes dans la zone de combat !\nPréparez vous\n\nVos HP: {game_state.player.hp}"
        self.dialogue_getter = dialogue_getter
        self.combat_system = CombatSystem()
        self.combat_log = []
        self.is_defeated = False
        self.inventory_display = None  # Pour l'affichage de l'inventaire
        self.is_defending = False  # Pour suivre l'état de défense
        self.defense_buttons = []  # Boutons spécifiques pour la défense
        self.inventory_timer = 0  # Timer pour l'inventaire
        self.in_defense_mode = False  # Pour suivre si on est dans le mode défense
        
        # Mise à jour du message initial avec les HP actuels si on est dans une zone de combat
        if message is not None and "zone de combat" in message.lower() and game_state.player:
            self.message = f"Vous êtes dans la zone de combat !\nPréparez vous\n\nVos HP: {game_state.player.hp}"
        
        # -- Polices de base --
        self.base_font_size = 24
        self.base_text_size = 20
        self.update_fonts()
        
        # -- Couleurs / design de la boîte --
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
        
        combat_button_width = 100
        combat_button_height = 40
        for action in combat_actions:
            text_surf = self.text_font.render(action, True, self.button_text_color)
            text_surf_hover = self.text_font.render(action, True, (200, 200, 200))
            self.combat_buttons.append({
                'rect': pygame.Rect(0, 0, combat_button_width, combat_button_height),
                'text': action,
                'hover': False,
                'lines_surface': [text_surf],
                'lines_surface_hover': [text_surf_hover]
            })

        # =============================
        #  BOUTONS DE DÉFAITE
        # =============================
        self.defeat_buttons = []
        defeat_actions = ["Quitter"]  # On ne garde que le bouton Quitter
        
        defeat_button_width = 100
        defeat_button_height = 40
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

        if current_line:
            lines.append(" ".join(current_line))
            total_height += line_height

        max_line_width = 0
        for line in lines:
            line_surface = font.render(line, True, self.text_color)
            if line_surface.get_width() > max_line_width:
                max_line_width = line_surface.get_width()

        return lines, total_height, max_line_width

    def update_dialog_dimensions(self):
        max_dialog_inner_width = 500 - self.padding * 2
        self.wrapped_lines, wrapped_text_height, max_line_width = self._wrap_text(
            self.message,
            self.text_font,
            max_dialog_inner_width
        )

        self.dialog_width = min(500, max(300, max_line_width + self.padding * 2))
        self.dialog_height = wrapped_text_height + self.padding * 3 + 160

        self.dialog_rect = pygame.Rect(
            (self.screen.get_width() - self.dialog_width) // 2,
            (self.screen.get_height() - self.dialog_height) // 2,
            self.dialog_width,
            self.dialog_height
        )

        # On gère l'emplacement des boutons
        button_spacing = 20
        if not self.is_defeated:
            # Vérifier si on n'a qu'un seul bouton "Continuer" (victoire)
            if len(self.combat_buttons) == 1 and self.combat_buttons[0]['text'] == "Continuer":
                # Centrer le bouton "Continuer"
                single_btn = self.combat_buttons[0]
                w = single_btn['rect'].width
                h = single_btn['rect'].height
                x = self.dialog_rect.centerx - w // 2
                y = self.dialog_rect.bottom - h - 60
                single_btn['rect'].update(x, y, w, h)

                # NE PAS placer le bouton Quitter
            else:
                # Placement normal (3 boutons : Attaquer, Se défendre, Fuir)
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
            # État de défaite : placement du bouton Quitter
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
    def create_defense_buttons(self):
        """Crée les boutons spécifiques au mode défense"""
        self.defense_buttons = []
        defense_actions = ["Ouvrir l'inventaire", "Retour au combat"]
        
        button_width = 150
        button_height = 40
        for action in defense_actions:
            text_surf = self.text_font.render(action, True, self.button_text_color)
            text_surf_hover = self.text_font.render(action, True, (200, 200, 200))
            self.defense_buttons.append({
                'rect': pygame.Rect(0, 0, button_width, button_height),
                'text': action,
                'hover': False,
                'lines_surface': [text_surf],
                'lines_surface_hover': [text_surf_hover]
            })

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

        print(f"\n=== DÉBUT DU TOUR ===")
        print(f"HP Joueur: {self.game_state.player.hp}")
        print(f"HP Ennemi: {self.game_state.pnj2.hp}")

        if action == "Attaquer":
            self.is_defending = False  # Réinitialiser l'état de défense
            self.in_defense_mode = False  # Sortir du mode défense
            weapon = None
            if hasattr(self.game_state.player, 'inventory'):
                weapon = self.game_state.player.inventory.get_equipped_weapon()
                if weapon:
                    print(f"Arme équipée: {weapon.name} (Dégâts: {weapon.value})")

            damage_player, is_enemy_dead = self.combat_system.attack(
                self.game_state.player,
                self.game_state.pnj2,
                weapon,
                False
            )
            print(f"\n=== APRÈS ATTAQUE JOUEUR ===")
            print(f"Dégâts infligés: {damage_player}")
            print(f"HP Joueur: {self.game_state.player.hp}")
            print(f"HP Ennemi: {self.game_state.pnj2.hp}")

            self.combat_log.append(f"Vous attaquez et infligez {damage_player} dégâts !")
            self.combat_log.append(f"Ennemi HP: {self.game_state.pnj2.hp}")

            if is_enemy_dead:
                victory_message = [
                    "Victoire ! L'ennemi est vaincu !",
                    "\nBravo, vous avez tué le méchant gorille !",
                    "Allez au bout de la montagne rejoindre votre famille."
                ]
                self.combat_log = victory_message
                self.game_state.pnj2.is_visible = False
                if hasattr(self.game_state, 'game_scene'):
                    self.game_state.game_scene.combat_zone_positions = set()
                    self.game_state.game_scene.in_combat_zone = False
                    self.game_state.game_scene.combat_dialog_active = False
                
                # Mettre à jour la quête 4
                quest_system.is_enemy_dead = True
                quest_system.quest4_done = True
                quest_system.advance_quest_if_done()
                
                # On remplace les 3 boutons par un seul "Continuer"
                self.combat_buttons = []
                continue_button = {
                    'rect': pygame.Rect(0, 0, 120, 40),
                    'text': "Continuer",
                    'hover': False,
                    'lines_surface': [self.text_font.render("Continuer", True, self.button_text_color)],
                    'lines_surface_hover': [self.text_font.render("Continuer", True, (200, 200, 200))]
                }
                self.combat_buttons.append(continue_button)
                
                self.message = "\n".join(victory_message)
                self.update_dialog_dimensions()
                return None

            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,
                False
            )
            print(f"\n=== APRÈS RIPOSTE ENNEMI ===")
            print(f"Dégâts subis: {damage_enemy}")
            print(f"HP Joueur: {self.game_state.player.hp}")
            print(f"HP Ennemi: {self.game_state.pnj2.hp}")

            self.combat_log.append(f"L'ennemi riposte et vous inflige {damage_enemy} dégâts !")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}")

            if is_player_dead:
                self.handle_player_death("Défaite ! Vous avez été vaincu !")
                return None

        elif action == "Se défendre":
            self.is_defending = True  # Activer l'état de défense
            self.in_defense_mode = True  # Activer le mode défense
            self.create_defense_buttons()  # Créer les boutons de défense
            
            self.combat_log.append("Vous vous mettez en position défensive.")
            self.combat_log.append("Choisissez une action :")
            self.combat_log.append("- Ouvrir l'inventaire (touche 'i')")
            self.combat_log.append("- Retourner au combat")
            
            self.message = "\n".join(self.combat_log)
            self.update_dialog_dimensions()
            return None

        elif action == "Ouvrir l'inventaire":
            if not self.inventory_display:
                self.inventory_display = InventoryDisplay(self.screen)
            self.inventory_display.toggle()
            self.inventory_timer = pygame.time.get_ticks()  # Démarrer le timer
            return None

        elif action == "Retour au combat":
            self.in_defense_mode = False  # Désactiver le mode défense
            
            # Appliquer la réduction de dégâts (5% des dégâts normaux)
            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,
                True,
                damage_reduction=0.95  # 95% de réduction
            )
            
            print(f"\n=== APRÈS DÉFENSE ===")
            print(f"Dégâts réduits subis: {damage_enemy}")
            print(f"HP Joueur: {self.game_state.player.hp}")
            print(f"HP Ennemi: {self.game_state.pnj2.hp}")

            self.combat_log.append("L'ennemi attaque, mais votre défense réduit considérablement les dégâts !")
            self.combat_log.append(f"Vous ne subissez que {damage_enemy} dégâts.")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}")

            if is_player_dead:
                self.handle_player_death("Défaite ! Vous avez été vaincu malgré votre défense !")
                return None

        elif action == "Fuir":
            self.is_defending = False  # Réinitialiser l'état de défense
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
                print(f"\n=== APRÈS ÉCHEC DE FUITE ===")
                print(f"Dégâts subis: {damage_enemy}")
                print(f"HP Joueur: {self.game_state.player.hp}")
                print(f"HP Ennemi: {self.game_state.pnj2.hp}")

                self.combat_log.append(f"L'ennemi vous attaque pendant votre fuite et inflige {damage_enemy} dégâts !")
                self.combat_log.append(f"Vos HP: {self.game_state.player.hp}")

                if is_player_dead:
                    self.handle_player_death("Défaite ! Vous avez été vaincu en essayant de fuir !")
                    return None

        print(f"\n=== FIN DU TOUR ===")
        print(f"HP Joueur: {self.game_state.player.hp}")
        print(f"HP Ennemi: {self.game_state.pnj2.hp}")

        self.message = "\n".join(self.combat_log)
        self.update_dialog_dimensions()

    def handle_player_death(self, death_message):
        self.combat_log = [death_message]
        self.message = "\n".join(self.combat_log)
        self.is_defeated = True
        self.game_state.game_over = True
        self.update_dialog_dimensions()

    # --------------------------------------------------------------------
    #   GESTION DES ÉVÉNEMENTS
    # --------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Si l'inventaire est visible, gérer ses événements en priorité
            if self.inventory_display and self.inventory_display.visible:
                if self.inventory_display.handle_click(event.pos, self.game_state.player.inventory, self.game_state.player):
                    # Fermer l'inventaire après utilisation d'un objet
                    self.inventory_display.hide()
                    return None
                return None

            # Si on est en mode défense, gérer les boutons de défense
            if self.in_defense_mode:
                for button in self.defense_buttons:
                    if button['rect'].collidepoint(event.pos):
                        return self.handle_combat_action(button['text'])
                return None

            if not self.is_defeated:
                # Bouton "Quitter" (si pas vaincu et qu'il est dessiné)
                if self.quit_button.collidepoint(event.pos):
                    return 'game'
                # Boutons de combat ou "Continuer"
                for button in self.combat_buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == "Continuer":
                            return 'game'
                        return self.handle_combat_action(button['text'])
            else:
                # Boutons de défaite (Quitter)
                for button in self.defeat_buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == "Quitter":
                            print("Fermeture du jeu...")
                            pygame.quit()
                            sys.exit(0)
                            
        elif event.type == pygame.MOUSEMOTION:
            # Mise à jour du survol pour l'inventaire
            if self.inventory_display and self.inventory_display.visible:
                self.inventory_display.update_hover(event.pos)
                return None

            # Mise à jour du survol pour les boutons de défense
            if self.in_defense_mode:
                for button in self.defense_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
                return None

            if not self.is_defeated:
                self.quit_button_hover = self.quit_button.collidepoint(event.pos)
                for button in self.combat_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
            else:
                for button in self.defeat_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:  # Touche 'i'
                if self.inventory_display:
                    if self.inventory_display.visible:
                        self.inventory_display.hide()
                    else:
                        self.inventory_display.toggle()
                        self.inventory_timer = pygame.time.get_ticks()
                    
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            self.update_dialog_dimensions()
            if self.inventory_display:
                self.inventory_display.needs_update = True
        return None

    def update(self):
        # Gestion du timer de l'inventaire
        if self.inventory_display and self.inventory_display.visible:
            current_time = pygame.time.get_ticks()
            if current_time - self.inventory_timer > 5000:  # 5 secondes
                self.inventory_display.hide()
        
        # Mise à jour si zone de combat
        if not self.combat_log and "zone de combat" in self.message.lower() and self.game_state.player:
            self.message = f"Vous êtes dans la zone de combat !\nPréparez vous\n\nVos HP: {self.game_state.player.hp}"
            self.update_dialog_dimensions()

    # --------------------------------------------------------------------
    #   RENDU
    # --------------------------------------------------------------------
    def render(self, screen):
        # Pas de fond noir général
        dialog_surface = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))
        dialog_surface.fill(self.bg_color)
        pygame.draw.rect(
            dialog_surface,
            self.dialog_border_color,
            dialog_surface.get_rect(),
            width=2,
            border_radius=10
        )

        # Afficher le texte
        y_offset = self.padding
        for line in self.wrapped_lines:
            line_surface = self.text_font.render(line, True, self.text_color)
            text_rect = line_surface.get_rect(centerx=self.dialog_rect.width // 2, top=y_offset)
            dialog_surface.blit(line_surface, text_rect)
            y_offset += line_surface.get_height() + 5

        # Choisir quels boutons afficher
        if self.is_defeated:
            buttons_to_render = self.defeat_buttons
        elif self.in_defense_mode:
            buttons_to_render = self.defense_buttons
        else:
            buttons_to_render = self.combat_buttons

        # Calcul des dimensions pour le positionnement des boutons
        button_spacing = 20
        total_width = sum(button['rect'].width for button in buttons_to_render) + button_spacing * (len(buttons_to_render) - 1)
        
        # Position horizontale des boutons (centrés)
        start_x = (self.dialog_rect.width - total_width) // 2
        
        # Position verticale des boutons (en bas de la boîte de dialogue)
        button_y = self.dialog_rect.height - 95  # Remonté de 10 pixels (de 80 à 90)

        # Mise à jour et rendu des boutons
        for i, button in enumerate(buttons_to_render):
            # Calculer la position du bouton
            button_x = start_x + i * (button['rect'].width + button_spacing)
            
            # Mettre à jour la position du rectangle du bouton
            # Ajout de la position de la boîte de dialogue pour synchroniser avec l'écran
            absolute_x = self.dialog_rect.x + button_x
            absolute_y = self.dialog_rect.y + button_y
            button['rect'].update(absolute_x, absolute_y, button['rect'].width, button['rect'].height)

            # Pour le rendu, utiliser les positions relatives à la surface de dialogue
            button_relative_rect = pygame.Rect(button_x, button_y, button['rect'].width, button['rect'].height)

            # Dessiner l'ombre du bouton
            shadow_rect = button_relative_rect.copy()
            shadow_rect.y += 2
            pygame.draw.rect(dialog_surface, (30, 30, 30), shadow_rect, border_radius=5)
            
            # Dessiner le bouton
            color = self.button_hover_color if button['hover'] else self.button_color
            pygame.draw.rect(dialog_surface, color, button_relative_rect, border_radius=5)
            pygame.draw.rect(dialog_surface, (255, 255, 255), button_relative_rect, 1, border_radius=5)
            
            # Dessiner le texte du bouton
            lines = button['lines_surface_hover'] if button['hover'] else button['lines_surface']
            total_lines_height = sum(s.get_height() for s in lines)
            current_y = button_relative_rect.centery - total_lines_height // 2
            
            for surf in lines:
                text_rect = surf.get_rect(
                    centerx=button_relative_rect.centerx,
                    centery=current_y + surf.get_height() // 2
                )
                dialog_surface.blit(surf, text_rect)
                current_y += surf.get_height()

        # Dessin du bouton "Quitter" si nécessaire
        if (not self.is_defeated and not self.in_defense_mode
            and not (len(self.combat_buttons) == 1 and self.combat_buttons[0]['text'] == "Continuer")):
            
            # Positionner le bouton Quitter en bas à droite
            quit_button_y = self.dialog_rect.height - 45  # Monté de 15 pixels (de 30 à 45)
            quit_button_x = self.dialog_rect.width - self.quit_button.width - 20
            
            # Mettre à jour la position absolue du rectangle de clic
            absolute_x = self.dialog_rect.x + quit_button_x
            absolute_y = self.dialog_rect.y + quit_button_y
            self.quit_button.update(absolute_x, absolute_y, self.quit_button.width, self.quit_button.height)
            
            # Créer un rectangle relatif pour le rendu
            button_relative_rect = pygame.Rect(quit_button_x, quit_button_y, self.quit_button.width, self.quit_button.height)
            
            # Dessiner l'ombre
            shadow_rect = button_relative_rect.copy()
            shadow_rect.y += 2
            pygame.draw.rect(dialog_surface, (30, 30, 30), shadow_rect, border_radius=5)
            
            # Dessiner le bouton
            color = self.button_hover_color if self.quit_button_hover else self.button_color
            pygame.draw.rect(dialog_surface, color, button_relative_rect, border_radius=5)
            pygame.draw.rect(dialog_surface, (255, 255, 255), button_relative_rect, 1, border_radius=5)
            
            # Dessiner le texte
            lines = self.quit_lines_surface_hover if self.quit_button_hover else self.quit_lines_surface
            total_lines_height = sum(s.get_height() for s in lines)
            current_y = button_relative_rect.centery - total_lines_height // 2
            
            for surf in lines:
                text_rect = surf.get_rect(
                    centerx=button_relative_rect.centerx,
                    centery=current_y + surf.get_height() // 2
                )
                dialog_surface.blit(surf, text_rect)
                current_y += surf.get_height()

        # Afficher la boîte de dialogue
        screen.blit(dialog_surface, self.dialog_rect)

        # Afficher l'inventaire par-dessus si nécessaire
        if self.inventory_display and self.inventory_display.visible:
            self.inventory_display.render(self.game_state.player.inventory)
