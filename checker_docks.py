import pandas as pd
import json
from get_folder import get_public_folder_files
from write_json import load_json


def ships_shipsowners_exel(df, sheet):
    global dict_exel
    if sheet == "РАЗОВЫЕ":
        df = df.iloc[:,[0, 1]]
    else:
        df = df.iloc[2:,[3, 4]]
    df.columns.values[0] = 'Судовладелец'
    df.columns.values[1] = 'Судно'
    df["Судно"] = df["Судно"].fillna("")
    df["Судовладелец"] = df["Судовладелец"].fillna("")
    df['Судовладелец'] = df['Судовладелец'].apply(lambda x: ''.join(x.strip().split('"')).lower())
    df['Судно'] = df['Судно'].apply(lambda x: ''.join(x.strip().split('"')).lower())
    # shipsowners_un.extend(df['Судовладелец'])
    # while '' in shipsowners_un:
    #     shipsowners_un.remove('')
    no_duplicates = df.drop_duplicates(subset=["Судовладелец", "Судно"])
    for index, row in no_duplicates.iterrows():
        if row[1] == "" or row[0] == "":
            continue
        dict_exel[row[0]] = dict_exel.get(row[0], set()) | {row[1]}


def ships_shipsowners_json():
    dict_json = {}
    with open('json_files\\ships.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = data["data"]
    for ship in data:
        key = ''.join(ship["shipowner"]["name"].strip().split('"')).lower()
        dict_json[key] = dict_json.get(key, set()) | {''.join(ship["name"].strip().split('"')).lower()}
    return dict_json


def ships_shipsowners_api():
    dict_api = {}
    with open('ships.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = data["data"]
    for ship in data:
        key = ''.join(ship["shipowner"]["name"].strip().split('"')).lower()
        dict_api[key] = dict_api.get(key, set()) | {''.join(ship["name"].strip().split('"')).lower()}
    return dict_api


def result_ship():
    dict_json = ships_shipsowners_json()
    dict_api = ships_shipsowners_api()
    result = {}
    result_exel, result_json, result_api = {}, {}, {}
    count_json, count_exel, count_api = 0,0,0
    for i in dict_exel.keys():
        count_exel += len(dict_exel[i])
        result_exel[i] = len(dict_exel[i])
    for i in dict_json.keys():
        count_json += len(dict_json[i])
        result_json[i] = len(dict_json[i])
    for i in dict_api.keys():
        count_api += len(dict_api[i])
        result_api[i] = len(dict_api[i])
    # check = {}
    # for i in dict_exel:
    #     # print(dict_json[i])
    #     # print(type(i))
    #     check[i] = list(dict_exel[i])
    # load_json("check.json", check)
    result["Общее количество Судовладельцев в JSON:"] = len(dict_json)
    result["Общее количество Судовладельцев в EXCEL:"] = len(dict_exel)
    result["Общее количество Судовладельцев в API:"] = len(dict_api)
    result["Общее количество Судов в API:"] = count_api
    result["Общее количество Судов в JSON:"] = count_json
    result["Общее количество Судов в EXCEL:"] = count_exel
    result["Количество судов по Судовладельцам в JSON:"] = result_json
    result["Количество судов по Судовладельцам в EXCEL:"] = result_exel
    result["Количество судов по Судовладельцам в API:"] = result_api
    load_json("result_ship.json", result)

dict_exel = {}

def check_ones(df):
    global set_docks
    df = [' '.join(i.strip().lower().split("-")) for i in df if i != '' and i.strip().lower() != 'срв']
    set_docks = set_docks.union(set(df))


def check_docks(df):
    global set_docks
    marshrut = df.iloc[0].fillna("")
    points = [' '.join(i.strip().lower().split("-")) for i in marshrut if i != '' and i.strip().lower() != 'срв']
    set_docks = set_docks.union(set(points))


def check_docks_json():
    list_docs = []
    with open('json_files\\docks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = data["data"]
    for docks in data:
        list_docs.append(docks["name"])
    return list_docs


def check_docks_api():
    list_docs_api = []
    with open('docks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = data["data"]
    for docks in data:
        list_docs_api.append(docks["name"])
    return list_docs_api




def result_docks():
    global set_docks
    result = {}
    list_docs = check_docks_json()
    list_docs_api = check_docks_api()
    result["Количесвтво доков в JSON"] = len(list_docs)
    result["Количесвтво доков в EXCEL"] = len(set_docks)
    result["Количесвтво доков в API"] = len(list_docs_api)
    result["Доки в JSON"] = list_docs
    result["Доки в EXCEK"] = list(set_docks)
    result["Доки в API"] = list_docs_api
    load_json("result_dokcs.json", result)

    

public_folder_url = 'https://disk.yandex.ru/d/CyBFEERMlPX9tw'
files = get_public_folder_files(public_folder_url)

sheets_names = ["Северный", "Северный1А",
                    "Исторический", "Центральный", "Круговой",
                    "Коломенский", "Серебряный Бор", "Западный"]
col = 1
set_docks = set()
for file in files:
    print(col)
    col += 1
    if col == 16:
        break
    for sheets in sheets_names:
        df = pd.read_excel(file['file'], sheet_name=sheets)
        ships_shipsowners_exel(df, sheets)
        check_docks(df)
    df = pd.read_excel(file['file'], sheet_name="РАЗОВЫЕ")
    ships_shipsowners_exel(df, "РАЗОВЫЕ")
    df["Новое наименование причала"] = df["Новое наименование причала"].fillna("")
    check_ones(df["Новое наименование причала"].unique())
    print(len(set_docks))

result_ship()
result_docks()
# print(set_docks)