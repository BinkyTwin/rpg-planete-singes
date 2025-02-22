import unittest
import os
from game.items import M16, ITEMS

class TestM16(unittest.TestCase):
    def test_item_position(self):
        """Test que l'item M16 est à la position (5,17)."""
        item = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
        self.assertEqual(item.position, (5, 17), "L'item M16 n'est pas à la position attendue (5,17).")

    def test_item_image_exists(self):
        """Test que l'image de l'item existe bien dans le dossier assets."""
        item = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), item.image_path)
        self.assertTrue(os.path.exists(image_path), f"L'image {item.image_path} n'existe pas.")

    def test_item_in_items_dict(self):
        """Test que l'item M16 est bien présent dans le dictionnaire ITEMS."""
        self.assertIn("m16", ITEMS, "L'item M16 n'est pas présent dans le dictionnaire ITEMS.")
        self.assertIsInstance(ITEMS["m16"], M16, "L'item dans le dictionnaire n'est pas une instance de M16.")
        self.assertEqual(ITEMS["m16"].position, (5, 17), "La position de l'item M16 dans le dictionnaire est incorrecte.")

    def test_confirmation_popup(self):
        """Test que l'interaction déclenche la demande de confirmation lorsque 'E' est pressé."""
        item = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
        confirmation_called = False
        def confirmation():
            nonlocal confirmation_called
            confirmation_called = True
            return True
        item.interact((5, 17), "E", confirmation)
        self.assertTrue(confirmation_called, "La bulle de confirmation n'a pas été déclenchée lors de l'appui sur 'E'.")

    def test_collect_item_on_yes(self):
        """Test que l'item est collecté (et flag mis à True) si la confirmation renvoie True."""
        item = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
        def confirmation():
            return True
        result = item.interact((5, 17), "E", confirmation)
        self.assertTrue(result, "L'item devrait être collecté avec confirmation positive.")
        self.assertTrue(item.collected, "Le flag 'collected' de l'item n'est pas mis à True après confirmation positive.")

    def test_item_persistence_on_no(self):
        """Test que l'item reste sur la map si la confirmation renvoie False."""
        item = M16("M16", (5, 17), "assets/tilesets/images/items/M16_full.png")
        def confirmation():
            return False
        result = item.interact((5, 17), "E", confirmation)
        self.assertFalse(result, "L'item devrait rester sur la map avec confirmation négative.")
        self.assertFalse(item.collected, "Le flag 'collected' de l'item ne devrait pas être True après confirmation négative.")

if __name__ == '__main__':
    unittest.main()
