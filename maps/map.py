from .tiles import Tile, Pickup


class Map:
    def __init__(self, width: int, height: int, default_terrain: str = "Ground", default_ispassable: bool = True):
        self._width = width
        self._height = height
        #Basic map generation
        self._grid: list[list[Tile]] = [[Tile(q=q, r=r, terrain_name=default_terrain, is_passable=default_ispassable) for q in range(width)] for r in range(height)]

        #Collections for game architecture
        self.lanes: list["Lane"] = []
        self.bases: list["Base"] = []
        self.spawn_points: list["SpawnPoint"] = []

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    #Checks if the given coordinates are within the map boundaries
    def is_valid_position(self, position:tuple[int, int]) -> bool:
        q, r = position
        return 0 <= q < self._width and 0 <= r < self._height

    #Get title if it has valid passion
    def get_tile(self, position:tuple[int, int]) -> Tile | None:
        if not self.is_valid_position(position):
            return None
        q, r = position
        return self._grid[r][q]

    #Check that can unit move or not
    def can_move_to(self, position:tuple[int, int]) -> bool:
        tile = self.get_tile(position)
        return tile.is_passable if tile else False

    def take_pickup(self, position:tuple[int, int]) -> Pickup | None:
        tile = self.get_tile(position)
        if not tile or not tile.pickup:
            return None

        item = tile.pickup
        tile.pickup = None
        return item

    #Collect resource
    def harvest_resource(self, position:tuple[int, int], requested_amount: int) -> int:
        tile = self.get_tile(position)
        if not tile or not tile.resource:
            return 0

        collected = tile.resource.collect(requested_amount)
        if tile.resource.amount == 0:
            tile.resource = None

        return collected

    #Return 6 neighbors of hex
    def get_neighbors(self, position:tuple[int, int]) -> list[tuple[int, int]]:
        if not self.is_valid_position(position):
            return []

        q, r = position
        horizontal = [(-1, 0), (1, 0)]

        if r % 2 == 0:
            vertical = [(-1, -1), (0, -1), (-1, 1), (0, 1)]
        else:
            vertical = [(0, -1), (1, -1), (0, 1), (1, 1)]

        neighbors = [(q + dq, r + dr) for dq, dr in vertical + horizontal]
        return [pos for pos in neighbors if self.is_valid_position(pos)]

    def add_lane(self, lane: "Lane"):
        self.lanes.append(lane)

    def add_base(self, base: "Base"):
        if len(self.bases) >= 2:
            raise ValueError("Map can only have 2 bases (Good and Evil)!")
        self.bases.append(base)

    def add_spawn_point(self, spawn_point: "SpawnPoint"):
        self.spawn_points.append(spawn_point)

    def get_base_by_team(self, team: str) -> Base | None:
        for base in self.bases:
            if base.team == team:
                return base
        return None

    def __repr__(self):
        return f'Map({self.width}, {self.height})'


class Lane:
    def __init__(self, name: str, has_bridge: bool = False):
        self.name = name # "Top", "Middle", "Bottom"
        self.has_bridge = has_bridge
        self.tiles: list[Tile] = [] #Ordered list of line tiles

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def __repr__(self):
        return f"Lane({self.name}, bridge={self.has_bridge}, tiles_count={len(self.tiles)})"

class Base:
    def __init__(self, team: str, spawn_position: tuple[int, int], shop_position: tuple[int, int]):
        self.team = team
        self.spawn_position = spawn_position
        self.shop_position = shop_position

    def __repr__(self):
        return f"Base(team={self.team}, spawn={self.spawn_position}, shop={self.shop_position})"


class SpawnPoint:
    def __init__(self, position: tuple[int, int], item_type: str, chance: float = 1.0, respawn_delay: int = 0, is_fixed: bool = False):
        self.position = position
        self.item_type = item_type
        self.chance = chance
        self.respawn_delay = respawn_delay
        self.is_fixed = is_fixed

    def __repr__(self):
        return f"SpawnPoint(pos={self.position}, type={self.item_type}, fixed={self.is_fixed})"