    Créer deux fichiers de documentation :
        cdc-pnj.md (Cahier des Charges) :
            Décrire la User Story : “En tant que joueur, je veux rencontrer un PNJ ‘orang_outan’ (même faction que moi), discuter avec lui pour lancer/mettre à jour une quête, puis le voir disparaître une fois le dialogue terminé.”
            Lister les critères d’acceptation (position éloignée, sprite orang_outan.png, dialogue en plusieurs messages, disparition du PNJ à la fin).
            Détailler les sous-tâches (classe PNJ, déclenchement du dialogue, intégration à la map Pygame, suppression du PNJ).
        todo-pnj.md (Approche TDD) :
            Lister les tests (par ex. test_pnj_creation, test_pnj_dialogue_flow, test_pnj_disappears_after_dialogue, etc.).
            Expliquer brièvement comment valider la disparition du PNJ au dernier message.

    Fonctionnalités à implémenter ou compléter :
        PNJ
            Race “orang_outan”.
            Même faction que le joueur (player.faction).
            Sprite = orang_outan.png.
            Position à distance (par ex. coins opposés, ou coordonnées (10,10) si le joueur est (1,1)).
        Interaction / Dialogue
            Quand le joueur entre en collision avec le PNJ ou s’en approche suffisamment, afficher les messages du PNJ (un par touche pressée).
            À la fin du dialogue (dernier message “au revoir”), supprimer instantanément le PNJ de la map (ex. retirer son sprite, retirer l’objet PNJ de la liste des entités).
        Mise à jour / Déclenchement de quête
            Au moment où le PNJ disparaît, marquer un objectif comme terminé ou en créer un nouveau dans QuestSystem.

    Production attendue
        Fichiers cdc-pnj.md et todo-pnj.md.
        Code pour :
            Créer ce PNJ orang_outan.
            L’afficher sur la map.
            Gérer le dialogue (multi-messages).
            Le faire disparaître (enlever son sprite, instance) une fois le dialogue fini.
            Mettre à jour ou activer une quête.
        Exemple d’intégration dans le fichier principal ou dans la scène de jeu (GameScene), montrant la création du PNJ, son placement, la détection de collision, l’affichage du dialogue, puis la disparition au dernier message.

Merci de tout générer (docs + code + exemple d’utilisation) !