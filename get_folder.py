import requests
from urllib.parse import urlencode

def get_public_folder_files(public_folder_url):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
    files = []

    offset = 0
    limit = 20  # Максимальное количество элементов, возвращаемых API за один запрос

    while True:
        final_url = f"{base_url}{urlencode(dict(public_key=public_folder_url, limit=limit, offset=offset))}"
        response = requests.get(final_url)
        if response.status_code == 200:
            data = response.json()['_embedded']['items']
            files.extend(data)
            offset += limit
            if len(data) < limit:
                break  # Если количество полученных файлов меньше лимита, это последняя порция файлов
        else:
            print("Failed to fetch files")
            break

    return files
