from abc import ABC, abstractmethod


class Terrain:
    def __init__(self, name: str = "Ground", is_passable: bool = True, move_cost: int = 1):
        if move_cost < 1:
            raise ValueError("Move cost must be at least 1!")
        self.name = name
        self.is_passable = is_passable
        self.move_cost = move_cost

    def can_pass(self, unit=None) -> bool:
        return self.is_passable

    def enter_cost(self, unit=None) -> int:
        return self.move_cost

    def to_dict(self) -> dict:
        return {
            "type": self.name,
            "is_passable": self.is_passable,
            "move_cost": self.move_cost,
        }

    @classmethod
    def from_dict(cls, data: dict | str) -> "Terrain":
        if isinstance(data, str):
            return TerrainLibrary.get(data)

        t_type = data.get("type", "Ground")
        cost = data.get("move_cost")
        passable = data.get("is_passable")

        if t_type == "Ground":
            return Terrain(name="Ground", move_cost=cost if cost is not None else 1)
        if t_type == "River":
            return RiverTerrain(move_cost=cost if cost is not None else 3)
        if t_type == "Forest":
            return ForestTerrain(move_cost=cost if cost is not None else 2, is_passable=passable if passable is not None else False)
        if t_type == "Bridge":
            return Terrain(name="Bridge", move_cost=cost if cost is not None else 1)

        return cls(
            name=t_type,
            is_passable=passable if passable is not None else True,
            move_cost=cost if cost is not None else 1,
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(name={self.name!r}, "
            f"passable={self.is_passable}, cost={self.move_cost})"
        )


class RiverTerrain(Terrain):
    def __init__(self, move_cost: int = 3):
        super().__init__("River", is_passable=True, move_cost=move_cost)

    def enter_cost(self, unit=None) -> int:
        if unit is not None and getattr(unit, "speed", 0) >= 4:
            return max(1, self.move_cost - 1)
        return self.move_cost


class ForestTerrain(Terrain):
    def __init__(self, move_cost: int = 2, is_passable: bool = False):
        super().__init__("Forest", is_passable=is_passable, move_cost=move_cost)

    def can_pass(self, unit=None) -> bool:
        if unit is not None and getattr(unit, "attack_power", 0) >= 20:
            return True
        return self.is_passable


class TerrainLibrary:
    _terrains: dict[str, Terrain] = {
        "Ground": Terrain(name="Ground", is_passable=True, move_cost=1),
        "River": RiverTerrain(),
        "Forest": ForestTerrain(),
        "Bridge": Terrain(name="Bridge", is_passable=True, move_cost=1),
    }

    @classmethod
    def get(cls, name: str) -> Terrain:
        return cls._terrains.get(name, cls._terrains["Ground"])


class Pickup(ABC):
    def __init__(self, name: str, value: int = 0):
        if value < 0:
            raise ValueError("Pickup cannot be negative!")
        self.name = name
        self.value = value

    @abstractmethod
    def apply(self, unit) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> Pickup:
        p_type = data.get("type", "GoldPickup")
        name = data.get("name", p_type)
        value = data.get("value", data.get("amount", 0))

        if p_type == "GoldPickup":
            return GoldPickup(amount=value, name=name)
        if p_type == "WeaponPickup":
            return WeaponPickup(
                name=name,
                bonus=data.get("bonus", 10),
                value=value,
            )
        if p_type == "HealPickup":
            return HealPickup(
                name=name,
                heal=data.get("heal", 30),
                value=value,
            )
        if p_type == "ItemPickup":
            return ItemPickup(
                name=name,
                bonus=data.get("bonus", 1),
                value=value,
            )
        raise ValueError(f"Unknown Pickup type: {p_type}")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, value={self.value})"


class GoldPickup(Pickup):
    def __init__(self, amount: int = 50, name: str = "Gold"):
        super().__init__(name=name, value=amount)

    def apply(self, unit) -> str:
        if unit is not None and hasattr(unit, "gold"):
            unit.gold += self.value
        return f"{self.name}: +{self.value}"


class WeaponPickup(Pickup):
    def __init__(self, name: str = "Weapon", bonus: int = 10, value: int = 100):
        super().__init__(name=name, value=value)
        self.bonus = bonus

    def apply(self, unit) -> str:
        if unit is not None and hasattr(unit, "attack_power"):
            unit.attack_power += self.bonus
        return f"{self.name}: +{self.bonus}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data


class HealPickup(Pickup):
    def __init__(self, name: str = "Heal", heal: int = 10, value: int = 50):
        super().__init__(name=name, value=value)
        self.heal = heal

    def apply(self, unit) -> str:
        healed = self.heal
        if unit is not None and hasattr(unit, "health") and hasattr(unit, "max_health"):
            before = unit.health
            unit.health = min(unit.max_health, unit.health + self.heal)
            healed = unit.health - before
        return f"{self.name}:HP +{healed}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["heal"] = self.heal
        return data


class ItemPickup(Pickup):
    def __init__(self, name: str = "Speed Scroll", bonus: int = 1, value: int = 75):
        super().__init__(name=name, value=value)
        self.bonus = bonus

    def apply(self, unit) -> str:
        if unit is not None:
            if hasattr(unit, "speed"):
                unit.speed += self.bonus
            if hasattr(unit, "action_points"):
                unit.action_points += self.bonus
        return f"{self.name}:speed +{self.bonus}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data


class Tile:
    def __init__(self, q: int = 0, r: int = 0, terrain_name: str = "Ground", is_passable: bool | None = None):
        self.position = (q, r)
        self._terrain = TerrainLibrary.get(terrain_name)
        self.is_passable = is_passable if is_passable is not None else self._terrain.is_passable
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
    def terrain(self) -> Terrain:
        return self._terrain

    @terrain.setter
    def terrain(self, value: Terrain):
        self._terrain = value
        self.is_passable = value.is_passable

    @property
    def terrain_name(self) -> str:
        return self._terrain.name

    @terrain_name.setter
    def terrain_name(self, value: str):
        self.terrain = TerrainLibrary.get(value)

    @property
    def move_cost(self) -> int:
        return self._terrain.move_cost

    def can_enter(self, unit=None) -> bool:
        if not self.is_passable:
            return False
        return self._terrain.can_pass(unit)

    def get_enter_cost(self, unit=None) -> int:
        return max(1, self._terrain.enter_cost(unit))

    def collect_pickup(self, unit=None) -> str | None:
        if self.pickup is None:
            return None
        result = self.pickup.apply(unit)
        self.pickup = None
        return result

    def to_dict(self) -> dict:
        return {
            "q": self.q,
            "r": self.r,
            "terrain_name": self.terrain_name,
            "terrain": self._terrain.to_dict(),
            "is_passable": self.is_passable,
            "pickup": self.pickup.to_dict() if self.pickup else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tile":
        terrain_source = data.get("terrain", data.get("terrain_name", "Ground"))
        terrain_obj = Terrain.from_dict(terrain_source)
        tile = cls(
            q=data["q"],
            r=data["r"],
            terrain_name=terrain_obj.name,
            is_passable=data.get("is_passable", terrain_obj.is_passable),
        )
        tile.terrain = terrain_obj
        if data.get("pickup"):
            tile.pickup = Pickup.from_dict(data["pickup"])
        return tile

    def __repr__(self):
        return (
            f"Tile({self.q}, {self.r}) is {self.terrain_name} "
            f"{'passable' if self.is_passable else 'not passable'}, "
            f"pickup: {self.pickup or ''}"
        )