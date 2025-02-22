## Fonctionnalité de gestion des mouvements

### Contrôles
- [x] Implémenter les contrôles Z/Q/S/D + flèches directionnelles ✔️
- [x] Gérer la vitesse de déplacement et l'animation du personnage ✔️

### Gestion de la map
- [x] Implémenter le système de calques :
  - [x] Calque "collisions" (bloque le mouvement) ✔️
  - [x] Calque "sol" (mouvement autorisé) ✔️
  - [x] Calque "three" (gestion de la profondeur graphique) ✔️
- [x] Empêcher le personnage de sortir des limites de la map ✔️
- [x] Créer un système de détection de collision avec les obstacles ✔️

### Apparence du personnage
- [x] Charger les sprites depuis le dossier "character" ✔️
- [x] Associer chaque race de singe à son sprite correspondant ✔️
- [x] Implémenter le changement de layer graphique pour le calque "three" ✔️

### Initialisation
- [x] Positionner le personnage sur le calque "sol" aux coordonnées (1,12) ✔️
- [x] Vérifier que la position initiale est valide (pas sur une collision) ✔️

### Tests
- [x] Tester tous les types de déplacement ✔️
- [x] Tester les collisions avec différents obstacles ✔️
- [x] Tester le rendu graphique sur le calque "three" ✔️

# TODO : Implémentation du Système de Mouvement

## Phase 1 : Configuration Initiale

### 1.1 Mise à jour du Système de Chargement de Carte
- [x] Adapter TiledMap pour la nouvelle structure de mapV3.tmx ✔️
- [x] Implémenter le chargement du nouveau tileset OGAtilesetsremixed ✔️
- [x] Vérifier la gestion des calques de la nouvelle carte ✔️

### 1.2 Position Initiale du Joueur
- [x] Déterminer les coordonnées de spawn en bas de la carte ✔️
- [x] Adapter le système de coordonnées pour la nouvelle taille de carte ✔️
- [x] Créer les tests pour valider la position initiale ✔️

## Phase 2 : Tests d'Intégration

### 2.1 Tests de Base
- [x] Test de chargement de la nouvelle carte ✔️
- [x] Test de spawn du joueur ✔️
- [x] Test de conversion des coordonnées ✔️

### 2.2 Tests de Mouvement
- [x] Test de déplacement basique (4 directions) ✔️
- [x] Test de collision avec les obstacles ✔️
- [x] Test de mouvement diagonal ✔️
- [x] Test de la vitesse de déplacement ✔️

### 2.3 Tests de Rendu
- [x] Test de centrage de la caméra ✔️
- [x] Test de transition entre les calques ✔️
- [ ] Test de performance (FPS)

## Phase 3 : Implémentation

### 3.1 Système de Mouvement
- [x] Adapter la classe Player pour la nouvelle carte ✔️
- [x] Implémenter le mouvement diagonal ✔️
- [x] Optimiser la détection de collision ✔️

### 3.2 Rendu et Caméra
- [ ] Centrer la caméra sur le joueur
- [ ] Gérer les bords de la nouvelle carte
- [ ] Implémenter les transitions de calque

### 3.3 Optimisation
- [ ] Optimiser le chargement des ressources
- [ ] Améliorer les performances de rendu
- [ ] Réduire la consommation mémoire

## Phase 4 : Validation

### 4.1 Tests Finaux
- [ ] Exécuter la suite complète de tests
- [ ] Vérifier la fluidité du mouvement
- [ ] Valider les transitions visuelles

### 4.2 Documentation
- [ ] Mettre à jour la documentation technique
- [ ] Documenter les changements de structure
- [ ] Ajouter des exemples d'utilisation
