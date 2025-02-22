import time
import unittest

from dialogue_system import DialogueManager

class TestDialogueManager(unittest.TestCase):
    def test_dialogue_flow_time_enforcement(self):
        messages = ["Message 1", "Message 2", "Au revoir"]
        callback_triggered = False

        def on_end():
            nonlocal callback_triggered
            callback_triggered = True

        dm = DialogueManager(messages, delay=0.5, on_end=on_end)

        # Initial message
        self.assertEqual(dm.current_message(), "Message 1")
        now = time.time()

        # Without delay, pressing SPACE should not advance
        msg = dm.next_message("SPACE", now)
        self.assertEqual(msg, "Message 1")

        # After delay passes, pressing SPACE advances message
        msg = dm.next_message("SPACE", now + 0.6)
        self.assertEqual(msg, "Message 2")

        # Advance to last message
        msg = dm.next_message("SPACE", now + 1.2)
        self.assertEqual(msg, "Au revoir")

        # Callback should not be triggered yet
        self.assertFalse(callback_triggered)

        # Press SPACE after delay to finish dialogue and trigger callback
        msg = dm.next_message("SPACE", now + 1.8)
        self.assertEqual(msg, "")
        self.assertTrue(callback_triggered)

    def test_no_advance_without_space(self):
        messages = ["Salut", "Au revoir"]
        dm = DialogueManager(messages, delay=0.5)
        now = time.time()
        # Pressing a key other than 'SPACE' should not advance
        msg = dm.next_message("ENTER", now + 1)
        self.assertEqual(msg, "Salut")

if __name__ == '__main__':
    unittest.main()
