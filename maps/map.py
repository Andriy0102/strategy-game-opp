class Map:
    ...


class Tile:
    def __init__(self, x: int = 0, y: int = 0, terrain_name: str = "Ground", is_passable = True):
        self.__x = x
        self.__y = y
        self.position = (x, y)
        self.terrain_name = terrain_name
        self.is_passable = is_passable

    @property
    def position(self) -> tuple[int, int]:
        return self.__x, self.__y

    @position.setter
    def position(self, coords: tuple[int, int]):
        if coords is not isinstance(coords, tuple):
            raise TypeError("Position must be a tuple of two integers")

        x, y = coords
        if x < 0 or y < 0:
            raise ValueError("Coordinates cannot be negative!")
        self.__x, self.__y = x, y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __repr__(self):
        return f'Tile({self.x}, {self.y}) is {self.terrain_name} {"passable" if self.is_passable else "not passable"}'


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

    @amount.setter
    def amount(self, value: int):
        if value < 0:
            raise ValueError("Amount cannot be negative!")
        self.__amount = value

    def collect(self, requested_amount) -> int:
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