# Todo Liste pour l'implémentation du PNJ 2

## Modifications du code

- [x] Modifier la classe [GameScene](cci:2://file:///c:/Users/djedd/Desktop/EMLV/Python/RPG/rpg-planete-singes/game/scenes/game_scene.py:8:0-453:33) pour ajouter un second PNJ
  - [x] Ajouter un attribut `pnj2` dans le constructeur
  - [x] Initialiser le PNJ2 avec la position (14,10)
  - [x] Synchroniser la faction avec le joueur comme pour le PNJ1

- [x] Adapter la méthode [handle_event](cci:1://file:///c:/Users/djedd/Desktop/EMLV/Python/RPG/rpg-planete-singes/game/scenes/game_scene.py:74:4-127:19) dans [GameScene](cci:2://file:///c:/Users/djedd/Desktop/EMLV/Python/RPG/rpg-planete-singes/game/scenes/game_scene.py:8:0-453:33)
  - [x] Ajouter la vérification d'interaction pour le PNJ2
  - [x] Implémenter la détection de proximité pour le PNJ2
  - [x] Gérer le déclenchement du dialogue pour le PNJ2

- [x] Système de dialogue
  - [x] Adapter le système pour gérer les dialogues du PNJ2
  - [x] S'assurer que les deux PNJ peuvent avoir des dialogues indépendants

## Tests

- [x] Ajouter des tests pour le PNJ2
  - [x] Tester l'initialisation correcte à la position (14,10)
  - [x] Vérifier la synchronisation de faction
  - [x] Tester le système de dialogue

## Vérifications finales

- [ ] Tester le jeu avec les deux PNJ
- [ ] Vérifier qu'il n'y a pas de conflits d'interaction
- [ ] S'assurer que les dialogues fonctionnent correctement pour les deux PNJ