import unittest
from maps import MapEditor, Map, Tile, Resources


class MapEditorTest(unittest.TestCase):
    def setUp(self):
        self.editor = MapEditor(width=5, height=5)

    def test_set_tile(self):
        new_tile = Tile(1, 1, terrain_name="Mountain", is_passable=False)
        success = self.editor.set_tile(1, 1, new_tile)
        self.assertTrue(success)

        tile = self.editor.map.get_tile((1, 1))
        self.assertIsNotNone(tile)
        if tile:
            self.assertEqual(tile.terrain_name, "Mountain")
            self.assertFalse(tile.is_passable)

        self.assertFalse(self.editor.set_tile(99, 99, new_tile))


    def test_set_resource(self):
        res = Resources("Gold", 100)

        self.assertTrue(self.editor.set_resource(2, 2, res))
        tile = self.editor.map.get_tile((2, 2))
        self.assertIsNotNone(tile)
        if tile and tile.resource:
            self.assertEqual(tile.resource.res_type, "Gold")

        mountain = Tile(2, 3, terrain_name="Mountain", is_passable=False)
        self.editor.set_tile(2, 3, mountain)
        self.assertFalse(self.editor.set_resource(2, 3, res))


    def test_create_level(self):
        level_map = self.editor.create_level()
        self.assertIsInstance(level_map, Map)
        self.assertEqual(level_map.width, 5)

if __name__ == '__main__':
    unittest.main()
