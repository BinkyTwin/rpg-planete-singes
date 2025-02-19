from game.player import Player
from game.factions import FactionName, FACTIONS
from game.inventory import Inventory
from game.items import ITEMS
from game.map import Map, TileType
from game.spawn_manager import SpawnManager
from game.quest_manager import Quest, QuestManager, DialogueManager
from game.npc_manager import NPCManager

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
        return
    
    print(f"Slots utilisés : {len(items)}/{player.inventory.max_slots}")
    print("\nObjets :")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.name} - {item.description} (Valeur: {item.value})")

def gerer_inventaire(player):
    while True:
        print("\n=== Gestion de l'inventaire ===")
        print("1. Voir l'inventaire")
        print("2. Ajouter un objet")
        print("3. Jeter un objet")
        print("4. Retour au menu principal")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            afficher_inventaire(player)
        
        elif choix == "2":
            while True:
                print("\nObjets disponibles :")
                print("0. Retour au menu précédent")
                items_list = list(ITEMS.values())
                for i, item in enumerate(items_list, 1):
                    print(f"{i}. {item.name} - {item.description}")
                
                try:
                    choix_item = int(input("\nChoisissez un objet à ajouter (0 pour retourner) : "))
                    if choix_item == 0:
                        break
                    if 1 <= choix_item <= len(items_list):
                        item = items_list[choix_item - 1]
                        if player.inventory.add_item(item):
                            print(f"\n{item.name} a été ajouté à l'inventaire")
                        else:
                            print("\nL'inventaire est plein !")
                    else:
                        print("\nNuméro d'objet invalide")
                except ValueError:
                    print("\nVeuillez entrer un numéro valide")
        
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
                    if player.inventory.remove_item(item):
                        print(f"\n{item.name} a été retiré de l'inventaire")
                else:
                    print("\nNuméro d'objet invalide")
            except ValueError:
                print("\nVeuillez entrer un numéro valide")
        
        elif choix == "4":
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

def creer_personnage():
    print("=== Création de votre personnage ===\n")
    
    while True:
        name = input("Entrez le nom de votre personnage : ").strip()
        if name:
            break
        print("Le nom ne peut pas être vide.")

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

    player = Player(name, 0, 0, race, faction_match)
    player.inventory = Inventory()
    
    print("\n=== Personnage créé avec succès ! ===")
    player.print_player()
    
    return player

def handle_npc_dialogue(npc):
    """Gère l'affichage des dialogues d'un PNJ"""
    print(f"\nDiscussion avec {npc.name}")
    while True:
        message = npc.get_next_dialogue()
        if message is None:
            break
        print(f"\n{message}")
        input("Appuyez sur Entrée pour continuer...")
    npc.reset_dialogue()

def gerer_deplacement(player, game_map, npc_manager):
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
        
        dx, dy = 0, 0
        if commande == "z":
            dx, dy = 0, -1
        elif commande == "s":
            dx, dy = 0, 1
        elif commande == "q":
            dx, dy = -1, 0
        elif commande == "d":
            dx, dy = 1, 0
        elif commande == "r":
            break
        else:
            print("Commande invalide")
            continue

        success, message = game_map.move_player(dx, dy)
        
        if message == "NPC_ENCOUNTER":
            npc = npc_manager.get_npc_at_position(
                game_map.player_x + dx,
                game_map.player_y + dy
            )
            if npc:
                handle_npc_dialogue(npc)
        elif message:
            print(f"\n{message}")

def init_quests(quest_manager, dialogue_manager):
    """Initialise les quêtes et dialogues du jeu"""
    main_quest = Quest(
        "Atteindre le camp des Masqués",
        "Retrouvez votre famille capturée par les Masqués",
        [
            "Trouver le PNJ dans le coin opposé",
            "Discuter avec le PNJ",
            "Récupérer une arme",
            "Combattre les ennemis",
            "Rejoindre le camp des Masqués"
        ]
    )
    quest_manager.add_quest(main_quest)
    main_quest.start_quest()
    
    dialogue_manager.add_dialogue("guide_pnj", [
        "Ah, te voilà enfin ! Je me demandais si tu arriverais...",
        "J'ai un message important pour toi...",
        "Les Masqués ont enlevé ta famille...",
        "Tu vas devoir récupérer des armes...",
        "Bonne chance dans ta quête, voyageur."
    ])

def afficher_quetes_actives(quest_manager):
    """Affiche les quêtes actives"""
    print("\n=== Quêtes actives ===")
    active_quests = quest_manager.list_active_quests()
    if not active_quests:
        print("Aucune quête active")
        return
    
    for quest in active_quests:
        print(f"\n{quest.title}")
        print(f"Description : {quest.description}")
        print(f"Objectif actuel : {quest.get_current_objective()}")

def menu_principal():
    player = None
    game_map = None
    spawn_manager = None
    quest_manager = QuestManager()
    dialogue_manager = DialogueManager()
    npc_manager = None
    
    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un nouveau personnage")
        if player:
            print("2. Gérer l'inventaire")
            print("3. Se déplacer")
            print("4. Voir les quêtes actives")
            print("5. Quitter")
        else:
            print("2. Quitter")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            player = creer_personnage()
            game_map = Map(10, 8)
            game_map.generate_default_map()
            
            # Initialisation du NPC Manager et création du guide
            npc_manager = NPCManager(game_map)
            guide_npc = npc_manager.create_guide_npc(game_map.player_x, game_map.player_y)
            npc_manager.add_npc(guide_npc)
            
            # Spawn initial d'items
            spawn_manager = SpawnManager(game_map)
            for _ in range(2):
                spawn_manager.spawn_item()
            # Initialisation des quêtes
            init_quests(quest_manager, dialogue_manager)
            
        elif choix == "2" and player:
            gerer_inventaire(player)
        elif choix == "2" and not player:
            print("Au revoir !")
            break
        elif choix == "3" and player:
            gerer_deplacement(player, game_map, npc_manager)
        elif choix == "4" and player:
            afficher_quetes_actives(quest_manager)
        elif choix == "5" and player:
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    print("Bienvenue dans le jeu des Singes !")
    menu_principal()
