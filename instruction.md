    Crée un fichier cdc-item.md qui décrit :
        La User Story du joueur qui voit un item “M16” sur la position (5,17) (image M16_full.png) et peut décider de le ramasser ou non (via une bulle de confirmation oui/non).
        Les critères d’acceptation (visibility de l’item, interaction en étant sur la même tuile, popup, ajout dans l’inventaire ou persistance sur la map).
        Les dépendances (système d’inventaire, système d’affichage, etc.).

    Crée un fichier todo-item.md (Approche TDD) :
        Liste les tests principaux :
            Test de présence de l’item “M16” sur (5,17).
            Test de l’ouverture de la bulle de confirmation à l’appui de la touche ‘E’.
            Test de l’ajout de l’item dans l’inventaire si l’on choisit “oui”.
            Test de la persistance de l’item sur la map si l’on choisit “non”.

    Implémente la fonctionnalité :
        L’item “M16” (avec M16_full.png pour l’icône) apparaît à la position (5,17).
        Lorsqu’on se trouve sur la même tuile et qu’on appuie sur ‘E’, une fenêtre ou bulle de confirmation apparaît (oui/non).
        Si on choisit oui, l’item est retiré de la map et ajouté à l’inventaire.
        Si on choisit non, l’item reste disponible à (5,17).
        Montre un exemple d’intégration de cette logique dans le code principal ou dans une scène de jeu (comment détecter la touche ‘E’, etc.).

Merci de :

    Générer d’abord cdc-item.md et todo-item.md.
    Génére les test unitères nécessaire pour valider la fonctionnalité.
    Puis produire tout le code nécessaire pour que cette feature soit opérationnelle, avec l’affichage de l’item sur la map, la détection de collision/interaction, la confirmation, et la gestion dans l’inventaire.
    Réaliser les tests et valide chacun de ces tests.