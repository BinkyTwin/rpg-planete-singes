# La Planète des Singes - RPG

## Introduction

"La Planète des Singes - RPG" est un jeu de rôle développé en Python utilisant la bibliothèque Pygame. Ce projet propose une aventure immersive où le joueur incarne un personnage évoluant dans un univers riche en quêtes, combats et interactions avec divers personnages non joueurs.

## Structure du Projet

- **main.py** : Point d'entrée principal du jeu. Il gère la configuration de l'environnement virtuel, l'installation automatique des dépendances et le lancement du jeu.
- **requirements.txt** : Liste des dépendances nécessaires (par exemple, Pygame).
- **venv/** : Environnement virtuel créé automatiquement lors du premier lancement.
- **game/** : Dossier regroupant l'ensemble des modules du jeu, incluant :
  - **player.py** : Définition et gestion du personnage joueur.
  - **factions.py** : Gestion des factions et des caractéristiques associées.
  - **inventory.py** : Gestion de l'inventaire du joueur.
  - **map.py**, **combat_system.py**, etc.
  - **scenes/** : Dossier contenant les différentes scènes du jeu (Menu, Création de Personnage, Jeu, Message de Combat, etc.).

## Installation et Exécution

### Prérequis

- Python 3.x (assurez-vous que Python et pip sont installés).
- Accès à Internet pour l'installation des dépendances (la première exécution télécharge automatiquement les modules nécessaires via pip).

### Étapes d'Installation et d'Exécution

1. **Cloner ou télécharger le projet** dans le répertoire de votre choix.

2. **Naviguer dans le répertoire du projet** via votre terminal :

   ```bash
   cd chemin/vers/rpg-planete-singes
   ```

3. **Lancer le jeu** :

   Le script `main.py` s'occupe de créer un environnement virtuel (dossier `venv/`) si celui-ci n'existe pas, et installe automatiquement les dépendances listées dans `requirements.txt`.

   Pour exécuter le jeu, utilisez la commande suivante :

   ```bash
   python main.py
   ```

   Si le projet n'est pas encore dans un environnement virtuel, le script se relancera automatiquement dans le bon contexte après avoir créé l'environnement et installé les dépendances.

## Contrôles et Fonctionnalités du Jeu

- **Menu Principal** : Choix entre "Nouvelle Partie", "Charger Partie", "Options" ou "Quitter" à l'aide des touches directionnelles ou de la souris.
- **Création de Personnage** : Saisie du nom, sélection de la race et de la faction du personnage.
- **Gameplay**:
  - **Mouvement**: Utilisez les touches ZQSD ou les flèches pour déplacer votre personnage.
  - **Interaction**: Appuyez sur la touche E pour interagir avec l'environnement (dialogues, objets, PNJ, etc.).
  - **Combat**: Engagez des combats contre des ennemis avec des mécanismes de combat détaillés et des bonus selon la race et l'arme équipée.
- **Interface**: Affichage des scènes, dialogues dynamiques, inventaire, et gestion des quêtes.

## Tests Unitaires

Chaque nouvelle fonctionnalité est accompagnée de tests unitaires pour assurer la robustesse du code. Pour exécuter ces tests (lorsqu'ils sont disponibles) :

1. Installez `pytest` (si ce n'est pas déjà fait) :

   ```bash
   pip install pytest
   ```

2. Exécutez les tests à la racine du projet :

   ```bash
   pytest
   ```

*(Note : Certains tests peuvent être en cours de développement pour certaines fonctionnalités.)*

## Contributeurs

- Auteur principal : Manissa Bouda , Abdelatif Djeddou , Mathis Beauchamp, Diahra Traore, Ghezlan Ben Bennasser, Reda Oubenal

---

Bonne aventure dans "La Planète des Singes - RPG" ! Profitez pleinement de votre exploration dans cet univers riche et dynamique.
