from typing import List, Tuple, Optional

class NPC:
    """Classe représentant un PNJ (Personnage Non Joueur)"""
    
    def __init__(self, name: str, x: int, y: int, dialogues: List[str]):
        self.name = name
        self.x = x
        self.y = y
        self.dialogues = dialogues
        self.dialogue_index = 0
        self.symbol = "P"
    
    def get_position(self) -> Tuple[int, int]:
        """Retourne la position actuelle du PNJ"""
        return (self.x, self.y)
    
    def get_next_dialogue(self) -> Optional[str]:
        """Retourne le prochain dialogue dans la séquence"""
        if self.dialogue_index < len(self.dialogues):
            message = self.dialogues[self.dialogue_index]
            self.dialogue_index += 1
            return message
        return None
    
    def reset_dialogue(self):
        """Réinitialise l'index des dialogues"""
        self.dialogue_index = 0

class NPCManager:
    """Gestionnaire des PNJs du jeu"""
    
    def __init__(self, game_map):
        self.npcs = []
        self.game_map = game_map
    
    def add_npc(self, npc: NPC):
        """Ajoute un PNJ au gestionnaire et le place sur la carte"""
        # Vérifie si la position est valide et que la case est vide
        if (0 <= npc.x < self.game_map.width and 
            0 <= npc.y < self.game_map.height and 
            self.game_map.grid[npc.y][npc.x] == "."):
            
            self.npcs.append(npc)
            self.game_map.grid[npc.y][npc.x] = npc.symbol
            return True
        return False
    
    def get_npc_at_position(self, x: int, y: int) -> Optional[NPC]:
        """Retourne le PNJ à la position donnée, s'il existe"""
        for npc in self.npcs:
            if npc.x == x and npc.y == y:
                return npc
        return None
    
    def create_guide_npc(self, player_x: int, player_y: int) -> NPC:
        """Crée le PNJ guide et le place à une position stratégique"""
        # On place le PNJ à quelques cases du joueur pour faciliter la première rencontre
        # mais pas trop près pour garder un minimum d'exploration
        guide_x = min(self.game_map.width - 2, player_x + 4)  # 4 cases à droite du joueur
        guide_y = min(self.game_map.height - 2, player_y + 2)  # 2 cases en bas du joueur
        
        # Si cette position est occupée, on essaie d'autres positions
        if self.game_map.grid[guide_y][guide_x] != ".":
            # Plan B : essayer à gauche du joueur
            guide_x = max(1, player_x - 4)
            guide_y = min(self.game_map.height - 2, player_y + 2)
            
            # Si toujours occupé, on place le PNJ dans une position par défaut
            if self.game_map.grid[guide_y][guide_x] != ".":
                guide_x = self.game_map.width // 2  # Au milieu de la carte
                guide_y = self.game_map.height // 2  # Au milieu de la carte
        
        guide = NPC(
            name="Guide",
            x=guide_x,
            y=guide_y,
            dialogues=[
                "Ah, te voilà enfin ! Je me demandais si tu arriverais...",
                "J'ai un message important pour toi...",
                "Les Masqués ont enlevé ta famille...",
                "Tu vas devoir récupérer des armes...",
                "Bonne chance dans ta quête, voyageur."
            ]
        )
        return guide 