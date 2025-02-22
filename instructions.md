Cahier de charges (cdc-pnj.md)

User Story :
“En tant que joueur, je veux voir le PNJ s’afficher correctement (en entier) et pouvoir discuter avec lui en appuyant d’abord sur E pour démarrer la conversation, puis sur Espace pour faire défiler les messages étape par étape, jusqu’à ce que la discussion se termine et que le PNJ disparaisse.”
Problème actuel :
Le sprite du PNJ “orang_outan” n’apparaît qu’à moitié (probablement un souci de positionnement, d’ancrage ou de zone de rendu sur l’écran).
La discussion ne se déroule pas comme prévu : impossible de passer d’un message à l’autre avec une touche.
Objectif attendu :
Corriger l’affichage du PNJ afin qu’il soit complètement visible à l’écran.
Afficher un message “Appuyez sur E pour discuter” lorsque le joueur est suffisamment proche.
Au clic sur E, le premier message du PNJ s’affiche et le texte “Appuyez sur Espace pour continuer” apparaît.
Au clic sur Espace, on passe au message suivant, etc.
À la fin du dernier message, le PNJ disparaît de la map.

