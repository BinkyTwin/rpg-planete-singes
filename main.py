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

def afficher_races_disponibles():
    print("\nRaces disponibles :")
    races_list = list(Player.RACES.keys())
    for i, race in enumerate(races_list, 1):
        print(f"\n{i}. {race.capitalize()} :")
        for stat, value in Player.RACES[race].items():
            print(f"  - {stat.capitalize()}: {value}")
    return races_list

def afficher_factions_disponibles():
    print("\nFactions disponibles :")
    factions_list = list(FactionName)
    for i, faction in enumerate(factions_list, 1):
        faction_obj = FACTIONS[faction]
        print(f"\n{i}. {faction.value} :")
        print(f"  {faction_obj.description}")
    return factions_list

def afficher_inventaire(player):
    print("\n=== Inventaire ===")
    items = player.inventory.get_items()
    if not items:
        print("L'inventaire est vide")
    else:
        print(f"Slots utilisés : {len(items)}/{player.inventory.max_slots}")
        print("\nObjets :")
        for i, item in enumerate(items, 1):
            equipped = " [ÉQUIPÉ]" if item == player.inventory.get_equipped_item() else ""
            print(f"{i}. {item}{equipped}")
    
    equipped_item = player.inventory.get_equipped_item()
    if equipped_item:
        print(f"\nItem équipé : {equipped_item}")
    else:
        print("\nAucun item équipé")

def gerer_inventaire(player, game_map, spawn_manager):
    while True:
        print("\n=== Gestion de l'inventaire ===")
        print("1. Voir l'inventaire")
        print("2. Ramasser un objet")
        print("3. Jeter un objet")
        print("4. Équiper/Déséquiper un objet")
        print("5. Retour au menu principal")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            afficher_inventaire(player)
        
        elif choix == "2":
            # Vérifie s'il y a un objet sur la position actuelle du joueur
            x, y = game_map.player_pos
            item = spawn_manager.get_item_at_position(x, y)
            
            if not item:
                print("\nIl n'y a aucun objet à ramasser ici.")
                continue
                
            print("\n=== Objet disponible ===")
            print(f"Nom : {item.name}")
            print(f"Type : {item.item_type.value}")
            print(f"Description : {item.description}")
            print(f"Valeur : {item.value}")
            
            while True:
                choix = input("\nVoulez-vous ramasser cet objet ? (o/n) : ").lower().strip()
                if choix == 'o':
                    if player.inventory.add_item(item):
                        spawn_manager.remove_item(x, y)
                        print(f"\nVous avez ramassé : {item.name}")
                    else:
                        print("\nVotre inventaire est plein !")
                    break
                elif choix == 'n':
                    print("\nVous laissez l'objet au sol.")
                    break
                else:
                    print("Choix invalide. Veuillez répondre par 'o' (oui) ou 'n' (non).")
        
        elif choix == "3":
            items = player.inventory.get_items()
            if not items:
                print("\nL'inventaire est vide")
                continue
                
            afficher_inventaire(player)
            try:
                choix_item = int(input("\nChoisissez un objet à jeter (numéro) : "))
                if 1 <= choix_item <= len(items):
                    item = items[choix_item - 1]
                    x, y = game_map.player_pos
                    
                    # Vérifie si la case actuelle est déjà occupée par un item
                    if spawn_manager.get_item_at_position(x, y):
                        print("\nIl y a déjà un objet ici. Déplacez-vous pour jeter cet objet.")
                        continue
                    
                    if player.inventory.remove_item(item):
                        # Ajoute l'item à la position actuelle du joueur
                        game_map.add_item(TileType.ITEM, x, y)
                        spawn_manager.spawned_items.append((item, x, y))
                        print(f"\nVous avez jeté : {item.name}")
                else:
                    print("\nNuméro d'objet invalide")
            except ValueError:
                print("\nVeuillez entrer un numéro valide")
        
        elif choix == "4":
            items = player.inventory.get_items()
            if not items:
                print("\nL'inventaire est vide")
                continue
            
            print("\n=== Équipement ===")
            equipped_item = player.inventory.get_equipped_item()
            if equipped_item:
                print(f"Item actuellement équipé : {equipped_item}")
                if input("\nVoulez-vous le déséquiper ? (o/n) : ").lower().strip() == 'o':
                    player.inventory.unequip_item()
                    print("Item déséquipé.")
                continue

            print("\nObjets équipables :")
            equipable_items = [(i, item) for i, item in enumerate(items, 1) 
                             if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]]
            
            if not equipable_items:
                print("Aucun objet équipable dans l'inventaire")
                continue

            for i, item in equipable_items:
                print(f"{i}. {item}")
            
            try:
                choix_item = int(input("\nChoisissez un objet à équiper (0 pour annuler) : "))
                if choix_item == 0:
                    continue
                if 1 <= choix_item <= len(equipable_items):
                    item = equipable_items[choix_item - 1][1]
                    if player.inventory.equip_item(item):
                        print(f"\n{item.name} a été équipé !")
                    else:
                        print("\nImpossible d'équiper cet objet.")
                else:
                    print("\nNuméro d'objet invalide")
            except ValueError:
                print("\nVeuillez entrer un numéro valide")
        
        elif choix == "5":
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

def creer_personnage():
    print("=== Création de votre personnage ===\n")
    
    # Demande du nom
    while True:
        name = input("Entrez le nom de votre personnage : ").strip()
        if name:
            break
        print("Le nom ne peut pas être vide.")

    # Choix de la race
    while True:
        races_list = afficher_races_disponibles()
        try:
            choix = int(input("\nChoisissez votre race (entrez le numéro) : "))
            if 1 <= choix <= len(races_list):
                race = races_list[choix - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(races_list)}")
        except ValueError:
            print("Veuillez entrer un numéro valide")

    # Choix de la faction
    while True:
        factions_list = afficher_factions_disponibles()
        try:
            choix = int(input("\nChoisissez votre faction (entrez le numéro) : "))
            if 1 <= choix <= len(factions_list):
                faction_match = factions_list[choix - 1]
                break
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(factions_list)}")
        except ValueError:
            print("Veuillez entrer un numéro valide")

    # Création du personnage avec un inventaire
    player = Player(name, 0, 0, race, faction_match)
    player.inventory = Inventory()  # Ajout de l'inventaire
    
    print("\n=== Personnage créé avec succès ! ===")
    player.print_player()
    
    return player

def gerer_deplacement(player, game_map, spawn_manager, dialogue_system):
    while True:
        print("\n=== Déplacement ===")
        game_map.display()
        print("\nCommandes :")
        print("z - Haut")
        print("s - Bas")
        print("q - Gauche")
        print("d - Droite")
        print("r - Retour au menu principal")
        
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
            print("Commande invalide")
            continue

        if message:
            print(f"\n{message}")
            
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
                print("\n=== Objet trouvé ! ===")
                print(f"Nom : {item.name}")
                print(f"Type : {item.item_type.value}")
                print(f"Description : {item.description}")
                print(f"Valeur : {item.value}")
                
                while True:
                    choix = input("\nVoulez-vous ramasser cet objet ? (o/n) : ").lower().strip()
                    if choix == 'o':
                        if player.inventory.add_item(item):
                            spawn_manager.remove_item(x, y)
                            print(f"\nVous avez ramassé : {item.name}")
                        else:
                            print("\nVotre inventaire est plein !")
                            # Remet le symbole de l'item sur la carte
                            game_map.add_item(TileType.ITEM, x, y)
                        break
                    elif choix == 'n':
                        # Remet le symbole de l'item sur la carte
                        game_map.add_item(TileType.ITEM, x, y)
                        print("\nVous laissez l'objet au sol.")
                        break
                    else:
                        print("Choix invalide. Veuillez répondre par 'o' (oui) ou 'n' (non).")
        
        # Met à jour le spawn manager avec la faction du joueur
        spawn_manager.update_with_player_faction(player.faction)
        
        # Après chaque déplacement réussi
        if success:
            # Vérifie si un ennemi est adjacent
            for enemy in spawn_manager.spawned_enemies:
                if enemy.is_adjacent_to(*game_map.player_pos):
                    print("\nUn ennemi est proche !")
                    result = gerer_combat(player, enemy, game_map, spawn_manager)
                    if result == "dead":
                        return "dead"
                    elif result == "fled":  # Fuite
                        # Logique de fuite
                        pass

def gerer_combat(player, enemy, game_map, spawn_manager):
    while True:
        print("\n=== Combat ===")
        print(f"Ennemi : {enemy.name} de la faction {enemy.faction.value}")
        print(f"Points de vie de l'ennemi : {enemy.hp}")
        print(f"Vos points de vie : {player.hp}")
        
        if player.inventory.get_equipped_item():
            print(f"Arme équipée : {player.inventory.get_equipped_item()}")
        else:
            print("Aucune arme équipée")
        
        print("\nActions disponibles :")
        print("1. Attaquer")
        print("2. Se défendre (et accéder à l'inventaire)")
        print("3. Tenter de fuir")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Phase d'attaque du joueur
            weapon = player.inventory.get_equipped_item()
            damage, is_fatal = CombatSystem.attack(player, enemy, weapon)
            print(f"\nVous infligez {damage} points de dégâts !")
            
            if is_fatal:
                print("L'ennemi a été vaincu !")
                return True
            
            # Phase d'attaque de l'ennemi
            enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon)
            print(f"L'ennemi vous inflige {enemy_damage} points de dégâts !")
            
            if player_dead:
                print("Vous avez été vaincu !")
                return "dead"
                
        elif choix == "2":
            print("\n=== Mode Défense ===")
            print("1. Gérer l'inventaire")
            print("2. Utiliser une potion")
            print("3. Changer d'arme")
            print("4. Retour au combat")
            
            action = input("\nQue souhaitez-vous faire ? ").strip()
            
            if action == "1":
                gerer_inventaire(player, game_map, spawn_manager)
            elif action == "2":
                # Cherche les potions dans l'inventaire
                potions = [(i, item) for i, item in enumerate(player.inventory.get_items()) 
                          if item.item_type == ItemType.POTION]
                
                if not potions:
                    print("Vous n'avez pas de potions !")
                else:
                    print("\nPotions disponibles :")
                    for i, (_, potion) in enumerate(potions, 1):
                        print(f"{i}. {potion}")
                    
                    try:
                        choix_potion = int(input("\nChoisissez une potion (0 pour annuler) : "))
                        if 1 <= choix_potion <= len(potions):
                            potion = potions[choix_potion-1][1]
                            player.hp = min(100, player.hp + potion.value)
                            player.inventory.remove_item(potion)
                            print(f"\nVous utilisez {potion.name} et récupérez {potion.value} HP !")
                    except ValueError:
                        print("Choix invalide")
                        
            elif action == "3":
                # Affiche les armes disponibles
                weapons = [(i, item) for i, item in enumerate(player.inventory.get_items()) 
                          if item.item_type == ItemType.WEAPON]
                
                if not weapons:
                    print("Vous n'avez pas d'armes !")
                else:
                    print("\nArmes disponibles :")
                    for i, (_, weapon) in enumerate(weapons, 1):
                        print(f"{i}. {weapon}")
                    
                    try:
                        choix_arme = int(input("\nChoisissez une arme (0 pour annuler) : "))
                        if 1 <= choix_arme <= len(weapons):
                            weapon = weapons[choix_arme-1][1]
                            player.inventory.equip_item(weapon)
                            print(f"\nVous équipez {weapon.name} !")
                    except ValueError:
                        print("Choix invalide")
            
            # L'ennemi attaque avec dégâts réduits
            enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon, defense_mode=True)
            print(f"\nEn défense, l'ennemi vous inflige {enemy_damage} points de dégâts (réduits) !")
            
            if player_dead:
                print("Vous avez été vaincu !")
                return "dead"
                
        elif choix == "3":
            # Tentative de fuite basée sur l'agilité
            chance_fuite = player.race_stats['agilite'] * 10  # 50-90% selon l'agilité
            if randint(1, 100) <= chance_fuite:
                print("Vous parvenez à fuir le combat !")
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
                print("Mais vous êtes coincé !")
            else:
                print("Tentative de fuite échouée !")
                # L'ennemi attaque pendant la fuite
                enemy_damage, player_dead = CombatSystem.attack(enemy, player, enemy.equipped_weapon)
                print(f"L'ennemi vous inflige {enemy_damage} points de dégâts !")
                
                if player_dead:
                    print("Vous avez été vaincu !")
                    return "dead"
        else:
            print("Choix invalide")

def menu_principal():
    player = None
    game_map = None
    spawn_manager = None
    dialogue_system = None  # Initialisation à None
    game_over = False
    start_time = None
    
    while True:
        print("\n=== Menu Principal ===")
        if game_over:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            print(f"\n=== GAME OVER ===")
            print(f"Temps de survie : {minutes} minutes et {seconds} secondes")
            print("\nStatistiques finales du personnage :")
            player.print_player()
            print("\n1. Créer un nouveau personnage")
            print("2. Quitter")
        elif not player:
            print("1. Créer un nouveau personnage")
            print("2. Quitter")
        else:
            print("1. Afficher les statistiques")
            print("2. Gérer l'inventaire")
            print("3. Se déplacer")
            print("4. Quitter")
        
        choix = input("\nVotre choix : ").strip()
        
        if game_over or not player:
            if choix == "1":
                player = creer_personnage()
                game_map = Map(10, 8)
                game_map.generate_default_map()
                spawn_manager = SpawnManager(game_map)
                dialogue_system = DialogueSystem()  # Création du système de dialogue
                start_time = time.time()
                game_over = False
                
                # Spawn initial d'items
                for _ in range(2):
                    spawn_manager.spawn_item()
            elif choix == "2":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
        else:
            if choix == "1":
                print("\n=== Statistiques du personnage ===")
                player.print_player()
            elif choix == "2":
                gerer_inventaire(player, game_map, spawn_manager)
            elif choix == "3":
                result = gerer_deplacement(player, game_map, spawn_manager, dialogue_system)
                if result == "dead":
                    game_over = True
            elif choix == "4":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    print("Bienvenue dans le jeu des Singes !")
    menu_principal()

# Initialisation des quêtes principales
main_quest = Quest(
    "À la recherche des vôtres",
    "Retrouvez votre famille kidnappée par les Masqués",
    {
        "Parler au PNJ": False,
        "Trouver l'arsenal": False,
        "Récupérer une arme": False,
        "Atteindre le camp des Masqués": False
    }
)

# Dans la boucle principale du jeu
def handle_dialogue(keys_pressed, dialogue_system, quest_system):
    if dialogue_system.is_dialogue_active:
        current_message = dialogue_system.get_current_message()
        # Afficher le message actuel (à implémenter selon votre système d'affichage)
        
        # Si une touche est pressée, passer au message suivant
        if any(keys_pressed):
            next_message = dialogue_system.next_message()
            if next_message is None:  # Dialogue terminé
                quest_system.complete_objective("À la recherche des vôtres", "Parler au PNJ")
                # Activer la recherche de l'arsenal