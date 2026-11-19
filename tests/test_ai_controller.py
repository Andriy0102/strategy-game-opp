from ai.ai_controller import AIController, AIUnitBehavior, EasyAIBehavior, MediumAIBehavior, HardAIBehavior
from units import Unit
from inspect import isabstract

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

def test_invalid_set_difficulty():
    ai = AIController("medium")
    ai.set_difficulty("banana")

    assert ai.get_difficulty() == "medium"

def test_enemy_squad_size():
    easy_ai = AIController("easy")
    medium_ai = AIController("medium")
    hard_ai = AIController("hard")

    assert easy_ai.get_enemy_squad_size() == 3
    assert medium_ai.get_enemy_squad_size() == 5
    assert hard_ai.get_enemy_squad_size() == 7

def test_ai_unit_behavior_is_abstract():

    assert isabstract(AIUnitBehavior)

def test_add_and_remove_behavior():
    ai = AIController("easy")
    unit = Unit("Soldier", 100, 20, 5)
    behavior = EasyAIBehavior(unit)

    ai.add_behavior(behavior)
    assert ai.get_behavior_count() == 1

    ai.remove_behavior(behavior)
    assert ai.get_behavior_count() == 0



def test_behavior_unit():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = EasyAIBehavior(unit)

    assert behavior.get_unit() is unit
    assert behavior.get_action() == "wait"

def test_invalid_behavior_for_difficulty():
    ai = AIController("easy")
    unit = Unit("Soldier", 100, 20, 5)
    behavior = HardAIBehavior(unit)

    try:
        ai.add_behavior(behavior)
        assert False
    except ValueError:
        pass


def test_easy_attack_action():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = EasyAIBehavior(unit)
    action = behavior.choose_action(True, False)

    assert action == "attack"

def test_easy_ai_does_not_collect_resource():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = EasyAIBehavior(unit)
    action = behavior.choose_action(False, True)

    assert action == "move"

def test_medium_collect_resource():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = MediumAIBehavior(unit)
    action = behavior.choose_action(False, True)

    assert action == "collect_resource"

def test_medium_move_action():
    unit = Unit("Soldier", 100, 20, 5)
    behavior = MediumAIBehavior(unit)
    action = behavior.choose_action(False, False)

    assert action == "move"

def test_medium_retreat_action():
    unit = Unit("Soldier", 20, 20, 5)
    behavior = MediumAIBehavior(unit)
    action = behavior.choose_action(True, False)

    assert action == "retreat"

def test_hard_retreat_action():
    unit = Unit("Soldier", 10, 20, 5)
    behavior = HardAIBehavior(unit)
    action = behavior.choose_action(True, False)

    assert action == "retreat"


def test_dead_unit():
    unit = Unit("Soldier", 10, 20, 5)
    unit.take_damage(20)
    behavior = MediumAIBehavior(unit)
    action = behavior.choose_action(True, True)

    assert action == "dead"

def test_polymorphism():
    unit = Unit("Soldier", 20, 20, 5)
    easy_behavior = EasyAIBehavior(unit)
    medium_behavior = MediumAIBehavior(unit)
    hard_behavior = HardAIBehavior(unit)

    easy_action = easy_behavior.choose_action(True, False)
    medium_action = medium_behavior.choose_action(True, False)
    hard_action = hard_behavior.choose_action(True, False)

    assert easy_action == "attack"
    assert medium_action == "retreat"
    assert hard_action == "attack"

def test_make_turn():
    ai = AIController("medium")
    unit1 = Unit("Soldier 1", 100, 20, 5)
    unit2 = Unit("Soldier 2", 20, 20, 5)
    behavior1 = MediumAIBehavior(unit1)
    behavior2 = MediumAIBehavior(unit2)
    ai.add_behavior(behavior1)
    ai.add_behavior(behavior2)
    actions = ai.make_turn(True, False)

    assert actions == ["attack", "retreat"]
    assert ai.get_turn_count() == 1

def test_change_difficulty_changes_behavior():
    ai = AIController("easy")
    unit = Unit("Soldier", 20, 20, 5)
    behavior = EasyAIBehavior(unit)
    ai.add_behavior(behavior)

    actions_before = ai.make_turn(True, False)
    assert actions_before == ["attack"]

    ai.set_difficulty("medium")
    actions_after = ai.make_turn(True, False)
    assert actions_after == ["retreat"]

def test_inheritance():
    assert issubclass(EasyAIBehavior, AIUnitBehavior)
    assert issubclass(MediumAIBehavior, AIUnitBehavior)
    assert issubclass(HardAIBehavior, AIUnitBehavior)

test_ai_controller_creation()
test_invalid_difficulty()
test_set_difficulty()
test_invalid_set_difficulty()
test_enemy_squad_size()
test_ai_unit_behavior_is_abstract()
test_add_and_remove_behavior()
test_behavior_unit()
test_invalid_behavior_for_difficulty()
test_easy_attack_action()
test_easy_ai_does_not_collect_resource()
test_medium_collect_resource()
test_medium_move_action()
test_medium_retreat_action()
test_hard_retreat_action()
test_dead_unit()
test_polymorphism()
test_make_turn()
test_change_difficulty_changes_behavior()
test_inheritance()

print("All AI tests passed!")