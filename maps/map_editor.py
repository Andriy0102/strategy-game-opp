from .map import Map, Lane, Base, SpawnPoint
from .tiles import Tile, TerrainLibrary, Terrain
from .resources import Resources


class MapTheme:
    def __init__(self, name: str, terrains: type[TerrainLibrary] | None = None, loot_kinds: list[str] | None = None):
        self.name = name
        self.terrains = terrains or TerrainLibrary
        self.loot_kinds = loot_kinds or ["Gold", "Weapon", "Heal", "Ability"]

    def get_terrain(self, name: str) -> Terrain:
        return self.terrains.get(name)

    def __repr__(self):
        return f"MapTheme(name={self.name}, loot_kinds={self.loot_kinds})"


class MapValidator:
    @staticmethod
    def validate(map_obj: Map) -> list[str]:

        errors = []
        if not MapValidator.check_bases(map_obj):
            errors.append("Invalid bases: Map must contain exactly 2 bases ('Good' and 'Evil').")
        if not MapValidator.check_lanes(map_obj):
            errors.append("Invalid lanes: Map must contain at least one defined path/lane.")
        if not MapValidator.check_spawn_points(map_obj):
            errors.append("Invalid spawn points: Some spawn points are out of bounds or on impassable terrain.")
        return errors

    @staticmethod
    def check_bases(map_obj: Map) -> bool:
        teams = [base.team for base in map_obj.bases]
        return len(map_obj.bases) == 2 and "Good" in teams and "Evil" in teams

    @staticmethod
    def check_lanes(map_obj: Map) -> bool:
        return len(map_obj.lanes) > 0

    @staticmethod
    def check_spawn_points(map_obj: Map) -> bool:
        for sp in map_obj.spawn_points:
            if not map_obj.is_valid_position(sp.position):
                return False
            tile = map_obj.get_tile(sp.position)
            if tile and not tile.is_passable:
                return False
        return True


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