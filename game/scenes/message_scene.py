import pygame
import os
from .base_scene import BaseScene
from game.combat_system import CombatSystem

class MessageScene(BaseScene):
    def __init__(self, screen, game_state, message, display_manager=None, dialogue_getter=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        self.message = message
        self.dialogue_getter = dialogue_getter
        self.combat_system = CombatSystem()
        self.combat_log = []  # Pour stocker les messages de combat
        
        # Tailles de base pour les polices
        self.base_font_size = 24
        self.base_text_size = 20
        self.update_fonts()
        
        # Couleurs
        self.text_color = (255, 255, 255)  # Blanc pour le texte
        self.button_color = (70, 70, 70, 200)  # Gris foncé semi-transparent pour le bouton
        self.button_hover_color = (90, 90, 90, 220)  # Gris plus clair pour le survol
        self.button_text_color = (255, 255, 255)  # Blanc pour le texte du bouton
        self.dialog_bg_color = (40, 40, 40, 180)  # Fond de la boîte de dialogue
        self.dialog_border_color = (100, 100, 100, 255)  # Bordure de la boîte de dialogue
        self.combat_text_color = (255, 200, 0)  # Jaune pour les messages de combat
        
        # Dimensions de la boîte de dialogue
        self.padding = 20
        self.button_padding = 10
        
        # Calcul des dimensions du texte
        self.text_surface = self.text_font.render(message, True, self.text_color)
        text_width = self.text_surface.get_width()
        text_height = self.text_surface.get_height()
        
        # Dimensions de la boîte de dialogue
        self.dialog_width = min(500, max(300, text_width + self.padding * 2))
        self.dialog_height = text_height + self.padding * 3 + 160  # Extra space for combat buttons
        
        self.dialog_rect = pygame.Rect(
            (screen.get_width() - self.dialog_width) // 2,
            (screen.get_height() - self.dialog_height) // 2,
            self.dialog_width,
            self.dialog_height
        )
        
        # Configuration des boutons de combat
        self.combat_buttons = []
        button_width = 120
        button_height = 35
        button_spacing = 10
        total_buttons_width = (button_width * 3) + (button_spacing * 2)
        start_x = self.dialog_rect.centerx - total_buttons_width // 2

        # Création des boutons de combat
        combat_actions = ["Attaquer", "Se défendre", "Fuir"]
        for i, action in enumerate(combat_actions):
            button_rect = pygame.Rect(
                start_x + (button_width + button_spacing) * i,
                self.dialog_rect.bottom - button_height - 60,
                button_width,
                button_height
            )
            self.combat_buttons.append({
                'rect': button_rect,
                'text': action,
                'hover': False,
                'text_surface': self.text_font.render(action, True, self.button_text_color),
                'text_surface_hover': self.text_font.render(action, True, (200, 200, 200))
            })

        # Bouton Quitter
        self.quit_button = pygame.Rect(
            self.dialog_rect.centerx - button_width // 2,
            self.dialog_rect.bottom - button_height - 15,
            button_width,
            button_height
        )
        self.quit_button_hover = False
        
        # Texte du bouton
        self.quit_text = self.text_font.render("Quitter", True, self.button_text_color)
        self.quit_text_hover = self.text_font.render("Quitter", True, (200, 200, 200))

    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            font_size = self.display_manager.get_scaled_font_size(self.base_font_size)
            text_size = self.display_manager.get_scaled_font_size(self.base_text_size)
        else:
            font_size = self.base_font_size
            text_size = self.base_text_size
            
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_font = pygame.font.SysFont("arial", text_size)

    def handle_combat_action(self, action):
        """Gère les actions de combat"""
        if not self.game_state.player:
            print("DEBUG: Pas de joueur trouvé")
            return
        
        if not hasattr(self.game_state, 'pnj2'):
            print("DEBUG: PNJ2 non trouvé")
            return

        # Réinitialiser le combat_log au début de chaque action
        self.combat_log = []

        print(f"DEBUG: Action de combat: {action}")
        print(f"DEBUG: HP Joueur: {self.game_state.player.hp}")
        print(f"DEBUG: HP PNJ2: {self.game_state.pnj2.hp}")

        if action == "Attaquer":
            # Récupérer l'arme équipée du joueur
            weapon = None
            if hasattr(self.game_state.player, 'inventory'):
                weapon = self.game_state.player.inventory.get_equipped_weapon()
                print(f"DEBUG: Arme équipée: {weapon.name if weapon else 'aucune'}")

            # Le joueur attaque
            damage_player, is_enemy_dead = self.combat_system.attack(
                self.game_state.player,
                self.game_state.pnj2,
                weapon,
                False  # Pas en mode défense
            )
            
            print(f"DEBUG: Dégâts infligés par le joueur: {damage_player}")
            
            # Ajouter le message de combat
            self.combat_log.append(f"Vous attaquez et infligez {damage_player} dégâts !")
            self.combat_log.append(f"PNJ2 HP: {self.game_state.pnj2.hp}/{self.game_state.pnj2.max_hp}")

            if is_enemy_dead:
                self.combat_log.append("Victoire ! Le PNJ2 est vaincu !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'

            # Le PNJ2 riposte avec son épée rouillée
            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,  # Utilise l'épée rouillée du PNJ2
                False  # Pas en mode défense
            )
            
            print(f"DEBUG: Dégâts infligés par le PNJ2: {damage_enemy}")
            
            self.combat_log.append(f"L'ennemie riposte avec son épée rouillée et vous inflige {damage_enemy} dégâts !")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")

            if is_player_dead:
                self.combat_log.append("Défaite ! Vous avez été vaincu !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'

        elif action == "Se défendre":
            # Le joueur se défend (réduction des dégâts de 95%)
            self.combat_log.append("Vous vous mettez en position défensive.")
            
            # Le PNJ2 attaque avec son épée rouillée
            damage_enemy, is_player_dead = self.combat_system.attack(
                self.game_state.pnj2,
                self.game_state.player,
                self.game_state.pnj2.held_item,
                True  # Mode défense activé
            )
            
            self.combat_log.append(f"Le PNJ2 attaque mais vous bloquez la majorité des dégâts !")
            self.combat_log.append(f"Vous ne subissez que {damage_enemy} dégâts.")
            self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")

            if is_player_dead:
                self.combat_log.append("Défaite ! Vous avez été vaincu malgré votre défense !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'

        elif action == "Fuir":
            # 50% de chance de réussir à fuir
            import random
            if random.random() < 0.5:
                self.combat_log.append("Vous réussissez à fuir le combat !")
                self.message = "\n".join(self.combat_log)
                self.update_dialog_dimensions()
                return 'game'
            else:
                self.combat_log.append("Vous n'arrivez pas à fuir !")
                
                # Le PNJ2 attaque pendant la tentative de fuite
                damage_enemy, is_player_dead = self.combat_system.attack(
                    self.game_state.pnj2,
                    self.game_state.player,
                    self.game_state.pnj2.held_item,
                    False
                )
                
                self.combat_log.append(f"Le PNJ2 vous attaque pendant votre tentative de fuite et inflige {damage_enemy} dégâts !")
                self.combat_log.append(f"Vos HP: {self.game_state.player.hp}/{self.game_state.player.max_hp}")

                if is_player_dead:
                    self.combat_log.append("Défaite ! Vous avez été vaincu en essayant de fuir !")
                    self.message = "\n".join(self.combat_log)
                    self.update_dialog_dimensions()
                    return 'game'

        # Mettre à jour le message avec le nouveau combat_log
        self.message = "\n".join(self.combat_log)
        self.update_dialog_dimensions()

    def update_dialog_dimensions(self):
        """Met à jour les dimensions de la boîte de dialogue en fonction du contenu"""
        # Recalculer les dimensions du texte
        self.text_surface = self.text_font.render(self.message, True, self.text_color)
        text_width = self.text_surface.get_width()
        text_height = self.text_surface.get_height()
        
        # Mettre à jour les dimensions de la boîte de dialogue
        self.dialog_width = min(500, max(300, text_width + self.padding * 2))
        self.dialog_height = text_height + self.padding * 3 + 160
        
        # Mettre à jour la position de la boîte de dialogue
        self.dialog_rect = pygame.Rect(
            (self.screen.get_width() - self.dialog_width) // 2,
            (self.screen.get_height() - self.dialog_height) // 2,
            self.dialog_width,
            self.dialog_height
        )
        
        # Mettre à jour la position des boutons
        button_width = 120
        button_height = 35
        button_spacing = 10
        total_buttons_width = (button_width * 3) + (button_spacing * 2)
        start_x = self.dialog_rect.centerx - total_buttons_width // 2

        for i, button in enumerate(self.combat_buttons):
            button['rect'] = pygame.Rect(
                start_x + (button_width + button_spacing) * i,
                self.dialog_rect.bottom - button_height - 60,
                button_width,
                button_height
            )
        
        self.quit_button.centerx = self.dialog_rect.centerx
        self.quit_button.bottom = self.dialog_rect.bottom - 15

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.quit_button.collidepoint(event.pos):
                    return 'game'
                # Vérification des clics sur les boutons de combat
                for button in self.combat_buttons:
                    if button['rect'].collidepoint(event.pos):
                        print(f"Action sélectionnée : {button['text']}")
                        return self.handle_combat_action(button['text'])
        elif event.type == pygame.MOUSEMOTION:
            self.quit_button_hover = self.quit_button.collidepoint(event.pos)
            # Mise à jour de l'état de survol des boutons de combat
            for button in self.combat_buttons:
                button['hover'] = button['rect'].collidepoint(event.pos)
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            self.update_dialog_dimensions()
        return None

    def update(self):
        pass

    def render(self, screen):
        # Supprimer ou commenter ces lignes pour enlever l'overlay
        # overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # overlay.fill((0, 0, 0, 100))
        # screen.blit(overlay, (0, 0))
        
        # Ajouter un fond opaque à la boîte de dialogue
        dialog_background = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))
        dialog_background.fill((0, 0, 0))  # Fond noir
        screen.blit(dialog_background, (self.dialog_rect.x, self.dialog_rect.y))
        
        # Créer la surface de la boîte de dialogue avec transparence
        dialog_surface = pygame.Surface(self.dialog_rect.size, pygame.SRCALPHA)
        
        # Dessiner le fond de la boîte avec un dégradé
        for i in range(self.dialog_rect.height):
            alpha = min(180, 150 + i // 2)  # Dégradé de transparence
            pygame.draw.line(dialog_surface, (*self.dialog_bg_color[:3], alpha),
                           (0, i), (self.dialog_rect.width, i))
        
        # Ajouter une bordure élégante
        pygame.draw.rect(dialog_surface, self.dialog_border_color, dialog_surface.get_rect(), 2, border_radius=10)
        
        # Rendu du message avec gestion du retour à la ligne
        words = self.message.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = self.text_font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()
            
            if current_width + word_width > self.dialog_rect.width - self.padding * 2:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Afficher les lignes de texte
        y_offset = self.padding
        for line in lines:
            line_surface = self.text_font.render(line, True, self.text_color)
            text_rect = line_surface.get_rect(centerx=self.dialog_rect.width // 2, top=y_offset)
            dialog_surface.blit(line_surface, text_rect)
            y_offset += line_surface.get_height() + 5

        # Rendu des boutons de combat
        for button in self.combat_buttons:
            # Effet d'ombre du bouton
            shadow_rect = button['rect'].copy()
            shadow_rect.x -= self.dialog_rect.x
            shadow_rect.y -= self.dialog_rect.y
            shadow_rect.y += 2
            pygame.draw.rect(dialog_surface, (30, 30, 30, 150), shadow_rect, border_radius=5)
            
            # Corps du bouton
            button_rect = button['rect'].copy()
            button_rect.x -= self.dialog_rect.x
            button_rect.y -= self.dialog_rect.y
            button_color = self.button_hover_color if button['hover'] else self.button_color
            pygame.draw.rect(dialog_surface, button_color, button_rect, border_radius=5)
            
            # Bordure brillante du bouton
            if button['hover']:
                pygame.draw.rect(dialog_surface, (120, 120, 120, 255), button_rect, 2, border_radius=5)
            else:
                pygame.draw.rect(dialog_surface, (90, 90, 90, 255), button_rect, 2, border_radius=5)
            
            # Texte du bouton
            text_surface = button['text_surface_hover'] if button['hover'] else button['text_surface']
            text_rect = text_surface.get_rect(center=button_rect.center)
            dialog_surface.blit(text_surface, text_rect)
        
        # Dessiner le bouton Quitter
        button_relative_rect = pygame.Rect(
            self.quit_button.x - self.dialog_rect.x,
            self.quit_button.y - self.dialog_rect.y,
            self.quit_button.width,
            self.quit_button.height
        )
        
        # Effet d'ombre du bouton
        shadow_rect = button_relative_rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(dialog_surface, (30, 30, 30, 150), shadow_rect, border_radius=5)
        
        # Corps du bouton
        button_color = self.button_hover_color if self.quit_button_hover else self.button_color
        pygame.draw.rect(dialog_surface, button_color, button_relative_rect, border_radius=5)
        
        # Bordure brillante du bouton
        if self.quit_button_hover:
            pygame.draw.rect(dialog_surface, (120, 120, 120, 255), button_relative_rect, 2, border_radius=5)
        else:
            pygame.draw.rect(dialog_surface, (90, 90, 90, 255), button_relative_rect, 2, border_radius=5)
        
        # Texte du bouton
        text_to_use = self.quit_text_hover if self.quit_button_hover else self.quit_text
        text_rect = text_to_use.get_rect(center=button_relative_rect.center)
        dialog_surface.blit(text_to_use, text_rect)
        
        # Afficher la boîte de dialogue
        screen.blit(dialog_surface, self.dialog_rect)
