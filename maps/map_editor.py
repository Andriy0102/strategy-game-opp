from maps.map import Map, Tile, Resources


class MapEditor:
    def __init__(self, width: int = 10, height: int = 10):
        self.map = Map(width, height)

    def set_tile(self, q: int, r: int, new_tile: Tile) -> bool:
        current_tile = self.map.get_tile((q, r))
        if current_tile is None:
            return False

        current_tile.terrain_name = new_tile.terrain_name
        current_tile.is_passable = new_tile.is_passable
        return True

    def set_resource(self, q: int, r: int, resource: Resources) -> bool:
        tile = self.map.get_tile((q, r))
        if tile is None or not tile.is_passable:
            return False

        tile.resource = resource
        return True

    def create_level(self) -> Map:
        return self.map
