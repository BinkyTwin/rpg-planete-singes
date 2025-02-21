## Fonctionnalité de gestion des mouvements

### Contrôles
- [x] Implémenter les contrôles Z/Q/S/D + flèches directionnelles ✔️
- [ ] Gérer la vitesse de déplacement et l'animation du personnage

### Gestion de la map
- [ ] Implémenter le système de calques :
  - [ ] Calque "collisions" (bloque le mouvement)
  - [ ] Calque "sol" (mouvement autorisé)
  - [ ] Calque "three" (gestion de la profondeur graphique)
- [ ] Empêcher le personnage de sortir des limites de la map
- [ ] Créer un système de détection de collision avec les obstacles

### Apparence du personnage
- [ ] Charger les sprites depuis le dossier "character"
- [ ] Associer chaque race de singe à son sprite correspondant
- [ ] Implémenter le changement de layer graphique pour le calque "three"

### Initialisation
- [ ] Positionner le personnage sur le calque "sol" aux coordonnées (1,12)
- [ ] Vérifier que la position initiale est valide (pas sur une collision)

### Tests
- [ ] Tester tous les types de déplacement
- [ ] Tester les collisions avec différents obstacles
- [ ] Tester le rendu graphique sur le calque "three"
