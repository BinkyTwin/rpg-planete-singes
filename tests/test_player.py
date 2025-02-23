import unittest
from game.player import Player
from game.factions import FactionName

class TestPlayer(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.player = Player("Test", 0, 0, "gorille", FactionName.VEILLEURS)

    def test_initial_hp(self):
        """Test de l'initialisation des HP"""
        self.assertEqual(self.player.hp, 120)  # Le gorille a 120 HP max
        self.assertEqual(self.player.max_hp, 120)

    def test_take_damage(self):
        """Test de la prise de dégâts"""
        damage = self.player.take_damage(30)
        self.assertEqual(damage, 30)
        self.assertEqual(self.player.hp, 90)

    def test_heal(self):
        """Test de la guérison"""
        self.player.take_damage(50)  # HP = 70
        healed = self.player.heal(20)
        self.assertEqual(healed, 20)
        self.assertEqual(self.player.hp, 90)

    def test_heal_not_exceed_max(self):
        """Test que la guérison ne dépasse pas les HP max"""
        self.player.take_damage(20)  # HP = 100
        healed = self.player.heal(30)
        self.assertEqual(healed, 20)  # Seulement 20 HP récupérés
        self.assertEqual(self.player.hp, self.player.max_hp)

    def test_damage_not_below_zero(self):
        """Test que les dégâts ne font pas passer les HP en négatif"""
        damage = self.player.take_damage(150)
        self.assertEqual(damage, 120)  # Seulement 120 HP perdus
        self.assertEqual(self.player.hp, 0)

    def test_is_alive(self):
        """Test de la vérification si le joueur est en vie"""
        self.assertTrue(self.player.is_alive())
        self.player.take_damage(120)
        self.assertFalse(self.player.is_alive())

    def test_different_races_hp(self):
        """Test des HP maximum différents selon les races"""
        gorille = Player("Gorille", 0, 0, "gorille", FactionName.VEILLEURS)
        bonobo = Player("Bonobo", 0, 0, "bonobo", FactionName.VEILLEURS)
        
        self.assertEqual(gorille.max_hp, 120)
        self.assertEqual(bonobo.max_hp, 90)

if __name__ == '__main__':
    unittest.main() 