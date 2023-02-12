import json


def load(file_path):
    with open(f"defines/{file_path}.json", encoding="utf-8") as f:
        return json.load(f)


def plaintext(file_path):
    with open(f"defines/{file_path}.txt", encoding="utf-8") as f:
        return list(f.readlines())


text = load("text")
