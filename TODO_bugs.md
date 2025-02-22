# TODO Liste des Bugs à Corriger

## 1. Menu Principal
- [x] Restaurer la navigation à la souris
  - [x] Créer test pour vérifier la détection des clics de souris
  - [x] Implémenter la détection des clics dans MenuScene
  - [x] Ajouter des zones cliquables pour chaque option du menu
- [ ] Améliorer l'interface du menu
  - [ ] Ajouter un rectangle blanc de sélection au survol de la souris
  - [ ] Ajouter un message "Aucune partie sauvegardée" pour l'option Charger Partie
  - [ ] Ajouter un message "En cours de construction" pour l'option Options
  - [ ] Ajouter un bouton Retour dans l'écran de création de personnage

## 2. Navigation Menu
- [x] Corriger les options de navigation
  - [x] Test pour vérifier toutes les options du menu (Nouvelle Partie, Charger, Options, Quitter)
  - [x] Implémenter la logique pour chaque option
  - [x] Ajouter des retours visuels lors de la sélection

## 3. Affichage de la Map
- [x] Corriger l'échelle et le dimensionnement
  - [x] Test pour vérifier les dimensions de la map par rapport à l'écran
  - [x] Ajuster le système de rendu pour maintenir les proportions
  - [x] Éliminer la bande noire à droite en plein écran
    - Modifié update_scale pour remplir tout l'écran
  - [x] Assurer que la map s'affiche correctement dans toutes les résolutions
    - Retiré le calque "arrière plan" inutile de la mapV3
- [ ] Corriger l'affichage de la map
  - [x] Ajuster le système de rendu pour maintenir les proportions
  - [x] Éliminer la bande noire à droite en plein écran
  - [ ] Supprimer les traits noirs entre les tuiles
  - [x] Retirer le calque "arrière plan" inutile
  - [ ] Vérifier l'ordre des calques (sol, feuilles, obstacles)

## 4. Système de Collisions
- [x] Restaurer le système de collisions
  - [x] Test pour vérifier la détection des collisions avec les murs
    - Modifié is_collision pour utiliser le calque "obstacles"
  - [ ] Test pour vérifier la détection des collisions avec les objets
  - [x] Implémenter la logique de collision dans la classe Player
    - Modifié la méthode move pour gérer correctement les collisions
  - [x] Assurer que les collisions fonctionnent avec l'échelle modifiée
- [ ] Corriger le système de collisions
  - [ ] Implémenter les collisions avec le calque "obstacles"
  - [ ] Gérer les collisions avec les arbres du calque "feuilles"
  - [ ] Permettre le déplacement sur le calque "sol"
  - [ ] Tester les collisions dans toutes les directions

## 5. Caméra Fixe
- [ ] Modifier le système de caméra
  - [ ] Test pour vérifier que la caméra reste fixe
  - [ ] Implémenter une caméra statique dans TiledMap
  - [ ] Ajuster le rendu pour une vue fixe de la map
  - [ ] Assurer que le joueur se déplace correctement dans la vue fixe

## Ordre de Priorité
1. ~~Affichage de la Map (critique pour la jouabilité)~~ ✓
2. ~~Système de Collisions (sécurité du gameplay)~~ ✓
3. Caméra Fixe (demande spécifique)
4. ~~Menu Principal (qualité de vie)~~ ✓
5. ~~Navigation Menu (qualité de vie)~~ ✓
6. Menu Principal (interface utilisateur)
7. Système de Collisions (gameplay)
8. Affichage de la Map (visuel)
9. Caméra Fixe (gameplay)

## Notes de Test
- Chaque correction a été accompagnée de tests unitaires
- Les tests vérifient le comportement avant et après correction
- Les changements sont documentés dans le code pour référence future
- Chaque correction doit être accompagnée de tests unitaires
- Les tests doivent vérifier le comportement avant et après correction
- Documenter les changements dans le code pour référence future
