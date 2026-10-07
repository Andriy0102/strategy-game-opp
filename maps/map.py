class Map:
    def __init__(self, width: int, height: int, default_terrain: str = "Ground", default_ispassable: bool = True):
        self._width = width
        self._height = height
        #Basic map generation
        self._grid: list[list[Tile]] = [[Tile(q=q, r=r, terrain_name=default_terrain, is_passable=default_ispassable) for q in range(width)] for r in range(height)]

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

    def __repr__(self):
        return f'Map({self.width}, {self.height})'


class Tile:
    def __init__(self, q: int = 0, r: int = 0, terrain_name: str = "Ground", is_passable: bool = True):
        self.position = (q, r)
        self.terrain_name = terrain_name
        self.is_passable = is_passable
        self._resource: Resources | None = None # Holds resource object or None

    @property
    def position(self) -> tuple[int, int]:
        return self._q, self._r

    # Protect coordinates from invalid types or negative indices
    @position.setter
    def position(self, coords: tuple[int, int]):
        if not isinstance(coords, tuple) or len(coords) != 2:
            raise TypeError("Position must be a tuple of two integers")

        q, r = coords
        if not isinstance(q, int) or not isinstance(r, int):
            raise TypeError("Coordinates must be integers")
        if q < 0 or r < 0:
            raise ValueError("Coordinates cannot be negative!")

        self._q, self._r = q, r

    @property
    def q(self) -> int:
        return self._q

    @property
    def r(self) -> int:
        return self._r

    @property
    def resource(self) -> Resources | None:
        return self._resource

    @resource.setter
    def resource(self, value: Resources | None):
        self._resource = value

    def __repr__(self):
        return f'Tile({self.q}, {self.r}) is {self.terrain_name} {"passable" if self.is_passable else "not passable"}, res: {self.resource if self.resource else ""}'


class Resources:
    def __init__(self, res_type: str = "Gold", amount: int = 1):
        self._res_type = res_type
        self.amount = amount

    @property
    def res_type(self) -> str:
        return self._res_type

    @property
    def amount(self) -> int:
        return self._amount

    # Prevent economic bugs or negative quantities
    @amount.setter
    def amount(self, value: int):
        if value < 0:
            raise ValueError("Amount cannot be negative!")
        self._amount = value

    #Safely deducts resources and returns the amount actually collected
    def collect(self, requested_amount: int) -> int:
        if requested_amount <= 0:
            return 0

        taken_amount = min(self.amount, requested_amount)
        self.amount -= taken_amount
        return taken_amount

    def __repr__(self):
        return f'Resources({self.res_type}: {self.amount})'