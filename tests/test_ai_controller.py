from ai.ai_controller import AIController, AIUnitBehavior


def test_ai_controller_creation():
    ai = AIController("medium")
    assert ai.get_difficulty() == "medium"
    assert ai.get_turn_count() == 0

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


def test_ai_controller_action():
    ai = AIController("medium")
    assert ai.choose_action(True, False) == "attack"
    assert ai.choose_action(False, True) == "collect_resource"
    assert ai.choose_action(False, False) == "move"


def test_make_turn():
    ai = AIController("medium")
    action = ai.make_turn(True, False)
    assert action == "attack"
    assert ai.get_turn_count() == 1


def test_unit_creation():
    unit = AIUnitBehavior("Soldier")
    assert unit.get_unit_name() == "Soldier"
    assert unit.get_health() == 100
    assert unit.get_action() == "wait"
    assert unit.is_alive() is True


def test_take_damage():
    unit = AIUnitBehavior("Soldier")
    unit.take_damage(35)
    assert unit.get_health() == 65

def test_negative_health():
    unit = AIUnitBehavior("Soldier")
    unit.set_health(-10)
    assert unit.get_health() == 0
    assert unit.is_alive() is False

def test_unit_collect_resource():
    unit = AIUnitBehavior("Soldier")
    action = unit.choose_action(False, True)
    assert action == "collect_resource"

def test_unit_move():
    unit = AIUnitBehavior("Soldier")
    action = unit.choose_action(False, False)
    assert action == "move"

def test_unit_retreat():
    unit = AIUnitBehavior("Soldier", 20)
    action = unit.choose_action(True, False)
    assert action == "retreat"


def test_dead_unit():
    unit = AIUnitBehavior("Soldier", 0)
    action = unit.choose_action(True, True)
    assert action == "dead"
    assert unit.is_alive() is False


test_ai_controller_creation()
test_invalid_difficulty()
test_set_difficulty()
test_enemy_squad_size()
test_ai_controller_action()
test_make_turn()

test_unit_creation()
test_take_damage()
test_negative_health()
test_unit_collect_resource()
test_unit_move()
test_unit_retreat()
test_dead_unit()

print("All tests passed!")