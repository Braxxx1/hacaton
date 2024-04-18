
from routes import get_id_routes

id_data = 1
data_list = []
id_id = {}

def get_dock_id(name_dock, letter, data):
    for d in data:
        Name_dock = ''.join(''.join(''.join(d['name'].split()).split('–')).split('-')).lower()
        Name_dock_2 = ''.join(''.join(''.join(name_dock.split()).split('–')).split('-')).lower()
        
        if Name_dock == Name_dock_2:
            dock_id = d['id']

            for sh in d['berth']:
                
                if len(sh['berth_letter']) == len(letter):

                    flag = True
                    for i in range(len(sh['berth_letter'])):
                        if abs(ord(sh['berth_letter'][i].upper()) - ord(letter[i].upper())) in [0, 990, 976, 975]:
                            continue
                        else:
                            flag = False
                    if flag:
                        return [dock_id, sh['number']]   
    return ''                     

    
def get_ship_id(name_ship, owner, data):

    for d in data:
        # print(d['name'], name_ship)
        if d['name'] == name_ship:
            ship_id = d['id']
            Owner = ''.join(d['shipowner']['name'].split('"')).lower()
            owner = ''.join(owner.split('"')).lower()
            if Owner == owner:
                return [ship_id, d['shipowner']['id']]
    return ['','']

def get_ones(df, sheeps_js, dock_js):
    global id_data, data_list
    for index, row in df.iterrows():
        if row[3] == 'СРВ' or row[4] == '-' or row[4] == '':
            continue
        f, f1 = get_ship_id(row[1], row[0], sheeps_js)
        f2 = get_dock_id(row[3], row[4], dock_js)
        if f == '' or f2 == '':
            continue
        d = {
        "id": id_data,
        "status": False,
        "dock_id": get_dock_id(row[3], row[4], dock_js)[0],
        "ship_id": get_ship_id(row[1], row[0], sheeps_js)[0],
        "route_id": None,
        "lot_id": None,
        "trip_id": None,
        "position": {
            "board": 1,
            "number": get_dock_id(row[3], row[4], dock_js)[1],
            "berth_letter": row[4]
        },
        "shipowner_id": get_ship_id(row[1], row[0], sheeps_js)[1],
        "timetable": {
            "start_date": str(row[5]).split()[0],
            "end_date": str(row[5]).split()[0],
            "start_time": 82800,
            "end_time": 83400,
            "duration": None
        },
        "cancel_schedule_id": None,
        "winner_ship_id": None
        }
        data_list.append(d)
        id_data += 1



def get_all(df, id_route, list_name, ships_js, dock_js):
    global id_data, id_id, data_list
    for index, row in df.iterrows():
        if row[3] == '' or row[4] == '':
            continue
        f = get_dock_id(list_name[0], row[7], dock_js)
        if row[5] == '':
            ship_id, owner_id = get_ship_id(row[4], row[3], ships_js)
        else:
            ship_id, owner_id = get_ship_id(row[5], row[3], ships_js)
            
        if f == '' or ship_id == '':
            continue
        
        if (id_route[0], ship_id, owner_id) in id_id:
            d = {
            "id": id_id[(id_route[0], ship_id, owner_id)],
            "status": False if 'не выходит' in row['Комментарий'] else True,
            "dock_id": get_dock_id(list_name[0], row[7], dock_js)[0],
            "ship_id": ship_id,
            "route_id": id_route[0],
            "lot_id": None,
            "trip_id": row[2],
            "position": {
                "board": 1,
                "number": get_dock_id(list_name[0], row[7], dock_js)[1],
                "berth_letter": row[7]
            },
            "shipowner_id": owner_id,
            "timetable": {
                "start_date": None,
                "end_date": None,
                "start_time": None,
                "end_time": None,
                "duration": None
            },
            "cancel_schedule_id": None,
            "winner_ship_id": None
            }
        else:
            id_id[(id_route[0], ship_id, owner_id)] = id_data
            d = {
            "id": id_data,
            "status": False if 'не выходит' in row['Комментарий'] else True,
            "dock_id": get_dock_id(list_name[0], row[7], dock_js)[0],
            "ship_id": ship_id,
            "route_id": id_route[0],
            "lot_id": None,
            "trip_id": row[2],
            "position": {
                "board": 1,
                "number": get_dock_id(list_name[0], row[7], dock_js)[1],
                "berth_letter": row[7]
            },
            "shipowner_id": owner_id,
            "timetable": {
                "start_date": None,
                "end_date": None,
                "start_time": None,
                "end_time": None,
                "duration": None
            },
            "cancel_schedule_id": None,
            "winner_ship_id": None
            }
            id_data += 1
        data_list.append(d)
        

def get_data(df, sheets, list_name, ships_js, dock_js):
    global data_list
   
    
    list_name = [i for i in list_name if i != '']
    if sheets == "РАЗОВЫЕ":
        df["Швартовое место"] = df["Швартовое место"].fillna("")
        df["Новое наименование причала"] = df["Новое наименование причала"].fillna("-")
        get_ones(df, ships_js, dock_js)
    else:
        df.columns.values[5] = "Замена судна"
        df["Замена судна"] = df["Замена судна"].fillna("")
        id_route = get_id_routes(sheets)
        get_all(df, id_route, list_name, ships_js, dock_js)


def get_data_date():
    return data_list

def data_list_null():
    global data_list
    data_list = []