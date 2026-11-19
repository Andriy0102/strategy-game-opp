import unittest
from units import Unit, Squad, Warrior, Archer, Mage, Scout


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

    def test_squad_add_remove(self):
        squad = Squad("Гама")
        unit1 = Unit("Knight", 100, 20, 3, 0, 0)

        squad.add_unit(unit1)
        self.assertEqual(len(squad.units), 1)

        squad.remove_unit(unit1)
        self.assertEqual(len(squad.units), 0)

    def test_squad_health_clear_dead(self):
        squad = Squad("Бета")
        unit1 = Unit("Knight", 100, 20, 3, 0, 0)
        unit2 = Unit("Archer", 30, 15, 4, 1, 1)

        squad.add_unit(unit1)
        squad.add_unit(unit2)

        self.assertEqual(squad.get_total_health(), 130)

        unit2.take_damage(50)
        squad.clear_dead_units()

        self.assertEqual(len(squad.units), 1)
        self.assertEqual(squad.get_total_health(), 100)

    def test_squad_methods_and_attack(self):
        squad = Squad("Альфа")
        unit1 = Unit("Knight", health=100,attack_power= 20, speed= 3)
        unit2 = Unit("Archer", health=50,attack_power= 15, speed= 4)
        target = Unit("Enemy", health=100, attack_power=10, speed=2)

        squad.add_unit(unit1)
        squad.add_unit(unit2)

        self.assertEqual(len(squad),2)
        self.assertEqual(squad[0], unit1)

        self.assertIn("Загін 'Альфа'",str(squad))

        squad.attack_target(target)
        self.assertEqual(target.health, 65)


class TestUnitClasses(unittest.TestCase):

    def test_warrior_defense_and_rage(self):
        warrior = Warrior("Тарас", health=120, attack_power=20, defense=5)
        enemy = Unit("Ворог1", health=100, attack_power=15, speed=3, defense=2)

        dealt_to_warrior = warrior.take_damage(15)
        self.assertEqual(dealt_to_warrior, 8)
        self.assertEqual(warrior.health, 112)

        self.assertTrue(warrior.special_ability())
        dealt_by_warrior = warrior.attack(enemy)
        self.assertEqual(dealt_by_warrior, 28)
        self.assertEqual(enemy.health, 72)

    def test_archer_distance_and_ability(self):
        archer = Archer("Олег", attack_power=18, x=0, y=0)
        tank = Warrior("Ворог2", health=120, defense=10, x=2, y=1)

        dealt = archer.attack(tank)
        self.assertEqual(dealt, 23)
        self.assertEqual(tank.health, 97)

        self.assertTrue(archer.special_ability(tank))
        self.assertEqual(tank.health, 69)


if __name__ == "__main__":
    unittest.main()



