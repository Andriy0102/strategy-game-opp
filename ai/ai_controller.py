class AIController:
    def __init__(self, difficulty="easy"):
        if difficulty in ("easy", "medium", "hard"):
            self._difficulty = difficulty
        else:
            self._difficulty = "easy"

        self._turn_count = 0

    def set_difficulty(self, difficulty):
        if difficulty in ("easy", "medium", "hard"):
            self._difficulty = difficulty

    def get_difficulty(self):
        return self._difficulty

    def get_enemy_squad_size(self):
        if self._difficulty == "easy":
            return 3
        elif self._difficulty == "medium":
            return 5
        else:
            return 7

    def choose_action(self, enemy_in_range, resource_nearby):
        if enemy_in_range:
            return "attack"

        if resource_nearby and self._difficulty != "easy":
            return "collect_resource"

        return "move"

    def make_turn(self, enemy_in_range, resource_nearby):
        self._turn_count += 1
        return self.choose_action(enemy_in_range, resource_nearby)

    def get_turn_count(self):
        return self._turn_count


class AIUnitBehavior:
    def __init__(self, unit_name, health=100):
        self._unit_name = unit_name
        self._health = health
        self._action = "wait"

    def get_unit_name(self):
        return self._unit_name

    def get_health(self):
        return self._health

    def get_action(self):
        return self._action

    def set_health(self, health):
        if health < 0:
            self._health = 0
        else:
            self._health = health

    def take_damage(self, damage):
        if damage > 0:
            self._health -= damage

        if self._health <= 0:
            self._health = 0

    def choose_action(self, enemy_in_range, resource_nearby):
        if self._health == 0:
            self._action = "dead"

        elif self._health <= 25:
            self._action = "retreat"

        elif enemy_in_range:
            self._action = "attack"

        elif resource_nearby:
            self._action = "collect_resource"

        else:
            self._action = "move"

        return self._action

    def is_alive(self):
        return self._health > 0