import pygame

# Constantes pour la position et l'apparence du rectangle de quête
QUEST_RECT_WIDTH = 300  # Largeur du rectangle
QUEST_RECT_HEIGHT = 40  # Hauteur du rectangle
QUEST_RECT_MARGIN = 10  # Marge par rapport au bord de l'écran
QUEST_RECT_COLOR = (50, 50, 50)  # Couleur de fond (gris foncé)
QUEST_TEXT_COLOR = (255, 255, 255)  # Couleur du texte (blanc)
QUEST_FONT_SIZE = 20  # Taille de la police

# Dictionnaire des textes de quêtes selon l'index
QUEST_TEXTS = {
    1: "Quête 1 : Parler au PNJ",
    2: "Quête 2 : Ramasser l'arme",
    4: "Quête 4 : Aller en (23,1)"
}

# Police pour le texte des quêtes (initialisée lors du premier appel)
_quest_font = None

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
    
    # Calculer la position X pour que le rectangle soit à droite
    screen_width = screen.get_width()
    quest_rect_x = screen_width - QUEST_RECT_WIDTH - QUEST_RECT_MARGIN
    
    # Dessiner le rectangle de fond
    quest_rect = pygame.Rect(quest_rect_x, QUEST_RECT_MARGIN, 
                           QUEST_RECT_WIDTH, QUEST_RECT_HEIGHT)
    pygame.draw.rect(screen, QUEST_RECT_COLOR, quest_rect)
    
    # Obtenir et dessiner le texte de la quête
    quest_text = QUEST_TEXTS.get(current_quest_index, "Quêtes terminées")
    print(f"Texte de quête affiché: {quest_text}")
    print("================================\n")
    
    text_surface = _quest_font.render(quest_text, True, QUEST_TEXT_COLOR)
    
    # Centrer le texte dans le rectangle
    text_rect = text_surface.get_rect(center=quest_rect.center)
    screen.blit(text_surface, text_rect)
