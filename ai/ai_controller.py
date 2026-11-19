from abc import ABC, abstractmethod

class AIController:
    def __init__(self, difficulty="easy"):
        if difficulty in ("easy", "medium", "hard"):
            self._difficulty = difficulty
        else:
            self._difficulty = "easy"

        self._turn_count = 0
        self._behaviors = []

    def add_behavior(self, behavior):
        expected_class = self.get_behavior_class()

        if not isinstance(behavior, expected_class):
            raise ValueError(f"Difficulty '{self._difficulty}' requires {expected_class.__name__}")
        self._behaviors.append(behavior)

    def remove_behavior(self, behavior):
        if behavior in self._behaviors:
            self._behaviors.remove(behavior)

    def get_behavior_count(self):
        return len(self._behaviors)

    def set_difficulty(self, difficulty):
        if difficulty  not in ("easy", "medium", "hard"):
            return

        self._difficulty = difficulty
        behavior_class = self.get_behavior_class()
        self._behaviors = [behavior_class(behavior.get_unit()) for behavior in self._behaviors]

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

    def get_behavior_class(self):
        if self._difficulty == "easy":
            return EasyAIBehavior
        elif self._difficulty == "medium":
            return MediumAIBehavior
        else:
            return HardAIBehavior


class AIUnitBehavior(ABC):
    def __init__(self, unit):
        self._unit = unit
        self._action = "wait"

    def get_unit(self):
        return self._unit

    def get_action(self):
        return self._action

    @abstractmethod
    def choose_action(self, enemy_in_range, resource_nearby):
        pass


class EasyAIBehavior(AIUnitBehavior):

    def choose_action(self, enemy_in_range, resource_nearby):
        if not self._unit.is_alive:
            self._action = "dead"
        elif enemy_in_range:
            self._action = "attack"
        else:
            self._action = "move"

        return self._action

class MediumAIBehavior(AIUnitBehavior):
    RETREAT_HEALTH_THRESHOLD = 25

    def choose_action(self, enemy_in_range, resource_nearby):
        if not self._unit.is_alive:
            self._action = "dead"
        elif self._unit.health <= self.RETREAT_HEALTH_THRESHOLD:
            self._action = "retreat"
        elif enemy_in_range:
            self._action = "attack"
        elif resource_nearby:
            self._action = "collect_resource"
        else:
            self._action = "move"
        return self._action

class HardAIBehavior(AIUnitBehavior):
    RETREAT_HEALTH_THRESHOLD = 10

    def choose_action(self, enemy_in_range, resource_nearby):
        if not self._unit.is_alive:
            self._action = "dead"
        elif self._unit.health <= self.RETREAT_HEALTH_THRESHOLD:
            self._action = "retreat"
        elif enemy_in_range:
            self._action = "attack"
        elif resource_nearby:
            self._action = "collect_resource"
        else:
            self._action = "move"
        return self._action
