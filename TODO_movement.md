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
