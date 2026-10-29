from .resources import Resources


class Terrain:
    def __init__(self, name: str, is_passable: bool = True, move_cost: int = 1):
        self.name = name
        self.is_passable = is_passable
        self.move_cost = move_cost

    def __repr__(self):
        return f"Terrain({self.name}, passable={self.is_passable}, cost={self.move_cost})"

class TerrainLibrary:
    _terrains = {
        "Ground": Terrain("Ground", True, 1),
        "River": Terrain("River", True, 3),
        "Forest": Terrain("Forest", False, 1),
        "Bridge": Terrain("Bridge", True, 1)
    }
    @classmethod
    def get(cls, name: str) -> Terrain:
        return cls._terrains.get(name, cls._terrains["Ground"])


class Pickup:
    def __init__(self, item_type: str, name: str, value: int = 0):
        self.item_type = item_type
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Pickup({self.item_type}: {self.name}, value={self.value})"

class Tile:
    def __init__(self, q: int = 0, r: int = 0, terrain_name: str = "Ground", is_passable: bool | None = None):
        self.position = (q, r)
        self._terrain = TerrainLibrary.get(terrain_name)
        self.is_passable = is_passable if is_passable is not None else self._terrain.is_passable
        self._resource: Resources | None = None # Holds resource object or None
        self.pickup: Pickup | None = None #An object in a tile

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
    def terrain_name(self) -> str:
        return self._terrain.name

    @terrain_name.setter
    def terrain_name(self, value: str):
        self._terrain = TerrainLibrary.get(value)
        self.is_passable = self._terrain.is_passable

    @property
    def move_cost(self) -> int:
        return self._terrain.move_cost

    @property
    def resource(self) -> Resources | None:
        return self._resource

    @resource.setter
    def resource(self, value: Resources | None):
        self._resource = value

    def __repr__(self):
        return f'Tile({self.q}, {self.r}) is {self.terrain_name} {"passable" if self.is_passable else "not passable"}, res: {self.resource if self.resource else ""}'
