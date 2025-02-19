class Quest:
    def __init__(self, title, description, objectives):
        self.title = title
        self.description = description
        self.objectives = objectives
        self.completed = False

class QuestSystem:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        
    def add_quest(self, quest):
        self.active_quests.append(quest)
        
    def complete_objective(self, quest_title, objective):
        for quest in self.active_quests:
            if quest.title == quest_title:
                if objective in quest.objectives:
                    quest.objectives[objective] = True
                    # Vérifier si tous les objectifs sont complétés
                    if all(quest.objectives.values()):
                        quest.completed = True
                        self.active_quests.remove(quest)
                        self.completed_quests.append(quest) 