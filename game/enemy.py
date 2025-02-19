from typing import Tuple
from .factions import FactionName, FACTIONS
from .items import Item
from random import choice, randint
from .player import Player

class Enemy:
    def __init__(self, name: str, faction: FactionName, x: int, y: int, race: str, equipped_weapon: Item = None):
        self.name = name
        self.faction = faction
        self.x = x
        self.y = y
        self.race = race
        self.equipped_weapon = equipped_weapon
        self.hp = 100
        
        # Copie les stats de la race choisie
        self.stats = Player.RACES[race].copy()
    
    def is_adjacent_to(self, x: int, y: int) -> bool:
        """Vérifie si l'ennemi est adjacent à une position donnée"""
        return abs(self.x - x) <= 1 and abs(self.y - y) <= 1

    def is_alive(self) -> bool:
        """Vérifie si l'ennemi est en vie"""
        return self.hp > 0

    def take_damage(self, damage: int):
        """Inflige des dégâts à l'ennemi"""
        self.hp = max(0, self.hp - damage)

    def __str__(self):
        return f"{self.name} ({self.faction.value})" 