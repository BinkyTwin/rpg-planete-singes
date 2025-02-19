class DialogueSystem:
    # Définition des dialogues du PNJ
    DIALOGUES_PNJ = [
        "Ah ! Enfin, je vous trouve ! J'ai parcouru des lieues pour vous retrouver...",
        
        "Je suis désolé d'être porteur de mauvaises nouvelles, mais votre famille a été enlevée par la faction des Masqués.",
        
        "Les Masqués... une organisation redoutable qui sème la terreur dans nos contrées. Ils ont établi leur camp à l'autre bout de ces terres.",
        
        "Pour les atteindre, vous devrez traverser des territoires hostiles. Sans armes, c'est du suicide...",
        
        "J'ai entendu parler d'un ancien arsenal abandonné non loin d'ici. Vous devriez commencer par y chercher de quoi vous défendre.",
        
        "Méfiez-vous, les sbires des Masqués patrouillent partout. Ils tenteront de vous empêcher d'atteindre leur camp.",
        
        "Votre mission, si vous l'acceptez, est claire : retrouvez l'arsenal, armez-vous, et frayez-vous un chemin jusqu'au camp des Masqués.",
        
        "Le temps presse. Votre famille compte sur vous. Que les anciens dieux vous protègent dans votre quête...",
        
        "Une dernière chose : si vous avez besoin de revoir vos objectifs, consultez votre journal de quête avec la touche 'J'.",
        
        "Je dois partir maintenant... Ma mission est accomplie. Que la chance soit avec vous, brave guerrier !"
    ]

    def __init__(self):
        self.current_dialogue_index = 0
        self.is_dialogue_active = False
        self.dialogues = []
        self.has_talked_to_npc = False
        self.dialogue_finished = False  # Nouveau flag pour suivre la fin du dialogue
        
    def start_dialogue(self):
        if not self.has_talked_to_npc:  # Premier dialogue uniquement
            self.dialogues = self.DIALOGUES_PNJ
            self.current_dialogue_index = 0
            self.is_dialogue_active = True
            self.has_talked_to_npc = True
            return self.get_current_message()
        return None
    
    def next_message(self):
        if self.is_dialogue_active:
            self.current_dialogue_index += 1
            if self.current_dialogue_index >= len(self.dialogues):
                self.is_dialogue_active = False
                self.dialogue_finished = True  # Marque le dialogue comme terminé
                return None
            return self.get_current_message()
        return None
    
    def get_current_message(self):
        if self.is_dialogue_active and self.current_dialogue_index < len(self.dialogues):
            return self.dialogues[self.current_dialogue_index]
        return None

    def display_message(self, message):
        if message:
            print("\n=== Message du PNJ ===")
            print(message)
            print("\nAppuyez sur Entrée pour continuer...")
            input()

    def is_dialogue_finished(self):
        return self.dialogue_finished 