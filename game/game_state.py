class GameState:
    def __init__(self):
        self.player = None
        self.map = None
        self.spawn_manager = None
        self.inventory = None
        self.current_scene = 'menu'
        self.game_over = False
        self.start_time = None 