#!/usr/bin/env python3
"""
La Planète des Singes - RPG
"""

import os
import sys
import pygame
from game.player import Player
from game.factions import FactionName, FACTIONS
from game.inventory import Inventory
from game.items import ITEMS, ItemType
from game.map import Map, TileType
from game.spawn_manager import SpawnManager
from game.combat_system import CombatSystem
from random import randint
import time
from game.dialogue_system import DialogueSystem
from game.game_state import GameState
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene
from game.scenes.character_creation_scene import CharacterCreationScene

class Game:
    def __init__(self):
        print("Initialisation du jeu...", flush=True)
        try:
            pygame.init()
            print("Pygame initialisé avec succès", flush=True)
            
            # Configuration de base
            self.WINDOW_WIDTH = 800
            self.WINDOW_HEIGHT = 600
            self.FPS = 60
            
            print("Création de la fenêtre...", flush=True)
            # Création de la fenêtre
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            pygame.display.set_caption("La Planète des Singes - RPG")
            print("Fenêtre créée avec succès", flush=True)
            
            # Horloge pour contrôler le FPS
            self.clock = pygame.time.Clock()
            
            print("Initialisation de l'état du jeu...", flush=True)
            # État du jeu
            self.game_state = GameState()
            print("État du jeu initialisé", flush=True)
            
            print("Chargement des scènes...", flush=True)
            # Scènes du jeu
            self.scenes = {
                'menu': MenuScene(self.screen, self.game_state),
                'game': GameScene(self.screen, self.game_state),
                'character_creation': CharacterCreationScene(self.screen, self.game_state)
            }
            self.current_scene = 'menu'
            print("Scènes chargées avec succès", flush=True)
            print("Initialisation terminée!", flush=True)
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de l'initialisation : {e}", flush=True)
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def handle_events(self):
        """Gère les événements globaux"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
                # Laisse la scène courante gérer l'événement
                new_scene = self.scenes[self.current_scene].handle_event(event)
                if new_scene and new_scene in self.scenes:
                    self.current_scene = new_scene
                
            return True
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de la gestion des événements : {e}", flush=True)
            import traceback
            traceback.print_exc()
            return False

    def update(self):
        """Met à jour l'état du jeu"""
        try:
            # Met à jour la scène courante
            self.scenes[self.current_scene].update()
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors de la mise à jour : {e}", flush=True)
            import traceback
            traceback.print_exc()

    def render(self):
        """Dessine le jeu"""
        try:
            # Efface l'écran
            self.screen.fill((0, 0, 0))
            
            # Dessine la scène courante
            self.scenes[self.current_scene].render()
            
            # Rafraîchit l'affichage
            pygame.display.flip()
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue lors du rendu : {e}", flush=True)
            import traceback
            traceback.print_exc()

    def run(self):
        """Boucle principale du jeu"""
        print("Démarrage de la boucle de jeu...", flush=True)
        try:
            running = True
            while running:
                # Gestion des événements
                running = self.handle_events()
                
                # Mise à jour
                self.update()
                
                # Rendu
                self.render()
                
                # Contrôle du FPS
                self.clock.tick(self.FPS)
                
            print("Fermeture du jeu...", flush=True)
            pygame.quit()
            sys.exit()
        except Exception as e:
            print(f"[ERREUR] Une erreur est survenue dans la boucle principale : {e}", flush=True)
            import traceback
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)

def afficher_races_disponibles():
    print("\nRaces disponibles :", flush=True)
    races_list = list(Player.RACES.keys())
    for i, race in enumerate(races_list, 1):
        print(f"\n{i}. {race.capitalize()} :", flush=True)
        for stat, value in Player.RACES[race].items():
            print(f"  - {stat.capitalize()}: {value}", flush=True)
    return races_list

def afficher_factions_disponibles():
    print("\nFactions disponibles :", flush=True)
    factions_list = list(FactionName)
    for i, faction in enumerate(factions_list, 1):
        faction_obj = FACTIONS[faction]
        print(f"\n{i}. {faction.value} :", flush=True)
        print(f"  {faction_obj.description}", flush=True)
    return factions_list

def afficher_inventaire(player):
    print("\n=== Inventaire ===", flush=True)
    items = player.inventory.get_items()
    if not items:
        print("L'inventaire est vide", flush=True)
    else:
        print(f"Slots utilisés : {len(items)}/{player.inventory.max_slots}", flush=True)
        print("\nObjets :", flush=True)
        for i, item in enumerate(items, 1):
            equipped = " [ÉQUIPÉ]" if item == player.inventory.get_equipped_item() else ""
            print(f"{i}. {item}{equipped}", flush=True)
    
    equipped_item = player.inventory.get_equipped_item()
    if equipped_item:
        print(f"\nItem équipé : {equipped_item}", flush=True)
    else:
        print("\nAucun item équipé", flush=True)

def gerer_inventaire(player, game_map, spawn_manager):
    while True:
        print("\n=== Gestion de l'inventaire ===", flush=True)
        print("1. Voir l'inventaire", flush=True)
        print("2. Ramasser un objet", flush=True)
        print("3. Jeter un objet", flush=True)
        print("4. Équiper/Déséquiper un objet", flush=True)
        print("5. Retour au menu principal", flush=True)
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            afficher_inventaire(player)
        
        elif choix == "2":
            # Vérifie s'il y a un objet sur la position actuelle du joueur
            x, y = game_map.player_pos
            item = spawn_manager.get_item_at_position(x, y)
            
            if not item:
                print("\nIl n'y a aucun objet à ramasser ici.", flush=True)
                continue
                
            print("\n=== Objet disponible ===", flush=True)
            print(f"Nom : {item.name}", flush=True)
            print(f"Type : {item.item_type.value}", flush=True)
            print(f"Description : {item.description}", flush=True)
            print(f"Valeur : {item.value}", flush=True)
            
            while True:
                choix = input("\nVoulez-vous ramasser cet objet ? (o/n) : ").lower().strip()
                if choix == 'o':
                    if player.inventory.add_item(item):
                        spawn_manager.remove_item(x, y)
                        print(f"\nVous avez ramassé : {item.name}", flush=True)
                    else:
                        print("\nVotre inventaire est plein !", flush=True)
                    break
                elif choix == 'n':
                    print("\nVous laissez l'objet au sol.", flush=True)
                    break
                else:
                    print("Choix invalide. Veuillez répondre par 'o' (oui) ou 'n' (non).", flush=True)
        
        elif choix == "3":
            items = player.inventory.get_items()
            if not items:
                print("\nL'inventaire est vide", flush=True)
                continue
                
            afficher_inventaire(player)
            try:
                choix_item = int(input("\nChoisissez un objet à jeter (numéro) : "))
                if 1 <= choix_item <= len(items):
                    item = items[choix_item - 1]
                    x, y = game_map.player_pos
                    
                    # Vérifie si la case actuelle est déjà occupée par un item
                    if spawn_manager.get_item_at_position(x, y):
                        print("\nIl y a déjà un objet ici. Déplacez-vous pour jeter cet objet.", flush=True)
                        continue
                    
                    if player.inventory.remove_item(item):
                        # Ajoute l'item à la position actuelle du joueur
                        game_map.add_item(TileType.ITEM, x, y)
                        spawn_manager.spawned_items.append((item, x, y))
                        print(f"\nVous avez jeté : {item.name}", flush=True)
                else:
                    print("\nNuméro d'objet invalide", flush=True)
            except ValueError:
                print("\nVeuillez entrer un numéro valide", flush=True)
        
        elif choix == "4":
            items = player.inventory.get_items()
            if not items:
                print("\nL'inventaire est vide", flush=True)
                continue
            
            print("\n=== Équipement ===", flush=True)
            equipped_item = player.inventory.get_equipped_item()
            if equipped_item:
                print(f"Item actuellement équipé : {equipped_item}", flush=True)
                if input("\nVoulez-vous le déséquiper ? (o/n) : ").lower().strip() == 'o':
                    player.inventory.unequip_item()
                    print("Item déséquipé.", flush=True)
                continue

            print("\nObjets équipables :", flush=True)
            equipable_items = [(i, item) for i, item in enumerate(items, 1) 
                             if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]]
            
            if not equipable_items:
                print("Aucun objet équipable dans l'inventaire", flush=True)
                continue

            for i, item in equipable_items:
                print(f"{i}. {item}", flush=True)
            
            try:
                choix_item = int(input("\nChoisissez un objet à équiper (0 pour annuler) : "))
                if choix_item == 0:
                    continue
                if 1 <= choix_item <= len(equipable_items):
                    item = equipable_items[choix_item - 1][1]
                    if player.inventory.equip_item(item):
                        print(f"\n{item.name} a été équipé !", flush=True)
                    else:
                        print("\nImpossible d'équiper cet objet.", flush=True)
                else:
                    print("\nNuméro d'objet invalide", flush=True)
            except ValueError:
                print("\nVeuillez entrer un numéro valide", flush=True)
        
        elif choix == "5":
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.", flush=True)

def creer_personnage():
    print("=== Création de votre personnage ===\n", flush=True)
    
    # Demande du nom
    while True:
        name = input("Entrez le nom de votre personnage : ").strip()
        if name:
            break
        print("Le nom ne peut pas être vide.", flush=True)

    # Choix de la race
    while True:
        races_list = afficher_races_disponibles()
        try:
            choix = int(input("\nChoisissez votre race (entrez le numéro) : "))
            if 1 <= choix <= len(races_list):
                race = races_list[choix - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(races_list)}", flush=True)
        except ValueError:
            print("Veuillez entrer un numéro valide", flush=True)

    # Choix de la faction
    while True:
        factions_list = afficher_factions_disponibles()
        try:
            choix = int(input("\nChoisissez votre faction (entrez le numéro) : "))
            if 1 <= choix <= len(factions_list):
                faction_match = factions_list[choix - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(factions_list)}", flush=True)
        except ValueError:
            print("Veuillez entrer un numéro valide", flush=True)

    # Création du personnage avec un inventaire
    player = Player(name, 0, 0, race, faction_match)
    player.inventory = Inventory()  # Ajout de l'inventaire
    
    print("\n=== Personnage créé avec succès ! ===", flush=True)
    player.print_player()
    
    return player

def gerer_deplacement(player, game_map, spawn_manager, dialogue_system):
    while True:
        print("\n=== Déplacement ===", flush=True)
        game_map.display()
        print("\nCommandes :", flush=True)
        print("z - Haut", flush=True)
        print("s - Bas", flush=True)
        print("q - Gauche", flush=True)
        print("d - Droite", flush=True)
        print("r - Retour au menu principal", flush=True)
        
        commande = input("\nVotre choix : ").lower().strip()
        
        if commande == "z":
            success, message, item_pos, rencontre_pnj = game_map.move_player(0, -1)
        elif commande == "s":
            success, message, item_pos, rencontre_pnj = game_map.move_player(0, 1)
        elif commande == "q":
            success, message, item_pos, rencontre_pnj = game_map.move_player(-1, 0)
        elif commande == "d":
            success, message, item_pos, rencontre_pnj = game_map.move_player(1, 0)
        elif commande == "r":
            break
        else:
            print("Commande invalide", flush=True)
            continue

        if message:
            print(f"\n{message}", flush=True)
            
        # Gestion de la rencontre avec le PNJ
        if rencontre_pnj:
            message = dialogue_system.start_dialogue()
            while message:
                dialogue_system.display_message(message)
                message = dialogue_system.next_message()
            
            # Fait disparaître le PNJ après le dialogue
            if dialogue_system.is_dialogue_finished():
                x, y = game_map.npc_pos
                game_map.remove_item(x, y)  # Enlève le PNJ de la carte
                game_map.npc_pos = None     # Efface la position du PNJ
            continue

        # Gestion de la découverte d'items
        if item_pos:
            x, y = item_pos
            item = spawn_manager.get_item_at_position(x, y)
            if item:
                print("\n=== Objet trouvé ! ===", flush=True)
                print(f"Nom : {item.name}", flush=True)
                print(f"Type : {item.item_type.value}", flush=True)
                print(f"Description : {item.description}", flush=True)
                print(f"Valeur : {item.value}", flush=True)
                
                while True:
                    choix = input("\nVoulez-vous ramasser cet objet ? (o/n) : ").lower().strip()
                    if choix == 'o':
                        if player.inventory.add_item(item):
                            spawn_manager.remove_item(x, y)
                            print(f"\nVous avez ramassé : {item.name}", flush=True)
                        else:
                            print("\nVotre inventaire est plein !", flush=True)
                            # Remet le symbole de l'item sur la carte
                            game_map.add_item(TileType.ITEM, x, y)
                        break
                    elif choix == 'n':
                        # Remet le symbole de l'item sur la carte
                        game_map.add_item(TileType.ITEM, x, y)
                        print("\nVous laissez l'objet au sol.", flush=True)
                        break
                    else:
                        print("Choix invalide. Veuillez répondre par 'o' (oui) ou 'n' (non).", flush=True)
        
        # Met à jour le spawn manager avec la faction du joueur
        spawn_manager.update_with_player_faction(player.faction)
        
        # Après chaque déplacement réussi
        if success:
            # Vérifie si un ennemi est adjacent
            for enemy in spawn_manager.spawned_enemies:
                if enemy.is_adjacent_to(*game_map.player_pos):
                    print("\nUn ennemi est proche !", flush=True)
                    result = gerer_combat(player, enemy, game_map, spawn_manager)
                    if result == "dead":
                        return "dead"
                    elif result == "fled":  # Fuite
                        # Logique de fuite
                        pass

def gerer_combat(player, enemy, game_map, spawn_manager):
    while True:
        print("\n=== Combat ===", flush=True)
        print(f"Ennemi : {enemy.name} de la faction {enemy.faction.value}", flush=True)
        print(f"Points de vie de l'ennemi : {enemy.hp}", flush=True)
        print(f"Vos points de vie : {player.hp}", flush=True)
        
        if player.inventory.get_equipped_item():
            print(f"Arme équipée : {player.inventory.get_equipped_item()}", flush=True)
        else:
            print("Aucune arme équipée", flush=True)
        
        print("\nActions disponibles :", flush=True)
        print("1. Attaquer", flush=True)
        print("2. Se défendre (et accéder à l'inventaire)", flush=True)
        print("3. Tenter de fuir", flush=True)
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Phase d'attaque du joueur
            weapon = player.inventory.get_equipped_item()
            damage, is_fatal = CombatSystem.attack(player, enemy, weapon)
            print(f"\nVous infligez {damage} points de dégâts !", flush=True)
            
            if is_fatal:
                print("L'ennemi a été vaincu !", flush=True)
                return True
            
            # Phase d'attaque de l'ennemi
            enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon)
            print(f"L'ennemi vous inflige {enemy_damage} points de dégâts !", flush=True)
            
            if player_dead:
                print("Vous avez été vaincu !", flush=True)
                return "dead"
                
        elif choix == "2":
            print("\n=== Mode Défense ===", flush=True)
            print("1. Gérer l'inventaire", flush=True)
            print("2. Utiliser une potion", flush=True)
            print("3. Changer d'arme", flush=True)
            print("4. Retour au combat", flush=True)
            
            action = input("\nQue souhaitez-vous faire ? ").strip()
            
            if action == "1":
                gerer_inventaire(player, game_map, spawn_manager)
            elif action == "2":
                # Cherche les potions dans l'inventaire
                potions = [(i, item) for i, item in enumerate(player.inventory.get_items()) 
                          if item.item_type == ItemType.POTION]
                
                if not potions:
                    print("Vous n'avez pas de potions !", flush=True)
                else:
                    print("\nPotions disponibles :", flush=True)
                    for i, (_, potion) in enumerate(potions, 1):
                        print(f"{i}. {potion}", flush=True)
                    
                    try:
                        choix_potion = int(input("\nChoisissez une potion (0 pour annuler) : "))
                        if 1 <= choix_potion <= len(potions):
                            potion = potions[choix_potion-1][1]
                            player.hp = min(100, player.hp + potion.value)
                            player.inventory.remove_item(potion)
                            print(f"\nVous utilisez {potion.name} et récupérez {potion.value} HP !", flush=True)
                    except ValueError:
                        print("Choix invalide", flush=True)
                        
            elif action == "3":
                # Affiche les armes disponibles
                weapons = [(i, item) for i, item in enumerate(player.inventory.get_items()) 
                          if item.item_type == ItemType.WEAPON]
                
                if not weapons:
                    print("Vous n'avez pas d'armes !", flush=True)
                else:
                    print("\nArmes disponibles :", flush=True)
                    for i, (_, weapon) in enumerate(weapons, 1):
                        print(f"{i}. {weapon}", flush=True)
                    
                    try:
                        choix_arme = int(input("\nChoisissez une arme (0 pour annuler) : "))
                        if 1 <= choix_arme <= len(weapons):
                            weapon = weapons[choix_arme-1][1]
                            player.inventory.equip_item(weapon)
                            print(f"\nVous équipez {weapon.name} !", flush=True)
                    except ValueError:
                        print("Choix invalide", flush=True)
            
            # L'ennemi attaque avec dégâts réduits
            enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon, defense_mode=True)
            print(f"\nEn défense, l'ennemi vous inflige {enemy_damage} points de dégâts (réduits) !", flush=True)
            
            if player_dead:
                print("Vous avez été vaincu !", flush=True)
                return "dead"
                
        elif choix == "3":
            # Tentative de fuite basée sur l'agilité
            chance_fuite = player.race_stats['agilite'] * 10  # 50-90% selon l'agilité
            if randint(1, 100) <= chance_fuite:
                print("Vous parvenez à fuir le combat !", flush=True)
                # Calcule la direction opposée à l'ennemi
                dx = player.x - enemy.x
                dy = player.y - enemy.y
                
                # Normalise la direction (pour avoir un déplacement de 1 case)
                if dx != 0:
                    dx = dx // abs(dx)
                if dy != 0:
                    dy = dy // abs(dy)
                
                # Si le joueur est sur la même ligne/colonne que l'ennemi,
                # choisit une direction perpendiculaire
                if dx == 0 and dy == 0:
                    possible_moves = [(0,1), (0,-1), (1,0), (-1,0)]
                else:
                    # Essaie de s'éloigner de 2 cases dans la direction opposée à l'ennemi
                    possible_moves = [(dx*2, dy*2)]
                    # Ajoute aussi les directions perpendiculaires comme backup
                    if dx != 0:
                        possible_moves.extend([(dx, 1), (dx, -1)])
                    if dy != 0:
                        possible_moves.extend([(1, dy), (-1, dy)])
                
                # Essaie chaque mouvement possible jusqu'à en trouver un valide
                escaped = False
                for move_dx, move_dy in possible_moves:
                    new_x = player.x + move_dx
                    new_y = player.y + move_dy
                    if (game_map.is_valid_position(new_x, new_y) and 
                        game_map.grid[new_y][new_x] == TileType.EMPTY.value):
                        success, _, _ = game_map.move_player(move_dx, move_dy)
                        if success:
                            escaped = True
                            break
                
                if escaped:
                    return "fled"
                print("Mais vous êtes coincé !", flush=True)
            else:
                print("Tentative de fuite échouée !", flush=True)
                # L'ennemi attaque pendant la fuite
                enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon)
                print(f"L'ennemi vous inflige {enemy_damage} points de dégâts !", flush=True)
                
                if player_dead:
                    print("Vous avez été vaincu !", flush=True)
                    return "dead"
        else:
            print("Choix invalide", flush=True)

def charger_carte_png(chemin_fichier):
    """Charge et affiche la carte PNG avec Pygame"""
    try:
        # Initialisation de Pygame
        pygame.init()
        
        # Chargement de l'image PNG
        map_image = pygame.image.load(chemin_fichier)
        
        # Obtention des dimensions de l'image
        MAPWIDTH = map_image.get_width()
        MAPHEIGHT = map_image.get_height()
        
        # Création de la fenêtre
        screen = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))
        pygame.display.set_caption("La Planète des Singes - RPG")
        
        # Affichage de l'image
        screen.blit(map_image, (0, 0))
        pygame.display.flip()
        
        # Création de la carte pour le jeu (12x12 par défaut)
        game_map = Map(12, 12)
        game_map.generate_default_map()
        
        # Boucle d'attente pour voir la carte (5 secondes)
        start_time = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False  # Permet de passer l'affichage avec une touche
            
            # Quitte après 5 secondes
            if pygame.time.get_ticks() - start_time > 5000:
                running = False
        
        pygame.quit()
        return game_map
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors du chargement de la carte PNG : {e}", flush=True)
        pygame.quit()
        return None

def run_game():
    """Lance le jeu avec toutes les dépendances nécessaires."""
    print("Démarrage du jeu...", flush=True)
    try:
        game = Game()
        print("Lancement de la boucle de jeu...", flush=True)
        game.run()
    except Exception as e:
        print(f"[ERREUR] Une erreur est survenue lors de l'exécution du jeu : {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Si nous ne sommes pas déjà dans un environnement virtuel
    if not os.environ.get("VIRTUAL_ENV"):
        print("=== Configuration de l'environnement de jeu ===", flush=True)
        from setup_utils import setup_environment, get_python_executable
        
        if setup_environment():
            print("\n=== Lancement du jeu ===", flush=True)
            # Relance le script dans l'environnement virtuel
            python_path = get_python_executable()
            try:
                os.execv(python_path, [python_path, __file__])
            except Exception as e:
                print(f"[ERREUR] Erreur lors du lancement du jeu : {e}", flush=True)
                sys.exit(1)
        else:
            print("[ERREUR] Impossible de configurer l'environnement. Veuillez vérifier les erreurs ci-dessus.", flush=True)
            sys.exit(1)
    else:
        # Nous sommes dans l'environnement virtuel, lance le jeu
        run_game()