
import requests
import re
from math import radians, cos, sin, asin, sqrt

from lxml import html,etree

import psycopg2
DB ={'base_name': 'obj_data', 'user_name':'locator' , 'password':'password'}


req_to_yandex_api = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}&results=1'
select_obj_in_squad = """ 
SELECT * FROM obj_locations
WHERE obj_lat BETWEEN {:f} AND {:f}
AND obj_lon BETWEEN {:f} AND {:f};
"""
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



ip_loactor = 'http://api.geoiplookup.net/?query={}'


def vichisly_po_ip(client_ip):
    request = requests.get(ip_loactor.format(client_ip))
    req_string = html.fromstring(request.text.encode('utf-8'))
    coords = req_string.find('results').find('result')
    lat = float(coords.find('latitude').text)
    lon = float(coords.find('longitude').text)

    return {'lat':lat,'lon':lon }


def create_locations_table(client_coords):
    psql_conn = psycopg2.connect(database = DB['base_name'], user = DB['user_name'], password = DB['password'],  port = "5432")
    cur = psql_conn.cursor()

    objects_in_squad = select_obj_in_squad.format(client_coords['lat']-0.01, client_coords['lat']+0.01, client_coords['lon']-0.01, client_coords['lon']+0.01) 

    cur.execute(objects_in_squad)
    return(len(cur.fetchall()))