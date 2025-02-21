# Cahier des charges pour la fonctionnalité de la gestion des mouvements

Pour que le joueur puisse bouger, il faut :

- Qu'il puisse utiliser les touches Z/Q/S/D pour se deplacer ainsi que les fleches du clavier. 
- Il ne faut pas que le personnage sorte de la map

La map est situé dans une foret, avec quelque obstacle et des arbres, elle est divisé en 3 calques : 
- Le calque "collisions": 
    Ne doit pas permettre au joueur de traverser cette cellule, c'est en quelque sorte un mur 
- Le calque "sol": 
    Le joueur peut se deplacer sur ce calque.
- Le calque "three": 
    Le joueur peut se deplacer sur ce calque, cependant, je veux que l'image de mon personnage passe en arrière plan, de sorte qu'il soit invisible quand il passe sur ce calque.

-L'apparrance du personnage: 
Il y a sur le fichier "character" les image des personnages, pour chaque race de singe il y a un personnage correspondant.

- L'apparition du joueur devra se faire sur le calque "sol", à la position (1, 12)

