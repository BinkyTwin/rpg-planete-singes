# Approche TDD - PNJ

## Phase 1: Correction du Sprite
- [x] Écrire le test `test_pnj_sprite_loading` pour vérifier le chargement du sprite `orang_outan.png`, incluant la vérification de la transparence et le découpage correct des frames.
- [x] Implémenter les corrections dans la classe `PNJ` pour assurer le chargement et l'affichage correct du sprite.
- [ ] Valider visuellement le rendu du PNJ sur la map.

## Phase 2: Amélioration du Dialogue
- [x] Écrire le test `test_pnj_dialogue_flow` pour simuler l'interaction : déclenchement du dialogue lorsque le joueur entre en collision ou s'approche, validation de l'attente de 500ms entre messages et passage au message suivant avec la touche `ESPACE`.
- [x] Modifier le système de dialogue pour activer le passage de message via la touche `ESPACE` et ajouter un délai minimum entre chaque message.
- [ ] Vérifier que le dialogue ne défile pas automatiquement et que le PNJ se supprime immédiatement après le dernier message "au revoir".

## Phase 3: Affichage du Message d'Aide 
- [x] Écrire le test `test_affichage_message_aide` pour vérifier l'affichage du message "Cliquez sur E pour discuter avec le pnj" lorsque le joueur est à proximité du PNJ.
- [x] Implémenter l'affichage permanent du message d'aide quand le joueur est proche, et son masquage pendant le dialogue.
- [ ] Valider l'intégration, la lisibilité et la réapparition du message après le dialogue.

## Validation Finale
- [ ] Exécuter l'ensemble des tests et vérifier visuellement l'intégration complète de la fonctionnalité PNJ dans le jeu.
- [ ] Documenter en détail les changements apportés et les validations effectuées.
