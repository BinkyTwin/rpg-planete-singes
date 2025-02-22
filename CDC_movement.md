# Cahier des Charges : Système de Mouvement et Positionnement

## 1. Objectif
Implémenter un système de mouvement fluide et réactif pour le jeu "La Planète des Singes", permettant au joueur de se déplacer dans un monde en 2D avec des collisions et des transitions de calques.

## 2. Spécifications Techniques

### 2.1 Carte
- Dimensions : 30x30 tuiles
- Taille des tuiles : 32x32 pixels
- Tileset : OGAtilesetsremixed.png (960x960 pixels, 900 tuiles)
- Position initiale du joueur : En bas de la carte

### 2.2 Système de Coordonnées
- Grille : Coordonnées basées sur les tuiles (0,0 en haut à gauche)
- Écran : Coordonnées en pixels avec le joueur centré
- Conversion fluide entre les deux systèmes

### 2.3 Déplacement du Joueur
- Vitesse de base : 1 tuile par action
- Contrôles :
  * ZQSD ou flèches directionnelles
  * Déplacement diagonal possible (vitesse normalisée)
- Animation fluide lors des déplacements
- 4 directions avec sprites correspondants

### 2.4 Collisions
- Détection précise avec les obstacles
- Gestion des différents types de terrain
- Transition fluide entre les calques (devant/derrière les objets)

### 2.5 Caméra
- Centrée sur le joueur
- Défilement fluide
- Gestion des bords de carte

## 3. Tests et Validation

### 3.1 Tests Unitaires
- Conversion de coordonnées
- Détection de collisions
- Gestion des entrées

### 3.2 Tests d'Intégration
- Mouvement complet (input → déplacement → rendu)
- Synchronisation caméra/joueur
- Transitions entre calques

### 3.3 Critères de Validation
- Déplacement fluide sans saccades
- Pas de traversée d'obstacles
- Transitions visuelles correctes
- Performance stable (60 FPS)

## 4. Contraintes Techniques
- Utilisation de Pygame pour le rendu
- Utilisation de Tiled pour la gestion des maps
- Compatibilité avec le système existant de gestion des assets
- Support des résolutions d'écran variables
