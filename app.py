import json
import pandas as pd
from get_folder import get_public_folder_files
from create_shipownerss import create_shipowners, get_data_owners
from create_ships_json import create_ships, get_data_sheeps
from write_json import load_json
from docks import plus, get_docks, get_dok_sh
from routes import create_routes_json, get_data_routes
from danya import get_data, get_data_date, data_list_null



public_folder_url = 'https://disk.yandex.ru/d/CyBFEERMlPX9tw'
files = get_public_folder_files(public_folder_url)

sheets_names = ["РАЗОВЫЕ", "Северный", "Северный1А",
                    "Исторический", "Центральный", "Круговой",
                    "Коломенский", "Серебряный Бор", "Западный"]
list_num = 1
for file in files:
    print(list_num)
    for sheets in sheets_names:
        print(sheets)
        df = pd.read_excel(file['file'], sheet_name=sheets)
        get_dok_sh(df, sheets)

dock = plus()

list_num = 1
for file in files:
    print(list_num)
    list_num += 1
    # if list_num < 6:
    for sheets in sheets_names:
        print(sheets)
        df = pd.read_excel(file['file'], sheet_name=sheets)
        marshrut = []
        if sheets == "РАЗОВЫЕ":
            column = "Наименование судовладельца"
        else:
            column = "Судовладелец"
            marshrut = df.iloc[0].fillna("")
            df = df.iloc[1:, :]
            df.rename(columns=df.iloc[0], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df = df.iloc[1:, :]
            create_routes_json(df, marshrut, sheets, dock)
        df[column] = df[column].fillna("")
        df["Судно"] = df["Судно"].fillna("")
        owners = create_shipowners(df, column)
        ship = create_ships(df, owners, column)
        get_data(df, sheets, marshrut, ship, dock)
    load_json(f"json_files\\{file['name']}.json", get_data_date())
    data_list_null()
load_json("json_files\\shipowners.json", get_data_owners())
load_json("json_files\\ships.json", get_data_sheeps())
load_json("json_files\\docks.json", get_docks())
load_json("json_files\\routes.json", get_data_routes())