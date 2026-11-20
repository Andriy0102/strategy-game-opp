import random
from .tiles import Tile, Pickup, GoldPickup, WeaponPickup, HealPickup, ItemPickup


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
    def can_move_to(self, position:tuple[int, int], unit=None) -> bool:
        tile = self.get_tile(position)
        return tile.can_enter(unit) if tile else False

    def take_pickup(self, position:tuple[int, int], unit=None) -> Pickup | str | None:
        tile = self.get_tile(position)
        if not tile or not tile.pickup:
            return None

        if unit is not None:
            return tile.collect_pickup(unit)

        item = tile.pickup
        tile.pickup = None
        return item

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

        neighbors = [(q + delta_q, r + delta_r) for delta_q, delta_r in vertical + horizontal]
        return [cell for cell in neighbors if self.is_valid_position(cell)]

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

    def to_dict(self) -> dict:
        tiles_list = []
        for r in range(self.height):
            for q in range(self.width):
                tile = self.get_tile((q, r))
                if tile:
                    tiles_list.append(tile.to_dict())

        return {
            "width": self.width,
            "height": self.height,
            "tiles": tiles_list,
            "bases": [base.to_dict() for base in self.bases],
            "spawn_points": [point.to_dict() for point in self.spawn_points],
            "lanes": [lane.to_dict() for lane in self.lanes]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Map":
        game_map = cls(width=data["width"], height=data["height"])

        for tile_data in data.get("tiles", []):
            tile = Tile.from_dict(tile_data)
            if not game_map.is_valid_position(tile.position):
                raise ValueError(f"Tile position out of bounds: {tile.position}")
            game_map._grid[tile.r][tile.q] = tile

        for base_data in data.get("bases", []):
            game_map.add_base(Base.from_dict(base_data))

        for point_data in data.get("spawn_points", []):
            game_map.add_spawn_point(SpawnPoint.from_dict(point_data))

        for lane_data in data.get("lanes", []):
            lane = Lane.from_dict(lane_data, game_map)
            game_map.add_lane(lane)

        return game_map

    def __repr__(self):
        return f'Map({self.width}, {self.height})'


class Lane:
    def __init__(self, name: str, has_bridge: bool = False):
        self.name = name # "Top", "Middle", "Bottom"
        self.has_bridge = has_bridge
        self.tiles: list[Tile] = [] #Ordered list of line tiles

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def get_total_move_cost(self, unit=None) -> int:
        return sum(tile.get_enter_cost(unit) for tile in self.tiles)

    def get_next_tile(self, current_position: tuple[int, int]) -> Tile | None:
        target = tuple(current_position)
        for step, tile in enumerate(self.tiles):
            if tile.position == target and step + 1 < len(self.tiles):
                return self.tiles[step + 1]
        return None

    def is_connected(self, game_map: Map) -> bool:
        if not self.tiles:
            return False
        if not game_map.is_valid_position(self.tiles[0].position):
            return False
        for step in range(len(self.tiles) - 1):
            start = self.tiles[step].position
            end = self.tiles[step + 1].position
            if not game_map.is_valid_position(end) or end not in game_map.get_neighbors(start):
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "has_bridge": self.has_bridge,
            "tiles": [list(tile.position) for tile in self.tiles],
        }

    @classmethod
    def from_dict(cls, data: dict, game_map: Map) -> "Lane":
        lane = cls(name=data["name"], has_bridge=data.get("has_bridge", False))
        for position in data.get("tiles", []):
            tile = game_map.get_tile(tuple(position))
            if tile is None:
                raise ValueError(f"Lane '{lane.name}' references invalid tile position {position}")
            lane.add_tile(tile)
        return lane

    def __repr__(self):
        return f"Lane({self.name}, bridge={self.has_bridge}, tiles_count={len(self.tiles)})"


class Shop:
    def __init__(self, catalog: list[tuple[Pickup, int]] | None = None):
        self.catalog: list[tuple[Pickup, int]] = (
            list(catalog)
            if catalog is not None
            else [
                (WeaponPickup(), 100),
                (HealPickup(), 50),
                (ItemPickup(), 75),
            ]
        )

    def add_item(self, pickup: Pickup, price: int):
        if price < 0:
            raise ValueError("Price cannot be negative!")
        self.catalog.append((pickup, price))

    def buy(self, item_name: str, unit) -> str | None:
        if unit is None or not hasattr(unit, "gold"):
            return None

        for pickup, price in self.catalog:
            if pickup.name == item_name:
                if unit.gold < price:
                    return None
                unit.gold -= price
                return pickup.apply(unit)
        return None

    def to_dict(self) -> dict:
        return {
            "catalog": [
                {"item": pickup.to_dict(), "price": price}
                for pickup, price in self.catalog
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Shop":
        items = [
            (Pickup.from_dict(entry["item"]), entry["price"])
            for entry in data.get("catalog", [])
        ]
        return cls(catalog=items)

    def __repr__(self):
        return f"Shop(items_count={len(self.catalog)})"


class Base:
    def __init__(self, team: str, spawn_position: tuple[int, int], shop_position: tuple[int, int], shop: Shop | None = None):
        self.team = team
        self.spawn_position = tuple(spawn_position)
        self.shop_position = tuple(shop_position)
        self.shop = shop if shop is not None else Shop()

    def is_at_spawn(self, position: tuple[int, int]) -> bool:
        return tuple(position) == self.spawn_position

    def is_at_shop(self, position: tuple[int, int]) -> bool:
        return tuple(position) == self.shop_position

    def is_valid_on_map(self, game_map: Map) -> bool:
        spawn_tile = game_map.get_tile(self.spawn_position)
        shop_tile = game_map.get_tile(self.shop_position)
        return (
            spawn_tile is not None
            and shop_tile is not None
            and spawn_tile.can_enter()
            and shop_tile.can_enter()
        )

    def buy_item(self, item_name: str, buyer_position: tuple[int, int], unit) -> str | None:
        if not self.is_at_shop(buyer_position):
            return None
        return self.shop.buy(item_name, unit)

    def to_dict(self) -> dict:
        return {
            "team": self.team,
            "spawn_position": list(self.spawn_position),
            "shop_position": list(self.shop_position),
            "shop": self.shop.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Base":
        shop_data = data.get("shop")
        shop_object = Shop.from_dict(shop_data) if isinstance(shop_data, dict) else None
        return cls(
            team=data["team"],
            spawn_position=tuple(data["spawn_position"]),
            shop_position=tuple(data["shop_position"]),
            shop=shop_object,
        )

    def __repr__(self):
        return f"Base(team={self.team}, spawn={self.spawn_position}, shop={self.shop_position})"


class SpawnPoint:
    def __init__(self, position: tuple[int, int], item_type: str, chance: float = 1.0, respawn_delay: int = 0, is_fixed: bool = False):
        self.position = tuple(position)
        self.item_type = item_type
        self.chance = chance
        self.respawn_delay = respawn_delay
        self.is_fixed = is_fixed

    @property
    def chance(self) -> float:
        return self._chance

    @chance.setter
    def chance(self, value: float):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Chance must be between 0.0 and 1.0!")
        self._chance = value

    @property
    def respawn_delay(self) -> int:
        return self._respawn_delay

    @respawn_delay.setter
    def respawn_delay(self, value: int):
        if value < 0:
            raise ValueError("Respawn delay cannot be negative!")
        self._respawn_delay = value

    def can_spawn(self, tile: Tile | None, generator: random.Random | None = None) -> bool:
        if tile is None or not tile.can_enter() or tile.pickup is not None:
            return False
        active_generator = generator if generator is not None else random
        return active_generator.random() <= self.chance

    def spawn(self, game_map: Map, generator: random.Random | None = None) -> Pickup | None:
        tile = game_map.get_tile(self.position)
        if not self.can_spawn(tile, generator):
            return None

        #Replace with a pickup registry/factory when adding custom/modded types.
        if self.item_type == "Gold":
            pickup = GoldPickup()
        elif self.item_type == "Weapon":
            pickup = WeaponPickup()
        elif self.item_type == "Heal":
            pickup = HealPickup()
        else:
            pickup = ItemPickup(name=self.item_type)

        tile.pickup = pickup
        return pickup

    def to_dict(self) -> dict:
        return {
            "position": list(self.position),
            "item_type": self.item_type,
            "chance": self.chance,
            "respawn_delay": self.respawn_delay,
            "is_fixed": self.is_fixed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SpawnPoint":
        return cls(
            position=tuple(data["position"]),
            item_type=data.get("item_type", "Gold"),
            chance=data.get("chance", 1.0),
            respawn_delay=data.get("respawn_delay", 0),
            is_fixed=data.get("is_fixed", False),
        )

    def __repr__(self):
        return f"SpawnPoint(pos={self.position}, type={self.item_type}, fixed={self.is_fixed})"