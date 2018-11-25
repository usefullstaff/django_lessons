import psycopg2
import json

import requests
from lxml import html,etree


DB ={'base_name': 'obj_data', 'user_name':'locator' , 'password':'password'}

select_obj_in_squad = """ 
SELECT * FROM obj_locations
WHERE obj_lat BETWEEN {:f} AND {:f}
AND obj_lon BETWEEN {:f} AND {:f};
"""
ip_loactor = 'http://api.geoiplookup.net/?query={}'


def fill_locations_table():
    psql_conn = psycopg2.connect(database = DB['base_name'], user = DB['user_name'], password = DB['password'],  port = "5432")
    cur = psql_conn.cursor()

    data = json.load(open('json_coords.json', encoding="utf8"))
    coords_list = data['features']


    for geo_dict in coords_list:
        obj_name = geo_dict['properties']['name']
        obj_type = geo_dict['properties']['podclass_r']
        obj_lon = geo_dict['geometry']['coordinates'][1]
        obj_lat = geo_dict['geometry']['coordinates'][0]
        obj_osm_id = geo_dict['properties']['osm_id']

        insert_location = "INSERT INTO obj_locations VALUES ({},{},{},{},{})".format ("'"+obj_name.replace("'", "")+"'", "'"+obj_type+"'", obj_lat, obj_lon, obj_osm_id )
        cur.execute(insert_location)         

    psql_conn.commit()
    psql_conn.close()


#fill_locations_table()    
"""
CREATE TABLE cafes(id SERIAL PRIMARY KEY, name TEXT);
SELECT AddGeometryColumn('cafes', 'point', 4326, 'POINT', 2);
-- сразу создаем индекс
CREATE INDEX cafes_idx ON cafes USING gist(point);
-- заполняем данными из OSM
INSERT INTO cafes (name, point)
  SELECT name, ST_Transform(way, 4326)
  FROM planet_osm_point
  WHERE amenity = 'cafe' AND name <> '';

SELECT name, ST_AsEWKT(point) FROM cafes WHERE ST_DWithin(point,ST_GeomFromEWKT('SRID=4326;POINT(27.599893 53.896199)'),0.005);

"""

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



loc_on_ip = vichisly_po_ip('195.222.85.234')
loc_on_browser = {'lat': 53.899263, 'lon': 27.6062208}


create_locations_table(loc_on_ip)

"""
create user locator with password 'password';
create database obj_data owner locator;

grant all privileges on database obj_data to locator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO locator;
GRANT USAGE ON SCHEMA public to locator;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO locator;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO locator;
ALTER ROLE locator WITH Superuser;

CREATE TABLE obj_locations( obj_name VARCHAR, obj_type VARCHAR, obj_lon numeric, obj_lat numeric, obj_osm_id bigint);
"""