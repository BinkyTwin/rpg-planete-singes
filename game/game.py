#!/usr/bin/env python3
"""
Module principal du jeu contenant la classe Game
"""

import sys
import pygame
from game.display_manager import DisplayManager
from game.game_state import GameState
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene
from game.scenes.character_creation_scene import CharacterCreationScene
from game.scenes.message_scene import MessageScene

class Game:
    def __init__(self):
        print("Initialisation du jeu...", flush=True)
        try:
            pygame.mixer.init()  # Initialisation du module de son
            print("Pygame initialisé avec succès", flush=True)
            
            # Initialisation de la musique de fond
            self.background_music = pygame.mixer.Sound("music/Background.mp3")
            self.background_music.set_volume(0.4)  # Volume à 40%
            self.background_music.play(loops=-1)  # -1 pour une répétition infinie
            
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
                'message': lambda: MessageScene(
                    self.display_manager.screen,
                    self.game_state,
                    self.game_state.temp_message,
                    self.display_manager
                )
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
        """Gère les entrées clavier pour le mouvement"""
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
            
            # Récupérer le résultat de la mise à jour
            new_scene = scene.update()
            
            # Si la scène demande un changement
            if new_scene and new_scene in self.scenes:
                print(f"DEBUG - Changement de scène: {self.current_scene} -> {new_scene}")
                self.current_scene = new_scene
                return
            
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