class Unit:
    """ Клас Юніт описує юніта для покрокової стратегії.
    Та також відповідає захарактеристики, переміщення, отримання пошкодження та атаку
    """

    def __init__(self, name: str, health: int, attack_power: int, speed: int, x: int =0, y: int =0):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.speed = speed
        self.action_points = speed
        self.x = x
        self.y = y
        self.is_alive = True

        print(f"[Init] Створення юніта '{self.name}' (HP: {self.health}, atk:{self.attack_power}) y позиції ({self.x}, {self.y})")

    def __del__(self):
        print(f"[Del] Об'єкт юніта '{self.name}' знищено з пам'яті")

    def get_info(self) -> str:
        status = "Живий" if self.is_alive else "Знищений"
        return f"Юніт:{self.name} | HP: {self.health}|{self.max_health} | Позиція: ({self.x}, {self.y}) | Стан: {status}"

    def move(self, new_x: int, new_y: int) -> bool:
        if not self.is_alive:
            print(f"{self.name} не може преміщатися, оскільки знищений")
            return False

        cost = 1
        if self.action_points <cost:
            print(f"Недостатньо очок для переміщення {self.name}")
            return False

        self.action_points -= cost
        self.x = new_x
        self.y = new_y
        print(f"{self.name} перемістився у позицію ({self.x}, {self.y}). Залишилося AP: {self.action_points}")
        return True

    def take_damage(self, damage: int):
        if not self.is_alive:
            print(f"{self.name} уже знищений і не може отримувати шкоду")
            return

        self.health -= damage
        print(f"{self.name} отримав {damage} пошкодження. Залишилося HP {max(0, self.health)}")

        if self.health <= 0:
            self.health =0
            self.is_alive = False
            print(f"Юніт {self.name} був знищений")

    def attack(self, target) -> int:
        if not self.is_alive:
            print(f"{self.name} не можу атакувати, оскільки знищений")
            return 0

        cost = 2
        if self.action_points <cost:
            print(f"Недостатньо очок дій для атаки юнітом {self.name}")
            return 0

        self.action_points -= cost
        print(f"{self.name} атакує {target.name} із силою {self.attack_power} (витрачено {cost} AP)")
        target.take_damage(self.attack_power)
        return self.attack_power

    def reset_turn(self):
        self.action_points = self.speed
        print(f"Хід юніта {self.name} оновлено. Очки дій відновлено до {self.action_points}")

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