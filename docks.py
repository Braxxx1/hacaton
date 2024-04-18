import pandas as pd
from write_json import load_json

 
def get_ower(df):
    global berth, id_dock, docks_list, docks_set
    df_temp = df
    selected_columns = df_temp.iloc[:, 7:]
    for j_columns in range(1, selected_columns.shape[1], 3):
        select = selected_columns.iloc[0, j_columns]
        temp_set = berth.get(select, set())
        unique_values = set(filter(lambda x: isinstance(x, str), selected_columns.iloc[2:,j_columns-1].unique()))
        berth[select] = temp_set | unique_values
        if select not in docks_set:
            docks_set.add(select)
            temp_dict = {
                    "id": id_dock,
                    "name": select,
                    "berth_cnt": 0,
                    "berth": [],
                    "address": None,
                    "type": "Причал",
                    "exploitation_type": {
                        "id": 1,
                        "name": "Пассажирские"
                    },
                    "department": None,
                    "timetable": {
                        "start": "00:00",
                        "end": "23:59"
                    },
                    "description": None,
                    "geopoint": {
                        "lon": None,
                        "lat": None
                    }
                }
            docks_list.append(temp_dict)
            id_dock+=1
 
 
def get_ones(df_temp):
    global berth, id_dock, docks_list, docks_set
    selected_columns = df_temp.iloc[:, [3,4]]
    no_duplicates = selected_columns.drop_duplicates(subset=["Новое наименование причала", "Швартовое место"])
    no_duplicates["Швартовое место"] = no_duplicates["Швартовое место"].fillna('-')
    for index, row in no_duplicates.iterrows():
        name_dock, name_sh = row.values[0], row.values[1]
        if name_dock != 'СРВ' and name_sh != '-':
            temp_set = berth.get(name_dock, set())
            unique_values = set(name_sh)
            berth[name_dock] = temp_set | unique_values
            if name_dock not in docks_set:
                docks_set.add(name_dock)
                temp_dict = {
                        "id": id_dock,
                        "name": name_dock,
                        "berth_cnt": 0,
                        "berth": [],
                        "address": None,
                        "type": "Причал",
                        "exploitation_type": {
                            "id": 1,
                            "name": "Пассажирские"
                        },
                        "department": None,
                        "timetable": {
                            "start": "00:00",
                            "end": "23:59"
                        },
                        "description": None,
                        "geopoint": {
                            "lon": None,
                            "lat": None
                        }
                    }
                docks_list.append(temp_dict)
                id_dock+=1
 
 
def get_dok_sh(df, column):
    if column != 'РАЗОВЫЕ':
        get_ower(df)
    else:
        get_ones(df)

               
def plus():  
    id_sh = 1
    for i_dock in range(len(docks_list)):
        temp_sh = berth[docks_list[i_dock]["name"]]
        docks_list[i_dock]["berth_cnt"] = len(temp_sh)
        temp_list = []
        for sh_name in sorted(list(temp_sh)):
            number = 1
            temp_dict = {"id": id_sh,
                        "number": number,
                        "berth_letter": sh_name
            }
            number+=1
            id_sh+=1
            temp_list.append(temp_dict)
        docks_list[i_dock]["berth"] = temp_list

    docks["data"].extend(docks_list)  #словарь docks
    # load_json('json_files\\docks.json', docks)
    return docks_list


def get_docks():
    return docks


berth = {}
id_dock = 1
docks_list = []   #все доки
docks_set = set() 
docks =  {"data": []} 