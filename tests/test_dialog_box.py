import unittest
import pygame
from game.ui.dialog_box import DialogBox

class TestDialogBox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    def test_dialog_creation(self):
        """Test la création d'une boîte de dialogue"""
        dialog = DialogBox(self.screen, "Test message")
        self.assertTrue(dialog.active)
        self.assertIsNone(dialog.result)
        self.assertEqual(dialog.message, "Test message")

    def test_dialog_yes_click(self):
        """Test le clic sur le bouton 'Oui'"""
        dialog = DialogBox(self.screen, "Test message")
        
        # Créer un événement de clic sur le bouton 'Oui'
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {
                'button': 1,
                'pos': (dialog.yes_button.centerx, dialog.yes_button.centery)
            }
        )
        
        # Vérifier que l'événement est correctement géré
        handled = dialog.handle_event(event)
        self.assertTrue(handled)
        self.assertTrue(dialog.result)
        self.assertFalse(dialog.active)

    def test_dialog_no_click(self):
        """Test le clic sur le bouton 'Non'"""
        dialog = DialogBox(self.screen, "Test message")
        
        # Créer un événement de clic sur le bouton 'Non'
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {
                'button': 1,
                'pos': (dialog.no_button.centerx, dialog.no_button.centery)
            }
        )
        
        # Vérifier que l'événement est correctement géré
        handled = dialog.handle_event(event)
        self.assertTrue(handled)
        self.assertFalse(dialog.result)
        self.assertFalse(dialog.active)

    def test_dialog_outside_click(self):
        """Test un clic en dehors des boutons"""
        dialog = DialogBox(self.screen, "Test message")
        
        # Créer un événement de clic en dehors des boutons
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {
                'button': 1,
                'pos': (0, 0)
            }
        )
        
        # Vérifier que l'événement n'est pas géré
        handled = dialog.handle_event(event)
        self.assertFalse(handled)
        self.assertTrue(dialog.active)
        self.assertIsNone(dialog.result)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
