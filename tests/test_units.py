import unittest
from units import Unit, Squad, Warrior, Archer, Mage, Scout
import os
import tempfile


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

    def test_mage_attack_and_healing(self):
        mage = Mage("Максим", attack_power=22, mana=40)
        ally = Warrior("Союзник", health=120, defense=5)
        ally.take_damage(50, ignore_defense=True)

        self.assertTrue(mage.special_ability(ally))
        self.assertEqual(ally.health, 95)
        self.assertEqual(mage.mana, 20)

        mage.reset_turn()
        self.assertEqual(mage.mana, 30)

        dealt = mage.attack(ally)
        self.assertEqual(dealt, 22)
        self.assertEqual(ally.health, 73)

    def test_scout_dodge_and_sprint(self):
        dodger = Scout("Ігор", health=80, speed=6, dodge_chance=1.0)
        target = Scout("Суперник", health=80, speed=6, dodge_chance=0.0)

        self.assertEqual(dodger.take_damage(30), 0)
        self.assertEqual(dodger.health, 80)

        self.assertEqual(target.take_damage(30), 29)
        self.assertEqual(target.health, 51)

        self.assertTrue(dodger.move(1, 0, move_cost=3))
        self.assertEqual(dodger.action_points, 4)

        self.assertTrue(dodger.special_ability())
        self.assertEqual(dodger.action_points, 6)
        self.assertFalse(dodger.special_ability())

    def test_apply_pickups(self):
        unit = Warrior("Тарас", health=100, attack_power=15, speed=4)
        unit.take_damage(50, ignore_defense=True)

        self.assertTrue(unit.apply_pickup("Heal"))
        self.assertEqual(unit.health, 80)

        self.assertTrue(unit.apply_pickup("Weapon"))
        self.assertEqual(unit.attack_power, 20)

        unit.move(1, 0)
        self.assertTrue(unit.apply_pickup("Ability"))
        self.assertEqual(unit.action_points, 4)
        self.assertFalse(unit.apply_pickup("Unknown"))


class TestSquadFeatures(unittest.TestCase):

    def setUp(self):
        self.squad = Squad("Авангард")
        self.warrior = Warrior("Тарас", health=120, attack_power=20, speed=3)
        self.archer = Archer("Олег", health=85, attack_power=18, speed=4)
        self.mage = Mage("Максим", health=70, attack_power=22, speed=3, mana=40)
        self.scout = Scout("Ігор", health=80, attack_power=14, speed=6, dodge_chance=0.5)
        self.squad.add_unit(self.warrior)
        self.squad.add_unit(self.archer)
        self.squad.add_unit(self.mage)
        self.squad.add_unit(self.scout)

    def test_search_and_filter(self):
        found = self.squad.find_by_name("олег")
        self.assertIs(found, self.archer)
        self.assertIsNone(self.squad.find_by_name("Невідомий"))

        archers = self.squad.filter_by_type(Archer)
        self.assertEqual(archers, [self.archer])

        healthy = self.squad.filter_by_health(85)
        self.assertEqual(len(healthy), 2)
        self.assertIn(self.warrior, healthy)
        self.assertIn(self.archer, healthy)

    def test_sort_units(self):
        sorted_by_speed = self.squad.sort_units(by="speed", reverse=True)
        self.assertEqual(sorted_by_speed[0], self.scout)
        self.assertEqual(sorted_by_speed[1], self.archer)

        sorted_by_hp_asc = self.squad.sort_units(by="health", reverse=False)
        self.assertEqual(sorted_by_hp_asc[0], self.mage)
        self.assertEqual(sorted_by_hp_asc[-1], self.warrior)

        with self.assertRaises(ValueError):
            self.squad.sort_units(by="invalid_field")

    def test_json_save_and_load(self):
        self.warrior.special_ability()
        self.mage.special_ability(self.warrior)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            temp_path = tmp.name

        try:
            self.squad.save_to_file(temp_path)
            loaded_squad = Squad.load_from_file(temp_path)

            self.assertEqual(loaded_squad.name, "Авангард")
            self.assertEqual(len(loaded_squad), 4)
            self.assertIsInstance(loaded_squad[0], Warrior)
            self.assertIsInstance(loaded_squad[1], Archer)
            self.assertIsInstance(loaded_squad[2], Mage)
            self.assertIsInstance(loaded_squad[3], Scout)

            self.assertTrue(loaded_squad[0].rage_active)
            self.assertEqual(loaded_squad[2].mana, 20)
            self.assertEqual(loaded_squad[3].dodge_chance, 0.5)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()



