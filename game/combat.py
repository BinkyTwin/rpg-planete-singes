from typing import Optional
from .player import Player
from .items import Item, ItemType
from .factions import FactionRelation

class CombatSystem:
    # Multiplicateurs de dégâts selon les relations entre factions
    FACTION_DAMAGE_MULTIPLIERS = {
        FactionRelation.ALLIED: 0.5,    # Dégâts réduits entre alliés
        FactionRelation.NEUTRAL: 1.0,   # Dégâts normaux
        FactionRelation.HOSTILE: 1.2    # Dégâts augmentés entre ennemis
    }

    # Bonus de dégâts selon le type d'arme et la race
    WEAPON_RACE_BONUS = {
        'chimpanze': {
            'épée_rouillée': 1.2,  # Bonus aux armes de mêlée
            'm4': 0.8,
            'glock': 1.0
        },
        'gorille': {
            'épée_rouillée': 1.4,  # Fort bonus aux armes de mêlée
            'm4': 0.7,
            'glock': 0.8
        },
        'orang_outan': {
            'épée_rouillée': 1.0,
            'm4': 1.2,  # Bonus aux armes à distance
            'glock': 1.2
        },
        'bonobo': {
            'épée_rouillée': 0.8,
            'm4': 1.3,  # Fort bonus aux armes à distance
            'glock': 1.2
        },
        'singe_hurleur': {
            'épée_rouillée': 1.1,
            'm4': 1.0,
            'glock': 1.1
        }
    }

    @staticmethod
    def calculate_damage(attacker: Player, defender: Player, weapon: Optional[Item] = None) -> float:
        """Calcule les dégâts en prenant en compte les statistiques, l'arme et les relations"""
        
        # Dégâts de base selon la force
        base_damage = attacker.race_stats['force'] * 2

        # Bonus/Malus selon l'agilité (précision)
        accuracy_modifier = attacker.race_stats['agilite'] / 10

        # Modificateur de faction
        faction_relation = attacker.get_relation_with(defender.faction)
        faction_multiplier = CombatSystem.FACTION_DAMAGE_MULTIPLIERS[faction_relation]

        # Bonus d'arme
        weapon_multiplier = 1.0
        if weapon and weapon.item_type == ItemType.WEAPON:
            weapon_multiplier = CombatSystem.WEAPON_RACE_BONUS.get(
                attacker.race, {}).get(weapon.name, 1.0)
            base_damage += weapon.value

        # Calcul final des dégâts
        final_damage = (base_damage * accuracy_modifier * faction_multiplier * weapon_multiplier)
        
        # Réduction des dégâts selon la force du défenseur
        defense = defender.race_stats['force'] * 0.5
        final_damage = max(0, final_damage - defense)

        return round(final_damage, 1)

    @staticmethod
    def attack(attacker: Player, defender: Player, weapon: Optional[Item] = None) -> tuple[float, bool]:
        """
        Effectue une attaque et retourne les dégâts infligés et si l'attaque est fatale
        """
        damage = CombatSystem.calculate_damage(attacker, defender, weapon)
        
        # Application des dégâts
        defender.hp -= damage
        
        # Vérifie si l'attaque est fatale
        is_fatal = defender.hp <= 0
        defender.hp = max(0, defender.hp)  # Empêche les PV négatifs
        
        return damage, is_fatal

    @staticmethod
    def can_attack(attacker: Player, defender: Player) -> bool:
        """Vérifie si l'attaque est possible selon les relations entre factions"""
        relation = attacker.get_relation_with(defender.faction)
        return relation != FactionRelation.ALLIED