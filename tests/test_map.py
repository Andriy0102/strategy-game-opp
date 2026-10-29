import unittest
from maps import Map, Lane, Base, SpawnPoint, Tile, Pickup, Resources, MapValidator


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

    def test_take_pickup(self):
        tile = self.map.get_tile((1, 1))
        item = Pickup(name="Boots", item_type="Artifact", value=500)
        tile.pickup = item
        taken = self.map.take_pickup((1, 1))
        self.assertEqual(taken, item)
        self.assertIsNone(tile.pickup)
        self.assertIsNone(self.map.take_pickup((1, 1)))

    def test_hex_get_neighbors(self):
        neighbors_r0 = self.map.get_neighbors((1, 0))
        for pos in neighbors_r0:
            self.assertTrue(self.map.is_valid_position(pos))
        neighbors_r1 = self.map.get_neighbors((1, 1))
        for pos in neighbors_r1:
            self.assertTrue(self.map.is_valid_position(pos))
        corner_neighbors = self.map.get_neighbors((0, 0))
        self.assertLess(len(corner_neighbors), 6)

    def test_bases_and_lanes(self):
        base_good = Base("Good", (0, 0), (0, 1))
        base_evil = Base("Evil", (3, 3), (3, 2))
        self.map.add_base(base_good)
        self.map.add_base(base_evil)
        self.assertEqual(len(self.map.bases), 2)
        self.assertEqual(self.map.get_base_by_team("Good"), base_good)
        with self.assertRaises(ValueError):
            self.map.add_base(Base("Neutral", (1, 1), (1, 2)))
        lane = Lane("Top")
        self.map.add_lane(lane)
        self.assertIn(lane, self.map.lanes)

    def test_spawn_points(self):
        sp = SpawnPoint(position=(1, 1), item_type="Gold", chance=0.8, respawn_delay=5)
        self.map.spawn_points.append(sp)
        self.assertIn(sp, self.map.spawn_points)

        sp_out = SpawnPoint(position=(10, 10), item_type="Potion")
        self.map.spawn_points.append(sp_out)

        tile = self.map.get_tile((2, 2))
        tile.is_passable = False
        sp_blocked = SpawnPoint(position=(2, 2), item_type="Weapon")
        self.map.spawn_points.append(sp_blocked)
        self.assertFalse(MapValidator.check_spawn_points(self.map))


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