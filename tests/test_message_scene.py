import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import pytest
from game.scenes.message_scene import MessageScene
import unittest


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


# Classe game_state fictive
class DummyGameState:
    pass

# Gestionnaire d'affichage fictif pour conserver la taille de police d'origine
class DummyDisplayManager:
    def get_scaled_font_size(self, size):
        return size

class TestMessageSceneDefeatButtonsCentering(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Créer une surface factice qui sert d'écran
        self.screen = pygame.Surface((800, 600))
        self.dummy_state = DummyGameState()
        # On attribue des objets fictifs pour player et pnj2
        self.dummy_state.player = object()
        self.dummy_state.pnj2 = object()
        # Instanciation de MessageScene avec un message de test
        self.scene = MessageScene(self.screen, self.dummy_state, "Test message", display_manager=DummyDisplayManager())

    def test_defeat_buttons_centering(self):
        # Simuler l'état de défaite
        self.scene.is_defeated = True
        # Forcer la mise à jour des dimensions de la boîte de dialogue
        self.scene.update_dialog_dimensions()

        defeat_buttons = self.scene.defeat_buttons
        self.assertTrue(len(defeat_buttons) > 0, "Les boutons de défaite devraient exister")

        button_width = 120
        button_height = 35
        button_spacing = 10
        defeat_count = len(defeat_buttons)
        expected_total_width = defeat_count * button_width + (defeat_count - 1) * button_spacing
        expected_start_x = self.scene.dialog_rect.centerx - expected_total_width // 2

        # Vérifier que chaque bouton est positionné correctement
        for i, button in enumerate(defeat_buttons):
            expected_x = expected_start_x + i * (button_width + button_spacing)
            self.assertEqual(button['rect'].x, expected_x, f"Bouton {i} : x incorrect")
            expected_y = self.scene.dialog_rect.bottom - button_height - 60
            self.assertEqual(button['rect'].y, expected_y, f"Bouton {i} : y incorrect")


if __name__ == "__main__":
    pytest.main(["-q"])
    unittest.main()
