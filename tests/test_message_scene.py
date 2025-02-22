import pygame
import pytest
from game.scenes.message_scene import MessageScene


def fake_dialogue_getter():
    # Pour tester, retourne un message incrémenté qui simule le prochain message du dialogue
    return "Message suivant"


def test_space_key_progression():
    # Initialiser pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    initial_message = "Bonjour PNJ"
    # Créer une instance de MessageScene avec fake_dialogue_getter
    ms = MessageScene(screen, game_state=None, message=initial_message, display_manager=None, dialogue_getter=fake_dialogue_getter)
    
    # Simuler un événement KEYDOWN pour la barre d'espace
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    result = ms.handle_event(event)
    
    # Vérifier que le message a été mis à jour
    assert ms.message == "Message suivant"
    # Ne doit pas renvoyer de changement de scène
    assert result is None


if __name__ == "__main__":
    pytest.main(["-q"])
