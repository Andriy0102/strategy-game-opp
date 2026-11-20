import unittest
from maps import (
    Terrain,
    TerrainLibrary,
    Pickup,
    GoldPickup,
    WeaponPickup,
    HealPickup,
    ItemPickup,
    Tile,
)
from units import Unit


def make_unit(gold: int = 0, health: int = 50, max_health: int = 100, attack_power: int = 10, speed: int = 2) -> Unit:
    unit = Unit(name="Tester", health=max_health, attack_power=attack_power, speed=speed)
    unit.health = health
    unit.action_points = speed
    unit.gold = gold
    return unit


class TerrainAndPickupTest(unittest.TestCase):
    def test_terrain_behavior_and_serialization(self):
        ground = TerrainLibrary.get("Ground")
        self.assertTrue(ground.can_pass())
        self.assertEqual(ground.enter_cost(), 1)

        with self.assertRaises(ValueError):
            Terrain(name="Bad", move_cost=0)

        river = TerrainLibrary.get("River")
        slow_unit = make_unit(speed=2)
        fast_unit = make_unit(speed=5)
        self.assertEqual(river.enter_cost(slow_unit), 3)
        self.assertEqual(river.enter_cost(fast_unit), 2)

        forest = TerrainLibrary.get("Forest")
        weak_unit = make_unit(attack_power=10)
        strong_unit = make_unit(attack_power=25)
        self.assertFalse(forest.can_pass(weak_unit))
        self.assertTrue(forest.can_pass(strong_unit))

        restored = Terrain.from_dict(river.to_dict())
        self.assertEqual(restored.name, "River")
        self.assertEqual(restored.move_cost, river.move_cost)

    def test_pickups_apply_and_serialization(self):
        unit = make_unit(gold=20, health=60, max_health=100, attack_power=10, speed=2)

        with self.assertRaises(ValueError):
            GoldPickup(amount=-5)

        gold = GoldPickup(amount=80)
        gold.apply(unit)
        self.assertEqual(unit.gold, 100)

        weapon = WeaponPickup(name="Blade", bonus=15, value=120)
        weapon.apply(unit)
        self.assertEqual(unit.attack_power, 25)

        heal = HealPickup(name="Potion", heal=50, value=50)
        heal.apply(unit)
        self.assertEqual(unit.health, 100)

        scroll = ItemPickup(name="Speed Scroll", bonus=2, value=75)
        scroll.apply(unit)
        self.assertEqual(unit.speed, 4)
        self.assertEqual(unit.action_points, 4)

        for pickup in (gold, weapon, heal, scroll):
            restored = Pickup.from_dict(pickup.to_dict())
            self.assertEqual(restored.name, pickup.name)
            self.assertEqual(restored.value, pickup.value)


class TileTest(unittest.TestCase):
    def test_position_and_validation(self):
        tile = Tile(q=2, r=3, terrain_name="Ground")
        self.assertEqual(tile.position, (2, 3))
        self.assertEqual(tile.q, 2)
        self.assertEqual(tile.r, 3)

        with self.assertRaises(ValueError):
            tile.position = (-1, 0)
        with self.assertRaises(TypeError):
            tile.position = "invalid"

    def test_collect_pickup(self):
        tile = Tile(q=1, r=1)
        self.assertIsNone(tile.collect_pickup())

        unit = make_unit(gold=10)
        tile.pickup = GoldPickup(amount=40)
        message = tile.collect_pickup(unit)

        self.assertIsNotNone(message)
        self.assertEqual(unit.gold, 50)
        self.assertIsNone(tile.pickup)


if __name__ == "__main__":
    unittest.main()