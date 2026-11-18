class AIController:
    def __init__(self, difficulty="easy"):
        if difficulty in ("easy", "medium", "hard"):
            self._difficulty = difficulty
        else:
            self._difficulty = "easy"

        self._turn_count = 0
        self._behaviors = []

    def add_behavior(self, behavior):
        self._behaviors.append(behavior)

    def remove_behavior(self, behavior):
        if behavior in self._behaviors:
            self._behaviors.remove(behavior)

    def get_behavior_count(self):
        return len(self._behaviors)

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


    def make_turn(self, enemy_in_range, resource_nearby):
        self._turn_count += 1
        actions = []
        for behavior in self._behaviors:
            action = behavior.choose_action(enemy_in_range, resource_nearby)
            actions.append(action)
        return actions

    def get_turn_count(self):
        return self._turn_count


class AIUnitBehavior:
    def __init__(self, unit):
        self._unit = unit
        self._action = "wait"

    def get_unit(self):
        return self._unit

    def get_action(self):
        return self._action

    def choose_action(self, enemy_in_range, resource_nearby, difficulty ="easy"):
        if not self._unit.is_alive:
            self._action = "dead"

        elif self._unit.health <= 25:
            self._action = "retreat"
        elif enemy_in_range:
            self._action = "attack"

        elif resource_nearby and difficulty != "easy":
            self._action = "collect_resource"

        else:
            self._action = "move"

        return self._action