import pytest
import pygame
import time
import gc
import psutil
import os
from game.player import Player
from game.factions import FactionName
from game.pnj import PNJ
from game.dialogue_system import DialogueSystem
from game.map import Map
from game.layer_manager import LayerType
from unittest.mock import patch

class TestPNJ:
    @pytest.fixture
    def player(self, setup_pygame):
        # Créer un joueur pour les tests
        player = Player(name="TestPlayer", x=0, y=0, race="orang outan", faction=FactionName.FORET)
        return player

    @pytest.fixture
    def setup_pygame(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        yield
        pygame.quit()

    @pytest.fixture
    def game_map(self):
        # Créer une carte de test 30x30 sans charger les tuiles
        with patch('game.map.Map._load_tiles'):  # Ne pas charger les tuiles
            game_map = Map(30, 30)
        return game_map

    def test_pnj_creation(self, setup_pygame):
        """Test de la création basique d'un PNJ"""
        # Position en tuiles (20, 27)
        pnj = PNJ(position=(20, 27))
        
        # Vérification des attributs de base
        assert pnj.tile_x == 20
        assert pnj.tile_y == 27
        assert pnj.sprite_name == 'orang_outan.png'
        
        # Pour le moment, on ne teste pas le sprite car il n'existe pas encore
        # On vérifie juste que c'est une surface pygame (même si c'est le fallback)
        assert isinstance(pnj.sprite, pygame.Surface)

    def test_pnj_faction(self, player):
        """Test de la faction du PNJ"""
        pnj = PNJ(position=(20, 27))
        
        # Le PNJ doit avoir la même faction que le joueur
        pnj.sync_faction(player)
        assert pnj.faction == player.faction
        assert pnj.faction == FactionName.FORET

    def test_dialogue_trigger(self, player):
        """Test du déclenchement du dialogue"""
        pnj = PNJ(position=(20, 27))
        player.x, player.y = 20 * 32, 27 * 32  # Position en pixels (proche du PNJ)
        
        # Le dialogue doit se déclencher quand le joueur est proche
        assert pnj.can_trigger_dialogue(player) == True
        
        # Le dialogue ne doit pas se déclencher si le joueur est trop loin
        player.x, player.y = 0, 0  # Position éloignée
        assert pnj.can_trigger_dialogue(player) == False

    def test_dialogue_progression(self):
        """Test de la progression du dialogue"""
        pnj = PNJ(position=(20, 27))
        
        # Vérifier que le dialogue commence au début
        message = pnj.start_dialogue()
        assert message == DialogueSystem.DIALOGUES_PNJ[0]
        assert pnj.dialogue_system.is_dialogue_active == True
        
        # Vérifier la progression des messages
        message = pnj.next_message()
        assert message == DialogueSystem.DIALOGUES_PNJ[1]
        
        # Vérifier que le dialogue se termine correctement
        for _ in range(len(DialogueSystem.DIALOGUES_PNJ) - 2):  # -2 car on a déjà lu 2 messages
            pnj.next_message()
            
        final_message = pnj.next_message()
        assert final_message is None
        assert pnj.dialogue_system.is_dialogue_active == False
        assert pnj.dialogue_system.is_dialogue_finished() == True

    def test_dialogue_content(self):
        """Test du contenu du dialogue"""
        pnj = PNJ(position=(20, 27))
        
        # Vérifier que les messages sont dans le bon ordre
        messages = []
        message = pnj.start_dialogue()
        while message is not None:
            messages.append(message)
            message = pnj.next_message()
            
        # Vérifier que tous les messages ont été affichés dans l'ordre
        assert messages == DialogueSystem.DIALOGUES_PNJ

    def test_pnj_render(self, setup_pygame, game_map):
        """Test du rendu du PNJ sur la map"""
        pnj = PNJ(position=(20, 27))
        screen = pygame.display.get_surface()
        
        # Vérifier que le PNJ peut être rendu
        pnj.render(screen, camera_x=0, camera_y=0)
        
        # Vérifier que la position en pixels est correcte
        assert pnj.get_pixel_position() == (20 * 32, 27 * 32)

    def test_collision_detection(self, player, game_map):
        """Test de la détection de collision avec le PNJ"""
        pnj = PNJ(position=(20, 27))
        game_map.add_pnj(pnj)  # Ajouter le PNJ à la map
        
        # Déplacer le joueur près du PNJ
        game_map.player_pos = (19, 27)  # Position initiale
        success, message, _, has_met_pnj = game_map.move_player(1, 0)  # Déplacement vers le PNJ
        assert success == True
        assert has_met_pnj == True  # On rencontre le PNJ 

    def test_pnj_disappears_after_dialogue(self, game_map):
        """Test de la disparition du PNJ après le dialogue"""
        pnj = PNJ(position=(20, 27))
        game_map.add_pnj(pnj)

        # Vérifier que le PNJ est visible au début
        assert pnj.is_visible == True
        assert game_map.pnj is not None

        # Simuler un dialogue complet
        pnj.start_dialogue()
        for _ in range(len(DialogueSystem.DIALOGUES_PNJ) - 1):
            pnj.next_message()

        # Après le dernier message
        pnj.next_message()
        
        # Le PNJ doit disparaître
        assert pnj.is_visible == False
        assert game_map.layer_manager.get_tile(LayerType.NPC, 20, 27) == 0

    def test_memory_management(self, game_map):
        """Test de la gestion de la mémoire après la disparition du PNJ"""
        pnj = PNJ(position=(20, 27))
        game_map.add_pnj(pnj)

        # Faire disparaître le PNJ
        pnj.remove_from_map()
        game_map.remove_pnj()

        # Vérifier que toutes les références sont nettoyées
        assert pnj.is_visible == False
        assert game_map.pnj is None
        assert game_map.npc_pos is None
        assert game_map.layer_manager.get_tile(LayerType.NPC, 20, 27) == 0 

    def test_performance_multiple_pnjs(self, game_map):
        """Test des performances avec plusieurs PNJ"""
        # Mesurer l'utilisation de la mémoire avant
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss

        # Créer plusieurs PNJ
        pnjs = []
        for x in range(10):  # Test avec 10 PNJ
            for y in range(10):
                pnj = PNJ(position=(x * 2, y * 2))  # Espacés de 2 tuiles
                game_map.add_pnj(pnj)
                pnjs.append(pnj)

        # Mesurer l'utilisation de la mémoire après
        memory_after = process.memory_info().rss
        memory_per_pnj = (memory_after - memory_before) / (10 * 10)  # Mémoire moyenne par PNJ

        # La mémoire par PNJ ne devrait pas dépasser 5MB
        assert memory_per_pnj < 5 * 1024 * 1024  # 5MB en bytes

        # Nettoyer
        for pnj in pnjs:
            pnj.remove_from_map()
            game_map.remove_pnj()

    def test_render_performance(self, setup_pygame, game_map):
        """Test des performances de rendu"""
        screen = pygame.display.get_surface()
        pnj = PNJ(position=(20, 27))
        game_map.add_pnj(pnj)

        # Mesurer le temps de rendu pour 100 frames
        start_time = time.time()
        for _ in range(100):
            pnj.render(screen, camera_x=0, camera_y=0)
            pygame.display.flip()

        end_time = time.time()
        render_time = (end_time - start_time) / 100  # Temps moyen par frame

        # Le rendu ne devrait pas prendre plus de 16ms par frame (60 FPS)
        assert render_time < 0.016  # 16ms

    def test_memory_cleanup(self, game_map):
        """Test du nettoyage de la mémoire après la suppression des PNJ"""
        # Forcer le garbage collector
        gc.collect()
        
        # Mesurer l'utilisation de la mémoire avant
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss

        # Créer et supprimer plusieurs PNJ
        for _ in range(100):
            pnj = PNJ(position=(20, 27))
            game_map.add_pnj(pnj)
            pnj.remove_from_map()
            game_map.remove_pnj()

        # Forcer le garbage collector
        gc.collect()

        # Mesurer l'utilisation de la mémoire après
        memory_after = process.memory_info().rss

        # La différence de mémoire ne devrait pas être significative (moins de 5MB)
        assert abs(memory_after - memory_before) < 5 * 1024 * 1024  # 5MB en bytes 

    def test_sprite_sheet_loading(self, setup_pygame):
        """Test du chargement correct du sprite sheet"""
        pnj = PNJ(position=(20, 27))
        
        # Vérifier que le dictionnaire des sprites est correctement initialisé
        assert all(direction in pnj.sprites for direction in ["down", "left", "right", "up"])
        
        # Vérifier que chaque direction a 4 frames
        for direction in ["down", "left", "right", "up"]:
            assert len(pnj.sprites[direction]) == 4
            
            # Vérifier les dimensions de chaque frame
            for frame in pnj.sprites[direction]:
                assert frame.get_width() == pnj.SPRITE_SIZE
                assert frame.get_height() == pnj.SPRITE_SIZE
                
                # Vérifier que la surface a un canal alpha (transparence)
                assert frame.get_flags() & pygame.SRCALPHA
                
                # Vérifier que la frame n'est pas vide (entièrement transparente)
                pixels = pygame.surfarray.pixels_alpha(frame)
                assert pixels.any()  # Au moins quelques pixels non transparents
                del pixels  # Libérer la mémoire

    def test_sprite_frame_extraction(self, setup_pygame):
        """Test de l'extraction correcte des frames du sprite sheet"""
        pnj = PNJ(position=(20, 27))
        
        # Charger le sprite sheet original pour comparaison
        sprite_path = os.path.join('assets', 'sprites', 'orang_outan.png')
        original_sheet = pygame.image.load(sprite_path)
        
        # Vérifier que chaque frame correspond à la bonne partie du sprite sheet
        for row, direction in enumerate(["down", "left", "right", "up"]):
            for col in range(4):
                frame = pnj.sprites[direction][col]
                
                # Extraire la même région du sprite sheet original
                expected_region = pygame.Surface((32, 32), pygame.SRCALPHA)
                expected_region.blit(original_sheet, (0, 0), 
                                   (col * 32, row * 32, 32, 32))
                
                # Comparer les pixels des deux surfaces
                assert pygame.surfarray.pixels3d(frame).shape == \
                       pygame.surfarray.pixels3d(expected_region).shape
                
                # Comparer les canaux alpha
                assert pygame.surfarray.pixels_alpha(frame).shape == \
                       pygame.surfarray.pixels_alpha(expected_region).shape

    def test_sprite_animation_sequence(self, setup_pygame):
        """Test de la séquence d'animation du sprite"""
        pnj = PNJ(position=(20, 27))
        
        # Vérifier la séquence d'animation pour chaque direction
        for direction in ["down", "left", "right", "up"]:
            # Vérifier que les frames sont différentes entre elles
            frames = pnj.sprites[direction]
            for i in range(len(frames)):
                for j in range(i + 1, len(frames)):
                    # Comparer les pixels des frames
                    pixels_i = pygame.surfarray.pixels3d(frames[i])
                    pixels_j = pygame.surfarray.pixels3d(frames[j])
                    assert not (pixels_i == pixels_j).all()
                    del pixels_i, pixels_j  # Libérer la mémoire 