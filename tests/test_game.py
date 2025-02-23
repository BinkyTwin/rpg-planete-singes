import pytest
import pygame
import os
import sys
from main import Game, load_dependencies
from game.scenes.message_scene import MessageScene

def test_background_music_initialization():
    # Chargement des dépendances
    load_dependencies()
    pygame.init()
    pygame.mixer.init()
    
    # Initialisation du jeu
    game = Game()
    
    # Vérification que la musique est bien chargée
    assert game.background_music is not None
    
    # Vérification que le volume est correctement réglé (avec une marge d'erreur)
    volume = game.background_music.get_volume()
    assert abs(volume - 0.4) < 0.01  # Tolérance de 1% pour le volume à 40%
    
    # Vérification que le fichier existe
    assert os.path.exists("music/Background.mp3")
    
    # Nettoyage
    pygame.quit()

def test_weapon_sound():
    # Chargement des dépendances
    load_dependencies()
    pygame.init()
    pygame.mixer.init()
    
    # Création d'une instance de MessageScene avec les paramètres minimaux requis
    scene = MessageScene(pygame.Surface((800, 600)), None, "Test message")
    
    # Vérification que le son de l'arme est bien chargé
    assert scene.weapon_sound is not None
    
    # Vérification que le volume est correctement réglé (avec une marge d'erreur)
    volume = scene.weapon_sound.get_volume()
    assert abs(volume - 0.8) < 0.01  # Tolérance de 1%
    
    # Vérification que le fichier existe
    assert os.path.exists("music/m16sound.mp3")
    
    # Nettoyage
    pygame.quit() 