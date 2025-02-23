from typing import Tuple, Optional
from .player import Player
from .enemy import Enemy
from .items import Item, ItemType
import math

class CombatSystem:
    # Bonus de dégâts selon la race et le type d'arme
    WEAPON_RACE_BONUS = {
        'chimpanze': {
            'épée_rouillée': 1.2,  # +20% avec les armes de mêlée
            'm4': 0.8,             # -20% avec les fusils
            'glock': 1.0           # Neutre avec les pistolets
        },
        'gorille': {
            'épée_rouillée': 1.4,  # +40% avec les armes de mêlée
            'm4': 0.7,             # -30% avec les fusils
            'glock': 0.8           # -20% avec les pistolets
        },
        'orang_outan': {
            'épée_rouillée': 1.0,  # Neutre avec les armes de mêlée
            'm4': 1.2,             # +20% avec les fusils
            'glock': 1.2           # +20% avec les pistolets
        },
        'bonobo': {
            'épée_rouillée': 0.8,  # -20% avec les armes de mêlée
            'm4': 1.3,             # +30% avec les fusils
            'glock': 1.2           # +20% avec les pistolets
        },
        'singe_hurleur': {
            'épée_rouillée': 1.1,  # +10% avec les armes de mêlée
            'm4': 1.0,             # Neutre avec les fusils
            'glock': 1.1           # +10% avec les pistolets
        }
    }

    @staticmethod
    def calculate_damage(attacker_stats: dict, weapon: Optional[Item], attacker_race: str = None) -> int:
        """Calcule les dégâts en prenant en compte les bonus de race"""
        base_damage = attacker_stats['force'] * 2
        
        if weapon and weapon.item_type == ItemType.WEAPON:
            # Applique le bonus de race si applicable
            race_multiplier = 1.0
            if attacker_race and attacker_race in CombatSystem.WEAPON_RACE_BONUS:
                race_multiplier = CombatSystem.WEAPON_RACE_BONUS[attacker_race].get(weapon.name, 1.0)
            
            base_damage += weapon.value * race_multiplier
            
        return int(base_damage)

    @staticmethod
    def attack(attacker, defender, weapon: Optional[Item], defense_mode: bool = False) -> Tuple[int, bool]:
        """Effectue une attaque en prenant en compte la race de l'attaquant"""
        print(f"DEBUG - Combat - HP avant attaque - Attaquant: {attacker.hp}/{attacker.max_hp}, Défenseur: {defender.hp}/{defender.max_hp}")
        
        attacker_race = attacker.race if hasattr(attacker, 'race') else None
        damage = CombatSystem.calculate_damage(
            attacker.stats if isinstance(attacker, Enemy) else attacker.race_stats,
            weapon,
            attacker_race
        )
        
        if defense_mode:
            # Réduit les dégâts de 95% en mode défense
            damage = math.ceil(damage * 0.05)
            print(f"DEBUG - Combat - Dégâts réduits en mode défense: {damage}")
        
        # Applique les dégâts
        old_hp = defender.hp
        defender.hp = max(0, defender.hp - damage)
        print(f"DEBUG - Combat - Dégâts infligés: {damage} - HP défenseur: {old_hp} -> {defender.hp}")
        
        return damage, defender.hp <= 0 