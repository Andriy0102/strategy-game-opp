from .map import Map, Lane, Base, SpawnPoint
from .tiles import Tile, TerrainLibrary, Terrain, Pickup


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
    def validate(game_map: Map) -> list[str]:
        errors = []
        if not MapValidator.check_bases(game_map):
            errors.append("Invalid bases: Map must contain 2 valid bases ('Good' and 'Evil') with distinct spawn and shop positions.")
        if not MapValidator.check_lanes(game_map):
            errors.append("Invalid lanes: Map must contain at least one connected path/lane.")
        if not MapValidator.check_spawn_points(game_map):
            errors.append("Invalid spawn points: Some spawn points are out of bounds or on non-enterable terrain.")
        return errors

    @staticmethod
    def check_bases(game_map: Map) -> bool:
        teams = [base.team for base in game_map.bases]
        if len(game_map.bases) != 2 or "Good" not in teams or "Evil" not in teams:
            return False
        for base in game_map.bases:
            if base.spawn_position == base.shop_position:
                return False
            if not base.is_valid_on_map(game_map):
                return False
        return True

    @staticmethod
    def check_lanes(game_map: Map) -> bool:
        if len(game_map.lanes) == 0:
            return False
        for lane in game_map.lanes:
            if not lane.tiles or not lane.is_connected(game_map):
                return False
            if any(not tile.can_enter() for tile in lane.tiles):
                return False
        return True

    @staticmethod
    def check_spawn_points(game_map: Map) -> bool:
        for spawn_point in game_map.spawn_points:
            if not game_map.is_valid_position(spawn_point.position):
                return False
            tile = game_map.get_tile(spawn_point.position)
            if tile is None or not tile.can_enter():
                return False
        return True


class MapEditor:
    def __init__(self, width: int = 10, height: int = 10, theme: MapTheme | None = None):
        self.theme = theme or MapTheme("DefaultTheme")
        self.map = Map(width, height, default_terrain=self.theme.get_terrain("Ground").name)

    def set_tile(self, q: int, r: int, new_tile: Tile) -> bool:
        current_tile = self.map.get_tile((q, r))
        if current_tile is None:
            return False

        current_tile.terrain_name = new_tile.terrain_name
        current_tile.is_passable = new_tile.is_passable
        current_tile.pickup = new_tile.pickup
        return True

    def set_pickup(self, q: int, r: int, pickup: Pickup | None) -> bool:
        tile = self.map.get_tile((q, r))
        if tile is None or not tile.can_enter():
            return False

        tile.pickup = pickup
        return True

    def add_lane(self, lane: Lane) -> bool:
        self.map.add_lane(lane)
        return True

    def add_base(self, base: Base) -> bool:
        try:
            self.map.add_base(base)
            return True
        except ValueError:
            return False

    def add_spawn_point(self, spawn_point: SpawnPoint) -> bool:
        try:
            self.map.add_spawn_point(spawn_point)
            return True
        except ValueError:
            return False

    def apply_theme(self, theme: MapTheme, replace_ground_only: bool = True) -> MapTheme:
        previous_ground_name = self.theme.get_terrain("Ground").name
        new_ground = theme.get_terrain("Ground")
        self.theme = theme

        for r in range(self.map.height):
            for q in range(self.map.width):
                tile = self.map.get_tile((q, r))
                if tile is None:
                    continue
                if not replace_ground_only or tile.terrain_name == previous_ground_name:
                    tile.terrain_name = new_ground.name
                    tile.is_passable = new_ground.is_passable

        return self.theme

    def create_level(self) -> Map:
        errors = MapValidator.validate(self.map)
        if errors:
            raise ValueError("Level validation failed:\n" + "\n".join(errors))
        return self.map