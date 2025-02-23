## Cahier des charges pour la fonctionnalité PNJ 2 

## Fonctionnement du système de PNJ sur notre jeu
D'après l'analyse du code, voici comment fonctionne le système de PNJ dans la version graphique :

Création du PNJ
Le PNJ est défini dans la classe PNJ (pnj.py)
Il est initialisé avec une position fixe (20, 27) dans la carte
Il utilise un sprite d'orang-outan chargé depuis assets/tilesets/images/orang_outan.png
Le sprite est découpé en 4 frames pour l'animation (bien que seule la première frame soit utilisée actuellement)
Intégration dans la scène de jeu Dans game_scene.py, le PNJ est initialisé dans le constructeur de GameScene :
python
CopyInsert
# Initialisation du PNJ
self.pnj = PNJ(position=(20, 27))
if self.game_state.player:
    self.pnj.sync_faction(self.game_state.player)
Interaction avec le PNJ L'interaction se fait via la touche 'E' et est gérée dans la méthode handle_event :
Quand le joueur appuie sur 'E' près du PNJ, le système vérifie si :
Le PNJ est visible (self.pnj.is_visible)
Le joueur est assez proche (can_trigger_dialogue)
Le PNJ n'est pas déjà en dialogue
Si ces conditions sont remplies, un dialogue démarre avec start_dialogue()
Le dialogue peut être avancé avec la touche ESPACE (next_message())
Système de dialogue
Le PNJ peut avoir plusieurs messages à afficher
Les messages sont affichés séquentiellement quand le joueur appuie sur ESPACE
Le système garde une trace de l'état du dialogue (is_in_dialogue)
Synchronisation avec le joueur
Le PNJ est synchronisé avec la faction du joueur au démarrage via sync_faction
Cela permet probablement de déterminer si le PNJ est amical ou hostile envers le joueur
C'est un système plus élaboré que la version précédente des ennemis, car il permet :

Une position fixe et permanente du PNJ
Des interactions via dialogue
Une représentation graphique avec sprite
Une intégration avec le système de factions
Une interaction contextuelle basée sur la proximité du joueur

## Comment va fonctionner le nouveau PNJ ?

Bien pour ce nouveau PNJ, je voudrais que tu prenne la meme chose que le PNJ numéro 1, que tu copie colle limite, et que tu le mettes à la position (14,10)