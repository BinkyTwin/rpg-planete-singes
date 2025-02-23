import pygame

# Système de quêtes simple avec variables d'état
# Chaque variable quest_X_done indique si la quête X est terminée

# Quête 1 : Devient True quand le PNJ disparaît
quest1_done = False

# Quête 2 : À mettre à True une fois les conditions de la deuxième quête remplies
quest2_done = False

# Quête 3 : Devient True quand la potion est ramassée
quest3_done = False

# Quête 4 : À mettre à True une fois les conditions de la quatrième quête remplies
quest4_done = False

# Indique quelle quête est actuellement active (de 1 à 4)
# À incrémenter manuellement quand une quête est terminée pour passer à la suivante
current_quest_index = 1

# Variable globale pour stocker la référence à la scène de jeu
_game_scene = None

# Variable pour le message de victoire
victory_message = None
victory_font = None

def set_game_scene(scene):
    """
    Enregistre la référence à la scène de jeu pour pouvoir afficher des messages.
    À appeler lors de l'initialisation de GameScene.
    """
    global _game_scene, victory_font
    _game_scene = scene
    # Initialiser la police pour le message de victoire
    victory_font = pygame.font.Font(None, 36)
    print(f"\n=== Enregistrement de la scène de jeu ===")
    print(f"Game scene définie: {_game_scene is not None}")
    print("=====================================\n")

def show_victory_message():
    """Affiche le message de victoire"""
    global victory_message
    if not victory_message and _game_scene:
        # Créer une surface semi-transparente pour le fond
        screen = _game_scene.screen
        victory_message = {
            'surface': pygame.Surface((screen.get_width(), screen.get_height())),
            'text': [
                "Félicitations ! Vous voici arrivé(e) à la tribu des Masqués.",
                "Vous apercevez votre famille de loin. Approchez et libérez-les."
            ]
        }
        victory_message['surface'].set_alpha(128)
        victory_message['surface'].fill((0, 0, 0))

def hide_victory_message():
    """Cache le message de victoire"""
    global victory_message
    victory_message = None

def handle_victory_event(event):
    """Gère les événements pour le message de victoire"""
    if victory_message and event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
            hide_victory_message()
            return True
    return False

def draw_victory_message(screen):
    """Dessine le message de victoire s'il est actif"""
    if victory_message and victory_font:
        # Dessiner le fond semi-transparent
        screen.blit(victory_message['surface'], (0, 0))
        
        # Calculer la position des lignes de texte
        total_height = len(victory_message['text']) * 40  # 40 pixels entre chaque ligne
        start_y = (screen.get_height() - total_height) // 2
        
        # Dessiner chaque ligne de texte
        for i, line in enumerate(victory_message['text']):
            text_surface = victory_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, start_y + i * 40))
            screen.blit(text_surface, text_rect)

def advance_quest_if_done():
    """
    Vérifie l'état des quêtes et met à jour current_quest_index automatiquement.
    """
    global current_quest_index
    
    print("\n=== État du système de quêtes ===")
    print(f"État des quêtes:")
    print(f"- quest1_done: {quest1_done}")
    print(f"- quest2_done: {quest2_done}")
    print(f"- quest3_done: {quest3_done}")
    print(f"- quest4_done: {quest4_done}")
    print(f"Index de quête actuel: {current_quest_index}")
    print(f"Game scene présente: {_game_scene is not None}")
    
    if quest1_done and current_quest_index == 1:
        current_quest_index = 2
        print("→ Progression: Passage à la quête 2")
    elif quest2_done and current_quest_index == 2:
        current_quest_index = 3
        print("→ Progression: Passage à la quête 3")
    elif quest3_done and current_quest_index == 3:
        current_quest_index = 4
        print("→ Progression: Passage à la quête 4")
    elif quest4_done and current_quest_index == 4:
        print("→ Toutes les quêtes sont terminées!")
        # Mettre current_quest_index à None pour indiquer la fin
        current_quest_index = None
        print("→ current_quest_index mis à None")
        
        # Afficher le message de victoire
        show_victory_message()
    
    print(f"Nouvel index de quête: {current_quest_index}")
    print("================================\n")

# Utilisation :
# 1. Dans votre code, importez ces variables : from game.quest_system import quest1_done, current_quest_index, etc.
# 2. Quand une quête est terminée :
#    - Mettez la variable correspondante à True (ex: quest1_done = True)
#    - Incrémentez current_quest_index pour passer à la quête suivante
# 3. Vous pouvez utiliser current_quest_index pour vérifier quelle quête est active
#    et adapter les dialogues ou événements en conséquence
