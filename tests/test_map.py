import os
import random
import tempfile
import unittest
from maps import (
    Map,
    Lane,
    Shop,
    Base,
    SpawnPoint,
    GoldPickup,
    WeaponPickup,
    HealPickup,
    ItemPickup,
    MapValidator,
    Storage,
)
from units import Unit


def make_unit(gold: int = 0, health: int = 50, max_health: int = 100, attack_power: int = 10, speed: int = 2,) -> Unit:
    unit = Unit(name="Tester", health=max_health, attack_power=attack_power, speed=speed)
    unit.health = health
    unit.action_points = speed
    unit.gold = gold
    return unit


class MapTest(unittest.TestCase):
    def setUp(self):
        self.game_map = Map(width=4, height=4)

    def test_position_and_movement(self):
        self.assertTrue(self.game_map.is_valid_position((0, 0)))
        self.assertTrue(self.game_map.is_valid_position((3, 3)))
        self.assertFalse(self.game_map.is_valid_position((4, 4)))
        self.assertFalse(self.game_map.is_valid_position((-1, 0)))

        tile = self.game_map.get_tile((2, 1))
        self.assertIsNotNone(tile)
        self.assertEqual(tile.position, (2, 1))

        self.assertTrue(self.game_map.can_move_to((1, 1)))
        blocked = self.game_map.get_tile((1, 1))
        blocked.is_passable = False
        self.assertFalse(self.game_map.can_move_to((1, 1)))
        self.assertFalse(self.game_map.can_move_to((99, 99)))

    def test_take_pickup(self):
        tile = self.game_map.get_tile((1, 1))
        scroll = ItemPickup(name="Boots", bonus=1, value=75)
        tile.pickup = scroll

        taken = self.game_map.take_pickup((1, 1))
        self.assertEqual(taken, scroll)
        self.assertIsNone(tile.pickup)
        self.assertIsNone(self.game_map.take_pickup((1, 1)))

        unit = make_unit(gold=25, health=40, max_health=100, attack_power=10)
        self.game_map.get_tile((0, 0)).pickup = GoldPickup(amount=75)
        self.game_map.get_tile((0, 1)).pickup = WeaponPickup(name="Sword", bonus=8)
        self.game_map.get_tile((0, 2)).pickup = HealPickup(name="Potion", heal=20)

        self.game_map.take_pickup((0, 0), unit=unit)
        self.game_map.take_pickup((0, 1), unit=unit)
        self.game_map.take_pickup((0, 2), unit=unit)

        self.assertEqual(unit.gold, 100)
        self.assertEqual(unit.attack_power, 18)
        self.assertEqual(unit.health, 60)

    def test_hex_neighbors(self):
        for neighbor in self.game_map.get_neighbors((1, 0)):
            self.assertTrue(self.game_map.is_valid_position(neighbor))
        for neighbor in self.game_map.get_neighbors((1, 1)):
            self.assertTrue(self.game_map.is_valid_position(neighbor))
        self.assertLess(len(self.game_map.get_neighbors((0, 0))), 6)

    def test_bases_and_lanes(self):
        good_base = Base("Good", (0, 0), (0, 1))
        evil_base = Base("Evil", (3, 3), (3, 2))
        self.game_map.add_base(good_base)
        self.game_map.add_base(evil_base)

        self.assertEqual(len(self.game_map.bases), 2)
        self.assertEqual(self.game_map.get_base_by_team("Good"), good_base)
        self.assertIsNone(self.game_map.get_base_by_team("Unknown"))

        with self.assertRaises(ValueError):
            self.game_map.add_base(Base("Third", (1, 1), (1, 2)))

        lane = Lane("Middle", has_bridge=True)
        first = self.game_map.get_tile((1, 1))
        second = self.game_map.get_tile((2, 1))
        lane.add_tile(first)
        lane.add_tile(second)
        self.game_map.add_lane(lane)

        self.assertIn(lane, self.game_map.lanes)
        self.assertTrue(lane.is_connected(self.game_map))
        self.assertEqual(lane.get_next_tile((1, 1)), second)
        self.assertIsNone(lane.get_next_tile((2, 1)))
        self.assertEqual(lane.get_total_move_cost(), 2)

    def test_shop_and_base_buy_item(self):
        shop = Shop(
            catalog=[
                (WeaponPickup(name="Axe", bonus=10), 100),
                (HealPickup(name="Heal", heal=25), 50),
            ]
        )
        base = Base("Good", (0, 0), (0, 1), shop=shop)
        unit = make_unit(gold=130, health=50, max_health=100, attack_power=10)

        self.assertTrue(base.is_at_spawn((0, 0)))
        self.assertTrue(base.is_at_shop((0, 1)))
        self.assertIsNone(base.buy_item("Heal", (0, 0), unit))

        self.assertIsNotNone(base.buy_item("Heal", (0, 1), unit))
        self.assertEqual(unit.gold, 80)
        self.assertEqual(unit.health, 75)

        self.assertIsNone(base.buy_item("Axe", (0, 1), unit))

    def test_spawn_points_and_validation(self):
        point = SpawnPoint(position=(1, 1), item_type="Gold", chance=1.0, respawn_delay=5)
        self.game_map.add_spawn_point(point)
        self.assertIn(point, self.game_map.spawn_points)

        with self.assertRaises(ValueError):
            SpawnPoint(position=(1, 1), item_type="Gold", chance=1.5)
        with self.assertRaises(ValueError):
            SpawnPoint(position=(1, 1), item_type="Gold", respawn_delay=-1)

        spawned = point.spawn(self.game_map, generator=random.Random(42))
        self.assertIsInstance(spawned, GoldPickup)
        self.assertEqual(self.game_map.get_tile((1, 1)).pickup, spawned)

        blocked = self.game_map.get_tile((2, 2))
        blocked.is_passable = False
        self.game_map.add_spawn_point(SpawnPoint(position=(2, 2), item_type="Weapon"))
        self.assertFalse(MapValidator.check_spawn_points(self.game_map))

    def test_serialization_and_storage(self):
        self.game_map.add_base(Base("Good", (0, 0), (0, 1)))
        self.game_map.add_base(Base("Evil", (3, 3), (3, 2)))
        lane = Lane("Bottom")
        lane.add_tile(self.game_map.get_tile((0, 3)))
        lane.add_tile(self.game_map.get_tile((1, 3)))
        self.game_map.add_lane(lane)
        self.game_map.add_spawn_point(SpawnPoint(position=(2, 2), item_type="Heal", chance=0.5))

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            temp_path = tmp.name

        try:
            Storage.save_map_to_file(self.game_map, temp_path)
            loaded = Storage.load_map_from_file(temp_path)
            self.assertEqual(loaded.width, self.game_map.width)
            self.assertEqual(loaded.height, self.game_map.height)
            self.assertEqual(len(loaded.bases), 2)
            self.assertEqual(len(loaded.lanes), 1)
            self.assertEqual(len(loaded.spawn_points), 1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()