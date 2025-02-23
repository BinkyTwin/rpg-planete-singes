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

    def attack(self, attacker, defender, weapon: Optional[Item] = None, is_defending: bool = False, damage_reduction: float = 0.0) -> Tuple[int, bool]:
        """
        Gère une attaque entre deux entités
        :param attacker: L'entité qui attaque
        :param defender: L'entité qui défend
        :param weapon: L'arme utilisée (optionnelle)
        :param is_defending: Si le défenseur est en position défensive
        :param damage_reduction: Pourcentage de réduction des dégâts (0.0 à 1.0)
        :return: (dégâts infligés, True si la cible est morte)
        """
        # Dégâts de base
        base_damage = 10  # Dégâts à mains nues
        
        # Si une arme est équipée, utiliser ses dégâts
        if weapon and weapon.item_type == ItemType.WEAPON:
            base_damage = weapon.value
            
            # Appliquer les bonus de race si disponibles
            if hasattr(attacker, 'race') and attacker.race in self.WEAPON_RACE_BONUS:
                weapon_bonuses = self.WEAPON_RACE_BONUS[attacker.race]
                if weapon.name.lower() in weapon_bonuses:
                    base_damage *= weapon_bonuses[weapon.name.lower()]
        
        # Calculer les dégâts finaux
        final_damage = base_damage
        
        # Appliquer la réduction de dégâts si en défense
        if is_defending:
            if damage_reduction > 0:
                final_damage *= (1 - damage_reduction)  # Réduction spécifiée (ex: 0.95 = 5% des dégâts)
            else:
                final_damage *= 0.5  # Réduction par défaut de 50%
        
        # Arrondir les dégâts
        final_damage = max(1, round(final_damage))  # Au moins 1 point de dégâts
        
        # Appliquer les dégâts
        defender.hp = max(0, defender.hp - final_damage)
        
        # Vérifier si la cible est morte
        is_dead = defender.hp <= 0
        
        return final_damage, is_dead 