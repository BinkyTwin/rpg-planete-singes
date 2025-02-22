class AideMessage:
    def __init__(self):
        self.message = "Cliquez sur E pour discuter avec le pnj"
        self.visible = False

    def update(self, player_near_pnj, in_dialogue):
        """
        Met à jour la visibilité du message d'aide.
        :param player_near_pnj: bool, True si le joueur est proche du PNJ.
        :param in_dialogue: bool, True si le dialogue est en cours.
        :return: bool, la visibilité actuelle du message.
        """
        if player_near_pnj and not in_dialogue:
            self.visible = True
        else:
            self.visible = False
        return self.visible

if __name__ == '__main__':
    # Exemple d'utilisation
    aide = AideMessage()
    # Simulation: joueur proche et pas en dialogue
    print(f"Message visible: {aide.update(player_near_pnj=True, in_dialogue=False)}")
    # Simulation: joueur proche mais en dialogue
    print(f"Message visible: {aide.update(player_near_pnj=True, in_dialogue=True)}")
    # Simulation: joueur loin
    print(f"Message visible: {aide.update(player_near_pnj=False, in_dialogue=False)}")
