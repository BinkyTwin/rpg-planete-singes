import pygame
import pytest
from game.scenes.game_scene import GameScene
from game.game_state import GameState
from game.player import Player
from game.factions import FactionName

class MockDisplayManager:
    def __init__(self):
        self.is_fullscreen = False
        
    def get_scaled_font_size(self, size):
        return size

@pytest.fixture
def game_setup():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState()
    game_state.player = Player("Test", 6, 28, "chimpanze", FactionName.VEILLEURS)
    display_manager = MockDisplayManager()
    game_scene = GameScene(screen, game_state, display_manager)
    return game_scene, game_state

def test_combat_zone_detection(game_setup):
    game_scene, game_state = game_setup
    
    # Test: Joueur hors de la zone de combat
    game_state.player.x = 10
    game_state.player.y = 10
    game_scene.update()
    assert not game_scene.in_combat_zone
    assert not game_scene.combat_dialog_active
    assert game_state.temp_message is None
    
    # Test: Joueur entre dans la zone de combat
    game_state.player.x = 14
    game_state.player.y = 9
    result = game_scene.update()
    assert game_scene.in_combat_zone
    assert game_scene.combat_dialog_active
    assert result == 'message'
    assert "zone de combat" in game_state.temp_message.lower()
    
    # Test: Joueur sort de la zone de combat
    game_state.player.x = 10
    game_state.player.y = 10
    game_scene.update()
    assert not game_scene.in_combat_zone
    assert not game_scene.combat_dialog_active
    assert game_state.temp_message is None

def test_combat_zone_positions(game_setup):
    game_scene, game_state = game_setup
    
    # Test de toutes les positions de la zone de combat
    combat_positions = [
        (14, 9), (14, 11), (13, 10), (15, 10),
        (13, 9), (15, 9), (13, 11), (15, 11)
    ]
    
    for x, y in combat_positions:
        game_state.player.x = x
        game_state.player.y = y
        game_scene.update()
        assert game_scene.in_combat_zone, f"Position ({x}, {y}) devrait être dans la zone de combat"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 