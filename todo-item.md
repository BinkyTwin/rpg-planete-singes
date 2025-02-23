# TODO - Système d'Items Interactifs

## Objectif
Créer un système d'items flexible et facilement extensible qui permet d'ajouter de nouveaux items sur la carte avec leurs propriétés spécifiques.

## Architecture Proposée
- [x] Créer une classe de base `CollectibleItem` qui hérite de `Item`
- [x] Utiliser le pattern Factory pour créer différents types d'items
- [x] Centraliser la logique d'interaction et de collecte
- [x] Utiliser un système de configuration pour définir les items et leurs positions

## Tests à Implémenter

### Tests de Base
- [x] Test de la classe CollectibleItem
  - [x] Création d'un item avec position et image
  - [x] Vérification des propriétés de base (type, valeur, description)
  - [x] Test de l'affichage sur la carte

### Tests d'Interaction
- [x] Test du système d'interaction
  - [x] Détection de la proximité du joueur
  - [x] Réponse à la touche 'E'
  - [x] Affichage de la boîte de dialogue
  - [x] Collecte de l'item

### Tests d'Intégration
- [x] Test avec différents types d'items
  - [x] Test avec une arme (M16)
  - [x] Test avec une potion (Banane)
  - [x] Vérification de l'ajout à l'inventaire
  - [x] Vérification de la disparition de la carte

### Tests de Factory
- [x] Test du système de création d'items
  - [x] Création d'items via configuration
  - [x] Validation des propriétés spécifiques
  - [x] Gestion des erreurs de configuration

## Tâches

### Phase 1 - Refactoring
- [x] Créer la classe CollectibleItem
- [x] Implémenter le système de Factory
- [x] Centraliser la logique d'interaction
- [x] Créer le système de configuration d'items

### Phase 2 - Implémentation
- [x] Adapter les items existants (M16, Banane)
- [x] Implémenter le système de collecte unifié
- [x] Ajouter le système de feedback visuel
- [x] Mettre en place la gestion d'inventaire

### Phase 3 - Tests et Validation
- [x] Exécuter la suite de tests complète
- [x] Vérifier les cas limites
- [x] Tester l'ajout d'un nouvel item
- [x] Valider l'expérience utilisateur

### Phase 4 - Améliorations UI/UX
- [x] Améliorer l'affichage de la boîte de dialogue
  - [x] Ajouter un retour à la ligne après la question principale
  - [x] Réduire la taille de la police pour les statistiques
  - [x] Améliorer la mise en page générale
- [x] Corriger la disparition des items
  - [x] S'assurer que l'item disparaît visuellement après la collecte
  - [x] Vérifier que l'état "collected" est correctement mis à jour
  - [ ] Ajouter une animation de collecte (optionnel)
