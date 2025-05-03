import json
from pathlib import Path

def read_json(path: str):
    with open(Path(path), "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: str, data):
    with open(Path(path), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
