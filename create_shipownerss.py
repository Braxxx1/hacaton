import pandas as pd


def do_dict(name):
    global id, data, add_owners
    name1 = ''.join(name.strip().split('"')).lower()
    if name1.strip().lower() not in add_owners and name != '':
        id += 1
        add_owners.add(name1.strip().lower())
        return {"id": id, "name":name, "inn":None, "ogrn":None, "contacts":None, "url":None}
    return ''


def create_shipowners(df, column):
    global data
    df = df[column].unique()  
    df = list(map(do_dict, df))
    data["data"].extend(filter(lambda x: x != '', df))
    return data['data']


def get_data_owners():
    return data


data = {'data':[]}
add_owners = set()
id = 0

