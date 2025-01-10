import os 
from .factions import FactionName, FACTIONS

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
        'orang_outan': {
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
        'singe_hurleur': {
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

    def __init__(self, name, x, y, race, faction):
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
        if faction not in self.FACTIONS:
            raise ValueError(f"Faction invalide. Choisissez parmi : {', '.join(self.FACTIONS)}")
        

        # points de vie du joueur
        self.hp = 100

        # points d'expérience du joueur
        self.xp = 0

        self.faction = faction
        self.faction_obj = FACTIONS[faction]

    def print_player(self):
        print(f"Nom : {self.name}")
        print(f"Position : ({self.x}, {self.y})")
        print(f"Race : {self.race}")
        print(f"Points de vie : {self.hp}")
        print(f"Expérience : {self.xp}")
        print("\nStatistiques de race :")
        for stat, value in self.race_stats.items():
            print(f"- {stat.capitalize()} : {value}")

    def get_relation_with(self, other_faction: FactionName):
        """Retourne la relation entre la faction du joueur et une autre faction"""
        return self.faction_obj.get_relation(other_faction)

# Création du joueur avec une faction
joueur1 = Player("lotfi", 2, 3, 'singe_hurleur', "Les Veilleurs des Montagnes")
joueur1.print_player()

