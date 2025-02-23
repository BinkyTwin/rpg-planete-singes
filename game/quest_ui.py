import pygame

# Constantes pour la position et l'apparence du rectangle de quête
QUEST_RECT_WIDTH = 300  # Largeur du rectangle
QUEST_RECT_HEIGHT = 40  # Hauteur du rectangle
QUEST_RECT_MARGIN = 10  # Marge par rapport au bord de l'écran
QUEST_RECT_COLOR = (50, 50, 50)  # Couleur de fond (gris foncé)
QUEST_TEXT_COLOR = (255, 255, 255)  # Couleur du texte (blanc)
QUEST_FONT_SIZE = 20  # Taille de la police

# Constantes pour le panneau des touches
SHORTCUT_RECT_HEIGHT = 140  # Augmentation de la hauteur pour accommoder la nouvelle ligne
SHORTCUT_RECT_COLOR = (50, 50, 50, 192)  # Couleur de fond avec transparence
SHORTCUT_TEXT_COLOR = (255, 255, 255)  # Couleur du texte
SHORTCUT_FONT_SIZE = 18  # Taille de la police

# Dictionnaire des textes de quêtes selon l'index
QUEST_TEXTS = {
    1: "Quête 1 : Parler au PNJ !",
    2: "Quête 2 : Ramasser l'arme !",
    3: "Quête 3 : Ramasser la potion !",
    4: "Quête 4 : allez au bout de la montagne ! "
}

# Police pour le texte des quêtes (initialisée lors du premier appel)
_quest_font = None

class QuestJournal:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.font = pygame.font.SysFont("arial", 28)
        self.title_font = pygame.font.SysFont("arial", 36)
        
        # Dimensions du journal
        self.width = int(screen.get_width() * 0.6)  # 60% de la largeur de l'écran
        self.height = int(screen.get_height() * 0.7)  # 70% de la hauteur de l'écran
        
        # Position du journal (centré)
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        
        # Couleurs
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.title_color = (200, 200, 255)
        
    def toggle(self):
        """Affiche ou cache le journal"""
        self.visible = not self.visible
        
    def hide(self):
        """Cache le journal"""
        self.visible = False
        
    def render(self, quest_system):
        """Affiche le journal des quêtes"""
        if not self.visible:
            return
            
        # Fond semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill(self.bg_color)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Rectangle du journal
        journal_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, journal_rect)
        pygame.draw.rect(self.screen, self.text_color, journal_rect, 2)
        
        # Titre
        title = self.title_font.render("JOURNAL DES QUÊTES", True, self.title_color)
        title_x = self.x + (self.width - title.get_width()) // 2
        self.screen.blit(title, (title_x, self.y + 20))
        
        # Liste des quêtes
        y_offset = self.y + 80
        line_height = 40
        
        quests = [
            ("Quête 1: Parler au PNJ", quest_system.quest1_done),
            ("Quête 2: Ramasser l'arme", quest_system.quest2_done),
            ("Quête 3: Ramasser la potion", quest_system.quest3_done),
            ("Quête 4: Atteindre la zone finale", quest_system.quest4_done)
        ]
        
        for quest_text, is_done in quests:
            status = "✓ Terminée" if is_done else "➤ En cours"
            color = (100, 255, 100) if is_done else (255, 255, 255)
            
            # Texte de la quête
            quest_surface = self.font.render(f"{quest_text} - {status}", True, color)
            self.screen.blit(quest_surface, (self.x + 30, y_offset))
            y_offset += line_height

def draw_shortcut_panel(screen):
    """
    Dessine le panneau des touches de raccourci en bas du rectangle de quête.
    """
    global _quest_font
    
    # Initialisation de la police si pas encore fait
    if _quest_font is None:
        _quest_font = pygame.font.Font(None, SHORTCUT_FONT_SIZE)
    
    # Position du panneau (en dessous du rectangle de quête)
    panel_x = screen.get_width() - QUEST_RECT_WIDTH - QUEST_RECT_MARGIN
    panel_y = QUEST_RECT_MARGIN + QUEST_RECT_HEIGHT + 5  # 5 pixels de marge entre les rectangles
    
    # Créer la surface semi-transparente
    shortcut_panel = pygame.Surface((QUEST_RECT_WIDTH, SHORTCUT_RECT_HEIGHT), pygame.SRCALPHA)
    shortcut_panel.fill(SHORTCUT_RECT_COLOR)
    
    # Liste des raccourcis à afficher
    shortcuts = [
        "Touches de raccourci :",
        "J : Journal de quêtes",
        "I : Inventaire",
        "E : Parler au PNJ",
        "E : Ramasser une arme",
        "E : Ramasser une potion",
        "N'oubliez pas d'équiper votre arme" 
    ]
    
    # Afficher chaque ligne de texte
    y_offset = 5
    for text in shortcuts:
        text_surface = _quest_font.render(text, True, SHORTCUT_TEXT_COLOR)
        text_x = (QUEST_RECT_WIDTH - text_surface.get_width()) // 2
        shortcut_panel.blit(text_surface, (text_x, y_offset))
        y_offset += 20
    
    # Afficher le panneau
    screen.blit(shortcut_panel, (panel_x, panel_y))

def draw_current_quest(screen, current_quest_index):
    """
    Dessine un rectangle contenant le texte de la quête active.
    """
    global _quest_font
    
    print("\n=== Rendu du rectangle de quête ===")
    print(f"Index de quête reçu: {current_quest_index}")
    
    # Initialisation de la police si pas encore fait
    if _quest_font is None:
        _quest_font = pygame.font.Font(None, QUEST_FONT_SIZE)
    
    # Récupérer le texte de la quête actuelle
    quest_text = QUEST_TEXTS.get(current_quest_index, "")
    if not quest_text:
        return
    
    # Créer la surface de texte
    text_surface = _quest_font.render(quest_text, True, QUEST_TEXT_COLOR)
    
    # Position du rectangle (en haut à droite)
    rect_x = screen.get_width() - QUEST_RECT_WIDTH - QUEST_RECT_MARGIN
    rect_y = QUEST_RECT_MARGIN
    
    # Dessiner le rectangle semi-transparent
    quest_rect = pygame.Surface((QUEST_RECT_WIDTH, QUEST_RECT_HEIGHT))
    quest_rect.fill(QUEST_RECT_COLOR)
    quest_rect.set_alpha(192)  # 75% opaque
    screen.blit(quest_rect, (rect_x, rect_y))
    
    # Centrer le texte dans le rectangle
    text_x = rect_x + (QUEST_RECT_WIDTH - text_surface.get_width()) // 2
    text_y = rect_y + (QUEST_RECT_HEIGHT - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))
    
    # Dessiner le panneau des raccourcis
    draw_shortcut_panel(screen)
    
    print(f"Rectangle de quête dessiné avec le texte: {quest_text}")
