from enum import Enum
from typing import Dict, Set

class FactionName(Enum):
    VEILLEURS = "Les Veilleurs des Montagnes"
    OMBRES = "Le Cercle des Ombres"
    BRUMES = "Le Clan des Brumes"
    FORET = "Les Enfants de la Forêt"

class FactionRelation(Enum):
    ALLIED = "allié"
    NEUTRAL = "neutre"
    HOSTILE = "hostile"

class Faction:
    def __init__(self, name: FactionName, description: str):
        self.name = name
        self.description = description
        self.relations: Dict[FactionName, FactionRelation] = {}

    def set_relation(self, other_faction: FactionName, relation: FactionRelation):
        self.relations[other_faction] = relation

    def get_relation(self, other_faction: FactionName) -> FactionRelation:
        return self.relations.get(other_faction, FactionRelation.NEUTRAL)

# Création des factions avec leurs descriptions
FACTIONS = {
    FactionName.VEILLEURS: Faction(
        FactionName.VEILLEURS,
        "Gardiens ancestraux des sommets, ils protègent les anciennes reliques et surveillent les terres depuis leurs citadelles."
    ),
    FactionName.OMBRES: Faction(
        FactionName.OMBRES,
        "Maîtres de l'espionnage et de la discrétion, ils œuvrent dans l'ombre pour maintenir l'équilibre du pouvoir."
    ),
    FactionName.BRUMES: Faction(
        FactionName.BRUMES,
        "Nomades mystérieux vivant dans les vallées brumeuses, experts en alchimie et en arts mystiques."
    ),
    FactionName.FORET: Faction(
        FactionName.FORET,
        "Protecteurs de la nature, ils vivent en harmonie avec la forêt et ses créatures."
    )
}

# Configuration des relations initiales entre factions
def initialize_faction_relations():
    # Les Veilleurs sont alliés avec les Enfants de la Forêt, hostiles aux Ombres
    FACTIONS[FactionName.VEILLEURS].set_relation(FactionName.FORET, FactionRelation.ALLIED)
    FACTIONS[FactionName.VEILLEURS].set_relation(FactionName.OMBRES, FactionRelation.HOSTILE)
    
    # Le Cercle des Ombres est allié avec le Clan des Brumes
    FACTIONS[FactionName.OMBRES].set_relation(FactionName.BRUMES, FactionRelation.ALLIED)
    FACTIONS[FactionName.OMBRES].set_relation(FactionName.VEILLEURS, FactionRelation.HOSTILE)
    
    # Le Clan des Brumes est neutre avec les Enfants de la Forêt
    FACTIONS[FactionName.BRUMES].set_relation(FactionName.FORET, FactionRelation.NEUTRAL)
    FACTIONS[FactionName.BRUMES].set_relation(FactionName.OMBRES, FactionRelation.ALLIED)
    
    # Les Enfants de la Forêt sont alliés avec les Veilleurs
    FACTIONS[FactionName.FORET].set_relation(FactionName.VEILLEURS, FactionRelation.ALLIED)
    FACTIONS[FactionName.FORET].set_relation(FactionName.BRUMES, FactionRelation.NEUTRAL)

initialize_faction_relations() 