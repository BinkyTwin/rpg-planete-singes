from enum import Enum
from typing import List, Dict, Optional

class QuestStatus(Enum):
    """Énumération des états possibles d'une quête"""
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class Quest:
    """Classe représentant une quête avec ses objectifs et son état"""
    
    def __init__(self, title: str, description: str, objectives: List[str]):
        self.title = title
        self.description = description
        self.objectives = objectives
        self.current_step = 0
        self.status = QuestStatus.NOT_STARTED
        
    def advance_step(self) -> bool:
        """
        Fait progresser la quête d'une étape
        Retourne True si la quête est terminée, False sinon
        """
        if self.status == QuestStatus.COMPLETED:
            return True
            
        self.current_step += 1
        if self.current_step >= len(self.objectives):
            self.status = QuestStatus.COMPLETED
            return True
            
        self.status = QuestStatus.IN_PROGRESS
        return False
        
    def get_current_objective(self) -> Optional[str]:
        """Retourne l'objectif actuel de la quête"""
        if self.current_step < len(self.objectives):
            return self.objectives[self.current_step]
        return None
        
    def start_quest(self):
        """Démarre la quête"""
        self.status = QuestStatus.IN_PROGRESS

class QuestManager:
    """Gestionnaire des quêtes du jeu"""
    
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        
    def add_quest(self, quest: Quest):
        """Ajoute une nouvelle quête au gestionnaire"""
        self.quests[quest.title] = quest
        
    def get_quest(self, title: str) -> Optional[Quest]:
        """Récupère une quête par son titre"""
        return self.quests.get(title)
        
    def update_quest(self, title: str, event: str) -> bool:
        """
        Met à jour l'état d'une quête en fonction d'un événement
        Retourne True si la mise à jour a réussi
        """
        quest = self.get_quest(title)
        if quest and quest.status != QuestStatus.COMPLETED:
            return quest.advance_step()
        return False
        
    def list_active_quests(self) -> List[Quest]:
        """Retourne la liste des quêtes actives"""
        return [quest for quest in self.quests.values() 
                if quest.status == QuestStatus.IN_PROGRESS]

class DialogueManager:
    """Gestionnaire des dialogues avec les PNJs"""
    
    def __init__(self):
        self.dialogues: Dict[str, List[str]] = {}
        
    def add_dialogue(self, npc_id: str, messages: List[str]):
        """Ajoute une séquence de dialogue pour un PNJ"""
        self.dialogues[npc_id] = messages
        
    def get_dialogue(self, npc_id: str) -> Optional[List[str]]:
        """Récupère les messages de dialogue d'un PNJ"""
        return self.dialogues.get(npc_id) 