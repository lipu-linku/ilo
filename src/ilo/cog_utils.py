import json
from pathlib import Path


def load_file(file_path, file_name):
    path = Path(file_path).parent / file_name
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        return list(f.readlines())
