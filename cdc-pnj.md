# Cahier des Charges - PNJ

## User Story

En tant que joueur, je veux rencontrer un PNJ de type `orang_outan` (même faction que moi) afin de discuter avec lui pour lancer ou mettre à jour une quête, puis voir le PNJ disparaître une fois le dialogue terminé.

## Critères d'Acceptation

- **Position** : Le PNJ doit apparaître à la position (20, 27) (en tuiles) sur la map.
- **Sprite** : Le PNJ utilise le sprite `orang_outan.png` et doit être affiché correctement (avec transparence et sans artefacts).
- **Dialogue** : Le système de dialogue doit gérer plusieurs messages, dont le dernier message est "au revoir".
- **Disparition** : Le PNJ doit disparaître immédiatement de la map à la fin du dialogue (retrait de son sprite et suppression de l'objet PNJ de la liste des entités).

## Sous-tâches

- Créer la classe `PNJ` avec les attributs nécessaires (race, faction, sprite, position).
- Implémenter le déclenchement du dialogue lors de la proximité du joueur (collision ou proximité suffisante).
- Intégrer le PNJ à la map Pygame dès le début du jeu après création du joueur.
- Assurer la suppression du PNJ à la fin du dialogue, une fois le message "au revoir" affiché.
