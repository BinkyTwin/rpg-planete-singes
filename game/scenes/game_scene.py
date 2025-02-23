import pygame
import os
from .base_scene import BaseScene
from game.tiled_map import TiledMap
from game.pnj import PNJ
from game.pnj2 import PNJ2
from game.items import ITEMS, ItemType
from game.ui.dialog_box import DialogBox
from ..quest_ui import draw_current_quest, QuestJournal
from ..ui.health_display import HealthDisplay
from ..ui.inventory_display import InventoryDisplay
import game.quest_system as quest_system
from ..database import GameDatabase

class GameScene(BaseScene):
    def __init__(self, screen, game_state, display_manager=None):
        super().__init__(screen, game_state)
        self.screen = screen
        self.display_manager = display_manager
        
        # Enregistrer cette scène dans le système de quêtes pour les messages
        quest_system.set_game_scene(self)
        
        # Initialiser le journal des quêtes
        self.quest_journal = QuestJournal(screen)
        
        # Initialiser l'affichage de la santé
        self.health_display = HealthDisplay(screen)
        
        # Initialiser l'affichage de l'inventaire
        self.inventory_display = InventoryDisplay(screen)
        
        # Utilisation d'une police système avec taille de base
        self.base_font_size = 24
        self.base_title_size = 36
        self.update_fonts()
        
        # Obtenir le chemin de base du projet
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        map_path = os.path.join(self.base_path, "assets", "mapV3.tmx")
        self.tiled_map = TiledMap(map_path)
        self.collision_rects = self.tiled_map.get_collider_rects()
        
        # Chargement des items
        self.items = {}
        for item_name, item in ITEMS.items():
            if hasattr(item, 'image_path'):
                image_path = os.path.join(self.base_path, item.image_path)
                if os.path.exists(image_path):
                    item_image = pygame.image.load(image_path)
                    item_image = pygame.transform.scale(item_image, (self.tiled_map.tile_size, self.tiled_map.tile_size))
                    self.items[item_name] = {'item': item, 'image': item_image}
        
        # Position initiale du joueur
        if self.game_state.player:
            # Position en tuiles (192/32=6, 896/32=28)
            self.game_state.player.x = 6
            self.game_state.player.y = 28
            # Le rectangle sera mis à jour automatiquement dans la classe Player
            print(f"Position initiale - Tuiles: ({self.game_state.player.x}, {self.game_state.player.y}), Pixels: ({self.game_state.player.rect.x}, {self.game_state.player.rect.y})")
        
        # Initialisation du PNJ
        self.pnj = PNJ(position=(20, 27))
        if self.game_state.player:
            self.pnj.sync_faction(self.game_state.player)
        
        # Initialisation du PNJ2 et ajout au game_state
        self.pnj2 = PNJ2(position=(14, 10))
        self.game_state.pnj2 = self.pnj2  # Ajout du PNJ2 au game_state
        if self.game_state.player:
            self.pnj2.sync_faction(self.game_state.player)
        
        # Variables pour l'animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # Millisecondes entre chaque frame
        self.last_direction = "down"  # Direction par défaut
        
        # Variables pour la caméra
        self.camera_x = 0
        self.camera_y = 0
        
        # Variables pour la boîte de dialogue
        self.dialog_box = None
        self.current_item = None
        
        # Zone de combat
        self.combat_zone_positions = {
            (14, 9), (14, 11), (13, 10), (15, 10),
            (13, 9), (15, 9), (13, 11), (15, 11)
        }
        self.in_combat_zone = False
        self.combat_dialog_active = False
        
        # Initialisation de la base de données
        self.db = GameDatabase()
        
        # Temps de début de la partie
        self.start_time = pygame.time.get_ticks()

    def update_fonts(self):
        """Met à jour les polices en fonction de l'échelle"""
        if self.display_manager:
            font_size = self.display_manager.get_scaled_font_size(self.base_font_size)
            title_size = self.display_manager.get_scaled_font_size(self.base_title_size)
        else:
            font_size = self.base_font_size
            title_size = self.base_title_size
            
        self.font = pygame.font.SysFont("arial", font_size)
        self.title_font = pygame.font.SysFont("arial", title_size)

    def handle_event(self, event):
        """Gère les événements du jeu"""
        # Si le message de victoire est affiché, le gérer en priorité
        if quest_system.handle_victory_event(event):
            return
            
        # Si une boîte de dialogue est active, la gérer en priorité
        if self.dialog_box and self.dialog_box.active:
            if self.dialog_box.handle_event(event):
                print("→ Dialogue terminé, fermeture de la boîte")
                # Si un choix a été fait
                if self.current_item and self.dialog_box.result is not None:
                    print(f"DEBUG: Résultat du dialogue: {self.dialog_box.result}")
                    if self.dialog_box.result:
                        # Ajouter l'item à l'inventaire
                        if self.add_item_to_inventory(self.current_item):
                            print(f"Item {self.current_item.name} ajouté à l'inventaire!")
                            
                            # Si c'est l'arme qui est ramassée, mettre à jour la quête 2
                            if self.current_item.name in ["M16", "m16"]:  
                                print("Arme (M16) ramassée - Mise à jour de la quête 2")
                                quest_system.quest2_done = True
                                quest_system.advance_quest_if_done()
                            # Si c'est une potion qui est ramassée, mettre à jour la quête 3
                            elif self.current_item.item_type.name == "POTION":
                                print("Potion ramassée - Mise à jour de la quête 3")
                                quest_system.quest3_done = True
                                quest_system.advance_quest_if_done()
                        else:
                            print(f"DEBUG: Impossible d'ajouter {self.current_item.name} à l'inventaire (plein?)")
                            self.current_item.collected = False  # Remettre l'item comme non collecté
                    else:
                        print(f"DEBUG: {self.current_item.name} laissé sur place.")
                self.dialog_box = None
                self.current_item = None
            return None

        # Gestion des clics dans l'inventaire
        if event.type == pygame.MOUSEBUTTONDOWN and self.inventory_display.visible:
            if self.inventory_display.handle_click(event.pos, self.game_state.player.inventory, self.game_state.player):
                return None  # Empêche la propagation de l'événement

        if event.type == pygame.KEYDOWN:
            print(f"DEBUG: Appui sur la touche {event.key}")
            if event.key == pygame.K_ESCAPE:
                # Si l'inventaire est visible, le fermer
                if self.inventory_display.visible:
                    self.inventory_display.hide()
                    return None
                # Si le journal des quêtes est visible, le fermer
                if self.quest_journal.visible:
                    self.quest_journal.hide()
                    return None
                return 'menu'
            # Gestion du dialogue avec le PNJ
            elif event.key == pygame.K_e:
                if self.pnj.is_visible and self.game_state.player and self.pnj.can_trigger_dialogue(self.game_state.player):
                    if not self.pnj.is_in_dialogue:
                        message = self.pnj.start_dialogue()
                        if message:
                            print(f"PNJ dit : {message}")
                else:
                    # Si pas de dialogue avec PNJ, vérifier les items
                    self.handle_item_interaction()

            # Gestion du passage au message suivant avec ESPACE
            elif event.key == pygame.K_SPACE and self.pnj.is_in_dialogue:
                message = self.pnj.next_message()
                if message:
                    print(f"PNJ dit : {message}")
            # Gestion du journal des quêtes avec la touche J
            elif event.key == pygame.K_j:
                self.quest_journal.toggle()
            # Gestion de l'inventaire avec la touche I
            elif event.key == pygame.K_i:
                self.inventory_display.toggle()
            # Gestion du mouvement du joueur
            elif event.key in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]:
                self.handle_player_movement(event.key)
            # Gestion de l'interaction avec les items
            elif event.key == pygame.K_e:
                self.handle_item_interaction()
                
        # Si la fenêtre est redimensionnée, mettre à jour les polices
        elif event.type == pygame.VIDEORESIZE:
            self.update_fonts()
            
        return None

    def handle_player_movement(self, key):
        print(f"=== DEBUG: Mouvement du joueur avec la touche {key} ===")
        if self.game_state.player:
            dx, dy = 0, 0
            if key == pygame.K_z:
                dy = -1
                self.last_direction = "up"
            elif key == pygame.K_s:
                dy = 1
                self.last_direction = "down"
            elif key == pygame.K_q:
                dx = -1
                self.last_direction = "left"
            elif key == pygame.K_d:
                dx = 1
                self.last_direction = "right"
            
            # Calcul de la nouvelle position en tuiles
            new_x = max(0, min(self.tiled_map.width - 1, self.game_state.player.x + dx))
            new_y = max(0, min(self.tiled_map.height - 1, self.game_state.player.y + dy))
            
            # Debug: Afficher les coordonnées avant mouvement
            print(f"Avant mouvement - Tuiles: ({self.game_state.player.x}, {self.game_state.player.y}), Pixels: ({self.game_state.player.rect.x}, {self.game_state.player.rect.y})")
            
            # Création d'un rectangle pour le joueur à la nouvelle position
            new_player_rect = pygame.Rect(
                new_x * self.tiled_map.tile_size,
                new_y * self.tiled_map.tile_size,
                self.tiled_map.tile_size,
                self.tiled_map.tile_size
            )
            
            # Vérification des collisions
            can_move = True
            for collision_rect in self.collision_rects:
                if new_player_rect.colliderect(collision_rect):
                    can_move = False
                    break
            
            # Mise à jour de la position si aucune collision
            if can_move:
                self.game_state.player.x = new_x
                self.game_state.player.y = new_y
                self.game_state.player.rect.x = new_x * self.tiled_map.tile_size
                self.game_state.player.rect.y = new_y * self.tiled_map.tile_size
                
                # Debug: Afficher les coordonnées après mouvement
                print(f"Après mouvement - Tuiles: ({self.game_state.player.x}, {self.game_state.player.y}), Pixels: ({self.game_state.player.rect.x}, {self.game_state.player.rect.y})")
                
                # Mettre à jour l'animation
                self.animation_timer = pygame.time.get_ticks()
                self.animation_frame = (self.animation_frame + 1) % 4
                
    def handle_item_interaction(self):
        """Gère l'interaction avec les items lorsque la touche E est pressée"""
        print("=== DEBUG: Interaction avec les items ===")
        if not self.game_state.player or self.dialog_box:
            return

        # Obtenir la position actuelle du joueur en tuiles
        player_pos = (self.game_state.player.x, self.game_state.player.y)
        
        # Vérifier tous les items non collectés
        for item_name, item_data in list(self.items.items()):  
            item = item_data['item']
            if not item.collected and hasattr(item, 'position') and item.position == player_pos:
                self.current_item = item
                # Créer une boîte de dialogue pour confirmer la collecte
                stats_text = None
                if item.item_type == ItemType.WEAPON:
                    stats_text = f"Dégâts: {item.value}"
                elif item.item_type == ItemType.ARMOR:
                    stats_text = f"Bonus HP: +{item.value}"
                elif item.item_type == ItemType.POTION:
                    stats_text = f"Restaure {item.value} HP"

                self.dialog_box = DialogBox(
                    self.screen,
                    f"Voulez-vous ramasser {item.name} ?",
                    stats_text=stats_text
                )
                break

    def add_item_to_inventory(self, item):
        """Ajoute un item à l'inventaire du joueur"""
        print("=== DEBUG: Tentative d'ajout d'item à l'inventaire ===")
        print(f"Item name: {item.name}")
        print(f"Items actuels: {list(self.items.keys())}")
        
        if not self.game_state.player or not hasattr(self.game_state.player, 'inventory'):
            print("DEBUG: Pas de joueur ou d'inventaire")
            return False

        if self.game_state.player.inventory.add_item(item):
            print(f"DEBUG: {item.name} ajouté à l'inventaire avec succès")
            # Marquer l'item comme collecté
            item.collected = True
            print(f"DEBUG: Item {item.name} marqué comme collecté")
            
            # Sauvegarder l'inventaire dans la base de données
            try:
                player_data = self.db.load_player(self.game_state.player.name)
                if player_data:
                    self.db.save_inventory(player_data['id'], self.game_state.player.inventory)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde de l'inventaire : {e}")
            
            # Forcer une mise à jour immédiate de l'affichage de l'inventaire
            if self.inventory_display and self.inventory_display.visible:
                self.inventory_display.needs_update = True
            
            return True
        else:
            print("DEBUG: Inventaire plein!")
            return False

    def handle_movement(self, keys):
        """Gère le mouvement du joueur"""
        print("=== DEBUG: Mouvement du joueur ===")
        if not self.game_state.player:
            return

        # Sauvegarde de l'ancienne position pour le debug
        old_x = self.game_state.player.x
        old_y = self.game_state.player.y
        old_rect_x = self.game_state.player.rect.x
        old_rect_y = self.game_state.player.rect.y

        print(f"Avant mouvement - Tuiles: ({old_x}, {old_y}), Pixels: ({old_rect_x}, {old_rect_y})")
        
        # Vérification des touches pressées et appel de handle_player_movement pour chaque direction
        if keys[pygame.K_z]:
            self.handle_player_movement(pygame.K_z)
        if keys[pygame.K_s]:
            self.handle_player_movement(pygame.K_s)
        if keys[pygame.K_q]:
            self.handle_player_movement(pygame.K_q)
        if keys[pygame.K_d]:
            self.handle_player_movement(pygame.K_d)

        print(f"Après mouvement - Tuiles: ({self.game_state.player.x}, {self.game_state.player.y}), Pixels: ({self.game_state.player.rect.x}, {self.game_state.player.rect.y})")

    def update(self):
        # Mettre à jour les animations des items
        for item_data in self.items.values():
            item = item_data['item']
            if item.is_animating:
                item.update_animation()

        # Vérifier si le joueur est dans la zone de combat
        if self.game_state.player:
            # Utiliser directement les coordonnées en tuiles du joueur
            player_pos = (self.game_state.player.x, self.game_state.player.y)
            was_in_combat_zone = self.in_combat_zone
            self.in_combat_zone = player_pos in self.combat_zone_positions
            
            print(f"DEBUG - Position du joueur: {player_pos}")
            print(f"DEBUG - Dans la zone de combat: {self.in_combat_zone}")
            print(f"DEBUG - Combat dialog active: {self.combat_dialog_active}")
            print(f"DEBUG - Était dans la zone: {was_in_combat_zone}")
            print(f"DEBUG - Positions de la zone de combat: {self.combat_zone_positions}")
            
            # Si le joueur entre dans la zone de combat
            if self.in_combat_zone and (not was_in_combat_zone or not self.combat_dialog_active):
                print("DEBUG - Conditions pour afficher le message remplies")
                if not self.game_state.temp_message:  # Vérifier si le message n'est pas déjà défini
                    self.game_state.temp_message = "Vous êtes dans la zone de combat !\nPréparez vous !"
                    self.combat_dialog_active = True
                    print("DEBUG - Changement vers la scène de message")
                    return 'message'
            # Si le joueur sort de la zone de combat
            elif not self.in_combat_zone and was_in_combat_zone:
                print("DEBUG - Le joueur sort de la zone de combat")
                self.combat_dialog_active = False
                self.game_state.temp_message = None

        """Met à jour l'état du jeu"""
        if self.game_state.player:
            # Debug: Position actuelle
            print(f"\n=== Vérification position finale ===")
            print(f"Position actuelle en tuiles: ({self.game_state.player.x}, {self.game_state.player.y})")
            print(f"Quest4 done? {quest_system.quest4_done}")
            
            # Définir la zone de déclenchement de la quête finale
            # Un ensemble de tuples (x,y) où la quête peut être validée
            zone_finale = {(21,1), (22,1), (23,1), (24,1)}
            
 
            # Vérifier si le joueur est dans la zone finale
            # et si la quête 4 n'est pas encore terminée
            position_joueur = (int(self.game_state.player.x), int(self.game_state.player.y))
            if position_joueur in zone_finale and not quest_system.quest4_done:
                print(f"→ Position finale {position_joueur} détectée (zone valide: {zone_finale})!")
                print("→ Première fois dans la zone finale")
                quest_system.quest4_done = True
                print("→ quest4_done mis à True")
                quest_system.advance_quest_if_done()
                print("→ advance_quest_if_done appelé")
            
            # Mise à jour de la position de la caméra
            self.camera_x = -self.game_state.player.x * self.tiled_map.tile_size + self.screen.get_width() // 2
            self.camera_y = -self.game_state.player.y * self.tiled_map.tile_size + self.screen.get_height() // 2
            # Mettre à jour l'animation du PNJ2
            if hasattr(self, 'pnj2') and self.pnj2.is_visible:
                self.pnj2.animation_frame = (self.pnj2.animation_frame + 1) % 4

        # Vérifier l'interaction avec le PNJ
        if self.game_state.player:
            # Mise à jour du PNJ1
            if self.pnj.is_visible:
                self.pnj.can_trigger_dialogue(self.game_state.player)
                
            # Mise à jour du PNJ2
            if hasattr(self, 'pnj2') and self.pnj2.is_visible:
                self.pnj2.can_trigger_dialogue(self.game_state.player)

    def update_camera(self):
        """Met à jour la position de la caméra pour suivre le joueur"""
        print("=== DEBUG: Mise à jour de la caméra ===")
        if not self.game_state.player:
            return
            
        # Obtenir le centre de l'écran
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        
        # Calculer la position cible de la caméra (centrée sur le joueur)
        self.camera_x = self.game_state.player.rect.x - screen_center_x
        self.camera_y = self.game_state.player.rect.y - screen_center_y
        
        # Limiter la caméra aux bords de la carte
        self.camera_x = max(0, min(self.camera_x, self.tiled_map.pixel_width - self.screen.get_width()))
        self.camera_y = max(0, min(self.camera_y, self.tiled_map.pixel_height - self.screen.get_height()))
        
        print(f"Camera position: ({self.camera_x}, {self.camera_y})")

    def render(self, screen):
        """Rendu de la scène de jeu"""
        print("=== DEBUG: Rendu de la scène de jeu ===")
        # Effacer l'écran
        #screen.fill((0, 0, 0))
        
        if self.tiled_map and self.game_state.player:
            # Mettre à jour la position de la caméra
            self.update_camera()
            
            # Dessiner la carte avec l'offset de la caméra
            self.tiled_map.render(screen, (-self.camera_x, -self.camera_y))
            
            # Afficher les items non collectés ou en cours d'animation
            print("\n=== DEBUG: Rendu des items ===")
            print(f"Nombre d'items à afficher: {len(self.items)}")
            for item_name, item_data in list(self.items.items()):
                item = item_data['item']
                if not item.collected:
                    print(f"DEBUG: Affichage de l'item {item_name} (collected: {item.collected}, animating: {item.is_animating})")
                    item_x = item.position[0] * self.tiled_map.tile_size - self.camera_x
                    item_y = item.position[1] * self.tiled_map.tile_size - self.camera_y
                    
                    # Si l'item est en cours d'animation, appliquer l'effet de fade out
                    if item.is_animating and item.animation:
                        surface_to_render = item.animation.apply_to_surface(item_data['image'])
                    else:
                        surface_to_render = item_data['image']
                        
                    screen.blit(surface_to_render, (item_x, item_y))
                else:
                    print(f"DEBUG: Item {item_name} est collecté, on ne l'affiche pas")

            # Afficher les coordonnées du joueur
            padding = 10
            debug_text = f"Tuiles: ({int(self.game_state.player.x)}, {int(self.game_state.player.y)}) | Pixels: ({int(self.game_state.player.rect.x)}, {int(self.game_state.player.rect.y)})"
            text_surface = self.font.render(debug_text, True, (255, 255, 255))
            
            bg_surface = pygame.Surface((text_surface.get_width() + padding * 2, text_surface.get_height() + padding * 2))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(128)
            screen.blit(bg_surface, (0, 0))
            screen.blit(text_surface, (padding, padding))
            
            # Affichage du joueur avec son sprite animé
            current_sprite = self.game_state.player.sprites[self.last_direction][self.animation_frame]
            
            # Position du joueur relative à la caméra
            screen_x = self.game_state.player.rect.x - self.camera_x
            screen_y = self.game_state.player.rect.y - self.camera_y
            
            # Ajuster la position pour centrer le sprite plus grand sur la tile
            sprite_offset_x = (self.game_state.player.sprite_size - self.tiled_map.tile_size) // 2
            sprite_offset_y = (self.game_state.player.sprite_size - self.tiled_map.tile_size) // 2
            
            player_pos = (
                screen_x - sprite_offset_x,
                screen_y - sprite_offset_y
            )
            
            # Afficher le sprite du joueur
            screen.blit(current_sprite, player_pos)

            # Afficher le PNJ s'il est visible
            if self.pnj.is_visible:
                self.pnj.render(screen, self.camera_x, self.camera_y)
            # Debug: Affichage du second PNJ
            if hasattr(self, 'pnj2') and self.pnj2.is_visible:
                print("DEBUG: Affichage du PNJ2")
                # Calculer la position de rendu attendue pour PNJ2
                if hasattr(self.pnj2, 'position'):
                    coords = self.pnj2.position
                elif hasattr(self.pnj2, 'x') and hasattr(self.pnj2, 'y'):
                    coords = (self.pnj2.x, self.pnj2.y)
                else:
                    coords = (0, 0)

                pnj2_screen_x = coords[0] * self.tiled_map.tile_size - self.camera_x
                pnj2_screen_y = coords[1] * self.tiled_map.tile_size - self.camera_y
                print(f"DEBUG: PNJ2 position de rendu attendue: ({pnj2_screen_x}, {pnj2_screen_y})")
                self.pnj2.render(screen, self.camera_x, self.camera_y)

            # Afficher le message directif si le joueur est proche du PNJ
            if self.pnj and self.pnj.is_visible and self.game_state.player and self.pnj.can_trigger_dialogue(self.game_state.player):
                directive_text = "Cliquez sur E pour discuter avec le pnj"
                directive_font = pygame.font.SysFont("arial", 24)
                directive_surface = directive_font.render(directive_text, True, (255, 255, 255))
                # Positionner le message en bas à gauche de l'écran
                screen.blit(directive_surface, (20, self.screen.get_height() - 60))

            # Afficher le dialogue du PNJ si actif
            if self.pnj.dialogue_system.is_dialogue_active:
                message = self.pnj.dialogue_system.get_current_message()
                if message:
                    # Créer une surface pour le texte du dialogue
                    text_surface = self.font.render(message, True, (255, 255, 255))
                    
                    # Créer un fond semi-transparent
                    padding = 20
                    bg_surface = pygame.Surface((text_surface.get_width() + padding * 2, text_surface.get_height() + padding * 2))
                    bg_surface.fill((0, 0, 0))
                    bg_surface.set_alpha(192)
                    
                    # Position du dialogue en bas de l'écran
                    dialog_x = (screen.get_width() - bg_surface.get_width()) // 2
                    dialog_y = screen.get_height() - bg_surface.get_height() - 20
                    
                    # Afficher le fond et le texte
                    screen.blit(bg_surface, (dialog_x, dialog_y))
                    screen.blit(text_surface, (dialog_x + padding, dialog_y + padding))

            # Afficher la boîte de dialogue si elle est active
            if self.dialog_box and self.dialog_box.active:
                self.dialog_box.render()

            # Dessiner le rectangle de quête en dernier pour qu'il soit au-dessus de tout
            draw_current_quest(screen, quest_system.current_quest_index)
            
            # Afficher le journal des quêtes s'il est visible
            self.quest_journal.render(quest_system)
            
            # Afficher l'inventaire s'il est visible
            if self.game_state.player and hasattr(self.game_state.player, 'inventory'):
                self.inventory_display.render(self.game_state.player.inventory)
            
            # Afficher le niveau de vie du joueur
            if self.game_state.player:
                self.health_display.render(self.game_state.player.hp)
            
            # Dessiner le message de victoire s'il est actif
            quest_system.draw_victory_message(screen)

    def test_coordinates(self):
        """Test du système de coordonnées"""
        # Coordonnées de test
        test_screen_x, test_screen_y = 24, 343
        
        # Test 1: Conversion écran -> grille
        grid_x, grid_y = self.screen_to_grid(test_screen_x, test_screen_y)
        print(f"Test 1: Screen ({test_screen_x}, {test_screen_y}) -> Grid ({grid_x}, {grid_y})")
        
        # Test 2: Conversion grille -> écran
        back_screen_x, back_screen_y = self.grid_to_screen(grid_x, grid_y)
        print(f"Test 2: Grid ({grid_x}, {grid_y}) -> Screen ({back_screen_x}, {back_screen_y})")
        
        # Test 3: Vérification de la cohérence
        if abs(test_screen_x - back_screen_x) > 32 or abs(test_screen_y - back_screen_y) > 32:
            print("ERREUR: La conversion aller-retour n'est pas cohérente!")

    def screen_to_grid(self, screen_x, screen_y):
        """Convertit les coordonnées écran en coordonnées grille"""
        # Taille des tuiles
        tile_size = self.tiled_map.tile_size
        
        # Position de la caméra (centre de l'écran)
        camera_x = self.screen.get_width() // 2
        camera_y = self.screen.get_height() // 2
        
        # Position relative à la caméra
        rel_x = screen_x - camera_x
        rel_y = screen_y - camera_y
        
        # Conversion en coordonnées grille
        grid_x = rel_x // tile_size
        grid_y = rel_y // tile_size
        
        return grid_x, grid_y
        
    def grid_to_screen(self, grid_x, grid_y):
        """Convertit les coordonnées grille en coordonnées écran"""
        # Taille des tuiles
        tile_size = self.tiled_map.tile_size
        
        # Position de la caméra (centre de l'écran)
        camera_x = self.screen.get_width() // 2
        camera_y = self.screen.get_height() // 2
        
        # Conversion en coordonnées écran
        screen_x = (grid_x * tile_size) + camera_x
        screen_y = (grid_y * tile_size) + camera_y
        
        return screen_x, screen_y

    def show_final_quest_message(self):
        """Affiche le message de fin quand toutes les quêtes sont terminées"""
        print("\n=== Affichage message final ===")
        print(f"État actuel de la boîte de dialogue: {self.dialog_box}")
        
        message = (
            "Félicitations ! Vous voici arrivé(e) à la tribu des Masqués.\n"
            "Vous apercevez votre famille de loin. Approchez et libérez-les."
        )
        print("→ Création de la boîte de dialogue")
        # Utiliser la même boîte de dialogue que pour les autres interactions
        self.dialog_box = DialogBox(
            message,
            self.screen,
            self.font,
            is_choice_dialog=False  # Pas de choix, juste un message à fermer
        )
        print("→ Boîte de dialogue créée et active")
        print("→ Appuyez sur Espace ou Échap pour fermer")
        print("→ État final de la boîte de dialogue:", self.dialog_box is not None)
        print("=====================================\n")

    def save_player_lifespan(self):
        """Sauvegarde la durée de vie du joueur"""
        if self.game_state.player:
            try:
                # Calculer la durée en secondes
                duration = (pygame.time.get_ticks() - self.start_time) // 1000
                
                # Charger les données du joueur
                player_data = self.db.load_player(self.game_state.player.name)
                if player_data:
                    # Sauvegarder la durée de vie
                    self.db.save_lifespan(player_data['id'], duration)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde de la durée de vie : {e}")

    def __del__(self):
        """Ferme la connexion à la base de données et sauvegarde la durée de vie"""
        self.save_player_lifespan()
        if hasattr(self, 'db'):
            self.db.close()