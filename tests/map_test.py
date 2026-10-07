import unittest
from maps import Map, Tile, Resources

class MapTest(unittest.TestCase):
    def setUp(self):
        self.map = Map(width=4, height=4)

    def test_is_valid_position(self):
        self.assertTrue(self.map.is_valid_position((0, 0)))
        self.assertTrue(self.map.is_valid_position((3, 3)))
        self.assertFalse(self.map.is_valid_position((4, 4)))
        self.assertFalse(self.map.is_valid_position((-1, 0)))

    def test_get_tile(self):
        tile = self.map.get_tile((2, 1))
        self.assertIsNotNone(tile)
        self.assertEqual(tile.position, (2, 1))

    def test_can_move_to(self):
        self.assertTrue(self.map.can_move_to((1, 1)))

        tile = self.map.get_tile((1, 1))
        if tile:
            tile.is_passable = False

        self.assertFalse(self.map.can_move_to((1, 1)))
        self.assertFalse(self.map.can_move_to((99, 99)))

    def test_harvest_resource(self):
        tile = self.map.get_tile((2, 2))
        if tile:
            tile.resource = Resources("Gold", 100)

        harvested = self.map.harvest_resource((2, 2), 40)
        self.assertEqual(harvested, 40)

        if tile and tile.resource:
            self.assertEqual(tile.resource.amount, 60)

        self.assertEqual(self.map.harvest_resource((0, 0), 10), 0)

    def test_hex_get_neighbors(self):
        neighbors_r0 = self.map.get_neighbors((1, 0))
        for pos in neighbors_r0:
            self.assertTrue(self.map.is_valid_position(pos))

        neighbors_r1 = self.map.get_neighbors((1, 1))
        for pos in neighbors_r1:
            self.assertTrue(self.map.is_valid_position(pos))

        corner_neighbors = self.map.get_neighbors((0, 0))
        self.assertLess(len(corner_neighbors), 6)


class TileTest(unittest.TestCase):
    def test_position_and_validation(self):
        tile = Tile(q=2, r=3, terrain_name="Forest")
        self.assertEqual(tile.position, (2, 3))

        with self.assertRaises(ValueError):
            tile.position = (-1, 0)

        with self.assertRaises(TypeError):
            tile.position = "invalid" 

    def test_resource(self):
        tile = Tile(1, 1)
        self.assertIsNone(tile.resource)
        tile.resource = Resources("Stone", 40)
        self.assertIsNotNone(tile.resource)


class ResourcesTest(unittest.TestCase):
    def test_init_and_validation(self):
        res = Resources("Gold", 100)
        self.assertEqual(res.res_type, "Gold")
        self.assertEqual(res.amount, 100)

        with self.assertRaises(ValueError):
            res.amount = -50

    def test_collect(self):
        res = Resources("Wood", 50)
        self.assertEqual(res.collect(20), 20)
        self.assertEqual(res.amount, 30)

        self.assertEqual(res.collect(100), 30)
        self.assertEqual(res.amount, 0)
        self.assertEqual(res.collect(-10), 0)

if __name__ == '__main__':
    unittest.main()
