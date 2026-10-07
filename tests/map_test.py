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
    pass


class ResourcesTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
