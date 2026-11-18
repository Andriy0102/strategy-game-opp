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