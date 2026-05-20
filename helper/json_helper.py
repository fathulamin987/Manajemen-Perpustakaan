import json
import os


def baca_json(path):

    if not os.path.exists(path):
        return []

    with open(path, "r") as file:
        return json.load(file)


def simpan_json(path, data):

    with open(path, "w") as file:
        json.dump(data, file, indent=4)