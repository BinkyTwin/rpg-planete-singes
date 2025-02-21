import pygame
import os

pygame.init()

# Chemin vers l'image
image_path = "assets/tilesets/images/Design sans titre.png"

print(f"Test de chargement de l'image: {image_path}")
print(f"Le fichier existe: {os.path.exists(image_path)}")
if os.path.exists(image_path):
    print(f"Taille du fichier: {os.path.getsize(image_path)} bytes")

try:
    image = pygame.image.load(image_path)
    print(f"Image chargée avec succès!")
    print(f"Dimensions: {image.get_width()}x{image.get_height()}")
except Exception as e:
    print(f"Erreur lors du chargement: {str(e)}") 