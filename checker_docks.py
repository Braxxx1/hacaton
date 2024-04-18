import pandas as pd
from get_folder import get_public_folder_files


def check_ones(df):
    global set_docks
    df = [' '.join(i.strip().lower().split("-")) for i in df if i != '' and i.strip().lower() != 'срв']
    set_docks = set_docks.union(set(df))


def check_docks(df):
    global set_docks
    marshrut = df.iloc[0].fillna("")
    points = [' '.join(i.strip().lower().split("-")) for i in marshrut if i != '' and i.strip().lower() != 'срв']
    set_docks = set_docks.union(set(points))

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
        check_docks(df)
    df = pd.read_excel(file['file'], sheet_name="РАЗОВЫЕ")
    df["Новое наименование причала"] = df["Новое наименование причала"].fillna("")
    check_ones(df["Новое наименование причала"].unique())
    print(len(set_docks))

print(set_docks)