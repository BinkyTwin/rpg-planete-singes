import unittest

from aide_message import AideMessage

class TestAideMessage(unittest.TestCase):
    def test_message_visible_when_near_and_not_in_dialogue(self):
        aide = AideMessage()
        visible = aide.update(player_near_pnj=True, in_dialogue=False)
        self.assertTrue(visible, 'Le message doit être visible quand le joueur est proche et pas en dialogue')

    def test_message_not_visible_when_in_dialogue(self):
        aide = AideMessage()
        visible = aide.update(player_near_pnj=True, in_dialogue=True)
        self.assertFalse(visible, 'Le message ne doit pas être visible en plein dialogue')

    def test_message_not_visible_when_far(self):
        aide = AideMessage()
        visible = aide.update(player_near_pnj=False, in_dialogue=False)
        self.assertFalse(visible, 'Le message ne doit pas être visible quand le joueur est loin')

if __name__ == '__main__':
    unittest.main()
