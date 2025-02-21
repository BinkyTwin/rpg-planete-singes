#!/usr/bin/env python3
"""
La Planète des Singes - RPG
"""

import os
import sys
import venv
import subprocess

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

class Game:
    def __init__(self):
        print("Initialisation du jeu...", flush=True)
        try:
            global pygame
            pygame.init()
            print("Pygame initialisé avec succès", flush=True)
            
            # Configuration de base
            self.WINDOW_WIDTH = 800
            self.WINDOW_HEIGHT = 600
            self.FPS = 60
            
            print("Création de la fenêtre...", flush=True)
            # Création de la fenêtre
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
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
                'menu': MenuScene(self.screen, self.game_state),
                'game': GameScene(self.screen, self.game_state),
                'character_creation': CharacterCreationScene(self.screen, self.game_state)
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
                    
                # Laisse la scène courante gérer l'événement
                new_scene = self.scenes[self.current_scene].handle_event(event)
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
            self.scenes[self.current_scene].update()
            
            if hasattr(self.scenes[self.current_scene], 'player'):
                move_vector = self.handle_input()
                self.scenes[self.current_scene].player.move(move_vector, 1/60)
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de la mise à jour : {e}", flush=True)
            import traceback
            traceback.print_exc()

    def render(self):
        """Dessine le jeu"""
        try:
            # Efface l'écran
            self.screen.fill((0, 0, 0))
            
            # Dessine la scène courante
            self.scenes[self.current_scene].render()
            
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
    global GameState, MenuScene, GameScene, CharacterCreationScene
    
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