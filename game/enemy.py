from typing import Tuple
from .factions import FactionName, FACTIONS
from .items import Item
from random import choice, randint

class Enemy:
    def __init__(self, name: str, faction: FactionName, x: int, y: int):
        self.name = name
        self.faction = faction
        self.faction_obj = FACTIONS[faction]
        self.x = x
        self.y = y
        self.hp = 100
        self.equipped_weapon: Item = None
        
        # Stats de base aléatoires mais équilibrées
        self.stats = {
            'force': randint(5, 9),
            'agilite': randint(5, 9),
            'intelligence': randint(5, 9),
            'furtivite': randint(5, 9),
            'diplomatie': randint(5, 9)
        }
    
    def is_adjacent_to(self, player_x: int, player_y: int) -> bool:
        """Vérifie si l'ennemi est adjacent au joueur"""
        return abs(self.x - player_x) <= 1 and abs(self.y - player_y) <= 1

    def is_alive(self) -> bool:
        """Vérifie si l'ennemi est en vie"""
        return self.hp > 0

    def take_damage(self, damage: int):
        """Inflige des dégâts à l'ennemi"""
        self.hp = max(0, self.hp - damage) 