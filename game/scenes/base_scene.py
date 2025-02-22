class BaseScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        
    def handle_event(self, event):
        """Gère les événements de la scène"""
        pass
        
    def update(self):
        """Met à jour la scène"""
        pass
        
    def render(self, screen):
        """Dessine la scène"""
        pass 