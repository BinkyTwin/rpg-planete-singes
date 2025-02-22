# CDC - Item M16

## User Story

En tant que joueur, je veux voir l'item **M16** apparaître sur la carte à la position (5,17) avec l'icône `M16_full.png`, afin de décider de le ramasser ou non via une bulle de confirmation (oui/non).

## Critères d'acceptation

- L’item **M16** est visible sur la map à la position (5,17).
- Lorsqu’on se trouve sur la même tuile, appuyer sur la touche **E** affiche une bulle de confirmation (oui/non).
- Si le joueur choisit **oui**, l’item est supprimé de la map et ajouté à l’inventaire.
- Si le joueur choisit **non**, l’item reste sur la map.

## Dépendances

- Système d'inventaire pour gérer les items ramassés.
- Système d'affichage pour l’item et la bulle de confirmation.
- Détection de collision et interaction joueur/item.
- Gestion des assets pour charger et afficher l'image `M16_full.png`.
