import time

class DialogueManager:
    def __init__(self, messages, delay=0.5, on_end=None):
        """
        Initialize the DialogueManager.

        :param messages: List of dialogue messages.
        :param delay: Minimum delay in seconds between message transitions.
        :param on_end: Callback function to call when dialogue ends.
        """
        self.messages = messages
        self.delay = delay
        self.on_end = on_end
        self.current_index = 0
        # Initialize last_update_time to current time so that immediate key press does not advance the message.
        self.last_update_time = time.time()

    def current_message(self):
        """Return the current dialogue message or empty string if finished."""
        if self.current_index < len(self.messages):
            return self.messages[self.current_index]
        return ""

    def next_message(self, key, current_time):
        """
        Process the input key and update the current message if conditions are met.
        :param key: The key pressed by the user (expects "SPACE").
        :param current_time: The current time in seconds.
        :return: The updated current message.
        """
        if key == "SPACE":
            if current_time - self.last_update_time >= self.delay:
                self.last_update_time = current_time
                self.current_index += 1
                if self.current_index >= len(self.messages) and self.on_end:
                    self.on_end()
        return self.current_message()
