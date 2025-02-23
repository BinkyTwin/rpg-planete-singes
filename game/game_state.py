class GameState:
    def __init__(self):
        """Initialise l'état du jeu avec des valeurs par défaut"""
        # Statistiques persistantes (ne sont pas réinitialisées)
        self.game_over_count = 0
        self.last_game_duration = 0
        self.total_play_time = 0
        
        # État du jeu
        self.initialize_game_state()
        
    def initialize_game_state(self):
        """Initialise ou réinitialise tous les attributs liés à l'état du jeu"""
        # Joueur et inventaire
        self.player = None
        self.inventory = None
        
        # Gestion de la carte et des spawns
        self.map = None
        self.spawn_manager = None
        
        # Gestion des PNJs
        self.active_pnj = None
        self.pnj2 = None
        
        # Gestion des scènes et messages
        self.current_scene = 'menu'
        self.temp_message = None
        self.previous_scene = None
        
        # États du jeu
        self.game_over = False
        self.combat_active = False
        self.dialog_active = False
        
        # Timing
        self.start_time = None
        self.pause_time = None
        
    def reset(self):
        """Réinitialise complètement l'état du jeu et met à jour les statistiques"""
        # Mise à jour des statistiques si c'était un game over
        if self.game_over:
            self.game_over_count += 1
            if self.start_time:
                import time
                current_time = time.time()
                session_duration = current_time - self.start_time
                self.last_game_duration = session_duration
                self.total_play_time += session_duration
        
        # Réinitialisation complète de l'état du jeu
        self.initialize_game_state()
        
        print("État du jeu réinitialisé avec succès")