Tu as accès à tous les fichiers de mon projet RPG en Python utilisant Pygame. Le problème principal est que mon personnage apparaît plusieurs fois à l'écran (en 16 exemplaires au lieu d'un seul). Cela semble être un problème lié à la gestion des sprites ou au redessin dans la boucle principale. Les captures d'écran montrent aussi des artefacts noirs dans certaines zones de l'écran.
Objectif :

Diagnostiquer et corriger le problème de duplication du personnage ainsi que les artefacts graphiques. Utilise une approche systématique pour identifier la cause et proposer une solution robuste.
Instructions :

    Analyse du problème :

        Parcours les fichiers du projet pour identifier la gestion des sprites (création, ajout aux groupes, dessin, mise à jour).

        Vérifie la boucle principale (game loop) pour voir si l'écran est correctement effacé avant de redessiner les éléments.

        Recherche si le sprite du personnage est ajouté plusieurs fois à un groupe ou recréé à chaque itération.

    Approche TDD (Test-Driven Development) :

        Écris un test unitaire pour vérifier que le personnage n'est dessiné qu'une seule fois sur l'écran.

        Ajoute un test pour détecter les artefacts graphiques (par exemple, vérifier que les pixels noirs inattendus n'apparaissent pas après le rendu).

    Débogage :

        Ajoute des points de journalisation (logging) dans les sections critiques du code, comme la création des sprites et leur ajout aux groupes.

        Vérifie si des instances multiples du sprite sont créées ou manipulées.

    Correction :

        Si le problème vient d'une mauvaise gestion des groupes de sprites, corrige le code pour t'assurer que chaque sprite est ajouté une seule fois.

        Si le problème vient d'un écran qui n'est pas correctement réinitialisé, ajoute un appel à screen.fill() ou équivalent avant chaque redessin.

    Optimisation :

        Vérifie si la gestion de la caméra ou du scrolling interfère avec l'affichage.

        Assure-toi que seules les parties nécessaires de l'écran sont mises à jour (par exemple, via pygame.display.update() avec des rectangles spécifiques).

    Validation :

        Une fois les corrections apportées, exécute les tests unitaires pour valider que le problème est résolu.

        Fais une vérification visuelle en exécutant le jeu pour confirmer que le personnage s'affiche correctement et qu'il n'y a plus d'artefacts noirs.

    Documentation :

        Documente les changements effectués dans le code.

        Explique brièvement la cause du problème et comment il a été résolu.

Ressources disponibles :

    Tous les fichiers du projet (code source, assets graphiques, etc.).

    Les captures d'écran fournies comme référence visuelle.

    La possibilité d'exécuter et de tester le jeu.

Résultat attendu :

    Le personnage doit s'afficher une seule fois sur l'écran.

    Les artefacts graphiques noirs doivent disparaître.

    Le jeu doit fonctionner normalement sans perte de performance.
