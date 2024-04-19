import pandas as pd


def do_dict(row, column, shipowner):
    global id, data, sl_class, all_ships
    if (row[column], row['Судно']) not in all_ships and row['Судно'] != '':
        all_ships.add((row[column], row['Судно']))
        id += 1
        # print(list(filter(lambda x: x["name"] == row[column], shipowner)), row['Судно'])
    
        
        shipowner_list = list(filter(lambda x: x["name"].lower() == ' '.join(map(lambda z: z.strip(), row[column].strip().split('"'))).strip().lower(), shipowner))
        if len(shipowner_list) != 0:
            shipowner_list = shipowner_list[0]
            return {"id":id, "name": row['Судно'], "class":sl_class,
                "shipowner":{'id': shipowner_list['id'], "name":shipowner_list['name']}, "boat_num": None, "capacity": None, 
                "description": None, "model": None}
        # else:
        #     return {"id":id, "name": row['Судно'], "class":sl_class,
        #         "shipowner":{'id': "", "name": ""}, "boat_num": None, "capacity": None, 
        #         "description": None, "model": None}
    return ''
    

def create_ships(df, owners, column):
    df_no_duplicates = df.drop_duplicates(subset=[column, "Судно"])
    df_no_duplicates["Судно"] = df["Судно"].fillna("")
    for _, row in df_no_duplicates.iterrows():
        to_add = do_dict(row, column, owners)
        if to_add != '':
            data["data"].append(to_add)
    return data['data']
        

def get_data_sheeps():
    return data


data = {'data':[]}
id = 0
sl_class = {'id': 1, "name": "Пассажирский флот", "code": "pass"}
all_ships = set()
