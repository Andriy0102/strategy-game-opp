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
        pass

    def attack(self, target) -> int:
        pass

    def reset_turn(self):
        self.action_points = self.speed
        print(f"Хід юніта {self.name} оновлено. Очки дій відновлено до {self.action_points}")

if __name__ == "__main__":
    warrior = Unit(name="Андрій", health=100, attack_power=20, speed=5, x=0, y=0 )
    print(warrior.get_info())

    #перевірка переміщення
    warrior.move(2,3)
    warrior.move(4, 5)
    print(warrior.get_info())

    #скидання ходу
    warrior.reset_turn()