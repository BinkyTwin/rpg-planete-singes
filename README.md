# La Planète des Singes - RPG 🦍

Un jeu de rôle (RPG) basé sur l'univers de "La Planète des Singes", développé en Python avec Pygame.

## 📋 Prérequis

- Python 3.11 ou supérieur
- Un système d'exploitation Windows, macOS ou Linux

## 🚀 Installation et Lancement

Le jeu dispose maintenant d'un système d'installation automatique ! Pour commencer à jouer, suivez simplement ces étapes :

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/rpg-planete-singes.git
cd rpg-planete-singes
```

2. Lancez le jeu :
```bash
python main.py
```

C'est tout ! Le script s'occupera automatiquement de :
- Créer un environnement virtuel Python
- Installer toutes les dépendances nécessaires
- Lancer le jeu

## 🎮 Fonctionnalités du Jeu

- Création de personnage avec choix de race et de faction
- Système de combat au tour par tour
- Gestion d'inventaire
- Système de dialogue
- Carte du monde interactive
- Interface graphique avec Pygame

## 🛠️ Structure du Projet

```
rpg-planete-singes/
├── assets/               # Ressources du jeu (images, sons, etc.)
├── game/                 # Code source principal
│   ├── scenes/          # Scènes du jeu (menu, combat, etc.)
│   ├── items/           # Définition des objets du jeu
│   └── ...             
├── main.py              # Point d'entrée du jeu
├── setup_utils.py       # Utilitaires d'installation
└── requirements.txt     # Dépendances Python
```

## 🔧 Développement

Pour les développeurs souhaitant contribuer au projet :

1. Les dépendances sont gérées dans `requirements.txt`
2. L'environnement virtuel est créé dans le dossier `venv/`
3. Le système d'installation automatique est géré par `setup_utils.py`

Pour installer manuellement les dépendances (si nécessaire) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix
# ou
venv\Scripts\activate     # Sur Windows
pip install -r requirements.txt
```

## ⚠️ Résolution des Problèmes

Si vous rencontrez des erreurs lors du lancement :

1. Vérifiez que Python 3.11+ est installé :
```bash
python --version
```

2. Assurez-vous que tous les fichiers sont présents :
- `main.py`
- `setup_utils.py`
- `requirements.txt`

3. Les messages d'erreur du jeu commencent par `[ERREUR]` et fournissent des informations sur le problème.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- L'univers de "La Planète des Singes"
- La communauté Pygame
- Tous les contributeurs du projet
