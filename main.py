from maps import (
    MapEditor,
    Base,
    Lane,
    GoldPickup,
    WeaponPickup,
    HealPickup,
    ItemPickup,
)
from maps.storage import Storage


def main():
    print("1. Initializing MapEditor (5x5 grid)...")
    editor = MapEditor(width=5, height=5)

    print("2. Adding bases and a connected lane...")
    editor.add_base(Base("Good", (0, 0), (0, 1)))
    editor.add_base(Base("Evil", (4, 4), (4, 3)))

    lane = Lane("MainLane")
    for coord in [(2, 2), (3, 2)]:
        lane.add_tile(editor.map.get_tile(coord))
    editor.add_lane(lane)

    print("3. Placing pickups on tiles...")
    editor.set_pickup(2, 2, GoldPickup(amount=150))
    editor.set_pickup(1, 2, WeaponPickup(name="Blade", bonus=12))
    editor.set_pickup(2, 1, HealPickup(name="Potion", heal=35))
    editor.set_pickup(3, 1, ItemPickup(name="Speed Scroll", bonus=1))

    print("4. Validating and building the level...")
    try:
        game_map = editor.create_level()
        print("Success: Map passed validation!")
    except ValueError as err:
        print(f"Validation error: {err}")
        return

    filename = "test_level_demo.json"
    print(f"5. Saving map to '{filename}' and loading it back...")
    Storage.save_map_to_file(game_map, filename)
    loaded_map = Storage.load_map_from_file(filename)

    print(
        f"Done: Loaded {loaded_map.width}x{loaded_map.height} map, "
        f"bases: {len(loaded_map.bases)}, lanes: {len(loaded_map.lanes)}."
    )


if __name__ == "__main__":
    main()