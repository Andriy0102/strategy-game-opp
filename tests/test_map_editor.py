import unittest
from maps import (
    Map,
    Base,
    Lane,
    SpawnPoint,
    Tile,
    GoldPickup,
    WeaponPickup,
    HealPickup,
    ItemPickup,
    MapEditor,
    MapValidator,
    MapTheme,
)


class MapEditorTest(unittest.TestCase):
    def setUp(self):
        self.editor = MapEditor(width=5, height=5)

    def test_set_tile(self):
        new_tile = Tile(q=1, r=1, terrain_name="River", is_passable=True)
        self.assertTrue(self.editor.set_tile(1, 1, new_tile))

        tile = self.editor.map.get_tile((1, 1))
        self.assertIsNotNone(tile)
        self.assertEqual(tile.terrain_name, "River")
        self.assertTrue(tile.can_enter())
        self.assertFalse(self.editor.set_tile(99, 99, new_tile))

    def test_set_pickups_and_blocked_tile(self):
        gold = GoldPickup(amount=100)
        weapon = WeaponPickup(name="Axe", bonus=10)
        heal = HealPickup(name="Heal", heal=25)
        item = ItemPickup(name="Shield", bonus=1)

        self.assertTrue(self.editor.set_pickup(0, 0, gold))
        self.assertTrue(self.editor.set_pickup(1, 0, weapon))
        self.assertTrue(self.editor.set_pickup(2, 0, heal))
        self.assertTrue(self.editor.set_pickup(3, 0, item))

        self.assertEqual(self.editor.map.get_tile((0, 0)).pickup, gold)
        self.assertEqual(self.editor.map.get_tile((1, 0)).pickup, weapon)
        self.assertEqual(self.editor.map.get_tile((2, 0)).pickup, heal)
        self.assertEqual(self.editor.map.get_tile((3, 0)).pickup, item)

        blocked_tile = Tile(q=2, r=3, terrain_name="Forest", is_passable=False)
        self.editor.set_tile(2, 3, blocked_tile)
        self.assertFalse(self.editor.set_pickup(2, 3, gold))

    def test_apply_theme(self):
        custom_tile = Tile(q=0, r=0, terrain_name="River", is_passable=True)
        self.editor.set_tile(0, 0, custom_tile)

        theme = MapTheme(name="Volcano")
        self.editor.apply_theme(theme, replace_ground_only=True)

        self.assertEqual(self.editor.theme.name, "Volcano")
        self.assertEqual(self.editor.map.get_tile((0, 0)).terrain_name, "River")
        self.assertEqual(
            self.editor.map.get_tile((1, 1)).terrain_name,
            theme.get_terrain("Ground").name,
        )

    def test_add_validator_and_create_level(self):
        errors = MapValidator.validate(self.editor.map)
        self.assertGreater(len(errors), 0)
        with self.assertRaises(ValueError):
            self.editor.create_level()

        self.assertTrue(self.editor.add_base(Base("Good", (0, 0), (0, 1))))
        self.assertTrue(self.editor.add_base(Base("Evil", (4, 4), (4, 3))))
        self.assertFalse(self.editor.add_base(Base("Extra", (1, 1), (1, 2))))

        lane = Lane("Middle")
        lane.add_tile(self.editor.map.get_tile((2, 2)))
        lane.add_tile(self.editor.map.get_tile((3, 2)))
        self.assertTrue(self.editor.add_lane(lane))
        self.assertTrue(self.editor.add_spawn_point(SpawnPoint((1, 1), "Gold")))

        level_map = self.editor.create_level()
        self.assertIsInstance(level_map, Map)
        self.assertEqual(level_map.width, 5)


if __name__ == "__main__":
    unittest.main()