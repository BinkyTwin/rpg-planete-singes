import pygame
import os

# Initialiser Pygame
pygame.init()

# Obtenir le chemin de base du projet
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "assets", "tilesets", "images", "Design sans titre.png")

print(f"Test de chargement de l'image: {image_path}")
print(f"Le fichier existe: {os.path.exists(image_path)}")
if os.path.exists(image_path):
    print(f"Taille du fichier: {os.path.getsize(image_path)} bytes")

try:
    image = pygame.image.load(image_path)
    print(f"Image chargée avec succès!")
    print(f"Dimensions: {image.get_width()}x{image.get_height()}")
except pygame.error as e:
    print(f"Erreur lors du chargement: {e}")
except Exception as e:
    print(f"Erreur inattendue : {e}")

# Quitter Pygame
pygame.quit()