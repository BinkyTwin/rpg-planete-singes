#!/usr/bin/env python3
"""
La Planète des Singes - RPG
"""

import os
import sys
import venv
import subprocess

def is_venv():
    """Vérifie si nous sommes dans un environnement virtuel"""
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def clean_venv(venv_path):
    """Nettoie l'environnement virtuel si nécessaire"""
    import shutil
    try:
        if os.path.exists(venv_path):
            print("\nNettoyage de l'ancien environnement virtuel...", flush=True)
            shutil.rmtree(venv_path, ignore_errors=True)
            # Attendre un peu pour s'assurer que Windows a bien libéré les fichiers
            import time
            time.sleep(2)
            print("[OK] Ancien environnement supprimé", flush=True)
    except Exception as e:
        print(f"[ATTENTION] Impossible de nettoyer complètement l'environnement : {e}", flush=True)
        print("Tentative de continuer malgré tout...", flush=True)

def setup_environment():
    """Configure l'environnement virtuel et installe les dépendances"""
    print("\n=== Configuration de l'environnement de jeu ===", flush=True)
    
    # Chemins importants
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(base_dir, "venv")
    requirements_file = os.path.join(base_dir, "requirements.txt")
    
    # Vérification de l'existence du fichier requirements.txt
    if not os.path.exists(requirements_file):
        print("[ERREUR] Le fichier requirements.txt est manquant!", flush=True)
        return None
        
    try:
        # Nettoyage de l'ancien venv si nécessaire
        clean_venv(venv_path)
        
        # Création du venv
        print("\n1. Création de l'environnement virtuel...", flush=True)
        venv.create(venv_path, with_pip=True)
        print("[OK] Environnement virtuel créé avec succès", flush=True)
        
        # Détermination du chemin de l'exécutable Python du venv
        if sys.platform == "win32":
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")
            venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
        else:
            venv_python = os.path.join(venv_path, "bin", "python")
            venv_pip = os.path.join(venv_path, "bin", "pip")
            
        if not os.path.exists(venv_python):
            print("[ERREUR] L'exécutable Python n'a pas été trouvé dans le venv!", flush=True)
            return None
            
        # Installation des dépendances directement avec le requirements.txt
        print("\n2. Installation des dépendances depuis requirements.txt...", flush=True)
        try:
            # Premier essai avec pip
            subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements_file])
        except subprocess.CalledProcessError:
            print("[ATTENTION] Première tentative échouée, nouvelle tentative...", flush=True)
            try:
                # Deuxième essai en forçant la réinstallation
                subprocess.check_call([venv_python, "-m", "pip", "install", "--ignore-installed", "-r", requirements_file])
            except subprocess.CalledProcessError as e:
                print(f"[ERREUR] Impossible d'installer les dépendances : {e}", flush=True)
                return None
                
        print("[OK] Dépendances installées avec succès\n", flush=True)
        
        return venv_python
        
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Erreur lors de l'installation : {e}", flush=True)
        return None
    except Exception as e:
        print(f"[ERREUR] Erreur inattendue : {e}", flush=True)
        import traceback
        traceback.print_exc()
        return None

def main():
    """Point d'entrée principal du jeu"""
    try:
        # Vérifie si nous sommes dans le venv
        if not is_venv():
            # Si nous ne sommes pas dans le venv, on le configure et on relance le script
            python_path = setup_environment()
            if python_path:
                print("\n=== Configuration terminée avec succès ===", flush=True)
                print("Relancement du jeu dans l'environnement virtuel...\n", flush=True)
                try:
                    # Sous Windows, on utilise subprocess.call au lieu de os.execv
                    if sys.platform == "win32":
                        subprocess.call([python_path, __file__])
                        sys.exit(0)
                    else:
                        os.execv(python_path, [python_path, __file__])
                except Exception as e:
                    print(f"[ERREUR] Erreur lors du relancement du jeu : {e}", flush=True)
                    sys.exit(1)
            else:
                print("\n[ERREUR] La configuration de l'environnement a échoué.", flush=True)
                print("Veuillez vérifier les erreurs ci-dessus et réessayer.", flush=True)
                sys.exit(1)
        else:
            # Nous sommes dans le venv, on peut importer les dépendances
            try:
                # Import des dépendances seulement une fois dans le venv
                print("\n=== Chargement des dépendances ===", flush=True)
                
                print("1. Importation de Pygame...", flush=True)
                import pygame
                pygame.init()
                print("[OK] Pygame importé et initialisé avec succès", flush=True)
                
                print("\n2. Importation des modules du jeu...", flush=True)
                from game.display_manager import DisplayManager
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
                print("[OK] Tous les modules du jeu ont été importés avec succès\n", flush=True)
                
                # Lancement du jeu
                print("=== Démarrage du jeu ===\n", flush=True)
                from game.game import Game  # On importe Game seulement maintenant
                game = Game()
                game.run()
                
            except ImportError as e:
                print(f"[ERREUR] Erreur lors du chargement des dépendances : {e}", flush=True)
                print("Assurez-vous que toutes les dépendances sont correctement installées.", flush=True)
                sys.exit(1)
            except Exception as e:
                print(f"[ERREUR] Une erreur est survenue : {e}", flush=True)
                import traceback
                traceback.print_exc()
                sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] Une erreur inattendue est survenue : {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()