
import requests
import re
from math import radians, cos, sin, asin, sqrt

req_to_yandex_api = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}&results=1'

def convert_adres(adres):
    clear_adres = re.sub(r'\([^()]*\)', '', adres)
    request = requests.get(req_to_yandex_api.format(clear_adres))
    if request.status_code == 200:
        req = request.json()
        if len(req['response']['GeoObjectCollection']['featureMember']) != 0:
            geo_dict = req['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')   

            result = {'longitude':float(geo_dict[0]), 'latitude':float(geo_dict[1])}
        else:
            result = {'longitude':None, 'latitude':None}

        return result
    else:
        return conect_error_message.format(request.status_code)
    pass



def haversine(lat1, lon1,  lat2, lon2):
    """
    Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
    https://en.wikipedia.org/wiki/Haversine_formula
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return round(km, 2)
    pass


