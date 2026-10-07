class Map:
    def __init__(self, width: int, height: int, default_terrain: str = "Ground", default_ispassable: bool = True):
        self.__width = width
        self.__height = height
        #Basic map generation
        self.__grid: list[list[Tile]] = [[Tile(q=q, r=r, terrain_name=default_terrain, is_passable=default_ispassable) for q in range(width)] for r in range(height)]

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    #Checks if the given coordinates are within the map boundaries
    def is_valid_position(self, position:tuple[int, int]) -> bool:
        q, r = position
        return 0 <= q < self.__width and 0 <= r < self.__height

    #Get title if it has valid passion
    def get_tile(self, position:tuple[int, int]) -> Tile | None:
        if not self.is_valid_position(position):
            return None
        q, r = position
        return self.__grid[r][q]

    #Check that can unit move or not
    def can_move_to(self, position:tuple[int, int]) -> bool:
        tile = self.get_tile(position)
        return tile.is_passable if tile else False

    #Collect resource
    def harvest_resource(self, position:tuple[int, int], requested_amount: int) -> int:
        tile = self.get_tile(position)
        if not tile or not tile.resource:
            return 0
        return tile.resource.collect(requested_amount)

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

        valid_neighbors = []
        for dq, dr in (horizontal + vertical):
            neighbors_pos = (q + dq, r + dr)
            if self.is_valid_position(neighbors_pos):
                valid_neighbors.append(neighbors_pos)
        return valid_neighbors

    def __repr__(self):
        return f'Map({self.width}, {self.height})'


class Tile:
    def __init__(self, q: int = 0, r: int = 0, terrain_name: str = "Ground", is_passable: bool = True):
        self.__q = 0
        self.__r = 0
        self.position = (q, r)
        self.terrain_name = terrain_name
        self.is_passable = is_passable
        self.__resource: Resources | None = None # Holds resource object or None

    @property
    def position(self) -> tuple[int, int]:
        return self.__q, self.__r

    # Protect coordinates from invalid types or negative indices
    @position.setter
    def position(self, coords: tuple[int, int]):
        if not isinstance(coords, tuple):
            raise TypeError("Position must be a tuple of two integers")

        q, r = coords
        if q < 0 or r < 0:
            raise ValueError("Coordinates cannot be negative!")
        self.__q, self.__r = q, r

    @property
    def q(self) -> int:
        return self.__q

    @property
    def r(self) -> int:
        return self.__r

    @property
    def resource(self) -> Resources | None:
        return self.__resource

    @resource.setter
    def resource(self, value: Resources | None):
        self.__resource = value

    def __repr__(self):
        return f'Tile({self.q}, {self.r}) is {self.terrain_name} {"passable" if self.is_passable else "not passable"}, res: {self.resource if self.__resource else ""}'


class Resources:
    def __init__(self, res_type: str = "Gold", amount: int = 1):
        self.__res_type = res_type
        self.__amount = 0
        self.amount = amount

    @property
    def res_type(self) -> str:
        return self.__res_type

    @property
    def amount(self) -> int:
        return self.__amount

    # Prevent economic bugs or negative quantities
    @amount.setter
    def amount(self, value: int):
        if value < 0:
            raise ValueError("Amount cannot be negative!")
        self.__amount = value

    #Safely deducts resources and returns the amount actually collected
    def collect(self, requested_amount: int) -> int:
        if requested_amount <= 0:
            return 0
        elif requested_amount > self.amount:
            taken_amount = self.amount
            self.__amount = 0
        else:
            taken_amount = requested_amount
            self.__amount -= requested_amount

        return taken_amount

    def __repr__(self):
        return f'Resources({self.res_type}: {self.amount})'