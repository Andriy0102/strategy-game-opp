class Unit:

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

if __name__ == "__main__":
    warrior = Unit(name="Андрій", health=100, attack_power=20, speed=5, x=0, y=0 )
    print(warrior.get_info())