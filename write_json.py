import json


def load_json(filename, data):
    file_path = filename
    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)