import json
from .map import Map


class Storage:
    @staticmethod
    def save_map_to_file(map_obj: Map, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(map_obj.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_map_from_file(filename: str) -> Map:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Map.from_dict(data)