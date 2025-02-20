import os 
from .factions import FactionName, FACTIONS
from .inventory import Inventory

class Player:
    RACES = {
        'chimpanze': {
            'agilite': 8,
            'force': 6,
            'intelligence': 7,
            'furtivite': 6,
            'diplomatie': 8
        },
        'gorille': {
            'agilite': 5,
            'force': 9,
            'intelligence': 6,
            'furtivite': 4,
            'diplomatie': 5
        },
        'orang outan': {
            'agilite': 6,
            'force': 7,
            'intelligence': 9,
            'furtivite': 5,
            'diplomatie': 7
        },
        'bonobo': {
            'agilite': 7,
            'force': 5,
            'intelligence': 7,
            'furtivite': 9,
            'diplomatie': 9
        },
        'singe hurleur': {
            'agilite': 8,
            'force': 6,
            'intelligence': 6,
            'furtivite': 7,
            'diplomatie': 6
        }
    }
    FACTIONS = {
        "Les Veilleurs des Montagnes",
        "Le Cercle des Ombres",
        "Le Clan des Brumes",
        "Les Enfants de la Forêt"
    }

    def __init__(self, name, x, y, race, faction: FactionName):
        # nom du joueur
        self.name = name

        # position du joueur
        self.x = x
        self.y = y

        # race du joueur
        if race not in self.RACES:
            raise ValueError(f"Race invalide. Choisissez parmi : {', '.join(self.RACES.keys())}")
        self.race = race
        self.race_stats = self.RACES[race].copy() # stats de la race

        # Faction du joueur
        self.faction = faction
        self.faction_obj = FACTIONS[faction]

        # points de vie du joueur
        self.hp = 100

        # points d'expérience du joueur
        self.xp = 0

        # Ajout de l'inventaire
        self.inventory = Inventory()

    def print_player(self):
        print(f"Nom : {self.name}")
        print(f"Position : ({self.x}, {self.y})")
        print(f"Race : {self.race}")
        print(f"Points de vie : {self.hp}")
        print(f"Expérience : {self.xp}")
        print("\nStatistiques de race :")
        for stat, value in self.race_stats.items():
            print(f"- {stat.capitalize()} : {value}")
        print(f"Slots d'inventaire : {len(self.inventory.get_items())}/{self.inventory.max_slots}")

    def get_relation_with(self, other_faction: FactionName):
        """Retourne la relation entre la faction du joueur et une autre faction"""
        return self.faction_obj.get_relation(other_faction)



