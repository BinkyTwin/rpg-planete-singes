import os 

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
        self.faction = faction
        self.faction_stats = self.FACTIONS[faction].copy() # stats de la faction

        # points de vie du joueur
        self.hp = 100

        # points d'expérience du joueur
        self.xp = 0

