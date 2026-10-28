from ai.ai_controller import AIController, AIUnitBehavior
from units import Unit


def test_ai_controller_creation():
    ai = AIController("medium")

    assert ai.get_difficulty() == "medium"
    assert ai.get_turn_count() == 0
    assert ai.get_behavior_count() == 0


def test_invalid_difficulty():
    ai = AIController("banana")

    assert ai.get_difficulty() == "easy"


def test_set_difficulty():
    ai = AIController()

    ai.set_difficulty("hard")

    assert ai.get_difficulty() == "hard"


def test_enemy_squad_size():
    easy_ai = AIController("easy")
    medium_ai = AIController("medium")
    hard_ai = AIController("hard")

    assert easy_ai.get_enemy_squad_size() == 3
    assert medium_ai.get_enemy_squad_size() == 5
    assert hard_ai.get_enemy_squad_size() == 7


def test_add_behavior():
    ai = AIController()

    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    ai.add_behavior(behavior)

    assert ai.get_behavior_count() == 1


def test_remove_behavior():
    ai = AIController()

    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    ai.add_behavior(behavior)
    ai.remove_behavior(behavior)

    assert ai.get_behavior_count() == 0


def test_behavior_unit():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    assert behavior.get_unit() is unit
    assert behavior.get_action() == "wait"


def test_attack_action():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(True, False, "medium")

    assert action == "attack"


def test_collect_resource():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(False, True, "medium")

    assert action == "collect_resource"


def test_easy_ai_does_not_collect_resource():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(False, True, "easy")

    assert action == "move"


def test_move_action():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(False, False, "medium")

    assert action == "move"


def test_retreat_action():
    unit = Unit("Soldier", 20, 20, 5)
    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(True, False, "medium")

    assert action == "retreat"


def test_dead_unit():
    unit = Unit("Soldier", 10, 20, 5)
    unit.take_damage(20)

    behavior = AIUnitBehavior(unit)

    action = behavior.choose_action(True, True, "medium")

    assert action == "dead"


def test_make_turn():
    ai = AIController("medium")

    unit1 = Unit("Soldier 1", 100, 20, 5)
    unit2 = Unit("Soldier 2", 20, 20, 5)

    behavior1 = AIUnitBehavior(unit1)
    behavior2 = AIUnitBehavior(unit2)

    ai.add_behavior(behavior1)
    ai.add_behavior(behavior2)

    actions = ai.make_turn(True, False)

    assert actions == ["attack", "retreat"]
    assert ai.get_turn_count() == 1


test_ai_controller_creation()
test_invalid_difficulty()
test_set_difficulty()
test_enemy_squad_size()

test_add_behavior()
test_remove_behavior()
test_behavior_unit()

test_attack_action()
test_collect_resource()
test_easy_ai_does_not_collect_resource()
test_move_action()
test_retreat_action()
test_dead_unit()

test_make_turn()

print("All AI tests passed!")