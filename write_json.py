import json


def load_json(filename, data):
    # Путь к файлу JSON
    file_path = filename
    # Запись словаря в файл JSON
    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)