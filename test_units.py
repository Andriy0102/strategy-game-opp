import unittest
from units import Unit

class UnitsTest(unittest.TestCase):
    def setUp(self):
        self.warrior = Unit(name="Андрій", health=100, attack_power=20, speed=5)
        self.enemy = Unit(name="Ворог", health=40, attack_power=10, speed=3)

    def test_move(self):
        result = self.warrior.move(2, 3)
        self.assertTrue(result)
        self.assertEqual(self.warrior.x, 2)
        self.assertEqual(self.warrior.y, 3)
        self.assertEqual(self.warrior.action_points, 4)

    def test_take_damage(self):
        self.warrior.take_damage(40)
        self.assertEqual(self.warrior.health, 60)
        self.assertTrue(self.warrior.is_alive)

        self.warrior.take_damage(70)
        self.assertEqual(self.warrior.health, 0)
        self.assertFalse(self.warrior.is_alive)

    def test_attack(self):
        self.warrior.attack(self.enemy)
        self.assertEqual(self.enemy.health, 20)
        self.assertEqual(self.warrior.action_points, 3)

    def test_reset_turn(self):
        self.warrior.move(1,1)
        self.warrior.reset_turn()
        self.assertEqual(self.warrior.action_points, 5)


if __name__ == "__main__":
    unittest.main()



