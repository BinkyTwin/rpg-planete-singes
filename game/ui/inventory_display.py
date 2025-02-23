import pygame
from game.items import ItemType  # Ajout de l'import manquant
import os

class InventoryDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.needs_update = False
        self.item_rects = []  # Liste des rectangles des items pour la détection des clics
        self.hovered_item = None  # Item survolé par la souris
        self.dialog_box = None  # Boîte de dialogue pour la confirmation
        self.pending_potion = None  # Potion en attente de confirmation
        
        # Polices
        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.header_font = pygame.font.SysFont("arial", 28, bold=True)
        self.item_font = pygame.font.SysFont("arial", 24)
        self.info_font = pygame.font.SysFont("arial", 20, italic=True)
        
        # Dimensions de l'inventaire
        self.width = int(screen.get_width() * 0.6)  # 60% de la largeur de l'écran
        self.height = int(screen.get_height() * 0.7)  # 70% de la hauteur de l'écran
        
        # Position de l'inventaire (centré)
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        
        # Couleurs
        self.bg_color = (20, 20, 30)  # Bleu très foncé
        self.border_color = (80, 80, 100)  # Bleu gris
        self.text_color = (220, 220, 220)  # Blanc cassé
        self.title_color = (255, 215, 0)  # Or
        self.equipped_color = (255, 215, 0)  # Or pour les objets équipés
        self.equipped_bg = (40, 40, 50)  # Fond légèrement plus clair pour l'item équipé
        self.info_color = (150, 150, 150)  # Gris pour les infos secondaires
        self.hover_color = (60, 60, 80)  # Couleur de survol
        
        # Taille des images d'items et espacement
        self.item_image_size = (48, 48)  # Images plus grandes
        self.item_padding = 15  # Espacement entre les items
        self.section_padding = 25  # Espacement entre les sections
        
        # Cache pour les images d'items
        self.item_images = {}
        
        # Dimensions pour la zone de défilement
        self.scroll_area_height = self.height - 150  # Hauteur disponible pour les items
        self.scroll_position = 0

    def toggle(self):
        """Affiche ou cache l'inventaire"""
        self.visible = not self.visible
        if self.visible:
            self.needs_update = True
        
    def hide(self):
        """Cache l'inventaire"""
        self.visible = False
        
    def load_item_image(self, image_path):
        """Charge et met en cache l'image d'un item"""
        if image_path not in self.item_images:
            try:
                base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                full_path = os.path.join(base_path, image_path)
                image = pygame.image.load(full_path)
                self.item_images[image_path] = pygame.transform.scale(image, self.item_image_size)
            except Exception as e:
                print(f"Erreur lors du chargement de l'image {image_path}: {e}")
                return None
        return self.item_images[image_path]

    def get_item_type_icon(self, item_type):
        """Retourne l'icône correspondant au type d'item"""
        if item_type.name == "WEAPON":
            return "⚔️"
        elif item_type.name == "ARMOR":
            return "🛡️"
        elif item_type.name == "POTION":
            return "🧪"
        return "📦"

    def update_hover(self, pos):
        """Met à jour l'item survolé"""
        self.hovered_item = None
        if not self.visible:
            return
            
        for item_rect, item in self.item_rects:
            if item_rect.collidepoint(pos):
                self.hovered_item = item
                break

    def get_item_use_text(self, item):
        """Retourne le texte d'action pour un item"""
        if item.item_type == ItemType.POTION:
            return "Cliquer pour utiliser"
        elif item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
            return "Cliquer pour équiper"
        return ""
        
    def show_confirmation_dialog(self, potion):
        """Affiche une boîte de dialogue de confirmation pour utiliser une potion avec gestion du retour à la ligne"""
        font = pygame.font.SysFont("arial", 20)  # Taille ajustée pour éviter les dépassements
        max_line_width = 260  # Largeur max du texte avant retour à la ligne

        # Découper le texte en plusieurs lignes si nécessaire
        text = f"Êtes-vous sûr de vouloir utiliser cette {potion.name} ?"
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] > max_line_width:
                lines.append(current_line.strip())  # Ajouter la ligne terminée
                current_line = word + " "  # Commencer une nouvelle ligne
            else:
                current_line = test_line

        lines.append(current_line.strip())  # Ajouter la dernière ligne

        # Définir la largeur et la hauteur dynamiquement
        box_width = 320  # Largeur fixe
        line_height = font.get_height() + 5
        box_height = 80 + (line_height * len(lines))  # Ajuster la hauteur en fonction du texte

        # Centrage de la boîte de dialogue
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2

        # Centrage vertical du texte
        text_start_y = box_y + 20

        self.dialog_box = {
            'rect': pygame.Rect(box_x, box_y, box_width, box_height),
            'text_lines': lines,
            'text_start_y': text_start_y,
            'yes_rect': pygame.Rect(box_x + 30, box_y + box_height - 50, 100, 40),
            'no_rect': pygame.Rect(box_x + box_width - 130, box_y + box_height - 50, 100, 40),
            'potion': potion,
            'font': font
        }


    def handle_dialog_click(self, pos, inventory, player):
        """Gère les clics sur la boîte de dialogue"""
        if not self.dialog_box:
            return False

        if self.dialog_box['yes_rect'].collidepoint(pos):
            potion = self.dialog_box['potion']
            # Soigner le joueur avant de supprimer la potion
            old_hp = player.hp
            player.hp = min(player.hp + potion.value, player.max_hp)
            print(f"DEBUG - Consommation potion: HP {old_hp} -> {player.hp} (max: {player.max_hp})")
            # Supprimer la potion de l'inventaire
            inventory.remove_item(potion)
            self.dialog_box = None
            self.pending_potion = None
            return True

        if self.dialog_box['no_rect'].collidepoint(pos):
            self.dialog_box = None
            self.pending_potion = None
            return True

        return False

    def handle_click(self, pos, inventory, player):
        """Gère les clics sur les items de l'inventaire"""
        if not self.visible:
            return False

        # Si une boîte de dialogue est active, gérer son clic en priorité
        if self.dialog_box:
            return self.handle_dialog_click(pos, inventory, player)

        # Vérifier les clics sur les items
        for item_rect, item in self.item_rects:
            if item_rect.collidepoint(pos):
                print(f"Clic sur l'item: {item.name}")
                
                if item.item_type == ItemType.POTION:
                    # Afficher la boîte de dialogue de confirmation
                    self.show_confirmation_dialog(item)
                    return True
                elif item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
                    # Équiper l'arme/armure
                    inventory.equip_item(item)
                    return True
                
                return True
        return False

    def render(self, inventory):
        """Affiche l'inventaire"""
        if not self.visible:
            return

        # Réinitialise la liste des rectangles des items
        self.item_rects = []

        # Met à jour l'item survolé
        mouse_pos = pygame.mouse.get_pos()
        self.update_hover(mouse_pos)

        # Fond semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Rectangle principal de l'inventaire avec bordure
        main_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, main_rect)
        pygame.draw.rect(self.screen, self.border_color, main_rect, 2)
        
        # Titre
        title = self.title_font.render("INVENTAIRE", True, self.title_color)
        title_x = self.x + (self.width - title.get_width()) // 2
        self.screen.blit(title, (title_x, self.y + 20))
        
        # Section équipement
        equipped_y = self.y + 80
        equipped_item = inventory.get_equipped_item()
        
        # Titre de la section équipement
        equip_header = self.header_font.render("Équipement actuel", True, self.text_color)
        self.screen.blit(equip_header, (self.x + 20, equipped_y))
        
        # Affichage de l'item équipé
        equipped_rect = pygame.Rect(self.x + 20, equipped_y + 40, self.width - 40, 70)
        pygame.draw.rect(self.screen, self.equipped_bg, equipped_rect)
        pygame.draw.rect(self.screen, self.equipped_color, equipped_rect, 2)
        
        if equipped_item:
            # Image de l'item équipé
            if hasattr(equipped_item, 'image_path'):
                item_image = self.load_item_image(equipped_item.image_path)
                if item_image:
                    self.screen.blit(item_image, (self.x + 30, equipped_y + 50))
            
            # Texte de l'item équipé
            equipped_text = f"{equipped_item.name} {self.get_item_type_icon(equipped_item.item_type)}"
            if hasattr(equipped_item, 'value'):
                if equipped_item.item_type.name == "WEAPON":
                    equipped_text += f" (Dégâts: {equipped_item.value})"
                elif equipped_item.item_type.name == "ARMOR":
                    equipped_text += f" (Défense: {equipped_item.value})"
            
            equipped_surface = self.header_font.render(equipped_text, True, self.equipped_color)
            self.screen.blit(equipped_surface, (self.x + 90, equipped_y + 60))
        else:
            # Message si rien n'est équipé
            no_equip_text = self.info_font.render("Aucun équipement sélectionné", True, self.info_color)
            text_x = self.x + (self.width - no_equip_text.get_width()) // 2
            self.screen.blit(no_equip_text, (text_x, equipped_y + 60))
        
        # Liste des objets
        items_y = equipped_y + 130
        items_header = self.header_font.render("Objets disponibles", True, self.text_color)
        self.screen.blit(items_header, (self.x + 20, items_y))
        
        # Zone de défilement pour les items
        items_start_y = items_y + 40
        current_y = items_start_y
        
        for item in inventory.get_items():
            # Rectangle de fond pour chaque item
            item_rect = pygame.Rect(self.x + 20, current_y, self.width - 40, 60)
            
            # Ajoute le rectangle et l'item à la liste pour la détection des clics
            self.item_rects.append((item_rect, item))
            
            # Fond différent selon l'état de l'item
            if item == self.hovered_item:
                pygame.draw.rect(self.screen, self.hover_color, item_rect)
            elif equipped_item and item.name == equipped_item.name:
                pygame.draw.rect(self.screen, self.equipped_bg, item_rect)
            else:
                pygame.draw.rect(self.screen, self.bg_color, item_rect)
            
            # Bordure selon l'état
            if equipped_item and item.name == equipped_item.name:
                pygame.draw.rect(self.screen, self.equipped_color, item_rect, 2)
            else:
                pygame.draw.rect(self.screen, self.border_color, item_rect, 1)
            
            # Image de l'item
            if hasattr(item, 'image_path'):
                item_image = self.load_item_image(item.image_path)
                if item_image:
                    self.screen.blit(item_image, (self.x + 30, current_y + 6))
            
            # Texte de l'item
            item_text = f"{item.name} {self.get_item_type_icon(item.item_type)}"
            if hasattr(item, 'value'):
                if item.item_type.name == "WEAPON":
                    item_text += f" (Dégâts: {item.value})"
                elif item.item_type.name == "ARMOR":
                    item_text += f" (Défense: {item.value})"
                elif item.item_type.name == "POTION":
                    item_text += f" (Soin: {item.value})"
            
            # Couleur du texte selon l'état
            text_color = self.equipped_color if equipped_item and item.name == equipped_item.name else self.text_color
            item_surface = self.item_font.render(item_text, True, text_color)
            self.screen.blit(item_surface, (self.x + 90, current_y + 17))
            
            # Affiche le texte d'action si l'item est survolé
            if item == self.hovered_item:
                action_text = self.get_item_use_text(item)
                if action_text:
                    action_surface = self.info_font.render(action_text, True, self.info_color)
                    self.screen.blit(action_surface, (self.x + self.width - 200, current_y + 20))
            
            current_y += 70

        # Afficher la boîte de dialogue si elle est active
        if self.dialog_box:
            # Fond semi-transparent
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            # Boîte de dialogue
            pygame.draw.rect(self.screen, self.bg_color, self.dialog_box['rect'])
            pygame.draw.rect(self.screen, self.border_color, self.dialog_box['rect'], 2)
            
            # Texte de la question
            y_offset = self.dialog_box['text_start_y']
            for line in self.dialog_box['text_lines']:
                text_surface = self.dialog_box['font'].render(line, True, self.text_color)
                self.screen.blit(text_surface, (self.dialog_box['rect'].x + 10, y_offset))
                y_offset += self.dialog_box['font'].get_height() + 5  # Décaler chaque ligne

            
            # Boutons
            for button, text in [
                (self.dialog_box['yes_rect'], "Oui"),
                (self.dialog_box['no_rect'], "Non")
            ]:
                pygame.draw.rect(self.screen, self.equipped_bg, button)
                pygame.draw.rect(self.screen, self.border_color, button, 2)
                text_surface = self.item_font.render(text, True, self.text_color)
                text_rect = text_surface.get_rect(center=button.center)
                self.screen.blit(text_surface, text_rect)
