from game.player import Player
from game.factions import FactionName, FACTIONS
from game.inventory import Inventory
from game.items import ITEMS

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

def menu_principal():
    player = None
    
    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un nouveau personnage")
        if player:
            print("2. Gérer l'inventaire")
            print("3. Quitter")
        else:
            print("2. Quitter")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            player = creer_personnage()
        elif choix == "2" and player:
            gerer_inventaire(player)
        elif choix == "2" and not player:
            print("Au revoir !")
            break
        elif choix == "3" and player:
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    print("Bienvenue dans le jeu des Singes !")
    menu_principal()
