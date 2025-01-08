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

    def __init__(self, name, x, y, race):
        self.name = name
        self.x = x
        self.y = y
        if race not in self.RACES:
            raise ValueError(f"Race invalide. Choisissez parmi : {', '.join(self.RACES.keys())}")
        self.race = race
        #self.stats = self.RACES[race].copy()
        self.stats = self.RACES[race].copy()
    
    def print_player(self):
        print("name : "+self.name +"\n")
        print("position x : "+str(self.x) +"\n")
        print("position y : "+str(self.y) +"\n")
        print("race : "+self.race +"\n")

joueur1 = Player("lotfi",2,3,'singe_hurleur')
joueur1.print_player()

