class Unit:

    def __init__(
            self,
            name: str,
            health: int,
            attack_power: int,
            speed: int,
            x: int =0,
            y: int =0,
            defense: int = 0,
            attack_range: int = 1,
            team: str = "Good"
    ):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.speed = speed
        self.action_points = speed
        self.x = x
        self.y = y
        self.defense = defense
        self.attack_range = attack_range
        self.team = team
        self.is_alive = True

    def __del__(self):
        print(f"[Del] Об'єкт юніта '{self.name}' знищено з пам'яті")

    def get_info(self) -> str:
        status = "Живий" if self.is_alive else "Знищений"
        return f"Юніт:{self.name} | HP: {self.health}|{self.max_health} | Позиція: ({self.x}, {self.y}) | Стан: {status}"

    def move(self, new_x: int, new_y: int, move_cost: int = 1) -> bool:
        if not self.is_alive or move_cost < 0 or self.action_points < move_cost:
             return False

        self.action_points -= move_cost
        self.x = new_x
        self.y = new_y
        return True

    def take_damage(self, damage: int, ignore_defense: bool = False )-> int:
        if not self.is_alive or damage <= 0:
            return 0

        actual_damage = damage if ignore_defense else max(1, damage - self.defense)

        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return actual_damage

    def attack(self, target) -> int:
        if not self.is_alive or not getattr(target, "is_alive", True):
            return 0

        cost = 2
        if self.action_points < cost:
            return 0

        self.action_points -= cost
        dealt = target.take_damage(self.attack_power)
        return dealt if dealt is not None else self.attack_power

    def reset_turn(self):
        self.action_points = self.speed

    def heal(self, amount: int) -> int:
        if not self.is_alive or amount <= 0:
            return 0
        old_health = self.health
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        return self.health - old_health

    def apply_pickup(self, pickup_type: str) -> bool:
        if not self.is_alive:
            return False
        if pickup_type == "Heal":
            self.heal(30)
            return True
        elif pickup_type == "Weapon":
            self.attack_power += 5
            return True
        elif pickup_type == "Ability":
            self.action_points = self.speed
            return True
        return False

    def special_ability(self, target=None) -> bool:
        return False

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "max_health": self.max_health,
            "health": self.health,
            "attack_power": self.attack_power,
            "speed": self.speed,
            "action_points": self.action_points,
            "x": self.x,
            "y": self.y,
            "defense": self.defense,
            "attack_range": self.attack_range,
            "team": self.team,
            "is_alive": self.is_alive,
    }


class Warrior(Unit):

    def __init__(
            self,
            name: str,
            health: int = 120,
            attack_power: int = 20,
            speed: int = 3,
            x: int = 0,
            y: int = 0,
            defense: int = 5,
            attack_range: int = 1,
            team: str = "Good"
    ):
        super().__init__(name, health, attack_power, speed, x, y, defense, attack_range, team)
        self.rage_active = False

    def take_damage(self, damage: int, ignore_defense: bool = False) -> int:
        if not self.is_alive or damage <= 0:
            return 0
        if ignore_defense:
            return super().take_damage(damage, ignore_defense=True)

        reduced_damage = damage - (self.defense + 2)
        if reduced_damage < 1:
            reduced_damage = 1
        return super().take_damage(reduced_damage, ignore_defense=True)

    def attack(self, target) -> int:
        if not self.is_alive or not target.is_alive:
            return 0

        cost = 2
        if self.action_points < cost:
            return 0

        self.action_points -= cost
        if self.rage_active:
            damage = int(self.attack_power * 1.5)
            self.rage_active = False
        else:
            damage = self.attack_power

        dealt = target.take_damage(damage)
        if dealt is None:
            return damage
        return dealt

    def special_ability(self, target=None) -> bool:
        if not self.is_alive or self.action_points < 1 or self.rage_active:
            return False
        self.action_points -= 1
        self.rage_active = True
        return True

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["rage_active"] = self.rage_active
        return data


class Archer(Unit):

    def __init__(
            self,
            name: str,
            health: int = 85,
            attack_power: int = 18,
            speed: int = 4,
            x: int = 0,
            y: int = 0,
            defense: int = 1,
            attack_range: int = 3,
            team: str = "Good"
    ):
        super().__init__(name, health, attack_power, speed, x, y, defense, attack_range, team)

    def attack(self, target) -> int:
        if not self.is_alive or not target.is_alive:
            return 0
        cost = 2
        if self.action_points < cost:
            return 0

        self.action_points -= cost
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        if distance >= 2:
            damage = self.attack_power + 5
        else:
            damage = self.attack_power

        dealt = target.take_damage(damage, ignore_defense=True)
        if dealt is None:
            return damage
        return dealt

    def special_ability(self, target=None) -> bool:
        if not self.is_alive or target is None or not target.is_alive:
            return False
        if self.action_points < 2:
            return False

        self.action_points -= 2
        target.take_damage(self.attack_power + 10, ignore_defense=True)
        return True


class Mage(Unit):

    def __init__(
            self,
            name: str,
            health: int = 70,
            attack_power: int = 22,
            speed: int = 3,
            x: int = 0,
            y: int = 0,
            defense: int = 0,
            attack_range: int = 2,
            team: str = "Good",
            mana: int = 40
    ):
        super().__init__(name, health, attack_power, speed, x, y, defense, attack_range, team)
        self.max_mana = mana
        self.mana = mana

    def attack(self, target) -> int:
        if not self.is_alive or not target.is_alive:
            return 0
        cost = 2
        if self.action_points < cost:
            return 0

        self.action_points -= cost
        dealt = target.take_damage(self.attack_power, ignore_defense=True)
        if dealt is None:
            return self.attack_power
        return dealt

    def special_ability(self, target=None) -> bool:
        if not self.is_alive or target is None or not target.is_alive:
            return False
        if self.action_points < 2 or self.mana < 20:
            return False

        self.action_points -= 2
        self.mana -= 20
        target.heal(25)
        return True

    def reset_turn(self):
        super().reset_turn()
        self.mana += 10
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["max_mana"] = self.max_mana
        data["mana"] = self.mana
        return data


class Squad:

    def __init__(self, name: str):
        self.name = name
        self.units: list[Unit] = []

    def add_unit(self, unit: Unit) -> None:
        if unit not in self.units:
            self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        if unit in self.units:
            self.units.remove(unit)

    def get_alive_units(self) -> list[Unit]:
        return [u for u in self.units if u.is_alive]

    def get_total_health(self) -> int:
        return sum(u.health for u in self.get_alive_units())

    def clear_dead_units(self) -> None:
        self.units = [u for u in self.units if u.is_alive]

    def move_squad(self, cost: int = 1) -> bool:
        alive = self.get_alive_units()
        if not alive:
            return False

        if all(u.action_points >= cost for u in alive):
            for u in alive:
                u.move(u.x + 1, u.y)
            return True
        return False

    def attack_target(self, target: Unit) -> int:
        total_damage = 0
        for unit in self.get_alive_units():
            if unit.action_points >= 2:
                total_damage += unit.attack(target)
        return total_damage

    def __str__(self) -> str:
        alive_count = len(self.get_alive_units())
        total_count = len(self.units)
        return f"Загін '{self.name}' [{alive_count}/{total_count} живих | Загальне HP: {self.get_total_health()}] "

    def __len__(self) -> int:
        return len(self.units)

    def __getitem__(self,index: int) -> Unit:
        return self.units[index]


if __name__ == "__main__":
    warrior = Unit(name="Андрій", health=100, attack_power=20, speed=5, x=0, y=0 )
    enemy = Unit(name="Ворог", health=40, attack_power=10, speed=3, x=1, y=1 )

    #ТЕСТ
    print("\n Демонмстрація переміщення ")
    warrior.move(1,0)

    print("\n Демонстрація атаки ")
    warrior.attack(enemy)
    warrior.attack(enemy)

    print("\n Ластовий стан ")
    print(warrior.get_info())
    print(enemy.get_info())