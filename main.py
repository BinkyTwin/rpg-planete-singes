#!/usr/bin/env python3
"""
La Planète des Singes - RPG
"""

import os
import sys
import venv
import subprocess
from game.display_manager import DisplayManager

# Variables globales pour les imports
pygame = None
Player = None
FactionName = None
FACTIONS = None
Inventory = None
ITEMS = None
ItemType = None
Map = None
TileType = None
SpawnManager = None
CombatSystem = None
DialogueSystem = None
GameState = None
MenuScene = None
GameScene = None
CharacterCreationScene = None
MessageScene = None

class Game:
    def __init__(self):
        print("Initialisation du jeu...", flush=True)
        try:
            global pygame
            pygame.init()
            print("Pygame initialisé avec succès", flush=True)
            
            # Initialiser le gestionnaire d'affichage
            self.display_manager = DisplayManager()
            self.FPS = 60
            
            print("Création de la fenêtre...", flush=True)
            # La fenêtre est déjà créée par le DisplayManager
            pygame.display.set_caption("La Planète des Singes - RPG")
            print("Fenêtre créée avec succès", flush=True)
            
            # Horloge pour contrôler le FPS
            self.clock = pygame.time.Clock()
            
            print("Initialisation de l'état du jeu...", flush=True)
            # État du jeu
            self.game_state = GameState()
            print("État du jeu initialisé", flush=True)
            
            print("Chargement des scènes...", flush=True)
            # Scènes du jeu
            self.scenes = {
                'menu': MenuScene(self.display_manager.screen, self.game_state, self.display_manager),
                'game': GameScene(self.display_manager.screen, self.game_state, self.display_manager),
                'character_creation': CharacterCreationScene(self.display_manager.screen, self.game_state, self.display_manager),
                'message': lambda: MessageScene(self.display_manager.screen, self.game_state, self.game_state.temp_message, self.display_manager)
            }
            self.current_scene = 'menu'
            print("Scènes chargées avec succès", flush=True)
            print("Initialisation terminée!", flush=True)
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de l'initialisation : {e}", flush=True)
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def handle_events(self):
        """Gère les événements globaux"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
                # Gérer le redimensionnement de la fenêtre
                elif event.type == pygame.VIDEORESIZE and not self.display_manager.is_fullscreen:
                    old_size = self.display_manager.handle_resize(event.w, event.h)
                    # Mettre à jour les scènes avec le nouveau screen
                    for scene_name, scene in self.scenes.items():
                        if callable(scene):
                            self.scenes[scene_name] = scene()
                        scene = self.scenes[scene_name]
                        scene.screen = self.display_manager.screen
                        
                # Gérer le basculement plein écran (Alt+Enter)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                        old_size = self.display_manager.toggle_fullscreen()
                        # Mettre à jour les scènes avec le nouveau screen
                        for scene_name, scene in self.scenes.items():
                            if callable(scene):
                                self.scenes[scene_name] = scene()
                            scene = self.scenes[scene_name]
                            scene.screen = self.display_manager.screen
                
                # Laisse la scène courante gérer l'événement
                scene = self.scenes[self.current_scene]
                if callable(scene):
                    self.scenes[self.current_scene] = scene()
                    scene = self.scenes[self.current_scene]
                new_scene = scene.handle_event(event)
                if new_scene and new_scene in self.scenes:
                    self.current_scene = new_scene
                
            return True
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de la gestion des événements : {e}", flush=True)
            import traceback
            traceback.print_exc()
            return False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_vector = [0, 0]
        
        # ZQSD
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            move_vector[1] -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_vector[1] += 1
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            move_vector[0] -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_vector[0] += 1
            
        return move_vector

    def update(self):
        """Met à jour l'état du jeu"""
        try:
            # Met à jour la scène courante
            scene = self.scenes[self.current_scene]
            if callable(scene):
                self.scenes[self.current_scene] = scene()
                scene = self.scenes[self.current_scene]
            scene.update()
            
            if hasattr(scene, 'player'):
                move_vector = self.handle_input()
                scene.player.move(move_vector, 1/60)
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de la mise à jour : {e}", flush=True)
            import traceback
            traceback.print_exc()

    def render(self):
        """Dessine le jeu"""
        try:
            # Efface l'écran
            self.display_manager.screen.fill((0, 0, 0))
            
            # Dessine la scène courante
            scene = self.scenes[self.current_scene]
            if callable(scene):
                self.scenes[self.current_scene] = scene()
                scene = self.scenes[self.current_scene]
            scene.render(self.display_manager.screen)
            
            # Rafraîchit l'affichage
            pygame.display.flip()
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors du rendu : {e}", flush=True)
            import traceback
            traceback.print_exc()

    def run(self):
        """Boucle principale du jeu"""
        print("Démarrage de la boucle de jeu...", flush=True)
        try:
            running = True
            while running:
                # Gestion des événements
                running = self.handle_events()
                
                # Mise à jour
                self.update()
                
                # Rendu
                self.render()
                
                # Contrôle du FPS
                self.clock.tick(self.FPS)
                
            print("Fermeture du jeu...", flush=True)
            pygame.quit()
            sys.exit()
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue dans la boucle principale : {e}", flush=True)
            import traceback
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)

def setup_environment():
    """Configure l'environnement virtuel et installe les dépendances"""
    print("=== Configuration de l'environnement de jeu ===", flush=True)
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
    venv_python = os.path.join(venv_path, "Scripts", "python.exe")
    
    try:
        if not os.path.exists(venv_path):
            print("Création de l'environnement virtuel...", flush=True)
            venv.create(venv_path, with_pip=True)
            print("Environnement virtuel créé avec succès", flush=True)
        
        print("Installation des dépendances...", flush=True)
        requirements_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements_file])
        print("[OK] Dépendances installées avec succès\n", flush=True)
        
        return venv_python
        
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Erreur lors de l'installation des dépendances : {e}", flush=True)
        return None
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la configuration de l'environnement : {e}", flush=True)
        return None

def load_dependencies():
    """Charge toutes les dépendances nécessaires"""
    global pygame, Player, FactionName, FACTIONS, Inventory, ITEMS, ItemType
    global Map, TileType, SpawnManager, CombatSystem, DialogueSystem
    global GameState, MenuScene, GameScene, CharacterCreationScene, MessageScene
    
    try:
        import pygame
        pygame.init()
        print("Pygame importé et initialisé avec succès", flush=True)
        
        from game.player import Player
        from game.factions import FactionName, FACTIONS
        from game.inventory import Inventory
        from game.items import ITEMS, ItemType
        from game.map import Map, TileType
        from game.spawn_manager import SpawnManager
        from game.combat_system import CombatSystem
        from game.dialogue_system import DialogueSystem
        from game.game_state import GameState
        from game.scenes.menu_scene import MenuScene
        from game.scenes.game_scene import GameScene
        from game.scenes.character_creation_scene import CharacterCreationScene
        from game.scenes.message_scene import MessageScene
        print("Toutes les dépendances ont été chargées avec succès", flush=True)
    except ImportError as e:
        print(f"[ERREUR] Erreur lors de l'importation des dépendances : {e}", flush=True)
        raise

def main():
    """Point d'entrée principal du jeu"""
    # Si nous ne sommes pas déjà dans un environnement virtuel
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
    venv_python = os.path.join(venv_path, "Scripts", "python.exe")
    
    if not os.path.exists(venv_path):
        python_path = setup_environment()
        if python_path:
            print("\n=== Lancement du jeu ===", flush=True)
            try:
                # Relance le script dans l'environnement virtuel
                os.execv(python_path, [python_path, __file__])
            except Exception as e:
                print(f"[ERREUR] Erreur lors du lancement du jeu : {e}", flush=True)
                sys.exit(1)
        else:
            print("[ERREUR] Impossible de configurer l'environnement. Veuillez vérifier les erreurs ci-dessus.", flush=True)
            sys.exit(1)
    else:
        # Nous sommes dans l'environnement virtuel, importe les dépendances et lance le jeu
        try:
            # Charge toutes les dépendances
            load_dependencies()
            
            # Lance le jeu
            print("Démarrage du jeu...", flush=True)
            game = Game()
            game.run()
            
        except ImportError as e:
            print(f"[ERREUR] Erreur lors de l'importation des dépendances : {e}", flush=True)
            sys.exit(1)
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue : {e}", flush=True)
            sys.exit(1)

if __name__ == "__main__":
    main()