import pandas as pd
import datetime


def get_lots(df, sheet, points, id_fic):
    global id_lots, active_main, trip_id, travel_time, set_lots, set_sheet, ficst_id
    points = list(map(lambda x: x.lower().strip(), points))
    unic_lots = tuple(filter(lambda x: x != 19091, sorted(df['Лот'].fillna(19091).unique())))
    changer = {'Парка Горького':"Парк Горького", 'Третьяковского':"Третьяковский",
               'Андреевского':"Андреевский", 'Коломенской':"Коломенское",
               'Нескучного сада':"Нескучный сад", "Китай-города": "Китай-город",
               "Патриаршего":"Патриарший", "Зарядья":"Зарядье", 'Киевской':'Киевский'}#, "Новоспасский":"Новоспасский"}
    lots = []
    temp_lots = []
    df['Комментарий'] = df['Комментарий'].fillna("")
    for i in unic_lots:
        new_dict = {"id": id_lots, "name":str(i), "active":False,
                    "trips":[]}
        temp_new_dict = {"name":str(i), "active":False,
                            "trips":[]}
        for ind, row in df[df['Лот'] == i].iterrows():
            act = False
            if "не выходит" not in row['Комментарий'] and row['Комментарий'] != "":
                act = True
                new_dict["active"] = True
                temp_new_dict["active"] = True
                active_main = True
                spliting = row['Комментарий'].split()
                if len(spliting) == 3:
                    list_ = list(zip(row['Подход'], row['Отход']))
                    for i in range(len(list_)):
                        new_sp = []
                        for x in list_[i]:
                            if isinstance(x, datetime.datetime):
                                new_sp.append(x.time())
                            else:
                                new_sp.append(x)
                        list_[i] = new_sp
                    list_ = list(map(lambda x:
                        (datetime.datetime.combine(datetime.date.today(), x[1]) - datetime.datetime.combine(datetime.date.today(), x[0])).total_seconds(), list_))       
                    travel_time += sum([i if i > 0 else 86400 + i for i in list_])               
                elif len(spliting) > 3:
                    spliting = spliting[3:]
                    if len(spliting) > 2:
                        spliting = [spliting[0], ' '.join(spliting[1:])]
                    if spliting[-1] in changer:
                        spliting[-1] = changer[spliting[-1]]
                    try:
                        list_ = list(zip(row['Подход'], row['Отход']))
                        if spliting[0] == "до":                     
                            list_ = list_[:points.index(spliting[1].lower()) + 1]
                        elif spliting[0] == 'с':
                            list_ = list_[points.index(spliting[1].lower()):]
                        elif spliting[0] == "кроме":
                            list_ = list_[:points.index(spliting[1].lower())] + list_[points.index(spliting[1].lower()) + 1:]
                        for i in range(len(list_)):
                            new_sp = []
                            for x in list_[i]:
                                if isinstance(x, datetime.datetime):
                                    new_sp.append(x.time())
                                else:
                                    new_sp.append(x)
                            list_[i] = new_sp
                        list_ = list(map(lambda x:
                            (datetime.datetime.combine(datetime.date.today(), x[1]) - datetime.datetime.combine(datetime.date.today(), x[0])).total_seconds(), list_))       
                        travel_time += sum([i if i > 0 else 86400 + i for i in list_])
                    except ValueError as e:
                        print("GOGO")
            trips_dict = {"id":trip_id, "name":str(row['Рейс']), "active":act}
            temp_trips_dict = {"name":str(row['Рейс']), "active":act}
            new_dict["trips"].append(trips_dict)
            temp_new_dict["trips"].append(temp_trips_dict)
            trip_id += 1
        lots.append(new_dict)
        temp_lots.append(temp_new_dict)
        id_lots += 1
    
    if temp_lots in set_lots and sheet in set_sheet:
        ficst_id = set_lots.index(temp_lots)
        return '-'
    set_lots.append(temp_lots)
    set_sheet.add(sheet)
    return lots        


def get_points(points, docs, sequense, direction):
    global points_id
    docs = [(i['id'], i['name']) for i in docs]
    points_dict = []
    for i in points:
        get_id = list(filter(lambda x: x[1] == i, docs))
        if len(get_id) != 0:
            new_dict = {"id": points_id, "sequence":sequense, "direction": direction,
                    "dock":{"id": get_id[0][0], "name":get_id[0][1]}}
        points_dict.append(new_dict)
        sequense += 1
        points_id += 1
    return points_dict


def create_routes_json(df, marshrut, sheet, docs):
    global id, active_main, travel_time, ficst_id
    travel_time = 0
    active_main = False
    sequence = 1
    direction = 1
    ficst_id = 0
    points = [i for i in marshrut if i != '']
    lots = get_lots(df, sheet, points, id)
    if lots != '-':
        data["data"].append({"id":id, "name":sheet, "short_name":None, "active":active_main,
                            "type":{"id":7, "name":"Прогулочный"},
                            "travel_time": int(travel_time),
                            "lots": lots,
                            "points":get_points(points, docs, sequence, direction),
                            "color": None})
        set_id_routes.append({sheet:[id, active_main]}) 
        id += 1         


def get_data_routes():
    return data

def get_id_routes(sheet):
    if ficst_id == 0:
        return set_id_routes[-1][sheet]
    return set_id_routes[ficst_id][sheet]
    # return [1, 1]
    

data = {'data':[]}
set_lots = []
set_sheet = set()
set_id_routes = []
id = 1
id_lots = 1
trip_id = 1
points_id = 1
active_main = False
travel_time = 0
ficst_id = 0