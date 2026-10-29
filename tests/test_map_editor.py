import unittest
from maps import Map, Base, Lane, Tile, Resources, MapEditor, MapValidator, MapTheme


class MapEditorTest(unittest.TestCase):
    def setUp(self):
        self.editor = MapEditor(width=5, height=5)

    def test_set_tile(self):
        new_tile = Tile(1, 1, terrain_name="Forest", is_passable=False)

        success = self.editor.set_tile(1, 1, new_tile)
        self.assertTrue(success)

        tile = self.editor.map.get_tile((1, 1))
        self.assertIsNotNone(tile)
        if tile:
            self.assertEqual(tile.terrain_name, "Forest")
            self.assertFalse(tile.is_passable)
        self.assertFalse(self.editor.set_tile(99, 99, new_tile))

    def test_set_resource(self):
        res = Resources("Gold", 100)
        self.assertTrue(self.editor.set_resource(2, 2, res))
        tile = self.editor.map.get_tile((2, 2))
        self.assertIsNotNone(tile)
        if tile and tile.resource:
            self.assertEqual(tile.resource.res_type, "Gold")

        mountain_tile = Tile(2, 3, terrain_name="Mountain", is_passable=False)
        self.editor.set_tile(2, 3, mountain_tile)
        self.assertFalse(self.editor.set_resource(2, 3, res))

    def test_map_theme(self):
        theme = MapTheme(name="Volcano")
        self.assertEqual(theme.name, "Volcano")
        self.assertIsNotNone(theme.get_terrain("Ground"))
        self.editor.apply_theme(theme)
        self.assertEqual(self.editor.theme.name, "Volcano")

    def test_validator_and_create_level(self):
        errors = MapValidator.validate(self.editor.map)
        self.assertGreater(len(errors), 0)
        with self.assertRaises(ValueError):
            self.editor.create_level()
        self.editor.add_base(Base("Good", (0, 0), (0, 1)))
        self.editor.add_base(Base("Evil", (4, 4), (4, 3)))
        lane = Lane("Mid")
        lane.add_tile(self.editor.map.get_tile((2, 2)))
        self.editor.add_lane(lane)
        level_map = self.editor.create_level()
        self.assertIsInstance(level_map, Map)
        self.assertEqual(level_map.width, 5)


if __name__ == '__main__':
    unittest.main()